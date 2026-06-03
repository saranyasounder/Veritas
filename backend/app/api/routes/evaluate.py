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
from app.core.logger import get_logger

# module level logger for tracking all evaluation requests
logger = get_logger(__name__)

# router groups all evaluation endpoints under one prefix
# registered in main.py with prefix='/api'
router = APIRouter()

class EvaluateRequest(BaseModel):
    """
    Request body for the evaluate endpoint.
    model_id follows OpenRouter format e.g. 'anthropic/claude-sonnet-4'
    reference and source are optional — metrics that need them
    will skip gracefully if not provided.
    """
    prompt: str                      # the question or input to evaluate
    model_id: str                    # which model to evaluate
    reference: Optional[str] = None  # expected answer for BLEU, ROUGE, BERTScore
    source: Optional[str] = None     # source document for hallucination detection


@router.post("/evaluate")
def evaluate(request: EvaluateRequest, db: Session = Depends(get_db)):
    """
    Runs a full evaluation cycle for a single prompt.

    Flow:
      1. Initialize model and metrics
      2. Run evaluation pipeline — generates response and scores it
      3. Save result to database
      4. Return structured result to frontend

    Returns:
        EvaluationResult containing response, all metric scores, and timestamp

    Raises:
        HTTPException 500: if model generation or any metric fails
    """
    logger.info(f"Evaluation request received | model={request.model_id}")

    # initialize model with the requested model id
    model = OpenRouterModel(model_id=request.model_id)

    # initialize all metrics — new instances per request
    # ensures no state bleeds between concurrent requests
    metrics = [
        BLEUMetric(),
        ROUGEMetric(),
        BERTScoreMetric(),
        CosineSimilarityMetric(),
        HallucinationMetric()
    ]

    # pipeline orchestrates model generation and metric scoring
    evaluation_pipeline = EvaluationPipeline(model=model, metrics=metrics)

    try:
        result = evaluation_pipeline.evaluate(
            prompt=request.prompt,
            reference=request.reference,
            source=request.source
        )
    except Exception as e:
        logger.error(f"Evaluation failed | model={request.model_id} | error={str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    # save result to database for historical tracking
    try:
        repo = EvaluationRepository(db)
        repo.save_evaluation(result)
        logger.info(f"Evaluation saved to database | model={request.model_id}")
    except Exception as e:
        # log but don't fail the request if save fails
        # user still gets their result even if persistence fails
        logger.error(f"Failed to save evaluation | error={str(e)}")

    logger.info(f"Evaluation complete | model={request.model_id}")
    return result