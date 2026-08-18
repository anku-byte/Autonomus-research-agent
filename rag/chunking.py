
from typing import Dict, List, Any
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(scraped_docs: List[Dict[str, str]], chunk_size: int = 600, chunk_overlap: int = 60) -> List[Dict[str, Any]]:
    """
    Splits scraped documents into text chunks with metadata (source URL and title).
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )

    chunks = []
    chunk_counter = 0

    for doc in scraped_docs:
        url = doc.get("url", "")
        title = doc.get("title", "")
        text = doc.get("text", "")

        if not text:
            continue

        doc_chunks = text_splitter.split_text(text)
        for idx, chunk in enumerate(doc_chunks):
            chunk_counter += 1
            chunks.append({
                "chunk_id": f"chunk_{chunk_counter}",
                "text": chunk,
                "metadata": {
                    "url": url,
                    "title": title,
                    "chunk_index": idx
                }
            })

    return chunks