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

def test_adjacency_matrix():
    g = Graph()

    g.add_edge("A", "B")

    nodes, matrix = g.adjacency_matrix()

    assert nodes == ["A", "B"]
    assert matrix == [
        [0, 1],
        [1, 0]
    ]
    
def test_degree():
    g = Graph()

    g.add_edge("A", "B")
    g.add_edge("A", "C")

    assert g.degree("A") == 2
    assert g.degree("B") == 1
    assert g.degree("C") == 1