"""Unit tests for the Sprint 3 graph algorithms of :class:`~pdl_graph.Graph`.

Covers:
- Breadth-first search (:meth:`Graph.bfs`)
- Depth-first search (:meth:`Graph.dfs`)
- Random walk (:meth:`Graph.random_walk`)
- Shortest path (:meth:`Graph.shortest_path`)
- Greedy vertex coloring (:meth:`Graph.graph_coloring`)
"""

import pytest

from pdl_graph import Graph


# ----------------------------------------------------------------------
# Breadth-First Search (BFS)
# ----------------------------------------------------------------------


def test_bfs_tree_level_order():
    """BFS visits vertices level by level in insertion order."""
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("B", "E")
    g.add_edge("C", "F")

    assert g.bfs("A") == ["A", "B", "C", "D", "E", "F"]


def test_bfs_graph_with_cycle():
    """BFS visits each reachable vertex exactly once even in presence of cycles."""
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "A")
    g.add_edge("C", "D")

    order = g.bfs("A")

    assert order == ["A", "B", "C", "D"]
    assert len(order) == len(set(order))


def test_bfs_directed_graph():
    """BFS respects edge direction in a directed graph."""
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("D", "A")  # incoming to A, not reachable from A

    assert g.bfs("A") == ["A", "B", "C"]
    assert g.bfs("C") == ["C"]


def test_bfs_disconnected_graph():
    """BFS only returns vertices in the connected component of the start node."""
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("C", "D")
    g.add_node("E")

    assert g.bfs("A") == ["A", "B"]
    assert g.bfs("C") == ["C", "D"]


def test_bfs_isolated_and_self_loop_node():
    """BFS on an isolated node or a node with a self-loop returns only that node."""
    g = Graph()
    g.add_node("A")
    g.add_edge("B", "B")

    assert g.bfs("A") == ["A"]
    assert g.bfs("B") == ["B"]


def test_bfs_empty_graph_and_nonexistent_node():
    """BFS raises ValueError when the starting node does not exist."""
    empty = Graph()
    with pytest.raises(ValueError, match="starting node"):
        empty.bfs("A")

    g = Graph()
    g.add_node("A")
    with pytest.raises(ValueError, match="starting node"):
        g.bfs("Z")


# ----------------------------------------------------------------------
# Depth-First Search (DFS)
# ----------------------------------------------------------------------


def test_dfs_tree_depth_order():
    """DFS explores each branch to its depth before backtracking."""
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "D")
    g.add_edge("B", "E")
    g.add_edge("C", "F")

    assert g.dfs("A") == ["A", "B", "D", "E", "C", "F"]


def test_dfs_graph_with_cycle():
    """DFS does not get stuck in cycles and visits each reachable node once."""
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "A")
    g.add_edge("C", "D")

    order = g.dfs("A")

    assert len(order) == 4
    assert set(order) == {"A", "B", "C", "D"}
    assert order[0] == "A"


def test_dfs_directed_graph():
    """DFS follows only outgoing edges in a directed graph."""
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("D", "A")

    assert g.dfs("A") == ["A", "B", "C"]
    assert g.dfs("B") == ["B", "C"]


def test_dfs_disconnected_graph():
    """DFS only visits the component reachable from the start node."""
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("C", "D")

    assert g.dfs("A") == ["A", "B"]
    assert g.dfs("C") == ["C", "D"]


def test_dfs_isolated_node():
    """DFS starting on an isolated node returns a single-element list."""
    g = Graph()
    g.add_node("X")

    assert g.dfs("X") == ["X"]


def test_dfs_empty_graph_and_nonexistent_node():
    """DFS raises ValueError when the starting node is missing."""
    with pytest.raises(ValueError, match="starting node"):
        Graph().dfs("A")

    g = Graph()
    g.add_node("A")
    with pytest.raises(ValueError, match="starting node"):
        g.dfs("UNKNOWN")


# ----------------------------------------------------------------------
# Random Walk
# ----------------------------------------------------------------------


def test_random_walk_valid_transitions_and_length():
    """Every step in a random walk traverses an existing edge in the graph."""
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "D")
    g.add_edge("D", "A")
    g.add_edge("A", "C")

    walk = g.random_walk("A", steps=15, seed=123)

    assert walk[0] == "A"
    assert len(walk) == 16
    for u, v in zip(walk, walk[1:]):
        assert g.has_edge(u, v)


def test_random_walk_reproducible_with_seed():
    """Two random walks with the same seed produce the exact same sequence."""
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "C")

    walk1 = g.random_walk("A", steps=10, seed=42)
    walk2 = g.random_walk("A", steps=10, seed=42)

    assert walk1 == walk2


def test_random_walk_zero_steps():
    """A random walk of 0 steps returns only the starting node."""
    g = Graph()
    g.add_edge("A", "B")

    assert g.random_walk("A", steps=0, seed=1) == ["A"]


def test_random_walk_isolated_node_stops_early():
    """A random walk on an isolated node cannot move and returns [start]."""
    g = Graph()
    g.add_node("A")

    assert g.random_walk("A", steps=5, seed=1) == ["A"]


def test_random_walk_directed_dead_end():
    """In a directed graph, the walk stops early when reaching a sink node."""
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("B", "C")  # C has no outgoing edges

    walk = g.random_walk("A", steps=10, seed=7)

    assert walk == ["A", "B", "C"]
    for u, v in zip(walk, walk[1:]):
        assert g.has_edge(u, v)


