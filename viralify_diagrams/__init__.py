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
- Intelligent diagram taxonomy and template system
- Support for C4, UML, DFD, ERD, BPMN, STRIDE, K8s, CI/CD diagrams
"""

__version__ = "2.2.0"

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

# Taxonomy and Classification
from viralify_diagrams.taxonomy import (
    # Categories and enums
    DiagramDomain,
    DiagramCategory,
    DiagramType,
    TargetAudience,
    DiagramComplexity,
    # Classifier
    RequestClassifier,
    ClassificationResult,
    # Router
    DiagramRouter,
    RoutingResult,
    SlideConfig,
    # Slide Optimizer
    SlideOptimizer,
    SlideRecommendation,
    OptimizationResult,
)

# Templates
from viralify_diagrams.templates import (
    # Base classes
    DiagramTemplate,
    TemplateElement,
    TemplateRelation,
    TemplateConstraint,
    TemplateConfig,
    ValidationResult,
    # Registry
    TemplateRegistry,
    get_template_registry,
    get_template,
    list_templates,
    register_template,
)

# Architecture Templates
from viralify_diagrams.templates.architecture import (
    C4ContextTemplate,
    C4ContainerTemplate,
    C4ComponentTemplate,
    C4DeploymentTemplate,
)

# UML Templates
from viralify_diagrams.templates.uml import (
    UMLClassTemplate,
    UMLSequenceTemplate,
    UMLActivityTemplate,
)

# Data Templates
from viralify_diagrams.templates.data import (
    DFDTemplate,
    ERDTemplate,
    DataLineageTemplate,
)

# Security Templates
from viralify_diagrams.templates.security import (
    STRIDEThreatTemplate,
)

# DevOps Templates
from viralify_diagrams.templates.devops import (
    CICDPipelineTemplate,
    KubernetesTemplate,
)

# Business Templates
from viralify_diagrams.templates.business import (
    BPMNProcessTemplate,
)

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
    # Taxonomy
    "DiagramDomain",
    "DiagramCategory",
    "DiagramType",
    "TargetAudience",
    "DiagramComplexity",
    "RequestClassifier",
    "ClassificationResult",
    "DiagramRouter",
    "RoutingResult",
    "SlideConfig",
    "SlideOptimizer",
    "SlideRecommendation",
    "OptimizationResult",
    # Templates - Base
    "DiagramTemplate",
    "TemplateElement",
    "TemplateRelation",
    "TemplateConstraint",
    "TemplateConfig",
    "ValidationResult",
    "TemplateRegistry",
    "get_template_registry",
    "get_template",
    "list_templates",
    "register_template",
    # Templates - Architecture (C4)
    "C4ContextTemplate",
    "C4ContainerTemplate",
    "C4ComponentTemplate",
    "C4DeploymentTemplate",
    # Templates - UML
    "UMLClassTemplate",
    "UMLSequenceTemplate",
    "UMLActivityTemplate",
    # Templates - Data
    "DFDTemplate",
    "ERDTemplate",
    "DataLineageTemplate",
    # Templates - Security
    "STRIDEThreatTemplate",
    # Templates - DevOps
    "CICDPipelineTemplate",
    "KubernetesTemplate",
    # Templates - Business
    "BPMNProcessTemplate",
]
