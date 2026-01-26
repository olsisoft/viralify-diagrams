#!/usr/bin/env python
"""
Custom Theme Example

Demonstrates creating and using custom themes for diagrams.
"""

import sys
sys.path.insert(0, '..')

from viralify_diagrams import (
    Diagram,
    Theme,
    ThemeManager,
    GridLayout,
    SVGExporter,
)
from viralify_diagrams.core.theme import ThemeColors, ThemeTypography, ThemeSpacing


def main():
    # Create a custom "Cyberpunk" theme
    cyberpunk_colors = ThemeColors(
        background="#0d0221",
        node_fill="#1a0a3e",
        node_stroke="#ff00ff",
        node_stroke_width=2,
        text_primary="#ffffff",
        text_secondary="#ff00ff",
        text_label="#00ffff",
        edge_color="#ff00ff",
        edge_arrow_color="#ff00ff",
        edge_width=2,
        cluster_fill="rgba(255, 0, 255, 0.1)",
        cluster_stroke="#ff00ff",
        cluster_stroke_width=2,
        cluster_label_color="#00ffff",
        highlight_primary="#ff00ff",
        highlight_secondary="#00ffff",
        highlight_tertiary="#ff6600",
        glow_color="#ff00ff",
        glow_blur=10,
        shadow_color="rgba(255, 0, 255, 0.5)",
        shadow_blur=15,
    )

    cyberpunk_typography = ThemeTypography(
        font_family="'Courier New', monospace",
        font_size_title=28,
        font_size_label=14,
        font_size_small=11,
        font_weight_normal=400,
        font_weight_title=700,
    )

    cyberpunk_spacing = ThemeSpacing(
        node_width=160,
        node_height=70,
        node_border_radius=0,  # Sharp edges for cyberpunk
        cluster_padding=25,
        cluster_border_radius=0,
    )

    cyberpunk_theme = Theme(
        name="cyberpunk",
        colors=cyberpunk_colors,
        typography=cyberpunk_typography,
        spacing=cyberpunk_spacing,
    )

    # Register the theme
    manager = ThemeManager()
    manager.register(cyberpunk_theme)

    # Also create from JSON (alternative method)
    neon_json = '''
    {
        "name": "neon-green",
        "colors": {
            "background": "#000000",
            "node_fill": "#001a00",
            "node_stroke": "#00ff00",
            "text_primary": "#ffffff",
            "text_label": "#00ff00",
            "edge_color": "#00ff00",
            "edge_arrow_color": "#00ff00",
            "cluster_fill": "rgba(0, 255, 0, 0.1)",
            "cluster_stroke": "#00ff00",
            "cluster_label_color": "#00ff00",
            "glow_color": "#00ff00",
            "glow_blur": 8
        },
        "typography": {
            "font_family": "monospace"
        }
    }
    '''
    neon_theme = Theme.from_json(neon_json)
    manager.register(neon_theme)

    # Create diagram with cyberpunk theme
    diagram = Diagram(
        title="Neural Network Architecture",
        description="Deep learning model structure",
        theme="cyberpunk",
        width=1200,
        height=800
    )

    # Add nodes for a neural network
    nodes = [
        ("input", "Input Layer"),
        ("conv1", "Conv2D"),
        ("pool1", "MaxPool"),
        ("conv2", "Conv2D"),
        ("pool2", "MaxPool"),
        ("flatten", "Flatten"),
        ("dense1", "Dense 256"),
        ("dropout", "Dropout"),
        ("output", "Output"),
    ]

    for node_id, label in nodes:
        diagram.add_node(node_id, label)

    # Add edges
    for i in range(len(nodes) - 1):
        diagram.add_edge(nodes[i][0], nodes[i+1][0])

    # Add clusters
    diagram.add_cluster("feature_extraction", "Feature Extraction",
                       ["conv1", "pool1", "conv2", "pool2"])
    diagram.add_cluster("classification", "Classification",
                       ["dense1", "dropout", "output"])

    # Apply grid layout
    layout = GridLayout(columns=3)
    diagram = layout.layout(diagram)

    # Export with cyberpunk theme
    exporter = SVGExporter()
    svg = exporter.export(diagram, "neural_network_cyberpunk.svg")
    print(f"Cyberpunk theme diagram saved ({len(svg)} bytes)")

    # Export with neon-green theme
    diagram.theme = "neon-green"
    svg = exporter.export(diagram, "neural_network_neon.svg")
    print(f"Neon-green theme diagram saved ({len(svg)} bytes)")

    # List all available themes
    print("\nAvailable themes:")
    for theme_name in manager.list_themes():
        print(f"  - {theme_name}")

    # Export theme to JSON (for sharing)
    print("\nCyberpunk theme JSON:")
    print(cyberpunk_theme.to_json()[:500] + "...")


if __name__ == "__main__":
    main()
