"""
Layout engines for Viralify Diagrams

Available layouts:
- GridLayout: Nodes arranged in a grid
- HorizontalLayout: Left-to-right flow
- VerticalLayout: Top-to-bottom flow
- RadialLayout: Central node with satellites
- GraphvizLayout: Hybrid layout using Graphviz algorithms (recommended for 10+ nodes)

Smart Edge Routing:
- SmartEdgeRouter: Intelligent edge routing with multiple algorithms
- EdgeRoutingMode: Direct, Bezier, Orthogonal, Curved, Bundled
- AnchorPoint: N, S, E, W, NE, NW, SE, SW, CENTER, AUTO

The GraphvizLayout uses PyGraphviz for optimal node positioning with:
- Edge crossing minimization
- Automatic cluster containment
- Multiple algorithms (dot, neato, fdp, sfdp, circo, twopi)
- Scales to 50+ components
"""

from viralify_diagrams.layouts.base import BaseLayout
from viralify_diagrams.layouts.grid import GridLayout
from viralify_diagrams.layouts.horizontal import HorizontalLayout
from viralify_diagrams.layouts.vertical import VerticalLayout
from viralify_diagrams.layouts.radial import RadialLayout
from viralify_diagrams.layouts.graphviz_layout import (
    GraphvizLayout,
    GraphvizAlgorithm,
    auto_layout,
)
from viralify_diagrams.layouts.smart_edges import (
    SmartEdgeRouter,
    EdgeRoutingMode,
    AnchorPoint,
    RoutedEdge,
    EdgeRoutingConfig,
    apply_smart_routing,
)

__all__ = [
    "BaseLayout",
    "GridLayout",
    "HorizontalLayout",
    "VerticalLayout",
    "RadialLayout",
    "GraphvizLayout",
    "GraphvizAlgorithm",
    "auto_layout",
    # Smart Edge Routing
    "SmartEdgeRouter",
    "EdgeRoutingMode",
    "AnchorPoint",
    "RoutedEdge",
    "EdgeRoutingConfig",
    "apply_smart_routing",
]


def get_layout(name: str, **kwargs) -> BaseLayout:
    """
    Get a layout engine by name.

    Args:
        name: Layout name (grid, horizontal, vertical, radial, graphviz, auto)
        **kwargs: Additional arguments for the layout

    Returns:
        Layout instance

    Example:
        >>> layout = get_layout("graphviz", algorithm="dot")
        >>> diagram = layout.layout(diagram)
    """
    layouts = {
        "grid": GridLayout,
        "horizontal": HorizontalLayout,
        "vertical": VerticalLayout,
        "radial": RadialLayout,
        "graphviz": GraphvizLayout,
        # Aliases for graphviz algorithms
        "dot": lambda **kw: GraphvizLayout(algorithm="dot", **kw),
        "neato": lambda **kw: GraphvizLayout(algorithm="neato", **kw),
        "fdp": lambda **kw: GraphvizLayout(algorithm="fdp", **kw),
        "sfdp": lambda **kw: GraphvizLayout(algorithm="sfdp", **kw),
        "circo": lambda **kw: GraphvizLayout(algorithm="circo", **kw),
        "twopi": lambda **kw: GraphvizLayout(algorithm="twopi", **kw),
    }

    if name == "auto":
        # Auto layout requires the diagram, so return a special function
        return GraphvizLayout(**kwargs)

    if name not in layouts:
        available = list(layouts.keys()) + ["auto"]
        raise ValueError(f"Unknown layout: {name}. Available: {available}")

    layout_class = layouts[name]
    if callable(layout_class) and not isinstance(layout_class, type):
        return layout_class(**kwargs)
    return layout_class(**kwargs)
