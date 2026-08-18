import json
from typing import Dict, Any
from graph.state import AgentState
from tools.llm import client

PLANNER_PROMPT = """You are a senior research planning assistant.
Break down the main research query into 3 specific, search-optimized sub-questions.

Main Query: {query}
{feedback_context}

Return a JSON object with this exact structure:
{{
"sub_questions": [
"Sub question 1",
"Sub question 2",
"Sub question 3"
]
}}
"""

def planner_node(state: AgentState) -> Dict[str, Any]:
    """
    Generates sub-questions. Adapts queries if evaluator feedback is present.
    """
    query = state.get("query", "")
    feedback = state.get("evaluator_feedback", "")

    print("\n--- Executing Planner Node ---")

    feedback_context = ""
    if feedback:
        print(f"[PLANNER REVISION] Adapting plan based on evaluator feedback: '{feedback}'")
        feedback_context = f"PREVIOUS SEARCH FEEDBACK/MISSING DATA: {feedback}\nGenerate NEW search queries to explicitly fill these missing gaps."

    prompt = PLANNER_PROMPT.format(query=query, feedback_context=feedback_context)

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You output JSON only."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.2
        )

        result = json.loads(response.choices[0].message.content)
        sub_qs = result.get("sub_questions", [query])
        print(f"Generated {len(sub_qs)} sub-questions: {sub_qs}")

        return {"sub_questions": sub_qs}

    except Exception as e:
        print(f"[PLANNER ERROR] Fallback to original query: {e}")
        return {"sub_questions": [query]}