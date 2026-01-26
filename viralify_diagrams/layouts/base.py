"""
Base Layout Engine

Abstract base class for all layout engines.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Optional
import math

from viralify_diagrams.core.diagram import Diagram, Node, Edge, Cluster, Position, Size


class BaseLayout(ABC):
    """
    Abstract base class for layout engines.

    Layout engines are responsible for positioning nodes, edges, and clusters
    within the diagram canvas.
    """

    def __init__(self):
        self.diagram: Optional[Diagram] = None
        self.spacing_x: float = 180  # Horizontal spacing between nodes
        self.spacing_y: float = 120  # Vertical spacing between nodes
        self.cluster_padding: float = 40  # Padding inside clusters

    @abstractmethod
    def layout(self, diagram: Diagram) -> Diagram:
        """
        Apply layout to the diagram.

        Args:
            diagram: The diagram to layout

        Returns:
            The diagram with updated positions
        """
        pass

    def _calculate_bounds(self, nodes: List[Node]) -> Tuple[float, float, float, float]:
        """Calculate bounding box of a set of nodes"""
        if not nodes:
            return (0, 0, 0, 0)

        min_x = min(n.position.x for n in nodes)
        min_y = min(n.position.y for n in nodes)
        max_x = max(n.position.x + n.size.width for n in nodes)
        max_y = max(n.position.y + n.size.height for n in nodes)

        return (min_x, min_y, max_x - min_x, max_y - min_y)

    def _center_diagram(self, diagram: Diagram) -> None:
        """Center all elements within the canvas"""
        if not diagram.nodes:
            return

        # Calculate current bounds
        min_x, min_y, content_width, content_height = self._calculate_bounds(diagram.nodes)

        # Calculate offset to center
        offset_x = (diagram.width - content_width) / 2 - min_x
        offset_y = (diagram.height - content_height) / 2 - min_y

        # Apply offset to all nodes
        for node in diagram.nodes:
            node.position.x += offset_x
            node.position.y += offset_y

        # Apply offset to all clusters
        for cluster in diagram.clusters:
            cluster.position.x += offset_x
            cluster.position.y += offset_y

    def _calculate_edge_control_points(self, diagram: Diagram) -> None:
        """Calculate control points for curved edges"""
        for edge in diagram.edges:
            source = diagram.get_node(edge.source)
            target = diagram.get_node(edge.target)

            if not source or not target:
                continue

            # Get center points
            source_center = source.center
            target_center = target.center

            # Calculate midpoint
            mid_x = (source_center.x + target_center.x) / 2
            mid_y = (source_center.y + target_center.y) / 2

            # Add slight curve based on distance
            dx = target_center.x - source_center.x
            dy = target_center.y - source_center.y
            distance = math.sqrt(dx * dx + dy * dy)

            # Perpendicular offset for curve
            curve_strength = min(distance * 0.15, 50)

            # Normalize perpendicular direction
            if distance > 0:
                perp_x = -dy / distance * curve_strength
                perp_y = dx / distance * curve_strength
            else:
                perp_x = perp_y = 0

            # Set control point
            edge.control_points = [
                Position(mid_x + perp_x, mid_y + perp_y)
            ]

    def _layout_cluster(self, cluster: Cluster, nodes: List[Node], diagram: Diagram) -> None:
        """Calculate cluster size and position based on its nodes"""
        cluster_nodes = [n for n in nodes if n.id in cluster.nodes]

        if not cluster_nodes:
            return

        # Get bounding box of nodes
        min_x, min_y, width, height = self._calculate_bounds(cluster_nodes)

        # Add padding
        cluster.position = Position(
            min_x - self.cluster_padding,
            min_y - self.cluster_padding
        )
        cluster.size = Size(
            width + 2 * self.cluster_padding,
            height + 2 * self.cluster_padding
        )

    def _get_node_anchor(
        self,
        node: Node,
        direction: str
    ) -> Position:
        """
        Get anchor point on node edge for edge connection.

        Args:
            node: The node
            direction: One of 'top', 'bottom', 'left', 'right'

        Returns:
            Position of the anchor point
        """
        x, y = node.position.x, node.position.y
        w, h = node.size.width, node.size.height

        anchors = {
            "top": Position(x + w / 2, y),
            "bottom": Position(x + w / 2, y + h),
            "left": Position(x, y + h / 2),
            "right": Position(x + w, y + h / 2),
        }

        return anchors.get(direction, node.center)
