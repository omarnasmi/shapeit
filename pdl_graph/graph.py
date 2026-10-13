
class Graph:
    def __init__(self, directed=False):
        """
        Initialize a graph.
        By default, the graph is undirected.
        """
        self.directed = directed
        self.adjacency = {}

    def add_node(self, node):
        """
        Add a node to the graph if it does not already exist.
        """
        if node not in self.adjacency:
            self.adjacency[node] = []

    def remove_node(self, node):
        """
        Remove a node and all edges connected to it.
        """
        if node in self.adjacency:
            del self.adjacency[node]

            for neighbors in self.adjacency.values():
                if node in neighbors:
                    neighbors.remove(node)

    def add_edge(self, source, target):
        """
        Add an edge between two nodes.
        Automatically create the nodes if they do not exist.
        """
        self.add_node(source)
        self.add_node(target)

        if target not in self.adjacency[source]:
            self.adjacency[source].append(target)

        if not self.directed:
            if source not in self.adjacency[target]:
                self.adjacency[target].append(source)

    def remove_edge(self, source, target):
        """
        Remove an edge between two nodes.
        """
        if source in self.adjacency and target in self.adjacency[source]:
            self.adjacency[source].remove(target)

        if not self.directed:
            if target in self.adjacency and source in self.adjacency[target]:
                self.adjacency[target].remove(source)

    def edges(self):
        """
        Return all edges of the graph without duplicates.
        """
        result = []
        seen = set()

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

    def has_edge(self, source, target):
        """
        Check if an edge exists between two nodes.
        """
        return target in self.adjacency.get(source, [])

    def neighbors(self, node):
        """
        Return the list of neighbors of a node.
        """
        return self.adjacency.get(node, [])

    def adjacency_matrix(self):
        """
        Return the list of nodes and the adjacency matrix.
        """
        nodes = list(self.adjacency.keys())
        matrix = []

        for source in nodes:
            row = []

            for target in nodes:
                if target in self.adjacency[source]:
                    row.append(1)
                else:
                    row.append(0)

            matrix.append(row)

        return nodes, matrix

    def __str__(self):
        """
        Return a readable representation of the graph.
        """
        return str(self.adjacency)

    def degree(self, node):
        """
        Return the degree of a node,
        which is the number of its neighbors.
        """
        if node not in self.adjacency:
            return 0

        return len(self.adjacency[node])
