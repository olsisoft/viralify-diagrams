"""
Diagram Taxonomy Categories

Comprehensive categorization of diagram types across all IT domains:
- Architecture (C4, TOGAF, ArchiMate, 4+1)
- Development (UML, ERD, Class, Sequence)
- Data (DFD, Lineage, Star Schema, ETL)
- Security (STRIDE, Threat Models, Zero Trust)
- Network (Topology, Segmentation, Zones)
- DevOps (CI/CD, Kubernetes, GitOps)
- Business (BPMN, Value Stream, Org Charts)
- Cloud (Reference Architectures, Well-Architected)
"""

from enum import Enum
from typing import Dict, List, Set


class DiagramDomain(str, Enum):
    """High-level domain classification"""
    ARCHITECTURE = "architecture"
    DEVELOPMENT = "development"
    DATA = "data"
    SECURITY = "security"
    NETWORK = "network"
    DEVOPS = "devops"
    BUSINESS = "business"
    CLOUD = "cloud"
    INFRASTRUCTURE = "infrastructure"
    INTEGRATION = "integration"


class DiagramCategory(str, Enum):
    """Mid-level category within domains"""
    # Architecture
    C4_MODEL = "c4_model"
    TOGAF = "togaf"
    ARCHIMATE = "archimate"
    FOUR_PLUS_ONE = "4+1_view"
    SOLUTION_ARCHITECTURE = "solution_architecture"
    ENTERPRISE_ARCHITECTURE = "enterprise_architecture"

    # Development / UML
    UML_STRUCTURAL = "uml_structural"
    UML_BEHAVIORAL = "uml_behavioral"
    UML_INTERACTION = "uml_interaction"
    API_DESIGN = "api_design"

    # Data
    DATA_MODELING = "data_modeling"
    DATA_FLOW = "data_flow"
    DATA_PIPELINE = "data_pipeline"
    DATA_WAREHOUSE = "data_warehouse"

    # Security
    THREAT_MODELING = "threat_modeling"
    SECURITY_ARCHITECTURE = "security_architecture"
    COMPLIANCE = "compliance"

    # Network
    NETWORK_TOPOLOGY = "network_topology"
    NETWORK_SECURITY = "network_security"

    # DevOps
    CI_CD = "ci_cd"
    CONTAINER_ORCHESTRATION = "container_orchestration"
    INFRASTRUCTURE_AS_CODE = "infrastructure_as_code"
    GITOPS = "gitops"

    # Business
    BUSINESS_PROCESS = "business_process"
    ORGANIZATIONAL = "organizational"
    STRATEGY = "strategy"

    # Cloud
    AWS_ARCHITECTURE = "aws_architecture"
    GCP_ARCHITECTURE = "gcp_architecture"
    AZURE_ARCHITECTURE = "azure_architecture"
    MULTI_CLOUD = "multi_cloud"
    HYBRID_CLOUD = "hybrid_cloud"

    # Infrastructure
    DATACENTER = "datacenter"
    VIRTUALIZATION = "virtualization"
    STORAGE = "storage"

    # Integration
    MICROSERVICES = "microservices"
    EVENT_DRIVEN = "event_driven"
    MESSAGE_QUEUE = "message_queue"


