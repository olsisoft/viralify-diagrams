"""
Diagram Generation Orchestrator

Coordinates the full diagram generation workflow:
1. Classifies the request
2. Routes to the appropriate template
3. Determines optimal slide count
4. Fetches content from presentation-generator
5. Generates diagrams using templates
"""

import os
from typing import Dict, Optional, Any, List, Tuple
from dataclasses import dataclass, field

from viralify_diagrams.core.diagram import Diagram, Node, Edge
from viralify_diagrams.taxonomy.categories import (
    DiagramDomain,
    DiagramType,
    TargetAudience,
    DiagramComplexity,
)
from viralify_diagrams.taxonomy.classifier import RequestClassifier, ClassificationResult
from viralify_diagrams.taxonomy.router import DiagramRouter, RoutingResult
from viralify_diagrams.taxonomy.slide_optimizer import SlideOptimizer, OptimizationResult
from viralify_diagrams.templates.registry import get_template_registry, get_template
from viralify_diagrams.templates.base import DiagramTemplate
from viralify_diagrams.integration.presentation_client import (
    PresentationGeneratorClient,
    DiagramContentRequest,
    DiagramContentResponse,
    ContentElement,
    ContentRelation,
    get_presentation_client,
)


@dataclass
class OrchestrationRequest:
    """Request for orchestrated diagram generation"""
    # Required
    topic: str
    description: Optional[str] = None

    # Optional hints
    diagram_type_hint: Optional[str] = None  # e.g., "c4_context", "sequence"
    domain_hint: Optional[str] = None  # e.g., "architecture", "data"

    # Audience and styling
    target_audience: str = "developer"
    complexity: str = "medium"
    theme: str = "corporate"

    # Output preferences
    language: str = "en"
    max_slides: Optional[int] = None
    max_elements_per_slide: int = 10

    # Source content
    source_documents: List[str] = field(default_factory=list)
    additional_context: Optional[str] = None


@dataclass
class GeneratedSlide:
    """A single generated slide/diagram"""
    slide_number: int
    title: str
    diagram: Diagram
    narration: Optional[str] = None
    notes: Optional[str] = None
    template_id: str = ""
    element_count: int = 0


