# Viralify Diagrams

Professional diagram generation for video content with theme customization and animation support.

## Features

- **Theme System**: Built-in themes (dark, light, corporate, neon, etc.) + custom theme support via JSON
- **Multiple Layouts**: Grid, horizontal, vertical, and radial layouts
- **Three Export Modes**:
  - Static SVG with named groups for external animation
  - Animated SVG with CSS animations
  - PNG frames for video composition
- **Narration Scripts**: Generate voiceover scripts synchronized with diagram animations
- **Video-Optimized**: Auto-simplification (max 8-10 nodes), high contrast, readable fonts

## Installation

```bash
pip install viralify-diagrams

# With PNG export support
pip install viralify-diagrams[png]

# With all optional dependencies
pip install viralify-diagrams[all]
```

## Quick Start

### Basic Diagram

```python
from viralify_diagrams import Diagram, Node, Edge, HorizontalLayout, SVGExporter

# Create diagram
diagram = Diagram(
    title="Microservices Architecture",
    description="Service communication flow"
)

# Add nodes
api = diagram.add_node("api", "API Gateway", description="Entry point")
auth = diagram.add_node("auth", "Auth Service", description="Authentication")
users = diagram.add_node("users", "User Service", description="User management")
db = diagram.add_node("db", "Database", description="PostgreSQL")

# Add edges
diagram.add_edge("api", "auth", label="JWT validation")
diagram.add_edge("api", "users", label="User requests")
diagram.add_edge("auth", "db", label="Credentials")
diagram.add_edge("users", "db", label="User data")

# Apply layout
layout = HorizontalLayout()
diagram = layout.layout(diagram)

# Export to SVG
exporter = SVGExporter()
svg_content = exporter.export(diagram, "architecture.svg")
```

### Custom Theme

```python
from viralify_diagrams import Theme, ThemeManager

# Create custom theme
my_theme = Theme.from_json('''{
    "name": "my-brand",
    "colors": {
        "background": "#0a0a1a",
        "node_fill": "#1a1a3e",
        "node_stroke": "#4a4aff",
        "edge_color": "#6a6aff",
        "text_primary": "#ffffff"
    }
}''')

# Register theme
ThemeManager().register(my_theme)

# Use theme
diagram = Diagram(title="My Diagram", theme="my-brand")
```

### Animated SVG Export

```python
from viralify_diagrams import AnimatedSVGExporter, AnimationConfig, AnimationType

# Configure animations
config = AnimationConfig(
    duration=0.5,           # seconds per element
    delay_between=0.3,      # delay between elements
    easing="ease-out",
    stagger=True
)

# Export with animations
exporter = AnimatedSVGExporter(config=config)
svg = exporter.export(
    diagram,
    output_path="animated.svg",
    node_animation=AnimationType.SCALE_IN,
    edge_animation=AnimationType.DRAW,
    cluster_animation=AnimationType.FADE_IN
)

# Get timing script for external use
timing = exporter.export_timing_script()
print(f"Total duration: {timing['total_duration']}s")
```

### PNG Frames for Video

```python
from viralify_diagrams import PNGFrameExporter, FrameConfig

# Configure frame export
config = FrameConfig(
    fps=30,
    element_duration=0.5,
    width=1920,
    height=1080
)

# Export frames
exporter = PNGFrameExporter(config=config)
frames = exporter.export(diagram, output_dir="./frames")

# Get manifest for video editing
manifest = exporter.export_frame_manifest()
print(f"Total frames: {manifest['total_frames']}")
print(f"Duration: {manifest['duration']}s")

# Create video with FFmpeg
exporter.create_video("output.mp4", audio_path="narration.mp3")
```

### Narration Script Generation

