"""
Layout engines for Viralify Diagrams

Available layouts:
- GridLayout: Nodes arranged in a grid
- HorizontalLayout: Left-to-right flow
- VerticalLayout: Top-to-bottom flow
- RadialLayout: Central node with satellites
"""

from viralify_diagrams.layouts.base import BaseLayout
from viralify_diagrams.layouts.grid import GridLayout
from viralify_diagrams.layouts.horizontal import HorizontalLayout
from viralify_diagrams.layouts.vertical import VerticalLayout
from viralify_diagrams.layouts.radial import RadialLayout

__all__ = [
    "BaseLayout",
    "GridLayout",
    "HorizontalLayout",
    "VerticalLayout",
    "RadialLayout",
]


def get_layout(name: str) -> BaseLayout:
    """Get a layout engine by name"""
    layouts = {
        "grid": GridLayout,
        "horizontal": HorizontalLayout,
        "vertical": VerticalLayout,
        "radial": RadialLayout,
    }

    if name not in layouts:
        raise ValueError(f"Unknown layout: {name}. Available: {list(layouts.keys())}")

    return layouts[name]()
