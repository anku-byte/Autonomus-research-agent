from typing import Dict, List, TypedDict, Any

class AgentState(TypedDict):
    """
    The central state dictionary passed between nodes in the LangGraph workflow.
    """
    query: str
    sub_questions: List[str]
    search_results: List[Dict[str, Any]]
    scraped_docs: List[Dict[str, str]]
    retrieved_chunks: List[Dict[str, Any]]
    extracted_data: List[Dict[str, Any]]
    final_report: str
    pdf_path: str
    is_cached: bool
    loop_count: int         # Tracks revision iteration count
    is_sufficient: bool     # Flag set by Evaluator Node
    evaluator_feedback: str # Feedback passed back to Planner if context is insufficient