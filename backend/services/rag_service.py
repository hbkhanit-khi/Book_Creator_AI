import os
import uuid
from typing import List, Dict
from fastapi import APIRouter, HTTPException
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels
from sqlmodel import Field, SQLModel, Session, select
from ..models import ChatRequest
from ..database import engine, create_db_and_tables
from .ai_service import get_embeddings, openai_client

# DB Model
class ChatMessage(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    role: str
    content: str
    timestamp: str # Simplified for now

router = APIRouter(prefix="/rag", tags=["rag"])

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_KEY = os.getenv("QDRANT_KEY")

# Initialize Qdrant
# Note: In production, do this in lifespan context or a singleton
try:
    if "localhost" in QDRANT_URL or "127.0.0.1" in QDRANT_URL:
         q_client = QdrantClient(url=QDRANT_URL)
    else:
         q_client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_KEY)
except:
    q_client = None # Handle gracefully if not available yet

COLLECTION_NAME = "book_content"

# Ensure collection exists
if q_client:
    try:
        q_client.get_collection(COLLECTION_NAME)
    except:
        q_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=qmodels.VectorParams(size=1536, distance=qmodels.Distance.COSINE),
        )

async def index_book_file(file_path: str, content: str):
    """Chunks content and uploads to Qdrant."""
    if not q_client:
        print("Qdrant client not initialized, skipping indexing.")
        return

    # Simple chunking by paragraphs or sentences
    # Refinement needed for production (overlap, recursive splitter)
    chunks = [c.strip() for c in content.split('\n\n') if len(c.strip()) > 50]
    
    points = []
    for chunk in chunks:
        vector = await get_embeddings(chunk)
        points.append(qmodels.PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={"text": chunk, "source": os.path.basename(file_path)}
        ))
        
    if points:
        q_client.upsert(
            collection_name=COLLECTION_NAME,
            points=points
        )
        print(f"Indexed {len(points)} chunks for {file_path}")

@router.post("/chat")
async def chat(request: ChatRequest):
    if not openai_client:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        
    user_query = request.messages[-1]['content']
    
    context_parts = []
    
    # 1. If user selected text, that is high priority context
    if request.context_text:
        context_parts.append(f"User Selected Text:\n{request.context_text}")
        
    # 2. Retrieve from Qdrant
    if q_client:
        query_vector = await get_embeddings(user_query)
        search_result = q_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=3
        )
        for hit in search_result:
            context_parts.append(f"Retrieved Context:\n{hit.payload['text']}")
            
    full_system_prompt = "You are a helpful assistant answering questions about the current book."
    if context_parts:
        full_system_prompt += "\n\nUse the following context to answer:\n" + "\n---\n".join(context_parts)
    
    # Construct messages for OpenAI
    api_messages = [{"role": "system", "content": full_system_prompt}]
    # We might want to pass history, but for now just the last query + system context
    api_messages.append({"role": "user", "content": user_query})
    
    # Save User Message to DB
    if engine:
        with Session(engine) as session:
            session.add(ChatMessage(role="user", content=user_query, timestamp=str(uuid.uuid4())))
            session.commit()

    response = await openai_client.chat.completions.create(
        model="gpt-4o", # or gpt-3.5-turbo
        messages=api_messages
    )
    
    bot_reply = response.choices[0].message.content
    
    # Save Assistant Message to DB
    if engine:
        with Session(engine) as session:
            session.add(ChatMessage(role="assistant", content=bot_reply, timestamp=str(uuid.uuid4())))
            session.commit()
    
    return {"reply": bot_reply}
