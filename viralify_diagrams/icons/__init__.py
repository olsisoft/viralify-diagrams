"""
Viralify Diagrams - Professional Icon System

Supports:
- AWS Architecture Icons (200+)
- Google Cloud Platform Icons (150+)
- Microsoft Azure Icons (180+)
- Kubernetes/CNCF Icons (50+)
- Generic Technology Icons (100+)

Usage:
    from viralify_diagrams.icons import get_icon, IconCategory

    # Get an icon by path
    icon = get_icon("aws/compute/ec2")

    # Use in a node
    node = Node(label="Web Server", icon="aws/compute/ec2")
"""

from viralify_diagrams.icons.registry import (
    IconRegistry,
    get_icon_registry,
    get_icon,
    list_icons,
    list_categories,
    IconInfo,
)

from viralify_diagrams.icons.categories import (
    IconCategory,
    IconProvider,
    CATEGORY_COLORS,
)

__all__ = [
    "IconRegistry",
    "get_icon_registry",
    "get_icon",
    "list_icons",
    "list_categories",
    "IconInfo",
    "IconCategory",
    "IconProvider",
    "CATEGORY_COLORS",
]
