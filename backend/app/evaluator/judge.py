from dataclasses import dataclass
from typing import Optional
import json
from app.models.base import BaseModel
from app.core.logger import get_logger

logger = get_logger(__name__)

@dataclass
class JudgeResult:
    """
    Stores qualitative scores from LLM as judge evaluation.
    Captures dimensions that mathematical metrics cannot measure.
    """
    helpfulness: float    # did the response actually help answer the question
    relevance: float      # did it address what was asked
    correctness: float    # is the information accurate
    completeness: float   # did it cover everything needed
    conciseness: float    # was it appropriately brief
    overall: float        # aggregate quality score
    reasoning: str        # judge's explanation of the scores


class LLMJudge:
    """
    Uses a second LLM to evaluate the quality of another LLM's response.
    Provides qualitative judgment that mathematical metrics cannot capture.
    """

    def __init__(self, model: BaseModel):
        # the model used as the judge
        # can be any model that implements BaseModel
        self.model = model

    def judge(self, prompt: str, response: str) -> JudgeResult:
        """
        Evaluates a model response across five quality dimensions.
        
        Args:
            prompt: the original question asked
            response: the model's answer to evaluate
            
        Returns:
            JudgeResult with scores and reasoning
            
        Raises:
            json.JSONDecodeError: if judge response cannot be parsed
        """
        # build structured evaluation prompt
        # explicit JSON format instruction reduces parsing failures
        judge_prompt = f"""
You are an expert evaluator. Rate the following response on a scale of 0 to 1.

Prompt: {prompt}
Response: {response}

Rate the response on:
- helpfulness
- relevance
- correctness
- completeness
- conciseness

Return your scores as JSON only. No other text. No markdown.
Example format:
{{
    "helpfulness": 0.9,
    "relevance": 0.8,
    "correctness": 0.7,
    "completeness": 0.8,
    "conciseness": 0.9,
    "overall": 0.82,
    "reasoning": "explanation here"
}}
"""
        logger.info(f"Running LLM judge evaluation")

        # send prompt to judge model
        model_response = self.model.generate(prompt=judge_prompt)

        # parse JSON response from judge
        # model is instructed to return JSON only
        # but parsing can still fail if model adds extra text
        try:
            scores = json.loads(model_response.content)
        except json.JSONDecodeError as e:
            logger.error(
                f"Judge response parsing failed | error={str(e)} | raw={model_response.content}"
            )
            raise

        logger.info(f"Judge evaluation complete | overall={scores['overall']}")

        return JudgeResult(
            helpfulness=scores["helpfulness"],
            relevance=scores["relevance"],
            correctness=scores["correctness"],
            completeness=scores["completeness"],
            conciseness=scores["conciseness"],
            overall=scores["overall"],
            reasoning=scores["reasoning"]
        )