
import sqlite3
import json
import os
from typing import Dict, Any, Optional

DB_PATH = os.path.join("outputs", "research_memory.db")

def init_db():
    """
    Initializes the SQLite database and creates the research_runs table if it doesn't exist.
    """
    os.makedirs("outputs", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS research_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT UNIQUE NOT NULL,
            sub_questions TEXT,
            extracted_data TEXT,
            final_report TEXT,
            pdf_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_cached_run(query: str) -> Optional[Dict[str, Any]]:
    """
    Checks if a research report already exists in the database for the given query.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT query, sub_questions, extracted_data, final_report, pdf_path 
        FROM research_runs 
        WHERE LOWER(query) = LOWER(?)
    """, (query.strip(),))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "query": row[0],
            "sub_questions": json.loads(row[1]),
            "extracted_data": json.loads(row[2]),
            "final_report": row[3],
            "pdf_path": row[4],
            "is_cached": True
        }
    return None

def save_research_run(state: Dict[str, Any]):
    """
    Saves or updates a completed research run in SQLite memory.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    query = state.get("query", "").strip()
    sub_questions = json.dumps(state.get("sub_questions", []))
    extracted_data = json.dumps(state.get("extracted_data", []))
    final_report = state.get("final_report", "")
    pdf_path = state.get("pdf_path", "")

    cursor.execute("""
        INSERT OR REPLACE INTO research_runs (query, sub_questions, extracted_data, final_report, pdf_path)
        VALUES (?, ?, ?, ?, ?)
    """, (query, sub_questions, extracted_data, final_report, pdf_path))

    conn.commit()
    conn.close()
    print(f"[MEMORY] Research run successfully persisted to SQLite database ({DB_PATH}).")