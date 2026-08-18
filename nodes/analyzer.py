
import json
from typing import Dict, Any, List
from graph.state import AgentState
from tools.llm import client

ANALYZER_PROMPT = """You are an expert research analyst.
Analyze the following context chunks retrieved from the web and extract key structured information related to the research query.

Research Query: {query}

Retrieved Context Chunks:
{context}

Extract all relevant entities/items matching the query (e.g., specific vehicle models, key statistics, products, or core findings).
Your output MUST be a valid JSON object matching this exact schema:
{{
"extracted_data": [
{{
  "entity": "Name of Product/Vehicle/Finding",
  "summary": "Brief overall summary or key takeaway",
  "key_specs": {{
    "price": "Price or Cost info",
    "key_feature_1": "Feature details",
    "key_feature_2": "Feature details"
  }},
  "pros": ["Pro 1", "Pro 2"],
  "cons": ["Con 1", "Con 2"],
  "source_url": "URL of the primary source chunk used"
}}
]
}}
"""

def analyzer_node(state: AgentState) -> Dict[str, Any]:
    """
    Takes state["retrieved_chunks"], passes context to the LLM,
    and extracts structured JSON findings into state["extracted_data"].
    """
    query = state.get("query", "")
    chunks = state.get("retrieved_chunks", [])

    print(f"\n--- Executing Analyzer Node across {len(chunks)} Chunks ---")

    if not chunks:
        print("[ANALYZER WARNING] No chunks found to analyze.")
        return {"extracted_data": []}

    # Format chunks for LLM context window
    formatted_context = ""
    for idx, chunk in enumerate(chunks, 1):
        source = chunk.get("metadata", {}).get("url", "N/A")
        formatted_context += f"--- Chunk {idx} (Source: {source}) ---\n{chunk.get('text', '')}\n\n"

    prompt = ANALYZER_PROMPT.format(query=query, context=formatted_context[:12000])  # Cap context window safety

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are a precise data extraction assistant that outputs only structured JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )

        content = response.choices[0].message.content
        parsed = json.loads(content)
        extracted = parsed.get("extracted_data", [])

        print(f"Successfully extracted {len(extracted)} structured factual entities.")
        return {"extracted_data": extracted}

    except Exception as e:
        print(f"[ANALYZER ERROR] Failed JSON extraction: {e}")
        return {"extracted_data": []}