class DiagramType(str, Enum):
    """Specific diagram type"""
    # C4 Model
    C4_CONTEXT = "c4_context"
    C4_CONTAINER = "c4_container"
    C4_COMPONENT = "c4_component"
    C4_CODE = "c4_code"
    C4_DEPLOYMENT = "c4_deployment"
    C4_DYNAMIC = "c4_dynamic"

    # TOGAF
    TOGAF_BUSINESS = "togaf_business"
    TOGAF_DATA = "togaf_data"
    TOGAF_APPLICATION = "togaf_application"
    TOGAF_TECHNOLOGY = "togaf_technology"

    # ArchiMate
    ARCHIMATE_STRATEGY = "archimate_strategy"
    ARCHIMATE_BUSINESS = "archimate_business"
    ARCHIMATE_APPLICATION = "archimate_application"
    ARCHIMATE_TECHNOLOGY = "archimate_technology"
    ARCHIMATE_MOTIVATION = "archimate_motivation"

    # UML Structural
    UML_CLASS = "uml_class"
    UML_OBJECT = "uml_object"
    UML_COMPONENT = "uml_component"
    UML_COMPOSITE = "uml_composite"
    UML_DEPLOYMENT = "uml_deployment"
    UML_PACKAGE = "uml_package"
    UML_PROFILE = "uml_profile"

    # UML Behavioral
    UML_ACTIVITY = "uml_activity"
    UML_STATE_MACHINE = "uml_state_machine"
    UML_USE_CASE = "uml_use_case"

    # UML Interaction
    UML_SEQUENCE = "uml_sequence"
    UML_COMMUNICATION = "uml_communication"
    UML_TIMING = "uml_timing"
    UML_INTERACTION_OVERVIEW = "uml_interaction_overview"

    # Data
    DFD_CONTEXT = "dfd_context"
    DFD_LEVEL0 = "dfd_level0"
    DFD_LEVEL1 = "dfd_level1"
    DFD_LEVEL2 = "dfd_level2"
    ERD = "erd"
    ERD_CHEN = "erd_chen"
    ERD_CROW_FOOT = "erd_crow_foot"
    DATA_LINEAGE = "data_lineage"
    STAR_SCHEMA = "star_schema"
    SNOWFLAKE_SCHEMA = "snowflake_schema"
    DATA_VAULT = "data_vault"
    ETL_PIPELINE = "etl_pipeline"
    ELT_PIPELINE = "elt_pipeline"
    STREAMING_PIPELINE = "streaming_pipeline"

    # Security
    STRIDE_THREAT_MODEL = "stride_threat_model"
    ATTACK_TREE = "attack_tree"
    ZERO_TRUST = "zero_trust"
    SECURITY_ZONES = "security_zones"
    IAM_ARCHITECTURE = "iam_architecture"
    ENCRYPTION_FLOW = "encryption_flow"

    # Network
    NETWORK_STAR = "network_star"
    NETWORK_MESH = "network_mesh"
    NETWORK_RING = "network_ring"
    NETWORK_BUS = "network_bus"
    NETWORK_HYBRID = "network_hybrid"
    NETWORK_TREE = "network_tree"
    VLAN_DIAGRAM = "vlan_diagram"
    VPC_DIAGRAM = "vpc_diagram"
    SUBNET_DIAGRAM = "subnet_diagram"
    FIREWALL_RULES = "firewall_rules"
    LOAD_BALANCER = "load_balancer"

    # DevOps
    CI_CD_PIPELINE = "ci_cd_pipeline"
    DEPLOYMENT_PIPELINE = "deployment_pipeline"
    RELEASE_PIPELINE = "release_pipeline"
    KUBERNETES_CLUSTER = "kubernetes_cluster"
    KUBERNETES_DEPLOYMENT = "kubernetes_deployment"
    KUBERNETES_SERVICES = "kubernetes_services"
    HELM_CHART = "helm_chart"
    DOCKER_COMPOSE = "docker_compose"
    TERRAFORM_GRAPH = "terraform_graph"
    ANSIBLE_PLAYBOOK = "ansible_playbook"
    GITOPS_WORKFLOW = "gitops_workflow"
    ARGOCD_FLOW = "argocd_flow"

    # Business
    BPMN_PROCESS = "bpmn_process"
    BPMN_COLLABORATION = "bpmn_collaboration"
    BPMN_CHOREOGRAPHY = "bpmn_choreography"
    VALUE_STREAM_MAP = "value_stream_map"
    ORG_CHART = "org_chart"
    CUSTOMER_JOURNEY = "customer_journey"
    STAKEHOLDER_MAP = "stakeholder_map"
    SWOT = "swot"
    PORTER_FIVE_FORCES = "porter_five_forces"

    # Cloud
    AWS_REFERENCE = "aws_reference"
    AWS_WELL_ARCHITECTED = "aws_well_architected"
    AWS_SERVERLESS = "aws_serverless"
    AWS_MICROSERVICES = "aws_microservices"
    GCP_REFERENCE = "gcp_reference"
    GCP_ANTHOS = "gcp_anthos"
    AZURE_REFERENCE = "azure_reference"
    AZURE_LANDING_ZONE = "azure_landing_zone"
    MULTI_CLOUD_ARCH = "multi_cloud_arch"

    # Integration
    MICROSERVICES_ARCH = "microservices_arch"
    API_GATEWAY = "api_gateway"
    SERVICE_MESH = "service_mesh"
    EVENT_SOURCING = "event_sourcing"
    CQRS = "cqrs"
    SAGA_PATTERN = "saga_pattern"
    MESSAGE_BROKER = "message_broker"
    PUB_SUB = "pub_sub"

    # Generic
    FLOWCHART = "flowchart"
    MIND_MAP = "mind_map"
    BLOCK_DIAGRAM = "block_diagram"
    HIERARCHY = "hierarchy"


