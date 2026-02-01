"""
Viralify Diagrams - Intelligent Taxonomy & Routing System

Provides:
- Automatic diagram type classification from natural language
- Smart routing to appropriate templates (C4, UML, DFD, etc.)
- Slide count optimization for enterprise-grade output
- Integration with presentation-generator for content population
"""

from viralify_diagrams.taxonomy.categories import (
    DiagramDomain,
    DiagramCategory,
    DiagramType,
    ComplexityLevel,
    AudienceType,
    DOMAIN_CATEGORIES,
    CATEGORY_TYPES,
)

from viralify_diagrams.taxonomy.classifier import (
    RequestClassifier,
    ClassificationResult,
    classify_request,
)

from viralify_diagrams.taxonomy.router import (
    DiagramRouter,
    RoutingResult,
    route_request,
)

from viralify_diagrams.taxonomy.slide_optimizer import (
    SlideOptimizer,
    SlideRecommendation,
    OptimizationConfig,
    optimize_slides,
)

__all__ = [
    # Categories
    "DiagramDomain",
    "DiagramCategory",
    "DiagramType",
    "ComplexityLevel",
    "AudienceType",
    "DOMAIN_CATEGORIES",
    "CATEGORY_TYPES",
    # Classification
    "RequestClassifier",
    "ClassificationResult",
    "classify_request",
    # Routing
    "DiagramRouter",
    "RoutingResult",
    "route_request",
    # Slide Optimization
    "SlideOptimizer",
    "SlideRecommendation",
    "OptimizationConfig",
    "optimize_slides",
]
