from typing import TypedDict, List , Dict
from langgraph.graph import StateGraph, END

class ResearchState(TypedDict):
    topic: str
    sub_queries: List[str]
    search_results: List[str]
    report: str
    reflection_notes: str    
    loop_count: int  
    evaluation: Dict

def build_graph():
    from src.agents import planner_node, searcher_node, reporter_node,reflector_node,should_continue, evaluator_node

    graph = StateGraph(ResearchState)

    graph.add_node("planner", planner_node)
    graph.add_node("searcher", searcher_node)
    graph.add_node("reflector", reflector_node)
    graph.add_node("reporter", reporter_node)
    graph.add_node("evaluator", evaluator_node)

    graph.set_entry_point("planner")
    graph.add_edge("planner", "searcher")
    graph.add_edge("searcher","reflector")
    graph.add_conditional_edges("reflector",should_continue,{
            "searcher": "searcher",
            "reporter": "reporter"
        })
    graph.add_edge('reporter','evaluator')
    graph.add_edge("evaluator", END)

    return graph.compile()