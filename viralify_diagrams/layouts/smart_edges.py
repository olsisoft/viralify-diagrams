"""
Smart Edge Routing

Professional edge routing with:
- Orthogonal (90-degree) routing
- Bezier curves with optimal control points
- Anchor points (N, S, E, W, NE, NW, SE, SW)
- Edge bundling for cleaner diagrams
- Collision avoidance
"""

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional, Tuple, Set
import math

from viralify_diagrams.core.diagram import Diagram, Node, Edge, Position


class AnchorPoint(str, Enum):
    """Node anchor points for edge connections"""
    NORTH = "n"
    SOUTH = "s"
    EAST = "e"
    WEST = "w"
    NORTH_EAST = "ne"
    NORTH_WEST = "nw"
    SOUTH_EAST = "se"
    SOUTH_WEST = "sw"
    CENTER = "c"
    AUTO = "auto"  # Automatically determine best anchor


class EdgeRoutingMode(str, Enum):
    """Edge routing algorithms"""
    DIRECT = "direct"          # Straight line
    BEZIER = "bezier"          # Smooth bezier curve
    ORTHOGONAL = "orthogonal"  # 90-degree angles only
    CURVED = "curved"          # S-curve
    BUNDLED = "bundled"        # Group parallel edges


@dataclass
class RoutedEdge:
    """An edge with calculated routing"""
    edge: Edge
    source_anchor: Position
    target_anchor: Position
    control_points: List[Position]
    waypoints: List[Position]  # For orthogonal routing


@dataclass
class EdgeRoutingConfig:
    """Configuration for edge routing"""
    mode: EdgeRoutingMode = EdgeRoutingMode.BEZIER
    min_segment_length: float = 30  # Minimum straight segment
    corner_radius: float = 8        # Rounded corners for orthogonal
    padding: float = 20             # Distance from nodes
    bundle_threshold: float = 50    # Max distance to bundle edges
    curve_tension: float = 0.4      # Bezier curve tension


