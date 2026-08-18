
import json
from typing import Dict, Any
from graph.state import AgentState
from tools.llm import client

WRITER_PROMPT = """You are a senior research analyst and technical communicator.
Your task is to write a comprehensive, professional research report in clean Markdown format based on the research query and extracted structured findings provided.

Primary Research Query: {query}

Extracted Findings (JSON):
{extracted_data}

Report Structure Requirements:
1. **Title**: Catchy, clear title based on the query.
2. **Executive Summary**: High-level synthesis of findings (2-3 paragraphs).
3. **Comparative Analysis Table**: Clean Markdown table comparing key specs, pricing, and key features.
4. **Detailed Entity Profiles**: Standalone subsections for each entity with pros, cons, and key technical specifications.
5. **Sources & References**: List of external URLs referenced.

Formatting Guidelines:
- Do NOT use formal top-level markdown headers like '# Title' if starting directly, but use standard ## and ### subheadings for hierarchy.
- Ensure all pricing and specification numbers are accurate to the extracted context.
"""

def writer_node(state: AgentState) -> Dict[str, Any]:
    """
    Synthesizes state["extracted_data"] into a publication-ready Markdown report stored in state["final_report"].
    """
    query = state.get("query", "")
    extracted_data = state.get("extracted_data", [])

    print(f"\n--- Executing Report Writer Node ---")

    formatted_json = json.dumps(extracted_data, indent=2)
    prompt = WRITER_PROMPT.format(query=query, extracted_data=formatted_json)

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are a professional research report writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        report = response.choices[0].message.content
        print("Successfully synthesized research report.")

        return {"final_report": report}

    except Exception as e:
        print(f"[WRITER ERROR] Failed report generation: {e}")
        return {"final_report": "# Research Report Generation Failed"}