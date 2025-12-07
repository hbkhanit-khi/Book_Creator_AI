import os
import httpx
from openai import AsyncOpenAI

# OLLAMA CONFIG
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = "qwen2.5:latest" # or just 'qwen'

# OPENAI CONFIG
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai_client = None
if OPENAI_API_KEY:
    openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def generate_book_content(prompt: str) -> str:
    """Generates content using Ollama (Qwen)."""
    async with httpx.AsyncClient() as client:
        # This is a simplified call to Ollama's generate endpoint
        # In production, we might want to use the /api/chat endpoint if qwen expects chat format
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = await client.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=300.0)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except Exception as e:
            print(f"Error calling Ollama: {e}")
            return f"Error generating content: {str(e)}"

async def get_embeddings(text: str) -> list[float]:
    """Generates embeddings using OpenAI."""
    if not openai_client:
        raise ValueError("OPENAI_API_KEY not set")
    
    response = await openai_client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding
