"""
UML Class Diagram Template

Standard UML 2.5 class diagram for object-oriented design:
- Classes with attributes and methods
- Interfaces
- Abstract classes
- Relationships: inheritance, composition, aggregation, association
"""

from typing import Dict, Optional, Any, List

from viralify_diagrams.templates.base import (
    DiagramTemplate,
    TemplateConfig,
    TemplateElement,
    TemplateRelation,
    TemplateConstraint,
    ElementShape,
    RelationType,
)


# =============================================================================
# UML Class Elements
# =============================================================================

UML_CLASS = TemplateElement(
    id="class",
    name="Class",
    description="A UML class with name, attributes, and methods",
    shape=ElementShape.RECTANGLE,
    default_color="#FFFACD",  # Light yellow
    default_stroke="#B8860B",
    required_fields=["name"],
    optional_fields=["attributes", "methods", "visibility", "stereotype"],
)

UML_INTERFACE = TemplateElement(
    id="interface",
    name="Interface",
    description="A UML interface (contract)",
    shape=ElementShape.RECTANGLE,
    default_color="#E6E6FA",  # Lavender
    default_stroke="#6A5ACD",
    required_fields=["name"],
    optional_fields=["methods", "stereotype"],
)

UML_ABSTRACT_CLASS = TemplateElement(
    id="abstract_class",
    name="Abstract Class",
    description="An abstract class that cannot be instantiated",
    shape=ElementShape.RECTANGLE,
    default_color="#FFE4E1",  # Misty rose
    default_stroke="#CD5C5C",
    required_fields=["name"],
    optional_fields=["attributes", "methods", "abstract_methods"],
)

UML_ENUM = TemplateElement(
    id="enum",
    name="Enumeration",
    description="An enumeration type with constants",
    shape=ElementShape.RECTANGLE,
    default_color="#E0FFFF",  # Light cyan
    default_stroke="#008B8B",
    required_fields=["name", "values"],
    optional_fields=["stereotype"],
)

UML_PACKAGE = TemplateElement(
    id="package",
    name="Package",
    description="A package containing classes",
    shape=ElementShape.PACKAGE,
    default_color="#F5F5F5",
    default_stroke="#696969",
    required_fields=["name"],
    allow_nesting=True,
    nested_types=["class", "interface", "abstract_class", "enum", "package"],
)

UML_NOTE = TemplateElement(
    id="note",
    name="Note",
    description="A UML note/comment",
    shape=ElementShape.DOCUMENT,
    default_color="#FFFFE0",  # Light yellow
    default_stroke="#DAA520",
    required_fields=["text"],
)


# =============================================================================
# UML Class Relations
# =============================================================================

UML_INHERITANCE = TemplateRelation(
    id="inherits",
    name="Inheritance",
    relation_type=RelationType.INHERITS,
    description="Class extends another class",
    line_style="solid",
    arrow_style="triangle",
)

UML_IMPLEMENTS = TemplateRelation(
    id="implements",
    name="Implements",
    relation_type=RelationType.IMPLEMENTS,
    description="Class implements an interface",
    line_style="dashed",
    arrow_style="triangle",
    allowed_target_types=["interface"],
)

UML_ASSOCIATION = TemplateRelation(
    id="association",
    name="Association",
    relation_type=RelationType.ASSOCIATION,
    description="Association between classes",
    line_style="solid",
    arrow_style="open",
    bidirectional=True,
)

UML_AGGREGATION = TemplateRelation(
    id="aggregation",
    name="Aggregation",
    relation_type=RelationType.AGGREGATION,
    description="Whole-part relationship (can exist independently)",
    line_style="solid",
    arrow_style="diamond",
)

UML_COMPOSITION = TemplateRelation(
    id="composition",
    name="Composition",
    relation_type=RelationType.COMPOSITION,
    description="Strong ownership (part cannot exist without whole)",
    line_style="solid",
    arrow_style="filled_diamond",
)

UML_DEPENDENCY = TemplateRelation(
    id="dependency",
    name="Dependency",
    relation_type=RelationType.DEPENDENCY,
    description="Uses or depends on another class",
    line_style="dashed",
    arrow_style="open",
)


# =============================================================================
# UML Class Template
# =============================================================================

