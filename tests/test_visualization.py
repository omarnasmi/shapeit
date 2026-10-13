"""Tests for :mod:`pdl_graph.visualization`.

All tests use the ``"Agg"`` (non-interactive) Matplotlib backend so that
the test suite can run in headless CI environments without a display server.

Each test function exercises one aspect of :func:`~pdl_graph.draw_graph`
behaviour – layout, content, error handling – in isolation.
"""

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pytest

from pdl_graph import Graph, draw_graph, visualize_graph


def test_draw_graph_represents_nodes_edges_and_labels():
    """draw_graph renders all nodes, edges, and text labels on the axes.

    Given a graph with 3 edges and 1 isolated node, the resulting axes
    must contain:

    - **1 scatter collection** holding all **4 node** positions,
    - **2 line objects** (one per edge), and
    - **4 text elements** whose contents equal the node identifiers.
    """
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
    """When no positions are supplied, nodes are placed on a unit circle.

    For a two-node graph the first node must be at ``(1, 0)`` (angle 0)
    and the second at ``(−1, 0)`` (angle π), matching the output of
    :func:`~pdl_graph.visualization._circular_positions`.
    """
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
    """draw_graph raises ValueError when called with a directed graph.

    The error message must mention the word ``"undirected"`` so callers
    can quickly understand why the call was rejected.
    """
    graph = Graph(directed=True)

    with pytest.raises(ValueError, match="undirected"):
        draw_graph(graph)


def test_visualize_graph_is_public_alias():
    """visualize_graph is the same object as draw_graph (public alias).

    This ensures that code that uses the older ``visualize_graph`` name
    continues to call exactly the same function without any indirection.
    """
    assert visualize_graph is draw_graph