def test_random_walk_invalid_inputs():
    """Random walk rejects missing start nodes and invalid step counts."""
    g = Graph()
    g.add_node("A")

    with pytest.raises(ValueError, match="starting node"):
        g.random_walk("MISSING", steps=3)

    with pytest.raises(ValueError, match="non-negative integer"):
        g.random_walk("A", steps=-1)

    with pytest.raises(ValueError, match="non-negative integer"):
        g.random_walk("A", steps=2.5)  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="non-negative integer"):
        g.random_walk("A", steps=True)


# ----------------------------------------------------------------------
# Shortest Path (Bellman-Ford)
# ----------------------------------------------------------------------


def test_shortest_path_undirected_weighted():
    """Shortest path finds the minimum-cost route in an undirected weighted graph."""
    g = Graph()
    g.add_edge("A", "B", 10)
    g.add_edge("A", "C", 2)
    g.add_edge("C", "D", 3)
    g.add_edge("D", "B", 1)

    path, distance = g.shortest_path("A", "B")

    assert path == ["A", "C", "D", "B"]
    assert distance == 6


def test_shortest_path_directed_negative_weights():
    """Bellman-Ford handles negative weights in a directed graph without negative cycles."""
    g = Graph(directed=True)
    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 5)
    g.add_edge("B", "C", -2)
    g.add_edge("C", "D", 3)

    path, distance = g.shortest_path("A", "D")

    assert path == ["A", "B", "C", "D"]
    assert distance == 5


def test_shortest_path_negative_cycle_raises():
    """Bellman-Ford raises ValueError when a negative-weight cycle is reachable."""
    g = Graph(directed=True)
    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", -3)
    g.add_edge("C", "A", 1)

    with pytest.raises(ValueError, match="negative-weight cycle"):
        g.shortest_path("A", "C")


def test_shortest_path_disconnected_and_unreachable_directed():
    """Shortest path raises ValueError when destination is unreachable."""
    undirected = Graph()
    undirected.add_edge("A", "B")
    undirected.add_edge("C", "D")

    with pytest.raises(ValueError, match="No path exists"):
        undirected.shortest_path("A", "D")

    directed = Graph(directed=True)
    directed.add_edge("A", "B")
    directed.add_edge("C", "B")

    with pytest.raises(ValueError, match="No path exists"):
        directed.shortest_path("A", "C")


def test_shortest_path_empty_and_nonexistent_nodes():
    """Shortest path raises ValueError on empty graphs or nonexistent endpoints."""
    with pytest.raises(ValueError, match="starting node"):
        Graph().shortest_path("A", "B")

    g = Graph()
    g.add_node("A")
    with pytest.raises(ValueError, match="destination node"):
        g.shortest_path("A", "B")
    with pytest.raises(ValueError, match="starting node"):
        g.shortest_path("B", "A")


# ----------------------------------------------------------------------
# Graph Coloring (Greedy)
# ----------------------------------------------------------------------


def assert_valid_coloring(graph: Graph, colors: dict[object, int]) -> None:
    """Assert that every vertex has a color and no two distinct adjacent vertices share one."""
    assert set(colors.keys()) == set(graph.adjacency.keys())
    for u, v in graph.edges():
        if u != v:
            assert colors[u] != colors[v]


def test_coloring_empty_and_isolated():
    """Empty graph returns {} and isolated nodes get color 0."""
    assert Graph().graph_coloring() == {}

    g = Graph()
    g.add_node("Solo")
    assert g.graph_coloring() == {"Solo": 0}


def test_coloring_even_and_odd_cycles():
    """Even cycle C_4 uses 2 colors; odd cycle C_5 uses 3 colors."""
    c4 = Graph()
    for a, b in [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A")]:
        c4.add_edge(a, b)
    colors_c4 = c4.graph_coloring()
    assert_valid_coloring(c4, colors_c4)
    assert len(set(colors_c4.values())) == 2

    c5 = Graph()
    for a, b in [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]:
        c5.add_edge(a, b)
    colors_c5 = c5.graph_coloring()
    assert_valid_coloring(c5, colors_c5)
    assert len(set(colors_c5.values())) == 3


@pytest.mark.parametrize("n", [1, 2, 4, 6])
def test_coloring_complete_graph_uses_n_colors(n):
    """A complete graph K_n requires exactly n distinct colors."""
    g = Graph()
    for i in range(n):
        g.add_node(i)
        for j in range(i + 1, n):
            g.add_edge(i, j)

    colors = g.graph_coloring()

    assert_valid_coloring(g, colors)
    assert len(set(colors.values())) == n


def test_coloring_disconnected_components_and_isolated_vertices():
    """Disconnected components and isolated nodes are all validly colored."""
    g = Graph()
    # Component 1: triangle
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "A")
    # Component 2: star
    g.add_edge("X", "Y1")
    g.add_edge("X", "Y2")
    g.add_edge("X", "Y3")
    # Component 3: isolated node
    g.add_node("ISO")

    colors = g.graph_coloring()

    assert_valid_coloring(g, colors)
    assert colors["ISO"] == 0
    assert len(set(colors.values())) == 3
