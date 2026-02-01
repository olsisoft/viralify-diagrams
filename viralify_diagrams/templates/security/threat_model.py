"""
STRIDE Threat Model Template

Microsoft's STRIDE threat modeling methodology:
- Spoofing
- Tampering
- Repudiation
- Information Disclosure
- Denial of Service
- Elevation of Privilege
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
# STRIDE Elements
# =============================================================================

STRIDE_EXTERNAL_ENTITY = TemplateElement(
    id="external_entity",
    name="External Entity",
    description="External actor (user, system, attacker)",
    shape=ElementShape.RECTANGLE,
    default_color="#E6E6E6",
    default_stroke="#666666",
    required_fields=["name"],
    optional_fields=["trust_level", "description"],
)

STRIDE_PROCESS = TemplateElement(
    id="process",
    name="Process",
    description="A process or service that can be attacked",
    shape=ElementShape.CIRCLE,
    default_color="#E6F3FF",
    default_stroke="#0066CC",
    required_fields=["name"],
    optional_fields=["technology", "port", "privileges"],
)

STRIDE_DATA_STORE = TemplateElement(
    id="data_store",
    name="Data Store",
    description="Database, file, or any data storage",
    shape=ElementShape.RECTANGLE,
    default_color="#FFFACD",
    default_stroke="#B8860B",
    required_fields=["name"],
    optional_fields=["encryption", "sensitivity"],
)

STRIDE_DATA_FLOW = TemplateElement(
    id="data_flow_node",
    name="Data Flow (as node)",
    description="Data in transit",
    shape=ElementShape.PARALLELOGRAM,
    default_color="#E6FFE6",
    default_stroke="#059669",
    required_fields=["name"],
    optional_fields=["protocol", "encryption"],
)

STRIDE_TRUST_BOUNDARY = TemplateElement(
    id="trust_boundary",
    name="Trust Boundary",
    description="Boundary between trust zones",
    shape=ElementShape.RECTANGLE,
    default_color="#FFF0F5",
    default_stroke="#DC2626",
    required_fields=["name"],
    optional_fields=["trust_level"],
    allow_nesting=True,
    nested_types=["process", "data_store", "external_entity"],
)

STRIDE_THREAT = TemplateElement(
    id="threat",
    name="Threat",
    description="An identified threat",
    shape=ElementShape.HEXAGON,
    default_color="#FFCCCC",
    default_stroke="#CC0000",
    required_fields=["name", "stride_category"],
    optional_fields=["severity", "likelihood", "description", "mitigations"],
)

STRIDE_MITIGATION = TemplateElement(
    id="mitigation",
    name="Mitigation",
    description="A security control or mitigation",
    shape=ElementShape.ROUNDED,
    default_color="#CCFFCC",
    default_stroke="#009900",
    required_fields=["name"],
    optional_fields=["type", "implementation_status"],
)

STRIDE_ASSET = TemplateElement(
    id="asset",
    name="Asset",
    description="Valuable asset to protect",
    shape=ElementShape.DIAMOND,
    default_color="#E6E6FA",
    default_stroke="#6A5ACD",
    required_fields=["name"],
    optional_fields=["value", "sensitivity"],
)


# =============================================================================
# STRIDE Relations
# =============================================================================

STRIDE_DATA_FLOW_REL = TemplateRelation(
    id="data_flow",
    name="Data Flow",
    relation_type=RelationType.FLOW,
    description="Flow of data between elements",
    line_style="solid",
    arrow_style="open",
    label_required=True,
)

STRIDE_TRUST_CROSSES = TemplateRelation(
    id="crosses_boundary",
    name="Crosses Trust Boundary",
    relation_type=RelationType.TRUST_BOUNDARY,
    description="Data flow crosses a trust boundary",
    line_style="dashed",
    arrow_style="open",
    line_color="#DC2626",
)

STRIDE_THREATENS = TemplateRelation(
    id="threatens",
    name="Threatens",
    relation_type=RelationType.THREAT,
    description="Threat targets an element",
    line_style="dashed",
    arrow_style="filled",
    line_color="#CC0000",
)

STRIDE_MITIGATES = TemplateRelation(
    id="mitigates",
    name="Mitigates",
    relation_type=RelationType.MITIGATION,
    description="Mitigation addresses a threat",
    line_style="solid",
    arrow_style="filled",
    line_color="#009900",
)

STRIDE_PROTECTS = TemplateRelation(
    id="protects",
    name="Protects",
    relation_type=RelationType.DEPENDS_ON,
    description="Mitigation protects an asset",
    line_style="solid",
    arrow_style="open",
    line_color="#009900",
)


# =============================================================================
# STRIDE Template
# =============================================================================

class STRIDEThreatTemplate(DiagramTemplate):
    """
    STRIDE Threat Model Template.

    Microsoft's threat modeling methodology.

    STRIDE Categories:
    - Spoofing: Pretending to be something/someone else
    - Tampering: Modifying data or code
    - Repudiation: Denying actions took place
    - Information Disclosure: Exposing sensitive data
    - Denial of Service: Making system unavailable
    - Elevation of Privilege: Gaining unauthorized access

    Best practices:
    - Start with DFD of the system
    - Identify trust boundaries
    - Apply STRIDE to each element crossing boundaries
    - Document mitigations for each threat
    - Prioritize by risk (severity × likelihood)
    """

    STRIDE_CATEGORIES = [
        "spoofing",
        "tampering",
        "repudiation",
        "information_disclosure",
        "denial_of_service",
        "elevation_of_privilege",
    ]

    def __init__(self):
        config = TemplateConfig(
            template_id="stride_threat",
            name="STRIDE Threat Model",
            description="Microsoft STRIDE threat modeling diagram",
            version="1.0.0",
            domain="security",
            category="threat_modeling",
            diagram_type="stride_threat_model",
            elements=[
                STRIDE_EXTERNAL_ENTITY,
                STRIDE_PROCESS,
                STRIDE_DATA_STORE,
                STRIDE_DATA_FLOW,
                STRIDE_TRUST_BOUNDARY,
                STRIDE_THREAT,
                STRIDE_MITIGATION,
                STRIDE_ASSET,
            ],
            relations=[
                STRIDE_DATA_FLOW_REL,
                STRIDE_TRUST_CROSSES,
                STRIDE_THREATENS,
                STRIDE_MITIGATES,
                STRIDE_PROTECTS,
            ],
            constraints=[
                TemplateConstraint(
                    id="has_trust_boundary",
                    name="Has Trust Boundary",
                    description="Threat model should have at least one trust boundary",
                    validator=lambda d: self._validate_trust_boundary(d),
                    severity="warning",
                ),
                TemplateConstraint(
                    id="threats_have_mitigations",
                    name="Threats Have Mitigations",
                    description="All threats should have mitigations",
                    validator=lambda d: self._validate_threat_mitigations(d),
                    severity="warning",
                ),
                TemplateConstraint(
                    id="valid_stride_category",
                    name="Valid STRIDE Category",
                    description="Threats must have valid STRIDE category",
                    validator=lambda d: self._validate_stride_category(d),
                    severity="error",
                ),
            ],
            max_elements=40,
            max_relations=60,
            default_layout="graphviz",
            default_theme="corporate",
        )
        super().__init__(config)

    def _validate_trust_boundary(self, diagram) -> List[str]:
        """Validate diagram has trust boundaries"""
        has_boundary = any(getattr(n, 'element_type', '') == 'trust_boundary'
                         for n in diagram.nodes)
        if not has_boundary:
            return ["Threat model should have at least one trust boundary"]
        return []

    def _validate_threat_mitigations(self, diagram) -> List[str]:
        """Validate all threats have mitigations"""
        threats = [n.id for n in diagram.nodes
                  if getattr(n, 'element_type', '') == 'threat']

        unmitigated = []
        for threat_id in threats:
            has_mitigation = any(
                e.source == threat_id and getattr(e, 'relation_type', '') == 'mitigates'
                for e in diagram.edges
            ) or any(
                e.target == threat_id and getattr(e, 'relation_type', '') == 'mitigates'
                for e in diagram.edges
            )
            if not has_mitigation:
                unmitigated.append(threat_id)

        if unmitigated:
            return [f"Threats without mitigations: {', '.join(unmitigated[:3])}"]
        return []

    def _validate_stride_category(self, diagram) -> List[str]:
        """Validate STRIDE categories are valid"""
        errors = []
        for node in diagram.nodes:
            if getattr(node, 'element_type', '') == 'threat':
                props = getattr(node, 'properties', {})
                category = props.get('stride_category', '').lower()
                if category and category not in self.STRIDE_CATEGORIES:
                    errors.append(f"Invalid STRIDE category '{category}' for threat '{node.label}'")
        return errors

    def create_element(
        self,
        element_type: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a STRIDE element"""
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

        # Add type-specific properties
        if element_type == "threat":
            element["stride_category"] = props.get("stride_category")
            element["severity"] = props.get("severity")  # critical, high, medium, low
            element["likelihood"] = props.get("likelihood")  # high, medium, low
            element["risk_score"] = self._calculate_risk(
                props.get("severity", "medium"),
                props.get("likelihood", "medium")
            )
            element["mitigations"] = props.get("mitigations", [])

        elif element_type == "mitigation":
            element["mitigation_type"] = props.get("type")  # preventive, detective, corrective
            element["implementation_status"] = props.get("implementation_status")  # implemented, planned, not_started

        elif element_type == "process":
            element["technology"] = props.get("technology")
            element["port"] = props.get("port")
            element["privileges"] = props.get("privileges")

        elif element_type == "data_store":
            element["encryption"] = props.get("encryption")
            element["sensitivity"] = props.get("sensitivity")

        elif element_type == "trust_boundary":
            element["trust_level"] = props.get("trust_level")

        return element

    def _calculate_risk(self, severity: str, likelihood: str) -> int:
        """Calculate risk score from severity and likelihood"""
        severity_scores = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        likelihood_scores = {"high": 3, "medium": 2, "low": 1}

        sev = severity_scores.get(severity.lower(), 2)
        lik = likelihood_scores.get(likelihood.lower(), 2)

        return sev * lik

    def create_relation(
        self,
        relation_type: str,
        source_id: str,
        target_id: str,
        label: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a STRIDE relation"""
        relation_def = self.get_relation_definition(relation_type)
        if not relation_def:
            relation_def = STRIDE_DATA_FLOW_REL

        props = properties or {}

        return {
            "source": source_id,
            "target": target_id,
            "label": label or "",
            "relation_type": relation_type,
            "line_style": relation_def.line_style,
            "arrow_style": relation_def.arrow_style,
            "line_color": relation_def.line_color,
            "protocol": props.get("protocol"),
            "encryption": props.get("encryption"),
            "properties": props,
        }

    def create_threat(
        self,
        name: str,
        stride_category: str,
        severity: str = "medium",
        likelihood: str = "medium",
        description: Optional[str] = None,
        attack_vector: Optional[str] = None,
        mitigations: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Helper to create a threat element.

        Args:
            name: Threat name
            stride_category: One of STRIDE categories
            severity: critical, high, medium, low
            likelihood: high, medium, low
            description: Detailed description
            attack_vector: How the attack is performed
            mitigations: List of mitigation IDs
        """
        if stride_category.lower() not in self.STRIDE_CATEGORIES:
            raise ValueError(f"Invalid STRIDE category: {stride_category}")

        return self.create_element("threat", name, {
            "stride_category": stride_category.lower(),
            "severity": severity,
            "likelihood": likelihood,
            "description": description,
            "attack_vector": attack_vector,
            "mitigations": mitigations or [],
        })

    def get_stride_threats_for_element(self, element_type: str) -> List[str]:
        """
        Get applicable STRIDE categories for an element type.

        Based on Microsoft's guidance:
        - External entities: Spoofing, Repudiation
        - Processes: All STRIDE categories
        - Data stores: Tampering, Information Disclosure, Denial of Service
        - Data flows: Tampering, Information Disclosure, Denial of Service
        """
        mapping = {
            "external_entity": ["spoofing", "repudiation"],
            "process": self.STRIDE_CATEGORIES,
            "data_store": ["tampering", "information_disclosure", "denial_of_service"],
            "data_flow": ["tampering", "information_disclosure", "denial_of_service"],
            "data_flow_node": ["tampering", "information_disclosure", "denial_of_service"],
        }
        return mapping.get(element_type, [])
