# PDL Graph

**PDL Graph** (`pdl_graph`) est une bibliothèque Python pour la création, la manipulation et la visualisation de graphes, développée dans le cadre de l'UE **Processus du Développement Logiciel** (M1 Informatique ILSEN).

Le cœur de la bibliothèque est développé de zéro — aucune bibliothèque comme NetworkX n'est utilisée pour implémenter les fonctionnalités principales.

## État actuel

Les fonctionnalités suivantes sont implémentées et testées :

- Graphes orientés et non orientés
- Ajout et suppression de nœuds et d'arêtes
- Recherche de voisins et vérification de l'existence d'une arête
- Calcul du degré d'un nœud
- Génération de la matrice d'adjacence
- Visualisation avec Matplotlib (`draw_graph`) pour les graphes non orientés

## Installation

Cloner le dépôt, puis installer le paquet (optionnellement dans un environnement virtuel) :

```bash
python -m venv .venv
source .venv/bin/activate

pip install .          # installation standard
pip install -e .       # installation éditable pour le développement
```

Dépendances : `matplotlib` (listé dans `pyproject.toml`).  
Pour exécuter les tests : `pytest` (listé dans `requirements.txt`).

## Prise en main rapide

```python
from pdl_graph import Graph, draw_graph

# Créer un graphe non orienté (par défaut)
g = Graph()
g.add_edge("A", "B")
g.add_edge("B", "C")
g.add_edge("C", "A")
g.add_node("D")          # nœud isolé

# Requêtes de base
print(g.neighbors("A"))  # ['B', 'C']
print(g.degree("A"))     # 2
print(g.edges())         # [('A', 'B'), ('B', 'C'), ('C', 'A')]

# Matrice d'adjacence
nodes, matrix = g.adjacency_matrix()

# Visualisation (graphes non orientés uniquement)
draw_graph(g, show=True)

# Graphe orienté
dg = Graph(directed=True)
dg.add_edge("X", "Y")
print(dg.neighbors("Y"))  # []  — orienté, pas d'arête retour
```

Un exemple exécutable est disponible dans [`examples/basic_visualization.py`](examples/basic_visualization.py).

## Structure du projet

```
pdl_graph/           # code source de la bibliothèque
├── __init__.py
├── graph.py         # classe Graph
└── visualization.py # draw_graph / visualize_graph

tests/               # suite de tests pytest
├── test_graph.py
└── test_visualization.py

examples/
└── basic_visualization.py

docs/                # documentation détaillée (en cours de rédaction)
└── visualization.md

pyproject.toml
requirements.txt
```

## Exécution des tests

```bash
pytest
```

## Documentation

La documentation détaillée de chaque module est en cours de rédaction dans [`docs/`](docs/).

## Feuille de route (Roadmap)

Fonctionnalités prévues pour les prochains sprints :

- Analyse de graphes (densité, composantes connexes, triangles, …)
- Algorithmes de parcours : BFS, DFS, marche aléatoire, plus court chemin
- Graphes pondérés et signés
- Attributs sur les nœuds et les arêtes
- Améliorations de la visualisation et exports (SVG, PNG, PDF)
- Interopérabilité avec NumPy / PyTorch

## Technologies

| Usage | Outil |
|---|---|
| Langage | Python ≥ 3.10 |
| Visualisation | Matplotlib |
| Tests | pytest |
| Gestion de versions | Git / GitHub |
| Gestion de projet | Linear |
