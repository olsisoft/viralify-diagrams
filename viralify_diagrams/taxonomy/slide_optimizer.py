"""
Slide Optimizer for Enterprise-Grade Diagram Output

Determines the optimal number of slides and their content distribution
for professional presentations based on:
- Element count and complexity
- Target audience attention span
- Information density guidelines
- Progressive disclosure principles
- Visual hierarchy best practices
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
from enum import Enum

from viralify_diagrams.taxonomy.categories import (
    DiagramType,
    ComplexityLevel,
    AudienceType,
    DIAGRAM_MAX_ELEMENTS,
)


class SlideType(str, Enum):
    """Types of slides in a presentation"""
    TITLE = "title"
    OVERVIEW = "overview"
    DETAIL = "detail"
    ZOOM = "zoom"
    TRANSITION = "transition"
    SUMMARY = "summary"
    LEGEND = "legend"


@dataclass
class OptimizationConfig:
    """Configuration for slide optimization"""
    # Element limits
    max_elements_per_slide: int = 8
    min_elements_per_slide: int = 3
    optimal_elements_per_slide: int = 6

    # Time constraints
    target_duration_per_slide_seconds: int = 45
    max_duration_per_slide_seconds: int = 90
    min_duration_per_slide_seconds: int = 20

    # Visual constraints
    max_edge_density: float = 2.5  # edges per node
    max_label_density: int = 15    # labels per slide

    # Progressive disclosure
    include_overview_slide: bool = True
    include_summary_slide: bool = True
    include_legend: bool = True

    # Quality settings
    enterprise_mode: bool = True   # Stricter limits for enterprise
    allow_element_splitting: bool = True  # Split large diagrams
    group_by_cluster: bool = True  # Group elements by logical clusters


@dataclass
class ElementGroup:
    """A group of related elements"""
    group_id: str
    name: str
    elements: List[str]  # Element IDs
    priority: int = 1    # Higher = more important
    cluster_id: Optional[str] = None


@dataclass
class SlideRecommendation:
    """Recommendation for a single slide"""
    slide_type: SlideType
    slide_index: int
    title: str
    description: str

    # Content
    element_ids: List[str] = field(default_factory=list)
    element_groups: List[ElementGroup] = field(default_factory=list)
    focus_area: Optional[str] = None

    # Timing
    estimated_duration_seconds: int = 45
    narration_points: List[str] = field(default_factory=list)

    # Visual settings
    zoom_level: float = 1.0
    highlight_elements: List[str] = field(default_factory=list)
    fade_elements: List[str] = field(default_factory=list)

    @property
    def element_count(self) -> int:
        return len(self.element_ids)


@dataclass
class OptimizationResult:
    """Complete optimization result"""
    slides: List[SlideRecommendation]
    total_elements: int
    total_duration_seconds: int
    optimization_score: float  # 0-100
    warnings: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)

    @property
    def slide_count(self) -> int:
        return len(self.slides)

    @property
    def avg_elements_per_slide(self) -> float:
        content_slides = [s for s in self.slides if s.slide_type not in [SlideType.TITLE, SlideType.SUMMARY, SlideType.LEGEND]]
        if not content_slides:
            return 0
        return sum(s.element_count for s in content_slides) / len(content_slides)


class SlideOptimizer:
    """
    Slide optimizer for enterprise-grade diagram presentations.

    Analyzes diagram complexity and recommends optimal slide breakdown
    for professional, readable output.

    Example:
        >>> optimizer = SlideOptimizer()
        >>> result = optimizer.optimize(
        ...     element_count=25,
        ...     diagram_type=DiagramType.MICROSERVICES_ARCH,
        ...     audience=AudienceType.ARCHITECT
        ... )
        >>> print(f"Recommended {result.slide_count} slides")
        >>> for slide in result.slides:
        ...     print(f"  {slide.title}: {slide.element_count} elements")
    """

    def __init__(self, config: Optional[OptimizationConfig] = None):
        self.config = config or OptimizationConfig()

    def optimize(
        self,
        element_count: int,
        diagram_type: DiagramType,
        audience: AudienceType = AudienceType.GENERAL,
        element_groups: Optional[List[ElementGroup]] = None,
        edge_count: Optional[int] = None,
        constraints: Optional[Dict] = None
    ) -> OptimizationResult:
        """
        Optimize slide breakdown for a diagram.

        Args:
            element_count: Total number of elements
            diagram_type: Type of diagram
            audience: Target audience
            element_groups: Pre-defined element groups
            edge_count: Number of edges (for density calculation)
            constraints: Additional constraints

        Returns:
            OptimizationResult with recommended slides
        """
        # Adjust config for audience
        config = self._adjust_config_for_audience(audience)

        # Calculate metrics
        edge_density = (edge_count / element_count) if edge_count and element_count else 1.5
        is_dense = edge_density > config.max_edge_density

        # Adjust max elements for density
        max_per_slide = config.max_elements_per_slide
        if is_dense:
            max_per_slide = int(max_per_slide * 0.7)

        # Calculate slide breakdown
        slides = self._calculate_slides(
            element_count=element_count,
            max_per_slide=max_per_slide,
            diagram_type=diagram_type,
            audience=audience,
            element_groups=element_groups,
            config=config
        )

        # Calculate metrics
        total_duration = sum(s.estimated_duration_seconds for s in slides)
        optimization_score = self._calculate_score(slides, element_count, config)
        warnings, suggestions = self._generate_feedback(slides, element_count, edge_density, config)

        return OptimizationResult(
            slides=slides,
            total_elements=element_count,
            total_duration_seconds=total_duration,
            optimization_score=optimization_score,
            warnings=warnings,
            suggestions=suggestions,
        )

    def _adjust_config_for_audience(self, audience: AudienceType) -> OptimizationConfig:
        """Adjust configuration based on audience"""
        config = OptimizationConfig(
            max_elements_per_slide=self.config.max_elements_per_slide,
            min_elements_per_slide=self.config.min_elements_per_slide,
            optimal_elements_per_slide=self.config.optimal_elements_per_slide,
            target_duration_per_slide_seconds=self.config.target_duration_per_slide_seconds,
            enterprise_mode=self.config.enterprise_mode,
        )

        if audience == AudienceType.EXECUTIVE:
            # Executives prefer fewer elements, shorter slides
            config.max_elements_per_slide = 5
            config.optimal_elements_per_slide = 4
            config.target_duration_per_slide_seconds = 30
            config.include_legend = False

        elif audience == AudienceType.ARCHITECT:
            # Architects can handle more complexity
            config.max_elements_per_slide = 12
            config.optimal_elements_per_slide = 8
            config.target_duration_per_slide_seconds = 60

        elif audience == AudienceType.DEVELOPER:
            # Developers want detail but not overwhelming
            config.max_elements_per_slide = 10
            config.optimal_elements_per_slide = 7
            config.target_duration_per_slide_seconds = 45

        elif audience == AudienceType.DATA_ENGINEER:
            # Data engineers are used to complex flows
            config.max_elements_per_slide = 12
            config.optimal_elements_per_slide = 9
            config.target_duration_per_slide_seconds = 50

        return config

    def _calculate_slides(
        self,
        element_count: int,
        max_per_slide: int,
        diagram_type: DiagramType,
        audience: AudienceType,
        element_groups: Optional[List[ElementGroup]],
        config: OptimizationConfig
    ) -> List[SlideRecommendation]:
        """Calculate optimal slide breakdown"""
        slides = []

        # Add overview slide if configured
        if config.include_overview_slide and element_count > max_per_slide:
            slides.append(SlideRecommendation(
                slide_type=SlideType.OVERVIEW,
                slide_index=1,
                title=self._get_overview_title(diagram_type),
                description="High-level view of the complete system",
                element_ids=[],  # All elements, simplified
                estimated_duration_seconds=config.target_duration_per_slide_seconds,
                narration_points=[
                    "This is the complete system overview",
                    "We'll explore each section in detail",
                ],
                zoom_level=0.5,  # Zoomed out
            ))

        # Calculate content slides
        if element_groups:
            # Use pre-defined groups
            content_slides = self._slides_from_groups(
                element_groups,
                max_per_slide,
                diagram_type,
                config,
                start_index=len(slides) + 1
            )
        else:
            # Calculate optimal grouping
            content_slides = self._calculate_content_slides(
                element_count,
                max_per_slide,
                diagram_type,
                config,
                start_index=len(slides) + 1
            )

        slides.extend(content_slides)

        # Add legend slide if configured and needed
        if config.include_legend and element_count > 8:
            slides.append(SlideRecommendation(
                slide_type=SlideType.LEGEND,
                slide_index=len(slides) + 1,
                title="Legend & Notation",
                description="Explanation of symbols and conventions",
                estimated_duration_seconds=20,
                narration_points=["Here's a quick reference for the notation used"],
            ))

        # Add summary slide if configured and multiple content slides
        if config.include_summary_slide and len(content_slides) > 2:
            slides.append(SlideRecommendation(
                slide_type=SlideType.SUMMARY,
                slide_index=len(slides) + 1,
                title="Summary",
                description="Key takeaways and next steps",
                estimated_duration_seconds=30,
                narration_points=[
                    "Let's recap the key points",
                    "The main components and their relationships",
                    "Next steps for implementation",
                ],
            ))

        return slides

    def _calculate_content_slides(
        self,
        element_count: int,
        max_per_slide: int,
        diagram_type: DiagramType,
        config: OptimizationConfig,
        start_index: int
    ) -> List[SlideRecommendation]:
        """Calculate content slides for elements"""
        slides = []

        if element_count <= max_per_slide:
            # Single content slide
            slides.append(SlideRecommendation(
                slide_type=SlideType.DETAIL,
                slide_index=start_index,
                title=self._get_detail_title(diagram_type, 1, 1),
                description="Complete diagram view",
                element_ids=[f"element_{i}" for i in range(element_count)],
                estimated_duration_seconds=config.target_duration_per_slide_seconds,
                narration_points=self._generate_narration_points(element_count),
            ))
        else:
            # Multiple content slides
            num_slides = self._calculate_optimal_slide_count(
                element_count,
                max_per_slide,
                config.min_elements_per_slide,
                config.optimal_elements_per_slide
            )

            elements_per_slide = element_count // num_slides
            remainder = element_count % num_slides

            current_element = 0
            for i in range(num_slides):
                # Distribute remainder elements
                slide_elements = elements_per_slide + (1 if i < remainder else 0)
                element_ids = [f"element_{j}" for j in range(current_element, current_element + slide_elements)]
                current_element += slide_elements

                # Determine slide type
                if i == 0:
                    slide_type = SlideType.DETAIL
                    focus = "primary components"
                else:
                    slide_type = SlideType.ZOOM
                    focus = f"section {i + 1}"

                slides.append(SlideRecommendation(
                    slide_type=slide_type,
                    slide_index=start_index + i,
                    title=self._get_detail_title(diagram_type, i + 1, num_slides),
                    description=f"Focus on {focus}",
                    element_ids=element_ids,
                    focus_area=f"section_{i}",
                    estimated_duration_seconds=config.target_duration_per_slide_seconds,
                    narration_points=self._generate_narration_points(slide_elements),
                ))

        return slides

    def _slides_from_groups(
        self,
        groups: List[ElementGroup],
        max_per_slide: int,
        diagram_type: DiagramType,
        config: OptimizationConfig,
        start_index: int
    ) -> List[SlideRecommendation]:
        """Create slides from pre-defined groups"""
        slides = []

        # Sort groups by priority
        sorted_groups = sorted(groups, key=lambda g: g.priority, reverse=True)

        current_slide_elements: List[str] = []
        current_groups: List[ElementGroup] = []
        slide_index = start_index

        for group in sorted_groups:
            # Check if group fits in current slide
            if len(current_slide_elements) + len(group.elements) <= max_per_slide:
                current_slide_elements.extend(group.elements)
                current_groups.append(group)
            else:
                # Create slide for current elements
                if current_slide_elements:
                    slides.append(SlideRecommendation(
                        slide_type=SlideType.DETAIL,
                        slide_index=slide_index,
                        title=self._get_group_title(current_groups),
                        description=f"Focus on: {', '.join(g.name for g in current_groups)}",
                        element_ids=current_slide_elements.copy(),
                        element_groups=current_groups.copy(),
                        estimated_duration_seconds=config.target_duration_per_slide_seconds,
                        narration_points=self._generate_group_narration(current_groups),
                    ))
                    slide_index += 1

                # Start new slide with current group
                current_slide_elements = group.elements.copy()
                current_groups = [group]

        # Don't forget last slide
        if current_slide_elements:
            slides.append(SlideRecommendation(
                slide_type=SlideType.DETAIL,
                slide_index=slide_index,
                title=self._get_group_title(current_groups),
                description=f"Focus on: {', '.join(g.name for g in current_groups)}",
                element_ids=current_slide_elements,
                element_groups=current_groups,
                estimated_duration_seconds=config.target_duration_per_slide_seconds,
                narration_points=self._generate_group_narration(current_groups),
            ))

        return slides

    def _calculate_optimal_slide_count(
        self,
        element_count: int,
        max_per_slide: int,
        min_per_slide: int,
        optimal_per_slide: int
    ) -> int:
        """Calculate optimal number of slides"""
        # Minimum slides needed
        min_slides = (element_count + max_per_slide - 1) // max_per_slide

        # Maximum slides (respecting min elements)
        max_slides = element_count // min_per_slide

        # Optimal slides
        optimal_slides = (element_count + optimal_per_slide - 1) // optimal_per_slide

        # Choose optimal within bounds
        return max(min_slides, min(optimal_slides, max_slides))

    def _get_overview_title(self, diagram_type: DiagramType) -> str:
        """Get overview slide title"""
        titles = {
            DiagramType.C4_CONTEXT: "System Context Overview",
            DiagramType.C4_CONTAINER: "Container Architecture Overview",
            DiagramType.MICROSERVICES_ARCH: "Microservices Overview",
            DiagramType.DATA_LINEAGE: "Data Flow Overview",
            DiagramType.KUBERNETES_CLUSTER: "Kubernetes Cluster Overview",
        }
        return titles.get(diagram_type, "System Overview")

    def _get_detail_title(
        self,
        diagram_type: DiagramType,
        index: int,
        total: int
    ) -> str:
        """Get detail slide title"""
        if total == 1:
            return "System Architecture"

        # Type-specific titles
        if diagram_type == DiagramType.MICROSERVICES_ARCH:
            sections = ["Core Services", "Supporting Services", "Infrastructure", "External Integrations"]
        elif diagram_type == DiagramType.DATA_LINEAGE:
            sections = ["Data Sources", "Ingestion Layer", "Transformation", "Data Products"]
        elif diagram_type == DiagramType.KUBERNETES_CLUSTER:
            sections = ["Control Plane", "Worker Nodes", "Networking", "Storage"]
        else:
            sections = [f"Section {i + 1}" for i in range(total)]

        if index <= len(sections):
            return sections[index - 1]
        return f"Section {index}"

    def _get_group_title(self, groups: List[ElementGroup]) -> str:
        """Get title from element groups"""
        if len(groups) == 1:
            return groups[0].name
        elif len(groups) <= 3:
            return " & ".join(g.name for g in groups)
        else:
            return f"{groups[0].name} and {len(groups) - 1} more"

    def _generate_narration_points(self, element_count: int) -> List[str]:
        """Generate narration points for a slide"""
        points = []

        if element_count <= 3:
            points.append("Let's examine each component in detail")
        elif element_count <= 6:
            points.append("This section contains several key components")
            points.append("Notice how they interact with each other")
        else:
            points.append("This is a complex section with multiple components")
            points.append("Let's focus on the main relationships")
            points.append("The key takeaway here is the data flow")

        return points

    def _generate_group_narration(self, groups: List[ElementGroup]) -> List[str]:
        """Generate narration for element groups"""
        points = []

        for group in groups[:3]:
            points.append(f"The {group.name} handles...")

        if len(groups) > 3:
            points.append(f"Plus {len(groups) - 3} additional components")

        return points

    def _calculate_score(
        self,
        slides: List[SlideRecommendation],
        element_count: int,
        config: OptimizationConfig
    ) -> float:
        """Calculate optimization score (0-100)"""
        score = 100.0

        # Penalize for too few or too many elements per slide
        for slide in slides:
            if slide.slide_type in [SlideType.DETAIL, SlideType.ZOOM]:
                if slide.element_count > config.max_elements_per_slide:
                    score -= 5 * (slide.element_count - config.max_elements_per_slide)
                elif slide.element_count < config.min_elements_per_slide and slide.element_count > 0:
                    score -= 3 * (config.min_elements_per_slide - slide.element_count)

        # Penalize for too many slides
        optimal_slide_count = (element_count + config.optimal_elements_per_slide - 1) // config.optimal_elements_per_slide
        if len(slides) > optimal_slide_count * 1.5:
            score -= 10

        # Bonus for good distribution
        content_slides = [s for s in slides if s.slide_type in [SlideType.DETAIL, SlideType.ZOOM]]
        if content_slides:
            counts = [s.element_count for s in content_slides if s.element_count > 0]
            if counts:
                variance = sum((c - sum(counts)/len(counts))**2 for c in counts) / len(counts)
                if variance < 4:  # Low variance is good
                    score += 5

        return max(0, min(100, score))

    def _generate_feedback(
        self,
        slides: List[SlideRecommendation],
        element_count: int,
        edge_density: float,
        config: OptimizationConfig
    ) -> Tuple[List[str], List[str]]:
        """Generate warnings and suggestions"""
        warnings = []
        suggestions = []

        # Check for overcrowded slides
        for slide in slides:
            if slide.element_count > config.max_elements_per_slide:
                warnings.append(f"Slide '{slide.title}' has {slide.element_count} elements (max: {config.max_elements_per_slide})")

        # Check edge density
        if edge_density > 3.0:
            warnings.append(f"High edge density ({edge_density:.1f}) may reduce readability")
            suggestions.append("Consider using edge bundling for cleaner visualization")

        # Suggestions for improvement
        if element_count > 20:
            suggestions.append("Consider splitting into multiple related diagrams")

        if len(slides) > 5:
            suggestions.append("Consider adding transition slides between major sections")

        return warnings, suggestions


def optimize_slides(
    element_count: int,
    diagram_type: DiagramType,
    audience: AudienceType = AudienceType.GENERAL,
    enterprise_mode: bool = True
) -> OptimizationResult:
    """
    Convenience function to optimize slides.

    Args:
        element_count: Number of elements
        diagram_type: Type of diagram
        audience: Target audience
        enterprise_mode: Use stricter enterprise limits

    Returns:
        OptimizationResult with recommended slides

    Example:
        >>> result = optimize_slides(18, DiagramType.MICROSERVICES_ARCH)
        >>> print(f"Recommended: {result.slide_count} slides")
    """
    config = OptimizationConfig(enterprise_mode=enterprise_mode)
    optimizer = SlideOptimizer(config)
    return optimizer.optimize(element_count, diagram_type, audience)
