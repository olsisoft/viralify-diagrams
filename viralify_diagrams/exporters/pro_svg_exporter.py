"""
Professional SVG Exporter

Enhanced SVG export with:
- Drop shadows and glow effects
- Gradient fills
- High-quality anti-aliased rendering
- Icon support
- Professional typography
- Retina (2x, 3x) export
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import html
import math

from viralify_diagrams.core.diagram import (
    Diagram, Node, Edge, Cluster, NodeShape, EdgeStyle, EdgeDirection, Position
)
from viralify_diagrams.core.theme import Theme, get_theme_manager
from viralify_diagrams.icons import get_icon, IconInfo


@dataclass
class RenderConfig:
    """Configuration for professional rendering"""
    # Shadows
    enable_shadows: bool = True
    shadow_blur: float = 8
    shadow_offset_x: float = 2
    shadow_offset_y: float = 4
    shadow_opacity: float = 0.3

    # Gradients
    enable_gradients: bool = True
    gradient_intensity: float = 0.15  # How much lighter/darker

    # Glow effects
    enable_glow: bool = True
    glow_blur: float = 12
    glow_opacity: float = 0.4

    # Icons
    show_icons: bool = True
    icon_size: int = 32

    # Typography
    font_family: str = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    label_font_size: int = 14
    label_font_weight: str = "500"

    # Retina
    scale: int = 1  # 1, 2, or 3 for retina

    # Anti-aliasing
    shape_rendering: str = "geometricPrecision"
    text_rendering: str = "optimizeLegibility"

    # Edges
    edge_smoothness: float = 0.5  # Bezier curve smoothness
    arrow_size: int = 8


class ProSVGExporter:
    """
    Professional-grade SVG exporter.

    Creates high-quality SVG output suitable for:
    - Video content (1080p, 4K)
    - Print materials
    - Marketing assets
    - Documentation
    """

    def __init__(
        self,
        theme: Optional[Theme] = None,
        config: Optional[RenderConfig] = None
    ):
        self.theme = theme
        self.config = config or RenderConfig()
        self._gradient_id = 0

    def export(
        self,
        diagram: Diagram,
        output_path: Optional[str] = None,
        scale: int = 1
    ) -> str:
        """
        Export diagram to professional SVG.

        Args:
            diagram: The diagram to export
            output_path: Optional file path
            scale: Resolution scale (1=normal, 2=retina, 3=super-retina)

        Returns:
            SVG content as string
        """
        self.config.scale = scale
        theme = self.theme or get_theme_manager().get(diagram.theme)
        self._gradient_id = 0

        svg_content = self._build_svg(diagram, theme)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(svg_content)

        return svg_content

    def _build_svg(self, diagram: Diagram, theme: Theme) -> str:
        """Build complete professional SVG document"""
        w = diagram.width * self.config.scale
        h = diagram.height * self.config.scale

        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 {diagram.width} {diagram.height}"
     width="{w}"
     height="{h}"
     shape-rendering="{self.config.shape_rendering}"
     text-rendering="{self.config.text_rendering}"
     id="viralify-diagram-pro">

  <title>{html.escape(diagram.title)}</title>
  <desc>{html.escape(diagram.description)}</desc>

  <defs>
    {self._build_fonts()}
    {self._build_filters(theme)}
    {self._build_markers(theme)}
    {self._build_gradients(theme)}
    {self._build_styles(theme)}
  </defs>

  <!-- Background -->
  {self._build_background(diagram, theme)}

  <!-- Diagram Content -->
  <g id="diagram-content" transform="scale({self.config.scale})">
'''

        # Render in order: clusters -> edges -> nodes
        svg += self._render_clusters(diagram, theme)
        svg += self._render_edges(diagram, theme)
        svg += self._render_nodes(diagram, theme)

        svg += '''  </g>
</svg>'''

        return svg

    def _build_fonts(self) -> str:
        """Build embedded font definitions"""
        return f'''
    <!-- Font import -->
    <style type="text/css">
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;display=swap');
    </style>'''

    def _build_filters(self, theme: Theme) -> str:
        """Build SVG filters for shadows and glows"""
        filters = ""

        if self.config.enable_shadows:
            filters += f'''
    <!-- Drop Shadow -->
    <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
      <feDropShadow dx="{self.config.shadow_offset_x}"
                    dy="{self.config.shadow_offset_y}"
                    stdDeviation="{self.config.shadow_blur}"
                    flood-color="#000000"
                    flood-opacity="{self.config.shadow_opacity}"/>
    </filter>

    <!-- Soft Shadow (for clusters) -->
    <filter id="soft-shadow" x="-50%" y="-50%" width="200%" height="200%">
      <feDropShadow dx="0" dy="2" stdDeviation="6"
                    flood-color="#000000" flood-opacity="0.15"/>
    </filter>'''

        if self.config.enable_glow:
            filters += f'''
    <!-- Glow Effect -->
    <filter id="glow" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="{self.config.glow_blur}" result="blur"/>
      <feFlood flood-color="{theme.colors.highlight_primary}" flood-opacity="{self.config.glow_opacity}"/>
      <feComposite in2="blur" operator="in"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <!-- Node Glow (accent color) -->
    <filter id="node-glow" x="-100%" y="-100%" width="300%" height="300%">
      <feGaussianBlur in="SourceAlpha" stdDeviation="4" result="blur"/>
      <feFlood flood-color="{theme.colors.node_stroke}" flood-opacity="0.6"/>
      <feComposite in2="blur" operator="in"/>
      <feMerge>
        <feMergeNode/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>'''

        return filters

    def _build_markers(self, theme: Theme) -> str:
        """Build professional arrow markers"""
        return f'''
    <!-- Arrow Forward (filled) -->
    <marker id="arrow-forward" viewBox="0 0 10 10" refX="8" refY="5"
            markerWidth="{self.config.arrow_size}" markerHeight="{self.config.arrow_size}"
            orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 L 2 5 Z" fill="{theme.colors.edge_color}"/>
    </marker>

    <!-- Arrow Forward (outline) -->
    <marker id="arrow-forward-outline" viewBox="0 0 10 10" refX="8" refY="5"
            markerWidth="{self.config.arrow_size}" markerHeight="{self.config.arrow_size}"
            orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10" fill="none" stroke="{theme.colors.edge_color}" stroke-width="1.5"/>
    </marker>

    <!-- Arrow Backward -->
    <marker id="arrow-backward" viewBox="0 0 10 10" refX="2" refY="5"
            markerWidth="{self.config.arrow_size}" markerHeight="{self.config.arrow_size}"
            orient="auto">
      <path d="M 10 0 L 0 5 L 10 10 L 8 5 Z" fill="{theme.colors.edge_color}"/>
    </marker>

    <!-- Circle marker -->
    <marker id="circle-marker" viewBox="0 0 10 10" refX="5" refY="5"
            markerWidth="6" markerHeight="6">
      <circle cx="5" cy="5" r="3" fill="{theme.colors.edge_color}"/>
    </marker>'''

    def _build_gradients(self, theme: Theme) -> str:
        """Build gradient definitions"""
        if not self.config.enable_gradients:
            return ""

        # Parse hex color and create lighter/darker versions
        def adjust_color(hex_color: str, factor: float) -> str:
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)

            if factor > 0:  # Lighten
                r = min(255, int(r + (255 - r) * factor))
                g = min(255, int(g + (255 - g) * factor))
                b = min(255, int(b + (255 - b) * factor))
            else:  # Darken
                r = max(0, int(r * (1 + factor)))
                g = max(0, int(g * (1 + factor)))
                b = max(0, int(b * (1 + factor)))

            return f"#{r:02x}{g:02x}{b:02x}"

        intensity = self.config.gradient_intensity
        node_fill = theme.colors.node_fill
        node_light = adjust_color(node_fill, intensity)
        node_dark = adjust_color(node_fill, -intensity)

        return f'''
    <!-- Node gradient -->
    <linearGradient id="node-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:{node_light}"/>
      <stop offset="100%" style="stop-color:{node_dark}"/>
    </linearGradient>

    <!-- Cluster gradient -->
    <linearGradient id="cluster-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:{adjust_color(theme.colors.cluster_fill, 0.1)}"/>
      <stop offset="100%" style="stop-color:{theme.colors.cluster_fill}"/>
    </linearGradient>

    <!-- Highlight gradient -->
    <linearGradient id="highlight-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{theme.colors.highlight_primary}"/>
      <stop offset="100%" style="stop-color:{theme.colors.highlight_secondary}"/>
    </linearGradient>'''

    def _build_styles(self, theme: Theme) -> str:
        """Build CSS styles"""
        shadow_filter = 'filter: url(#shadow);' if self.config.enable_shadows else ''
        gradient_fill = 'url(#node-gradient)' if self.config.enable_gradients else theme.colors.node_fill

        return f'''
    <style>
      .node-shape {{
        fill: {gradient_fill};
        stroke: {theme.colors.node_stroke};
        stroke-width: 2px;
        {shadow_filter}
        transition: all 0.2s ease;
      }}
      .node-shape:hover {{
        filter: url(#node-glow);
      }}
      .node-label {{
        fill: {theme.colors.text_label};
        font-family: {self.config.font_family};
        font-size: {self.config.label_font_size}px;
        font-weight: {self.config.label_font_weight};
        text-anchor: middle;
        dominant-baseline: middle;
        pointer-events: none;
      }}
      .node-sublabel {{
        fill: {theme.colors.text_secondary};
        font-family: {self.config.font_family};
        font-size: {self.config.label_font_size - 2}px;
        font-weight: 400;
        text-anchor: middle;
        dominant-baseline: middle;
        pointer-events: none;
      }}
      .edge-path {{
        fill: none;
        stroke: {theme.colors.edge_color};
        stroke-width: 2px;
        stroke-linecap: round;
        stroke-linejoin: round;
      }}
      .edge-label {{
        fill: {theme.colors.text_secondary};
        font-family: {self.config.font_family};
        font-size: 11px;
        font-weight: 500;
        text-anchor: middle;
        dominant-baseline: middle;
      }}
      .edge-label-bg {{
        fill: {theme.colors.background};
        opacity: 0.9;
      }}
      .cluster-bg {{
        fill: {theme.colors.cluster_fill};
        stroke: {theme.colors.cluster_stroke};
        stroke-width: 2px;
        filter: url(#soft-shadow);
      }}
      .cluster-label {{
        fill: {theme.colors.cluster_label_color};
        font-family: {self.config.font_family};
        font-size: {self.config.label_font_size}px;
        font-weight: 600;
        text-anchor: start;
      }}
    </style>'''

    def _build_background(self, diagram: Diagram, theme: Theme) -> str:
        """Build background with optional gradient"""
        bg_color = theme.colors.background

        if self.config.enable_gradients:
            # Subtle radial gradient for depth
            return f'''
  <defs>
    <radialGradient id="bg-gradient" cx="50%" cy="30%" r="80%">
      <stop offset="0%" style="stop-color:{theme.colors.background_secondary}"/>
      <stop offset="100%" style="stop-color:{bg_color}"/>
    </radialGradient>
  </defs>
  <rect width="100%" height="100%" fill="url(#bg-gradient)"/>'''
        else:
            return f'  <rect width="100%" height="100%" fill="{bg_color}"/>'

    def _render_nodes(self, diagram: Diagram, theme: Theme) -> str:
        """Render all nodes with professional styling"""
        svg = '    <!-- Nodes -->\n    <g id="nodes-layer">\n'

        for node in sorted(diagram.nodes, key=lambda n: n.order):
            svg += self._render_node(node, theme)

        svg += '    </g>\n\n'
        return svg

    def _render_node(self, node: Node, theme: Theme) -> str:
        """Render a single node with icon support"""
        x, y = node.position.x, node.position.y
        w, h = node.size.width, node.size.height
        cx, cy = x + w/2, y + h/2

        # Custom colors or theme
        fill = node.fill_color or (
            "url(#node-gradient)" if self.config.enable_gradients else theme.colors.node_fill
        )
        stroke = node.stroke_color or theme.colors.node_stroke
        text_color = node.text_color or theme.colors.text_label

        # Try to get icon
        icon: Optional[IconInfo] = None
        if node.icon and self.config.show_icons:
            icon = get_icon(node.icon)

        # Build shape
        shape_svg = self._render_node_shape(node.shape, x, y, w, h, fill, stroke, theme)

        # Build icon if available
        icon_svg = ""
        label_y = cy
        if icon:
            icon_size = self.config.icon_size
            icon_x = cx - icon_size / 2
            icon_y = y + 12
            icon_svg = f'''
        <g transform="translate({icon_x}, {icon_y})">
          <g transform="scale({icon_size/64})">
            {icon.svg_content}
          </g>
        </g>'''
            label_y = y + h - 18  # Move label below icon

        # Build label
        label_svg = f'''
        <text class="node-label" x="{cx}" y="{label_y}" fill="{text_color}">
          {html.escape(node.label)}
        </text>'''

        return f'''      <g id="{node.id}" class="node-group" data-order="{node.order}">
        {shape_svg}
        {icon_svg}
        {label_svg}
      </g>
'''

    def _render_node_shape(
        self,
        shape: NodeShape,
        x: float, y: float,
        w: float, h: float,
        fill: str, stroke: str,
        theme: Theme
    ) -> str:
        """Render professional node shapes"""
        rx = theme.spacing.node_border_radius

        if shape == NodeShape.RECTANGLE:
            return f'<rect class="node-shape" x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}"/>'

        elif shape == NodeShape.ROUNDED:
            return f'<rect class="node-shape" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'

        elif shape == NodeShape.CIRCLE:
            cx, cy = x + w/2, y + h/2
            r = min(w, h) / 2
            return f'<circle class="node-shape" cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}"/>'

        elif shape == NodeShape.DIAMOND:
            cx, cy = x + w/2, y + h/2
            points = f"{cx},{y} {x+w},{cy} {cx},{y+h} {x},{cy}"
            return f'<polygon class="node-shape" points="{points}" fill="{fill}" stroke="{stroke}"/>'

        elif shape == NodeShape.CYLINDER:
            # Professional database cylinder
            ellipse_h = h * 0.12
            body_y = y + ellipse_h
            body_h = h - 2 * ellipse_h
            return f'''<g class="node-shape">
          <ellipse cx="{x + w/2}" cy="{y + ellipse_h}" rx="{w/2 - 1}" ry="{ellipse_h}" fill="{fill}" stroke="{stroke}"/>
          <rect x="{x + 1}" y="{body_y}" width="{w - 2}" height="{body_h}" fill="{fill}"/>
          <line x1="{x + 1}" y1="{body_y}" x2="{x + 1}" y2="{y + h - ellipse_h}" stroke="{stroke}" stroke-width="2"/>
          <line x1="{x + w - 1}" y1="{body_y}" x2="{x + w - 1}" y2="{y + h - ellipse_h}" stroke="{stroke}" stroke-width="2"/>
          <ellipse cx="{x + w/2}" cy="{y + h - ellipse_h}" rx="{w/2 - 1}" ry="{ellipse_h}" fill="{fill}" stroke="{stroke}"/>
        </g>'''

        elif shape == NodeShape.HEXAGON:
            indent = w * 0.2
            points = f"{x+indent},{y} {x+w-indent},{y} {x+w},{y+h/2} {x+w-indent},{y+h} {x+indent},{y+h} {x},{y+h/2}"
            return f'<polygon class="node-shape" points="{points}" fill="{fill}" stroke="{stroke}"/>'

        elif shape == NodeShape.CLOUD:
            # Professional cloud shape using bezier curves
            cx, cy = x + w/2, y + h/2
            return f'''<path class="node-shape" d="
              M {x + w*0.25},{y + h*0.7}
              C {x},{y + h*0.7} {x},{y + h*0.35} {x + w*0.2},{y + h*0.3}
              C {x + w*0.15},{y + h*0.1} {x + w*0.35},{y} {x + w*0.5},{y + h*0.15}
              C {x + w*0.65},{y} {x + w*0.85},{y + h*0.1} {x + w*0.8},{y + h*0.3}
              C {x + w},{y + h*0.35} {x + w},{y + h*0.7} {x + w*0.75},{y + h*0.7}
              Z
            " fill="{fill}" stroke="{stroke}"/>'''

        elif shape == NodeShape.PARALLELOGRAM:
            skew = w * 0.15
            points = f"{x+skew},{y} {x+w},{y} {x+w-skew},{y+h} {x},{y+h}"
            return f'<polygon class="node-shape" points="{points}" fill="{fill}" stroke="{stroke}"/>'

        else:
            return f'<rect class="node-shape" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>'

    def _render_edges(self, diagram: Diagram, theme: Theme) -> str:
        """Render all edges with smooth curves"""
        svg = '    <!-- Edges -->\n    <g id="edges-layer">\n'

        for edge in sorted(diagram.edges, key=lambda e: e.order):
            svg += self._render_edge(edge, diagram, theme)

        svg += '    </g>\n\n'
        return svg

    def _render_edge(self, edge: Edge, diagram: Diagram, theme: Theme) -> str:
        """Render a single edge with professional styling"""
        source = diagram.get_node(edge.source)
        target = diagram.get_node(edge.target)

        if not source or not target:
            return ""

        # Get edge points
        src_point = self._get_edge_anchor(source, target)
        tgt_point = self._get_edge_anchor(target, source)

        # Edge color and style
        color = edge.color or theme.colors.edge_color
        width = edge.width or 2

        # Dash pattern
        dash = ""
        if edge.style == EdgeStyle.DASHED:
            dash = 'stroke-dasharray="8,4"'
        elif edge.style == EdgeStyle.DOTTED:
            dash = 'stroke-dasharray="2,4"'

        # Arrow markers
        markers = ""
        if edge.direction == EdgeDirection.FORWARD:
            markers = 'marker-end="url(#arrow-forward)"'
        elif edge.direction == EdgeDirection.BACKWARD:
            markers = 'marker-start="url(#arrow-backward)"'
        elif edge.direction == EdgeDirection.BOTH:
            markers = 'marker-start="url(#arrow-backward)" marker-end="url(#arrow-forward)"'

        # Build path (smooth bezier curve)
        path = self._build_smooth_path(src_point, tgt_point, edge.control_points)

        svg = f'''      <g id="{edge.id}" class="edge-group" data-order="{edge.order}">
        <path class="edge-path" d="{path}" stroke="{color}" stroke-width="{width}" {dash} {markers}/>
'''

        # Add label if present
        if edge.label:
            mid_x = (src_point.x + tgt_point.x) / 2
            mid_y = (src_point.y + tgt_point.y) / 2

            # Background for label
            label_w = len(edge.label) * 7 + 12
            label_h = 18

            svg += f'''        <rect class="edge-label-bg" x="{mid_x - label_w/2}" y="{mid_y - label_h/2}"
              width="{label_w}" height="{label_h}" rx="4"/>
        <text class="edge-label" x="{mid_x}" y="{mid_y}">{html.escape(edge.label)}</text>
'''

        svg += '      </g>\n'
        return svg

    def _get_edge_anchor(self, from_node: Node, to_node: Node) -> Position:
        """Calculate optimal edge anchor point on node boundary"""
        from_center = from_node.center
        to_center = to_node.center

        # Direction vector
        dx = to_center.x - from_center.x
        dy = to_center.y - from_center.y

        # Normalize
        length = math.sqrt(dx*dx + dy*dy)
        if length == 0:
            return from_center

        dx /= length
        dy /= length

        # Find intersection with node boundary
        w, h = from_node.size.width / 2, from_node.size.height / 2

        # For rounded rectangles, use ellipse-like intersection
        if abs(dx) * h > abs(dy) * w:
            # Exits through left/right
            t = w / abs(dx)
        else:
            # Exits through top/bottom
            t = h / abs(dy)

        return Position(
            from_center.x + dx * t,
            from_center.y + dy * t
        )

    def _build_smooth_path(
        self,
        start: Position,
        end: Position,
        control_points: List[Position]
    ) -> str:
        """Build smooth bezier curve path"""
        if control_points:
            # Use provided control points
            cp = control_points[0]
            return f"M {start.x},{start.y} Q {cp.x},{cp.y} {end.x},{end.y}"

        # Auto-generate smooth curve
        dx = end.x - start.x
        dy = end.y - start.y

        # Determine curve direction based on predominant axis
        smoothness = self.config.edge_smoothness

        if abs(dx) > abs(dy):
            # Horizontal dominant - curve vertically
            cp1_x = start.x + dx * smoothness
            cp1_y = start.y
            cp2_x = end.x - dx * smoothness
            cp2_y = end.y
        else:
            # Vertical dominant - curve horizontally
            cp1_x = start.x
            cp1_y = start.y + dy * smoothness
            cp2_x = end.x
            cp2_y = end.y - dy * smoothness

        return f"M {start.x},{start.y} C {cp1_x},{cp1_y} {cp2_x},{cp2_y} {end.x},{end.y}"

    def _render_clusters(self, diagram: Diagram, theme: Theme) -> str:
        """Render all clusters with professional styling"""
        svg = '    <!-- Clusters -->\n    <g id="clusters-layer">\n'

        for cluster in sorted(diagram.clusters, key=lambda c: c.order):
            svg += self._render_cluster(cluster, diagram, theme)

        svg += '    </g>\n\n'
        return svg

    def _render_cluster(self, cluster: Cluster, diagram: Diagram, theme: Theme) -> str:
        """Render a cluster with professional styling"""
        x, y = cluster.position.x, cluster.position.y
        w, h = cluster.size.width, cluster.size.height
        rx = theme.spacing.cluster_border_radius

        fill = cluster.fill_color or theme.colors.cluster_fill
        stroke = cluster.stroke_color or theme.colors.cluster_stroke
        label_color = cluster.label_color or theme.colors.cluster_label_color

        return f'''      <g id="{cluster.id}" class="cluster-group" data-order="{cluster.order}">
        <rect class="cluster-bg" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"
              fill="{fill}" stroke="{stroke}"/>
        <text class="cluster-label" x="{x + 16}" y="{y + 24}" fill="{label_color}">
          {html.escape(cluster.label)}
        </text>
      </g>
'''
