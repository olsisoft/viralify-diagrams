"""
Entity Relationship Diagram (ERD) Template

Standard ERD for database modeling:
- Chen notation
- Crow's Foot notation
- IDEF1X notation
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
# ERD Elements
# =============================================================================

ERD_ENTITY = TemplateElement(
    id="entity",
    name="Entity",
    description="A table or entity in the database",
    shape=ElementShape.RECTANGLE,
    default_color="#E6F3FF",
    default_stroke="#0066CC",
    required_fields=["name"],
    optional_fields=["attributes", "primary_key", "description"],
)

ERD_WEAK_ENTITY = TemplateElement(
    id="weak_entity",
    name="Weak Entity",
    description="An entity that depends on another entity",
    shape=ElementShape.RECTANGLE,
    default_color="#FFE6CC",
    default_stroke="#D97706",
    required_fields=["name", "identifying_relationship"],
    optional_fields=["attributes", "partial_key"],
)

ERD_ATTRIBUTE = TemplateElement(
    id="attribute",
    name="Attribute",
    description="An attribute of an entity (Chen notation)",
    shape=ElementShape.ELLIPSE,
    default_color="#FFFFFF",
    default_stroke="#666666",
    required_fields=["name"],
    optional_fields=["type", "is_key", "is_derived", "is_multivalued"],
)

ERD_RELATIONSHIP = TemplateElement(
    id="relationship",
    name="Relationship (as node)",
    description="A relationship between entities (Chen notation)",
    shape=ElementShape.DIAMOND,
    default_color="#E6FFE6",
    default_stroke="#059669",
    required_fields=["name"],
    optional_fields=["attributes"],
)

ERD_IDENTIFYING_RELATIONSHIP = TemplateElement(
    id="identifying_relationship",
    name="Identifying Relationship",
    description="Relationship that identifies a weak entity",
    shape=ElementShape.DIAMOND,
    default_color="#FFF0F5",
    default_stroke="#DC2626",
    required_fields=["name"],
)

ERD_SPECIALIZATION = TemplateElement(
    id="specialization",
    name="Specialization/Generalization",
    description="ISA hierarchy (subtype/supertype)",
    shape=ElementShape.HEXAGON,
    default_color="#E6E6FA",
    default_stroke="#6A5ACD",
    required_fields=["type"],  # total/partial, disjoint/overlapping
)


# =============================================================================
# ERD Relations (Crow's Foot notation)
# =============================================================================

ERD_ONE_TO_ONE = TemplateRelation(
    id="one_to_one",
    name="One-to-One",
    relation_type=RelationType.ASSOCIATION,
    description="1:1 relationship",
    line_style="solid",
    arrow_style="one",
)

ERD_ONE_TO_MANY = TemplateRelation(
    id="one_to_many",
    name="One-to-Many",
    relation_type=RelationType.ASSOCIATION,
    description="1:N relationship",
    line_style="solid",
    arrow_style="crow",
)

ERD_MANY_TO_MANY = TemplateRelation(
    id="many_to_many",
    name="Many-to-Many",
    relation_type=RelationType.ASSOCIATION,
    description="M:N relationship",
    line_style="solid",
    arrow_style="crow_both",
)

ERD_ZERO_OR_ONE = TemplateRelation(
    id="zero_or_one",
    name="Zero or One",
    relation_type=RelationType.ASSOCIATION,
    description="0..1 relationship (optional)",
    line_style="solid",
    arrow_style="circle_one",
)

ERD_ZERO_OR_MANY = TemplateRelation(
    id="zero_or_many",
    name="Zero or Many",
    relation_type=RelationType.ASSOCIATION,
    description="0..* relationship (optional many)",
    line_style="solid",
    arrow_style="circle_crow",
)

ERD_INHERITS = TemplateRelation(
    id="inherits",
    name="Inheritance",
    relation_type=RelationType.INHERITS,
    description="Subtype inherits from supertype",
    line_style="solid",
    arrow_style="triangle",
)

ERD_IDENTIFIES = TemplateRelation(
    id="identifies",
    name="Identifies",
    relation_type=RelationType.DEPENDS_ON,
    description="Identifying relationship for weak entity",
    line_style="solid",
    arrow_style="filled",
)


# =============================================================================
# ERD Template
# =============================================================================

class ERDTemplate(DiagramTemplate):
    """
    Entity Relationship Diagram Template.

    Shows the structure of a database.

    Notations supported:
    - Crow's Foot (default): Popular for database design
    - Chen: Academic notation with relationship diamonds

    Best practices:
    - Use consistent naming (singular or plural)
    - Show primary and foreign keys
    - Include cardinality on all relationships
    - Limit to 10-15 entities per diagram
    """

    def __init__(self):
        config = TemplateConfig(
            template_id="erd",
            name="Entity Relationship Diagram",
            description="Database schema and relationships",
            version="1.0.0",
            domain="data",
            category="data_modeling",
            diagram_type="erd",
            elements=[
                ERD_ENTITY,
                ERD_WEAK_ENTITY,
                ERD_ATTRIBUTE,
                ERD_RELATIONSHIP,
                ERD_IDENTIFYING_RELATIONSHIP,
                ERD_SPECIALIZATION,
            ],
            relations=[
                ERD_ONE_TO_ONE,
                ERD_ONE_TO_MANY,
                ERD_MANY_TO_MANY,
                ERD_ZERO_OR_ONE,
                ERD_ZERO_OR_MANY,
                ERD_INHERITS,
                ERD_IDENTIFIES,
            ],
            constraints=[
                TemplateConstraint(
                    id="entity_has_pk",
                    name="Entity Has Primary Key",
                    description="Entities should have a primary key",
                    validator=lambda d: self._validate_entity_pk(d),
                    severity="warning",
                ),
                TemplateConstraint(
                    id="weak_entity_has_identifying",
                    name="Weak Entity Needs Identifying Relationship",
                    description="Weak entities must have an identifying relationship",
                    validator=lambda d: self._validate_weak_entity(d),
                    severity="error",
                ),
            ],
            max_elements=30,
            max_relations=50,
            default_layout="graphviz",
            default_theme="corporate",
        )
        super().__init__(config)

    def _validate_entity_pk(self, diagram) -> List[str]:
        """Validate entities have primary keys"""
        no_pk = []
        for node in diagram.nodes:
            if getattr(node, 'element_type', '') == 'entity':
                props = getattr(node, 'properties', {})
                if not props.get('primary_key'):
                    no_pk.append(node.label)
        if no_pk:
            return [f"Entities without primary key: {', '.join(no_pk)}"]
        return []

    def _validate_weak_entity(self, diagram) -> List[str]:
        """Validate weak entities have identifying relationships"""
        errors = []
        weak_entities = [n.id for n in diagram.nodes
                        if getattr(n, 'element_type', '') == 'weak_entity']

        for weak_id in weak_entities:
            has_identifying = False
            for edge in diagram.edges:
                if (edge.source == weak_id or edge.target == weak_id):
                    if getattr(edge, 'relation_type', '') == 'identifies':
                        has_identifying = True
                        break
            if not has_identifying:
                errors.append(f"Weak entity '{weak_id}' has no identifying relationship")

        return errors

    def create_element(
        self,
        element_type: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create an ERD element"""
        props = properties or {}

        element_def = self.get_element_definition(element_type)
        if not element_def:
            raise ValueError(f"Unknown element type: {element_type}")

        element = {
            "id": props.get("id", label.lower().replace(" ", "_")),
            "label": label,
            "element_type": element_type,
            "shape": element_def.shape.value,
            "fill_color": props.get("color", element_def.default_color),
            "stroke_color": element_def.default_stroke,
            "properties": props,
        }

        # Add ERD-specific properties
        if element_type in ["entity", "weak_entity"]:
            element["attributes"] = props.get("attributes", [])
            element["primary_key"] = props.get("primary_key")
            element["foreign_keys"] = props.get("foreign_keys", [])

            # Build attribute compartments
            compartments = []
            if props.get("primary_key"):
                compartments.append({
                    "type": "pk",
                    "items": [props["primary_key"]] if isinstance(props["primary_key"], str)
                            else props["primary_key"]
                })
            if props.get("attributes"):
                compartments.append({
                    "type": "attributes",
                    "items": props["attributes"]
                })
            element["compartments"] = compartments

        elif element_type == "attribute":
            element["data_type"] = props.get("type")
            element["is_key"] = props.get("is_key", False)
            element["is_derived"] = props.get("is_derived", False)
            element["is_multivalued"] = props.get("is_multivalued", False)

        elif element_type == "specialization":
            element["specialization_type"] = props.get("type", "partial")
            element["disjointness"] = props.get("disjointness", "disjoint")

        return element

    def create_relation(
        self,
        relation_type: str,
        source_id: str,
        target_id: str,
        label: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create an ERD relationship"""
        relation_def = self.get_relation_definition(relation_type)
        if not relation_def:
            relation_def = ERD_ONE_TO_MANY

        props = properties or {}

        return {
            "source": source_id,
            "target": target_id,
            "label": label or props.get("name", ""),
            "relation_type": relation_type,
            "line_style": relation_def.line_style,
            "arrow_style": relation_def.arrow_style,
            "cardinality_source": props.get("cardinality_source"),
            "cardinality_target": props.get("cardinality_target"),
            "participation_source": props.get("participation_source", "partial"),  # total/partial
            "participation_target": props.get("participation_target", "partial"),
            "verb_phrase": props.get("verb_phrase"),  # e.g., "has", "belongs to"
            "properties": props,
        }

    def create_attribute(
        self,
        name: str,
        data_type: str,
        is_pk: bool = False,
        is_fk: bool = False,
        nullable: bool = True,
        default: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Helper to create an attribute definition.

        Args:
            name: Attribute name
            data_type: SQL data type (VARCHAR, INT, etc.)
            is_pk: Is primary key
            is_fk: Is foreign key
            nullable: Allows NULL
            default: Default value
        """
        return {
            "name": name,
            "type": data_type,
            "is_pk": is_pk,
            "is_fk": is_fk,
            "nullable": nullable,
            "default": default,
        }
