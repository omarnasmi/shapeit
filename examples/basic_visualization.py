"""Display a small ShapeIt graph with Matplotlib.

This script is the quickest way to see :mod:`pdl_graph` in action.
Run it directly from the repository root::

    python examples/basic_visualization.py

A Matplotlib window will open showing a triangle graph (A–B–C) plus an
isolated node (D).  Close the window to exit.
"""

from pdl_graph import Graph, draw_graph


if __name__ == "__main__":
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "A")
    graph.add_node("D")

    draw_graph(graph, show=True)
