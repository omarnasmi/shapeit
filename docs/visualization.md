# Visualisation des graphes

ShapeIt fournit une première visualisation des graphes avec
[Matplotlib](https://matplotlib.org/). Elle permet de représenter les graphes
simples, non orientés et non pondérés.

## Installation

Matplotlib est déclarée comme dépendance du projet. Depuis la racine du dépôt,
elle peut être installée avec :

```bash
python -m pip install -e .
```

Si l'environnement virtuel du projet est utilisé :

```bash
.venv/bin/python -m pip install -e .
```

## Afficher un graphe

La fonction `draw_graph` est disponible directement depuis `pdl_graph` :

```python
from pdl_graph import Graph, draw_graph

graph = Graph()
graph.add_edge("A", "B")
graph.add_edge("B", "C")
graph.add_edge("C", "A")
graph.add_node("D")  # nœud isolé

draw_graph(graph, show=True)
```

L'appel affiche :

- chaque nœud comme un point bleu ;
- chaque arête comme un segment noir ;
- l'identifiant de chaque nœud au centre du point ;
- les nœuds isolés, qui n'ont aucune arête.

Le placement automatique utilise un cercle et est déterministe : le même ordre
de nœuds produit le même placement.

L'exemple complet se trouve dans
[examples/basic_visualization.py](../examples/basic_visualization.py). Il peut
être lancé depuis la racine du projet avec :

```bash
PYTHONPATH=. .venv/bin/python examples/basic_visualization.py
```

## Contrôler la position des nœuds

Pour choisir précisément la position des nœuds, passer un dictionnaire
`positions` :

```python
positions = {
    "A": (0, 0),
    "B": (1, 0),
    "C": (1, 1),
    "D": (0, 1),
}

figure, axes = draw_graph(graph, positions=positions)
figure.show()
```

Le dictionnaire doit contenir exactement un couple `(x, y)` pour chaque nœud du
graphe. Une erreur `ValueError` est levée si un nœud est manquant ou si une
position supplémentaire est fournie.

## Personnaliser ou enregistrer la figure

`draw_graph` retourne toujours le couple `(figure, axes)` de Matplotlib. Cela
permet de personnaliser la figure ou de l'enregistrer :

```python
figure, axes = draw_graph(graph)
axes.set_title("Mon graphe")
figure.savefig("graph.png", dpi=150, bbox_inches="tight")
```

Il est également possible de fournir des axes existants :

```python
import matplotlib.pyplot as plt

figure, axes = plt.subplots(figsize=(6, 6))
draw_graph(graph, ax=axes)
figure.savefig("graph.svg")
```

Par défaut, `draw_graph` prépare la figure mais ne l'affiche pas. Utiliser
`show=True` pour appeler `matplotlib.pyplot.show()` :

```python
draw_graph(graph, show=True)
```

`visualize_graph` est aussi disponible comme alias de `draw_graph`.

## Limites actuelles

Cette première version prend en charge uniquement :

- les graphes créés avec `Graph` ;
- les graphes non orientés ;
- les graphes non pondérés.

Les graphes orientés sont refusés explicitement. La gestion des flèches, des
poids, des attributs avancés, des styles de nœuds et des algorithmes de
placement plus élaborés pourra être ajoutée dans une version ultérieure.

## Tests

Les tests de visualisation vérifient que les nœuds, les arêtes, les labels et
les nœuds isolés sont représentés correctement :

```bash
.venv/bin/python -m pytest tests/test_visualization.py -q
```
