"""Démonstration interactive de ShapeIt — Sprints 1, 2 et 3.

Lancer depuis la racine du dépôt : python3 demo.py
Une seule fenêtre Matplotlib avec les boutons Précédent / Suivant.
"""

import textwrap

import matplotlib.pyplot as plt
from matplotlib.widgets import Button

from pdl_graph import Graph, draw_graph


def page(sprint, titre, graphe, resultats, **options):
    """Décrire une vue sans lancer immédiatement une fenêtre."""
    return {
        "sprint": sprint,
        "titre": titre,
        "graphe": graphe,
        "resultats": resultats,
        "options": options,
    }


def construire_pages():
    """Préparer les exemples et calculer les résultats avec ShapeIt."""
    pages = []

    # SPRINT 1 — Création et manipulation
    base = Graph()
    base.add_node("A")
    base.add_node("B")
    base.add_edge("A", "B")
    base.add_edge("B", "C")
    pages.append(page(
        1, "Création d'un graphe", base,
        [
            f"Liste d'adjacence : {base}",
            f"Sommets : {list(base.adjacency)}",
            f"Arêtes : {base.edges()}",
            f"Voisins de B : {base.neighbors('B')}",
            f"Arête A–B présente : {base.has_edge('A', 'B')}",
            f"Arête A–C présente : {base.has_edge('A', 'C')}",
        ],
    ))

    base_modifie = Graph()
    base_modifie.add_edge("A", "B")
    base_modifie.add_edge("B", "C")
    base_modifie.remove_edge("A", "B")
    base_modifie.remove_node("C")
    pages.append(page(
        1, "Suppression d'une arête et d'un sommet", base_modifie,
        [
            "Départ : arêtes A–B et B–C.",
            "Suppression de A–B, puis du sommet C.",
            f"Liste d'adjacence finale : {base_modifie}",
        ],
    ))

    direction = Graph(directed=True)
    direction.add_edge("A", "B")
    direction.add_edge("B", "C")
    pages.append(page(
        1, "Graphe orienté", direction,
        [
            f"Arcs : {direction.edges()}",
            f"A vers B : {direction.has_edge('A', 'B')}",
            f"B vers A : {direction.has_edge('B', 'A')}",
            "Les flèches indiquent le sens des connexions.",
        ],
    ))

    # SPRINT 2 — Analyse
    analyse = Graph()
    analyse.add_edge("A", "B")
    analyse.add_edge("A", "C")
    analyse.add_edge("B", "D")
    sommets, matrice = analyse.adjacency_matrix()
    degres = [f"Degré de {n} : {analyse.degree(n)}" for n in sommets]
    pages.append(page(
        2, "Degrés, densité et matrice d'adjacence", analyse,
        [
            f"Sommets : {len(sommets)} ; arêtes : {len(analyse.edges())}",
            *degres,
            f"Densité : {analyse.density():.2f}",
            f"Ordre de la matrice : {sommets}",
            *[f"{n} : {ligne}" for n, ligne in zip(sommets, matrice)],
        ],
        layout="spring",
    ))

    groupes = Graph()
    groupes.add_edge("A", "B")
    groupes.add_edge("B", "C")
    groupes.add_edge("D", "E")
    groupes.add_node("F")
    composantes = groupes.connected_components()
    pages.append(page(
        2, "Composantes connexes", groupes,
        [
            f"Nombre de composantes : {len(composantes)}",
            f"Composantes : {[sorted(c) for c in composantes]}",
            "Chaque composante est représentée par une couleur.",
        ],
        layout="spring",
        highlight={
            "tab:blue": ["A", "B", "C"],
            "tab:orange": ["D", "E"],
            "lightgray": ["F"],
        },
    ))

    oriente = Graph(directed=True)
    oriente.add_edge("A", "B")
    oriente.add_edge("B", "C")
    oriente.add_edge("C", "A")
    oriente.add_edge("C", "D")
    oriente.add_node("E")
    fortes = oriente.strongly_connected_components()
    faibles = oriente.connected_components()
    pages.append(page(
        2, "Analyse d'un graphe orienté", oriente,
        [
            f"Arcs : {oriente.edges()}",
            f"Densité : {oriente.density():.2f}",
            f"Composantes faibles : {[sorted(c) for c in faibles]}",
            f"Composantes fortes : {[sorted(c) for c in fortes]}",
            "Les couleurs distinguent les composantes fortes.",
        ],
        layout="spring",
        highlight={
            "tab:blue": ["A", "B", "C"],
            "tab:orange": ["D"],
            "lightgray": ["E"],
        },
    ))

    vide = Graph()
    isole = Graph()
    isole.add_node("X")
    pages.append(page(
        2, "Cas particuliers", isole,
        [
            f"Composantes d'un graphe vide : {vide.connected_components()}",
            f"Densité d'un graphe vide : {vide.density()}",
            f"Degré d'un sommet isolé : {isole.degree('X')}",
            "Le dessin représente ici un sommet sans arête.",
        ],
    ))

    # SPRINT 3 — Parcours et plus court chemin
    parcours = Graph()
    parcours.add_edge("A", "B")
    parcours.add_edge("A", "C")
    parcours.add_edge("B", "D")
    parcours.add_edge("B", "E")
    ordre_bfs = parcours.bfs("A")
    ordre_dfs = parcours.dfs("A")
    marche = parcours.random_walk("A", 5, seed=42)

    pages.append(page(
        3, "Parcours en largeur (BFS)", parcours,
        [
            "Départ : A",
            f"Ordre de visite : {' → '.join(map(str, ordre_bfs))}",
            "Les numéros indiquent l'ordre de découverte.",
            "Il ne s'agit pas nécessairement d'un chemin continu.",
        ],
        layout="spring",
        visit_order=ordre_bfs,
    ))

    pages.append(page(
        3, "Parcours en profondeur (DFS)", parcours,
        [
            "Départ : A",
            f"Ordre de visite : {' → '.join(map(str, ordre_dfs))}",
            "Les numéros indiquent l'ordre de visite.",
        ],
        layout="spring",
        visit_order=ordre_dfs,
    ))

    pages.append(page(
        3, "Marche aléatoire", parcours,
        [
            "Départ : A ; nombre de pas demandé : 5",
            "Graine aléatoire : 42",
            f"Trajet : {' → '.join(map(str, marche))}",
            "Les passages répétés sont conservés.",
            "Les arêtes parcourues sont mises en évidence.",
        ],
        layout="spring",
        walk=marche,
    ))

    pondere = Graph()
    pondere.add_edge("A", "B", 4)
    pondere.add_edge("A", "C", 2)
    pondere.add_edge("C", "B", 1)
    pondere.add_edge("B", "D", 3)
    pondere.add_edge("C", "D", 7)
    pondere.add_edge("D", "E")
    chemin, distance = pondere.shortest_path("A", "D")
    pages.append(page(
        3, "Bellman-Ford — plus court chemin", pondere,
        [
            "Départ : A ; arrivée : D",
            f"Chemin : {' → '.join(map(str, chemin))}",
            f"Distance totale : {distance}",
            "Les nombres indiquent les poids des arêtes.",
            "Le chemin choisi est mis en évidence en vert.",
            "Poids par défaut de D–E : 1",
        ],
        layout="spring",
        show_weights=True,
        highlight_edges=list(zip(chemin, chemin[1:])),
        total_distance=distance,
    ))

    negatif = Graph(directed=True)
    negatif.add_edge("A", "B", 4)
    negatif.add_edge("A", "C", 5)
    negatif.add_edge("B", "C", -2)
    chemin_negatif, distance_negative = negatif.shortest_path("A", "C")
    pages.append(page(
        3, "Bellman-Ford — poids négatif", negatif,
        [
            "Départ : A ; arrivée : C",
            f"Chemin : {' → '.join(map(str, chemin_negatif))}",
            f"Distance totale : {distance_negative}",
            "Le poids B→C vaut −2.",
            "Bellman-Ford peut prendre en charge ce poids négatif.",
        ],
        layout="spring",
        show_weights=True,
        highlight_edges=list(zip(chemin_negatif, chemin_negatif[1:])),
        total_distance=distance_negative,
    ))

    cycle = Graph(directed=True)
    cycle.add_edge("A", "B", 2)
    cycle.add_edge("B", "C", -4)
    cycle.add_edge("C", "A", 1)
    try:
        cycle.shortest_path("A", "C")
    except ValueError as erreur:
        if "negative-weight cycle" in str(erreur):
            constat = "Cycle négatif accessible détecté."
        else:
            constat = f"Erreur : {erreur}"
    else:
        constat = "Le cycle négatif n'a pas été détecté."
    pages.append(page(
        3, "Bellman-Ford — cycle négatif", cycle,
        [
            "Cycle A → B → C → A",
            "Coût du cycle : 2 − 4 + 1 = −1",
            constat,
            "Il n'existe pas de plus court chemin fini.",
        ],
        layout="spring",
        show_weights=True,
    ))

    pages.append(page(
        3, "Cas particulier : même sommet", pondere,
        [
            "Départ : A ; arrivée : A",
            f"Résultat : {pondere.shortest_path('A', 'A')}",
            "En l'absence de cycle négatif accessible,",
            "la distance d'un sommet vers lui-même vaut 0.",
        ],
        layout="spring",
        show_weights=True,
    ))

    coloration_graphe = Graph()
    coloration_graphe.add_edge("A", "B")
    coloration_graphe.add_edge("B", "C")
    coloration_graphe.add_edge("C", "A")
    coloration_graphe.add_edge("C", "D")
    coloration_graphe.add_edge("E", "F")
    coloration_graphe.add_node("G")
    couleurs = coloration_graphe.graph_coloring()
    palette = [
        "tab:blue",
        "tab:orange",
        "tab:green",
        "tab:red",
        "tab:purple",
        "tab:brown",
    ]
    couleurs_visuelles = {
        sommet: palette[indice % len(palette)]
        for sommet, indice in couleurs.items()
    }
    nb_couleurs = len(set(couleurs.values()))
    pages.append(page(
        3, "Coloration gloutonne des sommets", coloration_graphe,
        [
            f"Coloration : {couleurs}",
            f"Nombre de couleurs utilisées : {nb_couleurs}",
            "Deux sommets adjacents ont toujours des couleurs différentes.",
            "Composante séparée (E–F) et sommet isolé (G) pris en charge.",
        ],
        layout="spring",
        node_color=couleurs_visuelles,
    ))

    return pages


