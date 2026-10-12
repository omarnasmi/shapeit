class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.adjacency = {}

    def add_node(self, node):
        """
        Ajoute un nœud au graphe s'il n'existe pas déjà.
        """
        if node not in self.adjacency:
            self.adjacency[node] = []

    def remove_node(self, node):
        """
        Supprime un nœud ainsi que toutes les arêtes qui lui sont liées.
        """
        if node in self.adjacency:
            del self.adjacency[node]

            for neighbors in self.adjacency.values():
                if node in neighbors:
                    neighbors.remove(node)

    def add_edge(self, source, target):
        """
        Ajoute une arête entre deux nœuds.
        Les nœuds sont créés automatiquement s'ils n'existent pas.
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
        Supprime une arête entre deux nœuds.
        """
        if source in self.adjacency and target in self.adjacency[source]:
            self.adjacency[source].remove(target)

        if not self.directed:
            if target in self.adjacency and source in self.adjacency[target]:
                self.adjacency[target].remove(source)

    def neighbors(self, node):
        """
        Retourne la liste des voisins d'un nœud.
        """
        return self.adjacency.get(node, [])

    def adjacency_matrix(self):
        """
        Retourne la liste des nœuds et la matrice d'adjacence du graphe.
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
        Retourne une représentation lisible du graphe.
        """
        return str(self.adjacency)

    def degree(self, node):
        """
        Retourne le degré d'un nœud,
        c'est-à-dire le nombre de voisins qu'il possède.
        """
        if node not in self.adjacency:
            return 0

        return len(self.adjacency[node])