class ComplexityLevel(str, Enum):
    """Complexity level for slide optimization"""
    SIMPLE = "simple"           # 1-3 elements, beginner audience
    MODERATE = "moderate"       # 4-8 elements, intermediate
    COMPLEX = "complex"         # 9-15 elements, advanced
    ENTERPRISE = "enterprise"   # 15+ elements, expert level


class AudienceType(str, Enum):
    """Target audience for diagram optimization"""
    EXECUTIVE = "executive"         # C-level, high-level view
    MANAGER = "manager"             # Project managers, team leads
    ARCHITECT = "architect"         # Solution/Enterprise architects
    DEVELOPER = "developer"         # Software engineers
    DEVOPS = "devops"               # DevOps/SRE engineers
    DATA_ENGINEER = "data_engineer" # Data engineers/analysts
    SECURITY = "security"           # Security engineers
    BUSINESS = "business"           # Business analysts
    GENERAL = "general"             # Mixed audience


# Domain to Categories mapping
DOMAIN_CATEGORIES: Dict[DiagramDomain, List[DiagramCategory]] = {
    DiagramDomain.ARCHITECTURE: [
        DiagramCategory.C4_MODEL,
        DiagramCategory.TOGAF,
        DiagramCategory.ARCHIMATE,
        DiagramCategory.FOUR_PLUS_ONE,
        DiagramCategory.SOLUTION_ARCHITECTURE,
        DiagramCategory.ENTERPRISE_ARCHITECTURE,
    ],
    DiagramDomain.DEVELOPMENT: [
        DiagramCategory.UML_STRUCTURAL,
        DiagramCategory.UML_BEHAVIORAL,
        DiagramCategory.UML_INTERACTION,
        DiagramCategory.API_DESIGN,
    ],
    DiagramDomain.DATA: [
        DiagramCategory.DATA_MODELING,
        DiagramCategory.DATA_FLOW,
        DiagramCategory.DATA_PIPELINE,
        DiagramCategory.DATA_WAREHOUSE,
    ],
    DiagramDomain.SECURITY: [
        DiagramCategory.THREAT_MODELING,
        DiagramCategory.SECURITY_ARCHITECTURE,
        DiagramCategory.COMPLIANCE,
    ],
    DiagramDomain.NETWORK: [
        DiagramCategory.NETWORK_TOPOLOGY,
        DiagramCategory.NETWORK_SECURITY,
    ],
    DiagramDomain.DEVOPS: [
        DiagramCategory.CI_CD,
        DiagramCategory.CONTAINER_ORCHESTRATION,
        DiagramCategory.INFRASTRUCTURE_AS_CODE,
        DiagramCategory.GITOPS,
    ],
    DiagramDomain.BUSINESS: [
        DiagramCategory.BUSINESS_PROCESS,
        DiagramCategory.ORGANIZATIONAL,
        DiagramCategory.STRATEGY,
    ],
    DiagramDomain.CLOUD: [
        DiagramCategory.AWS_ARCHITECTURE,
        DiagramCategory.GCP_ARCHITECTURE,
        DiagramCategory.AZURE_ARCHITECTURE,
        DiagramCategory.MULTI_CLOUD,
        DiagramCategory.HYBRID_CLOUD,
    ],
    DiagramDomain.INFRASTRUCTURE: [
        DiagramCategory.DATACENTER,
        DiagramCategory.VIRTUALIZATION,
        DiagramCategory.STORAGE,
    ],
    DiagramDomain.INTEGRATION: [
        DiagramCategory.MICROSERVICES,
        DiagramCategory.EVENT_DRIVEN,
        DiagramCategory.MESSAGE_QUEUE,
    ],
}


