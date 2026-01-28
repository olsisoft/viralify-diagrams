"""
Graphviz Layout Engine (Hybrid Approach)

Uses PyGraphviz for optimal node positioning, then viralify-diagrams for themed rendering.

This gives us the best of both worlds:
- Graphviz's sophisticated layout algorithms (dot, neato, fdp, sfdp, circo, twopi)
- viralify-diagrams' theming and SVG export capabilities

Supports:
- 50+ components with edge crossing minimization
- Automatic cluster containment
- Force-directed layouts for complex graphs
- Hierarchical layouts for DAGs
"""

import math
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum

from viralify_diagrams.layouts.base import BaseLayout
from viralify_diagrams.core.diagram import Diagram, Node, Edge, Cluster, Position, Size


class GraphvizAlgorithm(str, Enum):
    """Available Graphviz layout algorithms"""
    DOT = "dot"          # Hierarchical (best for DAGs, flowcharts)
    NEATO = "neato"      # Spring model (undirected graphs)
    FDP = "fdp"          # Force-directed (large graphs)
    SFDP = "sfdp"        # Scalable force-directed (100k+ nodes)
    CIRCO = "circo"      # Circular layout
    TWOPI = "twopi"      # Radial tree layout
    OSAGE = "osage"      # Array-based layout
    PATCHWORK = "patchwork"  # Squarified treemap


# Algorithm recommendations based on diagram characteristics
ALGORITHM_RECOMMENDATIONS = {
    "hierarchical": GraphvizAlgorithm.DOT,
    "flowchart": GraphvizAlgorithm.DOT,
    "dag": GraphvizAlgorithm.DOT,
    "pipeline": GraphvizAlgorithm.DOT,
    "network": GraphvizAlgorithm.NEATO,
    "undirected": GraphvizAlgorithm.NEATO,
    "large": GraphvizAlgorithm.SFDP,
    "circular": GraphvizAlgorithm.CIRCO,
    "radial": GraphvizAlgorithm.TWOPI,
    "tree": GraphvizAlgorithm.TWOPI,
    "default": GraphvizAlgorithm.DOT,
}


