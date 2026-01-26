"""Tests for core diagram functionality"""

import pytest
from viralify_diagrams import Diagram, Node, Edge
from viralify_diagrams.core.diagram import NodeShape, EdgeStyle, EdgeDirection


class TestDiagram:
    """Tests for Diagram class"""

    def test_create_empty_diagram(self):
        """Test creating an empty diagram"""
        diagram = Diagram(title="Test", description="Test diagram")
        assert diagram.title == "Test"
        assert diagram.description == "Test diagram"
        assert len(diagram.nodes) == 0
        assert len(diagram.edges) == 0
        assert len(diagram.clusters) == 0

    def test_add_node(self):
        """Test adding nodes to diagram"""
        diagram = Diagram(title="Test")
        node = diagram.add_node("node1", "Node 1", description="First node")

        assert len(diagram.nodes) == 1
        assert node.id == "node1"
        assert node.label == "Node 1"
        assert node.description == "First node"

    def test_add_node_with_shape(self):
        """Test adding nodes with different shapes"""
        diagram = Diagram(title="Test")
        node = diagram.add_node("db", "Database", shape=NodeShape.CYLINDER)

        assert node.shape == NodeShape.CYLINDER

    def test_add_edge(self):
        """Test adding edges between nodes"""
        diagram = Diagram(title="Test")
        diagram.add_node("a", "Node A")
        diagram.add_node("b", "Node B")
        edge = diagram.add_edge("a", "b", label="Connection")

        assert len(diagram.edges) == 1
        assert edge.source == "a"
        assert edge.target == "b"
        assert edge.label == "Connection"

    def test_add_cluster(self):
        """Test adding clusters"""
        diagram = Diagram(title="Test")
        diagram.add_node("a", "Node A")
        diagram.add_node("b", "Node B")
        diagram.add_node("c", "Node C")
        cluster = diagram.add_cluster("grp", "Group", ["a", "b"])

        assert len(diagram.clusters) == 1
        assert cluster.id == "grp"
        assert cluster.label == "Group"
        assert cluster.node_ids == ["a", "b"]

    def test_get_node(self):
        """Test retrieving nodes by ID"""
        diagram = Diagram(title="Test")
        diagram.add_node("test", "Test Node")

        node = diagram.get_node("test")
        assert node is not None
        assert node.label == "Test Node"

        missing = diagram.get_node("nonexistent")
        assert missing is None

    def test_simplify(self):
        """Test diagram simplification"""
        diagram = Diagram(title="Test")
        for i in range(20):
            diagram.add_node(f"node{i}", f"Node {i}")

        assert len(diagram.nodes) == 20

        diagram.simplify(max_nodes=10)
        assert len(diagram.nodes) == 10

    def test_assign_animation_order(self):
        """Test animation order assignment"""
        diagram = Diagram(title="Test")
        diagram.add_node("a", "A")
        diagram.add_node("b", "B")
        diagram.add_node("c", "C")
        diagram.add_edge("a", "b")
        diagram.add_edge("b", "c")

        diagram.assign_animation_order()

        # Source nodes should come first
        node_a = diagram.get_node("a")
        node_b = diagram.get_node("b")
        node_c = diagram.get_node("c")

        assert node_a.order < node_b.order
        assert node_b.order < node_c.order


class TestNode:
    """Tests for Node class"""

    def test_node_center(self):
        """Test node center calculation"""
        from viralify_diagrams.core.diagram import Position, Size

        node = Node(
            id="test",
            label="Test",
            position=Position(100, 100),
            size=Size(80, 40)
        )

        center = node.center
        assert center.x == 140  # 100 + 80/2
        assert center.y == 120  # 100 + 40/2

    def test_node_defaults(self):
        """Test node default values"""
        node = Node(id="test", label="Test")

        assert node.shape == NodeShape.ROUNDED
        assert node.order == 0
        assert node.fill_color is None
        assert node.stroke_color is None


class TestEdge:
    """Tests for Edge class"""

    def test_edge_defaults(self):
        """Test edge default values"""
        edge = Edge(id="e1", source="a", target="b")

        assert edge.style == EdgeStyle.SOLID
        assert edge.direction == EdgeDirection.FORWARD
        assert edge.label is None
        assert edge.color is None

    def test_edge_with_style(self):
        """Test edge with custom style"""
        edge = Edge(
            id="e1",
            source="a",
            target="b",
            style=EdgeStyle.DASHED,
            direction=EdgeDirection.BOTH
        )

        assert edge.style == EdgeStyle.DASHED
        assert edge.direction == EdgeDirection.BOTH
