from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from typing import Optional
from .base import BaseMetric, MetricResult

class BLEUMetric(BaseMetric):
    def __init__(self):
        super().__init__("BLEU")

    def compute(
        self,
        hypothesis: str,
        reference: Optional[str] = None,
        source: Optional[str] = None
    ) -> MetricResult:
        if not reference:
            return MetricResult(
                name=self.name,
                score=0.0,
                details={"skipped": "no reference provided"}
            )
        
        reference_tokens = reference.lower().split()
        hypothesis_tokens = hypothesis.lower().split()
        
        smoothing = SmoothingFunction().method1
        score = sentence_bleu(
            [reference_tokens],
            hypothesis_tokens,
            smoothing_function=smoothing
        )
        
        return MetricResult(name=self.name, score=round(score, 4))


class ROUGEMetric(BaseMetric):
    def __init__(self):
        super().__init__("ROUGE")
        self.scorer = rouge_scorer.RougeScorer(
            ['rouge1', 'rouge2', 'rougeL'],
            use_stemmer=True
        )

    def compute(
        self,
        hypothesis: str,
        reference: Optional[str] = None,
        source: Optional[str] = None
    ) -> MetricResult:
        if not reference:
            return MetricResult(
                name=self.name,
                score=0.0,
                details={"skipped": "no reference provided"}
            )
        
        scores = self.scorer.score(reference, hypothesis)
        
        return MetricResult(
            name=self.name,
            score=round(scores['rouge1'].fmeasure, 4),
            details={
                "rouge1": round(scores['rouge1'].fmeasure, 4),
                "rouge2": round(scores['rouge2'].fmeasure, 4),
                "rougeL": round(scores['rougeL'].fmeasure, 4)
            }
        )