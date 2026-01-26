"""
Viralify Diagrams - Professional diagram generation for video content

Fork of mingrammer/diagrams optimized for:
- Video-friendly layouts and readability
- Theme customization (including user-uploaded themes)
- SVG export with animation support
- Narration script generation for voiceover sync
"""

__version__ = "1.0.0"

from viralify_diagrams.core.diagram import Diagram, Cluster, Node, Edge
from viralify_diagrams.core.theme import Theme, ThemeManager
from viralify_diagrams.layouts import GridLayout, HorizontalLayout, VerticalLayout, RadialLayout
from viralify_diagrams.exporters import SVGExporter, PNGFrameExporter, AnimatedSVGExporter
from viralify_diagrams.narration import NarrationScript, DiagramNarrator

__all__ = [
    "Diagram",
    "Cluster",
    "Node",
    "Edge",
    "Theme",
    "ThemeManager",
    "GridLayout",
    "HorizontalLayout",
    "VerticalLayout",
    "RadialLayout",
    "SVGExporter",
    "PNGFrameExporter",
    "AnimatedSVGExporter",
    "NarrationScript",
    "DiagramNarrator",
]