```python
from viralify_diagrams import DiagramNarrator, NarrationStyle

# Create narrator
narrator = DiagramNarrator(
    style=NarrationStyle.EDUCATIONAL,
    language="en"
)

# Generate script
script = narrator.generate_script(
    diagram,
    element_duration=2.0,
    include_intro=True,
    include_conclusion=True
)

# Export formats
print(script.to_srt())   # SRT subtitles
print(script.to_ssml())  # SSML for TTS
print(script.to_json())  # JSON for processing

# Synchronize with animation timeline
timing = animated_exporter.export_timing_script()
synced_script = narrator.synchronize_with_animation(script, timing['elements'])
```

## Layouts

### HorizontalLayout
Left-to-right flow, ideal for pipelines and data flows.

### VerticalLayout
Top-to-bottom flow, ideal for hierarchies and layered architectures.

### GridLayout
Uniform grid pattern, ideal for comparing similar components.

### RadialLayout
Central node with satellites, ideal for hub-and-spoke architectures.

## Node Shapes

- `RECTANGLE` - Basic rectangle
- `ROUNDED` - Rounded corners (default)
- `CIRCLE` - Perfect circle
- `DIAMOND` - Decision node
- `HEXAGON` - Process node
- `CYLINDER` - Database/storage
- `CLOUD` - Cloud service

## Built-in Themes

- `dark` - Dark mode (default)
- `light` - Light mode
- `gradient` - Subtle gradient backgrounds
- `ocean` - Blue oceanic theme
- `corporate` - Professional business theme
- `neon` - Vibrant neon colors

## Animation Types

- `FADE_IN` - Fade in from transparent
- `SCALE_IN` - Scale up from center
- `SLIDE_LEFT/RIGHT/UP/DOWN` - Slide in from direction
- `DRAW` - Draw path (for edges)
- `PULSE` - Pulsing effect (looped)
- `GLOW` - Glow effect (looped)

## API Reference

### Diagram

```python
diagram = Diagram(
    title="Title",
    description="Description",
    theme="dark",
    width=1920,
    height=1080,
    padding=50,
    max_nodes=10  # Auto-simplification limit
)

# Methods
diagram.add_node(id, label, description=None, shape=NodeShape.ROUNDED)
diagram.add_edge(source_id, target_id, label=None, style=EdgeStyle.SOLID)
diagram.add_cluster(id, label, node_ids, description=None)
diagram.simplify(max_nodes=10)
diagram.assign_animation_order()
```

### Theme

```python
theme = Theme(
    name="my-theme",
    colors=ThemeColors(...),
    typography=ThemeTypography(...),
    spacing=ThemeSpacing(...)
)

# Load from JSON file
theme = Theme.from_json_file("theme.json")

# Export to JSON
json_str = theme.to_json()
```

### SVGExporter

```python
exporter = SVGExporter(theme=None)
svg_content = exporter.export(diagram, output_path=None)
elements = exporter.get_elements()  # List of SVGElement
```

### AnimatedSVGExporter

```python
exporter = AnimatedSVGExporter(theme=None, config=AnimationConfig())
svg = exporter.export(diagram, output_path, node_animation, edge_animation, cluster_animation)
timeline = exporter.get_timeline()
duration = exporter.get_total_duration()
timing_script = exporter.export_timing_script()
```

### PNGFrameExporter

```python
exporter = PNGFrameExporter(theme=None, config=FrameConfig())
frames = exporter.export(diagram, output_dir)
manifest = exporter.export_frame_manifest()
exporter.create_video(output_path, audio_path=None)
```

### DiagramNarrator

```python
narrator = DiagramNarrator(style=NarrationStyle.EDUCATIONAL, language="en")
script = narrator.generate_script(diagram, element_duration=2.0)
synced = narrator.synchronize_with_animation(script, animation_timeline)
```

## Requirements

- Python 3.9+
- Pillow (core)
- cairosvg (optional, for PNG export)
- FFmpeg (optional, for video creation)

## License

MIT License - see LICENSE file for details.

## Credits

Inspired by [mingrammer/diagrams](https://github.com/mingrammer/diagrams).

Built for [Viralify](https://viralify.io) - AI-powered educational video generation.
