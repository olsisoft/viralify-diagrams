#!/usr/bin/env python
"""
Basic Diagram Example

Demonstrates creating a simple microservices architecture diagram
with horizontal layout and SVG export.
"""

import sys
sys.path.insert(0, '..')

from viralify_diagrams import (
    Diagram,
    HorizontalLayout,
    SVGExporter,
    AnimatedSVGExporter,
    AnimationConfig,
    AnimationType,
    DiagramNarrator,
    NarrationStyle,
)
from viralify_diagrams.core.diagram import NodeShape, EdgeStyle


def main():
    # Create diagram
    diagram = Diagram(
        title="Microservices Architecture",
        description="A typical microservices communication flow with API Gateway pattern",
        theme="dark",
        width=1600,
        height=900
    )

    # Add nodes
    diagram.add_node(
        "client",
        "Client App",
        description="Mobile/Web application",
        shape=NodeShape.ROUNDED
    )

    diagram.add_node(
        "gateway",
        "API Gateway",
        description="Entry point and request routing",
        shape=NodeShape.HEXAGON
    )

    diagram.add_node(
        "auth",
        "Auth Service",
        description="JWT authentication and authorization",
        shape=NodeShape.ROUNDED
    )

    diagram.add_node(
        "users",
        "User Service",
        description="User management and profiles",
        shape=NodeShape.ROUNDED
    )

    diagram.add_node(
        "orders",
        "Order Service",
        description="Order processing and fulfillment",
        shape=NodeShape.ROUNDED
    )

    diagram.add_node(
        "db",
        "PostgreSQL",
        description="Primary database",
        shape=NodeShape.CYLINDER
    )

    diagram.add_node(
        "cache",
        "Redis Cache",
        description="Session and data caching",
        shape=NodeShape.CYLINDER
    )

    # Add edges
    diagram.add_edge("client", "gateway", label="HTTPS")
    diagram.add_edge("gateway", "auth", label="Validate Token")
    diagram.add_edge("gateway", "users", label="User API")
    diagram.add_edge("gateway", "orders", label="Order API")
    diagram.add_edge("auth", "cache", label="Sessions")
    diagram.add_edge("users", "db", label="User Data")
    diagram.add_edge("orders", "db", label="Order Data")

    # Add cluster
    diagram.add_cluster(
        "services",
        "Backend Services",
        ["auth", "users", "orders"],
        description="Core microservices layer"
    )

    diagram.add_cluster(
        "data",
        "Data Layer",
        ["db", "cache"],
        description="Persistent storage"
    )

    # Apply horizontal layout
    layout = HorizontalLayout()
    diagram = layout.layout(diagram)

    # Export static SVG
    print("Exporting static SVG...")
    exporter = SVGExporter()
    svg_content = exporter.export(diagram, "microservices_static.svg")
    print(f"Static SVG saved to microservices_static.svg ({len(svg_content)} bytes)")

    # Export animated SVG
    print("\nExporting animated SVG...")
    config = AnimationConfig(
        duration=0.6,
        delay_between=0.4,
        easing="ease-out",
        stagger=True
    )
    animated_exporter = AnimatedSVGExporter(config=config)
    animated_svg = animated_exporter.export(
        diagram,
        output_path="microservices_animated.svg",
        node_animation=AnimationType.SCALE_IN,
        edge_animation=AnimationType.DRAW,
        cluster_animation=AnimationType.FADE_IN
    )
    print(f"Animated SVG saved to microservices_animated.svg")
    print(f"Total animation duration: {animated_exporter.get_total_duration():.2f}s")

    # Export timing script
    timing = animated_exporter.export_timing_script()
    print(f"Animation has {len(timing['elements'])} elements")

    # Generate narration script
    print("\nGenerating narration script...")
    narrator = DiagramNarrator(
        style=NarrationStyle.EDUCATIONAL,
        language="en"
    )
    script = narrator.generate_script(
        diagram,
        element_duration=2.0,
        include_intro=True,
        include_conclusion=True
    )

    print(f"Narration duration: {script.total_duration:.2f}s")
    print(f"Segments: {len(script.segments)}")

    # Save SRT subtitles
    with open("narration.srt", "w") as f:
        f.write(script.to_srt())
    print("Saved narration.srt")

    # Save SSML for TTS
    with open("narration.ssml", "w") as f:
        f.write(script.to_ssml())
    print("Saved narration.ssml")

    # Print sample narration
    print("\n--- Sample Narration ---")
    for segment in script.segments[:5]:
        print(f"[{segment.start_time:.1f}s] {segment.text}")
    print("...")


if __name__ == "__main__":
    main()
