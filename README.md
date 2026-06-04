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

The backend runs at http://localhost:8000 and API docs are available at http://localhost:8000/docs

### Frontend setup

```bash
cd frontend
npm install
npm run dev
```

The frontend runs at http://localhost:5173

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

### GET /api/results

Returns all evaluations ordered by most recent first.

### GET /api/results/{model_id}

Returns all evaluations for a specific model.

---

## Deployment

### Backend on Render

1. Go to render.com and create a new Web Service
2. Connect your GitHub repository
3. Set Root Directory to backend
4. Set Build Command to pip install -r requirements.txt
5. Set Start Command to uvicorn app.main:app --host 0.0.0.0 --port $PORT
6. Add your environment variables

### Database on Supabase

1. Create a new project on supabase.com
2. Go to Settings then Database and copy the connection string
3. Add it as DATABASE_URL in your Render environment variables

### Frontend on Vercel

1. Go to vercel.com and import your GitHub repository
2. Set Framework to Vite
3. Set Root Directory to frontend
4. Add environment variable VITE_API_URL pointing to your Render backend URL

---

## Inspiration

This project was inspired by manual LLM evaluation work done during AI research at Star Lab at Oregon State University, where evaluating French-English translation model outputs was done entirely by hand. Veritas automates that evaluation loop at scale.

---

## License

MIT

---

Built by Saranya Sounder Rajan
