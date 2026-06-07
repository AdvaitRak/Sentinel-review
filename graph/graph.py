from langgraph.graph import StateGraph, START, END

from graph.state import PRReviewState
from graph.nodes.fetch_pr import fetch_pr
from graph.nodes.lint import lint


def build_graph():
    graph = StateGraph(PRReviewState)

    graph.add_node("fetch_pr", fetch_pr)
    graph.add_node("lint_node",lint)
    graph.add_edge(START, "fetch_pr")
    graph.add_edge("fetch_pr","lint_node")
    graph.add_edge("lint_node", END)

    return graph.compile()


review_graph = build_graph()