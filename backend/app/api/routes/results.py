from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.repository import EvaluationRepository
from app.database.session import get_db
from app.core.logger import get_logger

# module level logger for tracking all results requests
logger = get_logger(__name__)

# router groups all results endpoints
# registered in main.py with prefix='/api'
router = APIRouter()


@router.get("/results")
def get_all_results(db: Session = Depends(get_db)):
    """
    Returns all evaluation results ordered by most recent first.
    Used by the dashboard to populate the results history view.
    
    Returns:
        List of Evaluation objects with metrics and timestamps
    """
    logger.info("Fetching all evaluation results")
    repo = EvaluationRepository(db)
    return repo.get_all()


@router.get("/results/{model_id}")
def get_results_by_model(model_id: str, db: Session = Depends(get_db)):
    """
    Returns all evaluations for a specific model.
    Used by the dashboard model comparison view.
    
    Args:
        model_id: OpenRouter model identifier e.g. 'anthropic/claude-sonnet-4'
        
    Returns:
        List of Evaluation objects for that model
        
    Raises:
        HTTPException 404: if no evaluations exist for that model
    """
    logger.info(f"Fetching results for model | model={model_id}")
    
    repo = EvaluationRepository(db)
    results = repo.get_by_model(model_id)
    
    # return 404 instead of empty list so frontend
    # can distinguish between "no results" and "model doesn't exist"
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"No evaluations found for model {model_id}"
        )
    
    return results


@router.get("/results/{evaluation_id}")
def get_result_by_id(evaluation_id: int, db: Session = Depends(get_db)):
    """
    Returns a single evaluation by its database id.
    Used by the dashboard detail view when a user clicks on a result.
    
    Args:
        evaluation_id: auto generated integer primary key
        
    Returns:
        Single Evaluation object with full metric details
        
    Raises:
        HTTPException 404: if evaluation with that id doesn't exist
    """
    logger.info(f"Fetching evaluation by id | id={evaluation_id}")
    
    repo = EvaluationRepository(db)
    result = repo.get_by_id(evaluation_id)
    
    # return 404 if id doesn't exist in database
    # prevents frontend from receiving null and crashing
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Evaluation {evaluation_id} not found"
        )
    
    return result