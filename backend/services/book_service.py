import os
import asyncio
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlmodel import Session, select
from ..models import BookSpecification, ChapterOutline
from ..database import get_session
from ..database_models import Book
from .ai_service import generate_book_content
from .rag_service import index_book_file

router = APIRouter(prefix="/book", tags=["book"])

DOCS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/docs"))

async def generate_chapter_task(chapter: ChapterOutline, book_title: str, topic: str, audience: str, order: int):
    prompt = f"""
    Write a chapter titled '{chapter.title}' for a book about '{topic}' titled '{book_title}'.
    Target Audience: {audience}
    Chapter Description: {chapter.description}
    
    Format the output as Markdown. 
    Use headers (##) for sections. 
    Write typically 1000-2000 words.
    Do not include the book title as H1, just start with the chapter content.
    """
    
    content = await generate_book_content(prompt)
    
    # Add metadata for Docusaurus
    full_content = f"""---
sidebar_position: {order}
---

# {chapter.title}

{content}
"""
    
    # Sanitize filename
    filename = "".join(x for x in chapter.title if x.isalnum() or x in " -_").strip().replace(" ", "-").lower() + ".md"
    file_path = os.path.join(DOCS_PATH, filename)
    
    os.makedirs(DOCS_PATH, exist_ok=True)
    with open(file_path, "w") as f:
        f.write(full_content)
        
    # Index for RAG
    # We await this because it might be quick, or we could spawn another task.
    # For now, let's just await it to ensure consistency.
    await index_book_file(file_path, content)

@router.post("/create")
async def create_book(spec: BookSpecification, background_tasks: BackgroundTasks, session: Session = Depends(get_session)):
    
    # 1. Save to DB
    new_book = Book(title=spec.title, topic=spec.topic, target_audience=spec.target_audience)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    
    # Determine execution strategy: Serial or Parallel?
    # Parallel might overwhelm local Ollama if not careful, but let's try 1 by 1 for stability or small batches.
    # For this implementation, we'll queue them as background tasks.
    
    for i, chapter in enumerate(spec.chapters, start=1):
        background_tasks.add_task(
            generate_chapter_task, 
            chapter, spec.title, spec.topic, spec.target_audience, i
        )
        
    return {"status": "processing", "message": f"Started generation of {len(spec.chapters)} chapters.", "book_id": new_book.id}

@router.get("/list")
async def list_books(session: Session = Depends(get_session)):
    books = session.exec(select(Book)).all()
    # Simple mapping to link to Docusaurus (assuming first chapter follows valid link)
    # Refinement needed: Store slug in DB
    result = []
    for b in books:
        # Heuristic for link: docs/<first-chapter-ish-slug> or just /docs/intro if unknown
        # Since we don't store slugs yet, we'll point to docs root or generic
        result.append({
            "id": b.id,
            "title": b.title,
            "topic": b.topic,
            "audience": b.target_audience,
            "link": "/docs/intro" # Placeholder
        })
    return result
