
from typing import Dict, Any
from graph.state import AgentState
from rag.chunking import chunk_documents
from rag.vector_store import add_chunks_to_vector_store

def embedder_node(state: AgentState) -> Dict[str, Any]:
    """
    Takes state["scraped_docs"], chunks texts, embeds them, and persists into ChromaDB.
    """
    scraped_docs = state.get("scraped_docs", [])
    print("\n--- Executing Embedder Node ---")

    chunks = chunk_documents(scraped_docs)
    print(f"Generated {len(chunks)} total text chunks across {len(scraped_docs)} documents.")

    if chunks:
        add_chunks_to_vector_store(chunks)
        print("Successfully embedded and indexed chunks into local ChromaDB store.")

    return {}