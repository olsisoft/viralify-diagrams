"""
Professional Cloud Provider Themes

Themes based on official design guidelines:
- AWS: Amazon Web Services Architecture Icons guidelines
- GCP: Google Cloud Platform Material Design
- Azure: Microsoft Fluent Design System
- Corporate: Clean enterprise style
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum

from viralify_diagrams.core.theme import Theme


class ThemeVariant(str, Enum):
    """Theme color variants"""
    LIGHT = "light"
    DARK = "dark"


@dataclass
class GradientConfig:
    """Configuration for gradient fills"""
    enabled: bool = True
    direction: str = "vertical"  # vertical, horizontal, diagonal, radial
    color_stops: List[tuple] = field(default_factory=list)  # [(offset, color), ...]


@dataclass
class ShadowConfig:
    """Configuration for drop shadows"""
    enabled: bool = True
    offset_x: float = 2.0
    offset_y: float = 4.0
    blur: float = 8.0
    color: str = "rgba(0,0,0,0.15)"


@dataclass
class TypographyConfig:
    """Typography settings"""
    font_family: str = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    node_label_size: int = 13
    node_label_weight: str = "500"
    edge_label_size: int = 11
    edge_label_weight: str = "400"
    title_size: int = 24
    title_weight: str = "600"


@dataclass
class NodeStyleConfig:
    """Node styling configuration"""
    border_radius: int = 8
    border_width: float = 1.5
    min_width: int = 120
    min_height: int = 60
    padding: int = 16
    icon_size: int = 32
    icon_position: str = "top"  # top, left, center


@dataclass
class EdgeStyleConfig:
    """Edge styling configuration"""
    stroke_width: float = 2.0
    arrow_size: int = 8
    curve_type: str = "bezier"  # bezier, orthogonal, straight
    dash_pattern: Optional[str] = None


@dataclass
class ProfessionalTheme:
    """
    Professional theme with comprehensive styling options.

    Extends the base Theme with additional professional features:
    - Gradient support
    - Shadow configurations
    - Typography settings
    - Node and edge style configs
    """
    name: str
    variant: ThemeVariant

    # Core colors
    background: str
    foreground: str
    primary: str
    secondary: str
    accent: str

    # Node colors
    node_fill: str
    node_stroke: str
    node_text: str

    # Edge colors
    edge_stroke: str
    edge_label_color: str

    # Cluster colors
    cluster_fill: str
    cluster_stroke: str
    cluster_text: str

    # Category color palette
    category_colors: Dict[str, Dict[str, str]] = field(default_factory=dict)

    # Professional features
    gradient: GradientConfig = field(default_factory=GradientConfig)
    shadow: ShadowConfig = field(default_factory=ShadowConfig)
    typography: TypographyConfig = field(default_factory=TypographyConfig)
    node_style: NodeStyleConfig = field(default_factory=NodeStyleConfig)
    edge_style: EdgeStyleConfig = field(default_factory=EdgeStyleConfig)

    # Icon settings
    show_icons: bool = True
    icon_style: str = "colored"  # colored, monochrome, outlined

    def to_base_theme(self) -> Theme:
        """Convert to base Theme for compatibility"""
        return Theme(
            name=self.name,
            background=self.background,
            foreground=self.foreground,
            primary=self.primary,
            secondary=self.secondary,
            accent=self.accent,
            node_fill=self.node_fill,
            node_stroke=self.node_stroke,
            node_text=self.node_text,
            edge_stroke=self.edge_stroke,
            cluster_fill=self.cluster_fill,
            cluster_stroke=self.cluster_stroke,
        )

    def get_category_color(self, category: str, element: str = "fill") -> str:
        """Get color for a specific category"""
        if category in self.category_colors:
            return self.category_colors[category].get(element, self.node_fill)
        return self.node_fill


# =============================================================================
# AWS Theme - Based on AWS Architecture Icons Guidelines
# =============================================================================

AWS_CATEGORY_COLORS = {
    # Compute - Orange
    "compute": {"fill": "#FF9900", "stroke": "#CC7A00", "text": "#FFFFFF"},
    "container": {"fill": "#FF9900", "stroke": "#CC7A00", "text": "#FFFFFF"},
    "serverless": {"fill": "#FF9900", "stroke": "#CC7A00", "text": "#FFFFFF"},

    # Storage - Green
    "storage": {"fill": "#3F8624", "stroke": "#2D6119", "text": "#FFFFFF"},
    "database": {"fill": "#3B48CC", "stroke": "#2D3899", "text": "#FFFFFF"},

    # Network - Purple
    "network": {"fill": "#8C4FFF", "stroke": "#6B3DCC", "text": "#FFFFFF"},
    "cdn": {"fill": "#8C4FFF", "stroke": "#6B3DCC", "text": "#FFFFFF"},
    "load_balancer": {"fill": "#8C4FFF", "stroke": "#6B3DCC", "text": "#FFFFFF"},

    # Security - Red
    "security": {"fill": "#DD344C", "stroke": "#B32A3D", "text": "#FFFFFF"},
    "iam": {"fill": "#DD344C", "stroke": "#B32A3D", "text": "#FFFFFF"},

    # Integration - Pink
    "integration": {"fill": "#E7157B", "stroke": "#B81163", "text": "#FFFFFF"},
    "messaging": {"fill": "#E7157B", "stroke": "#B81163", "text": "#FFFFFF"},
    "queue": {"fill": "#E7157B", "stroke": "#B81163", "text": "#FFFFFF"},

    # Analytics - Blue
    "analytics": {"fill": "#01A88D", "stroke": "#018672", "text": "#FFFFFF"},
    "ml": {"fill": "#01A88D", "stroke": "#018672", "text": "#FFFFFF"},

    # Management - Coral
    "monitoring": {"fill": "#E7157B", "stroke": "#B81163", "text": "#FFFFFF"},
    "devops": {"fill": "#E7157B", "stroke": "#B81163", "text": "#FFFFFF"},

    # General
    "client": {"fill": "#545B64", "stroke": "#3D4248", "text": "#FFFFFF"},
    "user": {"fill": "#545B64", "stroke": "#3D4248", "text": "#FFFFFF"},
}

AWSTheme = ProfessionalTheme(
    name="aws",
    variant=ThemeVariant.LIGHT,

    # AWS brand colors
    background="#FFFFFF",
    foreground="#232F3E",
    primary="#FF9900",
    secondary="#232F3E",
    accent="#146EB4",

    # Node styling
    node_fill="#FFFFFF",
    node_stroke="#545B64",
    node_text="#232F3E",

    # Edge styling
    edge_stroke="#545B64",
    edge_label_color="#545B64",

    # Cluster styling
    cluster_fill="#F2F3F3",
    cluster_stroke="#879196",
    cluster_text="#232F3E",

    # Category colors
    category_colors=AWS_CATEGORY_COLORS,

    # Professional features
    gradient=GradientConfig(
        enabled=True,
        direction="vertical",
        color_stops=[(0, "#FFFFFF"), (100, "#F7F8F8")]
    ),
    shadow=ShadowConfig(
        enabled=True,
        offset_x=0,
        offset_y=2,
        blur=8,
        color="rgba(35,47,62,0.12)"
    ),
    typography=TypographyConfig(
        font_family="'Amazon Ember', 'Helvetica Neue', Helvetica, Arial, sans-serif",
        node_label_size=12,
        node_label_weight="500",
        edge_label_size=10,
        edge_label_weight="400",
        title_size=20,
        title_weight="700"
    ),
    node_style=NodeStyleConfig(
        border_radius=4,
        border_width=1,
        min_width=100,
        min_height=64,
        padding=12,
        icon_size=48,
        icon_position="top"
    ),
    edge_style=EdgeStyleConfig(
        stroke_width=1.5,
        arrow_size=8,
        curve_type="orthogonal",
        dash_pattern=None
    ),

    show_icons=True,
    icon_style="colored"
)


# =============================================================================
# GCP Theme - Based on Google Cloud Material Design
# =============================================================================

GCP_CATEGORY_COLORS = {
    # Compute - Blue
    "compute": {"fill": "#4285F4", "stroke": "#3367D6", "text": "#FFFFFF"},
    "container": {"fill": "#4285F4", "stroke": "#3367D6", "text": "#FFFFFF"},
    "serverless": {"fill": "#4285F4", "stroke": "#3367D6", "text": "#FFFFFF"},

    # Storage - Green
    "storage": {"fill": "#34A853", "stroke": "#2D9249", "text": "#FFFFFF"},
    "database": {"fill": "#34A853", "stroke": "#2D9249", "text": "#FFFFFF"},

    # Network - Yellow/Orange
    "network": {"fill": "#FBBC04", "stroke": "#E5A800", "text": "#202124"},
    "cdn": {"fill": "#FBBC04", "stroke": "#E5A800", "text": "#202124"},
    "load_balancer": {"fill": "#FBBC04", "stroke": "#E5A800", "text": "#202124"},

    # Security - Red
    "security": {"fill": "#EA4335", "stroke": "#D33426", "text": "#FFFFFF"},
    "iam": {"fill": "#EA4335", "stroke": "#D33426", "text": "#FFFFFF"},

    # Integration - Purple
    "integration": {"fill": "#9334E6", "stroke": "#7B2CBF", "text": "#FFFFFF"},
    "messaging": {"fill": "#9334E6", "stroke": "#7B2CBF", "text": "#FFFFFF"},
    "queue": {"fill": "#9334E6", "stroke": "#7B2CBF", "text": "#FFFFFF"},

    # Analytics - Cyan
    "analytics": {"fill": "#00BCD4", "stroke": "#00A0B4", "text": "#FFFFFF"},
    "ml": {"fill": "#FF6F00", "stroke": "#E56300", "text": "#FFFFFF"},

    # Management
    "monitoring": {"fill": "#607D8B", "stroke": "#546E7A", "text": "#FFFFFF"},
    "devops": {"fill": "#607D8B", "stroke": "#546E7A", "text": "#FFFFFF"},

    # General
    "client": {"fill": "#5F6368", "stroke": "#4A4E51", "text": "#FFFFFF"},
    "user": {"fill": "#5F6368", "stroke": "#4A4E51", "text": "#FFFFFF"},
}

GCPTheme = ProfessionalTheme(
    name="gcp",
    variant=ThemeVariant.LIGHT,

    # GCP brand colors
    background="#FFFFFF",
    foreground="#202124",
    primary="#4285F4",
    secondary="#5F6368",
    accent="#34A853",

    # Node styling
    node_fill="#FFFFFF",
    node_stroke="#DADCE0",
    node_text="#202124",

    # Edge styling
    edge_stroke="#5F6368",
    edge_label_color="#5F6368",

    # Cluster styling
    cluster_fill="#F8F9FA",
    cluster_stroke="#DADCE0",
    cluster_text="#202124",

    # Category colors
    category_colors=GCP_CATEGORY_COLORS,

    # Professional features
    gradient=GradientConfig(
        enabled=False,  # GCP uses flat colors
        direction="vertical",
        color_stops=[]
    ),
    shadow=ShadowConfig(
        enabled=True,
        offset_x=0,
        offset_y=1,
        blur=3,
        color="rgba(60,64,67,0.15)"
    ),
    typography=TypographyConfig(
        font_family="'Google Sans', 'Roboto', 'Noto Sans', sans-serif",
        node_label_size=14,
        node_label_weight="500",
        edge_label_size=12,
        edge_label_weight="400",
        title_size=22,
        title_weight="500"
    ),
    node_style=NodeStyleConfig(
        border_radius=8,
        border_width=1,
        min_width=120,
        min_height=56,
        padding=16,
        icon_size=40,
        icon_position="left"
    ),
    edge_style=EdgeStyleConfig(
        stroke_width=2,
        arrow_size=8,
        curve_type="bezier",
        dash_pattern=None
    ),

    show_icons=True,
    icon_style="colored"
)


# =============================================================================
# Azure Theme - Based on Microsoft Fluent Design System
# =============================================================================

AZURE_CATEGORY_COLORS = {
    # Compute - Light Blue
    "compute": {"fill": "#0078D4", "stroke": "#106EBE", "text": "#FFFFFF"},
    "container": {"fill": "#0078D4", "stroke": "#106EBE", "text": "#FFFFFF"},
    "serverless": {"fill": "#0078D4", "stroke": "#106EBE", "text": "#FFFFFF"},

    # Storage - Blue Gray
    "storage": {"fill": "#50E6FF", "stroke": "#00B7C3", "text": "#000000"},
    "database": {"fill": "#0078D4", "stroke": "#106EBE", "text": "#FFFFFF"},

    # Network - Teal
    "network": {"fill": "#008575", "stroke": "#006F60", "text": "#FFFFFF"},
    "cdn": {"fill": "#008575", "stroke": "#006F60", "text": "#FFFFFF"},
    "load_balancer": {"fill": "#008575", "stroke": "#006F60", "text": "#FFFFFF"},

    # Security - Yellow
    "security": {"fill": "#FFB900", "stroke": "#E6A700", "text": "#000000"},
    "iam": {"fill": "#FFB900", "stroke": "#E6A700", "text": "#000000"},

    # Integration - Purple
    "integration": {"fill": "#8764B8", "stroke": "#744DA9", "text": "#FFFFFF"},
    "messaging": {"fill": "#8764B8", "stroke": "#744DA9", "text": "#FFFFFF"},
    "queue": {"fill": "#8764B8", "stroke": "#744DA9", "text": "#FFFFFF"},

    # Analytics - Green
    "analytics": {"fill": "#00B294", "stroke": "#009980", "text": "#FFFFFF"},
    "ml": {"fill": "#00B294", "stroke": "#009980", "text": "#FFFFFF"},

    # Management - Gray
    "monitoring": {"fill": "#69797E", "stroke": "#566268", "text": "#FFFFFF"},
    "devops": {"fill": "#0078D4", "stroke": "#106EBE", "text": "#FFFFFF"},

    # General
    "client": {"fill": "#737373", "stroke": "#5C5C5C", "text": "#FFFFFF"},
    "user": {"fill": "#737373", "stroke": "#5C5C5C", "text": "#FFFFFF"},
}

AzureTheme = ProfessionalTheme(
    name="azure",
    variant=ThemeVariant.LIGHT,

    # Azure brand colors
    background="#FFFFFF",
    foreground="#323130",
    primary="#0078D4",
    secondary="#106EBE",
    accent="#00BCF2",

    # Node styling
    node_fill="#FFFFFF",
    node_stroke="#E1DFDD",
    node_text="#323130",

    # Edge styling
    edge_stroke="#605E5C",
    edge_label_color="#605E5C",

    # Cluster styling
    cluster_fill="#FAF9F8",
    cluster_stroke="#E1DFDD",
    cluster_text="#323130",

    # Category colors
    category_colors=AZURE_CATEGORY_COLORS,

    # Professional features - Fluent Design
    gradient=GradientConfig(
        enabled=True,
        direction="vertical",
        color_stops=[(0, "#FFFFFF"), (100, "#F3F2F1")]
    ),
    shadow=ShadowConfig(
        enabled=True,
        offset_x=0,
        offset_y=1.6,
        blur=3.6,
        color="rgba(0,0,0,0.132)"
    ),
    typography=TypographyConfig(
        font_family="'Segoe UI', 'Segoe UI Web', -apple-system, BlinkMacSystemFont, sans-serif",
        node_label_size=14,
        node_label_weight="600",
        edge_label_size=12,
        edge_label_weight="400",
        title_size=20,
        title_weight="600"
    ),
    node_style=NodeStyleConfig(
        border_radius=4,
        border_width=1,
        min_width=112,
        min_height=60,
        padding=12,
        icon_size=32,
        icon_position="left"
    ),
    edge_style=EdgeStyleConfig(
        stroke_width=1.5,
        arrow_size=7,
        curve_type="bezier",
        dash_pattern=None
    ),

    show_icons=True,
    icon_style="colored"
)


# =============================================================================
# Corporate Theme - Clean Enterprise Style
# =============================================================================

CORPORATE_CATEGORY_COLORS = {
    # Compute - Navy
    "compute": {"fill": "#1A365D", "stroke": "#0F2240", "text": "#FFFFFF"},
    "container": {"fill": "#1A365D", "stroke": "#0F2240", "text": "#FFFFFF"},
    "serverless": {"fill": "#2C5282", "stroke": "#1A365D", "text": "#FFFFFF"},

    # Storage - Steel Blue
    "storage": {"fill": "#2B6CB0", "stroke": "#1A4971", "text": "#FFFFFF"},
    "database": {"fill": "#2B6CB0", "stroke": "#1A4971", "text": "#FFFFFF"},

    # Network - Gray
    "network": {"fill": "#4A5568", "stroke": "#2D3748", "text": "#FFFFFF"},
    "cdn": {"fill": "#4A5568", "stroke": "#2D3748", "text": "#FFFFFF"},
    "load_balancer": {"fill": "#4A5568", "stroke": "#2D3748", "text": "#FFFFFF"},

    # Security - Dark Red
    "security": {"fill": "#9B2C2C", "stroke": "#742A2A", "text": "#FFFFFF"},
    "iam": {"fill": "#9B2C2C", "stroke": "#742A2A", "text": "#FFFFFF"},

    # Integration - Teal
    "integration": {"fill": "#285E61", "stroke": "#1D4044", "text": "#FFFFFF"},
    "messaging": {"fill": "#285E61", "stroke": "#1D4044", "text": "#FFFFFF"},
    "queue": {"fill": "#285E61", "stroke": "#1D4044", "text": "#FFFFFF"},

    # Analytics - Purple
    "analytics": {"fill": "#553C9A", "stroke": "#44337A", "text": "#FFFFFF"},
    "ml": {"fill": "#553C9A", "stroke": "#44337A", "text": "#FFFFFF"},

    # Management - Slate
    "monitoring": {"fill": "#718096", "stroke": "#4A5568", "text": "#FFFFFF"},
    "devops": {"fill": "#2D3748", "stroke": "#1A202C", "text": "#FFFFFF"},

    # General
    "client": {"fill": "#A0AEC0", "stroke": "#718096", "text": "#1A202C"},
    "user": {"fill": "#A0AEC0", "stroke": "#718096", "text": "#1A202C"},
}

CorporateTheme = ProfessionalTheme(
    name="corporate",
    variant=ThemeVariant.LIGHT,

    # Corporate brand colors
    background="#FFFFFF",
    foreground="#1A202C",
    primary="#2B6CB0",
    secondary="#4A5568",
    accent="#3182CE",

    # Node styling
    node_fill="#FFFFFF",
    node_stroke="#E2E8F0",
    node_text="#1A202C",

    # Edge styling
    edge_stroke="#718096",
    edge_label_color="#4A5568",

    # Cluster styling
    cluster_fill="#F7FAFC",
    cluster_stroke="#E2E8F0",
    cluster_text="#2D3748",

    # Category colors
    category_colors=CORPORATE_CATEGORY_COLORS,

    # Professional features
    gradient=GradientConfig(
        enabled=True,
        direction="vertical",
        color_stops=[(0, "#FFFFFF"), (100, "#F7FAFC")]
    ),
    shadow=ShadowConfig(
        enabled=True,
        offset_x=0,
        offset_y=4,
        blur=6,
        color="rgba(0,0,0,0.07)"
    ),
    typography=TypographyConfig(
        font_family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
        node_label_size=13,
        node_label_weight="500",
        edge_label_size=11,
        edge_label_weight="400",
        title_size=24,
        title_weight="600"
    ),
    node_style=NodeStyleConfig(
        border_radius=6,
        border_width=1,
        min_width=120,
        min_height=64,
        padding=16,
        icon_size=36,
        icon_position="top"
    ),
    edge_style=EdgeStyleConfig(
        stroke_width=1.5,
        arrow_size=8,
        curve_type="bezier",
        dash_pattern=None
    ),

    show_icons=True,
    icon_style="colored"
)


# =============================================================================
# Dark Variants
# =============================================================================

AWSThemeDark = ProfessionalTheme(
    name="aws-dark",
    variant=ThemeVariant.DARK,

    background="#232F3E",
    foreground="#FFFFFF",
    primary="#FF9900",
    secondary="#FFFFFF",
    accent="#146EB4",

    node_fill="#37475A",
    node_stroke="#5C6C7A",
    node_text="#FFFFFF",

    edge_stroke="#879196",
    edge_label_color="#D1D5DB",

    cluster_fill="#2A3A4D",
    cluster_stroke="#5C6C7A",
    cluster_text="#FFFFFF",

    category_colors=AWS_CATEGORY_COLORS,

    gradient=GradientConfig(
        enabled=True,
        direction="vertical",
        color_stops=[(0, "#37475A"), (100, "#2A3A4D")]
    ),
    shadow=ShadowConfig(
        enabled=True,
        offset_x=0,
        offset_y=4,
        blur=12,
        color="rgba(0,0,0,0.4)"
    ),
    typography=AWSTheme.typography,
    node_style=AWSTheme.node_style,
    edge_style=AWSTheme.edge_style,

    show_icons=True,
    icon_style="colored"
)


GCPThemeDark = ProfessionalTheme(
    name="gcp-dark",
    variant=ThemeVariant.DARK,

    background="#202124",
    foreground="#E8EAED",
    primary="#8AB4F8",
    secondary="#9AA0A6",
    accent="#81C995",

    node_fill="#303134",
    node_stroke="#5F6368",
    node_text="#E8EAED",

    edge_stroke="#9AA0A6",
    edge_label_color="#9AA0A6",

    cluster_fill="#292A2D",
    cluster_stroke="#5F6368",
    cluster_text="#E8EAED",

    category_colors=GCP_CATEGORY_COLORS,

    gradient=GradientConfig(enabled=False),
    shadow=ShadowConfig(
        enabled=True,
        offset_x=0,
        offset_y=2,
        blur=6,
        color="rgba(0,0,0,0.5)"
    ),
    typography=GCPTheme.typography,
    node_style=GCPTheme.node_style,
    edge_style=GCPTheme.edge_style,

    show_icons=True,
    icon_style="colored"
)


AzureThemeDark = ProfessionalTheme(
    name="azure-dark",
    variant=ThemeVariant.DARK,

    background="#1B1A19",
    foreground="#FFFFFF",
    primary="#2899F5",
    secondary="#0078D4",
    accent="#50E6FF",

    node_fill="#292827",
    node_stroke="#484644",
    node_text="#FFFFFF",

    edge_stroke="#A19F9D",
    edge_label_color="#D2D0CE",

    cluster_fill="#201F1E",
    cluster_stroke="#484644",
    cluster_text="#FFFFFF",

    category_colors=AZURE_CATEGORY_COLORS,

    gradient=GradientConfig(
        enabled=True,
        direction="vertical",
        color_stops=[(0, "#292827"), (100, "#201F1E")]
    ),
    shadow=ShadowConfig(
        enabled=True,
        offset_x=0,
        offset_y=3.2,
        blur=7.2,
        color="rgba(0,0,0,0.36)"
    ),
    typography=AzureTheme.typography,
    node_style=AzureTheme.node_style,
    edge_style=AzureTheme.edge_style,

    show_icons=True,
    icon_style="colored"
)


CorporateThemeDark = ProfessionalTheme(
    name="corporate-dark",
    variant=ThemeVariant.DARK,

    background="#1A202C",
    foreground="#F7FAFC",
    primary="#63B3ED",
    secondary="#A0AEC0",
    accent="#4FD1C5",

    node_fill="#2D3748",
    node_stroke="#4A5568",
    node_text="#F7FAFC",

    edge_stroke="#718096",
    edge_label_color="#A0AEC0",

    cluster_fill="#252D3D",
    cluster_stroke="#4A5568",
    cluster_text="#F7FAFC",

    category_colors=CORPORATE_CATEGORY_COLORS,

    gradient=GradientConfig(
        enabled=True,
        direction="vertical",
        color_stops=[(0, "#2D3748"), (100, "#1A202C")]
    ),
    shadow=ShadowConfig(
        enabled=True,
        offset_x=0,
        offset_y=4,
        blur=8,
        color="rgba(0,0,0,0.4)"
    ),
    typography=CorporateTheme.typography,
    node_style=CorporateTheme.node_style,
    edge_style=CorporateTheme.edge_style,

    show_icons=True,
    icon_style="colored"
)


# =============================================================================
# Theme Registry
# =============================================================================

_PROFESSIONAL_THEMES: Dict[str, ProfessionalTheme] = {
    "aws": AWSTheme,
    "aws-dark": AWSThemeDark,
    "gcp": GCPTheme,
    "gcp-dark": GCPThemeDark,
    "azure": AzureTheme,
    "azure-dark": AzureThemeDark,
    "corporate": CorporateTheme,
    "corporate-dark": CorporateThemeDark,
}


def get_professional_theme(name: str) -> Optional[ProfessionalTheme]:
    """
    Get a professional theme by name.

    Args:
        name: Theme name (aws, gcp, azure, corporate, or with -dark suffix)

    Returns:
        ProfessionalTheme or None if not found
    """
    return _PROFESSIONAL_THEMES.get(name.lower())


def list_professional_themes() -> List[str]:
    """
    List all available professional theme names.

    Returns:
        List of theme names
    """
    return list(_PROFESSIONAL_THEMES.keys())
