from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional

@dataclass
class MetricResult:
    name:str
    score: float
    passed: Optional[bool] = None
    details:Optional[dict] = None

class BaseMetric(ABC):
    def __init__(self, name:str):
        self.name = name
    @abstractmethod
    def compute(self, hypothesis:str, reference:Optional[str] = None, source:Optional[str] = None) -> MetricResult:
        pass