# Category to Types mapping
CATEGORY_TYPES: Dict[DiagramCategory, List[DiagramType]] = {
    # C4 Model
    DiagramCategory.C4_MODEL: [
        DiagramType.C4_CONTEXT,
        DiagramType.C4_CONTAINER,
        DiagramType.C4_COMPONENT,
        DiagramType.C4_CODE,
        DiagramType.C4_DEPLOYMENT,
        DiagramType.C4_DYNAMIC,
    ],
    # TOGAF
    DiagramCategory.TOGAF: [
        DiagramType.TOGAF_BUSINESS,
        DiagramType.TOGAF_DATA,
        DiagramType.TOGAF_APPLICATION,
        DiagramType.TOGAF_TECHNOLOGY,
    ],
    # ArchiMate
    DiagramCategory.ARCHIMATE: [
        DiagramType.ARCHIMATE_STRATEGY,
        DiagramType.ARCHIMATE_BUSINESS,
        DiagramType.ARCHIMATE_APPLICATION,
        DiagramType.ARCHIMATE_TECHNOLOGY,
        DiagramType.ARCHIMATE_MOTIVATION,
    ],
    # UML Structural
    DiagramCategory.UML_STRUCTURAL: [
        DiagramType.UML_CLASS,
        DiagramType.UML_OBJECT,
        DiagramType.UML_COMPONENT,
        DiagramType.UML_COMPOSITE,
        DiagramType.UML_DEPLOYMENT,
        DiagramType.UML_PACKAGE,
    ],
    # UML Behavioral
    DiagramCategory.UML_BEHAVIORAL: [
        DiagramType.UML_ACTIVITY,
        DiagramType.UML_STATE_MACHINE,
        DiagramType.UML_USE_CASE,
    ],
    # UML Interaction
    DiagramCategory.UML_INTERACTION: [
        DiagramType.UML_SEQUENCE,
        DiagramType.UML_COMMUNICATION,
        DiagramType.UML_TIMING,
        DiagramType.UML_INTERACTION_OVERVIEW,
    ],
    # Data Modeling
    DiagramCategory.DATA_MODELING: [
        DiagramType.ERD,
        DiagramType.ERD_CHEN,
        DiagramType.ERD_CROW_FOOT,
    ],
    # Data Flow
    DiagramCategory.DATA_FLOW: [
        DiagramType.DFD_CONTEXT,
        DiagramType.DFD_LEVEL0,
        DiagramType.DFD_LEVEL1,
        DiagramType.DFD_LEVEL2,
        DiagramType.DATA_LINEAGE,
    ],
    # Data Pipeline
    DiagramCategory.DATA_PIPELINE: [
        DiagramType.ETL_PIPELINE,
        DiagramType.ELT_PIPELINE,
        DiagramType.STREAMING_PIPELINE,
    ],
    # Data Warehouse
    DiagramCategory.DATA_WAREHOUSE: [
        DiagramType.STAR_SCHEMA,
        DiagramType.SNOWFLAKE_SCHEMA,
        DiagramType.DATA_VAULT,
    ],
    # Threat Modeling
    DiagramCategory.THREAT_MODELING: [
        DiagramType.STRIDE_THREAT_MODEL,
        DiagramType.ATTACK_TREE,
    ],
    # Security Architecture
    DiagramCategory.SECURITY_ARCHITECTURE: [
        DiagramType.ZERO_TRUST,
        DiagramType.SECURITY_ZONES,
        DiagramType.IAM_ARCHITECTURE,
        DiagramType.ENCRYPTION_FLOW,
    ],
    # Network Topology
    DiagramCategory.NETWORK_TOPOLOGY: [
        DiagramType.NETWORK_STAR,
        DiagramType.NETWORK_MESH,
        DiagramType.NETWORK_RING,
        DiagramType.NETWORK_TREE,
        DiagramType.NETWORK_HYBRID,
        DiagramType.VPC_DIAGRAM,
        DiagramType.SUBNET_DIAGRAM,
        DiagramType.VLAN_DIAGRAM,
    ],
    # Network Security
    DiagramCategory.NETWORK_SECURITY: [
        DiagramType.FIREWALL_RULES,
        DiagramType.LOAD_BALANCER,
    ],
    # CI/CD
    DiagramCategory.CI_CD: [
        DiagramType.CI_CD_PIPELINE,
        DiagramType.DEPLOYMENT_PIPELINE,
        DiagramType.RELEASE_PIPELINE,
    ],
    # Container Orchestration
    DiagramCategory.CONTAINER_ORCHESTRATION: [
        DiagramType.KUBERNETES_CLUSTER,
        DiagramType.KUBERNETES_DEPLOYMENT,
        DiagramType.KUBERNETES_SERVICES,
        DiagramType.HELM_CHART,
        DiagramType.DOCKER_COMPOSE,
    ],
    # Infrastructure as Code
    DiagramCategory.INFRASTRUCTURE_AS_CODE: [
        DiagramType.TERRAFORM_GRAPH,
        DiagramType.ANSIBLE_PLAYBOOK,
    ],
    # GitOps
    DiagramCategory.GITOPS: [
        DiagramType.GITOPS_WORKFLOW,
        DiagramType.ARGOCD_FLOW,
    ],
    # Business Process
    DiagramCategory.BUSINESS_PROCESS: [
        DiagramType.BPMN_PROCESS,
        DiagramType.BPMN_COLLABORATION,
        DiagramType.BPMN_CHOREOGRAPHY,
        DiagramType.VALUE_STREAM_MAP,
    ],
    # Organizational
    DiagramCategory.ORGANIZATIONAL: [
        DiagramType.ORG_CHART,
        DiagramType.STAKEHOLDER_MAP,
    ],
    # Strategy
    DiagramCategory.STRATEGY: [
        DiagramType.CUSTOMER_JOURNEY,
        DiagramType.SWOT,
        DiagramType.PORTER_FIVE_FORCES,
    ],
    # AWS
    DiagramCategory.AWS_ARCHITECTURE: [
        DiagramType.AWS_REFERENCE,
        DiagramType.AWS_WELL_ARCHITECTED,
        DiagramType.AWS_SERVERLESS,
        DiagramType.AWS_MICROSERVICES,
    ],
    # GCP
    DiagramCategory.GCP_ARCHITECTURE: [
        DiagramType.GCP_REFERENCE,
        DiagramType.GCP_ANTHOS,
    ],
    # Azure
    DiagramCategory.AZURE_ARCHITECTURE: [
        DiagramType.AZURE_REFERENCE,
        DiagramType.AZURE_LANDING_ZONE,
    ],
    # Multi-cloud
    DiagramCategory.MULTI_CLOUD: [
        DiagramType.MULTI_CLOUD_ARCH,
    ],
    # Microservices
    DiagramCategory.MICROSERVICES: [
        DiagramType.MICROSERVICES_ARCH,
        DiagramType.API_GATEWAY,
        DiagramType.SERVICE_MESH,
    ],
    # Event Driven
    DiagramCategory.EVENT_DRIVEN: [
        DiagramType.EVENT_SOURCING,
        DiagramType.CQRS,
        DiagramType.SAGA_PATTERN,
    ],
    # Message Queue
    DiagramCategory.MESSAGE_QUEUE: [
        DiagramType.MESSAGE_BROKER,
        DiagramType.PUB_SUB,
    ],
}


