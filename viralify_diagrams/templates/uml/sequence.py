"""
UML Sequence Diagram Template

Standard UML 2.5 sequence diagram for interaction modeling:
- Lifelines (participants)
- Messages (sync, async, return)
- Combined fragments (alt, loop, opt, par)
- Activation boxes
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
# UML Sequence Elements
# =============================================================================

UML_ACTOR_LIFELINE = TemplateElement(
    id="actor",
    name="Actor",
    description="A human actor/user in the sequence",
    shape=ElementShape.ACTOR,
    default_color="#FFFFFF",
    default_stroke="#333333",
    required_fields=["name"],
)

UML_OBJECT_LIFELINE = TemplateElement(
    id="object",
    name="Object Lifeline",
    description="An object/instance participating in the interaction",
    shape=ElementShape.LIFELINE,
    default_color="#E6F3FF",
    default_stroke="#0066CC",
    required_fields=["name"],
    optional_fields=["class_name", "stereotype"],
)

UML_BOUNDARY = TemplateElement(
    id="boundary",
    name="Boundary",
    description="UI or system boundary component",
    shape=ElementShape.LIFELINE,
    default_color="#FFE6CC",
    default_stroke="#D97706",
    required_fields=["name"],
)

UML_CONTROL = TemplateElement(
    id="control",
    name="Control",
    description="Controller or business logic component",
    shape=ElementShape.LIFELINE,
    default_color="#E6FFE6",
    default_stroke="#059669",
    required_fields=["name"],
)

UML_ENTITY = TemplateElement(
    id="entity",
    name="Entity",
    description="Data entity or model component",
    shape=ElementShape.LIFELINE,
    default_color="#FFF0F5",
    default_stroke="#DC2626",
    required_fields=["name"],
)

UML_DATABASE_LIFELINE = TemplateElement(
    id="database",
    name="Database",
    description="A database participant",
    shape=ElementShape.CYLINDER,
    default_color="#E8E8E8",
    default_stroke="#666666",
    required_fields=["name"],
)

UML_FRAGMENT = TemplateElement(
    id="fragment",
    name="Combined Fragment",
    description="A combined fragment (alt, loop, opt, par, etc.)",
    shape=ElementShape.RECTANGLE,
    default_color="#FAFAFA",
    default_stroke="#999999",
    required_fields=["fragment_type"],
    optional_fields=["condition", "label"],
    allow_nesting=True,
)


# =============================================================================
# UML Sequence Relations (Messages)
# =============================================================================

UML_SYNC_MESSAGE = TemplateRelation(
    id="sync_call",
    name="Synchronous Message",
    relation_type=RelationType.SYNC_CALL,
    description="Synchronous call (waits for response)",
    line_style="solid",
    arrow_style="filled",
    label_required=True,
)

UML_ASYNC_MESSAGE = TemplateRelation(
    id="async_call",
    name="Asynchronous Message",
    relation_type=RelationType.ASYNC_CALL,
    description="Asynchronous call (doesn't wait)",
    line_style="solid",
    arrow_style="open",
    label_required=True,
)

UML_RETURN_MESSAGE = TemplateRelation(
    id="return",
    name="Return Message",
    relation_type=RelationType.RETURN,
    description="Return from a call",
    line_style="dashed",
    arrow_style="open",
)

UML_CREATE_MESSAGE = TemplateRelation(
    id="create",
    name="Create Message",
    relation_type=RelationType.CREATE,
    description="Creates a new object",
    line_style="dashed",
    arrow_style="open",
)

UML_DESTROY_MESSAGE = TemplateRelation(
    id="destroy",
    name="Destroy Message",
    relation_type=RelationType.DESTROY,
    description="Destroys an object",
    line_style="solid",
    arrow_style="x",
)

UML_SELF_MESSAGE = TemplateRelation(
    id="self_call",
    name="Self Message",
    relation_type=RelationType.SYNC_CALL,
    description="Object calls itself",
    line_style="solid",
    arrow_style="filled",
)


# =============================================================================
# UML Sequence Template
# =============================================================================

class UMLSequenceTemplate(DiagramTemplate):
    """
    UML Sequence Diagram Template.

    Shows the dynamic interaction between objects over time.

    Best practices:
    - Keep lifelines to 5-8 participants
    - Use combined fragments for conditional logic
    - Show return messages for clarity
    - Number messages if needed for reference
    - Use activation boxes to show processing
    """

    def __init__(self):
        config = TemplateConfig(
            template_id="uml_sequence",
            name="UML Sequence Diagram",
            description="Time-ordered interaction between objects",
            version="1.0.0",
            domain="development",
            category="uml_interaction",
            diagram_type="uml_sequence",
            elements=[
                UML_ACTOR_LIFELINE,
                UML_OBJECT_LIFELINE,
                UML_BOUNDARY,
                UML_CONTROL,
                UML_ENTITY,
                UML_DATABASE_LIFELINE,
                UML_FRAGMENT,
            ],
            relations=[
                UML_SYNC_MESSAGE,
                UML_ASYNC_MESSAGE,
                UML_RETURN_MESSAGE,
                UML_CREATE_MESSAGE,
                UML_DESTROY_MESSAGE,
                UML_SELF_MESSAGE,
            ],
            constraints=[
                TemplateConstraint(
                    id="max_lifelines",
                    name="Maximum Lifelines",
                    description="Limit number of lifelines for readability",
                    validator=lambda d: self._validate_max_lifelines(d),
                    severity="warning",
                ),
                TemplateConstraint(
                    id="message_order",
                    name="Message Order",
                    description="Messages should have sequence numbers",
                    validator=lambda d: self._validate_message_order(d),
                    severity="info",
                ),
            ],
            max_elements=15,
            max_relations=40,
            default_layout="vertical",
            default_theme="corporate",
        )
        super().__init__(config)

    def _validate_max_lifelines(self, diagram) -> List[str]:
        """Warn if too many lifelines"""
        lifeline_count = sum(1 for n in diagram.nodes
                           if getattr(n, 'element_type', '') in
                           ['actor', 'object', 'boundary', 'control', 'entity', 'database'])
        if lifeline_count > 8:
            return [f"Too many lifelines ({lifeline_count}). Consider splitting into multiple diagrams."]
        return []

    def _validate_message_order(self, diagram) -> List[str]:
        """Info if messages don't have sequence numbers"""
        unsequenced = 0
        for edge in diagram.edges:
            props = getattr(edge, 'properties', {})
            if not props.get('sequence_number'):
                unsequenced += 1
        if unsequenced > 0:
            return [f"{unsequenced} messages without sequence numbers"]
        return []

    def create_element(
        self,
        element_type: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a UML sequence element"""
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

        # Add lifeline-specific properties
        if element_type in ["object", "boundary", "control", "entity"]:
            element["class_name"] = props.get("class_name")
            element["stereotype"] = props.get("stereotype")

        # Add fragment-specific properties
        if element_type == "fragment":
            element["fragment_type"] = props.get("fragment_type", "alt")
            element["condition"] = props.get("condition")
            element["operands"] = props.get("operands", [])

        return element

    def create_relation(
        self,
        relation_type: str,
        source_id: str,
        target_id: str,
        label: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a UML sequence message"""
        relation_def = self.get_relation_definition(relation_type)
        if not relation_def:
            relation_def = UML_SYNC_MESSAGE

        props = properties or {}

        return {
            "source": source_id,
            "target": target_id,
            "label": label or props.get("message", ""),
            "relation_type": relation_type,
            "line_style": relation_def.line_style,
            "arrow_style": relation_def.arrow_style,
            "sequence_number": props.get("sequence_number"),
            "arguments": props.get("arguments"),
            "return_value": props.get("return_value"),
            "guard_condition": props.get("guard_condition"),
            "properties": props,
        }

    def create_fragment(
        self,
        fragment_type: str,
        operands: List[Dict[str, Any]],
        label: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a combined fragment.

        Args:
            fragment_type: alt, opt, loop, par, break, critical, neg, assert
            operands: List of operand dicts with 'condition' and 'messages'
            label: Optional fragment label
        """
        valid_types = ["alt", "opt", "loop", "par", "break", "critical", "neg", "assert"]
        if fragment_type not in valid_types:
            raise ValueError(f"Invalid fragment type: {fragment_type}. Must be one of {valid_types}")

        return {
            "element_type": "fragment",
            "fragment_type": fragment_type,
            "label": label or fragment_type.upper(),
            "operands": operands,
        }
