"""
Viralify Diagrams - Professional diagram generation for video content

Fork of mingrammer/diagrams optimized for:
- Video-friendly layouts and readability
- Theme customization (including user-uploaded themes)
- SVG export with animation support
- Narration script generation for voiceover sync
- Hybrid layout using Graphviz for 50+ component diagrams
- Professional icons for AWS, GCP, Azure, Kubernetes
- Smart edge routing with bezier and orthogonal paths
- Cloud provider themes matching official design guidelines
- Enterprise edge management (100+ connections)
"""

__version__ = "2.1.0"

from viralify_diagrams.core.diagram import Diagram, Cluster, Node, Edge
from viralify_diagrams.core.theme import Theme, ThemeManager, get_theme_manager
from viralify_diagrams.layouts import (
    GridLayout,
    HorizontalLayout,
    VerticalLayout,
    RadialLayout,
    GraphvizLayout,
    GraphvizAlgorithm,
    auto_layout,
    get_layout,
    # Smart edge routing
    SmartEdgeRouter,
    EdgeRoutingMode,
    AnchorPoint,
    apply_smart_routing,
    # Edge bundling
    EdgeBundler,
    BundlingAlgorithm,
    BundleConfig,
    apply_edge_bundling,
    # Edge aggregation
    EdgeAggregator,
    AggregationMode,
    AggregationConfig,
    aggregate_edges,
    # Edge styling
    EdgeStyler,
    ImportanceMetric,
    ColorScheme,
    StyleConfig,
    style_edges,
    # Channel routing
    ChannelRouter,
    ChannelConfig,
    apply_channel_routing,
)
from viralify_diagrams.exporters import (
    SVGExporter,
    PNGFrameExporter,
    AnimatedSVGExporter,
    ProSVGExporter,
    RenderConfig,
)
from viralify_diagrams.narration import NarrationScript, DiagramNarrator

# Professional icons
from viralify_diagrams.icons import (
    IconRegistry,
    get_icon_registry,
    get_icon,
    list_icons,
    list_categories,
    IconInfo,
    IconCategory,
    IconProvider,
    CATEGORY_COLORS,
)

# Professional themes
from viralify_diagrams.themes import (
    ProfessionalTheme,
    AWSTheme,
    GCPTheme,
    AzureTheme,
    CorporateTheme,
    get_professional_theme,
    list_professional_themes,
)

__all__ = [
    # Core
    "Diagram",
    "Cluster",
    "Node",
    "Edge",
    # Themes
    "Theme",
    "ThemeManager",
    "get_theme_manager",
    # Professional Themes
    "ProfessionalTheme",
    "AWSTheme",
    "GCPTheme",
    "AzureTheme",
    "CorporateTheme",
    "get_professional_theme",
    "list_professional_themes",
    # Layouts
    "GridLayout",
    "HorizontalLayout",
    "VerticalLayout",
    "RadialLayout",
    "GraphvizLayout",
    "GraphvizAlgorithm",
    "auto_layout",
    "get_layout",
    # Smart Edge Routing
    "SmartEdgeRouter",
    "EdgeRoutingMode",
    "AnchorPoint",
    "apply_smart_routing",
    # Edge Bundling (Enterprise)
    "EdgeBundler",
    "BundlingAlgorithm",
    "BundleConfig",
    "apply_edge_bundling",
    # Edge Aggregation (Enterprise)
    "EdgeAggregator",
    "AggregationMode",
    "AggregationConfig",
    "aggregate_edges",
    # Edge Styling (Enterprise)
    "EdgeStyler",
    "ImportanceMetric",
    "ColorScheme",
    "StyleConfig",
    "style_edges",
    # Channel Routing (Enterprise)
    "ChannelRouter",
    "ChannelConfig",
    "apply_channel_routing",
    # Exporters
    "SVGExporter",
    "PNGFrameExporter",
    "AnimatedSVGExporter",
    "ProSVGExporter",
    "RenderConfig",
    # Icons
    "IconRegistry",
    "get_icon_registry",
    "get_icon",
    "list_icons",
    "list_categories",
    "IconInfo",
    "IconCategory",
    "IconProvider",
    "CATEGORY_COLORS",
    # Narration
    "NarrationScript",
    "DiagramNarrator",
]
