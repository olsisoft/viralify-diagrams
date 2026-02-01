"""
Data Flow Diagram (DFD) Template

Standard DFD for data-centric system modeling:
- Level 0 (Context Diagram)
- Level 1+ (Detailed processes)
- Gane-Sarson and Yourdon-DeMarco notations
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
# DFD Elements (Gane-Sarson notation by default)
# =============================================================================

DFD_EXTERNAL_ENTITY = TemplateElement(
    id="external_entity",
    name="External Entity",
    description="External system, person, or organization that interacts with the system",
    shape=ElementShape.RECTANGLE,
    default_color="#E6E6E6",
    default_stroke="#666666",
    required_fields=["name"],
    optional_fields=["description", "type"],
)

DFD_PROCESS = TemplateElement(
    id="process",
    name="Process",
    description="A process that transforms data",
    shape=ElementShape.ROUNDED,
    default_color="#E6F3FF",
    default_stroke="#0066CC",
    required_fields=["name", "number"],
    optional_fields=["description", "owner"],
)

DFD_DATA_STORE = TemplateElement(
    id="data_store",
    name="Data Store",
    description="A repository for data at rest",
    shape=ElementShape.RECTANGLE,  # Open-ended rectangle in DFD
    default_color="#FFFACD",
    default_stroke="#B8860B",
    required_fields=["name", "number"],
    optional_fields=["description", "technology"],
)

DFD_DATA_FLOW = TemplateElement(
    id="data_flow_node",
    name="Data Flow (as node)",
    description="Data in transit (rarely used as node)",
    shape=ElementShape.PARALLELOGRAM,
    default_color="#E6FFE6",
    default_stroke="#059669",
    required_fields=["name"],
)

# Alternative: Yourdon-DeMarco notation
DFD_PROCESS_YDM = TemplateElement(
    id="process_ydm",
    name="Process (Yourdon)",
    description="Process in Yourdon-DeMarco notation",
    shape=ElementShape.CIRCLE,
    default_color="#E6F3FF",
    default_stroke="#0066CC",
    required_fields=["name", "number"],
)

DFD_BOUNDARY = TemplateElement(
    id="boundary",
    name="System Boundary",
    description="The boundary of the system being modeled",
    shape=ElementShape.RECTANGLE,
    default_color="#FFFFFF",
    default_stroke="#999999",
    required_fields=["name"],
    allow_nesting=True,
    nested_types=["process", "data_store"],
)


# =============================================================================
# DFD Relations
# =============================================================================

DFD_FLOW = TemplateRelation(
    id="data_flow",
    name="Data Flow",
    relation_type=RelationType.FLOW,
    description="Flow of data between elements",
    line_style="solid",
    arrow_style="open",
    label_required=True,
)

DFD_BIDIRECTIONAL_FLOW = TemplateRelation(
    id="bidirectional_flow",
    name="Bidirectional Data Flow",
    relation_type=RelationType.FLOW,
    description="Two-way data flow",
    line_style="solid",
    arrow_style="both",
    label_required=True,
    bidirectional=True,
)


# =============================================================================
# DFD Template
# =============================================================================

class DFDTemplate(DiagramTemplate):
    """
    Data Flow Diagram Template.

    Shows how data moves through a system.

    Levels:
    - Level 0 (Context): System as single process with external entities
    - Level 1: Major processes and data stores
    - Level 2+: Detailed decomposition

    Best practices:
    - Use consistent numbering (1.0, 1.1, 1.2...)
    - Label all data flows
    - Balance data stores (data in = data out)
    - Keep 5-9 processes per level
    """

    def __init__(self):
        config = TemplateConfig(
            template_id="dfd",
            name="Data Flow Diagram",
            description="Shows data movement through a system",
            version="1.0.0",
            domain="data",
            category="data_flow",
            diagram_type="dfd_level0",
            elements=[
                DFD_EXTERNAL_ENTITY,
                DFD_PROCESS,
                DFD_DATA_STORE,
                DFD_DATA_FLOW,
                DFD_PROCESS_YDM,
                DFD_BOUNDARY,
            ],
            relations=[
                DFD_FLOW,
                DFD_BIDIRECTIONAL_FLOW,
            ],
            constraints=[
                TemplateConstraint(
                    id="flows_labeled",
                    name="Flows Labeled",
                    description="All data flows should be labeled",
                    validator=lambda d: self._validate_flows_labeled(d),
                    severity="warning",
                ),
                TemplateConstraint(
                    id="process_numbered",
                    name="Processes Numbered",
                    description="All processes should have numbers",
                    validator=lambda d: self._validate_process_numbers(d),
                    severity="warning",
                ),
                TemplateConstraint(
                    id="no_direct_external_flow",
                    name="No Direct External Flow",
                    description="External entities shouldn't connect directly to data stores",
                    validator=lambda d: self._validate_no_direct_external_flow(d),
                    severity="error",
                ),
            ],
            max_elements=20,
            max_relations=40,
            default_layout="graphviz",
            default_theme="corporate",
        )
        super().__init__(config)

    def _validate_flows_labeled(self, diagram) -> List[str]:
        """Validate all data flows have labels"""
        unlabeled = []
        for edge in diagram.edges:
            if not edge.label:
                unlabeled.append(f"{edge.source} -> {edge.target}")
        if unlabeled:
            return [f"Unlabeled data flows: {', '.join(unlabeled[:3])}{'...' if len(unlabeled) > 3 else ''}"]
        return []

    def _validate_process_numbers(self, diagram) -> List[str]:
        """Validate processes have numbers"""
        unnumbered = []
        for node in diagram.nodes:
            if getattr(node, 'element_type', '') in ['process', 'process_ydm']:
                props = getattr(node, 'properties', {})
                if not props.get('number'):
                    unnumbered.append(node.label)
        if unnumbered:
            return [f"Processes without numbers: {', '.join(unnumbered)}"]
        return []

    def _validate_no_direct_external_flow(self, diagram) -> List[str]:
        """Validate external entities don't connect directly to data stores"""
        errors = []
        element_types = {n.id: getattr(n, 'element_type', '') for n in diagram.nodes}

        for edge in diagram.edges:
            source_type = element_types.get(edge.source, '')
            target_type = element_types.get(edge.target, '')

            if source_type == 'external_entity' and target_type == 'data_store':
                errors.append(f"External entity '{edge.source}' connects directly to data store '{edge.target}'")
            if source_type == 'data_store' and target_type == 'external_entity':
                errors.append(f"Data store '{edge.source}' connects directly to external entity '{edge.target}'")

        return errors

    def create_element(
        self,
        element_type: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a DFD element"""
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

        # Add DFD-specific properties
        if element_type in ["process", "process_ydm"]:
            element["number"] = props.get("number")
            element["owner"] = props.get("owner")
        elif element_type == "data_store":
            element["number"] = props.get("number")
            element["technology"] = props.get("technology")

        return element

    def create_relation(
        self,
        relation_type: str,
        source_id: str,
        target_id: str,
        label: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a DFD data flow"""
        relation_def = self.get_relation_definition(relation_type)
        if not relation_def:
            relation_def = DFD_FLOW

        props = properties or {}

        return {
            "source": source_id,
            "target": target_id,
            "label": label or props.get("data_name", ""),
            "relation_type": relation_type,
            "line_style": relation_def.line_style,
            "arrow_style": relation_def.arrow_style,
            "data_elements": props.get("data_elements", []),  # List of data items
            "properties": props,
        }
