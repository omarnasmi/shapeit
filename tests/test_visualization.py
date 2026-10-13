import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from pdl_graph import Graph, draw_graph, visualize_graph


def test_draw_graph_represents_nodes_edges_and_labels():
    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_node("isolated")

    _, axes = draw_graph(
        graph,
        positions={
            "A": (0, 0),
            "B": (1, 0),
            "C": (1, 1),
            "isolated": (0, 1),
        },
    )

    assert len(axes.collections) == 1
    assert len(axes.collections[0].get_offsets()) == 4
    assert len(axes.lines) == 2
    assert {text.get_text() for text in axes.texts} == {
        "A",
        "B",
        "C",
        "isolated",
    }
    plt.close(axes.figure)


def test_draw_graph_uses_a_deterministic_layout_for_graph_nodes():
    graph = Graph()
    graph.add_node("A")
    graph.add_node("B")

    _, axes = draw_graph(graph)

    offsets = axes.collections[0].get_offsets()
    assert offsets[0, 0] == pytest.approx(1.0)
    assert offsets[0, 1] == pytest.approx(0.0)
    assert offsets[1, 0] == pytest.approx(-1.0)
    assert offsets[1, 1] == pytest.approx(0.0)
    plt.close(axes.figure)


def test_draw_graph_rejects_directed_graphs():
    graph = Graph(directed=True)

    with pytest.raises(ValueError, match="undirected"):
        draw_graph(graph)


def test_visualize_graph_is_public_alias():
    assert visualize_graph is draw_graph
