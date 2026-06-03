from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from typing import Optional
from .base import BaseMetric, MetricResult

class HallucinationMetric(BaseMetric):
    # minimum similarity score between hypothesis and source
    # anything below this is flagged as a potential hallucination
    THRESHOLD = 0.5

    def __init__(self):
        super().__init__("Hallucination")
        # load sentence transformer once at initialization
        # 'all-MiniLM-L6-v2' is lightweight and fast while still accurate
        # loading here avoids reloading the model on every compute call
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def compute(
        self,
        hypothesis: str,                    # the model's generated answer
        reference: Optional[str] = None,    # not used here — hallucination only needs source
        source: Optional[str] = None        # the document the answer should be based on
    ) -> MetricResult:
        # hallucination detection requires a source document to compare against
        # without it there is nothing to verify the answer against
        if not source:
            return MetricResult(
                name=self.name,
                score=0.0,
                details={"skipped": "no source provided"}
            )

        # convert both texts into embedding vectors
        # embeddings[0] = hypothesis embedding
        # embeddings[1] = source embedding
        # similar meaning = similar vectors = high cosine similarity
        embeddings = self.model.encode([hypothesis, source])

        # measure how similar the two vectors are
        # score of 1.0 = identical meaning
        # score of 0.0 = completely unrelated
        cosine_sim = cosine_similarity(
            [embeddings[0]],
            [embeddings[1]]
        )[0][0]

        # convert numpy float to plain python float
        # needed for database storage and JSON serialization
        score = round(float(cosine_sim), 4)

        return MetricResult(
            name=self.name,
            score=score,
            # passed=True means answer is grounded in source — no hallucination
            # passed=False means answer diverges from source — hallucination likely
            passed=cosine_sim >= self.THRESHOLD,
            details={
                # threshold used for this evaluation — stored for transparency
                "threshold": self.THRESHOLD,
                # explicit hallucination flag for easy dashboard display
                "hallucination_detected": cosine_sim < self.THRESHOLD
            }
        )