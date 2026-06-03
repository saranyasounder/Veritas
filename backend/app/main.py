from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import evaluate, results
from app.database.models import Base
from app.database.session import engine
from app.core.logger import get_logger

logger = get_logger(__name__)

# create FastAPI app first — everything else depends on this
app = FastAPI(
    title="Veritas",
    description="LLM Evaluation and Benchmarking Platform",
    version="1.0.0"
)

# allow React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register all routers under /api prefix
# evaluate.py routes become /api/evaluate
# results.py routes become /api/results
app.include_router(evaluate.router, prefix="/api")
app.include_router(results.router, prefix="/api")

@app.on_event("startup")
def startup():
    """
    Runs when the server starts.
    Creates all database tables if they don't exist.
    Safe to run multiple times — won't recreate existing tables.
    """
    logger.info("Starting Veritas — creating database tables")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ready")

@app.get("/")
def root():
    return {
        "name": "Veritas",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}