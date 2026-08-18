
from typing import Dict, Any, List
from graph.state import AgentState
from rag.vector_store import query_vector_store

def retriever_node(state: AgentState) -> Dict[str, Any]:
    """
    Queries ChromaDB for each sub-question in state["sub_questions"]
    and aggregates top relevant context chunks into state["retrieved_chunks"].
    """
    sub_questions = state.get("sub_questions", [])
    retrieved_chunks: List[Dict[str, Any]] = []

    print(f"\n--- Executing Retriever Node for {len(sub_questions)} Sub-Questions ---")

    for sq in sub_questions:
        print(f"Retrieving context for: '{sq}'")
        # Get top 3 most relevant chunks for this sub-question
        chunks = query_vector_store(query_text=sq, k=3)

        for chunk in chunks:
            retrieved_chunks.append({
                "sub_question": sq,
                "text": chunk["text"],
                "metadata": chunk["metadata"],
                "distance": chunk.get("distance", 0.0)
            })

    print(f"Retrieved {len(retrieved_chunks)} total context chunks across all sub-questions.")

    return {
        "retrieved_chunks": retrieved_chunks
    }
    