"""
Radial Layout Engine

Arranges nodes in concentric circles around a central node.
"""

import math
from typing import List, Dict, Set, Optional
from collections import defaultdict

from viralify_diagrams.layouts.base import BaseLayout
from viralify_diagrams.core.diagram import Diagram, Node, Position


class RadialLayout(BaseLayout):
    """
    Radial layout with a central node and satellites.

    Ideal for:
    - Hub-and-spoke architectures
    - API/Service relationships
    - Dependency visualization
    - Star topologies
    """

    def __init__(self, center_node_id: Optional[str] = None):
        super().__init__()
        self.center_node_id = center_node_id
        self.min_radius = 200
        self.radius_increment = 150

    def layout(self, diagram: Diagram) -> Diagram:
        """Apply radial layout to the diagram"""
        if not diagram.nodes:
            return diagram

        # Find center node
        center_node = self._find_center_node(diagram)

        # Calculate rings (distance from center)
        rings = self._calculate_rings(diagram, center_node)

        # Position nodes in rings
        self._position_nodes_in_rings(diagram, center_node, rings)

        # Layout clusters
        for cluster in diagram.clusters:
            self._layout_cluster(cluster, diagram.nodes, diagram)

        # Center in canvas
        self._center_diagram(diagram)

        # Calculate edge control points
        self._calculate_edge_control_points(diagram)

        # Assign animation order (center outward)
        self._assign_radial_order(diagram, center_node, rings)

        return diagram

    def _find_center_node(self, diagram: Diagram) -> Node:
        """Find the most connected node to use as center"""
        if self.center_node_id:
            node = diagram.get_node(self.center_node_id)
            if node:
                return node

        # Find node with most connections
        connection_count: Dict[str, int] = defaultdict(int)
        for edge in diagram.edges:
            connection_count[edge.source] += 1
            connection_count[edge.target] += 1

        if connection_count:
            center_id = max(connection_count.keys(), key=lambda x: connection_count[x])
            return diagram.get_node(center_id) or diagram.nodes[0]

        return diagram.nodes[0]

    def _calculate_rings(
        self,
        diagram: Diagram,
        center: Node
    ) -> Dict[int, List[Node]]:
        """
        Calculate which ring each node belongs to.
        Ring 0 = center, Ring 1 = directly connected, etc.
        """
        # Build adjacency list (undirected)
        neighbors: Dict[str, Set[str]] = defaultdict(set)
        for edge in diagram.edges:
            neighbors[edge.source].add(edge.target)
            neighbors[edge.target].add(edge.source)

        # BFS from center
        rings: Dict[int, List[Node]] = defaultdict(list)
        rings[0].append(center)

        visited = {center.id}
        queue = [(nid, 1) for nid in neighbors[center.id]]

        while queue:
            node_id, ring = queue.pop(0)
            if node_id in visited:
                continue

            visited.add(node_id)
            node = diagram.get_node(node_id)
            if node:
                rings[ring].append(node)

            for neighbor_id in neighbors[node_id]:
                if neighbor_id not in visited:
                    queue.append((neighbor_id, ring + 1))

        # Handle disconnected nodes - put them in outermost ring
        max_ring = max(rings.keys()) if rings else 0
        for node in diagram.nodes:
            if node.id not in visited:
                rings[max_ring + 1].append(node)

        return rings

    def _position_nodes_in_rings(
        self,
        diagram: Diagram,
        center: Node,
        rings: Dict[int, List[Node]]
    ) -> None:
        """Position nodes in concentric rings"""
        canvas_center_x = diagram.width / 2
        canvas_center_y = diagram.height / 2

        for ring_num, nodes in rings.items():
            if ring_num == 0:
                # Center node
                for node in nodes:
                    node.position = Position(
                        canvas_center_x - node.size.width / 2,
                        canvas_center_y - node.size.height / 2
                    )
            else:
                # Calculate radius for this ring
                radius = self.min_radius + (ring_num - 1) * self.radius_increment

                # Distribute nodes evenly around the ring
                angle_step = 2 * math.pi / len(nodes) if nodes else 0
                start_angle = -math.pi / 2  # Start from top

                for i, node in enumerate(nodes):
                    angle = start_angle + i * angle_step
                    x = canvas_center_x + radius * math.cos(angle) - node.size.width / 2
                    y = canvas_center_y + radius * math.sin(angle) - node.size.height / 2
                    node.position = Position(x, y)

    def _assign_radial_order(
        self,
        diagram: Diagram,
        center: Node,
        rings: Dict[int, List[Node]]
    ) -> None:
        """Assign animation order: center first, then outward"""
        order = 0
        for ring_num in sorted(rings.keys()):
            for node in rings[ring_num]:
                node.order = order
                order += 1

        # Edges get order based on their source node
        for edge in diagram.edges:
            source = diagram.get_node(edge.source)
            if source:
                edge.order = source.order + 1
