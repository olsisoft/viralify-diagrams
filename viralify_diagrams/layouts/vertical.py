"""
Vertical Layout Engine

Arranges nodes in a top-to-bottom flow, ideal for hierarchies and layered architectures.
"""

from typing import List, Dict, Set
from collections import defaultdict

from viralify_diagrams.layouts.base import BaseLayout
from viralify_diagrams.core.diagram import Diagram, Node, Position


class VerticalLayout(BaseLayout):
    """
    Vertical top-to-bottom layout.

    Ideal for:
    - Hierarchies
    - Layered architectures
    - Organization charts
    - Decision trees
    """

    def __init__(self):
        super().__init__()
        self.spacing_x = 150
        self.spacing_y = 120

    def layout(self, diagram: Diagram) -> Diagram:
        """Apply vertical layout to the diagram"""
        if not diagram.nodes:
            return diagram

        # Build adjacency list and calculate levels
        levels = self._calculate_levels(diagram)

        # Position nodes by level
        self._position_nodes_by_level(diagram, levels)

        # Layout clusters
        for cluster in diagram.clusters:
            self._layout_cluster(cluster, diagram.nodes, diagram)

        # Center in canvas
        self._center_diagram(diagram)

        # Calculate edge control points
        self._calculate_edge_control_points(diagram)

        # Assign animation order (top to bottom)
        diagram.assign_animation_order()

        return diagram

    def _calculate_levels(self, diagram: Diagram) -> Dict[str, int]:
        """
        Calculate the vertical level (row) for each node.
        """
        # Build adjacency list
        outgoing: Dict[str, List[str]] = defaultdict(list)
        incoming: Dict[str, int] = {node.id: 0 for node in diagram.nodes}

        for edge in diagram.edges:
            outgoing[edge.source].append(edge.target)
            if edge.target in incoming:
                incoming[edge.target] += 1

        # Find sources (no incoming edges)
        sources = [nid for nid, count in incoming.items() if count == 0]
        if not sources:
            sources = [diagram.nodes[0].id] if diagram.nodes else []

        # BFS to assign levels
        levels: Dict[str, int] = {}
        queue = [(nid, 0) for nid in sources]
        visited: Set[str] = set()

        while queue:
            node_id, level = queue.pop(0)
            if node_id in visited:
                if node_id in levels and level > levels[node_id]:
                    levels[node_id] = level
                continue

            visited.add(node_id)
            levels[node_id] = level

            for target in outgoing[node_id]:
                queue.append((target, level + 1))

        # Handle disconnected nodes
        for node in diagram.nodes:
            if node.id not in levels:
                levels[node.id] = 0

        return levels

    def _position_nodes_by_level(
        self,
        diagram: Diagram,
        levels: Dict[str, int]
    ) -> None:
        """Position nodes based on their levels (vertical)"""
        # Group nodes by level
        level_groups: Dict[int, List[Node]] = defaultdict(list)
        for node in diagram.nodes:
            level = levels.get(node.id, 0)
            level_groups[level].append(node)

        # Position each level
        for level, nodes in level_groups.items():
            y = diagram.padding + level * self.spacing_y

            # Calculate total width needed
            total_width = sum(n.size.width for n in nodes) + (len(nodes) - 1) * self.spacing_x
            start_x = (diagram.width - total_width) / 2

            current_x = start_x
            for node in nodes:
                node.position = Position(current_x, y)
                current_x += node.size.width + self.spacing_x