@dataclass
class OrchestrationResult:
    """Result of orchestrated diagram generation"""
    success: bool
    slides: List[GeneratedSlide] = field(default_factory=list)

    # Metadata
    classification: Optional[ClassificationResult] = None
    routing: Optional[RoutingResult] = None
    optimization: Optional[OptimizationResult] = None

    # Timing and stats
    total_elements: int = 0
    total_relations: int = 0

    # Errors and warnings
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class DiagramOrchestrator:
    """
    Main orchestrator for intelligent diagram generation.

    This class coordinates the full workflow:
    1. Takes a natural language request
    2. Classifies the diagram type needed
    3. Routes to the appropriate template
    4. Determines optimal slide breakdown
    5. Fetches content from presentation-generator
    6. Creates diagram objects using templates

    Example:
        >>> orchestrator = DiagramOrchestrator()
        >>> request = OrchestrationRequest(
        ...     topic="E-commerce microservices architecture",
        ...     target_audience="architect",
        ...     complexity="high"
        ... )
        >>> result = await orchestrator.generate(request)
        >>> for slide in result.slides:
        ...     # Export each slide
        ...     exporter.export(slide.diagram, f"slide_{slide.slide_number}.svg")
    """

    def __init__(
        self,
        presentation_client: Optional[PresentationGeneratorClient] = None,
        enable_content_fetch: bool = True
    ):
        """
        Initialize the orchestrator.

        Args:
            presentation_client: Client for fetching content
            enable_content_fetch: Whether to fetch content from service
        """
        self.classifier = RequestClassifier()
        self.router = DiagramRouter()
        self.optimizer = SlideOptimizer()
        self.registry = get_template_registry()
        self.presentation_client = presentation_client
        self.enable_content_fetch = enable_content_fetch

    async def generate(
        self,
        request: OrchestrationRequest
    ) -> OrchestrationResult:
        """
        Generate diagrams from a request.

        Args:
            request: The orchestration request

        Returns:
            OrchestrationResult with generated slides
        """
        result = OrchestrationResult(success=False)

        try:
            # Step 1: Classify the request
            classification = self._classify_request(request)
            result.classification = classification

            if not classification.diagram_type:
                result.errors.append("Could not determine diagram type")
                return result

            # Step 2: Route to template
            routing = self._route_to_template(classification, request)
            result.routing = routing

            if not routing.template_config:
                result.errors.append(f"No template found for {classification.diagram_type}")
                return result

            # Step 3: Optimize slide breakdown
            optimization = self._optimize_slides(routing, request)
            result.optimization = optimization

            # Step 4: Fetch content
            content = await self._fetch_content(
                request,
                classification,
                routing
            )

            if not content.success:
                result.warnings.append(f"Content fetch failed: {content.error}")
                # Generate with mock content
                content = self._generate_fallback_content(request, classification)

            # Step 5: Generate slides
            slides = self._generate_slides(
                request,
                routing,
                optimization,
                content
            )

            result.slides = slides
            result.success = len(slides) > 0
            result.total_elements = sum(s.element_count for s in slides)
            result.total_relations = sum(len(s.diagram.edges) for s in slides)

        except Exception as e:
            result.errors.append(f"Generation failed: {str(e)}")

        return result

    def _classify_request(
        self,
        request: OrchestrationRequest
    ) -> ClassificationResult:
        """Classify the request to determine diagram type"""
        # Use hint if provided
        if request.diagram_type_hint:
            try:
                diagram_type = DiagramType(request.diagram_type_hint)
                return ClassificationResult(
                    diagram_type=diagram_type,
                    confidence=1.0,
                    domain=DiagramDomain(request.domain_hint) if request.domain_hint else None,
                    complexity=DiagramComplexity(request.complexity),
                    audience=TargetAudience(request.target_audience)
                )
            except ValueError:
                pass

        # Classify from topic and description
        full_text = f"{request.topic}. {request.description or ''}"
        return self.classifier.classify(full_text)

    def _route_to_template(
        self,
        classification: ClassificationResult,
        request: OrchestrationRequest
    ) -> RoutingResult:
        """Route to appropriate template"""
        return self.router.route(
            classification,
            audience=request.target_audience,
            complexity=request.complexity
        )

    def _optimize_slides(
        self,
        routing: RoutingResult,
        request: OrchestrationRequest
    ) -> OptimizationResult:
        """Determine optimal slide breakdown"""
        # Estimate element count based on complexity
        complexity_elements = {
            "low": 5,
            "medium": 10,
            "high": 20,
            "very_high": 30
        }
        estimated_elements = complexity_elements.get(request.complexity, 10)

        return self.optimizer.optimize(
            total_elements=estimated_elements,
            diagram_type=routing.template_config.get("diagram_type") if routing.template_config else None,
            audience=request.target_audience,
            max_slides=request.max_slides,
            max_elements_per_slide=request.max_elements_per_slide
        )

    async def _fetch_content(
        self,
        request: OrchestrationRequest,
        classification: ClassificationResult,
        routing: RoutingResult
    ) -> DiagramContentResponse:
        """Fetch content from presentation-generator"""
        if not self.enable_content_fetch:
            return DiagramContentResponse(
                success=False,
                error="Content fetch disabled"
            )

        client = self.presentation_client or get_presentation_client()

        content_request = DiagramContentRequest(
            topic=request.topic,
            diagram_type=classification.diagram_type.value if classification.diagram_type else "generic",
            template_id=routing.template_config.get("template_id", "") if routing.template_config else "",
            context=request.additional_context,
            target_audience=request.target_audience,
            complexity=request.complexity,
            max_elements=request.max_elements_per_slide * (request.max_slides or 5),
            language=request.language,
            source_documents=request.source_documents
        )

        return await client.get_diagram_content(content_request)

    def _generate_fallback_content(
        self,
        request: OrchestrationRequest,
        classification: ClassificationResult
    ) -> DiagramContentResponse:
        """Generate fallback content when fetch fails"""
        from viralify_diagrams.integration.presentation_client import _generate_mock_content

        diagram_type = classification.diagram_type.value if classification.diagram_type else "generic"
        template_id = f"{classification.domain.value}_{diagram_type}" if classification.domain else diagram_type

        return _generate_mock_content(request.topic, diagram_type, template_id)

    def _generate_slides(
        self,
        request: OrchestrationRequest,
        routing: RoutingResult,
        optimization: OptimizationResult,
        content: DiagramContentResponse
    ) -> List[GeneratedSlide]:
        """Generate slide diagrams from content"""
        slides = []

        # Get template
        template_id = routing.template_config.get("template_id") if routing.template_config else None
        template = get_template(template_id) if template_id else None

        # Split content into slides based on optimization
        element_groups = self._split_elements_for_slides(
            content.elements,
            optimization
        )

        for i, (elements, relations) in enumerate(element_groups):
            slide_num = i + 1

            # Create diagram
            diagram = Diagram(
                title=f"{content.title or request.topic} ({slide_num}/{len(element_groups)})",
                theme=request.theme
            )

            # Add elements
            node_map = {}
            for elem in elements:
                node = self._create_node_from_element(elem, template)
                diagram.add_node(node)
                node_map[elem.id] = node

            # Add relations
            for rel in relations:
                if rel.source_id in node_map and rel.target_id in node_map:
                    edge = self._create_edge_from_relation(rel, template)
                    diagram.add_edge(edge)

            slide = GeneratedSlide(
                slide_number=slide_num,
                title=f"Slide {slide_num}: {request.topic}",
                diagram=diagram,
                narration=content.narration,
                template_id=template_id or "",
                element_count=len(elements)
            )
            slides.append(slide)

        return slides

    def _split_elements_for_slides(
        self,
        elements: List[ContentElement],
        optimization: OptimizationResult
    ) -> List[Tuple[List[ContentElement], List[ContentRelation]]]:
        """Split elements into groups for slides"""
        if not elements:
            return []

        max_per_slide = optimization.recommendation.max_elements_per_slide \
            if optimization.recommendation else 10

        groups = []
        for i in range(0, len(elements), max_per_slide):
            group_elements = elements[i:i + max_per_slide]
            group_ids = {e.id for e in group_elements}

            # Find relations within this group
            # (We'd need the full relations list here - simplified for now)
            group_relations = []

            groups.append((group_elements, group_relations))

        return groups

    def _create_node_from_element(
        self,
        element: ContentElement,
        template: Optional[DiagramTemplate]
    ) -> Node:
        """Create a Node from a ContentElement"""
        if template:
            # Use template to create element
            try:
                elem_dict = template.create_element(
                    element.element_type,
                    element.label,
                    {
                        "id": element.id,
                        "description": element.description,
                        **element.properties
                    }
                )
                return Node(
                    id=elem_dict["id"],
                    label=elem_dict["label"],
                    shape=elem_dict.get("shape", "rounded"),
                    fill_color=elem_dict.get("fill_color"),
                    stroke_color=elem_dict.get("stroke_color"),
                    properties=elem_dict.get("properties", {})
                )
            except Exception:
                pass

        # Fallback to simple node
        return Node(
            id=element.id,
            label=element.label,
            shape="rounded",
            properties={"description": element.description}
        )

    def _create_edge_from_relation(
        self,
        relation: ContentRelation,
        template: Optional[DiagramTemplate]
    ) -> Edge:
        """Create an Edge from a ContentRelation"""
        if template:
            try:
                rel_dict = template.create_relation(
                    relation.relation_type,
                    relation.source_id,
                    relation.target_id,
                    relation.label,
                    relation.properties
                )
                return Edge(
                    source=rel_dict["source"],
                    target=rel_dict["target"],
                    label=rel_dict.get("label", ""),
                    line_style=rel_dict.get("line_style", "solid"),
                    arrow_style=rel_dict.get("arrow_style", "open"),
                    properties=rel_dict.get("properties", {})
                )
            except Exception:
                pass

        # Fallback to simple edge
        return Edge(
            source=relation.source_id,
            target=relation.target_id,
            label=relation.label or "",
            line_style="solid",
            arrow_style="open"
        )


# Convenience function for simple use
async def orchestrate_diagram_generation(
    topic: str,
    description: Optional[str] = None,
    target_audience: str = "developer",
    complexity: str = "medium",
    theme: str = "corporate",
    **kwargs
) -> OrchestrationResult:
    """
    Convenience function for orchestrated diagram generation.

    Args:
        topic: The diagram topic
        description: Optional description
        target_audience: Target audience
        complexity: Diagram complexity
        theme: Visual theme
        **kwargs: Additional OrchestrationRequest parameters

    Returns:
        OrchestrationResult with generated diagrams
    """
    orchestrator = DiagramOrchestrator()
    request = OrchestrationRequest(
        topic=topic,
        description=description,
        target_audience=target_audience,
        complexity=complexity,
        theme=theme,
        **kwargs
    )
    return await orchestrator.generate(request)
