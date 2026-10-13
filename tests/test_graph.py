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
