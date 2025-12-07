#!/bin/bash
source venv/bin/activate
export OLLAMA_BASE_URL="http://localhost:11434"
# Export other keys here if needed, or rely on .env
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
