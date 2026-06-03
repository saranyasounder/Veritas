from openai import OpenAI
import os
from dotenv import load_dotenv
from app.core.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

def generate_reference(prompt: str) -> str:
    """
    Uses GPT-4o to generate an ideal reference answer for a given prompt.
    Used as ground truth for BLEU, ROUGE, and BERTScore evaluation.
    
    Args:
        prompt: the question or input to generate a reference for
        
    Returns:
        High quality reference answer string
        Empty string if generation fails
    """
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )

        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert assistant. Generate a concise, accurate, and comprehensive answer to the question. This will be used as a reference answer for evaluation purposes."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=500
        )

        reference = response.choices[0].message.content
        logger.info(f"Reference generated | prompt={prompt[:50]}")
        return reference

    except Exception as e:
        logger.error(f"Reference generation failed | error={str(e)}")
        return ""