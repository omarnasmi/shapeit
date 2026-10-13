"""Matplotlib visualisations for :mod:`pdl_graph`.

This module provides helpers to render :class:`~pdl_graph.Graph` instances
as 2-D plots using `Matplotlib <https://matplotlib.org/>`_.

The primary entry point is :func:`draw_graph`.  A public alias
:data:`visualize_graph` is also exported for backwards compatibility.

Typical usage
-------------
>>> from pdl_graph import Graph, draw_graph
>>> g = Graph()
>>> g.add_edge("A", "B")
>>> g.add_edge("B", "C")
>>> fig, ax = draw_graph(g)          # uses automatic circular layout
>>> fig.savefig("my_graph.png")      # persist the figure

Custom node positions
---------------------
Pass an explicit *positions* mapping to override the default circular
layout::

    >>> positions = {"A": (0, 0), "B": (1, 0), "C": (0.5, 1)}
    >>> fig, ax = draw_graph(g, positions=positions)
"""

from __future__ import annotations

import math
from collections.abc import Mapping

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def _circular_positions(nodes: list[object]) -> dict[object, tuple[float, float]]:
    """Compute deterministic node positions arranged on a unit circle.

    Nodes are placed at equal angular intervals starting at angle 0
    (i.e. the rightmost point of the circle) and going counter-clockwise.
    The arrangement is fully deterministic: given the same list of nodes
    in the same order the output is always identical.

    Args:
        nodes: Ordered list of node identifiers for which positions should
            be computed.

    Returns:
        A dictionary mapping each node identifier to an ``(x, y)`` tuple
        of floating-point coordinates on the unit circle.
        Returns an empty dict when *nodes* is empty.

    Example:
        >>> import math
        >>> positions = _circular_positions(["A", "B"])
        >>> positions["A"]          # angle 0
        (1.0, 0.0)
        >>> round(positions["B"][0], 10)  # angle π  ≈ (−1, 0)
        -1.0
    """
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

    Nodes are rendered as scatter-plot points (``tab:blue``), edges as
    black line segments, and each node's identifier as a centred text
    label.

    Layout
    ------
    When *positions* is ``None`` (the default), nodes are placed
    automatically on a unit circle by :func:`_circular_positions`.  The
    layout is deterministic: the same graph always produces the same
    picture regardless of insertion order, as long as the node list is
    stable.

    Axes configuration
    ------------------
    The axes aspect ratio is set to ``"equal"``, a 20 % margin is added
    around the content, and the axis frame / ticks are hidden so the
    plot looks clean out of the box.

    Args:
        graph: A :class:`~pdl_graph.Graph` instance.  Must be undirected
            (``graph.directed`` must be ``False``).
        positions: Optional mapping from **every** node identifier to an
            ``(x, y)`` coordinate pair.  When provided, the mapping must
            contain exactly the same set of nodes as *graph*.  If omitted,
            a circular layout is computed automatically.
        ax: Optional Matplotlib :class:`~matplotlib.axes.Axes` object on
            which to draw.  When ``None`` (default) a new figure and axes
            are created via :func:`matplotlib.pyplot.subplots`.
        show: When ``True``, :func:`matplotlib.pyplot.show` is called
            after drawing so that the figure is displayed interactively.
            Defaults to ``False``.

    Returns:
        A ``(figure, axes)`` tuple where *figure* is the
        :class:`~matplotlib.figure.Figure` containing the plot and *axes*
        is the :class:`~matplotlib.axes.Axes` on which nodes and edges
        were drawn.

    Raises:
        ValueError: If *graph* is directed (``graph.directed is True``),
            or if *positions* is provided but does not cover exactly the
            nodes present in *graph*.

    Example:
        Basic usage with automatic layout::

            >>> from pdl_graph import Graph, draw_graph
            >>> g = Graph()
            >>> g.add_edge(1, 2)
            >>> g.add_edge(2, 3)
            >>> fig, ax = draw_graph(g)

        Provide custom positions and save to a file::

            >>> positions = {1: (0, 0), 2: (1, 0), 3: (0.5, 1)}
            >>> fig, ax = draw_graph(g, positions=positions)
            >>> fig.savefig("graph.png", dpi=150)

        Draw into an existing axes object::

            >>> import matplotlib.pyplot as plt
            >>> fig, ax = plt.subplots()
            >>> draw_graph(g, ax=ax)
            (<Figure ...>, <Axes ...>)
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


#: Public alias for :func:`draw_graph` kept for backwards compatibility.
#:
#: .. deprecated::
#:    Prefer :func:`draw_graph` in new code.  ``visualize_graph`` may be
#:    removed in a future release.
visualize_graph = draw_graph
