from tavily import TavilyClient
import os
from dotenv import load_dotenv
from app.core.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

def search_source(query: str) -> str:
    """
    Searches the web for relevant content using Tavily.
    Returns a single string of combined search results
    to use as source document for hallucination detection.
    
    Args:
        query: the prompt or question to search for
        
    Returns:
        Combined text from top search results
        Empty string if search fails
    """
    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        
        # search and get raw content from top 3 results
        response = client.search(
            query=query,
            search_depth="basic",
            max_results=3,
            include_raw_content=True
        )
        
        # combine content from all results into one source document
        contents = []
        for result in response.get("results", []):
            content = result.get("content", "")
            if content:
                contents.append(content)
        
        combined = " ".join(contents)
        logger.info(f"Tavily search complete | query={query[:50]} | results={len(contents)}")
        return combined

    except Exception as e:
        logger.error(f"Tavily search failed | error={str(e)}")
        return ""