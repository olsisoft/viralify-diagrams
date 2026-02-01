"""
Kubernetes Architecture Template

Kubernetes cluster architecture and workloads:
- Cluster components (control plane, nodes)
- Workloads (Pods, Deployments, Services)
- Networking (Ingress, Services, Network Policies)
- Storage (PV, PVC, StorageClass)
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
# Kubernetes Elements
# =============================================================================

K8S_CLUSTER = TemplateElement(
    id="cluster",
    name="Cluster",
    description="Kubernetes cluster",
    shape=ElementShape.RECTANGLE,
    default_color="#FFFFFF",
    default_stroke="#326CE5",
    required_fields=["name"],
    optional_fields=["provider", "version"],
    allow_nesting=True,
    nested_types=["namespace", "node"],
)

K8S_NAMESPACE = TemplateElement(
    id="namespace",
    name="Namespace",
    description="Kubernetes namespace for isolation",
    shape=ElementShape.RECTANGLE,
    default_color="#F5F5F5",
    default_stroke="#666666",
    required_fields=["name"],
    allow_nesting=True,
    nested_types=["pod", "deployment", "service", "configmap", "secret", "pvc"],
)

K8S_NODE = TemplateElement(
    id="node",
    name="Node",
    description="Worker or control plane node",
    shape=ElementShape.SERVER,
    default_color="#E6F3FF",
    default_stroke="#326CE5",
    required_fields=["name"],
    optional_fields=["role", "instance_type", "capacity"],
    allow_nesting=True,
    nested_types=["pod"],
)

K8S_POD = TemplateElement(
    id="pod",
    name="Pod",
    description="Smallest deployable unit",
    shape=ElementShape.POD,
    default_color="#FFFFFF",
    default_stroke="#326CE5",
    required_fields=["name"],
    optional_fields=["containers", "replicas", "status"],
    allow_nesting=True,
    nested_types=["container"],
)

K8S_CONTAINER = TemplateElement(
    id="container",
    name="Container",
    description="Container within a pod",
    shape=ElementShape.CONTAINER,
    default_color="#E6FFE6",
    default_stroke="#059669",
    required_fields=["name", "image"],
    optional_fields=["ports", "resources"],
)

K8S_DEPLOYMENT = TemplateElement(
    id="deployment",
    name="Deployment",
    description="Manages ReplicaSets and Pods",
    shape=ElementShape.ROUNDED,
    default_color="#E6F3FF",
    default_stroke="#326CE5",
    required_fields=["name"],
    optional_fields=["replicas", "strategy", "selector"],
)

K8S_STATEFULSET = TemplateElement(
    id="statefulset",
    name="StatefulSet",
    description="Manages stateful applications",
    shape=ElementShape.ROUNDED,
    default_color="#FFE6CC",
    default_stroke="#D97706",
    required_fields=["name"],
    optional_fields=["replicas", "storage"],
)

K8S_DAEMONSET = TemplateElement(
    id="daemonset",
    name="DaemonSet",
    description="Runs pod on every node",
    shape=ElementShape.ROUNDED,
    default_color="#E6E6FA",
    default_stroke="#6A5ACD",
    required_fields=["name"],
)

K8S_SERVICE = TemplateElement(
    id="service",
    name="Service",
    description="Network service abstraction",
    shape=ElementShape.HEXAGON,
    default_color="#326CE5",
    default_stroke="#1A4BA0",
    required_fields=["name"],
    optional_fields=["type", "ports", "selector"],
)

K8S_INGRESS = TemplateElement(
    id="ingress",
    name="Ingress",
    description="HTTP/HTTPS routing",
    shape=ElementShape.TRAPEZOID,
    default_color="#FFE082",
    default_stroke="#F57C00",
    required_fields=["name"],
    optional_fields=["host", "paths", "tls"],
)

K8S_CONFIGMAP = TemplateElement(
    id="configmap",
    name="ConfigMap",
    description="Configuration data",
    shape=ElementShape.FILE,
    default_color="#FFFACD",
    default_stroke="#B8860B",
    required_fields=["name"],
)

K8S_SECRET = TemplateElement(
    id="secret",
    name="Secret",
    description="Sensitive configuration data",
    shape=ElementShape.FILE,
    default_color="#FCE4EC",
    default_stroke="#C2185B",
    required_fields=["name"],
    optional_fields=["type"],
)

K8S_PV = TemplateElement(
    id="pv",
    name="PersistentVolume",
    description="Cluster storage resource",
    shape=ElementShape.CYLINDER,
    default_color="#FFF3E0",
    default_stroke="#E65100",
    required_fields=["name"],
    optional_fields=["capacity", "storage_class"],
)

K8S_PVC = TemplateElement(
    id="pvc",
    name="PersistentVolumeClaim",
    description="Storage request by pod",
    shape=ElementShape.CYLINDER,
    default_color="#E3F2FD",
    default_stroke="#1565C0",
    required_fields=["name"],
    optional_fields=["size", "storage_class"],
)

K8S_HPA = TemplateElement(
    id="hpa",
    name="HorizontalPodAutoscaler",
    description="Automatic pod scaling",
    shape=ElementShape.DIAMOND,
    default_color="#E8F5E9",
    default_stroke="#2E7D32",
    required_fields=["name", "target"],
    optional_fields=["min_replicas", "max_replicas", "metrics"],
)

K8S_NETWORK_POLICY = TemplateElement(
    id="network_policy",
    name="NetworkPolicy",
    description="Pod network access rules",
    shape=ElementShape.HEXAGON,
    default_color="#FFEBEE",
    default_stroke="#C62828",
    required_fields=["name"],
    optional_fields=["ingress", "egress"],
)

K8S_EXTERNAL = TemplateElement(
    id="external",
    name="External Resource",
    description="External service or database",
    shape=ElementShape.CLOUD,
    default_color="#E0E0E0",
    default_stroke="#616161",
    required_fields=["name"],
    optional_fields=["type", "endpoint"],
)


# =============================================================================
# Kubernetes Relations
# =============================================================================

K8S_MANAGES = TemplateRelation(
    id="manages",
    name="Manages",
    relation_type=RelationType.DEPENDS_ON,
    description="Controller manages resource",
    line_style="solid",
    arrow_style="filled",
)

K8S_EXPOSES = TemplateRelation(
    id="exposes",
    name="Exposes",
    relation_type=RelationType.CONNECTS_TO,
    description="Service exposes pods",
    line_style="solid",
    arrow_style="open",
)

K8S_ROUTES_TO = TemplateRelation(
    id="routes_to",
    name="Routes To",
    relation_type=RelationType.FLOW,
    description="Ingress routes to service",
    line_style="solid",
    arrow_style="open",
)

K8S_MOUNTS = TemplateRelation(
    id="mounts",
    name="Mounts",
    relation_type=RelationType.USES,
    description="Pod mounts volume",
    line_style="dashed",
    arrow_style="open",
)

K8S_USES_CONFIG = TemplateRelation(
    id="uses_config",
    name="Uses Config",
    relation_type=RelationType.READS_FROM,
    description="Pod uses ConfigMap/Secret",
    line_style="dotted",
    arrow_style="open",
)

K8S_SCALES = TemplateRelation(
    id="scales",
    name="Scales",
    relation_type=RelationType.DEPENDS_ON,
    description="HPA scales deployment",
    line_style="dashed",
    arrow_style="filled",
)

K8S_CALLS = TemplateRelation(
    id="calls",
    name="Calls",
    relation_type=RelationType.CALLS,
    description="Service calls another service",
    line_style="solid",
    arrow_style="open",
)

K8S_NETWORK_ACCESS = TemplateRelation(
    id="network_access",
    name="Network Access",
    relation_type=RelationType.CONNECTS_TO,
    description="Network policy allows traffic",
    line_style="solid",
    arrow_style="both",
)


# =============================================================================
# Kubernetes Template
# =============================================================================

class KubernetesTemplate(DiagramTemplate):
    """
    Kubernetes Architecture Template.

    Shows Kubernetes cluster architecture and workloads.

    View types:
    - Cluster view: Nodes, control plane components
    - Namespace view: Workloads in a namespace
    - Network view: Services, ingress, network policies
    - Storage view: PVs, PVCs, StorageClasses

    Best practices:
    - Group by namespace
    - Show service mesh if applicable
    - Include external dependencies
    - Show HPA for scalable workloads
    """

    def __init__(self):
        config = TemplateConfig(
            template_id="kubernetes",
            name="Kubernetes Architecture",
            description="Kubernetes cluster and workload architecture",
            version="1.0.0",
            domain="devops",
            category="container_orchestration",
            diagram_type="kubernetes_cluster",
            elements=[
                K8S_CLUSTER,
                K8S_NAMESPACE,
                K8S_NODE,
                K8S_POD,
                K8S_CONTAINER,
                K8S_DEPLOYMENT,
                K8S_STATEFULSET,
                K8S_DAEMONSET,
                K8S_SERVICE,
                K8S_INGRESS,
                K8S_CONFIGMAP,
                K8S_SECRET,
                K8S_PV,
                K8S_PVC,
                K8S_HPA,
                K8S_NETWORK_POLICY,
                K8S_EXTERNAL,
            ],
            relations=[
                K8S_MANAGES,
                K8S_EXPOSES,
                K8S_ROUTES_TO,
                K8S_MOUNTS,
                K8S_USES_CONFIG,
                K8S_SCALES,
                K8S_CALLS,
                K8S_NETWORK_ACCESS,
            ],
            constraints=[
                TemplateConstraint(
                    id="deployment_has_service",
                    name="Deployment Has Service",
                    description="Deployments should have a service",
                    validator=lambda d: self._validate_deployment_service(d),
                    severity="info",
                ),
                TemplateConstraint(
                    id="prod_has_hpa",
                    name="Production Has HPA",
                    description="Production workloads should have HPA",
                    validator=lambda d: self._validate_prod_hpa(d),
                    severity="info",
                ),
            ],
            max_elements=50,
            max_relations=80,
            max_nesting_depth=4,
            default_layout="graphviz",
            default_theme="corporate",
            icon_set="k8s",
        )
        super().__init__(config)

    def _validate_deployment_service(self, diagram) -> List[str]:
        """Validate deployments have services"""
        deployments = [n.id for n in diagram.nodes
                      if getattr(n, 'element_type', '') == 'deployment']

        orphan_deployments = []
        for dep_id in deployments:
            has_service = any(
                getattr(e, 'relation_type', '') == 'exposes'
                and (e.target == dep_id or e.source == dep_id)
                for e in diagram.edges
            )
            if not has_service:
                orphan_deployments.append(dep_id)

        if orphan_deployments:
            return [f"Deployments without services: {', '.join(orphan_deployments[:3])}"]
        return []

    def _validate_prod_hpa(self, diagram) -> List[str]:
        """Validate production deployments have HPA"""
        # This is a simplified check - in practice, check namespace labels
        deployments = [n.id for n in diagram.nodes
                      if getattr(n, 'element_type', '') == 'deployment']

        hpa_targets = set()
        for node in diagram.nodes:
            if getattr(node, 'element_type', '') == 'hpa':
                props = getattr(node, 'properties', {})
                if props.get('target'):
                    hpa_targets.add(props['target'])

        no_hpa = [d for d in deployments if d not in hpa_targets]
        if no_hpa:
            return [f"Consider adding HPA for: {', '.join(no_hpa[:3])}"]
        return []

    def create_element(
        self,
        element_type: str,
        label: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a Kubernetes element"""
        props = properties or {}

        element_def = self.get_element_definition(element_type)
        if not element_def:
            raise ValueError(f"Unknown element type: {element_type}")

        element = {
            "id": props.get("id", label.lower().replace(" ", "_").replace("-", "_")),
            "label": label,
            "element_type": element_type,
            "shape": element_def.shape.value,
            "fill_color": props.get("color", element_def.default_color),
            "stroke_color": element_def.default_stroke,
            "properties": props,
        }

        # Add type-specific properties
        if element_type == "cluster":
            element["provider"] = props.get("provider")  # EKS, GKE, AKS, on-prem
            element["version"] = props.get("version")

        elif element_type == "node":
            element["role"] = props.get("role", "worker")  # control-plane, worker
            element["instance_type"] = props.get("instance_type")
            element["capacity"] = props.get("capacity")

        elif element_type == "pod":
            element["containers"] = props.get("containers", [])
            element["replicas"] = props.get("replicas", 1)
            element["status"] = props.get("status", "Running")

        elif element_type == "container":
            element["image"] = props.get("image")
            element["ports"] = props.get("ports", [])
            element["resources"] = props.get("resources", {})

        elif element_type in ["deployment", "statefulset"]:
            element["replicas"] = props.get("replicas", 1)
            element["strategy"] = props.get("strategy")
            element["selector"] = props.get("selector")

        elif element_type == "service":
            element["service_type"] = props.get("type", "ClusterIP")
            element["ports"] = props.get("ports", [])
            element["selector"] = props.get("selector")

        elif element_type == "ingress":
            element["host"] = props.get("host")
            element["paths"] = props.get("paths", [])
            element["tls"] = props.get("tls")

        elif element_type in ["pv", "pvc"]:
            element["capacity"] = props.get("capacity") or props.get("size")
            element["storage_class"] = props.get("storage_class")

        elif element_type == "hpa":
            element["target"] = props.get("target")
            element["min_replicas"] = props.get("min_replicas", 1)
            element["max_replicas"] = props.get("max_replicas", 10)
            element["metrics"] = props.get("metrics", [])

        return element

    def create_relation(
        self,
        relation_type: str,
        source_id: str,
        target_id: str,
        label: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a Kubernetes relation"""
        relation_def = self.get_relation_definition(relation_type)
        if not relation_def:
            relation_def = K8S_MANAGES

        props = properties or {}

        return {
            "source": source_id,
            "target": target_id,
            "label": label or "",
            "relation_type": relation_type,
            "line_style": relation_def.line_style,
            "arrow_style": relation_def.arrow_style,
            "port": props.get("port"),
            "protocol": props.get("protocol"),
            "properties": props,
        }
