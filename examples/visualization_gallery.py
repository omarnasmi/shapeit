"""Gallery of visualization examples.

Run from the repository root: python examples/visualization_gallery.py
Images are saved in examples/output/ (use --show to open windows).
"""

import sys
from pathlib import Path

import matplotlib

if "--show" not in sys.argv:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt

from pdl_graph import Graph, draw_graph


def build_examples():
    undirected = Graph()
    for a, b in [("A", "B"), ("B", "C"), ("C", "A"), ("C", "D"), ("D", "E"), ("E", "F"), ("F", "D")]:
        undirected.add_edge(a, b)
    undirected.add_node("Isolated")

    directed = Graph(directed=True)
    for a, b in [("Paris", "Lyon"), ("Lyon", "Paris"), ("Lyon", "Nice"), ("Nice", "Marseille"), ("Marseille", "Paris"), ("Paris", "Paris")]:
        directed.add_edge(a, b)

    dense = Graph()
    for i in range(14):
        dense.add_edge(i, (i + 1) % 14)
        dense.add_edge(i, (i + 4) % 14)

    return {
        "Graphe non oriente + sommet isole": (undirected, dict(layout="spring")),
        "Graphe oriente (fleches)": (directed, dict(layout="spring")),
        "Couleurs, tailles et groupes": (
            undirected,
            dict(
                layout="spring",
                node_size={"A": 50, "Isolated": 60},
                highlight={"tab:orange": ["A", "B", "C"], "tab:green": ["D", "E", "F"], "lightgray": ["Isolated"]},
            ),
        ),
        "Graphe dense (disposition spring)": (dense, dict(layout="spring")),
        "Graphe vide": (Graph(), {}),
    }


if __name__ == "__main__":
    out = Path(__file__).parent / "output"
    out.mkdir(exist_ok=True)
    examples = build_examples()
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    for ax, (title, (graph, opts)) in zip(axes.flat, examples.items()):
        draw_graph(graph, ax=ax, **opts)
        ax.set_title(title)
    for ax in list(axes.flat)[len(examples):]:
        ax.axis("off")
    fig.savefig(out / "gallery.png", dpi=120, bbox_inches="tight")
    print("Saved", out / "gallery.png")
    if "--show" in sys.argv:
        plt.show()
