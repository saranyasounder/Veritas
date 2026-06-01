from bert_score import score as bert_score
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import Optional
from .base import BaseMetric, MetricResult

class BERTScoreMetric(BaseMetric):
    def __init__(self):
        super().__init__("BERTScore")

    def compute(self, hypothesis: str, reference: Optional[str] = None, source: Optional[str] = None) -> MetricResult:
        if not reference:
            raise ValueError("BERTScore requires a reference string")
        
        P, R, F1 = bert_score([hypothesis], [reference], lang='en')
        return MetricResult(
    name=self.name,
    score=round(F1[0].item(), 4),
    details={
        "precision": round(P[0].item(), 4),
        "recall": round(R[0].item(), 4),
        "f1": round(F1[0].item(), 4)
    }
)
    
class CosineSimilarityMetric(BaseMetric):
    def __init__(self):
        super().__init__("CosineSimilarity")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def compute(self, hypothesis: str, reference: Optional[str] = None, source: Optional[str] = None) -> MetricResult:
        if not reference:
            raise ValueError("Cosine Similarity requires a reference string")
        
        embeddings = self.model.encode([hypothesis, reference])
        cosine_sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        
        return MetricResult(name=self.name, score=round(cosine_sim, 4))