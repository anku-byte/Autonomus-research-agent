
from typing import Dict, Any, List
from rag.vector_store import query_vector_store

def retrieval_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Retrieves relevant contextual documents from the vector store
    based on the current research task or query in state.
    """
    print("\n--- [RETRIEVAL NODE EXECUTING] ---")
    
    # Extract query from graph state
    query = state.get("query") or state.get("current_task", "")
    print(f"[Retrieval] Searching vector store for: '{query}'")

    try:
        # Perform similarity search
        results = query_vector_store(query=query, top_k=3)
        print(f"[Retrieval] Retrieved {len(results)} context documents.")
        
        # Format context for down-stream LLM nodes
        retrieved_context = "\n\n".join([doc["text"] for doc in results])
        
        # Update state
        return {
            **state,
            "retrieved_docs": results,
            "context": retrieved_context
        }
    except Exception as e:
        print(f"[Retrieval Warning] Vector search error: {e}")
        return {
            **state,
            "retrieved_docs": [],
            "context": "No local vector context available."
        }