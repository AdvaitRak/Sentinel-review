from langgraph.graph import StateGraph, START, END

from graph.state import PRReviewState
from graph.nodes.fetch_pr import fetch_pr


def build_graph():
    graph = StateGraph(PRReviewState)

    graph.add_node("fetch_pr", fetch_pr)
    graph.add_edge(START, "fetch_pr")
    graph.add_edge("fetch_pr", END)

    return graph.compile()


review_graph = build_graph()