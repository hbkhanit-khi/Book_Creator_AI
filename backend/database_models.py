from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    topic: str
    target_audience: str
    
    # We could link to chapters here if we spread them to DB
    # But for now, this tracks the high-level book concept.

class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str
    content: str
    timestamp: str 