class UMLClassTemplate(DiagramTemplate):
    """
    UML Class Diagram Template.

    Shows the static structure of a system with classes,
    interfaces, and their relationships.

    Best practices:
    - Group related classes in packages
    - Show only essential attributes/methods
    - Use proper UML notation for visibility (+, -, #, ~)
    - Limit diagram to 10-15 classes for readability
    """

    def __init__(self):
        config = TemplateConfig(
            template_id="uml_class",
            name="UML Class Diagram",
            description="Object-oriented class structure diagram",
            version="1.0.0",
            domain="development",
            category="uml_structural",
            diagram_type="uml_class",
            elements=[
                UML_CLASS,
                UML_INTERFACE,
                UML_ABSTRACT_CLASS,
                UML_ENUM,
                UML_PACKAGE,
                UML_NOTE,
            ],
            relations=[
                UML_INHERITANCE,
                UML_IMPLEMENTS,
                UML_ASSOCIATION,
                UML_AGGREGATION,
                UML_COMPOSITION,
                UML_DEPENDENCY,
            ],
            constraints=[
                TemplateConstraint(
                    id="no_self_inheritance",
                    name="No Self Inheritance",
                    description="A class cannot inherit from itself",
                    validator=lambda d: self._validate_no_self_inheritance(d),
                    severity="error",
                ),
                TemplateConstraint(
                    id="interface_no_attributes",
                    name="Interface No Attributes",
                    description="Interfaces should not have attributes (Java style)",
                    validator=lambda d: self._validate_interface_attributes(d),
                    severity="warning",
                ),
            ],
            max_elements=25,
            max_relations=50,
            default_layout="graphviz",
            default_theme="corporate",
        )
        super().__init__(config)

    def _validate_no_self_inheritance(self, diagram) -> List[str]:
        """Validate no class inherits from itself"""
        errors = []
        for edge in diagram.edges:
            if edge.source == edge.target:
                rel_type = getattr(edge, 'relation_type', '')
                if rel_type in ['inherits', 'implements']:
                    errors.append(f"Self-inheritance detected: {edge.source}")
        return errors

    def _validate_interface_attributes(self, diagram) -> List[str]:
        """Warn if interfaces have attributes"""
        warnings = []
        for node in diagram.nodes:
            if getattr(node, 'element_type', '') == 'interface':
                props = getattr(node, 'properties', {})
                if props.get('attributes'):
                    warnings.append(f"Interface '{node.label}' has attributes (consider removing)")
        return warnings

    def create_element(
        self,
        element_type: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a UML class element"""
        props = properties or {}

        element_def = self.get_element_definition(element_type)
        if not element_def:
            raise ValueError(f"Unknown element type: {element_type}")

        # Build class compartments
        compartments = []
        if element_type in ["class", "abstract_class"]:
            # Attributes compartment
            if props.get("attributes"):
                compartments.append({
                    "type": "attributes",
                    "items": props["attributes"]
                })
            # Methods compartment
            if props.get("methods"):
                compartments.append({
                    "type": "methods",
                    "items": props["methods"]
                })
        elif element_type == "interface":
            if props.get("methods"):
                compartments.append({
                    "type": "methods",
                    "items": props["methods"]
                })
        elif element_type == "enum":
            if props.get("values"):
                compartments.append({
                    "type": "values",
                    "items": props["values"]
                })

        return {
            "id": props.get("id", label.lower().replace(" ", "_")),
            "label": label,
            "element_type": element_type,
            "shape": element_def.shape.value,
            "fill_color": props.get("color", element_def.default_color),
            "stroke_color": element_def.default_stroke,
            "stereotype": props.get("stereotype"),
            "compartments": compartments,
            "properties": props,
        }

    def create_relation(
        self,
        relation_type: str,
        source_id: str,
        target_id: str,
        label: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a UML class relation"""
        relation_def = self.get_relation_definition(relation_type)
        if not relation_def:
            relation_def = UML_ASSOCIATION

        props = properties or {}

        return {
            "source": source_id,
            "target": target_id,
            "label": label or "",
            "relation_type": relation_type,
            "line_style": relation_def.line_style,
            "arrow_style": relation_def.arrow_style,
            "multiplicity_source": props.get("multiplicity_source"),
            "multiplicity_target": props.get("multiplicity_target"),
            "role_source": props.get("role_source"),
            "role_target": props.get("role_target"),
            "properties": props,
        }
