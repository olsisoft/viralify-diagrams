"""
SVG Exporter

Exports diagrams as static SVG with named groups for external animation.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import html

from viralify_diagrams.core.diagram import Diagram, Node, Edge, Cluster, NodeShape, EdgeStyle, EdgeDirection
from viralify_diagrams.core.theme import Theme, get_theme_manager


@dataclass
class SVGElement:
    """An SVG element with metadata"""
    id: str
    element_type: str  # node, edge, cluster
    svg_content: str
    order: int
    metadata: Dict[str, Any]


class SVGExporter:
    """
    Exports diagrams as static SVG.

    Features:
    - Named groups for each element (for animation targeting)
    - Theme-aware styling
    - Proper layering (clusters -> nodes -> edges)
    """

    def __init__(self, theme: Optional[Theme] = None):
        self.theme = theme
        self._elements: List[SVGElement] = []

    def export(self, diagram: Diagram, output_path: Optional[str] = None) -> str:
        """
        Export diagram to SVG.

        Args:
            diagram: The diagram to export
            output_path: Optional path to save SVG file

        Returns:
            SVG content as string
        """
        # Get theme
        if self.theme:
            theme = self.theme
        else:
            theme = get_theme_manager().get(diagram.theme)

        self._elements = []

        # Build SVG content
        svg_content = self._build_svg(diagram, theme)

        # Save to file if path provided
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(svg_content)

        return svg_content

    def _build_svg(self, diagram: Diagram, theme: Theme) -> str:
        """Build complete SVG document"""
        # SVG header
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {diagram.width} {diagram.height}"
     width="{diagram.width}"
     height="{diagram.height}"
     id="viralify-diagram">
  <title>{html.escape(diagram.title)}</title>
  <desc>{html.escape(diagram.description)}</desc>

  <!-- Styles -->
  <defs>
    {self._build_styles(theme)}
    {self._build_markers(theme)}
    {self._build_filters(theme)}
  </defs>

  <!-- Background -->
  <rect width="100%" height="100%" fill="{theme.colors.background}" />

  <!-- Diagram Content -->
  <g id="diagram-content">
'''
        # Render clusters (background layer)
        svg += '    <!-- Clusters -->\n    <g id="clusters-layer">\n'
        for cluster in sorted(diagram.clusters, key=lambda c: c.order):
            svg += self._render_cluster(cluster, theme)
        svg += '    </g>\n\n'

        # Render edges (middle layer)
        svg += '    <!-- Edges -->\n    <g id="edges-layer">\n'
        for edge in sorted(diagram.edges, key=lambda e: e.order):
            svg += self._render_edge(edge, diagram, theme)
        svg += '    </g>\n\n'

        # Render nodes (top layer)
        svg += '    <!-- Nodes -->\n    <g id="nodes-layer">\n'
        for node in sorted(diagram.nodes, key=lambda n: n.order):
            svg += self._render_node(node, theme)
        svg += '    </g>\n'

        # Close SVG
        svg += '''  </g>
</svg>'''

        return svg

    def _build_styles(self, theme: Theme) -> str:
        """Build CSS styles"""
        return f'''<style>
      .node {{
        fill: {theme.colors.node_fill};
        stroke: {theme.colors.node_stroke};
        stroke-width: {theme.colors.node_stroke_width}px;
      }}
      .node-label {{
        fill: {theme.colors.text_label};
        font-family: {theme.typography.font_family};
        font-size: {theme.typography.font_size_label}px;
        text-anchor: middle;
        dominant-baseline: middle;
      }}
      .edge {{
        stroke: {theme.colors.edge_color};
        stroke-width: {theme.colors.edge_width}px;
        fill: none;
      }}
      .edge-label {{
        fill: {theme.colors.text_secondary};
        font-family: {theme.typography.font_family};
        font-size: {theme.typography.font_size_small}px;
        text-anchor: middle;
      }}
      .cluster {{
        fill: {theme.colors.cluster_fill};
        stroke: {theme.colors.cluster_stroke};
        stroke-width: {theme.colors.cluster_stroke_width}px;
      }}
      .cluster-label {{
        fill: {theme.colors.cluster_label_color};
        font-family: {theme.typography.font_family};
        font-size: {theme.typography.font_size_label}px;
        font-weight: {theme.typography.font_weight_title};
      }}
    </style>'''

    def _build_markers(self, theme: Theme) -> str:
        """Build arrow markers for edges"""
        return f'''
    <!-- Arrow markers -->
    <marker id="arrow-forward" viewBox="0 0 10 10" refX="9" refY="5"
            markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="{theme.colors.edge_arrow_color}"/>
    </marker>
    <marker id="arrow-backward" viewBox="0 0 10 10" refX="1" refY="5"
            markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 10 0 L 0 5 L 10 10 z" fill="{theme.colors.edge_arrow_color}"/>
    </marker>'''

    def _build_filters(self, theme: Theme) -> str:
        """Build SVG filters for effects"""
        return f'''
    <!-- Glow effect -->
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="{theme.colors.glow_blur}" result="blur"/>
      <feFlood flood-color="{theme.colors.glow_color}" flood-opacity="0.5"/>
      <feComposite in2="blur" operator="in"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Shadow effect -->
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="2" dy="2" stdDeviation="{theme.colors.shadow_blur}"
                    flood-color="{theme.colors.shadow_color}"/>
    </filter>'''

    def _render_node(self, node: Node, theme: Theme) -> str:
        """Render a node as SVG"""
        x, y = node.position.x, node.position.y
        w, h = node.size.width, node.size.height
        rx = theme.spacing.node_border_radius

        # Apply custom colors if set
        fill = node.fill_color or theme.colors.node_fill
        stroke = node.stroke_color or theme.colors.node_stroke
        text_color = node.text_color or theme.colors.text_label

        # Build shape based on type
        shape_svg = self._get_shape_svg(node.shape, x, y, w, h, rx, fill, stroke)

        svg = f'''      <g id="{node.id}" class="node-group" data-order="{node.order}" data-type="node">
        {shape_svg}
        <text class="node-label" x="{x + w/2}" y="{y + h/2}" fill="{text_color}">
          {html.escape(node.label)}
        </text>
      </g>
'''
        self._elements.append(SVGElement(
            id=node.id,
            element_type="node",
            svg_content=svg,
            order=node.order,
            metadata={"label": node.label, "description": node.description}
        ))

        return svg

    def _get_shape_svg(
        self,
        shape: NodeShape,
        x: float, y: float,
        w: float, h: float,
        rx: float,
        fill: str, stroke: str
    ) -> str:
        """Generate SVG for different shapes"""
        stroke_width = 2

        if shape == NodeShape.RECTANGLE:
            return f'<rect class="node" x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'

        elif shape == NodeShape.ROUNDED:
            return f'<rect class="node" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'

        elif shape == NodeShape.CIRCLE:
            cx, cy = x + w/2, y + h/2
            r = min(w, h) / 2
            return f'<circle class="node" cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'

        elif shape == NodeShape.DIAMOND:
            cx, cy = x + w/2, y + h/2
            points = f"{cx},{y} {x+w},{cy} {cx},{y+h} {x},{cy}"
            return f'<polygon class="node" points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'

        elif shape == NodeShape.CYLINDER:
            # Database cylinder
            ellipse_h = h * 0.15
            return f'''<ellipse class="node" cx="{x + w/2}" cy="{y + ellipse_h}" rx="{w/2}" ry="{ellipse_h}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>
        <rect class="node" x="{x}" y="{y + ellipse_h}" width="{w}" height="{h - 2*ellipse_h}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>
        <ellipse class="node" cx="{x + w/2}" cy="{y + h - ellipse_h}" rx="{w/2}" ry="{ellipse_h}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'''

        elif shape == NodeShape.HEXAGON:
            indent = w * 0.2
            points = f"{x+indent},{y} {x+w-indent},{y} {x+w},{y+h/2} {x+w-indent},{y+h} {x+indent},{y+h} {x},{y+h/2}"
            return f'<polygon class="node" points="{points}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'

        elif shape == NodeShape.CLOUD:
            # Simplified cloud shape
            return f'<rect class="node" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx*2}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'

        else:
            # Default to rounded rectangle
            return f'<rect class="node" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>'

    def _render_edge(self, edge: Edge, diagram: Diagram, theme: Theme) -> str:
        """Render an edge as SVG"""
        source = diagram.get_node(edge.source)
        target = diagram.get_node(edge.target)

        if not source or not target:
            return ""

        # Get connection points
        src_center = source.center
        tgt_center = target.center

        # Edge color
        color = edge.color or theme.colors.edge_color
        width = edge.width or theme.colors.edge_width

        # Build path
        if edge.control_points:
            # Curved edge
            cp = edge.control_points[0]
            path = f"M {src_center.x},{src_center.y} Q {cp.x},{cp.y} {tgt_center.x},{tgt_center.y}"
        else:
            # Straight edge
            path = f"M {src_center.x},{src_center.y} L {tgt_center.x},{tgt_center.y}"

        # Edge style
        stroke_dasharray = ""
        if edge.style == EdgeStyle.DASHED:
            stroke_dasharray = 'stroke-dasharray="8,4"'
        elif edge.style == EdgeStyle.DOTTED:
            stroke_dasharray = 'stroke-dasharray="2,2"'

        # Arrow markers
        markers = ""
        if edge.direction == EdgeDirection.FORWARD:
            markers = 'marker-end="url(#arrow-forward)"'
        elif edge.direction == EdgeDirection.BACKWARD:
            markers = 'marker-start="url(#arrow-backward)"'
        elif edge.direction == EdgeDirection.BOTH:
            markers = 'marker-start="url(#arrow-backward)" marker-end="url(#arrow-forward)"'

        svg = f'''      <g id="{edge.id}" class="edge-group" data-order="{edge.order}" data-type="edge">
        <path class="edge" d="{path}" stroke="{color}" stroke-width="{width}" {stroke_dasharray} {markers}/>
'''
        # Add label if present
        if edge.label:
            mid_x = (src_center.x + tgt_center.x) / 2
            mid_y = (src_center.y + tgt_center.y) / 2
            svg += f'        <text class="edge-label" x="{mid_x}" y="{mid_y - 10}">{html.escape(edge.label)}</text>\n'

        svg += '      </g>\n'

        self._elements.append(SVGElement(
            id=edge.id,
            element_type="edge",
            svg_content=svg,
            order=edge.order,
            metadata={"label": edge.label, "description": edge.description}
        ))

        return svg

    def _render_cluster(self, cluster: Cluster, theme: Theme) -> str:
        """Render a cluster as SVG"""
        x, y = cluster.position.x, cluster.position.y
        w, h = cluster.size.width, cluster.size.height
        rx = theme.spacing.cluster_border_radius

        fill = cluster.fill_color or theme.colors.cluster_fill
        stroke = cluster.stroke_color or theme.colors.cluster_stroke
        label_color = cluster.label_color or theme.colors.cluster_label_color

        svg = f'''      <g id="{cluster.id}" class="cluster-group" data-order="{cluster.order}" data-type="cluster">
        <rect class="cluster" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>
        <text class="cluster-label" x="{x + 15}" y="{y + 25}" fill="{label_color}">{html.escape(cluster.label)}</text>
      </g>
'''
        self._elements.append(SVGElement(
            id=cluster.id,
            element_type="cluster",
            svg_content=svg,
            order=cluster.order,
            metadata={"label": cluster.label, "description": cluster.description}
        ))

        return svg

    def get_elements(self) -> List[SVGElement]:
        """Get all SVG elements with their metadata"""
        return sorted(self._elements, key=lambda e: e.order)
