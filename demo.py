from pdl_graph import Graph, draw_graph

graph = Graph()

# Ajouter des arêtes
graph.add_edge("A", "B")
graph.add_edge("A", "C")
graph.add_edge("B", "D")

# Afficher la liste d'adjacence
print("Liste d'adjacence :")
print(graph)

# Afficher les arêtes
print("Arêtes :", graph.edges())


# Afficher le calcul de la densité
n = len(graph.adjacency)
m = sum(1 for a, b in graph.edges() if a != b)

max_edges = n * (n - 1)
if not graph.directed:
    max_edges //= 2

print("\nNombre de sommets :", n)
print("Nombre d'arêtes :", m)
print("Nombre maximal d'arêtes :", max_edges)

print("\nCalcul de la densité :")

if n < 2:
    print("Densité = 0 (moins de 2 sommets)")
else:
    if graph.directed:
        print(f"D = {m} / ({n} × ({n} - 1))")
    else:
        print(f"D = 2 × {m} / ({n} × ({n} - 1))")

    print(f"D = {m} / {max_edges} = {graph.density():.2f}")

print(f"Densité du graphe : {graph.density():.2f} ({graph.density() * 100:.1f} %)")


# Afficher le graphe avec Matplotlib
draw_graph(graph, show=True)