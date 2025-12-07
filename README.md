# AI-Driven Book Creator & RAG Chatbot

An intelligent platform that generates technical books using local AI (Ollama/Qwen) and provides an interactive RAG (Retrieval-Augmented Generation) Chatbot for readers to ask questions about the content.

## 🚀 Features

*   **AI Book Generation**: Create structured books with chapters, titles, and target audiences using **Qwen (via Ollama)**.
*   **Interactive RAG Chatbot**: Chat with your book! Ask questions and get answers based *only* on the book's content using **OpenAI Agents**, **Qdrant**, and **Neon Postgres**.
*   **Context-Aware**: Select any text in the book to "Ask AI" specific questions about that paragraph.
*   **Book Management**: Dashboard to view and manage your generated library.
*   **Modern UI**: Built with **Docusaurus** for a beautiful reading experience.

## 🛠️ Tech Stack

*   **Frontend**: React (Docusaurus)
*   **Backend**: Python (FastAPI)
*   **AI Models**: 
    *   Generation: Qwen 2.5 (Local via Ollama)
    *   Chat/Embeddings: OpenAI GPT-4o & text-embedding-3
*   **Database**: 
    *   Vector Store: Qdrant Cloud
    *   Metadata/History: Neon Serverless Postgres
*   **ORM**: SQLModel

## 📋 Prerequisites

*   **Node.js** (v18+)
*   **Python** (v3.10+)
*   **Ollama**: Installed and running locally.
    *   Run `ollama pull qwen2.5` (or your preferred model).

## ⚙️ Setup

### 1. External Services
Ensure you have the following API keys/URLs:
*   **OpenAI API Key** (`OPENAI_API_KEY`)
*   **Qdrant Cloud** (`QDRANT_URL`, `QDRANT_KEY`)
*   **Neon Postgres** (`DATABASE_URL`)

### 2. Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the root `Books/` directory (or export variables):
```env
OLLAMA_BASE_URL=http://localhost:11434
OPENAI_API_KEY=sk-...
QDRANT_URL=https://...
QDRANT_KEY=...
DATABASE_URL=postgresql://user:pass@ep-xyz.aws.neon.tech/dbname?sslmode=require
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

## ▶️ Running the Project

### Start Backend
Run the helper script from the root directory:
```bash
./start_backend.sh
```
*Runs on http://localhost:8000*

### Start Frontend
In a separate terminal:
```bash
cd frontend
npm start
```
*Runs on http://localhost:3000*

## 📖 Usage

### 1. Create a Book
*   Navigate to **Create Book** in the top navigation.
*   Enter a **Title** (e.g., "The Future of AI"), **Topic**, and **Target Audience**.
*   Click **Start Generation**. The AI will write chapters in the background.

### 2. Read & Manage
*   Go to **My Books** to see your library.
*   Click **Read Book** to view the generated Markdown pages.

### 3. Chat with the Book
*   Click the **💬 AI Chat** bubble in the bottom right.
*   Ask questions like "What is this chapter about?".
*   **Power User Feature**: Highlight any text on the page, and the chat widget will automatically use it as context ("Using selection...").

## 📄 License
MIT
