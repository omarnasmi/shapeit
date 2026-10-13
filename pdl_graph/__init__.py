"""pdl_graph — Python graph manipulation and analysis library.

This package provides a lightweight, dependency-minimal implementation of
directed and undirected graphs, together with Matplotlib-based visualisation
helpers.

Public API
----------
- :class:`Graph` – adjacency-list graph supporting directed and undirected
  modes.
- :func:`draw_graph` / :func:`visualize_graph` – draw an undirected graph
  with Matplotlib (``visualize_graph`` is a public alias for ``draw_graph``).

Example
-------
>>> from pdl_graph import Graph, draw_graph
>>> g = Graph()
>>> g.add_edge("A", "B")
>>> g.add_edge("B", "C")
>>> fig, ax = draw_graph(g)
"""

from .graph import Graph
from .visualization import draw_graph, visualize_graph

__all__ = ["Graph", "draw_graph", "visualize_graph"]