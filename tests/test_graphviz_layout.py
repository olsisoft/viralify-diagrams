"""Tests for the GraphvizLayout hybrid approach"""

import pytest
from unittest.mock import patch, MagicMock

from viralify_diagrams import Diagram, GraphvizLayout, GraphvizAlgorithm, auto_layout


class TestGraphvizLayout:
    """Test suite for GraphvizLayout"""

    def test_layout_initialization(self):
        """Test that GraphvizLayout initializes correctly"""
        layout = GraphvizLayout()
        assert layout.algorithm == "dot"
        assert layout.rankdir == "TB"

    def test_layout_with_custom_algorithm(self):
        """Test custom algorithm selection"""
        layout = GraphvizLayout(algorithm="neato")
        assert layout.algorithm == "neato"

        layout = GraphvizLayout(algorithm="fdp", rankdir="LR")
        assert layout.algorithm == "fdp"
        assert layout.rankdir == "LR"

    def test_recommend_algorithm_dag(self):
        """Test algorithm recommendation for DAG"""
        diagram = Diagram(title="Test")
        diagram.add_node("a", "A")
        diagram.add_node("b", "B")
        diagram.add_node("c", "C")
        diagram.add_edge("a", "b")
        diagram.add_edge("b", "c")

        algorithm = GraphvizLayout.recommend_algorithm(diagram)
        assert algorithm == "dot"  # DAG should use dot

    def test_recommend_algorithm_large_graph(self):
        """Test algorithm recommendation for large graphs"""
        diagram = Diagram(title="Large Graph")

        # Create 150 nodes
        for i in range(150):
            diagram.add_node(f"node_{i}", f"Node {i}")

        # Add some edges
        for i in range(100):
            diagram.add_edge(f"node_{i}", f"node_{i+1}")

        algorithm = GraphvizLayout.recommend_algorithm(diagram)
        assert algorithm == "sfdp"  # Large graphs should use sfdp

    def test_is_dag_true(self):
        """Test DAG detection for acyclic graph"""
        diagram = Diagram(title="DAG")
        diagram.add_node("a", "A")
        diagram.add_node("b", "B")
        diagram.add_node("c", "C")
        diagram.add_edge("a", "b")
        diagram.add_edge("b", "c")

        assert GraphvizLayout._is_dag(diagram) is True

    def test_is_dag_false(self):
        """Test DAG detection for cyclic graph"""
        diagram = Diagram(title="Cyclic")
        diagram.add_node("a", "A")
        diagram.add_node("b", "B")
        diagram.add_node("c", "C")
        diagram.add_edge("a", "b")
        diagram.add_edge("b", "c")
        diagram.add_edge("c", "a")  # Creates cycle

        assert GraphvizLayout._is_dag(diagram) is False

    def test_layout_fallback_without_pygraphviz(self):
        """Test fallback layout when pygraphviz is not available"""
        layout = GraphvizLayout()
        layout._pgv = None  # Simulate pygraphviz not available

        diagram = Diagram(title="Test", width=800, height=600)
        diagram.add_node("a", "A")
        diagram.add_node("b", "B")
        diagram.add_edge("a", "b")

        result = layout.layout(diagram)

        # Should still return a valid diagram
        assert result is not None
        assert len(result.nodes) == 2
        # Nodes should have positions set
        for node in result.nodes:
            assert node.position is not None
            assert node.position.x >= 0
            assert node.position.y >= 0

    def test_layout_empty_diagram(self):
        """Test layout with empty diagram"""
        layout = GraphvizLayout()
        diagram = Diagram(title="Empty")

        result = layout.layout(diagram)
        assert result is not None
        assert len(result.nodes) == 0

    def test_layout_with_clusters(self):
        """Test layout with clusters"""
        diagram = Diagram(title="Clustered")

        # Add nodes
        diagram.add_node("api", "API Gateway")
        diagram.add_node("svc1", "Service 1")
        diagram.add_node("svc2", "Service 2")
        diagram.add_node("db", "Database")

        # Add cluster
        diagram.add_cluster("services", "Microservices", ["svc1", "svc2"])

        # Add edges
        diagram.add_edge("api", "svc1")
        diagram.add_edge("api", "svc2")
        diagram.add_edge("svc1", "db")
        diagram.add_edge("svc2", "db")

        layout = GraphvizLayout()
        # Use fallback since we may not have pygraphviz in test env
        layout._pgv = None

        result = layout.layout(diagram)

        assert result is not None
        assert len(result.clusters) == 1
        # Cluster should have size and position set
        cluster = result.clusters[0]
        assert cluster.size is not None
        assert cluster.position is not None


class TestAutoLayout:
    """Test the auto_layout convenience function"""

    def test_auto_layout(self):
        """Test auto_layout function"""
        diagram = Diagram(title="Auto")
        diagram.add_node("a", "A")
        diagram.add_node("b", "B")
        diagram.add_edge("a", "b")

        result = auto_layout(diagram)
        assert result is not None
        assert len(result.nodes) == 2


class TestGraphvizAlgorithmEnum:
    """Test GraphvizAlgorithm enum"""

    def test_algorithm_values(self):
        """Test that all algorithms have correct string values"""
        assert GraphvizAlgorithm.DOT.value == "dot"
        assert GraphvizAlgorithm.NEATO.value == "neato"
        assert GraphvizAlgorithm.FDP.value == "fdp"
        assert GraphvizAlgorithm.SFDP.value == "sfdp"
        assert GraphvizAlgorithm.CIRCO.value == "circo"
        assert GraphvizAlgorithm.TWOPI.value == "twopi"