class GraphvizLayout(BaseLayout):
    """
    Hybrid layout engine using Graphviz for positioning.

    This layout uses PyGraphviz to calculate optimal node positions,
    then updates the viralify Diagram with these positions for themed rendering.

    Features:
    - Edge crossing minimization
    - Automatic cluster handling
    - Multiple layout algorithms
    - Scales to 50+ components easily

    Example:
        >>> from viralify_diagrams import Diagram
        >>> from viralify_diagrams.layouts import GraphvizLayout
        >>>
        >>> diagram = Diagram(title="Architecture", theme="dark")
        >>> diagram.add_node("api", "API Gateway")
        >>> diagram.add_node("db", "PostgreSQL")
        >>> diagram.add_edge("api", "db")
        >>>
        >>> layout = GraphvizLayout(algorithm="dot")
        >>> diagram = layout.layout(diagram)
    """

    def __init__(
        self,
        algorithm: str = "dot",
        rankdir: str = "TB",
        nodesep: float = 0.8,
        ranksep: float = 1.0,
        splines: str = "spline",
        overlap: str = "false",
        scale: float = 72.0,  # Graphviz uses 72 DPI
    ):
        """
        Initialize Graphviz layout engine.

        Args:
            algorithm: Layout algorithm (dot, neato, fdp, sfdp, circo, twopi)
            rankdir: Direction for hierarchical layouts (TB, BT, LR, RL)
            nodesep: Minimum space between nodes (inches)
            ranksep: Minimum space between ranks/levels (inches)
            splines: Edge routing (spline, ortho, line, polyline, curved)
            overlap: Node overlap handling (false, scale, compress, etc.)
            scale: Scale factor for converting Graphviz coords to pixels
        """
        super().__init__()
        self.algorithm = algorithm
        self.rankdir = rankdir
        self.nodesep = nodesep
        self.ranksep = ranksep
        self.splines = splines
        self.overlap = overlap
        self.scale = scale

        # Check if pygraphviz is available
        self._pgv = None
        self._check_pygraphviz()

    def _check_pygraphviz(self) -> bool:
        """Check if PyGraphviz is available"""
        try:
            import pygraphviz as pgv
            self._pgv = pgv
            return True
        except ImportError:
            print("[GraphvizLayout] WARNING: pygraphviz not installed. "
                  "Install with: pip install pygraphviz")
            print("[GraphvizLayout] Falling back to simple layout")
            return False

    @classmethod
    def recommend_algorithm(cls, diagram: Diagram) -> str:
        """
        Recommend the best algorithm based on diagram characteristics.

        Args:
            diagram: The diagram to analyze

        Returns:
            Recommended algorithm name
        """
        num_nodes = len(diagram.nodes)
        num_edges = len(diagram.edges)
        has_clusters = len(diagram.clusters) > 0

        # Check if it's a DAG (directed acyclic)
        is_dag = cls._is_dag(diagram)

        # Large graphs need scalable algorithms
        if num_nodes > 100:
            return GraphvizAlgorithm.SFDP.value

        # DAGs and hierarchical structures
        if is_dag or has_clusters:
            return GraphvizAlgorithm.DOT.value

        # Sparse graphs with few edges
        edge_ratio = num_edges / max(num_nodes, 1)
        if edge_ratio < 1.5:
            return GraphvizAlgorithm.NEATO.value

        # Dense graphs
        if edge_ratio > 3:
            return GraphvizAlgorithm.FDP.value

        # Default to dot
        return GraphvizAlgorithm.DOT.value

    @staticmethod
    def _is_dag(diagram: Diagram) -> bool:
        """Check if the diagram is a directed acyclic graph"""
        # Simple cycle detection using DFS
        visited = set()
        rec_stack = set()

        adj = {}
        for node in diagram.nodes:
            adj[node.id] = []
        for edge in diagram.edges:
            if edge.source in adj:
                adj[edge.source].append(edge.target)

        def has_cycle(node_id: str) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)

            for neighbor in adj.get(node_id, []):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node_id)
            return False

        for node in diagram.nodes:
            if node.id not in visited:
                if has_cycle(node.id):
                    return False

        return True

    def layout(self, diagram: Diagram) -> Diagram:
        """
        Apply Graphviz layout to the diagram.

        Args:
            diagram: The diagram to layout

        Returns:
            The diagram with updated positions
        """
        if not diagram.nodes:
            return diagram

        # Use Graphviz if available, otherwise fallback
        if self._pgv:
            return self._layout_with_graphviz(diagram)
        else:
            return self._layout_fallback(diagram)

    def _layout_with_graphviz(self, diagram: Diagram) -> Diagram:
        """Apply layout using PyGraphviz"""
        pgv = self._pgv

        # Create AGraph
        G = pgv.AGraph(
            directed=True,
            strict=False,
            rankdir=self.rankdir,
            nodesep=self.nodesep,
            ranksep=self.ranksep,
            splines=self.splines,
            overlap=self.overlap,
        )

        # Add nodes with size hints
        for node in diagram.nodes:
            # Convert pixel size to inches (Graphviz uses inches)
            width_inches = node.size.width / self.scale
            height_inches = node.size.height / self.scale

            G.add_node(
                node.id,
                label=node.label,
                width=width_inches,
                height=height_inches,
                fixedsize="true",
                shape="box",
            )

        # Add edges
        for edge in diagram.edges:
            G.add_edge(
                edge.source,
                edge.target,
                label=edge.label or "",
            )

        # Add clusters (subgraphs)
        for cluster in diagram.clusters:
            subgraph_name = f"cluster_{cluster.id}"
            subgraph = G.add_subgraph(
                cluster.nodes,
                name=subgraph_name,
                label=cluster.label,
                style="rounded",
            )

        # Run layout algorithm
        try:
            G.layout(prog=self.algorithm)
        except Exception as e:
            print(f"[GraphvizLayout] Layout failed with {self.algorithm}: {e}")
            print("[GraphvizLayout] Trying fallback algorithm 'dot'")
            try:
                G.layout(prog="dot")
            except Exception as e2:
                print(f"[GraphvizLayout] Fallback also failed: {e2}")
                return self._layout_fallback(diagram)

        # Extract positions and update diagram
        positions = self._extract_positions(G)
        self._apply_positions(diagram, positions)

        # Extract edge control points for splines
        edge_points = self._extract_edge_points(G)
        self._apply_edge_points(diagram, edge_points)

        # Calculate cluster bounds based on node positions
        self._calculate_cluster_bounds(diagram)

        # Update diagram dimensions to fit content
        self._fit_to_content(diagram)

        # Center in canvas
        self._center_diagram(diagram)

        # Assign animation order based on topology
        diagram.assign_animation_order()

        return diagram

    def _extract_positions(self, G) -> Dict[str, Tuple[float, float]]:
        """Extract node positions from Graphviz graph"""
        positions = {}

        for node in G.nodes():
            pos_str = node.attr.get("pos", "0,0")
            if pos_str:
                try:
                    # Graphviz format: "x,y" or "x,y!"
                    pos_str = pos_str.rstrip("!")
                    x, y = map(float, pos_str.split(","))
                    positions[node.name] = (x, y)
                except (ValueError, AttributeError):
                    positions[node.name] = (0, 0)

        return positions

    def _extract_edge_points(self, G) -> Dict[Tuple[str, str], List[Tuple[float, float]]]:
        """Extract edge spline control points from Graphviz"""
        edge_points = {}

        for edge in G.edges():
            pos_str = edge.attr.get("pos", "")
            if pos_str:
                try:
                    # Graphviz spline format: "e,x,y x1,y1 x2,y2 ..."
                    # or "s,x,y x1,y1 x2,y2 ..."
                    points = []
                    parts = pos_str.split()

                    for part in parts:
                        if part.startswith("e,") or part.startswith("s,"):
                            # End/start point
                            coords = part[2:].split(",")
                            if len(coords) >= 2:
                                points.append((float(coords[0]), float(coords[1])))
                        elif "," in part:
                            coords = part.split(",")
                            if len(coords) >= 2:
                                points.append((float(coords[0]), float(coords[1])))

                    if points:
                        edge_points[(edge[0], edge[1])] = points

                except (ValueError, AttributeError):
                    pass

        return edge_points

    def _apply_positions(self, diagram: Diagram, positions: Dict[str, Tuple[float, float]]) -> None:
        """Apply extracted positions to diagram nodes"""
        if not positions:
            return

        # Find bounds to normalize
        min_x = min(p[0] for p in positions.values())
        min_y = min(p[1] for p in positions.values())
        max_x = max(p[0] for p in positions.values())
        max_y = max(p[1] for p in positions.values())

        # Add padding
        padding = 50

        for node in diagram.nodes:
            if node.id in positions:
                x, y = positions[node.id]

                # Normalize and scale to diagram size
                # Graphviz Y is inverted (0 at bottom)
                norm_x = (x - min_x) + padding
                norm_y = (max_y - y) + padding  # Flip Y axis

                # Center node on position
                node.position = Position(
                    norm_x - node.size.width / 2,
                    norm_y - node.size.height / 2
                )

    def _apply_edge_points(
        self,
        diagram: Diagram,
        edge_points: Dict[Tuple[str, str], List[Tuple[float, float]]]
    ) -> None:
        """Apply extracted control points to diagram edges"""
        if not edge_points:
            return

        # Find same normalization parameters
        all_points = []
        for points in edge_points.values():
            all_points.extend(points)

        if not all_points:
            return

        min_x = min(p[0] for p in all_points)
        max_y = max(p[1] for p in all_points)
        padding = 50

        for edge in diagram.edges:
            key = (edge.source, edge.target)
            if key in edge_points:
                points = edge_points[key]
                if len(points) >= 3:
                    # Use middle point as control point
                    mid_idx = len(points) // 2
                    x, y = points[mid_idx]

                    norm_x = (x - min_x) + padding
                    norm_y = (max_y - y) + padding

                    edge.control_points = [Position(norm_x, norm_y)]

    def _calculate_cluster_bounds(self, diagram: Diagram) -> None:
        """Calculate cluster bounds based on contained nodes"""
        for cluster in diagram.clusters:
            cluster_nodes = [n for n in diagram.nodes if n.id in cluster.nodes]
            if cluster_nodes:
                self._layout_cluster(cluster, diagram.nodes, diagram)

    def _fit_to_content(self, diagram: Diagram, padding: int = 100) -> None:
        """Resize diagram to fit content with padding"""
        if not diagram.nodes:
            return

        # Find content bounds
        min_x = min(n.position.x for n in diagram.nodes)
        min_y = min(n.position.y for n in diagram.nodes)
        max_x = max(n.position.x + n.size.width for n in diagram.nodes)
        max_y = max(n.position.y + n.size.height for n in diagram.nodes)

        # Include clusters
        for cluster in diagram.clusters:
            min_x = min(min_x, cluster.position.x)
            min_y = min(min_y, cluster.position.y)
            max_x = max(max_x, cluster.position.x + cluster.size.width)
            max_y = max(max_y, cluster.position.y + cluster.size.height)

        content_width = max_x - min_x + 2 * padding
        content_height = max_y - min_y + 2 * padding

        # Update diagram size if content is larger
        diagram.width = max(diagram.width, int(content_width))
        diagram.height = max(diagram.height, int(content_height))

    def _layout_fallback(self, diagram: Diagram) -> Diagram:
        """
        Simple fallback layout when Graphviz is not available.
        Uses basic force-directed simulation.
        """
        print("[GraphvizLayout] Using fallback force-directed layout")

        # Initialize random positions
        import random
        random.seed(42)

        positions = {}
        for node in diagram.nodes:
            positions[node.id] = [
                random.uniform(100, diagram.width - 100),
                random.uniform(100, diagram.height - 100)
            ]

        # Simple force-directed iterations
        for _ in range(100):
            forces = {nid: [0.0, 0.0] for nid in positions}

            # Repulsion between all nodes
            node_ids = list(positions.keys())
            for i, nid1 in enumerate(node_ids):
                for nid2 in node_ids[i + 1:]:
                    dx = positions[nid1][0] - positions[nid2][0]
                    dy = positions[nid1][1] - positions[nid2][1]
                    dist = max(math.sqrt(dx * dx + dy * dy), 1)

                    # Repulsion force
                    force = 10000 / (dist * dist)
                    fx = (dx / dist) * force
                    fy = (dy / dist) * force

                    forces[nid1][0] += fx
                    forces[nid1][1] += fy
                    forces[nid2][0] -= fx
                    forces[nid2][1] -= fy

            # Attraction along edges
            for edge in diagram.edges:
                if edge.source in positions and edge.target in positions:
                    dx = positions[edge.target][0] - positions[edge.source][0]
                    dy = positions[edge.target][1] - positions[edge.source][1]
                    dist = max(math.sqrt(dx * dx + dy * dy), 1)

                    # Attraction force
                    force = dist * 0.01
                    fx = (dx / dist) * force
                    fy = (dy / dist) * force

                    forces[edge.source][0] += fx
                    forces[edge.source][1] += fy
                    forces[edge.target][0] -= fx
                    forces[edge.target][1] -= fy

            # Apply forces
            for nid in positions:
                positions[nid][0] += forces[nid][0] * 0.1
                positions[nid][1] += forces[nid][1] * 0.1

                # Keep in bounds
                positions[nid][0] = max(50, min(diagram.width - 50, positions[nid][0]))
                positions[nid][1] = max(50, min(diagram.height - 50, positions[nid][1]))

        # Apply positions to nodes
        for node in diagram.nodes:
            if node.id in positions:
                node.position = Position(
                    positions[node.id][0] - node.size.width / 2,
                    positions[node.id][1] - node.size.height / 2
                )

        # Layout clusters
        for cluster in diagram.clusters:
            self._layout_cluster(cluster, diagram.nodes, diagram)

        # Calculate edge control points
        self._calculate_edge_control_points(diagram)

        # Assign animation order
        diagram.assign_animation_order()

        return diagram


def auto_layout(diagram: Diagram, **kwargs) -> Diagram:
    """
    Automatically layout a diagram using the best algorithm.

    This is a convenience function that:
    1. Analyzes the diagram structure
    2. Recommends the best Graphviz algorithm
    3. Applies the layout

    Args:
        diagram: The diagram to layout
        **kwargs: Additional arguments passed to GraphvizLayout

    Returns:
        The diagram with updated positions

    Example:
        >>> diagram = auto_layout(diagram)
    """
    algorithm = GraphvizLayout.recommend_algorithm(diagram)
    print(f"[auto_layout] Using algorithm: {algorithm}")

    layout = GraphvizLayout(algorithm=algorithm, **kwargs)
    return layout.layout(diagram)
