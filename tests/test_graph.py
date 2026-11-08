"""Tests for :class:`~pdl_graph.Graph`.

Each test function exercises a single public method or a closely related
pair of methods to keep failure messages narrow and easy to diagnose.
Tests follow the **Arrange / Act / Assert** pattern.
"""

from pdl_graph import Graph


def test_add_node():
    """Adding a node inserts it into the adjacency mapping with no neighbours.

    A newly added node must appear as a key in :attr:`~pdl_graph.Graph.adjacency`
    with an empty neighbour list.
    """
    g = Graph()

    g.add_node("A")

    assert "A" in g.adjacency


def test_add_edge():
    """Adding an undirected edge registers both directions in the adjacency mapping.

    For an undirected graph, ``add_edge(A, B)`` must make *B* a neighbour of
    *A* **and** *A* a neighbour of *B*.
    """
    g = Graph()

    g.add_edge("A", "B")

    assert "B" in g.neighbors("A")
    assert "A" in g.neighbors("B")


def test_remove_edge():
    """Removing an undirected edge clears both directions.

    After ``remove_edge(A, B)`` neither *B* should appear in the neighbours
    of *A* nor *A* in the neighbours of *B*.
    """
    g = Graph()

    g.add_edge("A", "B")
    g.remove_edge("A", "B")

    assert "B" not in g.neighbors("A")
    assert "A" not in g.neighbors("B")


def test_remove_node():
    """Removing a node deletes it and all references to it from other adjacency lists.

    After ``remove_node(B)``:
    - *B* must not be present as a key in :attr:`~pdl_graph.Graph.adjacency`.
    - *B* must not appear in the neighbour list of any remaining node.
    """
    g = Graph()

    g.add_edge("A", "B")
    g.remove_node("B")

    assert "B" not in g.adjacency
    assert "B" not in g.neighbors("A")


def test_directed_graph():
    """A directed graph only stores the edge in the stated direction.

    After ``add_edge(A, B)`` on a directed graph, *B* should be a neighbour
    of *A* but *A* must **not** be a neighbour of *B*.
    """
    g = Graph(directed=True)

    g.add_edge("A", "B")

    assert "B" in g.neighbors("A")
    assert "A" not in g.neighbors("B")


def test_adjacency_matrix():
    """The adjacency matrix correctly reflects a single undirected edge.

    For a graph with one edge ``(A, B)``, the matrix should be::

        nodes = ["A", "B"]
        matrix = [[0, 1],
                  [1, 0]]
    """
    g = Graph()

    g.add_edge("A", "B")

    nodes, matrix = g.adjacency_matrix()

    assert nodes == ["A", "B"]
    assert matrix == [
        [0, 1],
        [1, 0]
    ]


def test_degree():
    """The degree of a node equals the number of its direct neighbours.

    Node *A* is connected to both *B* and *C* so its degree must be 2,
    while *B* and *C* each have degree 1.
    """
    g = Graph()

    g.add_edge("A", "B")
    g.add_edge("A", "C")

    assert g.degree("A") == 2
    assert g.degree("B") == 1
    assert g.degree("C") == 1


def test_has_edge():
    """has_edge returns True for existing edges and False otherwise.

    For an undirected graph both ``has_edge(A, B)`` and ``has_edge(B, A)``
    must return ``True`` when the edge exists.  A query for a non-existent
    edge must return ``False``.
    """
    g = Graph()

    g.add_edge("A", "B")

    assert g.has_edge("A", "B")
    assert g.has_edge("B", "A")
    assert not g.has_edge("A", "C")


def test_edges():
    """edges() returns every undirected edge exactly once.

    For an undirected graph with two edges ``(A-B)`` and ``(A-C)`` the
    returned list must have length 2 and contain both tuples.
    """
    g = Graph()

    g.add_edge("A", "B")
    g.add_edge("A", "C")

    assert len(g.edges()) == 2
    assert ("A", "B") in g.edges()
    assert ("A", "C") in g.edges()


def test_edges_directed():
    """edges() for a directed graph includes each directed edge independently.

    Adding ``(A→B)`` and ``(B→A)`` to a directed graph must yield two
    distinct entries in :meth:`~pdl_graph.Graph.edges`.
    """
    g = Graph(directed=True)

    g.add_edge("A", "B")
    g.add_edge("B", "A")

    assert len(g.edges()) == 2
    assert ("A", "B") in g.edges()
    assert ("B", "A") in g.edges()



def test_density_empty_graph():
    """An empty graph has density 0."""
    g = Graph()
    assert g.density() == 0.0


def test_density_single_node():
    """A graph with one node has density 0."""
    g = Graph()
    g.add_node("A")
    assert g.density() == 0.0


