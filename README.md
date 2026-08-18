# 🔍 Autonomous RAG Research Agent

An end-to-end, multi-agent research assistant built with **LangGraph**, **Groq (OpenAI Client)**, **Tavily**, **ChromaDB**, and **Streamlit**. 

This agent accepts complex user queries, breaks them down into search-optimized sub-questions, scrapes live web data, indexes chunks into a vector database, runs quality evaluations with self-correcting retry loops, extracts structured findings, synthesizes publication-ready Markdown reports, and generates downloadable PDFs.

---

## 🌟 Key Features

* **📋 Dynamic Query Planning:** Decomposes complex research topics into targeted sub-questions using LLM JSON extraction.
* **🌐 Web Search & Scraping:** Fetches live search results via Tavily API and extracts structured text with Trafilatura.
* **🧠 Vector RAG Architecture:** Chunks scraped content and indexes vectors locally using Hugging Face embeddings in ChromaDB.
* **⚖️ Self-Correcting Quality Loops:** Features an Evaluator node that assesses context grounding and automatically triggers refined re-search loops if information is missing.
* **📊 Structured Analysis:** Distills raw text chunks into clean JSON items containing specs, pros, cons, and direct source URLs.
* **💾 Persistent SQLite Memory:** Automatically caches completed research runs. Duplicate queries return cached reports instantly without wasting API tokens.
* **📥 PDF Report Generation:** Automatically renders Markdown into styled, publication-ready PDF documents using ReportLab.
* **🖥️ Streamlit UI Dashboard:** Interactive, user-friendly frontend to execute queries, view node progress in real time, and download generated PDF reports.

---

## 🏗️ Agent Pipeline Architecture

```text
[ START ]
    │
    ▼
[ Planner Node ] ───────────────► [ Web Search Node ]
    ▲                                    │
    │ (Feedback Loop)                    ▼
    │                            [ Scraper Node ]
    │                                    │
    │                                    ▼
    │                            [ Embedder Node ]
    │                                    │
    │                                    ▼
[ Evaluator Node ] ◄──────────── [ Retriever Node ]
    │
    ├── (Context Insufficient) ──► Loop back to Planner
    │
    └── (Context Sufficient)
            │
            ▼
   [ Analyzer Node ]
            │
            ▼
    [ Writer Node ]
            │
            ▼
   [ Exporter Node ] ──► (Save SQLite Memory & PDF)
            │
            ▼
        [ END ]