def lancer_diaporama(pages):
    """Afficher toutes les démonstrations dans une seule fenêtre Matplotlib."""
    if not pages:
        return

    figure = plt.figure(figsize=(12, 7.5))
    figure.canvas.manager.set_window_title("ShapeIt — Démonstration")
    graphe_ax = figure.add_axes([0.04, 0.23, 0.60, 0.65])
    info_ax = figure.add_axes([0.66, 0.22, 0.31, 0.65])
    precedent_ax = figure.add_axes([0.31, 0.055, 0.15, 0.065])
    suivant_ax = figure.add_axes([0.54, 0.055, 0.15, 0.065])
    bouton_precedent = Button(precedent_ax, "Précédent")
    bouton_suivant = Button(suivant_ax, "Suivant")
    etat = {"index": 0}

    def afficher():
        index = etat["index"]
        item = pages[index]
        graphe_ax.clear()
        info_ax.clear()
        draw_graph(
            item["graphe"],
            ax=graphe_ax,
            show=False,
            **item["options"],
        )

        info_ax.set_xlim(0, 1)
        info_ax.set_ylim(0, 1)
        info_ax.axis("off")
        info_ax.text(
            0, 0.99,
            f"SPRINT {item['sprint']}",
            fontsize=11,
            fontweight="bold",
            color="#2563eb",
            va="top",
        )
        info_ax.text(
            0, 0.93, item["titre"],
            fontsize=13, fontweight="bold",
            va="top", wrap=True,
        )
        y = 0.81
        for resultat in item["resultats"]:
            morceaux = textwrap.wrap(
                str(resultat), width=38,
                break_long_words=False,
                break_on_hyphens=False,
            ) or [""]
            for morceau in morceaux:
                info_ax.text(0, y, morceau, fontsize=9.5, va="top")
                y -= 0.041
            y -= 0.025

        figure.suptitle(
            f"ShapeIt — Démonstration interactive   •   {index + 1} / {len(pages)}",
            fontsize=15, fontweight="bold", y=0.97,
        )
        bouton_precedent.label.set_color(
            "#555555" if index > 0 else "#aaaaaa"
        )
        bouton_suivant.label.set_color(
            "#555555" if index < len(pages) - 1 else "#aaaaaa"
        )
        figure.canvas.draw_idle()

    def precedent(_event):
        if etat["index"] > 0:
            etat["index"] -= 1
            afficher()

    def suivant(_event):
        if etat["index"] < len(pages) - 1:
            etat["index"] += 1
            afficher()

    bouton_precedent.on_clicked(precedent)
    bouton_suivant.on_clicked(suivant)
    afficher()
    plt.show()


def main():
    pages = construire_pages()
    print(f"{len(pages)} démonstrations disponibles dans la fenêtre ShapeIt.")
    print("Utilise les boutons Précédent et Suivant pour changer de vue.")
    lancer_diaporama(pages)


if __name__ == "__main__":
    main()
