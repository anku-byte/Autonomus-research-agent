
import json
from typing import Dict, Any
from graph.state import AgentState
from tools.llm import client

EVALUATOR_PROMPT = """You are a rigorous research quality evaluator.
Your job is to assess whether the retrieved context chunks provide sufficient, high-quality, and complete information to thoroughly answer the user's research query.

User Query: {query}

Retrieved Context Chunks ({chunk_count} chunks total):
{context}

Evaluate the information and return a JSON object strictly adhering to this schema:
{{
"is_sufficient": true | false,
"reasoning": "Brief explanation of why the context is or isn't sufficient",
"missing_aspects": ["Specific missing detail 1", "Specific missing detail 2"]
}}

Rules:
- Mark `is_sufficient` as true IF the context directly covers the core query with specifics (e.g. models, specs, numbers).
- Mark `is_sufficient` as false IF key information requested by the query is completely absent or too vague.
"""

def evaluator_node(state: AgentState) -> Dict[str, Any]:
    """
    Evaluates retrieved chunks for quality and completeness.
    Increments loop_count and sets is_sufficient flag.
    """
    query = state.get("query", "")
    chunks = state.get("retrieved_chunks", [])
    current_loop = state.get("loop_count", 0) + 1

    print(f"\n--- Executing Evaluator Node (Iteration {current_loop}) ---")

    if not chunks:
        print("[EVALUATOR] No chunks retrieved. Triggering re-research loop.")
        return {
            "is_sufficient": False,
            "loop_count": current_loop,
            "evaluator_feedback": "No relevant context was found in the initial web search. Search for broader alternative terms."
        }

    # Format context preview for evaluation
    formatted_context = ""
    for idx, chunk in enumerate(chunks[:10], 1):
        formatted_context += f"- Chunk {idx}: {chunk.get('text', '')[:300]}\n"

    prompt = EVALUATOR_PROMPT.format(
        query=query,
        chunk_count=len(chunks),
        context=formatted_context
    )

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are a research evaluator outputting strict JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.0
        )

        result = json.loads(response.choices[0].message.content)
        is_sufficient = result.get("is_sufficient", True)
        reasoning = result.get("reasoning", "")
        missing = result.get("missing_aspects", [])

        feedback = f"Reason: {reasoning}. Missing details: {', '.join(missing)}" if missing else reasoning

        print(f"[EVALUATOR DECISION] Sufficient: {is_sufficient} | Details: {reasoning}")

        return {
            "is_sufficient": is_sufficient,
            "loop_count": current_loop,
            "evaluator_feedback": feedback
        }

    except Exception as e:
        print(f"[EVALUATOR ERROR] Defaulting to sufficient due to error: {e}")
        return {
            "is_sufficient": True,
            "loop_count": current_loop,
            "evaluator_feedback": ""
        }