# Keywords for classification
DIAGRAM_KEYWORDS: Dict[DiagramType, Set[str]] = {
    # C4
    DiagramType.C4_CONTEXT: {"c4", "context", "system context", "high-level", "bird's eye"},
    DiagramType.C4_CONTAINER: {"container", "c4 container", "applications", "services"},
    DiagramType.C4_COMPONENT: {"component", "c4 component", "modules", "internal"},
    DiagramType.C4_CODE: {"code", "c4 code", "classes", "implementation"},

    # UML
    DiagramType.UML_CLASS: {"class diagram", "classes", "inheritance", "uml class", "oop"},
    DiagramType.UML_SEQUENCE: {"sequence", "sequence diagram", "interactions", "messages", "call flow"},
    DiagramType.UML_ACTIVITY: {"activity", "activity diagram", "workflow", "process flow"},
    DiagramType.UML_STATE_MACHINE: {"state", "state machine", "states", "transitions", "fsm"},
    DiagramType.UML_USE_CASE: {"use case", "actors", "user stories"},
    DiagramType.UML_COMPONENT: {"uml component", "component diagram"},
    DiagramType.UML_DEPLOYMENT: {"deployment diagram", "uml deployment"},

    # Data
    DiagramType.ERD: {"erd", "entity relationship", "entities", "database schema", "tables"},
    DiagramType.DFD_CONTEXT: {"dfd", "data flow", "context diagram"},
    DiagramType.DFD_LEVEL0: {"dfd level 0", "level-0 dfd"},
    DiagramType.DATA_LINEAGE: {"lineage", "data lineage", "data flow", "provenance", "traceability"},
    DiagramType.STAR_SCHEMA: {"star schema", "fact table", "dimensions", "data warehouse"},
    DiagramType.SNOWFLAKE_SCHEMA: {"snowflake schema", "normalized dimensions"},
    DiagramType.ETL_PIPELINE: {"etl", "extract transform load", "data pipeline"},
    DiagramType.ELT_PIPELINE: {"elt", "extract load transform"},
    DiagramType.STREAMING_PIPELINE: {"streaming", "kafka", "real-time", "event stream"},

    # Security
    DiagramType.STRIDE_THREAT_MODEL: {"stride", "threat model", "threats", "vulnerabilities"},
    DiagramType.ATTACK_TREE: {"attack tree", "attack vector", "threat tree"},
    DiagramType.ZERO_TRUST: {"zero trust", "never trust", "verify always"},
    DiagramType.SECURITY_ZONES: {"security zones", "dmz", "trust zones"},

    # Network
    DiagramType.NETWORK_STAR: {"star topology", "hub and spoke", "central node"},
    DiagramType.NETWORK_MESH: {"mesh topology", "full mesh", "partial mesh"},
    DiagramType.VPC_DIAGRAM: {"vpc", "virtual private cloud", "subnets"},
    DiagramType.VLAN_DIAGRAM: {"vlan", "virtual lan", "network segmentation"},

    # DevOps
    DiagramType.CI_CD_PIPELINE: {"ci/cd", "cicd", "pipeline", "continuous integration", "continuous delivery"},
    DiagramType.KUBERNETES_CLUSTER: {"kubernetes", "k8s", "cluster", "nodes", "pods"},
    DiagramType.KUBERNETES_DEPLOYMENT: {"k8s deployment", "kubernetes deployment", "replicas"},
    DiagramType.DOCKER_COMPOSE: {"docker compose", "docker-compose", "multi-container"},
    DiagramType.TERRAFORM_GRAPH: {"terraform", "infrastructure as code", "iac"},
    DiagramType.GITOPS_WORKFLOW: {"gitops", "git ops", "argocd", "flux"},

    # Business
    DiagramType.BPMN_PROCESS: {"bpmn", "business process", "workflow"},
    DiagramType.ORG_CHART: {"org chart", "organization chart", "hierarchy", "reporting structure"},
    DiagramType.VALUE_STREAM_MAP: {"value stream", "vsm", "lean"},
    DiagramType.CUSTOMER_JOURNEY: {"customer journey", "user journey", "touchpoints"},

    # Cloud
    DiagramType.AWS_REFERENCE: {"aws", "amazon web services", "aws architecture"},
    DiagramType.AWS_SERVERLESS: {"serverless", "lambda", "aws lambda"},
    DiagramType.GCP_REFERENCE: {"gcp", "google cloud", "gcp architecture"},
    DiagramType.AZURE_REFERENCE: {"azure", "microsoft azure", "azure architecture"},

    # Integration
    DiagramType.MICROSERVICES_ARCH: {"microservices", "micro-services", "distributed"},
    DiagramType.API_GATEWAY: {"api gateway", "api management", "api routing"},
    DiagramType.SERVICE_MESH: {"service mesh", "istio", "linkerd", "envoy"},
    DiagramType.EVENT_SOURCING: {"event sourcing", "event store"},
    DiagramType.CQRS: {"cqrs", "command query", "read model", "write model"},
    DiagramType.MESSAGE_BROKER: {"message broker", "rabbitmq", "activemq"},
    DiagramType.PUB_SUB: {"pub/sub", "publish subscribe", "pubsub"},

    # Generic
    DiagramType.FLOWCHART: {"flowchart", "flow chart", "decision tree"},
    DiagramType.MIND_MAP: {"mind map", "brainstorm", "ideas"},
    DiagramType.BLOCK_DIAGRAM: {"block diagram", "blocks", "system diagram"},
    DiagramType.HIERARCHY: {"hierarchy", "tree", "parent child"},
}