def test_density_without_edges():
    """A graph without edges has density 0."""
    g = Graph()
    g.add_node("A")
    g.add_node("B")
    assert g.density() == 0.0


def test_density_undirected_graph():
    """Check density of a partially connected undirected graph."""
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")

    assert g.density() == 2 / 3


def test_density_directed_graph():
    """Check density of a partially connected directed graph."""
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("B", "C")

    assert g.density() == 1 / 3


def test_density_complete_graph():
    """A complete undirected graph has density 1."""
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "C")

    assert g.density() == 1.0


def test_density_self_loop():
    """Self-loops are ignored in the density calculation."""
    g = Graph()
    g.add_edge("A", "A")
    g.add_node("B")

    assert g.density() == 0.0


def test_density_complete_directed_graph():
    """A complete directed graph has density 1."""
    g = Graph(directed=True)
    g.add_edge("A", "B")
    g.add_edge("B", "A")

    assert g.density() == 1.0

def test_default_edge_weight():
    """An edge without an explicit weight has a default weight of 1."""
    g = Graph()

    g.add_edge("A", "B")

    assert g.get_edge_weight("A", "B") == 1
    assert g.get_edge_weight("B", "A") == 1


def test_custom_edge_weight():
    """An edge can store and return a custom numerical weight."""
    g = Graph()

    g.add_edge("A", "B", 5)

    assert g.get_edge_weight("A", "B") == 5
    assert g.get_edge_weight("B", "A") == 5


def test_directed_edge_weight():
    """A directed graph stores the weight only in the given direction."""
    g = Graph(directed=True)

    g.add_edge("A", "B", 4)

    assert g.get_edge_weight("A", "B") == 4


def test_remove_edge_removes_weight():
    """Removing an edge also removes its stored weight."""
    g = Graph()

    g.add_edge("A", "B", 6)
    g.remove_edge("A", "B")

    assert ("A", "B") not in g.weights
    assert ("B", "A") not in g.weights


def test_remove_node_removes_weights():
    """Removing a node also removes every weight linked to that node."""
    g = Graph()

    g.add_edge("A", "B", 3)
    g.add_edge("B", "C", 7)

    g.remove_node("B")

    assert ("A", "B") not in g.weights
    assert ("B", "A") not in g.weights
    assert ("B", "C") not in g.weights
    assert ("C", "B") not in g.weights


def test_invalid_edge_weight():
    """A non-numeric edge weight must be rejected."""
    g = Graph()

    try:
        g.add_edge("A", "B", "invalid")
        assert False
    except TypeError:
        pass


def test_shortest_path_weighted():
    """Dijkstra returns the shortest weighted path and its total distance."""
    g = Graph()

    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 2)
    g.add_edge("C", "B", 1)
    g.add_edge("B", "D", 3)
    g.add_edge("C", "D", 7)

    path, distance = g.shortest_path("A", "D")

    assert path == ["A", "C", "B", "D"]
    assert distance == 6


def test_shortest_path_unweighted():
    """Unweighted edges are treated as having a cost of 1."""
    g = Graph()

    g.add_edge("A", "B")
    g.add_edge("B", "C")

    path, distance = g.shortest_path("A", "C")

    assert path == ["A", "B", "C"]
    assert distance == 2


def test_shortest_path_directed():
    """Shortest path respects edge direction in a directed graph."""
    g = Graph(directed=True)

    g.add_edge("A", "B", 2)
    g.add_edge("B", "C", 3)

    path, distance = g.shortest_path("A", "C")

    assert path == ["A", "B", "C"]
    assert distance == 5


def test_shortest_path_same_node():
    """The shortest path from a node to itself has distance 0."""
    g = Graph()

    g.add_node("A")

    path, distance = g.shortest_path("A", "A")

    assert path == ["A"]
    assert distance == 0


def test_shortest_path_missing_start():
    """A missing starting node must raise ValueError."""
    g = Graph()

    g.add_node("B")

    try:
        g.shortest_path("A", "B")
        assert False
    except ValueError:
        pass


def test_shortest_path_missing_end():
    """A missing destination node must raise ValueError."""
    g = Graph()

    g.add_node("A")

    try:
        g.shortest_path("A", "B")
        assert False
    except ValueError:
        pass


def test_shortest_path_no_path():
    """A graph with no route between the nodes must raise ValueError."""
    g = Graph()

    g.add_node("A")
    g.add_node("B")

    try:
        g.shortest_path("A", "B")
        assert False
    except ValueError:
        pass


def test_shortest_path_negative_weight():
    """Dijkstra must reject negative edge weights."""
    g = Graph()

    g.add_edge("A", "B", -2)

    try:
        g.shortest_path("A", "B")
        assert False
    except ValueError:
        pass