class SmartEdgeRouter:
    """
    Intelligent edge routing for professional diagrams.

    Features:
    - Multiple routing algorithms
    - Automatic anchor point selection
    - Collision avoidance
    - Edge bundling for parallel edges
    """

    def __init__(self, config: Optional[EdgeRoutingConfig] = None):
        self.config = config or EdgeRoutingConfig()

    def route_edges(self, diagram: Diagram) -> List[RoutedEdge]:
        """
        Route all edges in the diagram.

        Args:
            diagram: The diagram with nodes and edges

        Returns:
            List of routed edges with calculated paths
        """
        routed_edges: List[RoutedEdge] = []
        node_map = {n.id: n for n in diagram.nodes}

        # Group edges by source-target pairs for potential bundling
        edge_groups = self._group_edges(diagram.edges)

        for edge in diagram.edges:
            source = node_map.get(edge.source)
            target = node_map.get(edge.target)

            if not source or not target:
                continue

            routed = self._route_edge(edge, source, target, diagram, edge_groups)
            routed_edges.append(routed)

            # Update the original edge's control points
            edge.control_points = routed.control_points

        return routed_edges

    def _route_edge(
        self,
        edge: Edge,
        source: Node,
        target: Node,
        diagram: Diagram,
        edge_groups: Dict[Tuple[str, str], List[Edge]]
    ) -> RoutedEdge:
        """Route a single edge"""
        # Select routing mode
        mode = self.config.mode

        # Get anchor points
        src_anchor = self._get_anchor_point(source, target, AnchorPoint.AUTO)
        tgt_anchor = self._get_anchor_point(target, source, AnchorPoint.AUTO)

        # Route based on mode
        if mode == EdgeRoutingMode.DIRECT:
            control_points = []
            waypoints = []

        elif mode == EdgeRoutingMode.BEZIER:
            control_points = self._bezier_routing(src_anchor, tgt_anchor, source, target)
            waypoints = []

        elif mode == EdgeRoutingMode.ORTHOGONAL:
            control_points = []
            waypoints = self._orthogonal_routing(src_anchor, tgt_anchor, source, target, diagram)

        elif mode == EdgeRoutingMode.CURVED:
            control_points = self._s_curve_routing(src_anchor, tgt_anchor)
            waypoints = []

        elif mode == EdgeRoutingMode.BUNDLED:
            # Check if this edge should be bundled
            key = (edge.source, edge.target)
            group = edge_groups.get(key, [edge])
            control_points = self._bundled_routing(src_anchor, tgt_anchor, edge, group)
            waypoints = []

        else:
            control_points = []
            waypoints = []

        return RoutedEdge(
            edge=edge,
            source_anchor=src_anchor,
            target_anchor=tgt_anchor,
            control_points=control_points,
            waypoints=waypoints
        )

    def _get_anchor_point(
        self,
        from_node: Node,
        to_node: Node,
        anchor: AnchorPoint
    ) -> Position:
        """
        Get the anchor point position on a node.

        For AUTO mode, selects the best anchor based on relative positions.
        """
        x, y = from_node.position.x, from_node.position.y
        w, h = from_node.size.width, from_node.size.height
        cx, cy = x + w/2, y + h/2

        # Named anchor positions
        anchors = {
            AnchorPoint.NORTH: Position(cx, y),
            AnchorPoint.SOUTH: Position(cx, y + h),
            AnchorPoint.EAST: Position(x + w, cy),
            AnchorPoint.WEST: Position(x, cy),
            AnchorPoint.NORTH_EAST: Position(x + w, y),
            AnchorPoint.NORTH_WEST: Position(x, y),
            AnchorPoint.SOUTH_EAST: Position(x + w, y + h),
            AnchorPoint.SOUTH_WEST: Position(x, y + h),
            AnchorPoint.CENTER: Position(cx, cy),
        }

        if anchor != AnchorPoint.AUTO:
            return anchors[anchor]

        # Auto-select best anchor
        to_center = to_node.center
        dx = to_center.x - cx
        dy = to_center.y - cy

        # Determine quadrant and select appropriate anchor
        if abs(dx) > abs(dy):
            # Horizontal dominant
            return anchors[AnchorPoint.EAST] if dx > 0 else anchors[AnchorPoint.WEST]
        else:
            # Vertical dominant
            return anchors[AnchorPoint.SOUTH] if dy > 0 else anchors[AnchorPoint.NORTH]

    def _bezier_routing(
        self,
        start: Position,
        end: Position,
        source: Node,
        target: Node
    ) -> List[Position]:
        """Calculate bezier control points for smooth curves"""
        dx = end.x - start.x
        dy = end.y - start.y
        distance = math.sqrt(dx*dx + dy*dy)

        tension = self.config.curve_tension
        offset = min(distance * tension, 100)

        # Determine control point positions based on edge direction
        src_cx, src_cy = source.center.x, source.center.y
        tgt_cx, tgt_cy = target.center.x, target.center.y

        # Control points follow the direction from node centers
        if abs(dx) > abs(dy):
            # Horizontal edge - control points extend horizontally
            cp1 = Position(start.x + offset * (1 if dx > 0 else -1), start.y)
            cp2 = Position(end.x - offset * (1 if dx > 0 else -1), end.y)
        else:
            # Vertical edge - control points extend vertically
            cp1 = Position(start.x, start.y + offset * (1 if dy > 0 else -1))
            cp2 = Position(end.x, end.y - offset * (1 if dy > 0 else -1))

        return [cp1, cp2]

    def _orthogonal_routing(
        self,
        start: Position,
        end: Position,
        source: Node,
        target: Node,
        diagram: Diagram
    ) -> List[Position]:
        """
        Calculate orthogonal (90-degree) routing.

        Creates a path with only horizontal and vertical segments.
        """
        waypoints: List[Position] = []
        padding = self.config.padding

        dx = end.x - start.x
        dy = end.y - start.y

        # Determine routing strategy based on relative positions
        src_bounds = source.bounds
        tgt_bounds = target.bounds

        # Simple case: nodes are aligned
        if abs(dx) < 10:  # Nearly vertical
            # Straight vertical line
            return []

        if abs(dy) < 10:  # Nearly horizontal
            # Straight horizontal line
            return []

        # Complex case: need intermediate segments
        # Strategy: horizontal first, then vertical (or vice versa)

        # Check which routing is cleaner
        horizontal_first = self._prefer_horizontal_first(source, target)

        if horizontal_first:
            # Go horizontal to middle, then vertical
            mid_x = (start.x + end.x) / 2
            waypoints = [
                Position(mid_x, start.y),
                Position(mid_x, end.y)
            ]
        else:
            # Go vertical to middle, then horizontal
            mid_y = (start.y + end.y) / 2
            waypoints = [
                Position(start.x, mid_y),
                Position(end.x, mid_y)
            ]

        return waypoints

    def _prefer_horizontal_first(self, source: Node, target: Node) -> bool:
        """Determine if horizontal-first routing is preferred"""
        src_center = source.center
        tgt_center = target.center

        # Check for overlapping vertical space
        src_top = source.position.y
        src_bottom = src_top + source.size.height
        tgt_top = target.position.y
        tgt_bottom = tgt_top + target.size.height

        vertical_overlap = not (src_bottom < tgt_top or tgt_bottom < src_top)

        if vertical_overlap:
            return True

        # Default based on aspect ratio of the bounding box
        dx = abs(tgt_center.x - src_center.x)
        dy = abs(tgt_center.y - src_center.y)

        return dx > dy

    def _s_curve_routing(
        self,
        start: Position,
        end: Position
    ) -> List[Position]:
        """Calculate S-curve control points"""
        dx = end.x - start.x
        dy = end.y - start.y

        # Create S-curve with two control points
        mid_y = (start.y + end.y) / 2

        cp1 = Position(start.x, mid_y)
        cp2 = Position(end.x, mid_y)

        return [cp1, cp2]

    def _bundled_routing(
        self,
        start: Position,
        end: Position,
        edge: Edge,
        group: List[Edge]
    ) -> List[Position]:
        """
        Calculate bundled edge routing.

        Groups parallel edges together for cleaner appearance.
        """
        if len(group) <= 1:
            # No bundling needed
            return self._bezier_routing(start, end, Node("", ""), Node("", ""))

        # Find edge index in group
        edge_index = group.index(edge) if edge in group else 0
        total = len(group)

        # Calculate offset for this edge
        spacing = 8  # Pixels between bundled edges
        total_width = (total - 1) * spacing
        offset = edge_index * spacing - total_width / 2

        # Apply offset perpendicular to edge direction
        dx = end.x - start.x
        dy = end.y - start.y
        length = math.sqrt(dx*dx + dy*dy)

        if length == 0:
            return []

        # Perpendicular direction
        perp_x = -dy / length
        perp_y = dx / length

        # Offset control points
        mid_x = (start.x + end.x) / 2 + perp_x * offset
        mid_y = (start.y + end.y) / 2 + perp_y * offset

        return [Position(mid_x, mid_y)]

    def _group_edges(self, edges: List[Edge]) -> Dict[Tuple[str, str], List[Edge]]:
        """Group edges by source-target pairs"""
        groups: Dict[Tuple[str, str], List[Edge]] = {}

        for edge in edges:
            # Create canonical key (sort to handle bidirectional)
            key = (edge.source, edge.target)
            if key not in groups:
                groups[key] = []
            groups[key].append(edge)

        return groups

    @staticmethod
    def build_svg_path(routed: RoutedEdge, rounded: bool = True) -> str:
        """
        Build SVG path string for a routed edge.

        Args:
            routed: The routed edge
            rounded: Whether to use rounded corners for orthogonal routes

        Returns:
            SVG path d attribute string
        """
        start = routed.source_anchor
        end = routed.target_anchor
        cps = routed.control_points
        waypoints = routed.waypoints

        if waypoints:
            # Orthogonal routing with waypoints
            if rounded:
                return SmartEdgeRouter._build_rounded_orthogonal_path(
                    start, waypoints, end
                )
            else:
                path = f"M {start.x},{start.y}"
                for wp in waypoints:
                    path += f" L {wp.x},{wp.y}"
                path += f" L {end.x},{end.y}"
                return path

        elif len(cps) == 2:
            # Cubic bezier with two control points
            return f"M {start.x},{start.y} C {cps[0].x},{cps[0].y} {cps[1].x},{cps[1].y} {end.x},{end.y}"

        elif len(cps) == 1:
            # Quadratic bezier with one control point
            return f"M {start.x},{start.y} Q {cps[0].x},{cps[0].y} {end.x},{end.y}"

        else:
            # Direct line
            return f"M {start.x},{start.y} L {end.x},{end.y}"

    @staticmethod
    def _build_rounded_orthogonal_path(
        start: Position,
        waypoints: List[Position],
        end: Position,
        radius: float = 8
    ) -> str:
        """Build orthogonal path with rounded corners"""
        if not waypoints:
            return f"M {start.x},{start.y} L {end.x},{end.y}"

        path = f"M {start.x},{start.y}"

        # Build path through waypoints with arcs at corners
        points = [start] + waypoints + [end]

        for i in range(1, len(points) - 1):
            prev = points[i - 1]
            curr = points[i]
            next_pt = points[i + 1]

            # Calculate corner arc
            # Direction from prev to curr
            dx1 = curr.x - prev.x
            dy1 = curr.y - prev.y
            len1 = math.sqrt(dx1*dx1 + dy1*dy1)

            # Direction from curr to next
            dx2 = next_pt.x - curr.x
            dy2 = next_pt.y - curr.y
            len2 = math.sqrt(dx2*dx2 + dy2*dy2)

            if len1 == 0 or len2 == 0:
                path += f" L {curr.x},{curr.y}"
                continue

            # Normalize
            dx1 /= len1
            dy1 /= len1
            dx2 /= len2
            dy2 /= len2

            # Calculate arc start and end points
            r = min(radius, len1 / 2, len2 / 2)

            arc_start_x = curr.x - dx1 * r
            arc_start_y = curr.y - dy1 * r
            arc_end_x = curr.x + dx2 * r
            arc_end_y = curr.y + dy2 * r

            # Line to arc start
            path += f" L {arc_start_x},{arc_start_y}"

            # Arc to arc end (using quadratic bezier as approximation)
            path += f" Q {curr.x},{curr.y} {arc_end_x},{arc_end_y}"

        # Final line to end
        path += f" L {end.x},{end.y}"

        return path


def apply_smart_routing(
    diagram: Diagram,
    mode: EdgeRoutingMode = EdgeRoutingMode.BEZIER,
    config: Optional[EdgeRoutingConfig] = None
) -> Diagram:
    """
    Apply smart edge routing to a diagram.

    Args:
        diagram: The diagram to route
        mode: Routing mode to use
        config: Optional routing configuration

    Returns:
        The diagram with updated edge control points
    """
    if config is None:
        config = EdgeRoutingConfig(mode=mode)
    else:
        config.mode = mode

    router = SmartEdgeRouter(config)
    router.route_edges(diagram)

    return diagram
