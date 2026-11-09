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

import random
from collections import deque

class Graph:
    """Adjacency-list graph supporting directed and undirected modes.

    The graph is stored as a dictionary mapping each node to the ordered
    list of its neighbours.

    Attributes:
        directed (bool): True if the graph is directed.
        adjacency (dict): Mapping from each node to its neighbours.
        weights (dict): Mapping from an edge to its numerical weight.
    """

    def __init__(self, directed: bool = False) -> None:
        """Initialise an empty graph.

        Args:
            directed: When True, edges are one-way.
                Defaults to False.
        """
        self.directed = directed
        self.adjacency: dict[object, list[object]] = {}

        # Edge weights are stored separately so that the existing
        # adjacency-list representation remains compatible.
        self.weights: dict[
            tuple[object, object],
            int | float,
        ] = {}

    # ------------------------------------------------------------------
    # Node operations
    # ------------------------------------------------------------------

    def add_node(self, node: object) -> None:
        """Add a node if it does not already exist."""
        if node not in self.adjacency:
            self.adjacency[node] = []

    def remove_node(self, node: object) -> None:
        """Remove a node and all edges associated with it."""
        if node not in self.adjacency:
            return

        del self.adjacency[node]

        # Remove the node from all neighbour lists.
        for neighbors in self.adjacency.values():
            if node in neighbors:
                neighbors.remove(node)

        # Remove all weights related to the deleted node.
        edges_to_remove = [
            edge
            for edge in self.weights
            if node in edge
        ]

        for edge in edges_to_remove:
            del self.weights[edge]

    # ------------------------------------------------------------------
    # Edge operations
    # ------------------------------------------------------------------

    def add_edge(
        self,
        source: object,
        target: object,
        weight: int | float = 1,
    ) -> None:
        """Add an edge between source and target.

        Nodes are automatically created if necessary.

        Args:
            source: Origin node.
            target: Destination node.
            weight: Numerical edge weight. Defaults to 1.

        Raises:
            TypeError: If weight is not numeric.
        """
        if (
            not isinstance(weight, (int, float))
            or isinstance(weight, bool)
        ):
            raise TypeError(
                "The edge weight must be numeric."
            )

        self.add_node(source)
        self.add_node(target)

        if target not in self.adjacency[source]:
            self.adjacency[source].append(target)

        self.weights[(source, target)] = weight

        if not self.directed:
            if source not in self.adjacency[target]:
                self.adjacency[target].append(source)

            self.weights[(target, source)] = weight

    def remove_edge(
        self,
        source: object,
        target: object,
    ) -> None:
        """Remove an edge and its associated weight."""
        if (
            source in self.adjacency
            and target in self.adjacency[source]
        ):
            self.adjacency[source].remove(target)

        self.weights.pop((source, target), None)

        if not self.directed:
            if (
                target in self.adjacency
                and source in self.adjacency[target]
            ):
                self.adjacency[target].remove(source)

            self.weights.pop((target, source), None)

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------

    def edges(self) -> list[tuple[object, object]]:
        """Return all edges without duplicates.

        Directed graphs keep every directed edge.
        Undirected graphs return each edge only once.
        """
        result: list[tuple[object, object]] = []
        seen: set[frozenset] = set()

        for source, neighbors in self.adjacency.items():
            for target in neighbors:
                if self.directed:
                    result.append((source, target))
                else:
                    edge = frozenset(
                        (source, target)
                    )

                    if edge not in seen:
                        seen.add(edge)
                        result.append(
                            (source, target)
                        )

        return result

    def has_edge(
        self,
        source: object,
        target: object,
    ) -> bool:
        """Return True if an edge exists."""
        return target in self.adjacency.get(
            source,
            [],
        )

    def get_edge_weight(
        self,
        source: object,
        target: object,
    ) -> int | float:
        """Return the weight associated with an edge.

        Raises:
            ValueError: If the edge does not exist.
        """
        if not self.has_edge(source, target):
            raise ValueError(
                f"The edge ({source!r}, {target!r}) "
                "does not exist."
            )

        return self.weights[
            (source, target)
        ]

    def neighbors(
        self,
        node: object,
    ) -> list[object]:
        """Return the direct neighbours of a node."""
        return self.adjacency.get(
            node,
            [],
        )

    def degree(
        self,
        node: object,
        mode: str = "out",
    ) -> int:
        """Calculate the degree of a node.

        For directed graphs:
        - out: outgoing degree
        - in: incoming degree
        - total: incoming + outgoing

        For undirected graphs, a self-loop counts twice.
        """
        if node not in self.adjacency:
            return 0

        if not self.directed:
            node_degree = len(
                self.adjacency[node]
            )

            if node in self.adjacency[node]:
                node_degree += 1

            return node_degree

        out_degree = len(
            self.adjacency[node]
        )

        in_degree = sum(
            1
            for neighbors
            in self.adjacency.values()
            if node in neighbors
        )

        if mode == "in":
            return in_degree

        if mode == "out":
            return out_degree

        if mode == "total":
            return in_degree + out_degree

        raise ValueError(
            "mode must be 'in', 'out' or 'total'"
        )

    def density(self) -> float:
        """Calculate graph density.

        Self-loops are ignored.
        """
        n = len(self.adjacency)

        if n < 2:
            return 0.0

        m = sum(
            1
            for source, target in self.edges()
            if source != target
        )

        if self.directed:
            return m / (
                n * (n - 1)
            )

        return (
            2 * m
        ) / (
            n * (n - 1)
        )

    # ------------------------------------------------------------------
    # Connected components
    # ------------------------------------------------------------------

    def connected_components(
        self,
    ) -> list[set]:
        """Find connected components.

        For directed graphs, weak connectivity is used.
        """
        visited = set()
        components = []

        connections = {
            node: set()
            for node in self.adjacency
        }

        for source, neighbors in (
            self.adjacency.items()
        ):
            for target in neighbors:
                connections[source].add(
                    target
                )
                connections[target].add(
                    source
                )

        for node in self.adjacency:
            if node in visited:
                continue

            component = set()
            stack = [node]

            visited.add(node)

            while stack:
                current = stack.pop()
                component.add(current)

                for neighbor in (
                    connections[current]
                ):
                    if neighbor not in visited:
                        visited.add(
                            neighbor
                        )
                        stack.append(
                            neighbor
                        )

            components.append(
                component
            )

        return components

    def strongly_connected_components(
        self,
    ) -> list[set]:
        """Find strongly connected components.

        Kosaraju's algorithm is used for directed graphs.
        """
        if not self.directed:
            return self.connected_components()

        visited = set()
        order = []

        # First DFS: finishing order.
        for start in self.adjacency:
            if start in visited:
                continue

            visited.add(start)

            stack = [
                (
                    start,
                    iter(
                        self.adjacency[start]
                    ),
                )
            ]

            while stack:
                node, neighbors = stack[-1]

                neighbor = next(
                    neighbors,
                    None,
                )

                if neighbor is None:
                    order.append(node)
                    stack.pop()

                elif neighbor not in visited:
                    visited.add(
                        neighbor
                    )

                    stack.append(
                        (
                            neighbor,
                            iter(
                                self.adjacency[
                                    neighbor
                                ]
                            ),
                        )
                    )

        # Reverse graph.
        reversed_graph = {
            node: []
            for node in self.adjacency
        }

        for source, neighbors in (
            self.adjacency.items()
        ):
            for target in neighbors:
                reversed_graph[
                    target
                ].append(source)

        visited.clear()
        components = []

        # Second DFS.
        for start in reversed(order):
            if start in visited:
                continue

            component = set()
            stack = [start]

            visited.add(start)

            while stack:
                node = stack.pop()
                component.add(node)

                for neighbor in (
                    reversed_graph[node]
                ):
                    if neighbor not in visited:
                        visited.add(
                            neighbor
                        )
                        stack.append(
                            neighbor
                        )

            components.append(
                component
            )

        return components

    # ------------------------------------------------------------------
    # Matrix representation
    # ------------------------------------------------------------------

    def adjacency_matrix(
        self,
    ) -> tuple[
        list[object],
        list[list[int]],
    ]:
        """Return the adjacency matrix.

        The matrix contains 1 when an edge exists
        and 0 otherwise.
        """
        nodes = list(
            self.adjacency.keys()
        )

        matrix: list[
            list[int]
        ] = []

        for source in nodes:
            row: list[int] = []

            for target in nodes:
                if (
                    target
                    in self.adjacency[source]
                ):
                    row.append(1)
                else:
                    row.append(0)

            matrix.append(row)

        return nodes, matrix

    # ------------------------------------------------------------------
    # Graph traversal
    # ------------------------------------------------------------------

    def bfs(
        self,
        start: object,
    ) -> list[object]:
        """Perform a breadth-first search."""
        if start not in self.adjacency:
            raise ValueError(
                "The starting node "
                "does not exist."
            )

        visited = {start}
        path = []

        queue = deque(
            [start]
        )

        while queue:
            current = queue.popleft()

            path.append(
                current
            )

            for neighbor in (
                self.neighbors(current)
            ):
                if neighbor not in visited:
                    visited.add(
                        neighbor
                    )
                    queue.append(
                        neighbor
                    )

        return path

    def dfs(
        self,
        start: object,
    ) -> list[object]:
        """Perform a depth-first search."""
        if start not in self.adjacency:
            raise ValueError(
                "The starting node "
                "does not exist."
            )

        visited = set()
        path = []
        stack = [start]

        while stack:
            current = stack.pop()

            if current in visited:
                continue

            visited.add(
                current
            )

            path.append(
                current
            )

            for neighbor in reversed(
                self.neighbors(current)
            ):
                if neighbor not in visited:
                    stack.append(
                        neighbor
                    )

        return path

    def random_walk(
        self,
        start: object,
        steps: int,
        seed=None,
    ) -> list[object]:
        """Perform a random walk."""
        if (
            not isinstance(steps, int)
            or isinstance(steps, bool)
            or steps < 0
        ):
            raise ValueError(
                "The number of steps must be "
                "a non-negative integer."
            )

        if start not in self.adjacency:
            raise ValueError(
                "The starting node "
                "does not exist."
            )

        rng = random.Random(seed)

        path = [start]
        current = start

        for _ in range(steps):
            node_neighbors = (
                self.neighbors(current)
            )

            if not node_neighbors:
                break

            current = rng.choice(
                node_neighbors
            )

            path.append(
                current
            )

        return path

    # ------------------------------------------------------------------
    # Shortest path
    # ------------------------------------------------------------------

    def shortest_path(
        self,
        start: object,
        end: object,
    ) -> tuple[
        list[object],
        int | float,
    ]:
        """Find the shortest path using Bellman-Ford.

        Supports positive and negative edge weights.
        Detects negative-weight cycles reachable
        from the starting node.
        """
        if start not in self.adjacency:
            raise ValueError(
                "The starting node does not exist."
            )

        if end not in self.adjacency:
            raise ValueError(
                "The destination node does not exist."
            )

        distances = {
            node: float("inf")
            for node in self.adjacency
        }

        previous = {
            node: None
            for node in self.adjacency
        }

        distances[start] = 0

        # Relax all edges at most |V| - 1 times.
        for _ in range(len(self.adjacency) - 1):
            updated = False

            for source, target in self.edges():
                weight = self.get_edge_weight(
                    source, target
                )

                # An undirected edge can be
                # traversed in both directions.
                directions = [(source, target)]

                if not self.directed and source != target:
                    directions.append((target, source))

                for u, v in directions:
                    if distances[u] == float("inf"):
                        continue

                    new_distance = distances[u] + weight

                    if new_distance < distances[v]:
                        distances[v] = new_distance
                        previous[v] = u
                        updated = True

            if not updated:
                break

        # Detect reachable negative-weight cycles.
        for source, target in self.edges():
            weight = self.get_edge_weight(
                source, target
            )

            directions = [(source, target)]

            if not self.directed and source != target:
                directions.append((target, source))

            for u, v in directions:
                if (
                    distances[u] != float("inf")
                    and distances[u] + weight < distances[v]
                ):
                    raise ValueError(
                        "A negative-weight cycle "
                        "is reachable from the starting node."
                    )

        if distances[end] == float("inf"):
            raise ValueError(
                f"No path exists between "
                f"{start!r} and {end!r}."
            )

        # Reconstruct the shortest path.
        path = []
        current = end

        while current is not None:
            path.append(current)
            current = previous[current]

        path.reverse()

        return path, distances[end]


    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """Return a readable representation of the graph."""
        return str(
            self.adjacency
        )