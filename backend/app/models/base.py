from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional

# dataclass automatically generates __init__, __repr__, and __eq__
# so we don't have to write boilerplate code to initialize the fields
@dataclass
class ModelResponse:
    content: str          # the actual text the model generated
    model: str            # which model generated it e.g. "anthropic/claude-sonnet-4"
    prompt_tokens: int    # how many tokens your prompt used
    completion_tokens: int # how many tokens the response used
    latency_ms: float     # how long the API call took in milliseconds
    cost_usd: float       # how much this call cost in dollars


class BaseModel(ABC):
    
    def __init__(self, model_id: str):
        # store which model this instance represents
        self.model_id = model_id

    @abstractmethod
    def generate(
        self, 
        prompt: str,                        # the question or input to the model
        system_prompt: Optional[str] = None, # instructions to guide the model's behavior        
        max_tokens: int = 1000             
    ) -> ModelResponse:                     
        pass                                