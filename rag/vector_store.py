
import os
from typing import Dict, List, Any
import chromadb
from rag.embeddings import get_embeddings

# Initialize persistent ChromaDB local storage directory
DB_PATH = os.path.join(os.getcwd(), "outputs", "chroma_db")
chroma_client = chromadb.PersistentClient(path=DB_PATH)

def get_or_create_collection(collection_name: str = "research_chunks"):
    """
    Gets or creates a Chroma collection.
    """
    return chroma_client.get_or_create_collection(name=collection_name)

def add_chunks_to_vector_store(chunks: List[Dict[str, Any]], collection_name: str = "research_chunks"):
    """
    Embeds and stores text chunks and metadata in ChromaDB.
    """
    if not chunks:
        return

    collection = get_or_create_collection(collection_name)

    ids = [c["chunk_id"] for c in chunks]
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]

    # Generate embeddings locally
    embeddings = get_embeddings(texts)

    # Upsert vectors into ChromaDB
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

def query_vector_store(query_text: str, k: int = 5, collection_name: str = "research_chunks") -> List[Dict[str, Any]]:
    """
    Queries ChromaDB for top-k semantically relevant chunks.
    """
    collection = get_or_create_collection(collection_name)
    query_embedding = get_embeddings([query_text])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    formatted_results = []
    if results and "documents" in results and results["documents"]:
        docs = results["documents"][0]
        metadatas = results["metadatas"][0] if "metadatas" in results else [{}] * len(docs)
        distances = results["distances"][0] if "distances" in results and results["distances"] else [0.0] * len(docs)

        for text, meta, dist in zip(docs, metadatas, distances):
            formatted_results.append({
                "text": text,
                "metadata": meta,
                "distance": dist
            })

    return formatted_results