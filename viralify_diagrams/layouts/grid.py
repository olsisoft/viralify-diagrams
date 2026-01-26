"""
Grid Layout Engine

Arranges nodes in a uniform grid pattern.
"""

import math
from typing import List

from viralify_diagrams.layouts.base import BaseLayout
from viralify_diagrams.core.diagram import Diagram, Node, Position


class GridLayout(BaseLayout):
    """
    Grid layout arranges nodes in rows and columns.

    Ideal for:
    - Comparing similar components
    - Microservices overview
    - Feature comparison
    - Equal-weight relationships
    """

    def __init__(self, columns: int = None):
        super().__init__()
        self.columns = columns  # Auto-calculate if None
        self.spacing_x = 180
        self.spacing_y = 120

    def layout(self, diagram: Diagram) -> Diagram:
        """Apply grid layout to the diagram"""
        if not diagram.nodes:
            return diagram

        # Calculate grid dimensions
        n = len(diagram.nodes)
        if self.columns:
            cols = self.columns
        else:
            # Auto-calculate: aim for roughly square grid, favor wider
            cols = math.ceil(math.sqrt(n * 1.5))

        rows = math.ceil(n / cols)

        # Position nodes in grid
        self._position_nodes_in_grid(diagram, rows, cols)

        # Layout clusters
        for cluster in diagram.clusters:
            self._layout_cluster(cluster, diagram.nodes, diagram)

        # Center in canvas
        self._center_diagram(diagram)

        # Calculate edge control points
        self._calculate_edge_control_points(diagram)

        # Assign animation order (left to right, top to bottom)
        for i, node in enumerate(diagram.nodes):
            node.order = i

        return diagram

    def _position_nodes_in_grid(
        self,
        diagram: Diagram,
        rows: int,
        cols: int
    ) -> None:
        """Position nodes in a grid pattern"""
        # Calculate cell size
        cell_width = diagram.nodes[0].size.width + self.spacing_x
        cell_height = diagram.nodes[0].size.height + self.spacing_y

        # Calculate starting position to center the grid
        grid_width = cols * cell_width - self.spacing_x
        grid_height = rows * cell_height - self.spacing_y
        start_x = (diagram.width - grid_width) / 2
        start_y = (diagram.height - grid_height) / 2

        for i, node in enumerate(diagram.nodes):
            row = i // cols
            col = i % cols

            x = start_x + col * cell_width
            y = start_y + row * cell_height

            node.position = Position(x, y)
