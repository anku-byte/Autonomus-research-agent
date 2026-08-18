
import os
import sys
import json
import streamlit as st

# Add root directory to path for clean imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import validate_config
from db.database import init_db, get_cached_run
from graph.builder import build_graph

# Page Configuration
st.set_page_config(
    page_title="Autonomous Research Agent",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Autonomous RAG Research Agent")
st.caption("Powered by LangGraph, ChromaDB, Groq LLM, & Tavily")

# Initialize Environment & Database
try:
    validate_config()
    init_db()
except Exception as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

# Sidebar Options
with st.sidebar:
    st.header("⚙️ Settings")
    force_refresh = st.checkbox("Bypass SQLite Cache (Force Fresh Search)", value=False)
    st.divider()
    st.markdown("**Pipeline Workflow:**")
    st.markdown("""
    1. 📋 Planner Node
    2. 🌐 Tavily Search Node
    3. 📄 Web Scraper Node
    4. 🧠 Embedder Node (Chroma)
    5. 🔎 Retriever Node
    6. ⚖️ Quality Evaluator Node
    7. 📊 Analyzer Node
    8. 📝 Writer Node
    9. 📥 Exporter Node (PDF)
    """)

# User Input
query = st.text_input(
    "Enter Research Topic or Question:",
    placeholder="e.g., List top 3 electric vehicles under $40,000"
)

if st.button("Run Autonomous Agent", type="primary"):
    if not query.strip():
        st.warning("Please enter a valid search query.")
        st.stop()

    # Check Cache first unless force refresh is checked
    if not force_refresh:
        cached_run = get_cached_run(query)
        if cached_run:
            st.success("⚡ Memory Hit! Retrieved instantly from SQLite Cache.")
            
            tab1, tab2, tab3 = st.tabs(["📄 Final Report", "📊 Extracted JSON", "📋 Sub-Questions"])
            
            with tab1:
                st.markdown(cached_run["final_report"])
                if os.path.exists(cached_run["pdf_path"]):
                    with open(cached_run["pdf_path"], "rb") as pdf_file:
                        st.download_button(
                            label="📥 Download PDF Report",
                            data=pdf_file,
                            file_name="Research_Report.pdf",
                            mime="application/pdf"
                        )

            with tab2:
                st.json(cached_run["extracted_data"])

            with tab3:
                st.write(cached_run["sub_questions"])

            st.stop()

    # Execute Graph if not cached
    st.info("🚀 Initiating LangGraph Pipeline execution...")
    status_container = st.status("Executing Research Nodes...", expanded=True)

    try:
        app = build_graph()

        initial_state = {
            "query": query,
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

        status_container.write("🧠 Decomposing query into sub-questions...")
        final_state = app.invoke(initial_state)
        status_container.update(label="✅ Research Pipeline Completed Successfully!", state="complete", expanded=False)

        # Display Results
        report_md = final_state.get("final_report", "")
        pdf_path = final_state.get("pdf_path", "")
        extracted = final_state.get("extracted_data", [])
        sub_qs = final_state.get("sub_questions", [])

        tab1, tab2, tab3 = st.tabs(["📄 Final Report", "📊 Extracted JSON", "📋 Sub-Questions"])

        with tab1:
            st.markdown(report_md)
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_file,
                        file_name="Research_Report.pdf",
                        mime="application/pdf"
                    )

        with tab2:
            st.json(extracted)

        with tab3:
            st.write(sub_qs)

    except Exception as e:
        status_container.update(label="❌ Graph Execution Failed", state="error")
        st.error(f"Error during execution: {e}")