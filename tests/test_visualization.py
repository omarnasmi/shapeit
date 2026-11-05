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


def test_directed_graph_draws_arrows():
    """Directed edges are drawn as arrow patches, not plain lines."""
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("B", "A")
    g.add_edge("B", "C")
    _, ax = draw_graph(g)
    assert len(ax.patches) == 3
    assert len(ax.lines) == 0
    plt.close(ax.figure)


def test_empty_graph_and_isolated_nodes():
    """Empty graphs and isolated nodes are drawn without error."""
    _, ax = draw_graph(Graph(directed=True), layout="spring")
    assert len(ax.texts) == 0
    plt.close(ax.figure)
    g = Graph()
    for n in "ABC":
        g.add_node(n)
    _, ax = draw_graph(g, layout="spring")
    assert len(ax.texts) == 3 and len(ax.lines) == 0
    plt.close(ax.figure)


def test_custom_colors_sizes_and_highlight():
    """Colours, sizes and highlight groups are applied; bad input rejected."""
    g = Graph()
    g.add_edge("A", "B")
    g.add_node("C")
    _, ax = draw_graph(
        g,
        node_color={"A": "green"},
        node_size={"A": 50},
        highlight={"red": ["B"]},
    )
    sc = ax.collections[0]
    assert sc.get_sizes()[0] == 2500
    colors = [tuple(c[:3]) for c in sc.get_facecolors()]
    assert colors[0] == (0.0, 0.5019607843137255, 0.0)
    assert colors[1] == (1.0, 0.0, 0.0)
    plt.close(ax.figure)
    with pytest.raises(ValueError):
        draw_graph(g, highlight={"red": ["Z"]})
    with pytest.raises(ValueError):
        draw_graph(g, layout="nope")


def test_spring_layout_limits_overlaps():
    """Spring layout keeps nodes of a dense graph apart."""
    import math

    from pdl_graph.visualization import _spring_positions

    g = Graph()
    for i in range(12):
        g.add_edge(i, (i + 1) % 12)
        g.add_edge(i, (i + 5) % 12)
    pts = list(_spring_positions(list(g.adjacency), g.edges()).values())
    smallest = min(
        math.dist(p, q) for i, p in enumerate(pts) for q in pts[i + 1 :]
    )
    assert smallest > 0.1


def test_visualize_graph_is_public_alias():
    """visualize_graph is the same object as draw_graph (public alias).

    This ensures that code that uses the older ``visualize_graph`` name
    continues to call exactly the same function without any indirection.
    """
    assert visualize_graph is draw_graph
