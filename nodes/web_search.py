
from typing import Dict, Any, List
from graph.state import AgentState
from tools.search_tool import execute_search

def web_search_node(state: AgentState) -> Dict[str, Any]:
    """
    Iterates over state["sub_questions"], performs a search for each,
    and aggregates results in state["search_results"].
    """
    sub_questions = state.get("sub_questions", [])
    all_results: List[Dict[str, Any]] = []

    print(f"--- Executing Web Search for {len(sub_questions)} Sub-Questions ---")

    for sq in sub_questions:
        print(f"Searching: '{sq}'")
        results = execute_search(query=sq, max_results=3)

        for item in results:
            all_results.append({
                "sub_question": sq,
                "title": item["title"],
                "url": item["url"],
                "snippet": item["snippet"]
            })

    return {
        "search_results": all_results
    }