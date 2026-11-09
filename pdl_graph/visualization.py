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
from collections.abc import Iterable, Mapping

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.colors import to_rgb
from matplotlib.figure import Figure
from matplotlib.patches import Circle, FancyArrowPatch


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


def _spring_positions(
    nodes: list[object],
    edges: list[tuple[object, object]],
    iterations: int = 200,
) -> dict[object, tuple[float, float]]:
    """Deterministic force-directed (Fruchterman-Reingold) layout.

    Nodes start on a circle, repel each other and are attracted along
    edges, which limits overlaps. Isolated nodes are pushed apart by the
    repulsion. The result is normalised into ``[-1, 1]``.
    """
    n = len(nodes)
    if n == 0:
        return {}
    if n == 1:
        return {nodes[0]: (0.0, 0.0)}

    pos = _circular_positions(nodes)
    xs = [pos[v][0] for v in nodes]
    ys = [pos[v][1] for v in nodes]
    index = {v: i for i, v in enumerate(nodes)}
    pairs = {
        (min(index[a], index[b]), max(index[a], index[b]))
        for a, b in edges
        if a != b
    }
    k = math.sqrt(4.0 / n)
    temperature = 0.5
    cooling = temperature / (iterations + 1)
    for _ in range(iterations):
        dx = [0.0] * n
        dy = [0.0] * n
        for i in range(n):
            for j in range(i + 1, n):
                vx, vy = xs[i] - xs[j], ys[i] - ys[j]
                dist = max(math.hypot(vx, vy), 1e-6)
                force = k * k / dist
                fx, fy = vx / dist * force, vy / dist * force
                dx[i] += fx
                dy[i] += fy
                dx[j] -= fx
                dy[j] -= fy
        for i, j in pairs:
            vx, vy = xs[i] - xs[j], ys[i] - ys[j]
            dist = max(math.hypot(vx, vy), 1e-6)
            force = dist * dist / k
            fx, fy = vx / dist * force, vy / dist * force
            dx[i] -= fx
            dy[i] -= fy
            dx[j] += fx
            dy[j] += fy
        for i in range(n):
            # weak gravity keeps isolated nodes / components near the centre
            dx[i] -= xs[i] * 1.0
            dy[i] -= ys[i] * 1.0
            length = max(math.hypot(dx[i], dy[i]), 1e-6)
            step = min(length, temperature)
            xs[i] += dx[i] / length * step
            ys[i] += dy[i] / length * step
        temperature -= cooling

    cx, cy = sum(xs) / n, sum(ys) / n
    xs = [x - cx for x in xs]
    ys = [y - cy for y in ys]
    scale = max(max(abs(v) for v in xs + ys), 1e-6)
    return {v: (xs[i] / scale, ys[i] / scale) for i, v in enumerate(nodes)}


def _per_node(value, nodes, default, name):
    """Expand a scalar or mapping *value* into a per-node dict."""
    if value is None:
        return {node: default for node in nodes}
    if isinstance(value, Mapping):
        unknown = set(value) - set(nodes)
        if unknown:
            raise ValueError(f"{name} refers to unknown nodes: {sorted(map(str, unknown))}")
        return {node: value.get(node, default) for node in nodes}
    return {node: value for node in nodes}


def _text_color(color) -> str:
    """Return black or white, whichever is readable on *color*."""
    r, g, b = to_rgb(color)
    return "black" if 0.299 * r + 0.587 * g + 0.114 * b > 0.55 else "white"


