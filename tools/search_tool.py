
from typing import Dict, List, Any
from tavily import TavilyClient
from app.config import TAVILY_API_KEY

# Initialize Tavily client
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

def execute_search(query: str, max_results: int = 3) -> List[Dict[str, Any]]:
    """
    Executes a search query via Tavily API and returns formatted results.
    """
    try:
        response = tavily_client.search(query=query, max_results=max_results)
        results = []

        for item in response.get("results", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "snippet": item.get("content", "")
            })

        return results
    except Exception as e:
        print(f"[SEARCH ERROR] Failed search for '{query}': {e}")
        return []