"""
Base Template Classes

Defines the foundation for all diagram templates with:
- Template elements (nodes with specific shapes/icons)
- Template relations (allowed connection types)
- Template constraints (validation rules)
- Template configuration (layout, styling, limits)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Set, Callable, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from viralify_diagrams.core.diagram import Diagram, Node, Edge


class ElementShape(str, Enum):
    """Standard shapes for template elements"""
    RECTANGLE = "rectangle"
    ROUNDED = "rounded"
    CIRCLE = "circle"
    ELLIPSE = "ellipse"
    DIAMOND = "diamond"
    HEXAGON = "hexagon"
    CYLINDER = "cylinder"
    CLOUD = "cloud"
    DOCUMENT = "document"
    PARALLELOGRAM = "parallelogram"
    TRAPEZOID = "trapezoid"
    ACTOR = "actor"              # UML actor (stick figure)
    LIFELINE = "lifeline"        # UML sequence lifeline
    PACKAGE = "package"          # UML package
    COMPONENT = "component"      # UML component
    NODE = "node"                # UML deployment node
    ARTIFACT = "artifact"        # UML artifact
    DATABASE = "database"        # Cylinder variant
    QUEUE = "queue"              # Message queue
    FOLDER = "folder"
    FILE = "file"
    BROWSER = "browser"
    MOBILE = "mobile"
    SERVER = "server"
    CONTAINER = "container"      # Docker-like container
    POD = "pod"                  # Kubernetes pod


@dataclass
class TemplateElement:
    """Definition of an element type in a template"""
    id: str
    name: str
    description: str
    shape: ElementShape
    default_icon: Optional[str] = None      # Icon path
    default_color: Optional[str] = None     # Fill color
    default_stroke: Optional[str] = None    # Stroke color
    min_width: int = 100
    min_height: int = 60
    required_fields: List[str] = field(default_factory=list)  # Required properties
    optional_fields: List[str] = field(default_factory=list)  # Optional properties
    max_instances: Optional[int] = None     # Max elements of this type
    allow_nesting: bool = False             # Can contain other elements
    nested_types: List[str] = field(default_factory=list)  # Allowed nested element types

    def validate_properties(self, properties: Dict[str, Any]) -> List[str]:
        """Validate element properties"""
        errors = []
        for req_field in self.required_fields:
            if req_field not in properties or not properties[req_field]:
                errors.append(f"Missing required field: {req_field}")
        return errors


class RelationType(str, Enum):
    """Types of relationships between elements"""
    # General
    USES = "uses"
    CALLS = "calls"
    DEPENDS_ON = "depends_on"
    CONNECTS_TO = "connects_to"

    # Data flow
    READS_FROM = "reads_from"
    WRITES_TO = "writes_to"
    SENDS_TO = "sends_to"
    RECEIVES_FROM = "receives_from"

    # UML
    INHERITS = "inherits"
    IMPLEMENTS = "implements"
    ASSOCIATION = "association"
    AGGREGATION = "aggregation"
    COMPOSITION = "composition"
    DEPENDENCY = "dependency"
    REALIZATION = "realization"

    # Sequence
    SYNC_CALL = "sync_call"
    ASYNC_CALL = "async_call"
    RETURN = "return"
    CREATE = "create"
    DESTROY = "destroy"

    # Process
    FLOW = "flow"
    CONDITIONAL = "conditional"
    PARALLEL = "parallel"

    # Security
    TRUST_BOUNDARY = "trust_boundary"
    THREAT = "threat"
    MITIGATION = "mitigation"


@dataclass
class TemplateRelation:
    """Definition of a relation type in a template"""
    id: str
    name: str
    relation_type: RelationType
    description: str

    # Constraints
    allowed_source_types: List[str] = field(default_factory=list)
    allowed_target_types: List[str] = field(default_factory=list)
    bidirectional: bool = False
    required: bool = False
    max_instances: Optional[int] = None

    # Visual
    line_style: str = "solid"     # solid, dashed, dotted
    line_color: Optional[str] = None
    arrow_style: str = "open"     # open, filled, diamond, triangle
    label_required: bool = False


@dataclass
class TemplateConstraint:
    """A validation constraint for the template"""
    id: str
    name: str
    description: str
    validator: Callable[['Diagram'], List[str]]  # Returns list of error messages
    severity: str = "error"       # error, warning, info


@dataclass
class TemplateConfig:
    """Configuration for a diagram template"""
    # Identification
    template_id: str
    name: str
    description: str
    version: str = "1.0.0"

    # Categorization
    domain: str = "architecture"
    category: str = "general"
    diagram_type: str = "generic"

    # Elements and relations
    elements: List[TemplateElement] = field(default_factory=list)
    relations: List[TemplateRelation] = field(default_factory=list)
    constraints: List[TemplateConstraint] = field(default_factory=list)

    # Layout
    default_layout: str = "graphviz"
    layout_options: Dict[str, Any] = field(default_factory=dict)

    # Limits
    max_elements: int = 20
    max_relations: int = 50
    max_nesting_depth: int = 3

    # Visual
    default_theme: str = "corporate"
    icon_set: str = "generic"  # aws, gcp, azure, k8s, generic

    # Enterprise settings
    require_legend: bool = True
    require_title: bool = True
    allow_orphan_elements: bool = False


@dataclass
class ValidationResult:
    """Result of template validation"""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)

    def add_error(self, message: str):
        self.errors.append(message)
        self.is_valid = False

    def add_warning(self, message: str):
        self.warnings.append(message)

    def add_info(self, message: str):
        self.info.append(message)

    def merge(self, other: 'ValidationResult'):
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.info.extend(other.info)
        if other.errors:
            self.is_valid = False


class DiagramTemplate(ABC):
    """
    Abstract base class for diagram templates.

    Templates define:
    - What elements are allowed
    - What relationships are valid
    - Validation constraints
    - Default styling and layout

    Example implementation:
        class C4ContextTemplate(DiagramTemplate):
            def __init__(self):
                super().__init__(self._build_config())

            def _build_config(self) -> TemplateConfig:
                return TemplateConfig(
                    template_id="c4_context",
                    name="C4 Context Diagram",
                    ...
                )
    """

    def __init__(self, config: TemplateConfig):
        self.config = config
        self._element_map: Dict[str, TemplateElement] = {
            e.id: e for e in config.elements
        }
        self._relation_map: Dict[str, TemplateRelation] = {
            r.id: r for r in config.relations
        }

    @property
    def template_id(self) -> str:
        return self.config.template_id

    @property
    def name(self) -> str:
        return self.config.name

    @abstractmethod
    def create_element(
        self,
        element_type: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a diagram element from template.

        Args:
            element_type: Type of element (from template)
            label: Display label
            properties: Additional properties

        Returns:
            Element definition dict for Diagram.add_node()
        """
        pass

    @abstractmethod
    def create_relation(
        self,
        relation_type: str,
        source_id: str,
        target_id: str,
        label: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a relation from template.

        Args:
            relation_type: Type of relation (from template)
            source_id: Source element ID
            target_id: Target element ID
            label: Optional relation label
            properties: Additional properties

        Returns:
            Relation definition dict for Diagram.add_edge()
        """
        pass

    def validate(self, diagram: 'Diagram') -> ValidationResult:
        """
        Validate a diagram against this template.

        Args:
            diagram: The diagram to validate

        Returns:
            ValidationResult with errors, warnings, and info
        """
        result = ValidationResult(is_valid=True)

        # Check element limits
        if len(diagram.nodes) > self.config.max_elements:
            result.add_error(
                f"Too many elements: {len(diagram.nodes)} (max: {self.config.max_elements})"
            )

        # Check relation limits
        if len(diagram.edges) > self.config.max_relations:
            result.add_error(
                f"Too many relations: {len(diagram.edges)} (max: {self.config.max_relations})"
            )

        # Validate element types
        result.merge(self._validate_elements(diagram))

        # Validate relations
        result.merge(self._validate_relations(diagram))

        # Run custom constraints
        for constraint in self.config.constraints:
            errors = constraint.validator(diagram)
            for error in errors:
                if constraint.severity == "error":
                    result.add_error(error)
                elif constraint.severity == "warning":
                    result.add_warning(error)
                else:
                    result.add_info(error)

        # Check for orphan elements
        if not self.config.allow_orphan_elements:
            orphans = self._find_orphan_elements(diagram)
            for orphan in orphans:
                result.add_warning(f"Orphan element (no connections): {orphan}")

        return result

    def _validate_elements(self, diagram: 'Diagram') -> ValidationResult:
        """Validate all elements in the diagram"""
        result = ValidationResult(is_valid=True)
        element_counts: Dict[str, int] = {}

        for node in diagram.nodes:
            # Check if element type is allowed
            element_type = getattr(node, 'element_type', None)
            if element_type:
                if element_type not in self._element_map:
                    result.add_error(f"Unknown element type: {element_type}")
                    continue

                template_element = self._element_map[element_type]

                # Count instances
                element_counts[element_type] = element_counts.get(element_type, 0) + 1

                # Check max instances
                if template_element.max_instances:
                    if element_counts[element_type] > template_element.max_instances:
                        result.add_error(
                            f"Too many {element_type} elements (max: {template_element.max_instances})"
                        )

                # Validate required properties
                node_props = getattr(node, 'properties', {})
                prop_errors = template_element.validate_properties(node_props)
                for error in prop_errors:
                    result.add_error(f"Element '{node.label}': {error}")

        return result

    def _validate_relations(self, diagram: 'Diagram') -> ValidationResult:
        """Validate all relations in the diagram"""
        result = ValidationResult(is_valid=True)

        # Build element type map
        element_types: Dict[str, str] = {}
        for node in diagram.nodes:
            element_types[node.id] = getattr(node, 'element_type', 'unknown')

        for edge in diagram.edges:
            # Check if relation type is allowed
            relation_type = getattr(edge, 'relation_type', None)
            if relation_type and relation_type in self._relation_map:
                template_relation = self._relation_map[relation_type]

                # Check source type constraint
                source_type = element_types.get(edge.source)
                if template_relation.allowed_source_types:
                    if source_type not in template_relation.allowed_source_types:
                        result.add_error(
                            f"Invalid source type for {relation_type}: {source_type}"
                        )

                # Check target type constraint
                target_type = element_types.get(edge.target)
                if template_relation.allowed_target_types:
                    if target_type not in template_relation.allowed_target_types:
                        result.add_error(
                            f"Invalid target type for {relation_type}: {target_type}"
                        )

                # Check label requirement
                if template_relation.label_required and not edge.label:
                    result.add_warning(
                        f"Relation {edge.source} -> {edge.target} should have a label"
                    )

        return result

    def _find_orphan_elements(self, diagram: 'Diagram') -> List[str]:
        """Find elements with no connections"""
        connected = set()
        for edge in diagram.edges:
            connected.add(edge.source)
            connected.add(edge.target)

        orphans = []
        for node in diagram.nodes:
            if node.id not in connected:
                orphans.append(node.label)

        return orphans

    def get_element_types(self) -> List[str]:
        """Get all allowed element types"""
        return list(self._element_map.keys())

    def get_relation_types(self) -> List[str]:
        """Get all allowed relation types"""
        return list(self._relation_map.keys())

    def get_element_definition(self, element_type: str) -> Optional[TemplateElement]:
        """Get element definition by type"""
        return self._element_map.get(element_type)

    def get_relation_definition(self, relation_type: str) -> Optional[TemplateRelation]:
        """Get relation definition by type"""
        return self._relation_map.get(relation_type)

    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary"""
        return {
            "template_id": self.config.template_id,
            "name": self.config.name,
            "description": self.config.description,
            "version": self.config.version,
            "domain": self.config.domain,
            "category": self.config.category,
            "diagram_type": self.config.diagram_type,
            "elements": [
                {
                    "id": e.id,
                    "name": e.name,
                    "shape": e.shape.value,
                    "description": e.description,
                }
                for e in self.config.elements
            ],
            "relations": [
                {
                    "id": r.id,
                    "name": r.name,
                    "type": r.relation_type.value,
                    "description": r.description,
                }
                for r in self.config.relations
            ],
            "max_elements": self.config.max_elements,
            "default_layout": self.config.default_layout,
            "default_theme": self.config.default_theme,
        }