def draw_graph(
    graph,
    *,
    positions: Mapping[object, tuple[float, float]] | None = None,
    layout: str = "circular",
    node_color=None,
    node_size=None,
    highlight: Mapping[object, Iterable[object]] | None = None,
    edge_color: str = "black",
    highlight_edges: Iterable[tuple[object, object]] | None = None,
    visit_order: Iterable[object] | None = None,
    walk: Iterable[object] | None = None,
    show_weights: bool = False,
    total_distance: int | float | None = None,
    title: str | None = None,
    ax: Axes | None = None,
    show: bool = False,
) -> tuple[Figure, Axes]:
    """Draw a directed or undirected graph with Matplotlib.

    Args:
        graph: A :class:`~pdl_graph.Graph`.
        positions: Optional mapping covering exactly every node. Overrides
            *layout*.
        layout: ``"circular"`` (default) or ``"spring"`` (force-directed,
            deterministic, limits overlaps on non-trivial graphs).
        node_color: A single colour or a ``{node: colour}`` mapping
            (default ``tab:blue``).
        node_size: A single diameter in points or a ``{node: size}``
            mapping. By default the size adapts to the label length so
            names stay readable.
        highlight: Mapping ``{colour: nodes}``; each group of nodes is
            coloured with its colour (overrides *node_color*), e.g. to show
            analysis results such as components or a path.
        edge_color: Colour of the edges.
        highlight_edges: Edges to emphasise (for example a shortest path).
        visit_order: Order in which nodes were discovered by BFS/DFS.
        walk: Consecutive nodes visited during a random walk (repeats allowed).
        show_weights: Display the numerical weight of each edge.
        total_distance: Optional shortest-path distance shown under the graph.
        title: Optional title of the figure.
        ax: Existing axes to draw on.
        show: Call :func:`matplotlib.pyplot.show` after drawing.

    Directed edges are drawn as arrows pointing to the target; reciprocal
    edges are curved so both stay visible. Empty graphs give an empty axes
    and isolated nodes are drawn without edges.

    Returns:
        ``(figure, axes)``.

    Raises:
        ValueError: If *positions* does not cover exactly the graph nodes,
            if *layout* is unknown, or if colour/size/highlight refer to
            unknown nodes.
    """
    nodes = list(graph.adjacency)
    edges = graph.edges()
    if positions is not None:
        node_positions = dict(positions)
    elif layout == "circular":
        node_positions = _circular_positions(nodes)
    elif layout == "spring":
        node_positions = _spring_positions(nodes, edges)
    else:
        raise ValueError(f"unknown layout: {layout!r}")
    if set(node_positions) != set(nodes):
        raise ValueError("positions must contain exactly every graph node")

    default_sizes = {
        node: max(26.0, 9.0 * len(str(node)) + 14.0) for node in nodes
    }
    diameters = _per_node(node_size, nodes, None, "node_size")
    diameters = {
        node: float(diameters[node] if diameters[node] is not None else default_sizes[node])
        for node in nodes
    }
    colors = _per_node(node_color, nodes, "tab:blue", "node_color")
    for group_color, members in (highlight or {}).items():
        members = list(members)
        unknown = [m for m in members if m not in colors]
        if unknown:
            raise ValueError(f"highlight refers to unknown nodes: {unknown}")
        for member in members:
            colors[member] = group_color

    # A traversal order (BFS/DFS) is not necessarily an edge-by-edge path.
    # Only actual path edges are highlighted for shortest paths and walks.
    ordered_nodes = list(visit_order) if visit_order is not None else None
    walk_nodes = list(walk) if walk is not None else None
    if ordered_nodes is not None:
        if len(ordered_nodes) != len(set(ordered_nodes)):
            raise ValueError("visit_order must not repeat nodes")
        unknown = [node for node in ordered_nodes if node not in graph.adjacency]
        if unknown:
            raise ValueError(f"visit_order refers to unknown nodes: {unknown}")
    if walk_nodes is not None:
        unknown = [node for node in walk_nodes if node not in graph.adjacency]
        if unknown:
            raise ValueError(f"walk refers to unknown nodes: {unknown}")
        for source, target in zip(walk_nodes, walk_nodes[1:]):
            if not graph.has_edge(source, target):
                raise ValueError(f"walk uses a missing edge: {(source, target)!r}")

    selected_edges = set(highlight_edges or [])
    if walk_nodes is not None:
        selected_edges.update(zip(walk_nodes, walk_nodes[1:]))
    actual_edges = set(edges)
    for source, target in selected_edges:
        if (source, target) not in actual_edges and not (
            not graph.directed and (target, source) in actual_edges
        ):
            raise ValueError(f"highlight_edges contains a missing edge: {(source, target)!r}")

    if ax is None:
        figure, ax = plt.subplots(figsize=(8.5, 6))
    else:
        figure = ax.figure

    edge_set = set(edges)
    for source, target in edges:
        selected = ((source, target) in selected_edges or
                    (not graph.directed and (target, source) in selected_edges))
        current_color = "tab:green" if selected else edge_color
        current_width = 3.8 if selected else 1.4
        sx, sy = node_positions[source]
        tx, ty = node_positions[target]
        if source == target:
            radius = 0.12
            ax.add_patch(
                Circle((sx, sy + radius * 1.6), radius, fill=False,
                       edgecolor=current_color, linewidth=current_width, zorder=1)
            )
        elif graph.directed:
            curved = (target, source) in edge_set
            ax.add_patch(
                FancyArrowPatch(
                    (sx, sy), (tx, ty),
                    arrowstyle="-|>", mutation_scale=15,
                    connectionstyle="arc3,rad=0.2" if curved else "arc3,rad=0",
                    shrinkA=diameters[source] / 2 + 1,
                    shrinkB=diameters[target] / 2 + 1,
                    color=current_color, linewidth=current_width, zorder=1,
                )
            )
        else:
            ax.plot([sx, tx], [sy, ty], color=current_color, linewidth=current_width, zorder=1)

        if show_weights:
            weight = graph.get_edge_weight(source, target)
            mx, my = (sx + tx) / 2, (sy + ty) / 2
            if source == target:
                my += 0.32
            else:
                # Shift labels slightly away from their edges for readability.
                length = max(math.hypot(tx - sx, ty - sy), 1e-9)
                mx += -(ty - sy) / length * 0.07
                my += (tx - sx) / length * 0.07
            ax.text(mx, my, str(weight), ha="center", va="center",
                    fontsize=10, fontweight="bold", zorder=5,
                    bbox={"facecolor": "white", "alpha": 0.92,
                          "edgecolor": "none", "boxstyle": "round,pad=0.2"})

    if nodes:
        ax.scatter(
            [node_positions[v][0] for v in nodes],
            [node_positions[v][1] for v in nodes],
            s=[diameters[v] ** 2 for v in nodes],
            color=[colors[v] for v in nodes],
            edgecolors="black",
            linewidths=0.8,
            zorder=2,
            clip_on=False,
        )
        for node in nodes:
            x, y = node_positions[node]
            ax.text(x, y, str(node), ha="center", va="center", zorder=3,
                    color=_text_color(colors[node]), fontweight="bold")

    if walk_nodes is not None:
        # Number each move. Repeated passages are deliberately visible.
        passage_counts = {}
        for step, (source, target) in enumerate(zip(walk_nodes, walk_nodes[1:]), start=1):
            key = (source, target) if graph.directed else frozenset((source, target))
            repetition = passage_counts.get(key, 0)
            passage_counts[key] = repetition + 1
            sx, sy = node_positions[source]
            tx, ty = node_positions[target]
            mx, my = (sx + tx) / 2, (sy + ty) / 2
            dx, dy = tx - sx, ty - sy
            length = max(math.hypot(dx, dy), 1e-9)
            offset = 14 + 16 * repetition
            ax.annotate(str(step), (mx, my),
                        xytext=(-dy / length * offset, dx / length * offset),
                        textcoords="offset points", ha="center", va="center",
                        fontsize=8, fontweight="bold", color="white", zorder=7,
                        bbox={"boxstyle": "circle,pad=0.25", "facecolor": "#b45309",
                              "edgecolor": "white", "linewidth": 1})

    if ordered_nodes is not None:
        for order_number, node in enumerate(ordered_nodes, start=1):
            x, y = node_positions[node]
            ax.annotate(str(order_number), (x, y), xytext=(18, 16),
                        textcoords="offset points", ha="center", va="center",
                        fontsize=9, fontweight="bold", color="white", zorder=6,
                        bbox={"boxstyle": "circle,pad=0.25", "facecolor": "#b45309",
                              "edgecolor": "white", "linewidth": 1})

    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", pad=18)
    if total_distance is not None:
        ax.text(0.5, -0.03, f"Distance totale : {total_distance}",
                transform=ax.transAxes, ha="center", va="top",
                fontsize=11, fontweight="bold", color="tab:green")
    if walk_nodes is not None:
        description = "  →  ".join(str(node) for node in walk_nodes)
        ax.text(0.5, -0.1, f"Marche aléatoire : {description}",
                transform=ax.transAxes, ha="center", va="top", fontsize=10,
                wrap=True)
        # The step-by-step sequence preserves repeat visits that cannot be
        # expressed by one unique number on each vertex.
    ax.set_aspect("equal")
    ax.margins(0.38)
    ax.autoscale_view()
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