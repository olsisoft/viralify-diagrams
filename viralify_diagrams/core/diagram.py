"""
Core Diagram Components

Provides Node, Edge, Cluster, and Diagram classes for building diagrams.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union, Tuple
from enum import Enum
import uuid


class NodeShape(str, Enum):
    """Available node shapes"""
    RECTANGLE = "rectangle"
    ROUNDED = "rounded"
    CIRCLE = "circle"
    DIAMOND = "diamond"
    HEXAGON = "hexagon"
    CYLINDER = "cylinder"  # For databases
    PARALLELOGRAM = "parallelogram"  # For I/O
    CLOUD = "cloud"  # For cloud services


class EdgeStyle(str, Enum):
    """Edge line styles"""
    SOLID = "solid"
    DASHED = "dashed"
    DOTTED = "dotted"


class EdgeDirection(str, Enum):
    """Edge arrow directions"""
    FORWARD = "forward"  # ->
    BACKWARD = "backward"  # <-
    BOTH = "both"  # <->
    NONE = "none"  # --


@dataclass
class Position:
    """2D position"""
    x: float = 0.0
    y: float = 0.0

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(self.x - other.x, self.y - other.y)

    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)


@dataclass
class Size:
    """2D size"""
    width: float = 120.0
    height: float = 80.0

    def to_tuple(self) -> Tuple[float, float]:
        return (self.width, self.height)


@dataclass
class Node:
    """
    A node in the diagram.

    Attributes:
        id: Unique identifier
        label: Display label (auto-truncated if too long)
        icon: Icon identifier (e.g., "aws/compute/ec2")
        shape: Node shape
        position: Position in the diagram (set by layout)
        size: Node dimensions
        metadata: Custom metadata for narration
        order: Reveal order for animations (lower = earlier)
    """
    label: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    icon: Optional[str] = None
    shape: NodeShape = NodeShape.ROUNDED
    position: Position = field(default_factory=Position)
    size: Size = field(default_factory=Size)
    metadata: Dict[str, Any] = field(default_factory=dict)
    order: int = 0  # Animation order
    group: Optional[str] = None  # SVG group ID
    description: str = ""  # For narration

    # Style overrides (None = use theme)
    fill_color: Optional[str] = None
    stroke_color: Optional[str] = None
    text_color: Optional[str] = None

    def __post_init__(self):
        # Auto-truncate long labels
        if len(self.label) > 20:
            self.label = self.label[:17] + "..."

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "label": self.label,
            "icon": self.icon,
            "shape": self.shape.value,
            "position": {"x": self.position.x, "y": self.position.y},
            "size": {"width": self.size.width, "height": self.size.height},
            "metadata": self.metadata,
            "order": self.order,
            "group": self.group,
            "description": self.description,
            "fill_color": self.fill_color,
            "stroke_color": self.stroke_color,
            "text_color": self.text_color,
        }

    @property
    def center(self) -> Position:
        """Get center position of node"""
        return Position(
            self.position.x + self.size.width / 2,
            self.position.y + self.size.height / 2
        )

    @property
    def bounds(self) -> Tuple[float, float, float, float]:
        """Get bounding box (x, y, width, height)"""
        return (self.position.x, self.position.y, self.size.width, self.size.height)


@dataclass
class Edge:
    """
    An edge connecting two nodes.

    Attributes:
        source: Source node ID
        target: Target node ID
        label: Optional edge label
        style: Line style
        direction: Arrow direction
        order: Reveal order for animations
    """
    source: str  # Node ID
    target: str  # Node ID
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    label: Optional[str] = None
    style: EdgeStyle = EdgeStyle.SOLID
    direction: EdgeDirection = EdgeDirection.FORWARD
    order: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    description: str = ""  # For narration

    # Control points for curved edges (set by layout)
    control_points: List[Position] = field(default_factory=list)

    # Style overrides
    color: Optional[str] = None
    width: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "source": self.source,
            "target": self.target,
            "label": self.label,
            "style": self.style.value,
            "direction": self.direction.value,
            "order": self.order,
            "metadata": self.metadata,
            "description": self.description,
            "control_points": [{"x": p.x, "y": p.y} for p in self.control_points],
            "color": self.color,
            "width": self.width,
        }


@dataclass
class Cluster:
    """
    A cluster (group) of nodes.

    Attributes:
        id: Unique identifier
        label: Display label
        nodes: List of node IDs in this cluster
        position: Position (set by layout)
        size: Size (calculated from contained nodes)
    """
    label: str
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    nodes: List[str] = field(default_factory=list)  # Node IDs
    position: Position = field(default_factory=Position)
    size: Size = field(default_factory=Size)
    order: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    description: str = ""

    # Nested clusters
    clusters: List["Cluster"] = field(default_factory=list)

    # Style overrides
    fill_color: Optional[str] = None
    stroke_color: Optional[str] = None
    label_color: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "label": self.label,
            "nodes": self.nodes,
            "position": {"x": self.position.x, "y": self.position.y},
            "size": {"width": self.size.width, "height": self.size.height},
            "order": self.order,
            "metadata": self.metadata,
            "description": self.description,
            "clusters": [c.to_dict() for c in self.clusters],
            "fill_color": self.fill_color,
            "stroke_color": self.stroke_color,
            "label_color": self.label_color,
        }

    def add_node(self, node_id: str) -> None:
        """Add a node to this cluster"""
        if node_id not in self.nodes:
            self.nodes.append(node_id)

    def add_cluster(self, cluster: "Cluster") -> None:
        """Add a nested cluster"""
        self.clusters.append(cluster)


@dataclass
class Diagram:
    """
    Main diagram container.

    Attributes:
        title: Diagram title
        nodes: All nodes
        edges: All edges
        clusters: All clusters
        theme: Theme name or Theme object
        layout: Layout name
    """
    title: str = "Diagram"
    description: str = ""
    nodes: List[Node] = field(default_factory=list)
    edges: List[Edge] = field(default_factory=list)
    clusters: List[Cluster] = field(default_factory=list)
    theme: str = "dark"
    layout: str = "horizontal"

    # Canvas settings
    width: int = 1920
    height: int = 1080
    padding: int = 50

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Maximum nodes for auto-simplification
    max_nodes: int = 10

    def __post_init__(self):
        self._node_map: Dict[str, Node] = {}
        self._rebuild_node_map()

    def _rebuild_node_map(self) -> None:
        """Rebuild the node ID to node mapping"""
        self._node_map = {node.id: node for node in self.nodes}

    def add_node(self, node: Node) -> Node:
        """Add a node to the diagram"""
        self.nodes.append(node)
        self._node_map[node.id] = node
        return node

    def add_edge(self, edge: Edge) -> Edge:
        """Add an edge to the diagram"""
        self.edges.append(edge)
        return edge

    def add_cluster(self, cluster: Cluster) -> Cluster:
        """Add a cluster to the diagram"""
        self.clusters.append(cluster)
        return cluster

    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node by ID"""
        return self._node_map.get(node_id)

    def connect(
        self,
        source: Union[str, Node],
        target: Union[str, Node],
        label: Optional[str] = None,
        style: EdgeStyle = EdgeStyle.SOLID,
        direction: EdgeDirection = EdgeDirection.FORWARD,
    ) -> Edge:
        """Connect two nodes with an edge"""
        source_id = source.id if isinstance(source, Node) else source
        target_id = target.id if isinstance(target, Node) else target

        edge = Edge(
            source=source_id,
            target=target_id,
            label=label,
            style=style,
            direction=direction,
        )
        return self.add_edge(edge)

    def should_simplify(self) -> bool:
        """Check if diagram needs simplification"""
        return len(self.nodes) > self.max_nodes

    def simplify(self) -> "Diagram":
        """
        Create a simplified version of the diagram.
        Groups similar nodes and reduces complexity.
        """
        if not self.should_simplify():
            return self

        # Group nodes by icon/type
        groups: Dict[str, List[Node]] = {}
        for node in self.nodes:
            key = node.icon or node.shape.value
            if key not in groups:
                groups[key] = []
            groups[key].append(node)

        # Create simplified diagram
        simplified = Diagram(
            title=self.title,
            description=self.description,
            theme=self.theme,
            layout=self.layout,
            width=self.width,
            height=self.height,
            padding=self.padding,
            max_nodes=self.max_nodes,
        )

        # Keep individual nodes up to max, then group the rest
        kept_count = 0
        for key, group_nodes in sorted(groups.items(), key=lambda x: -len(x[1])):
            if kept_count < self.max_nodes - 1:
                # Keep individual nodes
                for node in group_nodes[:max(1, self.max_nodes - kept_count - 1)]:
                    simplified.add_node(node)
                    kept_count += 1
            else:
                # Group remaining nodes
                if len(group_nodes) > 1:
                    grouped = Node(
                        label=f"{group_nodes[0].label} (+{len(group_nodes) - 1})",
                        icon=group_nodes[0].icon,
                        shape=group_nodes[0].shape,
                        description=f"Group of {len(group_nodes)} similar components",
                    )
                    simplified.add_node(grouped)
                else:
                    simplified.add_node(group_nodes[0])
                break

        # Rebuild edges for kept nodes
        kept_ids = {n.id for n in simplified.nodes}
        for edge in self.edges:
            if edge.source in kept_ids and edge.target in kept_ids:
                simplified.add_edge(edge)

        return simplified

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "title": self.title,
            "description": self.description,
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": [e.to_dict() for e in self.edges],
            "clusters": [c.to_dict() for c in self.clusters],
            "theme": self.theme,
            "layout": self.layout,
            "width": self.width,
            "height": self.height,
            "padding": self.padding,
            "metadata": self.metadata,
            "max_nodes": self.max_nodes,
        }

    def get_render_order(self) -> List[Union[Node, Edge, Cluster]]:
        """
        Get all elements in render/animation order.
        Clusters first, then nodes, then edges.
        """
        elements: List[Union[Node, Edge, Cluster]] = []

        # Clusters first (background)
        elements.extend(sorted(self.clusters, key=lambda x: x.order))

        # Nodes
        elements.extend(sorted(self.nodes, key=lambda x: x.order))

        # Edges last (foreground)
        elements.extend(sorted(self.edges, key=lambda x: x.order))

        return elements

    def assign_animation_order(self) -> None:
        """
        Auto-assign animation order based on graph topology.
        Source nodes first, then follow edges.
        """
        # Find source nodes (no incoming edges)
        incoming = {node.id: 0 for node in self.nodes}
        for edge in self.edges:
            if edge.target in incoming:
                incoming[edge.target] += 1

        # BFS from sources
        sources = [nid for nid, count in incoming.items() if count == 0]
        if not sources:
            sources = [self.nodes[0].id] if self.nodes else []

        visited = set()
        order = 0
        queue = list(sources)

        while queue:
            node_id = queue.pop(0)
            if node_id in visited:
                continue

            visited.add(node_id)
            node = self.get_node(node_id)
            if node:
                node.order = order
                order += 1

            # Find outgoing edges and their targets
            for edge in self.edges:
                if edge.source == node_id:
                    edge.order = order
                    order += 1
                    if edge.target not in visited:
                        queue.append(edge.target)

        # Assign order to clusters based on their nodes
        for cluster in self.clusters:
            if cluster.nodes:
                min_order = min(
                    self.get_node(nid).order
                    for nid in cluster.nodes
                    if self.get_node(nid)
                )
                cluster.order = max(0, min_order - 1)
