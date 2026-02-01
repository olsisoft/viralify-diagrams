"""
BPMN Process Diagram Template

Business Process Model and Notation (BPMN 2.0):
- Events (start, intermediate, end)
- Activities (tasks, sub-processes)
- Gateways (exclusive, parallel, inclusive)
- Swimlanes (pools, lanes)
- Artifacts (data objects, annotations)
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
# BPMN Elements
# =============================================================================

# Events
BPMN_START_EVENT = TemplateElement(
    id="start_event",
    name="Start Event",
    description="Process start point",
    shape=ElementShape.CIRCLE,
    default_color="#FFFFFF",
    default_stroke="#059669",
    required_fields=[],
    optional_fields=["trigger"],
    max_instances=1,
)

BPMN_END_EVENT = TemplateElement(
    id="end_event",
    name="End Event",
    description="Process end point",
    shape=ElementShape.CIRCLE,
    default_color="#FFFFFF",
    default_stroke="#DC2626",
    required_fields=[],
    optional_fields=["result"],
)

BPMN_INTERMEDIATE_EVENT = TemplateElement(
    id="intermediate_event",
    name="Intermediate Event",
    description="Event during process execution",
    shape=ElementShape.CIRCLE,
    default_color="#FFFFFF",
    default_stroke="#D97706",
    required_fields=["name"],
    optional_fields=["trigger", "catching"],
)

BPMN_TIMER_EVENT = TemplateElement(
    id="timer_event",
    name="Timer Event",
    description="Time-based trigger",
    shape=ElementShape.CIRCLE,
    default_color="#FFFFFF",
    default_stroke="#0066CC",
    required_fields=["name"],
    optional_fields=["duration", "date", "cycle"],
)

BPMN_MESSAGE_EVENT = TemplateElement(
    id="message_event",
    name="Message Event",
    description="Message trigger",
    shape=ElementShape.CIRCLE,
    default_color="#FFFFFF",
    default_stroke="#6A5ACD",
    required_fields=["name"],
    optional_fields=["message"],
)

# Activities
BPMN_TASK = TemplateElement(
    id="task",
    name="Task",
    description="Atomic activity",
    shape=ElementShape.ROUNDED,
    default_color="#E6F3FF",
    default_stroke="#0066CC",
    required_fields=["name"],
    optional_fields=["description", "performer"],
)

BPMN_USER_TASK = TemplateElement(
    id="user_task",
    name="User Task",
    description="Task performed by human",
    shape=ElementShape.ROUNDED,
    default_color="#E6F3FF",
    default_stroke="#0066CC",
    required_fields=["name"],
    optional_fields=["assignee", "form"],
)

BPMN_SERVICE_TASK = TemplateElement(
    id="service_task",
    name="Service Task",
    description="Automated service task",
    shape=ElementShape.ROUNDED,
    default_color="#E6FFE6",
    default_stroke="#059669",
    required_fields=["name"],
    optional_fields=["implementation", "service"],
)

BPMN_SCRIPT_TASK = TemplateElement(
    id="script_task",
    name="Script Task",
    description="Script execution task",
    shape=ElementShape.ROUNDED,
    default_color="#FFE6CC",
    default_stroke="#D97706",
    required_fields=["name"],
    optional_fields=["script_format", "script"],
)

BPMN_SUBPROCESS = TemplateElement(
    id="subprocess",
    name="Sub-Process",
    description="Composite activity",
    shape=ElementShape.ROUNDED,
    default_color="#F5F5F5",
    default_stroke="#666666",
    required_fields=["name"],
    allow_nesting=True,
    nested_types=["task", "user_task", "service_task", "gateway", "event"],
)

BPMN_CALL_ACTIVITY = TemplateElement(
    id="call_activity",
    name="Call Activity",
    description="Invokes another process",
    shape=ElementShape.ROUNDED,
    default_color="#E6E6FA",
    default_stroke="#6A5ACD",
    required_fields=["name", "called_element"],
)

# Gateways
BPMN_EXCLUSIVE_GATEWAY = TemplateElement(
    id="exclusive_gateway",
    name="Exclusive Gateway (XOR)",
    description="Only one path taken",
    shape=ElementShape.DIAMOND,
    default_color="#FFFFFF",
    default_stroke="#333333",
    required_fields=[],
    optional_fields=["default"],
)

BPMN_PARALLEL_GATEWAY = TemplateElement(
    id="parallel_gateway",
    name="Parallel Gateway (AND)",
    description="All paths taken simultaneously",
    shape=ElementShape.DIAMOND,
    default_color="#FFFFFF",
    default_stroke="#333333",
    required_fields=[],
)

BPMN_INCLUSIVE_GATEWAY = TemplateElement(
    id="inclusive_gateway",
    name="Inclusive Gateway (OR)",
    description="One or more paths taken",
    shape=ElementShape.DIAMOND,
    default_color="#FFFFFF",
    default_stroke="#333333",
    required_fields=[],
)

BPMN_EVENT_GATEWAY = TemplateElement(
    id="event_gateway",
    name="Event-Based Gateway",
    description="Path based on event",
    shape=ElementShape.DIAMOND,
    default_color="#FFFFFF",
    default_stroke="#333333",
    required_fields=[],
)

# Swimlanes
BPMN_POOL = TemplateElement(
    id="pool",
    name="Pool",
    description="Participant (organization, system)",
    shape=ElementShape.RECTANGLE,
    default_color="#FFFFFF",
    default_stroke="#0066CC",
    required_fields=["name"],
    allow_nesting=True,
    nested_types=["lane", "task", "gateway", "event", "subprocess"],
)

BPMN_LANE = TemplateElement(
    id="lane",
    name="Lane",
    description="Role or department within pool",
    shape=ElementShape.RECTANGLE,
    default_color="#FAFAFA",
    default_stroke="#CCCCCC",
    required_fields=["name"],
    allow_nesting=True,
    nested_types=["task", "gateway", "event"],
)

# Artifacts
BPMN_DATA_OBJECT = TemplateElement(
    id="data_object",
    name="Data Object",
    description="Data used or produced",
    shape=ElementShape.FILE,
    default_color="#FFFACD",
    default_stroke="#B8860B",
    required_fields=["name"],
    optional_fields=["state"],
)

BPMN_DATA_STORE = TemplateElement(
    id="data_store",
    name="Data Store",
    description="Persistent data storage",
    shape=ElementShape.CYLINDER,
    default_color="#E8E8E8",
    default_stroke="#666666",
    required_fields=["name"],
)

BPMN_ANNOTATION = TemplateElement(
    id="annotation",
    name="Text Annotation",
    description="Additional information",
    shape=ElementShape.DOCUMENT,
    default_color="#FFFFE0",
    default_stroke="#DAA520",
    required_fields=["text"],
)


# =============================================================================
# BPMN Relations
# =============================================================================

BPMN_SEQUENCE_FLOW = TemplateRelation(
    id="sequence_flow",
    name="Sequence Flow",
    relation_type=RelationType.FLOW,
    description="Order of activities",
    line_style="solid",
    arrow_style="filled",
)

BPMN_CONDITIONAL_FLOW = TemplateRelation(
    id="conditional_flow",
    name="Conditional Flow",
    relation_type=RelationType.CONDITIONAL,
    description="Flow with condition",
    line_style="solid",
    arrow_style="filled",
    label_required=True,
)

BPMN_DEFAULT_FLOW = TemplateRelation(
    id="default_flow",
    name="Default Flow",
    relation_type=RelationType.FLOW,
    description="Default path from gateway",
    line_style="solid",
    arrow_style="filled",
)

BPMN_MESSAGE_FLOW = TemplateRelation(
    id="message_flow",
    name="Message Flow",
    relation_type=RelationType.SENDS_TO,
    description="Message between pools",
    line_style="dashed",
    arrow_style="open",
)

BPMN_ASSOCIATION = TemplateRelation(
    id="association",
    name="Association",
    relation_type=RelationType.ASSOCIATION,
    description="Links artifact to element",
    line_style="dotted",
    arrow_style="none",
)

BPMN_DATA_ASSOCIATION = TemplateRelation(
    id="data_association",
    name="Data Association",
    relation_type=RelationType.FLOW,
    description="Data input/output",
    line_style="dotted",
    arrow_style="open",
)


# =============================================================================
# BPMN Template
# =============================================================================

class BPMNProcessTemplate(DiagramTemplate):
    """
    BPMN Process Diagram Template.

    Business Process Model and Notation 2.0.

    Diagram types:
    - Collaboration: Multiple pools with message flows
    - Process: Single pool with lanes
    - Choreography: Message exchanges between participants

    Best practices:
    - Use pools for participants
    - Use lanes for roles/departments
    - Label all sequence flows from gateways
    - Include error handling
    - Keep processes to 15-20 activities
    """

    def __init__(self):
        config = TemplateConfig(
            template_id="bpmn_process",
            name="BPMN Process Diagram",
            description="Business Process Model and Notation diagram",
            version="1.0.0",
            domain="business",
            category="business_process",
            diagram_type="bpmn_process",
            elements=[
                BPMN_START_EVENT,
                BPMN_END_EVENT,
                BPMN_INTERMEDIATE_EVENT,
                BPMN_TIMER_EVENT,
                BPMN_MESSAGE_EVENT,
                BPMN_TASK,
                BPMN_USER_TASK,
                BPMN_SERVICE_TASK,
                BPMN_SCRIPT_TASK,
                BPMN_SUBPROCESS,
                BPMN_CALL_ACTIVITY,
                BPMN_EXCLUSIVE_GATEWAY,
                BPMN_PARALLEL_GATEWAY,
                BPMN_INCLUSIVE_GATEWAY,
                BPMN_EVENT_GATEWAY,
                BPMN_POOL,
                BPMN_LANE,
                BPMN_DATA_OBJECT,
                BPMN_DATA_STORE,
                BPMN_ANNOTATION,
            ],
            relations=[
                BPMN_SEQUENCE_FLOW,
                BPMN_CONDITIONAL_FLOW,
                BPMN_DEFAULT_FLOW,
                BPMN_MESSAGE_FLOW,
                BPMN_ASSOCIATION,
                BPMN_DATA_ASSOCIATION,
            ],
            constraints=[
                TemplateConstraint(
                    id="has_start",
                    name="Has Start Event",
                    description="Process should have a start event",
                    validator=lambda d: self._validate_has_start(d),
                    severity="warning",
                ),
                TemplateConstraint(
                    id="has_end",
                    name="Has End Event",
                    description="Process should have an end event",
                    validator=lambda d: self._validate_has_end(d),
                    severity="warning",
                ),
                TemplateConstraint(
                    id="gateway_flows_labeled",
                    name="Gateway Flows Labeled",
                    description="Flows from exclusive gateways should be labeled",
                    validator=lambda d: self._validate_gateway_labels(d),
                    severity="warning",
                ),
                TemplateConstraint(
                    id="parallel_balance",
                    name="Parallel Gateway Balance",
                    description="Parallel split should have join",
                    validator=lambda d: self._validate_parallel_balance(d),
                    severity="warning",
                ),
            ],
            max_elements=40,
            max_relations=60,
            default_layout="horizontal",
            default_theme="corporate",
        )
        super().__init__(config)

    def _validate_has_start(self, diagram) -> List[str]:
        """Validate process has start event"""
        has_start = any(getattr(n, 'element_type', '') == 'start_event'
                       for n in diagram.nodes)
        if not has_start:
            return ["Process should have a start event"]
        return []

    def _validate_has_end(self, diagram) -> List[str]:
        """Validate process has end event"""
        has_end = any(getattr(n, 'element_type', '') == 'end_event'
                     for n in diagram.nodes)
        if not has_end:
            return ["Process should have an end event"]
        return []

    def _validate_gateway_labels(self, diagram) -> List[str]:
        """Validate flows from exclusive gateways are labeled"""
        exclusive_gateways = [n.id for n in diagram.nodes
                            if getattr(n, 'element_type', '') == 'exclusive_gateway']

        unlabeled = []
        for gw_id in exclusive_gateways:
            outgoing = [e for e in diagram.edges if e.source == gw_id]
            for edge in outgoing:
                if not edge.label:
                    unlabeled.append(f"{gw_id} -> {edge.target}")

        if unlabeled:
            return [f"Unlabeled flows from gateways: {', '.join(unlabeled[:3])}"]
        return []

    def _validate_parallel_balance(self, diagram) -> List[str]:
        """Validate parallel gateways are balanced"""
        parallel_count = sum(1 for n in diagram.nodes
                           if getattr(n, 'element_type', '') == 'parallel_gateway')

        if parallel_count % 2 != 0:
            return ["Unbalanced parallel gateways (split without join)"]
        return []

    def create_element(
        self,
        element_type: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a BPMN element"""
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
        if element_type in ["start_event", "intermediate_event", "message_event"]:
            element["trigger"] = props.get("trigger")

        elif element_type == "timer_event":
            element["duration"] = props.get("duration")
            element["date"] = props.get("date")
            element["cycle"] = props.get("cycle")

        elif element_type in ["task", "user_task", "service_task", "script_task"]:
            element["performer"] = props.get("performer")
            element["description"] = props.get("description")

        elif element_type == "user_task":
            element["assignee"] = props.get("assignee")
            element["form"] = props.get("form")

        elif element_type == "service_task":
            element["implementation"] = props.get("implementation")
            element["service"] = props.get("service")

        elif element_type == "call_activity":
            element["called_element"] = props.get("called_element")

        elif element_type == "exclusive_gateway":
            element["default"] = props.get("default")

        elif element_type == "data_object":
            element["state"] = props.get("state")

        return element

    def create_relation(
        self,
        relation_type: str,
        source_id: str,
        target_id: str,
        label: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a BPMN relation"""
        relation_def = self.get_relation_definition(relation_type)
        if not relation_def:
            relation_def = BPMN_SEQUENCE_FLOW

        props = properties or {}

        return {
            "source": source_id,
            "target": target_id,
            "label": label or props.get("condition", ""),
            "relation_type": relation_type,
            "line_style": relation_def.line_style,
            "arrow_style": relation_def.arrow_style,
            "condition": props.get("condition"),
            "is_default": props.get("is_default", False),
            "properties": props,
        }
