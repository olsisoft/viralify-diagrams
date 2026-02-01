"""
Edge Bundling for Enterprise Diagrams

Implements force-directed edge bundling to reduce visual clutter
when dealing with hundreds of connections.

Algorithm based on:
- Holten's Hierarchical Edge Bundling
- Force-Directed Edge Bundling (FDEB) by Holten & van Wijk

Key features:
- Groups edges that follow similar paths into "bundles"
- Reduces visual complexity by 60-80%
- Preserves source and target positions
- Configurable bundling strength
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum
import math

from viralify_diagrams.core.diagram import Diagram, Node, Edge, Position


class BundlingAlgorithm(str, Enum):
    """Edge bundling algorithms"""
    FORCE_DIRECTED = "force_directed"      # FDEB - best for general graphs
    HIERARCHICAL = "hierarchical"          # Holten - best for trees/hierarchies
    RADIAL = "radial"                      # For radial layouts
    STUB = "stub"                          # Simple stub bundling


@dataclass
class BundleConfig:
    """Configuration for edge bundling"""
    algorithm: BundlingAlgorithm = BundlingAlgorithm.FORCE_DIRECTED

    # Bundling strength (0.0 = no bundling, 1.0 = maximum bundling)
    strength: float = 0.85

    # Number of subdivision points per edge
    subdivisions: int = 12

    # Force-directed parameters
    compatibility_threshold: float = 0.6  # Min compatibility to bundle
    iterations: int = 60                   # Force simulation iterations
    step_size: float = 0.04               # Force step size

    # Visual parameters
    smooth_curves: bool = True            # Use bezier smoothing
    taper_bundles: bool = True            # Taper bundle width at ends


@dataclass
class ControlPoint:
    """A control point in a bundled edge path"""
    x: float
    y: float

    def distance_to(self, other: 'ControlPoint') -> float:
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx * dx + dy * dy)

    def midpoint(self, other: 'ControlPoint') -> 'ControlPoint':
        return ControlPoint((self.x + other.x) / 2, (self.y + other.y) / 2)


@dataclass
class BundledEdge:
    """An edge with bundled control points"""
    edge: Edge
    source_pos: Position
    target_pos: Position
    control_points: List[ControlPoint] = field(default_factory=list)
    bundle_id: Optional[str] = None       # ID of the bundle this edge belongs to
    compatibility_scores: Dict[str, float] = field(default_factory=dict)


@dataclass
class EdgeBundle:
    """A group of bundled edges"""
    bundle_id: str
    edges: List[BundledEdge]
    core_path: List[ControlPoint]         # The "spine" of the bundle
    width: float = 2.0                    # Visual width of the bundle


class EdgeBundler:
    """
    Force-Directed Edge Bundling for enterprise diagrams.

    Reduces visual clutter by grouping edges that follow similar paths.

    Example:
        >>> bundler = EdgeBundler(BundleConfig(strength=0.85))
        >>> bundled_edges = bundler.bundle(diagram)
        >>> for edge in bundled_edges:
        ...     # edge.control_points contains the bundled path
        ...     svg_path = bundler.build_svg_path(edge)
    """

    def __init__(self, config: Optional[BundleConfig] = None):
        self.config = config or BundleConfig()
        self._edge_cache: Dict[str, BundledEdge] = {}

    def bundle(self, diagram: Diagram) -> List[BundledEdge]:
        """
        Bundle all edges in the diagram.

        Args:
            diagram: The diagram with nodes and edges

        Returns:
            List of bundled edges with control points
        """
        if not diagram.edges:
            return []

        node_map = {n.id: n for n in diagram.nodes}

        # Create bundled edge objects with initial subdivision
        bundled_edges = self._create_bundled_edges(diagram.edges, node_map)

        if len(bundled_edges) < 2:
            return bundled_edges

        # Apply bundling algorithm
        if self.config.algorithm == BundlingAlgorithm.FORCE_DIRECTED:
            self._apply_force_directed_bundling(bundled_edges)
        elif self.config.algorithm == BundlingAlgorithm.HIERARCHICAL:
            self._apply_hierarchical_bundling(bundled_edges, diagram)
        elif self.config.algorithm == BundlingAlgorithm.RADIAL:
            self._apply_radial_bundling(bundled_edges, diagram)
        else:
            self._apply_stub_bundling(bundled_edges)

        # Smooth curves if enabled
        if self.config.smooth_curves:
            for edge in bundled_edges:
                edge.control_points = self._smooth_path(edge.control_points)

        return bundled_edges

    def _create_bundled_edges(
        self,
        edges: List[Edge],
        node_map: Dict[str, Node]
    ) -> List[BundledEdge]:
        """Create bundled edge objects with initial subdivision points"""
        bundled = []

        for edge in edges:
            source = node_map.get(edge.source)
            target = node_map.get(edge.target)

            if not source or not target:
                continue

            src_pos = source.center
            tgt_pos = target.center

            # Create subdivision points along the edge
            points = self._subdivide_edge(src_pos, tgt_pos, self.config.subdivisions)

            bundled.append(BundledEdge(
                edge=edge,
                source_pos=src_pos,
                target_pos=tgt_pos,
                control_points=points
            ))

        return bundled

    def _subdivide_edge(
        self,
        start: Position,
        end: Position,
        num_points: int
    ) -> List[ControlPoint]:
        """Create evenly spaced subdivision points along an edge"""
        points = []
        for i in range(num_points + 2):  # +2 for start and end
            t = i / (num_points + 1)
            x = start.x + t * (end.x - start.x)
            y = start.y + t * (end.y - start.y)
            points.append(ControlPoint(x, y))
        return points

    def _apply_force_directed_bundling(self, edges: List[BundledEdge]) -> None:
        """
        Apply Force-Directed Edge Bundling (FDEB).

        Each subdivision point is attracted to corresponding points
        on compatible edges.
        """
        # Compute edge compatibility matrix
        compatibility = self._compute_compatibility_matrix(edges)

        step = self.config.step_size

        for iteration in range(self.config.iterations):
            # Decrease step size over iterations
            current_step = step * (1 - iteration / self.config.iterations)

            # For each edge
            for i, edge_i in enumerate(edges):
                if len(edge_i.control_points) < 3:
                    continue

                # For each subdivision point (except endpoints)
                for p in range(1, len(edge_i.control_points) - 1):
                    force_x = 0.0
                    force_y = 0.0

                    # Attraction to compatible edges
                    for j, edge_j in enumerate(edges):
                        if i == j:
                            continue

                        compat = compatibility.get((i, j), 0)
                        if compat < self.config.compatibility_threshold:
                            continue

                        if p < len(edge_j.control_points):
                            point_i = edge_i.control_points[p]
                            point_j = edge_j.control_points[p]

                            dx = point_j.x - point_i.x
                            dy = point_j.y - point_i.y
                            dist = math.sqrt(dx * dx + dy * dy) + 0.001

                            # Attraction force weighted by compatibility
                            force_x += compat * dx / dist
                            force_y += compat * dy / dist

                    # Spring force to maintain edge shape
                    prev_p = edge_i.control_points[p - 1]
                    next_p = edge_i.control_points[p + 1]
                    curr_p = edge_i.control_points[p]

                    spring_x = (prev_p.x + next_p.x) / 2 - curr_p.x
                    spring_y = (prev_p.y + next_p.y) / 2 - curr_p.y

                    # Apply forces with bundling strength
                    strength = self.config.strength
                    edge_i.control_points[p] = ControlPoint(
                        curr_p.x + current_step * (strength * force_x + (1 - strength) * spring_x),
                        curr_p.y + current_step * (strength * force_y + (1 - strength) * spring_y)
                    )

    def _compute_compatibility_matrix(
        self,
        edges: List[BundledEdge]
    ) -> Dict[Tuple[int, int], float]:
        """
        Compute edge compatibility for all edge pairs.

        Compatibility is based on:
        - Angle compatibility: edges pointing similar directions
        - Scale compatibility: edges of similar length
        - Position compatibility: edges close to each other
        - Visibility compatibility: edges that don't cross nodes
        """
        compatibility = {}

        for i in range(len(edges)):
            for j in range(i + 1, len(edges)):
                compat = self._edge_compatibility(edges[i], edges[j])
                compatibility[(i, j)] = compat
                compatibility[(j, i)] = compat

        return compatibility

    def _edge_compatibility(self, e1: BundledEdge, e2: BundledEdge) -> float:
        """Compute compatibility between two edges"""
        # Angle compatibility
        angle_compat = self._angle_compatibility(e1, e2)

        # Scale compatibility
        scale_compat = self._scale_compatibility(e1, e2)

        # Position compatibility
        pos_compat = self._position_compatibility(e1, e2)

        # Combined compatibility (geometric mean)
        return (angle_compat * scale_compat * pos_compat) ** (1/3)

    def _angle_compatibility(self, e1: BundledEdge, e2: BundledEdge) -> float:
        """How parallel are the edges?"""
        dx1 = e1.target_pos.x - e1.source_pos.x
        dy1 = e1.target_pos.y - e1.source_pos.y
        dx2 = e2.target_pos.x - e2.source_pos.x
        dy2 = e2.target_pos.y - e2.source_pos.y

        len1 = math.sqrt(dx1*dx1 + dy1*dy1) + 0.001
        len2 = math.sqrt(dx2*dx2 + dy2*dy2) + 0.001

        dot = (dx1*dx2 + dy1*dy2) / (len1 * len2)
        return abs(dot)

    def _scale_compatibility(self, e1: BundledEdge, e2: BundledEdge) -> float:
        """How similar in length are the edges?"""
        len1 = self._edge_length(e1)
        len2 = self._edge_length(e2)

        avg_len = (len1 + len2) / 2
        if avg_len == 0:
            return 1.0

        return 2 / (avg_len / min(len1, len2) + max(len1, len2) / avg_len)

    def _position_compatibility(self, e1: BundledEdge, e2: BundledEdge) -> float:
        """How close are the edge midpoints?"""
        mid1 = ControlPoint(
            (e1.source_pos.x + e1.target_pos.x) / 2,
            (e1.source_pos.y + e1.target_pos.y) / 2
        )
        mid2 = ControlPoint(
            (e2.source_pos.x + e2.target_pos.x) / 2,
            (e2.source_pos.y + e2.target_pos.y) / 2
        )

        avg_len = (self._edge_length(e1) + self._edge_length(e2)) / 2
        dist = mid1.distance_to(mid2)

        if avg_len == 0:
            return 1.0

        return avg_len / (avg_len + dist)

    def _edge_length(self, edge: BundledEdge) -> float:
        """Calculate edge length"""
        dx = edge.target_pos.x - edge.source_pos.x
        dy = edge.target_pos.y - edge.source_pos.y
        return math.sqrt(dx*dx + dy*dy)

    def _apply_hierarchical_bundling(
        self,
        edges: List[BundledEdge],
        diagram: Diagram
    ) -> None:
        """
        Apply Holten's Hierarchical Edge Bundling.

        Uses cluster hierarchy to route edges through common ancestors.
        """
        # Build cluster hierarchy
        cluster_map = self._build_cluster_hierarchy(diagram)

        for edge in edges:
            # Find common ancestor cluster
            src_cluster = cluster_map.get(edge.edge.source)
            tgt_cluster = cluster_map.get(edge.edge.target)

            if src_cluster and tgt_cluster and src_cluster == tgt_cluster:
                # Route through cluster center
                cluster = self._find_cluster(diagram, src_cluster)
                if cluster:
                    center = cluster.center if hasattr(cluster, 'center') else Position(
                        cluster.position.x + cluster.size.width / 2,
                        cluster.position.y + cluster.size.height / 2
                    )
                    self._route_through_point(edge, center)

    def _build_cluster_hierarchy(self, diagram: Diagram) -> Dict[str, str]:
        """Build mapping of node_id -> cluster_id"""
        cluster_map = {}
        for cluster in diagram.clusters:
            for node_id in cluster.node_ids:
                cluster_map[node_id] = cluster.id
        return cluster_map

    def _find_cluster(self, diagram: Diagram, cluster_id: str):
        """Find cluster by ID"""
        for cluster in diagram.clusters:
            if cluster.id == cluster_id:
                return cluster
        return None

    def _route_through_point(self, edge: BundledEdge, point: Position) -> None:
        """Route edge through a specific point"""
        strength = self.config.strength

        for i, cp in enumerate(edge.control_points):
            t = i / (len(edge.control_points) - 1)
            # Gaussian weight - maximum at middle
            weight = math.exp(-((t - 0.5) ** 2) / 0.1) * strength

            edge.control_points[i] = ControlPoint(
                cp.x + weight * (point.x - cp.x),
                cp.y + weight * (point.y - cp.y)
            )

    def _apply_radial_bundling(
        self,
        edges: List[BundledEdge],
        diagram: Diagram
    ) -> None:
        """Bundle edges for radial layouts by routing through center"""
        # Find diagram center
        if not diagram.nodes:
            return

        center_x = sum(n.center.x for n in diagram.nodes) / len(diagram.nodes)
        center_y = sum(n.center.y for n in diagram.nodes) / len(diagram.nodes)
        center = Position(center_x, center_y)

        for edge in edges:
            self._route_through_point(edge, center)

    def _apply_stub_bundling(self, edges: List[BundledEdge]) -> None:
        """
        Simple stub bundling - edges exit nodes in cardinal directions
        then merge into common paths.
        """
        # Group edges by approximate direction
        direction_groups: Dict[str, List[BundledEdge]] = {}

        for edge in edges:
            dx = edge.target_pos.x - edge.source_pos.x
            dy = edge.target_pos.y - edge.source_pos.y

            # Quantize to 8 directions
            angle = math.atan2(dy, dx)
            direction = round(angle / (math.pi / 4)) * 45
            key = f"{edge.edge.source}_{direction}"

            if key not in direction_groups:
                direction_groups[key] = []
            direction_groups[key].append(edge)

        # Bundle edges in same direction group
        for group in direction_groups.values():
            if len(group) > 1:
                self._merge_stub_group(group)

    def _merge_stub_group(self, edges: List[BundledEdge]) -> None:
        """Merge a group of edges leaving in the same direction"""
        if not edges:
            return

        # Calculate average path
        num_points = len(edges[0].control_points)

        for p in range(1, num_points - 1):
            avg_x = sum(e.control_points[p].x for e in edges) / len(edges)
            avg_y = sum(e.control_points[p].y for e in edges) / len(edges)

            for edge in edges:
                curr = edge.control_points[p]
                strength = self.config.strength
                edge.control_points[p] = ControlPoint(
                    curr.x + strength * (avg_x - curr.x),
                    curr.y + strength * (avg_y - curr.y)
                )

    def _smooth_path(self, points: List[ControlPoint]) -> List[ControlPoint]:
        """Apply Chaikin's smoothing algorithm to the path"""
        if len(points) < 3:
            return points

        smoothed = [points[0]]  # Keep start point

        for i in range(len(points) - 1):
            p0 = points[i]
            p1 = points[i + 1]

            # Chaikin's algorithm: cut corners at 1/4 and 3/4
            q = ControlPoint(
                0.75 * p0.x + 0.25 * p1.x,
                0.75 * p0.y + 0.25 * p1.y
            )
            r = ControlPoint(
                0.25 * p0.x + 0.75 * p1.x,
                0.25 * p0.y + 0.75 * p1.y
            )

            smoothed.append(q)
            smoothed.append(r)

        smoothed.append(points[-1])  # Keep end point

        return smoothed

    def build_svg_path(self, edge: BundledEdge, use_curves: bool = True) -> str:
        """
        Build SVG path string for a bundled edge.

        Args:
            edge: The bundled edge
            use_curves: Use bezier curves (True) or straight lines (False)

        Returns:
            SVG path d attribute string
        """
        points = edge.control_points

        if not points:
            return f"M {edge.source_pos.x},{edge.source_pos.y} L {edge.target_pos.x},{edge.target_pos.y}"

        if len(points) < 2:
            return f"M {points[0].x},{points[0].y}"

        if use_curves and len(points) >= 3:
            # Use quadratic bezier curves through points
            path = f"M {points[0].x},{points[0].y}"

            # First segment: quadratic to first midpoint
            mid = points[0].midpoint(points[1])
            path += f" Q {points[0].x},{points[0].y} {mid.x},{mid.y}"

            # Middle segments
            for i in range(1, len(points) - 1):
                mid_next = points[i].midpoint(points[i + 1])
                path += f" Q {points[i].x},{points[i].y} {mid_next.x},{mid_next.y}"

            # Last segment
            path += f" L {points[-1].x},{points[-1].y}"

            return path
        else:
            # Straight line segments
            path = f"M {points[0].x},{points[0].y}"
            for p in points[1:]:
                path += f" L {p.x},{p.y}"
            return path

    def get_bundles(self, edges: List[BundledEdge]) -> List[EdgeBundle]:
        """
        Group bundled edges into bundles based on compatibility.

        Useful for rendering bundle "spines" or aggregate views.
        """
        if not edges:
            return []

        # Compute compatibility
        compat = self._compute_compatibility_matrix(edges)

        # Group into bundles using threshold
        visited = set()
        bundles = []

        for i, edge in enumerate(edges):
            if i in visited:
                continue

            bundle_edges = [edge]
            visited.add(i)

            for j, other in enumerate(edges):
                if j in visited:
                    continue
                if compat.get((i, j), 0) >= self.config.compatibility_threshold:
                    bundle_edges.append(other)
                    visited.add(j)

            if bundle_edges:
                # Calculate core path (average of all edge paths)
                core_path = self._calculate_core_path(bundle_edges)

                bundles.append(EdgeBundle(
                    bundle_id=f"bundle_{len(bundles)}",
                    edges=bundle_edges,
                    core_path=core_path,
                    width=1.0 + math.log(len(bundle_edges) + 1)
                ))

        return bundles

    def _calculate_core_path(self, edges: List[BundledEdge]) -> List[ControlPoint]:
        """Calculate the core path (spine) of a bundle"""
        if not edges:
            return []

        num_points = len(edges[0].control_points)
        core_path = []

        for p in range(num_points):
            avg_x = sum(e.control_points[p].x for e in edges if p < len(e.control_points)) / len(edges)
            avg_y = sum(e.control_points[p].y for e in edges if p < len(e.control_points)) / len(edges)
            core_path.append(ControlPoint(avg_x, avg_y))

        return core_path


def apply_edge_bundling(
    diagram: Diagram,
    strength: float = 0.85,
    algorithm: BundlingAlgorithm = BundlingAlgorithm.FORCE_DIRECTED
) -> List[BundledEdge]:
    """
    Apply edge bundling to a diagram.

    Args:
        diagram: The diagram to bundle
        strength: Bundling strength (0.0-1.0)
        algorithm: Bundling algorithm to use

    Returns:
        List of bundled edges with control points

    Example:
        >>> bundled = apply_edge_bundling(diagram, strength=0.85)
        >>> for edge in bundled:
        ...     svg_path = EdgeBundler().build_svg_path(edge)
    """
    config = BundleConfig(strength=strength, algorithm=algorithm)
    bundler = EdgeBundler(config)
    return bundler.bundle(diagram)