# Recommended layouts per diagram type
DIAGRAM_LAYOUTS: Dict[DiagramType, str] = {
    # C4 - Hierarchical
    DiagramType.C4_CONTEXT: "vertical",
    DiagramType.C4_CONTAINER: "vertical",
    DiagramType.C4_COMPONENT: "graphviz",
    DiagramType.C4_CODE: "graphviz",

    # UML
    DiagramType.UML_CLASS: "graphviz",
    DiagramType.UML_SEQUENCE: "vertical",
    DiagramType.UML_ACTIVITY: "vertical",
    DiagramType.UML_STATE_MACHINE: "graphviz",
    DiagramType.UML_USE_CASE: "radial",

    # Data
    DiagramType.ERD: "graphviz",
    DiagramType.DFD_CONTEXT: "radial",
    DiagramType.DATA_LINEAGE: "horizontal",
    DiagramType.ETL_PIPELINE: "horizontal",
    DiagramType.STAR_SCHEMA: "radial",

    # Security
    DiagramType.STRIDE_THREAT_MODEL: "graphviz",
    DiagramType.ZERO_TRUST: "radial",
    DiagramType.SECURITY_ZONES: "vertical",

    # Network
    DiagramType.NETWORK_STAR: "radial",
    DiagramType.NETWORK_MESH: "graphviz",
    DiagramType.VPC_DIAGRAM: "vertical",

    # DevOps
    DiagramType.CI_CD_PIPELINE: "horizontal",
    DiagramType.KUBERNETES_CLUSTER: "vertical",
    DiagramType.GITOPS_WORKFLOW: "horizontal",

    # Business
    DiagramType.BPMN_PROCESS: "horizontal",
    DiagramType.ORG_CHART: "vertical",
    DiagramType.VALUE_STREAM_MAP: "horizontal",

    # Integration
    DiagramType.MICROSERVICES_ARCH: "graphviz",
    DiagramType.SERVICE_MESH: "graphviz",
    DiagramType.MESSAGE_BROKER: "radial",
}


# Maximum recommended elements per diagram type
DIAGRAM_MAX_ELEMENTS: Dict[DiagramType, int] = {
    DiagramType.C4_CONTEXT: 8,
    DiagramType.C4_CONTAINER: 12,
    DiagramType.C4_COMPONENT: 15,
    DiagramType.UML_CLASS: 10,
    DiagramType.UML_SEQUENCE: 8,
    DiagramType.ERD: 12,
    DiagramType.DFD_CONTEXT: 6,
    DiagramType.DATA_LINEAGE: 15,
    DiagramType.KUBERNETES_CLUSTER: 12,
    DiagramType.MICROSERVICES_ARCH: 10,
}


def get_domain_for_category(category: DiagramCategory) -> DiagramDomain:
    """Get the domain for a given category"""
    for domain, categories in DOMAIN_CATEGORIES.items():
        if category in categories:
            return domain
    return DiagramDomain.ARCHITECTURE  # Default


def get_category_for_type(diagram_type: DiagramType) -> DiagramCategory:
    """Get the category for a given diagram type"""
    for category, types in CATEGORY_TYPES.items():
        if diagram_type in types:
            return category
    return DiagramCategory.SOLUTION_ARCHITECTURE  # Default
