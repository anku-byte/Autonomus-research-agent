import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    project_root = Path(__file__).resolve().parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

from app.config import ConfigurationError, validate_config
from db.database import init_db, get_cached_run
from graph.builder import build_graph

def main():
    try:
        validate_config()
        init_db()
        print("Autonomous Agent initialized successfully.\n")

        test_query = "List top 3 electric vehicles under $40,000"
        print(f"Checking Memory Cache for Query: '{test_query}'...")

        cached_run = get_cached_run(test_query)
        if cached_run:
            print("\n==========================================")
            print("   [MEMORY HIT] RETRIEVED FROM SQLITE CACHE")
            print("==========================================")
            print(f"Query: {cached_run['query']}")
            print(f"PDF Path: {cached_run['pdf_path']}\n")
            return

        print("[MEMORY MISS] Executing Full Self-Correcting LangGraph Pipeline...\n")
        app = build_graph()

        initial_state = {
            "query": test_query,
            "sub_questions": [],
            "search_results": [],
            "scraped_docs": [],
            "retrieved_chunks": [],
            "extracted_data": [],
            "final_report": "",
            "pdf_path": "",
            "is_cached": False,
            "loop_count": 0,
            "is_sufficient": False,
            "evaluator_feedback": ""
        }
        final_state = app.invoke(initial_state)

        pdf = final_state.get("pdf_path", "")
        loops = final_state.get("loop_count", 1)
        print("\n==========================================")
        print("   RESEARCH PIPELINE COMPLETE & PERSISTED")
        print("==========================================")
        print(f"Total Iteration Loops Executed: {loops}")
        print(f"Markdown Report saved: outputs/report.md")
        print(f"PDF Document saved:      {pdf}\n")

    except ConfigurationError as e:
        print(f"[CONFIG ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[GRAPH ERROR] Failed during graph execution: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()