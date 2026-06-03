from typing import Optional
from openai import OpenAI
import time
import os
from dotenv import load_dotenv
from .base import BaseModel, ModelResponse

# load environment variables from .env file
load_dotenv()

# default max tokens for all requests
MAX_TOKENS = 2048


class OpenRouterModel(BaseModel):

    def __init__(self, model_id: str):
        # initialize parent class with model_id
        super().__init__(model_id)

        # create openrouter client using openai sdk
        # openrouter uses same format as openai but different base url
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = MAX_TOKENS
    ) -> ModelResponse:
        # record start time to calculate latency
        start_time = time.time()

        # build messages list
        # add system prompt first if provided
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # make api call to openrouter
        response = self.client.chat.completions.create(
            model=self.model_id,
            messages=messages,
            max_tokens=max_tokens
        )

        # calculate how long the api call took in milliseconds
        latency = (time.time() - start_time) * 1000

        # return standardized response object
        # cost_usd is 0.0 for now — will add real calculation later
        return ModelResponse(
            content=response.choices[0].message.content,
            model=self.model_id,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            latency_ms=latency,
            cost_usd=0.0
        )