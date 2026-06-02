from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.models.openrouter import OpenRouterModel
from app.evaluator.pipeline import EvaluationPipeline
from app.evaluator.judge import LLMJudge
from app.metrics.lexical import BLEUMetric, ROUGEMetric
from app.metrics.semantic import BERTScoreMetric, CosineSimilarityMetric
from app.metrics.hallucination import HallucinationMetric
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
def evaluate(request: EvaluateRequest):
    """
    Runs a full evaluation cycle for a single prompt.
    
    Flow:
      1. Initialize model and metrics
      2. Run evaluation pipeline — generates response and scores it
      3. Return structured result to frontend
      
    Returns:
        EvaluationResult containing response, all metric scores, and timestamp
        
    Raises:
        HTTPException 500: if model generation or any metric fails
    """
    logger.info(f"Evaluation request received | model={request.model_id}")

    # initialize model with the requested model id
    # OpenRouterModel handles all models through one unified client
    model = OpenRouterModel(model_id=request.model_id)

    # initialize all metrics for this evaluation
    # new instances per request ensures no state bleeds between requests
    metrics = [
        BLEUMetric(),            # word overlap — precision focused
        ROUGEMetric(),           # word overlap — recall focused
        BERTScoreMetric(),       # semantic similarity using embeddings
        CosineSimilarityMetric(), # cosine distance between embeddings
        HallucinationMetric()    # checks if response is grounded in source
    ]

    # pipeline orchestrates model generation and metric scoring
    evaluation_pipeline = EvaluationPipeline(model=model, metrics=metrics)

    try:
        result = evaluation_pipeline.evaluate(
            prompt=request.prompt,
            reference=request.reference,  # passed to lexical and semantic metrics
            source=request.source         # passed to hallucination metric
        )
    except Exception as e:
        # log the full error before returning HTTP response
        # HTTPException converts the error into a proper JSON error response
        # with status code 500 so the frontend can handle it gracefully
        logger.error(f"Evaluation failed | model={request.model_id} | error={str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    logger.info(f"Evaluation complete | model={request.model_id}")
    return result