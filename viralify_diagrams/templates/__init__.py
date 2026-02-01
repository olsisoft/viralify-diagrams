"""
Viralify Diagrams - Template System

Provides diagram templates for various standards and methodologies:
- Architecture: C4 Model, TOGAF, ArchiMate
- Development: UML (Class, Sequence, Activity, State)
- Data: DFD, ERD, Data Lineage, Star Schema
- Security: STRIDE, Threat Models, Zero Trust
- DevOps: CI/CD Pipelines, Kubernetes, GitOps
- Business: BPMN, Value Stream, Org Charts
"""

from viralify_diagrams.templates.base import (
    DiagramTemplate,
    TemplateElement,
    TemplateRelation,
    TemplateConstraint,
    TemplateConfig,
    ValidationResult,
)

from viralify_diagrams.templates.registry import (
    TemplateRegistry,
    get_template_registry,
    get_template,
    list_templates,
    register_template,
)

__all__ = [
    # Base classes
    "DiagramTemplate",
    "TemplateElement",
    "TemplateRelation",
    "TemplateConstraint",
    "TemplateConfig",
    "ValidationResult",
    # Registry
    "TemplateRegistry",
    "get_template_registry",
    "get_template",
    "list_templates",
    "register_template",
]
