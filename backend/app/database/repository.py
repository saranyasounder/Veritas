from sqlalchemy.orm import Session
from typing import List, Optional
from .models import Evaluation
from app.evaluator.pipeline import EvaluationResult
from app.core.logger import get_logger

logger = get_logger(__name__)

class EvaluationRepository:
    """
    Handles all database operations for evaluation results.
    Single point of contact between the app and the evaluations table.
    """

    def __init__(self, db_session: Session):
        # inject database session — makes testing easier
        # session is created per request and closed after
        self.db = db_session

    def save_evaluation(self, evaluation_result: EvaluationResult) -> Evaluation:
        """
        Persists an evaluation result to the database.
        Converts MetricResult objects to plain dicts for JSON storage.
        """
        # serialize metrics from MetricResult objects to plain dicts
        # PostgreSQL JSON column requires serializable types
        serialized_metrics = {
            name: {
                "score": result.score,
                "passed": result.passed,
                "details": result.details
            }
            for name, result in evaluation_result.metrics.items()
        }

        evaluation = Evaluation(
            prompt=evaluation_result.prompt,
            model=evaluation_result.model,
            response=evaluation_result.response,
            metrics=serialized_metrics
        )

        self.db.add(evaluation)
        self.db.commit()
        # refresh to get auto generated fields like id and timestamp
        self.db.refresh(evaluation)

        logger.info(f"Evaluation saved | id={evaluation.id} | model={evaluation.model}")
        return evaluation

    def get_all(self) -> List[Evaluation]:
        """Returns all evaluations ordered by most recent first."""
        return self.db.query(Evaluation)\
                      .order_by(Evaluation.timestamp.desc())\
                      .all()

    def get_by_model(self, model_name: str) -> List[Evaluation]:
        """Returns all evaluations for a specific model."""
        return self.db.query(Evaluation)\
                      .filter(Evaluation.model == model_name)\
                      .order_by(Evaluation.timestamp.desc())\
                      .all()