
"""Demonstration of ShapeIt features from Sprints 1, 2 and 3.

Run from the project root: python3 demo.py
"""

from pdl_graph import Graph, draw_graph


def titre(texte):
    print(f"\n{'=' * 55}\n{texte}\n{'=' * 55}")


def afficher_matrice(graph):
    sommets, matrice = graph.adjacency_matrix()

    if not sommets:
        print("Matrice vide")
        return

    largeur = max(5, *(len(str(s)) + 2 for s in sommets))

    print(" " * largeur + "".join(f"{str(s):>{largeur}}" for s in sommets))

    for sommet, ligne in zip(sommets, matrice):
        print(
            f"{str(sommet):>{largeur}}"
            + "".join(f"{valeur:>{largeur}}" for valeur in ligne)
        )


def main():
    # =========================================================
    # SPRINT 1 - CRÉATION ET MANIPULATION
    # =========================================================

    titre("SPRINT 1 - CRÉATION ET MANIPULATION DE GRAPHES")

    base = Graph()
    base.add_node("A")
    base.add_node("B")
    base.add_edge("A", "B")
    base.add_edge("B", "C")

    print("Liste d'adjacence :")
    print(base)
    print("Sommets :", list(base.adjacency))
    print("Arêtes :", base.edges())
    print("Voisins de B :", base.neighbors("B"))
    print("Arête A-B présente :", base.has_edge("A", "B"))
    print("Arête A-C présente :", base.has_edge("A", "C"))

    titre("Manipulation : supprimer une arête et un sommet")

    base.remove_edge("A", "B")
    print("Après suppression de A-B :", base.edges())

    base.remove_node("C")
    print("Après suppression de C :")
    print(base)

    titre("Graphe orienté - Sprint 1")

    direction = Graph(directed=True)
    direction.add_edge("A", "B")
    direction.add_edge("B", "C")

    print("Arêtes orientées :", direction.edges())
    print("A vers B :", direction.has_edge("A", "B"))
    print("B vers A :", direction.has_edge("B", "A"))

    print("\nAffichage du graphe orienté (fermer la fenêtre pour continuer).")
    draw_graph(direction, show=True)

    # =========================================================
    # SPRINT 2 - GRAPHE NON ORIENTÉ
    # =========================================================

    titre("SPRINT 2 - ANALYSE D'UN GRAPHE NON ORIENTÉ")

    graph = Graph()
    graph.add_edge("A", "B")
    graph.add_edge("A", "C")
    graph.add_edge("B", "D")

    titre("1. Graphe utilisé pour les analyses")

    print("Liste d'adjacence :")
    print(graph)
    print("Arêtes :", graph.edges())

    titre("2. Degré des sommets")

    for sommet in graph.adjacency:
        print(f"Degré de {sommet} : {graph.degree(sommet)}")

    titre("3. Densité du graphe")

    n = len(graph.adjacency)
    m = len(graph.edges())
    maximum = n * (n - 1) // 2

    print(f"Sommets : {n}, arêtes : {m}, maximum possible : {maximum}")
    print(
        f"Densité = {m}/{maximum} = "
        f"{graph.density():.2f} ({graph.density() * 100:.1f} %)"
    )

    titre("4. Matrice d'adjacence")

    afficher_matrice(graph)
    print("1 : arête présente ; 0 : arête absente")

    print("\nVisualisation du graphe non orienté (fermer pour continuer).")
    draw_graph(graph, layout="spring", show=True)

    titre("5. Composantes connexes")

    groupes = Graph()
    groupes.add_edge("A", "B")
    groupes.add_edge("B", "C")
    groupes.add_edge("D", "E")
    groupes.add_node("F")

    composantes = groupes.connected_components()

    print("Composantes :", [sorted(c) for c in composantes])
    print("Nombre de composantes :", len(composantes))

    print("\nVisualisation des composantes (fermer pour continuer).")

    draw_graph(
        groupes,
        layout="spring",
        highlight={
            "tab:blue": ["A", "B", "C"],
            "tab:orange": ["D", "E"],
            "lightgray": ["F"],
        },
        show=True,
    )

    titre("6. Cas particuliers")

    vide = Graph()
    print("Composantes d'un graphe vide :", vide.connected_components())
    print("Densité d'un graphe vide :", vide.density())

    seul = Graph()
    seul.add_node("X")
    print("Degré d'un sommet isolé :", seul.degree("X"))

    # =========================================================
    # SPRINT 2 - GRAPHE ORIENTÉ
    # =========================================================

    titre("SPRINT 2 - ANALYSE D'UN GRAPHE ORIENTÉ")

    oriente = Graph(directed=True)

    oriente.add_edge("A", "B")
    oriente.add_edge("B", "C")
    oriente.add_edge("C", "A")
    oriente.add_edge("C", "D")
    oriente.add_node("E")

    titre("7. Structure du graphe orienté")

    print("Liste d'adjacence :")
    print(oriente)
    print("Arêtes :", oriente.edges())

    titre("8. Degrés entrants et sortants")

    for sommet in oriente.adjacency:
        entrant = oriente.degree(sommet, mode="in")
        sortant = oriente.degree(sommet, mode="out")
        total = oriente.degree(sommet, mode="total")

        print(
            f"{sommet} : entrant = {entrant}, "
            f"sortant = {sortant}, total = {total}"
        )

    titre("9. Densité du graphe orienté")

    n = len(oriente.adjacency)
    m = len(oriente.edges())
    maximum = n * (n - 1)

    print(f"Sommets : {n}, arcs : {m}, maximum possible : {maximum}")
    print(
        f"Densité = {m}/{maximum} = "
        f"{oriente.density():.2f} ({oriente.density() * 100:.1f} %)"
    )

    titre("10. Matrice d'adjacence")

    afficher_matrice(oriente)
    print("Ligne : sommet de départ ; colonne : sommet d'arrivée")

    titre("11. Composantes faiblement connexes")

    faibles = oriente.connected_components()

    print("Composantes :", [sorted(c) for c in faibles])
    print("Nombre de composantes :", len(faibles))

    titre("12. Composantes fortement connexes")

    fortes = oriente.strongly_connected_components()

    print("Composantes :", [sorted(c) for c in fortes])
    print("Nombre de composantes :", len(fortes))

    # =========================================================
    # VISUALISATION FINALE
    # =========================================================

    titre("13. VISUALISATION FINALE DU GRAPHE ORIENTÉ")

    print("Arcs : A -> B, B -> C, C -> A, C -> D")
    print("Sommet isolé : E")
    print("Composantes fortes : {A, B, C}, {D}, {E}")
    print("\nLes couleurs distinguent les composantes fortes.")

    draw_graph(
        oriente,
        layout="spring",
        highlight={
            "tab:blue": ["A", "B", "C"],
            "tab:orange": ["D"],
            "lightgray": ["E"],
        },
        show=True,
    )

    # =========================================================
    # SPRINT 3 - GRAPH TRAVERSAL ALGORITHMS
    # =========================================================

    titre("SPRINT 3 - GRAPH TRAVERSAL ALGORITHMS")

    graph3 = Graph()
    graph3.add_edge("A", "B")
    graph3.add_edge("A", "C")
    graph3.add_edge("B", "D")
    graph3.add_edge("B", "E")

    print("Adjacency list:")
    print(graph3)

    # Breadth-first search
    titre("1. BREADTH-FIRST SEARCH (BFS)")
    print("BFS from A:", graph3.bfs("A"))

    # Depth-first search
    titre("2. DEPTH-FIRST SEARCH (DFS)")
    print("DFS from A:", graph3.dfs("A"))

    # Random walk
    titre("3. RANDOM WALK")
    print("Random walk from A:", graph3.random_walk("A", 5, seed=42))
    print("Same seed:", graph3.random_walk("A", 5, seed=42))

    # Graph visualization
    titre("4. GRAPH VISUALIZATION")
    draw_graph(graph3, layout="spring", show=True)


if __name__ == "__main__":
    main()
