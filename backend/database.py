import os
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = os.getenv("DATABASE_URL") # postgresql://user:password@host/dbname

# Use synchronous engine for simplicity with SQLModel, or async if advanced
engine = None
if DATABASE_URL:
    engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    if engine:
        SQLModel.metadata.create_all(engine)

def get_session():
    if not engine:
        return None
    with Session(engine) as session:
        yield session
