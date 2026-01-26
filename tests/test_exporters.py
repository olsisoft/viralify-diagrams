"""Tests for exporters"""

import pytest
from viralify_diagrams import (
    Diagram,
    SVGExporter,
    AnimatedSVGExporter,
    HorizontalLayout,
)
from viralify_diagrams.exporters.animated_svg_exporter import (
    AnimationConfig,
    AnimationType,
)


def create_sample_diagram():
    """Create a sample diagram for testing"""
    diagram = Diagram(
        title="Test Diagram",
        description="A test diagram"
    )
    diagram.add_node("a", "Node A")
    diagram.add_node("b", "Node B")
    diagram.add_node("c", "Node C")
    diagram.add_edge("a", "b", label="A to B")
    diagram.add_edge("b", "c", label="B to C")

    layout = HorizontalLayout()
    return layout.layout(diagram)


class TestSVGExporter:
    """Tests for SVGExporter"""

    def test_export_basic(self):
        """Test basic SVG export"""
        diagram = create_sample_diagram()
        exporter = SVGExporter()

        svg = exporter.export(diagram)

        assert svg.startswith('<?xml version="1.0"')
        assert '<svg' in svg
        assert '</svg>' in svg

    def test_export_contains_nodes(self):
        """Test that SVG contains node elements"""
        diagram = create_sample_diagram()
        exporter = SVGExporter()

        svg = exporter.export(diagram)

        assert 'id="a"' in svg
        assert 'id="b"' in svg
        assert 'id="c"' in svg
        assert 'Node A' in svg
        assert 'Node B' in svg

    def test_export_contains_edges(self):
        """Test that SVG contains edge elements"""
        diagram = create_sample_diagram()
        exporter = SVGExporter()

        svg = exporter.export(diagram)

        assert 'class="edge"' in svg
        assert 'A to B' in svg

    def test_export_has_layers(self):
        """Test that SVG has proper layer structure"""
        diagram = create_sample_diagram()
        exporter = SVGExporter()

        svg = exporter.export(diagram)

        assert 'id="clusters-layer"' in svg
        assert 'id="edges-layer"' in svg
        assert 'id="nodes-layer"' in svg

    def test_get_elements(self):
        """Test getting element metadata"""
        diagram = create_sample_diagram()
        exporter = SVGExporter()
        exporter.export(diagram)

        elements = exporter.get_elements()

        assert len(elements) > 0
        node_elements = [e for e in elements if e.element_type == "node"]
        edge_elements = [e for e in elements if e.element_type == "edge"]

        assert len(node_elements) == 3
        assert len(edge_elements) == 2


class TestAnimatedSVGExporter:
    """Tests for AnimatedSVGExporter"""

    def test_export_with_animations(self):
        """Test animated SVG export"""
        diagram = create_sample_diagram()
        exporter = AnimatedSVGExporter()

        svg = exporter.export(diagram)

        assert '<style>' in svg
        assert '@keyframes' in svg
        assert 'animation:' in svg

    def test_custom_config(self):
        """Test with custom animation config"""
        config = AnimationConfig(
            duration=1.0,
            delay_between=0.5,
            easing="linear"
        )
        exporter = AnimatedSVGExporter(config=config)
        diagram = create_sample_diagram()

        svg = exporter.export(diagram)

        assert 'linear' in svg
        assert '1s' in svg or '1.0s' in svg

    def test_animation_types(self):
        """Test different animation types"""
        diagram = create_sample_diagram()
        exporter = AnimatedSVGExporter()

        svg = exporter.export(
            diagram,
            node_animation=AnimationType.SCALE_IN,
            edge_animation=AnimationType.DRAW
        )

        assert 'scaleIn' in svg
        assert 'drawPath' in svg

    def test_get_timeline(self):
        """Test getting animation timeline"""
        diagram = create_sample_diagram()
        exporter = AnimatedSVGExporter()
        exporter.export(diagram)

        timeline = exporter.get_timeline()

        assert len(timeline) > 0
        assert all(hasattr(t, 'element_id') for t in timeline)
        assert all(hasattr(t, 'start_time') for t in timeline)

    def test_get_total_duration(self):
        """Test getting total animation duration"""
        config = AnimationConfig(
            duration=0.5,
            delay_between=0.3,
            initial_delay=0.5
        )
        exporter = AnimatedSVGExporter(config=config)
        diagram = create_sample_diagram()
        exporter.export(diagram)

        duration = exporter.get_total_duration()

        assert duration > 0
        # Should be at least initial_delay + some element durations
        assert duration >= 0.5

    def test_export_timing_script(self):
        """Test exporting timing script"""
        diagram = create_sample_diagram()
        exporter = AnimatedSVGExporter()
        exporter.export(diagram)

        timing = exporter.export_timing_script()

        assert 'total_duration' in timing
        assert 'config' in timing
        assert 'elements' in timing
        assert len(timing['elements']) > 0
