
from typing import List
from sentence_transformers import SentenceTransformer

# Initialize a fast, accurate 384-dimensional local embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Converts a list of text strings into vector embeddings.
    """
    if not texts:
        return []
    embeddings = embedding_model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()