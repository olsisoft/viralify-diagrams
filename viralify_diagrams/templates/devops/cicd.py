"""
CI/CD Pipeline Template

Continuous Integration and Continuous Deployment pipelines:
- Build stages
- Test stages
- Deploy stages
- Environments
- Approvals and gates
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
# CI/CD Elements
# =============================================================================

CICD_SOURCE = TemplateElement(
    id="source",
    name="Source Repository",
    description="Git repository or source control",
    shape=ElementShape.FOLDER,
    default_color="#F5F5F5",
    default_stroke="#333333",
    required_fields=["name"],
    optional_fields=["provider", "branch"],
)

CICD_TRIGGER = TemplateElement(
    id="trigger",
    name="Trigger",
    description="Pipeline trigger (push, PR, schedule)",
    shape=ElementShape.HEXAGON,
    default_color="#E6FFE6",
    default_stroke="#059669",
    required_fields=["type"],
    optional_fields=["condition", "schedule"],
)

CICD_STAGE = TemplateElement(
    id="stage",
    name="Stage",
    description="Pipeline stage (build, test, deploy)",
    shape=ElementShape.ROUNDED,
    default_color="#E6F3FF",
    default_stroke="#0066CC",
    required_fields=["name"],
    optional_fields=["jobs", "parallel"],
    allow_nesting=True,
    nested_types=["job"],
)

CICD_JOB = TemplateElement(
    id="job",
    name="Job",
    description="Individual job within a stage",
    shape=ElementShape.RECTANGLE,
    default_color="#FFFFFF",
    default_stroke="#666666",
    required_fields=["name"],
    optional_fields=["steps", "runner", "timeout"],
)

CICD_STEP = TemplateElement(
    id="step",
    name="Step",
    description="Individual step within a job",
    shape=ElementShape.RECTANGLE,
    default_color="#F5F5F5",
    default_stroke="#999999",
    required_fields=["name"],
    optional_fields=["command", "action"],
)

CICD_ARTIFACT = TemplateElement(
    id="artifact",
    name="Artifact",
    description="Build artifact (binary, container image)",
    shape=ElementShape.FILE,
    default_color="#FFFACD",
    default_stroke="#B8860B",
    required_fields=["name"],
    optional_fields=["type", "path"],
)

CICD_REGISTRY = TemplateElement(
    id="registry",
    name="Registry",
    description="Artifact or container registry",
    shape=ElementShape.CYLINDER,
    default_color="#E6E6FA",
    default_stroke="#6A5ACD",
    required_fields=["name"],
    optional_fields=["provider", "url"],
)

CICD_ENVIRONMENT = TemplateElement(
    id="environment",
    name="Environment",
    description="Deployment environment (dev, staging, prod)",
    shape=ElementShape.CLOUD,
    default_color="#FFE6CC",
    default_stroke="#D97706",
    required_fields=["name"],
    optional_fields=["type", "url", "protection_rules"],
)

CICD_APPROVAL = TemplateElement(
    id="approval",
    name="Approval Gate",
    description="Manual or automated approval",
    shape=ElementShape.DIAMOND,
    default_color="#FFF0F5",
    default_stroke="#DC2626",
    required_fields=["name"],
    optional_fields=["approvers", "type"],
)

CICD_NOTIFICATION = TemplateElement(
    id="notification",
    name="Notification",
    description="Notification channel (Slack, email)",
    shape=ElementShape.PARALLELOGRAM,
    default_color="#E8F5E9",
    default_stroke="#2E7D32",
    required_fields=["channel"],
    optional_fields=["condition"],
)

CICD_SECRET = TemplateElement(
    id="secret",
    name="Secret",
    description="Secret or credential store",
    shape=ElementShape.HEXAGON,
    default_color="#FCE4EC",
    default_stroke="#C2185B",
    required_fields=["name"],
    optional_fields=["provider"],
)


# =============================================================================
# CI/CD Relations
# =============================================================================

CICD_TRIGGERS = TemplateRelation(
    id="triggers",
    name="Triggers",
    relation_type=RelationType.FLOW,
    description="Triggers the next stage/job",
    line_style="solid",
    arrow_style="filled",
)

CICD_ON_SUCCESS = TemplateRelation(
    id="on_success",
    name="On Success",
    relation_type=RelationType.CONDITIONAL,
    description="Proceeds on success",
    line_style="solid",
    arrow_style="open",
    line_color="#059669",
)

CICD_ON_FAILURE = TemplateRelation(
    id="on_failure",
    name="On Failure",
    relation_type=RelationType.CONDITIONAL,
    description="Proceeds on failure",
    line_style="dashed",
    arrow_style="open",
    line_color="#DC2626",
)

CICD_PRODUCES = TemplateRelation(
    id="produces",
    name="Produces",
    relation_type=RelationType.WRITES_TO,
    description="Produces an artifact",
    line_style="solid",
    arrow_style="open",
)

CICD_CONSUMES = TemplateRelation(
    id="consumes",
    name="Consumes",
    relation_type=RelationType.READS_FROM,
    description="Consumes an artifact",
    line_style="dashed",
    arrow_style="open",
)

CICD_DEPLOYS_TO = TemplateRelation(
    id="deploys_to",
    name="Deploys To",
    relation_type=RelationType.FLOW,
    description="Deploys to an environment",
    line_style="solid",
    arrow_style="filled",
)

CICD_REQUIRES_APPROVAL = TemplateRelation(
    id="requires_approval",
    name="Requires Approval",
    relation_type=RelationType.DEPENDS_ON,
    description="Requires approval before proceeding",
    line_style="dashed",
    arrow_style="diamond",
)

CICD_NOTIFIES = TemplateRelation(
    id="notifies",
    name="Notifies",
    relation_type=RelationType.SENDS_TO,
    description="Sends notification",
    line_style="dotted",
    arrow_style="open",
)


# =============================================================================
# CI/CD Template
# =============================================================================

class CICDPipelineTemplate(DiagramTemplate):
    """
    CI/CD Pipeline Template.

    Shows continuous integration and deployment workflows.

    Common patterns:
    - Linear: Source → Build → Test → Deploy
    - Parallel: Multiple test jobs in parallel
    - Fan-out/Fan-in: Deploy to multiple environments
    - Blue/Green: Deploy to staging, swap to prod

    Best practices:
    - Show all stages clearly
    - Include approval gates for production
    - Show artifact flow
    - Include notification channels
    """

    def __init__(self):
        config = TemplateConfig(
            template_id="cicd_pipeline",
            name="CI/CD Pipeline",
            description="Continuous Integration/Deployment pipeline",
            version="1.0.0",
            domain="devops",
            category="ci_cd",
            diagram_type="ci_cd_pipeline",
            elements=[
                CICD_SOURCE,
                CICD_TRIGGER,
                CICD_STAGE,
                CICD_JOB,
                CICD_STEP,
                CICD_ARTIFACT,
                CICD_REGISTRY,
                CICD_ENVIRONMENT,
                CICD_APPROVAL,
                CICD_NOTIFICATION,
                CICD_SECRET,
            ],
            relations=[
                CICD_TRIGGERS,
                CICD_ON_SUCCESS,
                CICD_ON_FAILURE,
                CICD_PRODUCES,
                CICD_CONSUMES,
                CICD_DEPLOYS_TO,
                CICD_REQUIRES_APPROVAL,
                CICD_NOTIFIES,
            ],
            constraints=[
                TemplateConstraint(
                    id="has_source",
                    name="Has Source",
                    description="Pipeline should start with a source",
                    validator=lambda d: self._validate_has_source(d),
                    severity="warning",
                ),
                TemplateConstraint(
                    id="prod_has_approval",
                    name="Production Has Approval",
                    description="Production deployment should have approval",
                    validator=lambda d: self._validate_prod_approval(d),
                    severity="warning",
                ),
            ],
            max_elements=30,
            max_relations=50,
            default_layout="horizontal",
            default_theme="corporate",
        )
        super().__init__(config)

    def _validate_has_source(self, diagram) -> List[str]:
        """Validate pipeline has a source"""
        has_source = any(getattr(n, 'element_type', '') in ['source', 'trigger']
                        for n in diagram.nodes)
        if not has_source:
            return ["Pipeline should have a source or trigger"]
        return []

    def _validate_prod_approval(self, diagram) -> List[str]:
        """Validate production environments have approvals"""
        warnings = []
        prod_envs = [n.id for n in diagram.nodes
                    if getattr(n, 'element_type', '') == 'environment'
                    and 'prod' in n.label.lower()]

        for prod_id in prod_envs:
            has_approval = any(
                (e.target == prod_id and getattr(e, 'relation_type', '') == 'requires_approval')
                or (e.source == prod_id and getattr(e, 'relation_type', '') == 'requires_approval')
                for e in diagram.edges
            )
            if not has_approval:
                warnings.append(f"Production environment '{prod_id}' has no approval gate")

        return warnings

    def create_element(
        self,
        element_type: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a CI/CD element"""
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
        if element_type == "source":
            element["provider"] = props.get("provider")  # github, gitlab, bitbucket
            element["branch"] = props.get("branch")

        elif element_type == "trigger":
            element["trigger_type"] = props.get("type")  # push, pr, schedule, manual
            element["condition"] = props.get("condition")
            element["schedule"] = props.get("schedule")

        elif element_type == "stage":
            element["jobs"] = props.get("jobs", [])
            element["parallel"] = props.get("parallel", False)

        elif element_type == "job":
            element["steps"] = props.get("steps", [])
            element["runner"] = props.get("runner")
            element["timeout"] = props.get("timeout")

        elif element_type == "artifact":
            element["artifact_type"] = props.get("type")  # binary, container, package
            element["path"] = props.get("path")

        elif element_type == "environment":
            element["env_type"] = props.get("type")  # development, staging, production
            element["url"] = props.get("url")
            element["protection_rules"] = props.get("protection_rules", [])

        elif element_type == "approval":
            element["approvers"] = props.get("approvers", [])
            element["approval_type"] = props.get("type", "manual")  # manual, automated

        return element

    def create_relation(
        self,
        relation_type: str,
        source_id: str,
        target_id: str,
        label: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a CI/CD relation"""
        relation_def = self.get_relation_definition(relation_type)
        if not relation_def:
            relation_def = CICD_TRIGGERS

        props = properties or {}

        return {
            "source": source_id,
            "target": target_id,
            "label": label or "",
            "relation_type": relation_type,
            "line_style": relation_def.line_style,
            "arrow_style": relation_def.arrow_style,
            "line_color": getattr(relation_def, 'line_color', None),
            "condition": props.get("condition"),
            "properties": props,
        }

    def create_pipeline(
        self,
        name: str,
        stages: List[Dict[str, Any]],
        source: Optional[Dict[str, Any]] = None,
        environments: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Helper to create a complete pipeline definition.

        Args:
            name: Pipeline name
            stages: List of stage definitions
            source: Source repository definition
            environments: List of environment definitions
        """
        return {
            "name": name,
            "source": source,
            "stages": stages,
            "environments": environments or [],
        }
