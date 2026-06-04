---

## Getting Started

### Prerequisites

- Python 3.13+
- Node.js 20+
- PostgreSQL 15+
- API keys: OpenRouter, Tavily

### 1. Clone the repository

```bash
git clone https://github.com/saranyasounder/Veritas.git
cd Veritas
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `backend/.env`:

```env
OPENROUTER_API_KEY=your_openrouter_key
TAVILY_API_KEY=your_tavily_key
DATABASE_URL=postgresql://postgres:password@localhost:5432/veritas
REDIS_URL=redis://localhost:6379
```

Create the database:

```bash
psql postgres
CREATE DATABASE veritas;
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173`

### 4. Docker

```bash
docker-compose up
```

---

## API Reference

### POST /api/evaluate

Run a full evaluation for a single prompt.

**Request body:**
```json
{
  "prompt": "What is machine learning?",
  "model_id": "openai/gpt-3.5-turbo",
  "reference": null,
  "source": null
}
```

If `reference` is null — GPT-4o auto-generates it.
If `source` is null — Tavily auto-fetches it.

**Response:**
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

## Deployment

### Backend — Render

1. New Web Service → connect GitHub repo
2. Root Directory: `backend`
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

### Database — Supabase

1. New Project → copy connection string from Settings → Database
2. Add as `DATABASE_URL` in Render environment variables

### Frontend — Vercel

1. Import GitHub repo
2. Framework: Vite
3. Root Directory: `frontend`
4. Add environment variable: `VITE_API_URL=your_render_backend_url`

---

## Inspiration

This project was inspired by manual LLM evaluation work done during AI research at Star Lab (Oregon State University), where evaluating French-English translation model outputs was done by hand. Veritas automates that evaluation loop at scale.

---

## License

MIT

---

<p align="center">Built by <a href="https://github.com/saranyasounder">Saranya Sounder Rajan</a></p>
