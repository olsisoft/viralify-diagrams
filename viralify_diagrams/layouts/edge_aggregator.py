"""
Edge Aggregation for Enterprise Diagrams

Aggregates multiple edges between clusters or node groups into
single representative edges with count badges.

Key features:
- Cluster-to-cluster aggregation
- Bidirectional edge merging
- Count badges with styling
- Preserves edge metadata (types, weights)
- Supports filtering and drill-down
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Tuple, Any
from enum import Enum
from collections import defaultdict

from viralify_diagrams.core.diagram import Diagram, Node, Edge, Cluster, Position, Size


class AggregationMode(str, Enum):
    """Edge aggregation modes"""
    CLUSTER = "cluster"           # Aggregate by cluster membership
    NODE_GROUP = "node_group"     # Aggregate by custom node groups
    BIDIRECTIONAL = "bidirectional"  # Merge A->B and B->A
    EDGE_TYPE = "edge_type"       # Aggregate by edge type/label


@dataclass
class AggregationConfig:
    """Configuration for edge aggregation"""
    mode: AggregationMode = AggregationMode.CLUSTER

    # Minimum edges to trigger aggregation
    min_edges_to_aggregate: int = 2

    # Show count badge
    show_count_badge: bool = True

    # Badge styling
    badge_radius: int = 12
    badge_fill: str = "#4A5568"
    badge_text_color: str = "#FFFFFF"
    badge_font_size: int = 11

    # Aggregate edge styling
    aggregate_stroke_width: float = 2.0
    aggregate_stroke_color: str = "#718096"

    # Scale stroke width by count
    scale_by_count: bool = True
    max_stroke_width: float = 8.0

    # Preserve individual edges for drill-down
    preserve_original_edges: bool = True

    # Custom node groups (for NODE_GROUP mode)
    node_groups: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class EdgeMetadata:
    """Metadata for aggregated edges"""
    edge_types: Set[str] = field(default_factory=set)
    total_weight: float = 0.0
    labels: List[str] = field(default_factory=list)
    original_edges: List[Edge] = field(default_factory=list)


@dataclass
class AggregatedEdge:
    """An aggregated edge representing multiple connections"""
    id: str
    source_group: str             # Cluster/group ID
    target_group: str             # Cluster/group ID
    source_pos: Position          # Position for rendering
    target_pos: Position
    count: int                    # Number of aggregated edges
    metadata: EdgeMetadata
    bidirectional: bool = False   # True if edges flow both ways

    # Badge position (calculated)
    badge_pos: Optional[Position] = None

    @property
    def stroke_width(self) -> float:
        """Calculate stroke width based on count"""
        return min(1.0 + 0.5 * self.count, 8.0)


@dataclass
class AggregationResult:
    """Result of edge aggregation"""
    aggregated_edges: List[AggregatedEdge]
    original_edges: List[Edge]    # Preserved for drill-down
    group_map: Dict[str, str]     # node_id -> group_id mapping
    stats: Dict[str, Any]


class EdgeAggregator:
    """
    Edge Aggregator for enterprise diagrams.

    Reduces visual complexity by combining multiple edges
    between clusters or node groups into single aggregated edges.

    Example:
        >>> aggregator = EdgeAggregator(AggregationConfig(mode=AggregationMode.CLUSTER))
        >>> result = aggregator.aggregate(diagram)
        >>> for agg_edge in result.aggregated_edges:
        ...     print(f"{agg_edge.source_group} -> {agg_edge.target_group}: {agg_edge.count}")
    """

    def __init__(self, config: Optional[AggregationConfig] = None):
        self.config = config or AggregationConfig()

    def aggregate(self, diagram: Diagram) -> AggregationResult:
        """
        Aggregate edges in the diagram.

        Args:
            diagram: The diagram with nodes, edges, and clusters

        Returns:
            AggregationResult with aggregated edges and metadata
        """
        # Build group mapping
        group_map = self._build_group_map(diagram)

        # Group edges by source-target groups
        edge_groups = self._group_edges(diagram.edges, group_map)

        # Create aggregated edges
        aggregated = self._create_aggregated_edges(edge_groups, diagram, group_map)

        # Calculate badge positions
        for agg_edge in aggregated:
            agg_edge.badge_pos = self._calculate_badge_position(agg_edge)

        # Compute stats
        stats = {
            "original_edge_count": len(diagram.edges),
            "aggregated_edge_count": len(aggregated),
            "reduction_ratio": 1 - len(aggregated) / max(len(diagram.edges), 1),
            "group_count": len(set(group_map.values())),
            "max_aggregation": max((e.count for e in aggregated), default=0),
        }

        return AggregationResult(
            aggregated_edges=aggregated,
            original_edges=diagram.edges if self.config.preserve_original_edges else [],
            group_map=group_map,
            stats=stats
        )

    def _build_group_map(self, diagram: Diagram) -> Dict[str, str]:
        """Build mapping of node_id -> group_id"""
        group_map = {}

        if self.config.mode == AggregationMode.CLUSTER:
            # Map nodes to their clusters
            for cluster in diagram.clusters:
                for node_id in cluster.node_ids:
                    group_map[node_id] = cluster.id

            # Nodes not in clusters get their own group
            for node in diagram.nodes:
                if node.id not in group_map:
                    group_map[node.id] = f"standalone_{node.id}"

        elif self.config.mode == AggregationMode.NODE_GROUP:
            # Use custom node groups
            for group_id, node_ids in self.config.node_groups.items():
                for node_id in node_ids:
                    group_map[node_id] = group_id

            # Ungrouped nodes
            for node in diagram.nodes:
                if node.id not in group_map:
                    group_map[node.id] = f"ungrouped_{node.id}"

        elif self.config.mode == AggregationMode.BIDIRECTIONAL:
            # Each node is its own group (aggregation by direction)
            for node in diagram.nodes:
                group_map[node.id] = node.id

        elif self.config.mode == AggregationMode.EDGE_TYPE:
            # Each node is its own group (aggregation by edge type)
            for node in diagram.nodes:
                group_map[node.id] = node.id

        return group_map

    def _group_edges(
        self,
        edges: List[Edge],
        group_map: Dict[str, str]
    ) -> Dict[Tuple[str, str], List[Edge]]:
        """Group edges by source-target group pairs"""
        edge_groups: Dict[Tuple[str, str], List[Edge]] = defaultdict(list)

        for edge in edges:
            src_group = group_map.get(edge.source, edge.source)
            tgt_group = group_map.get(edge.target, edge.target)

            # For bidirectional mode, use canonical key (sorted)
            if self.config.mode == AggregationMode.BIDIRECTIONAL:
                key = tuple(sorted([src_group, tgt_group]))
            else:
                key = (src_group, tgt_group)

            edge_groups[key].append(edge)

        return edge_groups

    def _create_aggregated_edges(
        self,
        edge_groups: Dict[Tuple[str, str], List[Edge]],
        diagram: Diagram,
        group_map: Dict[str, str]
    ) -> List[AggregatedEdge]:
        """Create aggregated edges from edge groups"""
        aggregated = []
        node_map = {n.id: n for n in diagram.nodes}
        cluster_map = {c.id: c for c in diagram.clusters}

        for (src_group, tgt_group), edges in edge_groups.items():
            # Skip if below threshold
            if len(edges) < self.config.min_edges_to_aggregate:
                # Create individual aggregated edges
                for edge in edges:
                    src_node = node_map.get(edge.source)
                    tgt_node = node_map.get(edge.target)
                    if src_node and tgt_node:
                        aggregated.append(AggregatedEdge(
                            id=f"agg_{edge.source}_{edge.target}",
                            source_group=src_group,
                            target_group=tgt_group,
                            source_pos=src_node.center,
                            target_pos=tgt_node.center,
                            count=1,
                            metadata=EdgeMetadata(
                                edge_types={edge.label} if edge.label else set(),
                                labels=[edge.label] if edge.label else [],
                                original_edges=[edge]
                            ),
                            bidirectional=False
                        ))
                continue

            # Calculate group positions
            src_pos = self._get_group_center(src_group, group_map, node_map, cluster_map)
            tgt_pos = self._get_group_center(tgt_group, group_map, node_map, cluster_map)

            if not src_pos or not tgt_pos:
                continue

            # Collect metadata
            metadata = EdgeMetadata(
                edge_types=set(),
                total_weight=0.0,
                labels=[],
                original_edges=edges
            )

            for edge in edges:
                if edge.label:
                    metadata.edge_types.add(edge.label)
                    metadata.labels.append(edge.label)

            # Check bidirectionality
            bidirectional = False
            if self.config.mode == AggregationMode.BIDIRECTIONAL:
                src_to_tgt = sum(1 for e in edges if group_map.get(e.source) == src_group)
                tgt_to_src = len(edges) - src_to_tgt
                bidirectional = src_to_tgt > 0 and tgt_to_src > 0

            aggregated.append(AggregatedEdge(
                id=f"agg_{src_group}_{tgt_group}",
                source_group=src_group,
                target_group=tgt_group,
                source_pos=src_pos,
                target_pos=tgt_pos,
                count=len(edges),
                metadata=metadata,
                bidirectional=bidirectional
            ))

        return aggregated

    def _get_group_center(
        self,
        group_id: str,
        group_map: Dict[str, str],
        node_map: Dict[str, Node],
        cluster_map: Dict[str, Cluster]
    ) -> Optional[Position]:
        """Get the center position of a group"""
        # Check if it's a cluster
        if group_id in cluster_map:
            cluster = cluster_map[group_id]
            return Position(
                cluster.position.x + cluster.size.width / 2,
                cluster.position.y + cluster.size.height / 2
            )

        # Check if it's a standalone node
        if group_id.startswith("standalone_"):
            node_id = group_id[11:]  # Remove "standalone_" prefix
            if node_id in node_map:
                return node_map[node_id].center

        # Find all nodes in the group
        nodes_in_group = [
            node_map[node_id]
            for node_id, gid in group_map.items()
            if gid == group_id and node_id in node_map
        ]

        if not nodes_in_group:
            # Try direct node lookup
            if group_id in node_map:
                return node_map[group_id].center
            return None

        # Calculate centroid
        avg_x = sum(n.center.x for n in nodes_in_group) / len(nodes_in_group)
        avg_y = sum(n.center.y for n in nodes_in_group) / len(nodes_in_group)

        return Position(avg_x, avg_y)

    def _calculate_badge_position(self, edge: AggregatedEdge) -> Position:
        """Calculate position for the count badge"""
        # Place badge at midpoint of edge
        mid_x = (edge.source_pos.x + edge.target_pos.x) / 2
        mid_y = (edge.source_pos.y + edge.target_pos.y) / 2

        return Position(mid_x, mid_y)

    def build_svg_elements(self, result: AggregationResult) -> str:
        """
        Build SVG elements for aggregated edges.

        Returns SVG string with edges and badges.
        """
        svg_parts = []

        # Define filter for badge shadow
        svg_parts.append('''
        <defs>
            <filter id="badge-shadow" x="-50%" y="-50%" width="200%" height="200%">
                <feDropShadow dx="0" dy="1" stdDeviation="2" flood-opacity="0.3"/>
            </filter>
        </defs>
        ''')

        for edge in result.aggregated_edges:
            # Calculate stroke width
            stroke_width = self.config.aggregate_stroke_width
            if self.config.scale_by_count:
                stroke_width = min(
                    stroke_width + 0.5 * edge.count,
                    self.config.max_stroke_width
                )

            # Edge path
            path = self._build_edge_path(edge)

            # Edge element
            edge_svg = f'''
            <path d="{path}"
                  stroke="{self.config.aggregate_stroke_color}"
                  stroke-width="{stroke_width}"
                  fill="none"
                  stroke-linecap="round"
                  class="aggregated-edge"
                  data-source="{edge.source_group}"
                  data-target="{edge.target_group}"
                  data-count="{edge.count}"/>
            '''
            svg_parts.append(edge_svg)

            # Bidirectional arrows
            if edge.bidirectional:
                svg_parts.append(self._build_bidirectional_arrows(edge, stroke_width))

            # Count badge
            if self.config.show_count_badge and edge.count > 1 and edge.badge_pos:
                badge_svg = f'''
                <g class="count-badge" filter="url(#badge-shadow)">
                    <circle cx="{edge.badge_pos.x}" cy="{edge.badge_pos.y}"
                            r="{self.config.badge_radius}"
                            fill="{self.config.badge_fill}"/>
                    <text x="{edge.badge_pos.x}" y="{edge.badge_pos.y}"
                          text-anchor="middle"
                          dominant-baseline="central"
                          fill="{self.config.badge_text_color}"
                          font-size="{self.config.badge_font_size}"
                          font-weight="600"
                          font-family="Inter, sans-serif">
                        {edge.count}
                    </text>
                </g>
                '''
                svg_parts.append(badge_svg)

        return '\n'.join(svg_parts)

    def _build_edge_path(self, edge: AggregatedEdge) -> str:
        """Build SVG path for an aggregated edge"""
        # Simple bezier curve
        dx = edge.target_pos.x - edge.source_pos.x
        dy = edge.target_pos.y - edge.source_pos.y

        # Control points for curve
        cx1 = edge.source_pos.x + dx * 0.25
        cy1 = edge.source_pos.y + dy * 0.1
        cx2 = edge.target_pos.x - dx * 0.25
        cy2 = edge.target_pos.y - dy * 0.1

        return f"M {edge.source_pos.x},{edge.source_pos.y} C {cx1},{cy1} {cx2},{cy2} {edge.target_pos.x},{edge.target_pos.y}"

    def _build_bidirectional_arrows(self, edge: AggregatedEdge, stroke_width: float) -> str:
        """Build arrows for bidirectional edges"""
        import math

        dx = edge.target_pos.x - edge.source_pos.x
        dy = edge.target_pos.y - edge.source_pos.y
        angle = math.atan2(dy, dx)

        arrow_size = 6 + stroke_width

        # Forward arrow at target
        ax1 = edge.target_pos.x - arrow_size * math.cos(angle - 0.4)
        ay1 = edge.target_pos.y - arrow_size * math.sin(angle - 0.4)
        ax2 = edge.target_pos.x - arrow_size * math.cos(angle + 0.4)
        ay2 = edge.target_pos.y - arrow_size * math.sin(angle + 0.4)

        forward = f'''
        <polygon points="{edge.target_pos.x},{edge.target_pos.y} {ax1},{ay1} {ax2},{ay2}"
                 fill="{self.config.aggregate_stroke_color}"/>
        '''

        # Backward arrow at source
        bx1 = edge.source_pos.x + arrow_size * math.cos(angle - 0.4)
        by1 = edge.source_pos.y + arrow_size * math.sin(angle - 0.4)
        bx2 = edge.source_pos.x + arrow_size * math.cos(angle + 0.4)
        by2 = edge.source_pos.y + arrow_size * math.sin(angle + 0.4)

        backward = f'''
        <polygon points="{edge.source_pos.x},{edge.source_pos.y} {bx1},{by1} {bx2},{by2}"
                 fill="{self.config.aggregate_stroke_color}"/>
        '''

        return forward + backward


def aggregate_edges(
    diagram: Diagram,
    mode: AggregationMode = AggregationMode.CLUSTER,
    min_edges: int = 2
) -> AggregationResult:
    """
    Aggregate edges in a diagram.

    Args:
        diagram: The diagram to aggregate
        mode: Aggregation mode
        min_edges: Minimum edges to trigger aggregation

    Returns:
        AggregationResult with aggregated edges

    Example:
        >>> result = aggregate_edges(diagram, mode=AggregationMode.CLUSTER)
        >>> print(f"Reduced {result.stats['original_edge_count']} edges to {result.stats['aggregated_edge_count']}")
    """
    config = AggregationConfig(mode=mode, min_edges_to_aggregate=min_edges)
    aggregator = EdgeAggregator(config)
    return aggregator.aggregate(diagram)
