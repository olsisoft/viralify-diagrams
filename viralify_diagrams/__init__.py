"""
Viralify Diagrams - Professional diagram generation for video content

Fork of mingrammer/diagrams optimized for:
- Video-friendly layouts and readability
- Theme customization (including user-uploaded themes)
- SVG export with animation support
- Narration script generation for voiceover sync
- Hybrid layout using Graphviz for 50+ component diagrams
"""

__version__ = "1.1.0"

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
)
from viralify_diagrams.exporters import SVGExporter, PNGFrameExporter, AnimatedSVGExporter
from viralify_diagrams.narration import NarrationScript, DiagramNarrator

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
    # Layouts
    "GridLayout",
    "HorizontalLayout",
    "VerticalLayout",
    "RadialLayout",
    "GraphvizLayout",
    "GraphvizAlgorithm",
    "auto_layout",
    "get_layout",
    # Exporters
    "SVGExporter",
    "PNGFrameExporter",
    "AnimatedSVGExporter",
    # Narration
    "NarrationScript",
    "DiagramNarrator",
]
