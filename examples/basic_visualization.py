"""Display a small ShapeIt graph with Matplotlib."""

from pdl_graph import Graph, draw_graph


if __name__ == "__main__":
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "A")
    graph.add_node("D")
    

    draw_graph(graph, show=True)
