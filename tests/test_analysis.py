"""Unit tests for the Sprint 2 analysis methods of :class:`Graph`."""

import pytest

from pdl_graph import Graph


def complete(n, directed=False):
    g = Graph(directed=directed)
    for i in range(n):
        for j in range(n):
            if i != j:
                g.add_edge(i, j)
    return g


# --------------------------------------------------------------- degree
def test_degree_unknown_node_is_zero():
    assert Graph().degree("X") == 0


def test_degree_isolated_node():
    g = Graph()
    g.add_node("A")
    assert g.degree("A") == 0


def test_degree_after_removals():
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.remove_edge("A", "B")
    assert g.degree("A") == 1
    g.remove_node("C")
    assert g.degree("A") == 0


def test_degree_duplicate_edges_counted_once():
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("A", "B")
    g.add_edge("B", "A")
    assert g.degree("A") == 1


def test_degree_self_loop():
    g = Graph()
    g.add_edge("A", "A")
    assert g.degree("A") == 1


def test_degree_directed_is_out_degree():
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("D", "A")
    assert g.degree("A") == 2
    assert g.degree("B") == 0
    assert g.degree("D") == 1


@pytest.mark.parametrize("n", [2, 3, 5])
def test_degree_complete_graph(n):
    g = complete(n)
    assert all(g.degree(i) == n - 1 for i in range(n))


# -------------------------------------------------------------- density
def test_density_empty_and_single():
    assert Graph().density() == 0.0
    assert Graph(directed=True).density() == 0.0
    g = Graph()
    g.add_node("A")
    assert g.density() == 0.0


@pytest.mark.parametrize("n", [2, 3, 4, 6])
@pytest.mark.parametrize("directed", [False, True])
def test_density_complete(n, directed):
    assert complete(n, directed).density() == 1.0


def test_density_partial_undirected():
    g = Graph()
    for a, b in [(1, 2), (2, 3), (3, 4)]:
        g.add_edge(a, b)
    assert g.density() == pytest.approx(0.5)  # 3 / 6


def test_density_partial_directed():
    g = Graph(directed=True)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_node(4)
    assert g.density() == pytest.approx(2 / 12)


def test_density_nodes_without_edges():
    g = Graph()
    for n in "ABC":
        g.add_node(n)
    assert g.density() == 0.0


def test_density_ignores_self_loops():
    g = Graph(directed=True)
    g.add_edge("A", "A")
    g.add_edge("A", "B")
    assert g.density() == pytest.approx(0.5)


def test_density_bounds():
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    assert 0.0 <= g.density() <= 1.0


# ------------------------------------------------- connected components
def norm(components):
    return sorted(sorted(c) for c in components)


def test_components_empty_graph():
    assert Graph().connected_components() == []
    assert Graph(directed=True).connected_components() == []


def test_components_single_and_isolated_nodes():
    g = Graph()
    g.add_node("A")
    assert g.connected_components() == [["A"]]
    g.add_node("B")
    assert norm(g.connected_components()) == [["A"], ["B"]]


def test_components_connected_graph():
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "A")
    assert norm(g.connected_components()) == [["A", "B", "C"]]


def test_components_multiple():
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("C", "D")
    g.add_edge("D", "E")
    g.add_node("F")
    assert norm(g.connected_components()) == [
        ["A", "B"],
        ["C", "D", "E"],
        ["F"],
    ]


def test_components_cover_every_node_once():
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(3, 4)
    g.add_node(5)
    flat = [n for c in g.connected_components() for n in c]
    assert sorted(flat) == sorted(g.adjacency)


def test_components_self_loop():
    g = Graph()
    g.add_edge("A", "A")
    assert g.connected_components() == [["A"]]


def test_components_directed_are_weak():
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("C", "B")
    g.add_node("D")
    assert norm(g.connected_components()) == [["A", "B", "C"], ["D"]]


def test_components_after_edge_removal_splits():
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.remove_edge("B", "C")
    assert norm(g.connected_components()) == [["A", "B"], ["C"]]


def test_components_do_not_modify_graph():
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.connected_components()
    assert g.adjacency == {"A": ["B"], "B": []}


# ----------------------------------------------------- adjacency matrix
def test_matrix_empty_graph():
    assert Graph().adjacency_matrix() == ([], [])


def test_matrix_single_node():
    g = Graph()
    g.add_node("A")
    assert g.adjacency_matrix() == (["A"], [[0]])


def test_matrix_undirected_is_symmetric():
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    nodes, m = g.adjacency_matrix()
    assert nodes == ["A", "B", "C"]
    assert m == [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
    assert all(m[i][j] == m[j][i] for i in range(3) for j in range(3))


def test_matrix_directed_is_not_symmetric():
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    nodes, m = g.adjacency_matrix()
    assert nodes == ["A", "B", "C"]
    assert m == [[0, 1, 0], [0, 0, 1], [0, 0, 0]]


def test_matrix_self_loop_and_isolated_node():
    g = Graph()
    g.add_edge("A", "A")
    g.add_node("B")
    assert g.adjacency_matrix() == (["A", "B"], [[1, 0], [0, 0]])


def test_matrix_complete_graph():
    nodes, m = complete(3).adjacency_matrix()
    assert m == [[0, 1, 1], [1, 0, 1], [1, 1, 0]]


def test_matrix_row_sums_match_degrees():
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    nodes, m = g.adjacency_matrix()
    assert [sum(row) for row in m] == [g.degree(n) for n in nodes]
