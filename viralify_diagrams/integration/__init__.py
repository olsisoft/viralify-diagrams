"""
Viralify Diagrams - Integration Module

Provides integration with external services:
- Presentation Generator: Gets content for diagram templates
- Content Enrichment: Fetches additional context for diagrams
"""

from viralify_diagrams.integration.presentation_client import (
    PresentationGeneratorClient,
    DiagramContentRequest,
    DiagramContentResponse,
    ContentElement,
    get_presentation_client,
)

from viralify_diagrams.integration.orchestrator import (
    DiagramOrchestrator,
    OrchestrationRequest,
    OrchestrationResult,
    orchestrate_diagram_generation,
)

__all__ = [
    # Client
    "PresentationGeneratorClient",
    "DiagramContentRequest",
    "DiagramContentResponse",
    "ContentElement",
    "get_presentation_client",
    # Orchestrator
    "DiagramOrchestrator",
    "OrchestrationRequest",
    "OrchestrationResult",
    "orchestrate_diagram_generation",
]
