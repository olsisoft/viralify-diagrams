"""
UML Activity Diagram Template

Standard UML 2.5 activity diagram for workflow modeling:
- Actions and activities
- Control flow (decisions, forks, joins, merges)
- Swimlanes (partitions)
- Object nodes and data flow
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
# UML Activity Elements
# =============================================================================

UML_INITIAL_NODE = TemplateElement(
    id="initial",
    name="Initial Node",
    description="Starting point of the activity",
    shape=ElementShape.CIRCLE,
    default_color="#333333",
    default_stroke="#333333",
    required_fields=[],
    max_instances=1,
)

UML_FINAL_NODE = TemplateElement(
    id="final",
    name="Activity Final Node",
    description="End point of the activity",
    shape=ElementShape.CIRCLE,
    default_color="#333333",
    default_stroke="#333333",
    required_fields=[],
)

UML_FLOW_FINAL = TemplateElement(
    id="flow_final",
    name="Flow Final Node",
    description="End point of a specific flow (not entire activity)",
    shape=ElementShape.CIRCLE,
    default_color="#FFFFFF",
    default_stroke="#333333",
    required_fields=[],
)

UML_ACTION = TemplateElement(
    id="action",
    name="Action",
    description="An atomic action or step",
    shape=ElementShape.ROUNDED,
    default_color="#E6F3FF",
    default_stroke="#0066CC",
    required_fields=["name"],
    optional_fields=["description", "precondition", "postcondition"],
)

UML_CALL_BEHAVIOR = TemplateElement(
    id="call_behavior",
    name="Call Behavior Action",
    description="Invokes another activity",
    shape=ElementShape.ROUNDED,
    default_color="#FFE6CC",
    default_stroke="#D97706",
    required_fields=["name", "behavior"],
)

UML_DECISION = TemplateElement(
    id="decision",
    name="Decision Node",
    description="Conditional branching point",
    shape=ElementShape.DIAMOND,
    default_color="#FFFFFF",
    default_stroke="#333333",
    required_fields=[],
)

UML_MERGE = TemplateElement(
    id="merge",
    name="Merge Node",
    description="Merges multiple flows into one",
    shape=ElementShape.DIAMOND,
    default_color="#FFFFFF",
    default_stroke="#333333",
    required_fields=[],
)

UML_FORK = TemplateElement(
    id="fork",
    name="Fork Node",
    description="Splits flow into concurrent paths",
    shape=ElementShape.RECTANGLE,
    default_color="#333333",
    default_stroke="#333333",
    required_fields=[],
)

UML_JOIN = TemplateElement(
    id="join",
    name="Join Node",
    description="Synchronizes concurrent paths",
    shape=ElementShape.RECTANGLE,
    default_color="#333333",
    default_stroke="#333333",
    required_fields=[],
)

UML_SWIMLANE = TemplateElement(
    id="swimlane",
    name="Swimlane (Partition)",
    description="Groups actions by actor or system",
    shape=ElementShape.RECTANGLE,
    default_color="#FAFAFA",
    default_stroke="#CCCCCC",
    required_fields=["name"],
    allow_nesting=True,
    nested_types=["action", "decision", "merge", "fork", "join", "call_behavior"],
)

UML_OBJECT_NODE = TemplateElement(
    id="object_node",
    name="Object Node",
    description="Data object in the flow",
    shape=ElementShape.RECTANGLE,
    default_color="#FFFACD",
    default_stroke="#B8860B",
    required_fields=["name"],
    optional_fields=["type", "state"],
)

UML_DATASTORE = TemplateElement(
    id="datastore",
    name="Data Store",
    description="Persistent data storage",
    shape=ElementShape.CYLINDER,
    default_color="#E8E8E8",
    default_stroke="#666666",
    required_fields=["name"],
)

UML_SIGNAL_SEND = TemplateElement(
    id="signal_send",
    name="Send Signal",
    description="Sends a signal/event",
    shape=ElementShape.PARALLELOGRAM,
    default_color="#E6FFE6",
    default_stroke="#059669",
    required_fields=["signal"],
)

UML_SIGNAL_RECEIVE = TemplateElement(
    id="signal_receive",
    name="Receive Signal",
    description="Waits for a signal/event",
    shape=ElementShape.PARALLELOGRAM,
    default_color="#FFF0F5",
    default_stroke="#DC2626",
    required_fields=["signal"],
)

UML_TIME_EVENT = TemplateElement(
    id="time_event",
    name="Time Event",
    description="Triggered by time",
    shape=ElementShape.HEXAGON,
    default_color="#FFFFFF",
    default_stroke="#333333",
    required_fields=["expression"],
)


# =============================================================================
# UML Activity Relations
# =============================================================================

UML_CONTROL_FLOW = TemplateRelation(
    id="flow",
    name="Control Flow",
    relation_type=RelationType.FLOW,
    description="Sequence of actions",
    line_style="solid",
    arrow_style="open",
)

UML_CONDITIONAL_FLOW = TemplateRelation(
    id="conditional",
    name="Conditional Flow",
    relation_type=RelationType.CONDITIONAL,
    description="Flow with guard condition",
    line_style="solid",
    arrow_style="open",
    label_required=True,
)

UML_OBJECT_FLOW = TemplateRelation(
    id="object_flow",
    name="Object Flow",
    relation_type=RelationType.FLOW,
    description="Data flow between actions",
    line_style="solid",
    arrow_style="open",
)

UML_EXCEPTION_FLOW = TemplateRelation(
    id="exception",
    name="Exception Flow",
    relation_type=RelationType.FLOW,
    description="Exception/error handling flow",
    line_style="dashed",
    arrow_style="open",
    line_color="#DC2626",
)


# =============================================================================
# UML Activity Template
# =============================================================================

class UMLActivityTemplate(DiagramTemplate):
    """
    UML Activity Diagram Template.

    Shows the flow of activities and actions in a process.

    Best practices:
    - Use swimlanes to show responsibility
    - Keep decision branches to 2-3 paths
    - Use fork/join for true parallelism
    - Include exception handling flows
    - Limit to 15-20 actions per diagram
    """

    def __init__(self):
        config = TemplateConfig(
            template_id="uml_activity",
            name="UML Activity Diagram",
            description="Workflow and process flow diagram",
            version="1.0.0",
            domain="development",
            category="uml_behavioral",
            diagram_type="uml_activity",
            elements=[
                UML_INITIAL_NODE,
                UML_FINAL_NODE,
                UML_FLOW_FINAL,
                UML_ACTION,
                UML_CALL_BEHAVIOR,
                UML_DECISION,
                UML_MERGE,
                UML_FORK,
                UML_JOIN,
                UML_SWIMLANE,
                UML_OBJECT_NODE,
                UML_DATASTORE,
                UML_SIGNAL_SEND,
                UML_SIGNAL_RECEIVE,
                UML_TIME_EVENT,
            ],
            relations=[
                UML_CONTROL_FLOW,
                UML_CONDITIONAL_FLOW,
                UML_OBJECT_FLOW,
                UML_EXCEPTION_FLOW,
            ],
            constraints=[
                TemplateConstraint(
                    id="has_initial",
                    name="Has Initial Node",
                    description="Activity should have an initial node",
                    validator=lambda d: self._validate_has_initial(d),
                    severity="warning",
                ),
                TemplateConstraint(
                    id="has_final",
                    name="Has Final Node",
                    description="Activity should have a final node",
                    validator=lambda d: self._validate_has_final(d),
                    severity="warning",
                ),
                TemplateConstraint(
                    id="fork_join_balance",
                    name="Fork/Join Balance",
                    description="Each fork should have a corresponding join",
                    validator=lambda d: self._validate_fork_join(d),
                    severity="warning",
                ),
            ],
            max_elements=30,
            max_relations=50,
            default_layout="vertical",
            default_theme="corporate",
        )
        super().__init__(config)

    def _validate_has_initial(self, diagram) -> List[str]:
        """Validate diagram has initial node"""
        has_initial = any(getattr(n, 'element_type', '') == 'initial'
                        for n in diagram.nodes)
        if not has_initial:
            return ["Activity diagram should have an initial node"]
        return []

    def _validate_has_final(self, diagram) -> List[str]:
        """Validate diagram has final node"""
        has_final = any(getattr(n, 'element_type', '') in ['final', 'flow_final']
                       for n in diagram.nodes)
        if not has_final:
            return ["Activity diagram should have a final node"]
        return []

    def _validate_fork_join(self, diagram) -> List[str]:
        """Validate fork/join balance"""
        fork_count = sum(1 for n in diagram.nodes
                        if getattr(n, 'element_type', '') == 'fork')
        join_count = sum(1 for n in diagram.nodes
                        if getattr(n, 'element_type', '') == 'join')
        if fork_count != join_count:
            return [f"Unbalanced fork/join: {fork_count} forks, {join_count} joins"]
        return []

    def create_element(
        self,
        element_type: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a UML activity element"""
        props = properties or {}

        element_def = self.get_element_definition(element_type)
        if not element_def:
            raise ValueError(f"Unknown element type: {element_type}")

        element = {
            "id": props.get("id", label.lower().replace(" ", "_") if label else element_type),
            "label": label,
            "element_type": element_type,
            "shape": element_def.shape.value,
            "fill_color": props.get("color", element_def.default_color),
            "stroke_color": element_def.default_stroke,
            "properties": props,
        }

        # Add type-specific properties
        if element_type == "action":
            element["precondition"] = props.get("precondition")
            element["postcondition"] = props.get("postcondition")
        elif element_type == "call_behavior":
            element["behavior"] = props.get("behavior")
        elif element_type == "object_node":
            element["object_type"] = props.get("type")
            element["state"] = props.get("state")
        elif element_type in ["signal_send", "signal_receive"]:
            element["signal"] = props.get("signal")
        elif element_type == "time_event":
            element["expression"] = props.get("expression")

        return element

    def create_relation(
        self,
        relation_type: str,
        source_id: str,
        target_id: str,
        label: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a UML activity relation"""
        relation_def = self.get_relation_definition(relation_type)
        if not relation_def:
            relation_def = UML_CONTROL_FLOW

        props = properties or {}

        return {
            "source": source_id,
            "target": target_id,
            "label": label or "",
            "relation_type": relation_type,
            "line_style": relation_def.line_style,
            "arrow_style": relation_def.arrow_style,
            "guard": props.get("guard"),  # [condition]
            "weight": props.get("weight"),  # For object flow
            "properties": props,
        }
