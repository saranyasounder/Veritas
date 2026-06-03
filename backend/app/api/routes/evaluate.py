from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from app.models.openrouter import OpenRouterModel
from app.evaluator.pipeline import EvaluationPipeline
from app.metrics.lexical import BLEUMetric, ROUGEMetric
from app.metrics.semantic import BERTScoreMetric, CosineSimilarityMetric
from app.metrics.hallucination import HallucinationMetric
from app.database.repository import EvaluationRepository
from app.database.session import get_db
from app.utils.search import search_source
from app.utils.reference import generate_reference
from app.core.logger import get_logger

# module level logger for tracking all evaluation requests
logger = get_logger(__name__)

# router groups all evaluation endpoints under /api prefix
router = APIRouter()


class EvaluateRequest(BaseModel):
    """
    Request body for the evaluate endpoint.
    model_id follows OpenRouter format e.g. 'openai/gpt-3.5-turbo'
    reference and source are optional — if not provided:
      - reference is auto-generated using GPT-4o
      - source is auto-fetched from the web using Tavily
    """
    prompt: str                      # the question or input to evaluate
    model_id: str                    # which model to evaluate
    reference: Optional[str] = None  # expected answer — auto-generated if not provided
    source: Optional[str] = None     # source document — auto-fetched if not provided


@router.post("/evaluate")
def evaluate(request: EvaluateRequest, db: Session = Depends(get_db)):
    """
    Runs a full evaluation cycle for a single prompt.

    Flow:
      1. Initialize model and metrics
      2. Auto-fetch source via Tavily if not provided
      3. Auto-generate reference via GPT-4o if not provided
      4. Run evaluation pipeline — generates response and scores it
      5. Save result to database
      6. Return structured result to frontend

    Returns:
        EvaluationResult containing response, all metric scores, and timestamp

    Raises:
        HTTPException 500: if model generation or any metric fails
    """
    logger.info(f"Evaluation request received | model={request.model_id}")

    # initialize model with the requested model id
    # OpenRouterModel handles all models through one unified client
    model = OpenRouterModel(model_id=request.model_id)

    # initialize all metrics — new instances per request
    # ensures no state bleeds between concurrent requests
    metrics = [
        BLEUMetric(),             # word overlap — precision focused
        ROUGEMetric(),            # word overlap — recall focused
        BERTScoreMetric(),        # semantic similarity using embeddings
        CosineSimilarityMetric(), # cosine distance between embeddings
        HallucinationMetric()     # checks if response is grounded in source
    ]

    # pipeline orchestrates model generation and metric scoring
    evaluation_pipeline = EvaluationPipeline(model=model, metrics=metrics)

    # auto fetch source document using Tavily if not provided by user
    # source is used by HallucinationMetric to verify factual grounding
    if not request.source:
        logger.info("No source provided — fetching from Tavily")
        auto_source = search_source(request.prompt)
    else:
        auto_source = request.source

    # auto generate reference answer using GPT-4o if not provided by user
    # reference is used by BLEU, ROUGE, BERTScore, and CosineSimilarity
    # GPT-4o acts as ground truth — its answer is the benchmark
    if not request.reference:
        logger.info("No reference provided — generating with GPT-4o")
        auto_reference = generate_reference(request.prompt)
    else:
        auto_reference = request.reference

    # run full evaluation pipeline
    try:
        result = evaluation_pipeline.evaluate(
            prompt=request.prompt,
            reference=auto_reference,  # auto-generated or user-provided
            source=auto_source         # auto-fetched or user-provided
        )
    except Exception as e:
        logger.error(f"Evaluation failed | model={request.model_id} | error={str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    # persist result to database for historical tracking and dashboard display
    # non-blocking — if save fails, user still gets their result
    try:
        repo = EvaluationRepository(db)
        repo.save_evaluation(result)
        logger.info(f"Evaluation saved | model={request.model_id}")
    except Exception as e:
        logger.error(f"Failed to save evaluation | error={str(e)}")

    logger.info(f"Evaluation complete | model={request.model_id}")
    return result