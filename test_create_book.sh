curl -X POST "http://localhost:8000/book/create" \
-H "Content-Type: application/json" \
-d '{
  "title": "The Future of AI Agents",
  "topic": "Artificial Intelligence",
  "target_audience": "Developers and Tech Enthusiasts",
  "chapters": [
    {
      "title": "Introduction to Agents",
      "description": "What are AI agents and how do they differ from simple LLMs?"
    },
    {
      "title": "Building your first Agent",
      "description": "A step-by-step guide to using LangChain or similar tools."
    }
  ]
}'
