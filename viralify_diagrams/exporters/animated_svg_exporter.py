"""
Animated SVG Exporter

Exports diagrams as SVG with embedded CSS animations.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from viralify_diagrams.core.diagram import Diagram, Node, Edge, Cluster
from viralify_diagrams.core.theme import Theme, get_theme_manager
from viralify_diagrams.exporters.svg_exporter import SVGExporter


class AnimationType(str, Enum):
    """Types of animations"""
    FADE_IN = "fade_in"
    SCALE_IN = "scale_in"
    SLIDE_LEFT = "slide_left"
    SLIDE_RIGHT = "slide_right"
    SLIDE_UP = "slide_up"
    SLIDE_DOWN = "slide_down"
    DRAW = "draw"  # For edges - draws the path
    PULSE = "pulse"
    GLOW = "glow"


@dataclass
class AnimationConfig:
    """Configuration for animations"""
    duration: float = 0.5  # seconds per element
    delay_between: float = 0.3  # delay between elements
    easing: str = "ease-out"
    stagger: bool = True  # stagger animations by order
    loop: bool = False
    initial_delay: float = 0.5  # delay before first animation


@dataclass
class AnimationTimeline:
    """Timeline entry for an element"""
    element_id: str
    element_type: str  # node, edge, cluster
    start_time: float
    duration: float
    animation_type: AnimationType


class AnimatedSVGExporter(SVGExporter):
    """
    Exports diagrams as SVG with CSS animations.

    Features:
    - Automatic animation sequencing based on element order
    - Multiple animation types (fade, scale, slide, draw)
    - Configurable timing and easing
    - Loop support for continuous animations
    """

    def __init__(
        self,
        theme: Optional[Theme] = None,
        config: Optional[AnimationConfig] = None
    ):
        super().__init__(theme)
        self.config = config or AnimationConfig()
        self._timeline: List[AnimationTimeline] = []

    def export(
        self,
        diagram: Diagram,
        output_path: Optional[str] = None,
        node_animation: AnimationType = AnimationType.FADE_IN,
        edge_animation: AnimationType = AnimationType.DRAW,
        cluster_animation: AnimationType = AnimationType.FADE_IN
    ) -> str:
        """
        Export diagram to animated SVG.

        Args:
            diagram: The diagram to export
            output_path: Optional path to save SVG file
            node_animation: Animation type for nodes
            edge_animation: Animation type for edges
            cluster_animation: Animation type for clusters

        Returns:
            Animated SVG content as string
        """
        # Get theme
        if self.theme:
            theme = self.theme
        else:
            theme = get_theme_manager().get(diagram.theme)

        self._elements = []
        self._timeline = []

        # Build timeline
        self._build_timeline(
            diagram,
            node_animation,
            edge_animation,
            cluster_animation
        )

        # Build animated SVG
        svg_content = self._build_animated_svg(
            diagram,
            theme,
            node_animation,
            edge_animation,
            cluster_animation
        )

        # Save to file if path provided
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(svg_content)

        return svg_content

    def _build_timeline(
        self,
        diagram: Diagram,
        node_animation: AnimationType,
        edge_animation: AnimationType,
        cluster_animation: AnimationType
    ) -> None:
        """Build animation timeline based on element order"""
        current_time = self.config.initial_delay

        # Clusters first (background)
        for cluster in sorted(diagram.clusters, key=lambda c: c.order):
            self._timeline.append(AnimationTimeline(
                element_id=cluster.id,
                element_type="cluster",
                start_time=current_time,
                duration=self.config.duration,
                animation_type=cluster_animation
            ))
            if self.config.stagger:
                current_time += self.config.delay_between

        # Nodes next
        for node in sorted(diagram.nodes, key=lambda n: n.order):
            self._timeline.append(AnimationTimeline(
                element_id=node.id,
                element_type="node",
                start_time=current_time,
                duration=self.config.duration,
                animation_type=node_animation
            ))
            if self.config.stagger:
                current_time += self.config.delay_between

        # Edges last
        for edge in sorted(diagram.edges, key=lambda e: e.order):
            self._timeline.append(AnimationTimeline(
                element_id=edge.id,
                element_type="edge",
                start_time=current_time,
                duration=self.config.duration,
                animation_type=edge_animation
            ))
            if self.config.stagger:
                current_time += self.config.delay_between

    def _build_animated_svg(
        self,
        diagram: Diagram,
        theme: Theme,
        node_animation: AnimationType,
        edge_animation: AnimationType,
        cluster_animation: AnimationType
    ) -> str:
        """Build complete animated SVG document"""
        import html

        # Calculate total animation duration
        total_duration = 0
        if self._timeline:
            last = self._timeline[-1]
            total_duration = last.start_time + last.duration

        # SVG header
        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 {diagram.width} {diagram.height}"
     width="{diagram.width}"
     height="{diagram.height}"
     id="viralify-diagram-animated">
  <title>{html.escape(diagram.title)}</title>
  <desc>{html.escape(diagram.description)}</desc>

  <!-- Styles and Animations -->
  <defs>
    {self._build_styles(theme)}
    {self._build_markers(theme)}
    {self._build_filters(theme)}
  </defs>

  <style>
    {self._build_animation_css(node_animation, edge_animation, cluster_animation)}
  </style>

  <!-- Background -->
  <rect width="100%" height="100%" fill="{theme.colors.background}" />

  <!-- Diagram Content -->
  <g id="diagram-content">
'''
        # Render clusters (background layer)
        svg += '    <!-- Clusters -->\n    <g id="clusters-layer">\n'
        for cluster in sorted(diagram.clusters, key=lambda c: c.order):
            svg += self._render_animated_cluster(cluster, theme, cluster_animation)
        svg += '    </g>\n\n'

        # Render edges (middle layer)
        svg += '    <!-- Edges -->\n    <g id="edges-layer">\n'
        for edge in sorted(diagram.edges, key=lambda e: e.order):
            svg += self._render_animated_edge(edge, diagram, theme, edge_animation)
        svg += '    </g>\n\n'

        # Render nodes (top layer)
        svg += '    <!-- Nodes -->\n    <g id="nodes-layer">\n'
        for node in sorted(diagram.nodes, key=lambda n: n.order):
            svg += self._render_animated_node(node, theme, node_animation)
        svg += '    </g>\n'

        # Close SVG
        svg += '''  </g>
</svg>'''

        return svg

    def _build_animation_css(
        self,
        node_animation: AnimationType,
        edge_animation: AnimationType,
        cluster_animation: AnimationType
    ) -> str:
        """Build CSS animation keyframes and classes"""
        css = """
    /* Base animation states */
    .node-group, .edge-group, .cluster-group {
      opacity: 0;
    }

    /* Keyframes */
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }

    @keyframes scaleIn {
      from {
        opacity: 0;
        transform: scale(0);
      }
      to {
        opacity: 1;
        transform: scale(1);
      }
    }

    @keyframes slideLeft {
      from {
        opacity: 0;
        transform: translateX(-50px);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }

    @keyframes slideRight {
      from {
        opacity: 0;
        transform: translateX(50px);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }

    @keyframes slideUp {
      from {
        opacity: 0;
        transform: translateY(50px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @keyframes slideDown {
      from {
        opacity: 0;
        transform: translateY(-50px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @keyframes drawPath {
      from {
        stroke-dashoffset: 1000;
        opacity: 1;
      }
      to {
        stroke-dashoffset: 0;
        opacity: 1;
      }
    }

    @keyframes pulse {
      0%, 100% {
        opacity: 1;
        transform: scale(1);
      }
      50% {
        opacity: 0.8;
        transform: scale(1.05);
      }
    }

    @keyframes glow {
      0%, 100% {
        filter: none;
      }
      50% {
        filter: url(#glow);
      }
    }
"""
        # Add element-specific animation classes
        for entry in self._timeline:
            animation_name = self._get_animation_name(entry.animation_type)
            iteration = "infinite" if self.config.loop else "1"
            fill_mode = "forwards"

            # Special handling for draw animation
            if entry.animation_type == AnimationType.DRAW:
                css += f"""
    #{entry.element_id} {{
      animation: {animation_name} {entry.duration}s {self.config.easing} {entry.start_time}s {iteration} {fill_mode};
    }}
    #{entry.element_id} .edge {{
      stroke-dasharray: 1000;
      stroke-dashoffset: 1000;
    }}
"""
            else:
                css += f"""
    #{entry.element_id} {{
      animation: {animation_name} {entry.duration}s {self.config.easing} {entry.start_time}s {iteration} {fill_mode};
    }}
"""

        return css

    def _get_animation_name(self, animation_type: AnimationType) -> str:
        """Map animation type to CSS keyframe name"""
        mapping = {
            AnimationType.FADE_IN: "fadeIn",
            AnimationType.SCALE_IN: "scaleIn",
            AnimationType.SLIDE_LEFT: "slideLeft",
            AnimationType.SLIDE_RIGHT: "slideRight",
            AnimationType.SLIDE_UP: "slideUp",
            AnimationType.SLIDE_DOWN: "slideDown",
            AnimationType.DRAW: "drawPath",
            AnimationType.PULSE: "pulse",
            AnimationType.GLOW: "glow",
        }
        return mapping.get(animation_type, "fadeIn")

    def _render_animated_node(
        self,
        node: Node,
        theme: Theme,
        animation: AnimationType
    ) -> str:
        """Render a node with animation attributes"""
        import html

        x, y = node.position.x, node.position.y
        w, h = node.size.width, node.size.height
        rx = theme.spacing.node_border_radius

        fill = node.fill_color or theme.colors.node_fill
        stroke = node.stroke_color or theme.colors.node_stroke
        text_color = node.text_color or theme.colors.text_label

        shape_svg = self._get_shape_svg(node.shape, x, y, w, h, rx, fill, stroke)

        # Add transform-origin for scale animations
        transform_origin = f"transform-origin: {x + w/2}px {y + h/2}px;"

        svg = f'''      <g id="{node.id}" class="node-group" data-order="{node.order}" data-type="node" style="{transform_origin}">
        {shape_svg}
        <text class="node-label" x="{x + w/2}" y="{y + h/2}" fill="{text_color}">
          {html.escape(node.label)}
        </text>
      </g>
'''
        return svg

    def _render_animated_edge(
        self,
        edge: Edge,
        diagram: Diagram,
        theme: Theme,
        animation: AnimationType
    ) -> str:
        """Render an edge with animation attributes"""
        # Use parent class render but add animation class
        svg = self._render_edge(edge, diagram, theme)
        return svg

    def _render_animated_cluster(
        self,
        cluster: Cluster,
        theme: Theme,
        animation: AnimationType
    ) -> str:
        """Render a cluster with animation attributes"""
        import html

        x, y = cluster.position.x, cluster.position.y
        w, h = cluster.size.width, cluster.size.height
        rx = theme.spacing.cluster_border_radius

        fill = cluster.fill_color or theme.colors.cluster_fill
        stroke = cluster.stroke_color or theme.colors.cluster_stroke
        label_color = cluster.label_color or theme.colors.cluster_label_color

        transform_origin = f"transform-origin: {x + w/2}px {y + h/2}px;"

        svg = f'''      <g id="{cluster.id}" class="cluster-group" data-order="{cluster.order}" data-type="cluster" style="{transform_origin}">
        <rect class="cluster" x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}"/>
        <text class="cluster-label" x="{x + 15}" y="{y + 25}" fill="{label_color}">{html.escape(cluster.label)}</text>
      </g>
'''
        return svg

    def get_timeline(self) -> List[AnimationTimeline]:
        """Get the animation timeline"""
        return self._timeline

    def get_total_duration(self) -> float:
        """Get total animation duration in seconds"""
        if not self._timeline:
            return 0
        last = self._timeline[-1]
        return last.start_time + last.duration

    def export_timing_script(self) -> Dict[str, Any]:
        """
        Export timing script for external animation control.

        Returns a dict with:
        - total_duration: Total animation time
        - elements: List of elements with timing info
        """
        elements = []
        for entry in self._timeline:
            elements.append({
                "id": entry.element_id,
                "type": entry.element_type,
                "start": entry.start_time,
                "duration": entry.duration,
                "animation": entry.animation_type.value
            })

        return {
            "total_duration": self.get_total_duration(),
            "config": {
                "duration_per_element": self.config.duration,
                "delay_between": self.config.delay_between,
                "easing": self.config.easing,
                "loop": self.config.loop
            },
            "elements": elements
        }
