"""
C4 Model Templates

Implementation of Simon Brown's C4 Model for software architecture:
- Context: System context diagram (level 1)
- Container: Container diagram (level 2)
- Component: Component diagram (level 3)
- Code: Code/class diagram (level 4)
- Deployment: Deployment diagram

Reference: https://c4model.com/
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
# C4 Element Definitions
# =============================================================================

# Context Level Elements
C4_PERSON = TemplateElement(
    id="person",
    name="Person",
    description="A user of the system (human actor)",
    shape=ElementShape.ACTOR,
    default_color="#08427B",
    default_stroke="#052E56",
    required_fields=["name"],
    optional_fields=["description", "type"],
)

C4_SOFTWARE_SYSTEM = TemplateElement(
    id="software_system",
    name="Software System",
    description="The highest level of abstraction - a software system",
    shape=ElementShape.ROUNDED,
    default_color="#1168BD",
    default_stroke="#0B4884",
    required_fields=["name"],
    optional_fields=["description", "technology"],
)

C4_EXTERNAL_SYSTEM = TemplateElement(
    id="external_system",
    name="External System",
    description="An external software system outside the boundary",
    shape=ElementShape.ROUNDED,
    default_color="#999999",
    default_stroke="#666666",
    required_fields=["name"],
    optional_fields=["description", "technology"],
)

# Container Level Elements
C4_CONTAINER = TemplateElement(
    id="container",
    name="Container",
    description="An application or data store (web app, API, database, etc.)",
    shape=ElementShape.ROUNDED,
    default_color="#438DD5",
    default_stroke="#2E6295",
    required_fields=["name", "technology"],
    optional_fields=["description", "port"],
)

C4_DATABASE = TemplateElement(
    id="database",
    name="Database",
    description="A database or data store",
    shape=ElementShape.CYLINDER,
    default_color="#438DD5",
    default_stroke="#2E6295",
    required_fields=["name", "technology"],
    optional_fields=["description", "schema"],
)

C4_MESSAGE_QUEUE = TemplateElement(
    id="message_queue",
    name="Message Queue",
    description="A message broker or queue",
    shape=ElementShape.QUEUE,
    default_color="#438DD5",
    default_stroke="#2E6295",
    required_fields=["name", "technology"],
    optional_fields=["description"],
)

# Component Level Elements
C4_COMPONENT = TemplateElement(
    id="component",
    name="Component",
    description="A component within a container",
    shape=ElementShape.COMPONENT,
    default_color="#85BBF0",
    default_stroke="#5A9BD4",
    required_fields=["name"],
    optional_fields=["description", "technology", "interface"],
)

# Deployment Level Elements
C4_DEPLOYMENT_NODE = TemplateElement(
    id="deployment_node",
    name="Deployment Node",
    description="Infrastructure node (server, cloud service, etc.)",
    shape=ElementShape.NODE,
    default_color="#FFFFFF",
    default_stroke="#438DD5",
    required_fields=["name"],
    optional_fields=["description", "technology", "instances"],
    allow_nesting=True,
    nested_types=["container", "deployment_node"],
)

C4_INFRASTRUCTURE_NODE = TemplateElement(
    id="infrastructure_node",
    name="Infrastructure Node",
    description="Cloud or on-premise infrastructure",
    shape=ElementShape.CLOUD,
    default_color="#FFFFFF",
    default_stroke="#999999",
    required_fields=["name"],
    optional_fields=["description", "provider"],
    allow_nesting=True,
    nested_types=["deployment_node"],
)


# =============================================================================
# C4 Relation Definitions
# =============================================================================

C4_USES = TemplateRelation(
    id="uses",
    name="Uses",
    relation_type=RelationType.USES,
    description="A relationship where one element uses another",
    line_style="solid",
    arrow_style="open",
    label_required=False,
)

C4_READS_FROM = TemplateRelation(
    id="reads_from",
    name="Reads From",
    relation_type=RelationType.READS_FROM,
    description="Reads data from a data store",
    line_style="solid",
    arrow_style="open",
    allowed_target_types=["database"],
)

C4_WRITES_TO = TemplateRelation(
    id="writes_to",
    name="Writes To",
    relation_type=RelationType.WRITES_TO,
    description="Writes data to a data store",
    line_style="solid",
    arrow_style="open",
    allowed_target_types=["database"],
)

C4_SENDS_TO = TemplateRelation(
    id="sends_to",
    name="Sends To",
    relation_type=RelationType.SENDS_TO,
    description="Sends messages/events to a queue",
    line_style="dashed",
    arrow_style="open",
    allowed_target_types=["message_queue"],
)

C4_CALLS = TemplateRelation(
    id="calls",
    name="Calls",
    relation_type=RelationType.CALLS,
    description="Makes API/function calls to another component",
    line_style="solid",
    arrow_style="filled",
)


# =============================================================================
# C4 Context Template
# =============================================================================

class C4ContextTemplate(DiagramTemplate):
    """
    C4 Context Diagram Template (Level 1).

    Shows the system in context with users and external systems.

    Best practices:
    - Focus on the system boundary
    - Show all users (personas) and external systems
    - Keep it simple (5-10 elements max)
    - Use simple relationships
    """

    def __init__(self):
        config = TemplateConfig(
            template_id="c4_context",
            name="C4 Context Diagram",
            description="System context diagram showing users and external systems",
            version="1.0.0",
            domain="architecture",
            category="c4_model",
            diagram_type="c4_context",
            elements=[
                C4_PERSON,
                C4_SOFTWARE_SYSTEM,
                C4_EXTERNAL_SYSTEM,
            ],
            relations=[
                C4_USES,
            ],
            constraints=[
                TemplateConstraint(
                    id="single_system",
                    name="Single System Focus",
                    description="Context diagram should focus on one system",
                    validator=lambda d: self._validate_single_system(d),
                    severity="warning",
                ),
            ],
            max_elements=10,
            max_relations=20,
            default_layout="vertical",
            default_theme="corporate",
            require_legend=True,
        )
        super().__init__(config)

    def _validate_single_system(self, diagram) -> List[str]:
        """Validate that there's one primary system"""
        system_count = sum(1 for n in diagram.nodes
                         if getattr(n, 'element_type', '') == 'software_system')
        if system_count == 0:
            return ["Context diagram should have at least one software system"]
        if system_count > 1:
            return ["Context diagram should focus on one primary system"]
        return []

    def create_element(
        self,
        element_type: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a C4 context element"""
        props = properties or {}

        element_def = self.get_element_definition(element_type)
        if not element_def:
            raise ValueError(f"Unknown element type: {element_type}")

        return {
            "id": props.get("id", label.lower().replace(" ", "_")),
            "label": label,
            "element_type": element_type,
            "shape": element_def.shape.value,
            "fill_color": props.get("color", element_def.default_color),
            "stroke_color": element_def.default_stroke,
            "description": props.get("description", ""),
            "technology": props.get("technology", ""),
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
        """Create a C4 context relation"""
        relation_def = self.get_relation_definition(relation_type)
        if not relation_def:
            relation_def = C4_USES  # Default to uses

        return {
            "source": source_id,
            "target": target_id,
            "label": label or "",
            "relation_type": relation_type,
            "line_style": relation_def.line_style,
            "arrow_style": relation_def.arrow_style,
            "properties": properties or {},
        }


# =============================================================================
# C4 Container Template
# =============================================================================

class C4ContainerTemplate(DiagramTemplate):
    """
    C4 Container Diagram Template (Level 2).

    Shows the containers within a system.

    Best practices:
    - Show all containers (applications, databases, queues)
    - Include technology choices
    - Show communication protocols
    - Max 12-15 containers for readability
    """

    def __init__(self):
        config = TemplateConfig(
            template_id="c4_container",
            name="C4 Container Diagram",
            description="Container diagram showing applications and data stores",
            version="1.0.0",
            domain="architecture",
            category="c4_model",
            diagram_type="c4_container",
            elements=[
                C4_PERSON,
                C4_SOFTWARE_SYSTEM,
                C4_EXTERNAL_SYSTEM,
                C4_CONTAINER,
                C4_DATABASE,
                C4_MESSAGE_QUEUE,
            ],
            relations=[
                C4_USES,
                C4_READS_FROM,
                C4_WRITES_TO,
                C4_SENDS_TO,
                C4_CALLS,
            ],
            max_elements=15,
            max_relations=40,
            default_layout="graphviz",
            default_theme="corporate",
            require_legend=True,
        )
        super().__init__(config)

    def create_element(
        self,
        element_type: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a C4 container element"""
        props = properties or {}

        element_def = self.get_element_definition(element_type)
        if not element_def:
            raise ValueError(f"Unknown element type: {element_type}")

        return {
            "id": props.get("id", label.lower().replace(" ", "_")),
            "label": label,
            "element_type": element_type,
            "shape": element_def.shape.value,
            "fill_color": props.get("color", element_def.default_color),
            "stroke_color": element_def.default_stroke,
            "description": props.get("description", ""),
            "technology": props.get("technology", ""),
            "port": props.get("port"),
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
        """Create a C4 container relation"""
        relation_def = self.get_relation_definition(relation_type)
        if not relation_def:
            relation_def = C4_USES

        props = properties or {}

        return {
            "source": source_id,
            "target": target_id,
            "label": label or props.get("protocol", ""),
            "relation_type": relation_type,
            "line_style": relation_def.line_style,
            "arrow_style": relation_def.arrow_style,
            "protocol": props.get("protocol"),
            "properties": props,
        }


# =============================================================================
# C4 Component Template
# =============================================================================

class C4ComponentTemplate(DiagramTemplate):
    """
    C4 Component Diagram Template (Level 3).

    Shows the components within a container.

    Best practices:
    - Focus on one container at a time
    - Show interfaces and dependencies
    - Include external dependencies
    - Consider splitting large components
    """

    def __init__(self):
        config = TemplateConfig(
            template_id="c4_component",
            name="C4 Component Diagram",
            description="Component diagram showing internal structure of a container",
            version="1.0.0",
            domain="architecture",
            category="c4_model",
            diagram_type="c4_component",
            elements=[
                C4_CONTAINER,
                C4_DATABASE,
                C4_COMPONENT,
                C4_EXTERNAL_SYSTEM,
            ],
            relations=[
                C4_USES,
                C4_READS_FROM,
                C4_WRITES_TO,
                C4_CALLS,
            ],
            max_elements=20,
            max_relations=50,
            default_layout="graphviz",
            default_theme="corporate",
        )
        super().__init__(config)

    def create_element(
        self,
        element_type: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a C4 component element"""
        props = properties or {}

        element_def = self.get_element_definition(element_type)
        if not element_def:
            raise ValueError(f"Unknown element type: {element_type}")

        return {
            "id": props.get("id", label.lower().replace(" ", "_")),
            "label": label,
            "element_type": element_type,
            "shape": element_def.shape.value,
            "fill_color": props.get("color", element_def.default_color),
            "stroke_color": element_def.default_stroke,
            "description": props.get("description", ""),
            "technology": props.get("technology", ""),
            "interface": props.get("interface"),
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
        """Create a C4 component relation"""
        relation_def = self.get_relation_definition(relation_type)
        if not relation_def:
            relation_def = C4_USES

        return {
            "source": source_id,
            "target": target_id,
            "label": label or "",
            "relation_type": relation_type,
            "line_style": relation_def.line_style,
            "arrow_style": relation_def.arrow_style,
            "properties": properties or {},
        }


# =============================================================================
# C4 Deployment Template
# =============================================================================

class C4DeploymentTemplate(DiagramTemplate):
    """
    C4 Deployment Diagram Template.

    Shows how containers are deployed to infrastructure.

    Best practices:
    - Show deployment environments (dev, staging, prod)
    - Include infrastructure nodes (servers, cloud services)
    - Show container instances with replica counts
    - Include network boundaries
    """

    def __init__(self):
        config = TemplateConfig(
            template_id="c4_deployment",
            name="C4 Deployment Diagram",
            description="Deployment diagram showing infrastructure and container mapping",
            version="1.0.0",
            domain="architecture",
            category="c4_model",
            diagram_type="c4_deployment",
            elements=[
                C4_DEPLOYMENT_NODE,
                C4_INFRASTRUCTURE_NODE,
                C4_CONTAINER,
                C4_DATABASE,
            ],
            relations=[
                C4_USES,
                TemplateRelation(
                    id="deployed_on",
                    name="Deployed On",
                    relation_type=RelationType.DEPENDS_ON,
                    description="Container deployed on a node",
                    line_style="dashed",
                    arrow_style="open",
                ),
            ],
            max_elements=25,
            max_relations=40,
            max_nesting_depth=3,
            default_layout="vertical",
            default_theme="aws",  # Common for deployment diagrams
            icon_set="aws",
        )
        super().__init__(config)

    def create_element(
        self,
        element_type: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a C4 deployment element"""
        props = properties or {}

        element_def = self.get_element_definition(element_type)
        if not element_def:
            raise ValueError(f"Unknown element type: {element_type}")

        return {
            "id": props.get("id", label.lower().replace(" ", "_")),
            "label": label,
            "element_type": element_type,
            "shape": element_def.shape.value,
            "fill_color": props.get("color", element_def.default_color),
            "stroke_color": element_def.default_stroke,
            "description": props.get("description", ""),
            "technology": props.get("technology", ""),
            "instances": props.get("instances", 1),
            "provider": props.get("provider"),
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
        """Create a C4 deployment relation"""
        relation_def = self.get_relation_definition(relation_type)
        if not relation_def:
            relation_def = C4_USES

        return {
            "source": source_id,
            "target": target_id,
            "label": label or "",
            "relation_type": relation_type,
            "line_style": relation_def.line_style,
            "arrow_style": relation_def.arrow_style,
            "properties": properties or {},
        }
