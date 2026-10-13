"""Matplotlib visualizations for :mod:`pdl_graph`."""

from __future__ import annotations

import math
from collections.abc import Mapping

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def _circular_positions(nodes: list[object]) -> dict[object, tuple[float, float]]:
    """Return deterministic positions for nodes on a unit circle."""
    if not nodes:
        return {}

    angle_step = 2 * math.pi / len(nodes)
    return {
        node: (math.cos(index * angle_step), math.sin(index * angle_step))
        for index, node in enumerate(nodes)
    }


def draw_graph(
    graph,
    *,
    positions: Mapping[object, tuple[float, float]] | None = None,
    ax: Axes | None = None,
    show: bool = False,
) -> tuple[Figure, Axes]:
    """Draw an undirected, unweighted graph with Matplotlib.

    Nodes are drawn as points, edges as line segments, and node identifiers as
    labels. If ``positions`` is omitted, nodes are placed deterministically on
    a circle. The figure and axes are returned so callers can customize or
    save the visualization.

    Args:
        graph: A :class:`pdl_graph.Graph` instance.
        positions: Optional mapping from every node identifier to an ``(x, y)``
            coordinate.
        ax: Optional Matplotlib axes on which to draw.
        show: Whether to call :func:`matplotlib.pyplot.show`.

    Raises:
        ValueError: If the graph is directed or positions do not contain
            exactly the graph's nodes.
    """
    if graph.directed:
        raise ValueError("draw_graph only supports undirected graphs")

    nodes = list(graph.adjacency)
    node_positions = (
        _circular_positions(nodes) if positions is None else dict(positions)
    )
    if set(node_positions) != set(nodes):
        raise ValueError("positions must contain exactly every graph node")

    if ax is None:
        figure, ax = plt.subplots()
    else:
        figure = ax.figure

    for source, target in graph.edges():
        source_x, source_y = node_positions[source]
        target_x, target_y = node_positions[target]
        ax.plot(
            [source_x, target_x],
            [source_y, target_y],
            color="black",
            linewidth=1,
            zorder=1,
        )

    if nodes:
        ax.scatter(
            [node_positions[node][0] for node in nodes],
            [node_positions[node][1] for node in nodes],
            color="tab:blue",
            zorder=2,
        )
        for node in nodes:
            x, y = node_positions[node]
            ax.text(x, y, str(node), ha="center", va="center", zorder=3)

    ax.set_aspect("equal")
    ax.margins(0.2)
    ax.axis("off")

    if show:
        plt.show()

    return figure, ax


visualize_graph = draw_graph
