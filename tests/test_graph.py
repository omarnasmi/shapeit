from pdl_graph import Graph


def test_add_node():
    g = Graph()

    g.add_node("A")

    assert "A" in g.adjacency


def test_add_edge():
    g = Graph()

    g.add_edge("A", "B")

    assert "B" in g.neighbors("A")
    assert "A" in g.neighbors("B")


def test_remove_edge():
    g = Graph()

    g.add_edge("A", "B")
    g.remove_edge("A", "B")

    assert "B" not in g.neighbors("A")
    assert "A" not in g.neighbors("B")


def test_remove_node():
    g = Graph()

    g.add_edge("A", "B")
    g.remove_node("B")

    assert "B" not in g.adjacency
    assert "B" not in g.neighbors("A")


def test_directed_graph():
    g = Graph(directed=True)

    g.add_edge("A", "B")

    assert "B" in g.neighbors("A")
    assert "A" not in g.neighbors("B")
    