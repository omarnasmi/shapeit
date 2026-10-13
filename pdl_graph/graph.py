"""Core graph data structure for :mod:`pdl_graph`.

This module exposes the :class:`Graph` class, an adjacency-list
implementation that supports both directed and undirected graphs.
Nodes can be any hashable Python object (strings, integers, …).

Typical usage
-------------
>>> from pdl_graph.graph import Graph
>>> g = Graph()
>>> g.add_edge("A", "B")
>>> g.add_edge("A", "C")
>>> g.neighbors("A")
['B', 'C']
>>> g.degree("A")
2
"""

from __future__ import annotations


class Graph:
    """Adjacency-list graph supporting directed and undirected modes.

    The graph is stored as a dictionary mapping each node to the **ordered**
    list of its neighbours.  All mutating operations (add/remove node/edge)
    maintain this dictionary in a consistent state.

    Attributes:
        directed (bool): ``True`` if edges are one-way (directed),
            ``False`` (default) if edges are bidirectional (undirected).
        adjacency (dict[object, list[object]]): Mapping from every node to
            the ordered list of nodes it is directly connected to.

    Example:
        Create an undirected triangle::

            >>> g = Graph()
            >>> g.add_edge("A", "B")
            >>> g.add_edge("B", "C")
            >>> g.add_edge("C", "A")
            >>> len(g.edges())
            3

        Create a directed graph::

            >>> dg = Graph(directed=True)
            >>> dg.add_edge("X", "Y")
            >>> dg.has_edge("X", "Y")
            True
            >>> dg.has_edge("Y", "X")
            False
    """

    def __init__(self, directed: bool = False) -> None:
        """Initialise an empty graph.

        Args:
            directed: When ``True`` the graph treats edges as one-way
                (i.e. adding an edge from *A* to *B* does **not**
                automatically add an edge from *B* to *A*).
                Defaults to ``False`` (undirected).

        Example:
            >>> g = Graph()
            >>> g.directed
            False
            >>> dg = Graph(directed=True)
            >>> dg.directed
            True
        """
        self.directed = directed
        self.adjacency: dict[object, list[object]] = {}

    # ------------------------------------------------------------------
    # Node operations
    # ------------------------------------------------------------------

    def add_node(self, node: object) -> None:
        """Add a node to the graph if it does not already exist.

        Calling this method on an existing node is a **no-op**; the node's
        neighbour list is left unchanged.

        Args:
            node: Any hashable object to use as the node identifier.

        Example:
            >>> g = Graph()
            >>> g.add_node("X")
            >>> "X" in g.adjacency
            True
            >>> g.add_node("X")  # duplicate → no-op
            >>> list(g.adjacency.keys())
            ['X']
        """
        if node not in self.adjacency:
            self.adjacency[node] = []

    def remove_node(self, node: object) -> None:
        """Remove a node and all edges that reference it.

        All occurrences of *node* in every neighbour list are deleted before
        the node entry itself is removed from :attr:`adjacency`.  If *node*
        does not exist, the method is a **no-op**.

        Args:
            node: Identifier of the node to remove.

        Example:
            >>> g = Graph()
            >>> g.add_edge("A", "B")
            >>> g.remove_node("B")
            >>> "B" in g.adjacency
            False
            >>> g.neighbors("A")
            []
        """
        if node in self.adjacency:
            del self.adjacency[node]

            for neighbors in self.adjacency.values():
                if node in neighbors:
                    neighbors.remove(node)

    # ------------------------------------------------------------------
    # Edge operations
    # ------------------------------------------------------------------

    def add_edge(self, source: object, target: object) -> None:
        """Add an edge between *source* and *target*.

        Both nodes are created automatically if they do not yet exist.
        Duplicate edges are silently ignored (the graph does not support
        multi-edges).

        For an **undirected** graph the reverse edge (*target* → *source*)
        is also added so that the neighbour lists remain symmetric.

        Args:
            source: Identifier of the origin node.
            target: Identifier of the destination node.

        Example:
            Undirected edge (both directions stored)::

                >>> g = Graph()
                >>> g.add_edge("A", "B")
                >>> g.neighbors("A")
                ['B']
                >>> g.neighbors("B")
                ['A']

            Directed edge (one direction only)::

                >>> dg = Graph(directed=True)
                >>> dg.add_edge("A", "B")
                >>> dg.neighbors("A")
                ['B']
                >>> dg.neighbors("B")
                []
        """
        self.add_node(source)
        self.add_node(target)

        if target not in self.adjacency[source]:
            self.adjacency[source].append(target)

        if not self.directed:
            if source not in self.adjacency[target]:
                self.adjacency[target].append(source)

    def remove_edge(self, source: object, target: object) -> None:
        """Remove the edge between *source* and *target*.

        For an **undirected** graph the reverse edge (*target* → *source*)
        is also removed.  If the edge does not exist the method is a
        **no-op** and no exception is raised.

        Args:
            source: Identifier of the origin node.
            target: Identifier of the destination node.

        Example:
            >>> g = Graph()
            >>> g.add_edge("A", "B")
            >>> g.remove_edge("A", "B")
            >>> g.has_edge("A", "B")
            False
            >>> g.has_edge("B", "A")
            False
        """
        if source in self.adjacency and target in self.adjacency[source]:
            self.adjacency[source].remove(target)

        if not self.directed:
            if target in self.adjacency and source in self.adjacency[target]:
                self.adjacency[target].remove(source)

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def edges(self) -> list[tuple[object, object]]:
        """Return all edges of the graph without duplicates.

        For a **directed** graph every ``(source, target)`` pair in
        :attr:`adjacency` is included as a separate directed edge.

        For an **undirected** graph each unordered pair ``{source, target}``
        appears exactly once in the returned list; the order of nodes within
        the tuple follows the iteration order of :attr:`adjacency`.

        Returns:
            A list of ``(source, target)`` tuples representing all edges.

        Example:
            Undirected graph — no duplicate edges::

                >>> g = Graph()
                >>> g.add_edge("A", "B")
                >>> g.edges()
                [('A', 'B')]

            Directed graph — both directions are distinct edges::

                >>> dg = Graph(directed=True)
                >>> dg.add_edge("A", "B")
                >>> dg.add_edge("B", "A")
                >>> sorted(dg.edges())
                [('A', 'B'), ('B', 'A')]
        """
        result: list[tuple[object, object]] = []
        seen: set[frozenset] = set()

        for source, neighbors in self.adjacency.items():
            for target in neighbors:
                if self.directed:
                    result.append((source, target))
                else:
                    edge = frozenset((source, target))

                    if edge not in seen:
                        seen.add(edge)
                        result.append((source, target))

        return result

    def has_edge(self, source: object, target: object) -> bool:
        """Check whether a direct edge from *source* to *target* exists.

        For an **undirected** graph, ``has_edge(A, B)`` and
        ``has_edge(B, A)`` always return the same value because both
        directions are stored.

        Args:
            source: Identifier of the origin node.
            target: Identifier of the destination node.

        Returns:
            ``True`` if the edge exists, ``False`` otherwise (including
            when either node is absent from the graph).

        Example:
            >>> g = Graph()
            >>> g.add_edge("A", "B")
            >>> g.has_edge("A", "B")
            True
            >>> g.has_edge("B", "A")
            True
            >>> g.has_edge("A", "C")
            False
        """
        return target in self.adjacency.get(source, [])

    def neighbors(self, node: object) -> list[object]:
        """Return the list of direct neighbours of *node*.

        For an **undirected** graph, if an edge ``(A, B)`` exists then *B*
        appears in ``neighbors("A")`` and *A* appears in ``neighbors("B")``.

        Args:
            node: Identifier of the node whose neighbours are requested.

        Returns:
            An ordered list of neighbour node identifiers, or an empty list
            if *node* is not in the graph.

        Example:
            >>> g = Graph()
            >>> g.add_edge("A", "B")
            >>> g.add_edge("A", "C")
            >>> g.neighbors("A")
            ['B', 'C']
            >>> g.neighbors("Z")  # unknown node
            []
        """
        return self.adjacency.get(node, [])

    def degree(self, node: object) -> int:
        """Return the degree of *node* (number of direct neighbours).

        For an **undirected** graph this is the number of edges incident to
        *node*.  For a **directed** graph this is the *out-degree* (number
        of outgoing edges), since only the outgoing adjacency list is stored
        per node.

        Args:
            node: Identifier of the node.

        Returns:
            The degree as a non-negative integer.  Returns ``0`` if *node*
            is not in the graph.

        Example:
            >>> g = Graph()
            >>> g.add_edge("A", "B")
            >>> g.add_edge("A", "C")
            >>> g.degree("A")
            2
            >>> g.degree("B")
            1
            >>> g.degree("Z")  # unknown node
            0
        """
        if node not in self.adjacency:
            return 0

        return len(self.adjacency[node])

    def adjacency_matrix(
        self,
    ) -> tuple[list[object], list[list[int]]]:
        """Return a matrix representation of the graph's adjacency.

        The node order in the returned list determines both the row and
        column indices of the matrix.  The order follows the insertion
        order of nodes in :attr:`adjacency` (Python ≥ 3.7 dict ordering).

        Returns:
            A two-element tuple ``(nodes, matrix)`` where:

            - **nodes** – ordered list of all node identifiers.
            - **matrix** – a square ``N × N`` list-of-lists of ``int``
              values where ``matrix[i][j]`` is ``1`` when an edge from
              ``nodes[i]`` to ``nodes[j]`` exists, and ``0`` otherwise.

        Example:
            >>> g = Graph()
            >>> g.add_edge("A", "B")
            >>> nodes, mat = g.adjacency_matrix()
            >>> nodes
            ['A', 'B']
            >>> mat
            [[0, 1], [1, 0]]
        """
        nodes = list(self.adjacency.keys())
        matrix: list[list[int]] = []

        for source in nodes:
            row: list[int] = []

            for target in nodes:
                if target in self.adjacency[source]:
                    row.append(1)
                else:
                    row.append(0)

            matrix.append(row)

        return nodes, matrix

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """Return a human-readable representation of the adjacency mapping.

        The output is the string form of :attr:`adjacency` and is primarily
        intended for quick debugging in interactive sessions.

        Returns:
            String representation of the internal adjacency dictionary.

        Example:
            >>> g = Graph()
            >>> g.add_edge("A", "B")
            >>> print(g)
            {'A': ['B'], 'B': ['A']}
        """
        return str(self.adjacency)
