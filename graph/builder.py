from langgraph.graph import StateGraph, START, END
from graph.state import AgentState
from nodes.planner import planner_node
from nodes.web_search import web_search_node
from nodes.scraper import scraper_node
from nodes.embedder import embedder_node
from nodes.retriever import retriever_node
from nodes.evaluator import evaluator_node
from nodes.analyzer import analyzer_node
from nodes.writer import writer_node
from nodes.exporter import exporter_node

def route_after_evaluation(state: AgentState) -> str:
    """
    Conditional Edge Routing Function:
    - If context is sufficient OR max loops reached (2) -> proceed to analyzer.
    - If context is insufficient -> loop back to planner.
    """
    is_sufficient = state.get("is_sufficient", True)
    loop_count = state.get("loop_count", 0)

    MAX_LOOPS = 2

    if is_sufficient or loop_count >= MAX_LOOPS:
        if loop_count >= MAX_LOOPS and not is_sufficient:
            print(f"[ROUTER] Max re-research limit ({MAX_LOOPS}) reached. Proceeding with best available context.")
        else:
            print("[ROUTER] Quality threshold passed. Proceeding to Analyzer.")
        return "analyzer"
    else:
        print(f"[ROUTER] Re-research needed (Loop {loop_count}/{MAX_LOOPS}). Routing back to Planner.")
        return "planner"

def build_graph():
    """
    Builds the Phase 11 LangGraph workflow with self-correcting conditional loops.
    """
    builder = StateGraph(AgentState)

    # Add nodes
    builder.add_node("planner", planner_node)
    builder.add_node("web_search", web_search_node)
    builder.add_node("scraper", scraper_node)
    builder.add_node("embedder", embedder_node)
    builder.add_node("retriever", retriever_node)
    builder.add_node("evaluator", evaluator_node)
    builder.add_node("analyzer", analyzer_node)
    builder.add_node("writer", writer_node)
    builder.add_node("exporter", exporter_node)

    # Connect standard flow
    builder.add_edge(START, "planner")
    builder.add_edge("planner", "web_search")
    builder.add_edge("web_search", "scraper")
    builder.add_edge("scraper", "embedder")
    builder.add_edge("embedder", "retriever")
    builder.add_edge("retriever", "evaluator")

    # CONDITIONAL LOOP EDGE from Evaluator
    builder.add_conditional_edges(
        "evaluator",
        route_after_evaluation,
        {
            "analyzer": "analyzer",
            "planner": "planner"
        }
    )

    builder.add_edge("analyzer", "writer")
    builder.add_edge("writer", "exporter")
    builder.add_edge("exporter", END)

    graph = builder.compile()
    return graph