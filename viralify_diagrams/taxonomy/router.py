"""
Diagram Router

Routes classified requests to appropriate templates and configurations.
Integrates with:
- Template Registry for diagram templates
- Slide Optimizer for multi-slide recommendations
- Presentation Generator for content population
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, TYPE_CHECKING
import asyncio

from viralify_diagrams.taxonomy.categories import (
    DiagramDomain,
    DiagramCategory,
    DiagramType,
    ComplexityLevel,
    AudienceType,
    DIAGRAM_LAYOUTS,
    DIAGRAM_MAX_ELEMENTS,
)
from viralify_diagrams.taxonomy.classifier import (
    RequestClassifier,
    ClassificationResult,
    classify_request,
)

if TYPE_CHECKING:
    from viralify_diagrams.templates.base import DiagramTemplate


@dataclass
class TemplateConfig:
    """Configuration for a diagram template"""
    template_id: str
    diagram_type: DiagramType
    layout: str
    max_elements: int
    constraints: Dict[str, Any] = field(default_factory=dict)
    style_overrides: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SlideConfig:
    """Configuration for a single slide/diagram"""
    slide_index: int
    title: str
    diagram_type: DiagramType
    template_config: TemplateConfig
    elements: List[Dict[str, Any]] = field(default_factory=list)
    narration_hint: str = ""
    focus_area: Optional[str] = None  # For zoomed views


@dataclass
class RoutingResult:
    """Result of diagram routing"""
    # Classification
    classification: ClassificationResult

    # Recommended template
    primary_template: TemplateConfig

    # Slide breakdown (for multi-slide presentations)
    slides: List[SlideConfig]

    # Layout recommendation
    recommended_layout: str

    # Edge routing recommendation (for complex diagrams)
    edge_routing: str  # bundled, channel, smart, direct

    # Theme recommendation
    recommended_theme: str

    # Integration hints for presentation-generator
    presentation_hints: Dict[str, Any] = field(default_factory=dict)

    @property
    def slide_count(self) -> int:
        return len(self.slides)

    def to_dict(self) -> Dict:
        """Convert to dictionary for API response"""
        return {
            "classification": self.classification.to_dict(),
            "template": {
                "id": self.primary_template.template_id,
                "type": self.primary_template.diagram_type.value,
                "layout": self.primary_template.layout,
                "max_elements": self.primary_template.max_elements,
            },
            "slides": [
                {
                    "index": s.slide_index,
                    "title": s.title,
                    "type": s.diagram_type.value,
                    "element_count": len(s.elements),
                    "focus_area": s.focus_area,
                }
                for s in self.slides
            ],
            "slide_count": self.slide_count,
            "layout": self.recommended_layout,
            "edge_routing": self.edge_routing,
            "theme": self.recommended_theme,
        }


class DiagramRouter:
    """
    Intelligent diagram router.

    Routes requests to appropriate templates based on classification,
    determines optimal slide count, and provides configuration for
    enterprise-grade output.

    Example:
        >>> router = DiagramRouter()
        >>> result = router.route(
        ...     "Create a C4 diagram for our banking system with 15 microservices",
        ...     audience=AudienceType.ARCHITECT
        ... )
        >>> print(f"Recommended: {result.slide_count} slides")
        >>> for slide in result.slides:
        ...     print(f"  Slide {slide.slide_index}: {slide.title}")
    """

    def __init__(self):
        self.classifier = RequestClassifier()
        self._template_registry = None  # Lazy load

    def route(
        self,
        request: str,
        audience: Optional[AudienceType] = None,
        max_slides: Optional[int] = None,
        context: Optional[Dict] = None
    ) -> RoutingResult:
        """
        Route a request to appropriate template and configuration.

        Args:
            request: Natural language request
            audience: Target audience (overrides detected)
            max_slides: Maximum number of slides to generate
            context: Additional context from presentation-generator

        Returns:
            RoutingResult with template config and slide breakdown
        """
        # Step 1: Classify the request
        classification = self.classifier.classify(request, context)

        # Override audience if specified
        if audience:
            classification.audience = audience

        # Step 2: Get template configuration
        template_config = self._get_template_config(classification)

        # Step 3: Calculate optimal slide breakdown
        slides = self._calculate_slide_breakdown(
            classification,
            template_config,
            max_slides
        )

        # Step 4: Determine edge routing strategy
        edge_routing = self._determine_edge_routing(classification)

        # Step 5: Recommend theme
        theme = self._recommend_theme(classification)

        # Step 6: Generate presentation hints
        hints = self._generate_presentation_hints(classification, slides)

        return RoutingResult(
            classification=classification,
            primary_template=template_config,
            slides=slides,
            recommended_layout=DIAGRAM_LAYOUTS.get(
                classification.diagram_type, "graphviz"
            ),
            edge_routing=edge_routing,
            recommended_theme=theme,
            presentation_hints=hints,
        )

    def _get_template_config(
        self,
        classification: ClassificationResult
    ) -> TemplateConfig:
        """Get template configuration for the classified request"""
        diagram_type = classification.diagram_type

        # Get layout
        layout = DIAGRAM_LAYOUTS.get(diagram_type, "graphviz")

        # Get max elements
        max_elements = DIAGRAM_MAX_ELEMENTS.get(diagram_type, 10)

        # Adjust for complexity
        if classification.complexity == ComplexityLevel.SIMPLE:
            max_elements = min(max_elements, 6)
        elif classification.complexity == ComplexityLevel.ENTERPRISE:
            max_elements = int(max_elements * 1.5)

        # Build constraints
        constraints = self._get_type_constraints(diagram_type)

        # Build style overrides based on audience
        style_overrides = self._get_audience_styles(classification.audience)

        return TemplateConfig(
            template_id=f"template_{diagram_type.value}",
            diagram_type=diagram_type,
            layout=layout,
            max_elements=max_elements,
            constraints=constraints,
            style_overrides=style_overrides,
        )

    def _get_type_constraints(self, diagram_type: DiagramType) -> Dict[str, Any]:
        """Get constraints specific to diagram type"""
        constraints = {
            "allow_self_loops": False,
            "require_labels": True,
        }

        # C4 Model constraints
        if diagram_type in [DiagramType.C4_CONTEXT, DiagramType.C4_CONTAINER]:
            constraints.update({
                "max_depth": 2,
                "require_system_boundary": True,
                "allowed_relationships": ["uses", "reads_from", "writes_to", "sends_to"],
            })

        # UML constraints
        elif diagram_type == DiagramType.UML_CLASS:
            constraints.update({
                "show_attributes": True,
                "show_methods": True,
                "allowed_relationships": ["inherits", "implements", "association", "composition", "aggregation"],
            })

        elif diagram_type == DiagramType.UML_SEQUENCE:
            constraints.update({
                "max_lifelines": 8,
                "show_return_messages": True,
                "number_messages": True,
            })

        # Data constraints
        elif diagram_type == DiagramType.ERD:
            constraints.update({
                "show_cardinality": True,
                "notation": "crow_foot",
            })

        elif diagram_type == DiagramType.DATA_LINEAGE:
            constraints.update({
                "show_transformations": True,
                "direction": "left_to_right",
            })

        # Security constraints
        elif diagram_type == DiagramType.STRIDE_THREAT_MODEL:
            constraints.update({
                "threat_categories": ["spoofing", "tampering", "repudiation", "information_disclosure", "denial_of_service", "elevation_of_privilege"],
                "show_trust_boundaries": True,
            })

        # DevOps constraints
        elif diagram_type == DiagramType.CI_CD_PIPELINE:
            constraints.update({
                "show_stages": True,
                "show_gates": True,
                "direction": "left_to_right",
            })

        elif diagram_type in [DiagramType.KUBERNETES_CLUSTER, DiagramType.KUBERNETES_DEPLOYMENT]:
            constraints.update({
                "show_namespaces": True,
                "show_resources": True,
                "group_by_namespace": True,
            })

        return constraints

    def _get_audience_styles(self, audience: AudienceType) -> Dict[str, Any]:
        """Get style overrides based on audience"""
        base_styles = {
            "font_size_node": 14,
            "font_size_edge": 12,
            "show_technical_details": True,
            "icon_style": "colored",
        }

        if audience == AudienceType.EXECUTIVE:
            base_styles.update({
                "font_size_node": 16,
                "show_technical_details": False,
                "simplify_labels": True,
                "highlight_business_value": True,
                "max_elements_per_slide": 6,
            })

        elif audience == AudienceType.ARCHITECT:
            base_styles.update({
                "show_technical_details": True,
                "show_protocols": True,
                "show_technology_stack": True,
                "max_elements_per_slide": 12,
            })

        elif audience == AudienceType.DEVELOPER:
            base_styles.update({
                "show_code_references": True,
                "show_interfaces": True,
                "show_api_specs": True,
                "max_elements_per_slide": 10,
            })

        elif audience == AudienceType.DEVOPS:
            base_styles.update({
                "show_infrastructure": True,
                "show_deployment_config": True,
                "show_monitoring": True,
                "max_elements_per_slide": 10,
            })

        elif audience == AudienceType.DATA_ENGINEER:
            base_styles.update({
                "show_data_types": True,
                "show_transformations": True,
                "show_volumes": True,
                "max_elements_per_slide": 12,
            })

        elif audience == AudienceType.SECURITY:
            base_styles.update({
                "show_trust_boundaries": True,
                "highlight_attack_surface": True,
                "show_controls": True,
                "max_elements_per_slide": 8,
            })

        return base_styles

    def _calculate_slide_breakdown(
        self,
        classification: ClassificationResult,
        template_config: TemplateConfig,
        max_slides: Optional[int]
    ) -> List[SlideConfig]:
        """
        Calculate optimal slide breakdown for enterprise-grade output.

        Rules:
        - Max 8-10 elements per slide for readability
        - Progressive disclosure: overview -> details
        - Cluster related elements
        - Zoom into complex areas
        """
        slides = []
        diagram_type = classification.diagram_type
        estimated_elements = classification.estimated_elements

        # Calculate base slide count
        max_per_slide = template_config.style_overrides.get("max_elements_per_slide", 8)

        if estimated_elements <= max_per_slide:
            # Single slide is sufficient
            slides.append(SlideConfig(
                slide_index=1,
                title=self._generate_slide_title(diagram_type, "overview"),
                diagram_type=diagram_type,
                template_config=template_config,
                narration_hint="Overview of the complete system",
            ))
        else:
            # Multiple slides needed
            slides = self._generate_multi_slide_breakdown(
                diagram_type,
                estimated_elements,
                max_per_slide,
                template_config,
                classification.complexity
            )

        # Apply max_slides limit if specified
        if max_slides and len(slides) > max_slides:
            slides = slides[:max_slides]

        return slides

    def _generate_multi_slide_breakdown(
        self,
        diagram_type: DiagramType,
        element_count: int,
        max_per_slide: int,
        template_config: TemplateConfig,
        complexity: ComplexityLevel
    ) -> List[SlideConfig]:
        """Generate multi-slide breakdown based on diagram type"""
        slides = []

        # C4 Model: natural hierarchy
        if diagram_type in [DiagramType.C4_CONTEXT, DiagramType.C4_CONTAINER, DiagramType.C4_COMPONENT]:
            return self._c4_slide_breakdown(diagram_type, element_count, template_config)

        # UML Sequence: split by interaction groups
        elif diagram_type == DiagramType.UML_SEQUENCE:
            return self._sequence_slide_breakdown(element_count, template_config)

        # Data lineage: split by pipeline stages
        elif diagram_type == DiagramType.DATA_LINEAGE:
            return self._lineage_slide_breakdown(element_count, template_config)

        # Generic breakdown
        else:
            num_slides = (element_count + max_per_slide - 1) // max_per_slide

            # Always start with overview
            slides.append(SlideConfig(
                slide_index=1,
                title=self._generate_slide_title(diagram_type, "overview"),
                diagram_type=diagram_type,
                template_config=template_config,
                narration_hint="High-level overview of the system",
            ))

            # Add detail slides
            for i in range(1, num_slides):
                slides.append(SlideConfig(
                    slide_index=i + 1,
                    title=self._generate_slide_title(diagram_type, f"detail_{i}"),
                    diagram_type=diagram_type,
                    template_config=template_config,
                    focus_area=f"section_{i}",
                    narration_hint=f"Detailed view of section {i}",
                ))

        return slides

    def _c4_slide_breakdown(
        self,
        diagram_type: DiagramType,
        element_count: int,
        template_config: TemplateConfig
    ) -> List[SlideConfig]:
        """Generate C4 model slide breakdown"""
        slides = []

        if diagram_type == DiagramType.C4_CONTEXT:
            # Context: 1-2 slides
            slides.append(SlideConfig(
                slide_index=1,
                title="System Context",
                diagram_type=DiagramType.C4_CONTEXT,
                template_config=template_config,
                narration_hint="Overview of the system and its external actors",
            ))

        elif diagram_type == DiagramType.C4_CONTAINER:
            # Container: overview + per-container details
            slides.append(SlideConfig(
                slide_index=1,
                title="Container Overview",
                diagram_type=DiagramType.C4_CONTAINER,
                template_config=template_config,
                narration_hint="All containers in the system",
            ))

            # Add slides for major container groups
            container_groups = (element_count + 5) // 6
            for i in range(container_groups):
                slides.append(SlideConfig(
                    slide_index=len(slides) + 1,
                    title=f"Container Group {i + 1}",
                    diagram_type=DiagramType.C4_CONTAINER,
                    template_config=template_config,
                    focus_area=f"group_{i}",
                    narration_hint=f"Detailed view of container group {i + 1}",
                ))

        elif diagram_type == DiagramType.C4_COMPONENT:
            # Component: per-container component diagrams
            slides.append(SlideConfig(
                slide_index=1,
                title="Component Overview",
                diagram_type=DiagramType.C4_COMPONENT,
                template_config=template_config,
                narration_hint="High-level component structure",
            ))

        return slides

    def _sequence_slide_breakdown(
        self,
        interaction_count: int,
        template_config: TemplateConfig
    ) -> List[SlideConfig]:
        """Generate sequence diagram slide breakdown"""
        slides = []
        max_interactions = 6

        num_slides = (interaction_count + max_interactions - 1) // max_interactions

        for i in range(num_slides):
            slides.append(SlideConfig(
                slide_index=i + 1,
                title=f"Sequence Flow - Part {i + 1}" if num_slides > 1 else "Sequence Flow",
                diagram_type=DiagramType.UML_SEQUENCE,
                template_config=template_config,
                focus_area=f"interactions_{i * max_interactions}_{(i + 1) * max_interactions}",
                narration_hint=f"Interactions {i * max_interactions + 1} to {min((i + 1) * max_interactions, interaction_count)}",
            ))

        return slides

    def _lineage_slide_breakdown(
        self,
        element_count: int,
        template_config: TemplateConfig
    ) -> List[SlideConfig]:
        """Generate data lineage slide breakdown"""
        slides = []

        # Overview
        slides.append(SlideConfig(
            slide_index=1,
            title="Data Lineage Overview",
            diagram_type=DiagramType.DATA_LINEAGE,
            template_config=template_config,
            narration_hint="End-to-end data flow",
        ))

        # Source to staging
        slides.append(SlideConfig(
            slide_index=2,
            title="Sources to Staging",
            diagram_type=DiagramType.DATA_LINEAGE,
            template_config=template_config,
            focus_area="ingestion",
            narration_hint="Data ingestion from source systems",
        ))

        # Transformation layer
        if element_count > 8:
            slides.append(SlideConfig(
                slide_index=3,
                title="Transformation Layer",
                diagram_type=DiagramType.DATA_LINEAGE,
                template_config=template_config,
                focus_area="transformation",
                narration_hint="Data transformations and business logic",
            ))

        # Consumption
        slides.append(SlideConfig(
            slide_index=len(slides) + 1,
            title="Data Consumption",
            diagram_type=DiagramType.DATA_LINEAGE,
            template_config=template_config,
            focus_area="consumption",
            narration_hint="Data marts and consumption layer",
        ))

        return slides

    def _determine_edge_routing(
        self,
        classification: ClassificationResult
    ) -> str:
        """Determine edge routing strategy based on complexity"""
        element_count = classification.estimated_elements
        diagram_type = classification.diagram_type

        # Channel routing for orthogonal diagrams
        if diagram_type in [DiagramType.CI_CD_PIPELINE, DiagramType.ETL_PIPELINE, DiagramType.DATA_LINEAGE]:
            return "channel"

        # Bundling for complex graphs
        if element_count > 15:
            return "bundled"

        # Smart routing for medium complexity
        if element_count > 8:
            return "smart"

        return "direct"

    def _recommend_theme(self, classification: ClassificationResult) -> str:
        """Recommend theme based on domain and category"""
        diagram_type = classification.diagram_type

        # Cloud-specific themes
        if diagram_type in [DiagramType.AWS_REFERENCE, DiagramType.AWS_SERVERLESS, DiagramType.AWS_MICROSERVICES]:
            return "aws"
        elif diagram_type in [DiagramType.GCP_REFERENCE, DiagramType.GCP_ANTHOS]:
            return "gcp"
        elif diagram_type in [DiagramType.AZURE_REFERENCE, DiagramType.AZURE_LANDING_ZONE]:
            return "azure"

        # Audience-specific themes
        if classification.audience == AudienceType.EXECUTIVE:
            return "corporate"
        elif classification.audience in [AudienceType.DEVELOPER, AudienceType.DEVOPS]:
            return "dark"

        return "corporate"

    def _generate_slide_title(self, diagram_type: DiagramType, suffix: str) -> str:
        """Generate slide title"""
        type_titles = {
            DiagramType.C4_CONTEXT: "System Context",
            DiagramType.C4_CONTAINER: "Container Diagram",
            DiagramType.C4_COMPONENT: "Component Diagram",
            DiagramType.UML_CLASS: "Class Diagram",
            DiagramType.UML_SEQUENCE: "Sequence Diagram",
            DiagramType.ERD: "Entity Relationship Diagram",
            DiagramType.DATA_LINEAGE: "Data Lineage",
            DiagramType.MICROSERVICES_ARCH: "Microservices Architecture",
            DiagramType.KUBERNETES_CLUSTER: "Kubernetes Architecture",
            DiagramType.CI_CD_PIPELINE: "CI/CD Pipeline",
        }

        base_title = type_titles.get(diagram_type, "System Diagram")

        if suffix == "overview":
            return f"{base_title} - Overview"
        elif suffix.startswith("detail_"):
            return f"{base_title} - Detail View"
        else:
            return base_title

    def _generate_presentation_hints(
        self,
        classification: ClassificationResult,
        slides: List[SlideConfig]
    ) -> Dict[str, Any]:
        """Generate hints for presentation-generator integration"""
        return {
            "total_slides": len(slides),
            "estimated_duration_seconds": len(slides) * 45,  # ~45s per slide
            "narration_style": self._get_narration_style(classification.audience),
            "transition_type": "fade",
            "animation_order": self._get_animation_order(classification.diagram_type),
            "key_points_per_slide": 3,
            "requires_legend": classification.estimated_elements > 6,
            "include_summary_slide": len(slides) > 2,
            "elements_to_populate": classification.detected_entities,
        }

    def _get_narration_style(self, audience: AudienceType) -> str:
        """Get narration style for audience"""
        styles = {
            AudienceType.EXECUTIVE: "professional",
            AudienceType.ARCHITECT: "technical",
            AudienceType.DEVELOPER: "educational",
            AudienceType.BUSINESS: "casual",
        }
        return styles.get(audience, "professional")

    def _get_animation_order(self, diagram_type: DiagramType) -> str:
        """Get animation order for diagram type"""
        if diagram_type in [DiagramType.DATA_LINEAGE, DiagramType.CI_CD_PIPELINE, DiagramType.ETL_PIPELINE]:
            return "left_to_right"
        elif diagram_type in [DiagramType.C4_CONTEXT, DiagramType.C4_CONTAINER, DiagramType.ORG_CHART]:
            return "top_to_bottom"
        elif diagram_type in [DiagramType.UML_SEQUENCE]:
            return "sequential"
        else:
            return "center_out"


def route_request(
    request: str,
    audience: Optional[AudienceType] = None,
    max_slides: Optional[int] = None,
    context: Optional[Dict] = None
) -> RoutingResult:
    """
    Convenience function to route a diagram request.

    Args:
        request: Natural language request
        audience: Target audience
        max_slides: Maximum slides
        context: Additional context

    Returns:
        RoutingResult with complete routing information

    Example:
        >>> result = route_request(
        ...     "Create a complete C4 architecture for our e-commerce platform",
        ...     audience=AudienceType.ARCHITECT,
        ...     max_slides=5
        ... )
        >>> print(f"Will generate {result.slide_count} slides")
    """
    router = DiagramRouter()
    return router.route(request, audience, max_slides, context)
