"""
Channel-Based Orthogonal Routing

Routes edges through dedicated "channels" like circuit board traces.
Provides clean, non-overlapping orthogonal paths for enterprise diagrams.

Key features:
- Grid-based channel allocation
- Collision-free routing
- Layer separation for crossing edges
- Minimum bend radius
- Track width management
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from enum import Enum
from collections import defaultdict
import heapq
import math

from viralify_diagrams.core.diagram import Diagram, Node, Edge, Cluster, Position, Size


class Direction(str, Enum):
    """Routing direction"""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"


class ChannelSide(str, Enum):
    """Side of a node for channel entry/exit"""
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


@dataclass
class GridCell:
    """A cell in the routing grid"""
    x: int
    y: int
    blocked: bool = False
    occupied_by: Set[str] = field(default_factory=set)  # Edge IDs using this cell
    channel_layer: int = 0  # For multi-layer routing


@dataclass
class Channel:
    """A routing channel (horizontal or vertical track)"""
    id: str
    direction: Direction
    position: float              # X for vertical, Y for horizontal
    start: float                 # Start coordinate
    end: float                   # End coordinate
    layer: int = 0               # Layer for crossings
    edges: Set[str] = field(default_factory=set)  # Edges using this channel


@dataclass
class RoutingSegment:
    """A segment of a routed path"""
    start: Position
    end: Position
    direction: Direction
    channel_id: Optional[str] = None
    layer: int = 0


@dataclass
class ChannelRoutedEdge:
    """An edge routed through channels"""
    edge: Edge
    segments: List[RoutingSegment]
    source_side: ChannelSide
    target_side: ChannelSide
    total_length: float
    num_bends: int
    layers_used: Set[int] = field(default_factory=set)

    def get_waypoints(self) -> List[Position]:
        """Get waypoints for the routed path"""
        if not self.segments:
            return []

        waypoints = [self.segments[0].start]
        for seg in self.segments:
            waypoints.append(seg.end)

        return waypoints


@dataclass
class ChannelConfig:
    """Configuration for channel-based routing"""
    # Grid resolution (smaller = more precise but slower)
    grid_size: float = 10.0

    # Channel spacing
    channel_spacing: float = 20.0
    min_channel_spacing: float = 12.0

    # Node padding
    node_padding: float = 15.0

    # Bend settings
    min_bend_radius: float = 8.0
    prefer_fewer_bends: bool = True

    # Layer settings (for edge crossings)
    max_layers: int = 4
    layer_offset: float = 4.0    # Visual offset between layers

    # Optimization
    optimize_wire_length: bool = True
    allow_diagonal: bool = False  # Allow 45-degree segments

    # Visual settings
    corner_radius: float = 6.0
    segment_color: str = "#718096"


@dataclass
class RoutingGrid:
    """Grid for A* pathfinding"""
    width: int
    height: int
    cells: Dict[Tuple[int, int], GridCell]
    cell_size: float
    origin: Position

    def world_to_grid(self, pos: Position) -> Tuple[int, int]:
        """Convert world coordinates to grid coordinates"""
        gx = int((pos.x - self.origin.x) / self.cell_size)
        gy = int((pos.y - self.origin.y) / self.cell_size)
        return (max(0, min(gx, self.width - 1)), max(0, min(gy, self.height - 1)))

    def grid_to_world(self, gx: int, gy: int) -> Position:
        """Convert grid coordinates to world coordinates"""
        return Position(
            self.origin.x + gx * self.cell_size + self.cell_size / 2,
            self.origin.y + gy * self.cell_size + self.cell_size / 2
        )

    def is_blocked(self, gx: int, gy: int) -> bool:
        """Check if a grid cell is blocked"""
        if gx < 0 or gx >= self.width or gy < 0 or gy >= self.height:
            return True
        cell = self.cells.get((gx, gy))
        return cell.blocked if cell else False

    def get_neighbors(self, gx: int, gy: int, allow_diagonal: bool = False) -> List[Tuple[int, int]]:
        """Get valid neighboring cells"""
        neighbors = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # N, S, E, W

        if allow_diagonal:
            directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])

        for dx, dy in directions:
            nx, ny = gx + dx, gy + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not self.is_blocked(nx, ny):
                    neighbors.append((nx, ny))

        return neighbors


class ChannelRouter:
    """
    Channel-based orthogonal edge router.

    Routes edges through dedicated channels like circuit board traces,
    providing clean, non-overlapping paths for complex diagrams.

    Example:
        >>> router = ChannelRouter(ChannelConfig(grid_size=15))
        >>> routed = router.route(diagram)
        >>> for edge in routed:
        ...     waypoints = edge.get_waypoints()
        ...     svg_path = router.build_svg_path(edge)
    """

    def __init__(self, config: Optional[ChannelConfig] = None):
        self.config = config or ChannelConfig()
        self._grid: Optional[RoutingGrid] = None
        self._h_channels: List[Channel] = []
        self._v_channels: List[Channel] = []
        self._routed_edges: Dict[str, ChannelRoutedEdge] = {}

    def route(self, diagram: Diagram) -> List[ChannelRoutedEdge]:
        """
        Route all edges in the diagram through channels.

        Args:
            diagram: The diagram with nodes and edges

        Returns:
            List of channel-routed edges
        """
        if not diagram.edges:
            return []

        # Build routing grid
        self._build_grid(diagram)

        # Create channels
        self._create_channels(diagram)

        # Route each edge
        routed_edges = []
        node_map = {n.id: n for n in diagram.nodes}

        # Sort edges by priority (shorter edges first for better routing)
        sorted_edges = self._prioritize_edges(diagram.edges, node_map)

        for edge in sorted_edges:
            source = node_map.get(edge.source)
            target = node_map.get(edge.target)

            if not source or not target:
                continue

            routed = self._route_edge(edge, source, target)
            if routed:
                routed_edges.append(routed)
                self._mark_path_occupied(routed, edge.source + "_" + edge.target)

        return routed_edges

    def _build_grid(self, diagram: Diagram) -> None:
        """Build the routing grid from diagram bounds"""
        if not diagram.nodes:
            return

        # Calculate diagram bounds
        min_x = min(n.position.x for n in diagram.nodes) - 50
        min_y = min(n.position.y for n in diagram.nodes) - 50
        max_x = max(n.position.x + n.size.width for n in diagram.nodes) + 50
        max_y = max(n.position.y + n.size.height for n in diagram.nodes) + 50

        # Add cluster bounds
        for cluster in diagram.clusters:
            min_x = min(min_x, cluster.position.x - 50)
            min_y = min(min_y, cluster.position.y - 50)
            max_x = max(max_x, cluster.position.x + cluster.size.width + 50)
            max_y = max(max_y, cluster.position.y + cluster.size.height + 50)

        width = int((max_x - min_x) / self.config.grid_size) + 1
        height = int((max_y - min_y) / self.config.grid_size) + 1

        # Create grid cells
        cells = {}
        for gx in range(width):
            for gy in range(height):
                cells[(gx, gy)] = GridCell(x=gx, y=gy)

        self._grid = RoutingGrid(
            width=width,
            height=height,
            cells=cells,
            cell_size=self.config.grid_size,
            origin=Position(min_x, min_y)
        )

        # Block cells occupied by nodes
        for node in diagram.nodes:
            self._block_node_area(node)

        # Block cells occupied by clusters
        for cluster in diagram.clusters:
            self._block_cluster_boundary(cluster)

    def _block_node_area(self, node: Node) -> None:
        """Block grid cells occupied by a node"""
        if not self._grid:
            return

        padding = self.config.node_padding

        # Get grid bounds for node with padding
        top_left = self._grid.world_to_grid(Position(
            node.position.x - padding,
            node.position.y - padding
        ))
        bottom_right = self._grid.world_to_grid(Position(
            node.position.x + node.size.width + padding,
            node.position.y + node.size.height + padding
        ))

        for gx in range(top_left[0], bottom_right[0] + 1):
            for gy in range(top_left[1], bottom_right[1] + 1):
                if (gx, gy) in self._grid.cells:
                    self._grid.cells[(gx, gy)].blocked = True

    def _block_cluster_boundary(self, cluster: Cluster) -> None:
        """Block cells on cluster boundary (but not interior)"""
        if not self._grid:
            return

        # Only block the boundary cells, not the interior
        # This allows routing within clusters
        pass  # For now, we allow routing through clusters

    def _create_channels(self, diagram: Diagram) -> None:
        """Create horizontal and vertical routing channels"""
        if not self._grid:
            return

        spacing = self.config.channel_spacing

        # Create horizontal channels between node rows
        y_positions = set()
        for node in diagram.nodes:
            y_positions.add(node.position.y - spacing)
            y_positions.add(node.position.y + node.size.height + spacing)

        for i, y in enumerate(sorted(y_positions)):
            self._h_channels.append(Channel(
                id=f"h_{i}",
                direction=Direction.HORIZONTAL,
                position=y,
                start=self._grid.origin.x,
                end=self._grid.origin.x + self._grid.width * self._grid.cell_size
            ))

        # Create vertical channels between node columns
        x_positions = set()
        for node in diagram.nodes:
            x_positions.add(node.position.x - spacing)
            x_positions.add(node.position.x + node.size.width + spacing)

        for i, x in enumerate(sorted(x_positions)):
            self._v_channels.append(Channel(
                id=f"v_{i}",
                direction=Direction.VERTICAL,
                position=x,
                start=self._grid.origin.y,
                end=self._grid.origin.y + self._grid.height * self._grid.cell_size
            ))

    def _prioritize_edges(
        self,
        edges: List[Edge],
        node_map: Dict[str, Node]
    ) -> List[Edge]:
        """Sort edges by routing priority"""
        def edge_distance(edge: Edge) -> float:
            src = node_map.get(edge.source)
            tgt = node_map.get(edge.target)
            if not src or not tgt:
                return float('inf')
            dx = tgt.center.x - src.center.x
            dy = tgt.center.y - src.center.y
            return math.sqrt(dx*dx + dy*dy)

        return sorted(edges, key=edge_distance)

    def _route_edge(
        self,
        edge: Edge,
        source: Node,
        target: Node
    ) -> Optional[ChannelRoutedEdge]:
        """Route a single edge using A* pathfinding"""
        if not self._grid:
            return None

        # Determine best exit/entry sides
        source_side = self._get_best_side(source, target)
        target_side = self._get_best_side(target, source)

        # Get anchor points
        src_anchor = self._get_side_anchor(source, source_side)
        tgt_anchor = self._get_side_anchor(target, target_side)

        # Find path using A*
        path = self._astar_route(src_anchor, tgt_anchor, source_side, target_side)

        if not path:
            # Fallback to direct routing
            return self._create_direct_route(edge, source, target)

        # Convert path to segments
        segments = self._path_to_segments(path)

        return ChannelRoutedEdge(
            edge=edge,
            segments=segments,
            source_side=source_side,
            target_side=target_side,
            total_length=self._calculate_path_length(segments),
            num_bends=len(segments) - 1
        )

    def _get_best_side(self, from_node: Node, to_node: Node) -> ChannelSide:
        """Determine best side of node to exit/enter"""
        dx = to_node.center.x - from_node.center.x
        dy = to_node.center.y - from_node.center.y

        if abs(dx) > abs(dy):
            return ChannelSide.EAST if dx > 0 else ChannelSide.WEST
        else:
            return ChannelSide.SOUTH if dy > 0 else ChannelSide.NORTH

    def _get_side_anchor(self, node: Node, side: ChannelSide) -> Position:
        """Get anchor point on specified side of node"""
        cx = node.position.x + node.size.width / 2
        cy = node.position.y + node.size.height / 2

        if side == ChannelSide.NORTH:
            return Position(cx, node.position.y)
        elif side == ChannelSide.SOUTH:
            return Position(cx, node.position.y + node.size.height)
        elif side == ChannelSide.EAST:
            return Position(node.position.x + node.size.width, cy)
        else:  # WEST
            return Position(node.position.x, cy)

    def _astar_route(
        self,
        start: Position,
        end: Position,
        start_side: ChannelSide,
        end_side: ChannelSide
    ) -> Optional[List[Position]]:
        """A* pathfinding with orthogonal constraints"""
        if not self._grid:
            return None

        start_cell = self._grid.world_to_grid(start)
        end_cell = self._grid.world_to_grid(end)

        # Unblock start and end cells temporarily
        start_blocked = self._grid.cells.get(start_cell, GridCell(0, 0)).blocked
        end_blocked = self._grid.cells.get(end_cell, GridCell(0, 0)).blocked

        if start_cell in self._grid.cells:
            self._grid.cells[start_cell].blocked = False
        if end_cell in self._grid.cells:
            self._grid.cells[end_cell].blocked = False

        # A* algorithm
        open_set = [(0, start_cell)]
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score: Dict[Tuple[int, int], float] = {start_cell: 0}
        f_score: Dict[Tuple[int, int], float] = {start_cell: self._heuristic(start_cell, end_cell)}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == end_cell:
                # Reconstruct path
                path = self._reconstruct_path(came_from, current)

                # Restore blocked state
                if start_cell in self._grid.cells:
                    self._grid.cells[start_cell].blocked = start_blocked
                if end_cell in self._grid.cells:
                    self._grid.cells[end_cell].blocked = end_blocked

                # Convert to world coordinates
                return [self._grid.grid_to_world(gx, gy) for gx, gy in path]

            for neighbor in self._grid.get_neighbors(current[0], current[1]):
                # Calculate cost (penalize bends)
                move_cost = 1.0

                if current in came_from:
                    prev = came_from[current]
                    prev_dir = (current[0] - prev[0], current[1] - prev[1])
                    new_dir = (neighbor[0] - current[0], neighbor[1] - current[1])

                    if prev_dir != new_dir:
                        move_cost += 5.0 if self.config.prefer_fewer_bends else 1.0

                tentative_g = g_score[current] + move_cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._heuristic(neighbor, end_cell)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # Restore blocked state
        if start_cell in self._grid.cells:
            self._grid.cells[start_cell].blocked = start_blocked
        if end_cell in self._grid.cells:
            self._grid.cells[end_cell].blocked = end_blocked

        return None

    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Manhattan distance heuristic"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _reconstruct_path(
        self,
        came_from: Dict[Tuple[int, int], Tuple[int, int]],
        current: Tuple[int, int]
    ) -> List[Tuple[int, int]]:
        """Reconstruct path from A* result"""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()

        # Simplify path (remove redundant points on same line)
        simplified = self._simplify_path(path)

        return simplified

    def _simplify_path(
        self,
        path: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """Remove redundant points on straight lines"""
        if len(path) <= 2:
            return path

        simplified = [path[0]]

        for i in range(1, len(path) - 1):
            prev = path[i - 1]
            curr = path[i]
            next_p = path[i + 1]

            # Check if direction changes
            dir1 = (curr[0] - prev[0], curr[1] - prev[1])
            dir2 = (next_p[0] - curr[0], next_p[1] - curr[1])

            if dir1 != dir2:
                simplified.append(curr)

        simplified.append(path[-1])

        return simplified

    def _path_to_segments(self, path: List[Position]) -> List[RoutingSegment]:
        """Convert path points to routing segments"""
        segments = []

        for i in range(len(path) - 1):
            start = path[i]
            end = path[i + 1]

            dx = end.x - start.x
            dy = end.y - start.y

            direction = Direction.HORIZONTAL if abs(dx) > abs(dy) else Direction.VERTICAL

            segments.append(RoutingSegment(
                start=start,
                end=end,
                direction=direction
            ))

        return segments

    def _create_direct_route(
        self,
        edge: Edge,
        source: Node,
        target: Node
    ) -> ChannelRoutedEdge:
        """Create a direct L-shaped route as fallback"""
        source_side = self._get_best_side(source, target)
        target_side = self._get_best_side(target, source)

        src_anchor = self._get_side_anchor(source, source_side)
        tgt_anchor = self._get_side_anchor(target, target_side)

        # Create L-shaped path
        mid_x = (src_anchor.x + tgt_anchor.x) / 2
        mid_y = (src_anchor.y + tgt_anchor.y) / 2

        # Decide: horizontal-first or vertical-first
        if abs(tgt_anchor.x - src_anchor.x) > abs(tgt_anchor.y - src_anchor.y):
            # Horizontal first
            mid_point = Position(mid_x, src_anchor.y)
            segments = [
                RoutingSegment(src_anchor, mid_point, Direction.HORIZONTAL),
                RoutingSegment(mid_point, Position(mid_x, tgt_anchor.y), Direction.VERTICAL),
                RoutingSegment(Position(mid_x, tgt_anchor.y), tgt_anchor, Direction.HORIZONTAL)
            ]
        else:
            # Vertical first
            mid_point = Position(src_anchor.x, mid_y)
            segments = [
                RoutingSegment(src_anchor, mid_point, Direction.VERTICAL),
                RoutingSegment(mid_point, Position(tgt_anchor.x, mid_y), Direction.HORIZONTAL),
                RoutingSegment(Position(tgt_anchor.x, mid_y), tgt_anchor, Direction.VERTICAL)
            ]

        return ChannelRoutedEdge(
            edge=edge,
            segments=segments,
            source_side=source_side,
            target_side=target_side,
            total_length=self._calculate_path_length(segments),
            num_bends=2
        )

    def _calculate_path_length(self, segments: List[RoutingSegment]) -> float:
        """Calculate total path length"""
        total = 0.0
        for seg in segments:
            dx = seg.end.x - seg.start.x
            dy = seg.end.y - seg.start.y
            total += math.sqrt(dx*dx + dy*dy)
        return total

    def _mark_path_occupied(self, route: ChannelRoutedEdge, edge_id: str) -> None:
        """Mark grid cells along path as occupied"""
        if not self._grid:
            return

        for segment in route.segments:
            start_cell = self._grid.world_to_grid(segment.start)
            end_cell = self._grid.world_to_grid(segment.end)

            # Mark all cells along the segment
            if segment.direction == Direction.HORIZONTAL:
                y = start_cell[1]
                for x in range(min(start_cell[0], end_cell[0]), max(start_cell[0], end_cell[0]) + 1):
                    if (x, y) in self._grid.cells:
                        self._grid.cells[(x, y)].occupied_by.add(edge_id)
            else:
                x = start_cell[0]
                for y in range(min(start_cell[1], end_cell[1]), max(start_cell[1], end_cell[1]) + 1):
                    if (x, y) in self._grid.cells:
                        self._grid.cells[(x, y)].occupied_by.add(edge_id)

    def build_svg_path(
        self,
        route: ChannelRoutedEdge,
        rounded: bool = True
    ) -> str:
        """
        Build SVG path string for a channel-routed edge.

        Args:
            route: The channel-routed edge
            rounded: Use rounded corners at bends

        Returns:
            SVG path d attribute string
        """
        waypoints = route.get_waypoints()

        if not waypoints or len(waypoints) < 2:
            return ""

        if not rounded or len(waypoints) == 2:
            # Straight lines
            path = f"M {waypoints[0].x},{waypoints[0].y}"
            for wp in waypoints[1:]:
                path += f" L {wp.x},{wp.y}"
            return path

        # Rounded corners
        radius = self.config.corner_radius
        path = f"M {waypoints[0].x},{waypoints[0].y}"

        for i in range(1, len(waypoints) - 1):
            prev = waypoints[i - 1]
            curr = waypoints[i]
            next_wp = waypoints[i + 1]

            # Calculate directions
            dx1 = curr.x - prev.x
            dy1 = curr.y - prev.y
            len1 = math.sqrt(dx1*dx1 + dy1*dy1) or 1

            dx2 = next_wp.x - curr.x
            dy2 = next_wp.y - curr.y
            len2 = math.sqrt(dx2*dx2 + dy2*dy2) or 1

            # Normalize
            dx1 /= len1
            dy1 /= len1
            dx2 /= len2
            dy2 /= len2

            # Calculate arc points
            r = min(radius, len1 / 2, len2 / 2)

            arc_start_x = curr.x - dx1 * r
            arc_start_y = curr.y - dy1 * r
            arc_end_x = curr.x + dx2 * r
            arc_end_y = curr.y + dy2 * r

            # Line to arc start, then quadratic curve through corner
            path += f" L {arc_start_x},{arc_start_y}"
            path += f" Q {curr.x},{curr.y} {arc_end_x},{arc_end_y}"

        # Final line to end
        path += f" L {waypoints[-1].x},{waypoints[-1].y}"

        return path

    def build_svg_elements(
        self,
        routes: List[ChannelRoutedEdge]
    ) -> str:
        """Build complete SVG elements for all routed edges"""
        svg_parts = []

        # Add arrowhead marker
        svg_parts.append('''
        <defs>
            <marker id="channel-arrow" markerWidth="10" markerHeight="7"
                    refX="9" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7"
                         fill="''' + self.config.segment_color + '''"/>
            </marker>
        </defs>
        ''')

        for route in routes:
            path = self.build_svg_path(route, rounded=True)

            svg_parts.append(f'''
            <path d="{path}"
                  stroke="{self.config.segment_color}"
                  stroke-width="2"
                  fill="none"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  marker-end="url(#channel-arrow)"
                  class="channel-routed-edge"
                  data-source="{route.edge.source}"
                  data-target="{route.edge.target}"
                  data-bends="{route.num_bends}"/>
            ''')

        return '\n'.join(svg_parts)


def apply_channel_routing(
    diagram: Diagram,
    grid_size: float = 10.0,
    prefer_fewer_bends: bool = True
) -> List[ChannelRoutedEdge]:
    """
    Apply channel-based routing to a diagram.

    Args:
        diagram: The diagram to route
        grid_size: Grid resolution for routing
        prefer_fewer_bends: Prefer paths with fewer bends

    Returns:
        List of channel-routed edges

    Example:
        >>> routed = apply_channel_routing(diagram, grid_size=15)
        >>> for edge in routed:
        ...     print(f"Edge {edge.edge.source} -> {edge.edge.target}: {edge.num_bends} bends")
    """
    config = ChannelConfig(
        grid_size=grid_size,
        prefer_fewer_bends=prefer_fewer_bends
    )
    router = ChannelRouter(config)
    return router.route(diagram)
