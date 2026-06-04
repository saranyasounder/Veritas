# Veritas

> LLM Evaluation and Benchmarking Platform

---

## Screenshots

![Evaluate Page](assets/EvalImage1.png)

![Evaluation Scores](assets/EvalImage2.png)

---

## What is Veritas

Veritas is a full-stack LLM evaluation and benchmarking platform that automatically measures the quality of AI-generated responses across multiple dimensions. Unlike single-metric tools, Veritas combines traditional NLP metrics, embedding-based semantic evaluation, retrieval-based hallucination detection, and LLM-as-a-Judge scoring to give a complete picture of model performance.

Built for ML engineers, AI researchers, and data scientists who need a systematic and reproducible way to evaluate and compare foundation models.

---

## Evaluation Pipeline

```
                        +------------------+
                        |   User Prompt    |
                        +--------+---------+
                                 |
              +------------------+------------------+
              |                                     |
    +---------v---------+               +-----------v---------+
    |   Tavily Search   |               |  GPT-4o Reference   |
    |  Auto-fetch web   |               |  Auto-generate the  |
    |  source document  |               |  ideal answer       |
    +---------+---------+               +-----------+---------+
              |                                     |
              +------------------+------------------+
                                 |
                        +--------v---------+
                        |  OpenRouter LLM  |
                        |  Generate model  |
                        |  response        |
                        +--------+---------+
                                 |
         +-----------+-----------+-----------+-----------+
         |           |           |           |           |
    +----v----+ +----v----+ +----v----+ +----v----+ +----v----+
    |  BLEU   | |  ROUGE  | |  BERT   | | Cosine  | | Halluc  |
    |  Score  | |  Score  | |  Score  | |  Sim    | | ination |
    +---------+ +---------+ +---------+ +---------+ +---------+
         |           |           |           |           |
         +-----------+-----------+-----------+-----------+
                                 |
                        +--------v---------+
                        |   PostgreSQL DB  |
                        |   Save results   |
                        +--------+---------+
                                 |
                        +--------v---------+
                        |    Dashboard     |
                        |   View history   |
                        +------------------+
```

---

## Features

- Multi-model evaluation across GPT, Claude, Gemini, Llama, and Mistral through a single unified API
- Five evaluation metrics including BLEU, ROUGE, BERTScore, Cosine Similarity, and Hallucination Detection
- Auto source fetching via Tavily that searches the web for relevant source documents automatically
- Auto reference generation via GPT-4o that generates an ideal reference answer automatically
- LLM-as-a-Judge that uses a second LLM to evaluate response quality across helpfulness, relevance, correctness, completeness, and conciseness
- Evaluation history with all results persisted to PostgreSQL and viewable in the dashboard
- Production-grade architecture that is modular and containerized with logging, error handling, and dependency injection throughout
- Dark mode React frontend with animated glass-card design and score visualizations
- Toggle controls to switch between auto and manual source and reference input

---

## Evaluation Metrics

| Metric | Type | What it measures | Auto input |
|--------|------|-----------------|------------|
| BLEU | Lexical | Word overlap precision between response and reference | GPT-4o generates reference |
| ROUGE | Lexical | Word overlap recall between response and reference | GPT-4o generates reference |
| BERTScore | Semantic | Meaning similarity using transformer embeddings | GPT-4o generates reference |
| Cosine Similarity | Semantic | Embedding distance between response and reference | GPT-4o generates reference |
| Hallucination | Retrieval | Whether response is grounded in source document | Tavily fetches source |

---

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy and PostgreSQL
- Pydantic for settings and validation
- OpenRouter for unified LLM access
- Hugging Face Transformers for BERTScore and sentence embeddings
- Tavily for web search and auto source fetching
- Docker

### Frontend
- React 18
- Tailwind CSS
- Axios
- React Router

---

## Project Structure

```
veritas/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── evaluate.py
│   │   │       └── results.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── logger.py
│   │   ├── database/
│   │   │   ├── models.py
│   │   │   ├── repository.py
│   │   │   └── session.py
│   │   ├── evaluator/
│   │   │   ├── pipeline.py
│   │   │   └── judge.py
│   │   ├── metrics/
│   │   │   ├── base.py
│   │   │   ├── lexical.py
│   │   │   ├── semantic.py
│   │   │   └── hallucination.py
│   │   ├── models/
│   │   │   ├── base.py
│   │   │   └── openrouter.py
│   │   └── utils/
│   │       ├── search.py
│   │       └── reference.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Evaluate.jsx
│   │   │   └── Results.jsx
│   │   ├── components/
│   │   │   └── shared/
│   │   │       ├── Navbar.jsx
│   │   │       └── LoadingSpinner.jsx
│   │   └── services/
│   │       └── api.js
│   └── package.json
├── assets/
│   ├── EvalImage1.png
│   └── EvalImage2.png
├── docker-compose.yml
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.13 or higher
- Node.js 20 or higher
- PostgreSQL 15 or higher
- OpenRouter API key from openrouter.ai
- Tavily API key from app.tavily.com

### Clone the repository

```bash
git clone https://github.com/saranyasounder/Veritas.git
cd Veritas
```

### Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a file called .env inside the backend folder:

```
OPENROUTER_API_KEY=your_openrouter_key
TAVILY_API_KEY=your_tavily_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/veritas
REDIS_URL=redis://localhost:6379
```

Create the database:

```bash
psql postgres
CREATE DATABASE veritas;
\q
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at http://localhost:8000 and API docs at http://localhost:8000/docs

### Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:5173

### Docker

```bash
docker-compose up
```

---

## API Reference

### POST /api/evaluate

Run a full evaluation for a single prompt.

Request body:

```json
{
  "prompt": "What is machine learning?",
  "model_id": "openai/gpt-3.5-turbo",
  "reference": null,
  "source": null
}
```

If reference is null, GPT-4o auto-generates it. If source is null, Tavily auto-fetches it.

Response:

```json
{
  "prompt": "What is machine learning?",
  "model": "openai/gpt-3.5-turbo",
  "response": "Machine learning is...",
  "metrics": {
    "BLEU": { "score": 0.03, "passed": null, "details": null },
    "ROUGE": { "score": 0.43, "passed": null, "details": { "rouge1": 0.43, "rouge2": 0.24, "rougeL": 0.28 } },
    "BERTScore": { "score": 0.84, "passed": null, "details": { "precision": 0.88, "recall": 0.96, "f1": 0.84 } },
    "CosineSimilarity": { "score": 0.69, "passed": null, "details": null },
    "Hallucination": { "score": 0.74, "passed": true, "details": { "threshold": 0.5, "hallucination_detected": false } }
  },
  "timestamp": "2026-06-03T14:00:00"
}
```

### GET /api/results

Returns all evaluations ordered by most recent first.

### GET /api/results/{model_id}

Returns all evaluations for a specific model.

---

## Inspiration

This project was inspired by manual LLM evaluation work done during AI research at Star Lab at Oregon State University, where evaluating French-English translation model outputs was done entirely by hand. Veritas automates that evaluation loop at scale.

---

Built by Saranya Sounder Rajan
