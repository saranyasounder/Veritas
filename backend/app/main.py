from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Veritas",
    description = "LLM Evaluation and Benchmarking Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # only allow requests from React
    allow_credentials=True ,                  # allow cookies and auth headers
    allow_methods=["*"] ,                     # allow GET, POST, PUT, DELETE etc
    allow_headers=["*"] ,                     # allow any headers
)

@app.get("/")
def root():
    return {
        "name": "Veritas",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}