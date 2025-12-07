from pydantic import BaseModel
from typing import List, Optional

class ChapterOutline(BaseModel):
    title: str
    description: str

class BookSpecification(BaseModel):
    title: str
    topic: str
    target_audience: str
    chapters: List[ChapterOutline]

class ChatRequest(BaseModel):
    messages: List[dict] # {role: str, content: str}
    context_text: Optional[str] = None # Selected text from the UI
