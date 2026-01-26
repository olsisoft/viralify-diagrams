"""
PNG Frame Exporter

Exports diagrams as a sequence of PNG frames for video composition.
"""

import os
import io
import tempfile
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

from viralify_diagrams.core.diagram import Diagram, Node, Edge, Cluster
from viralify_diagrams.core.theme import Theme, get_theme_manager
from viralify_diagrams.exporters.svg_exporter import SVGExporter

# Optional imports for rendering
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import cairosvg
    HAS_CAIRO = True
except ImportError:
    HAS_CAIRO = False


@dataclass
class FrameConfig:
    """Configuration for frame export"""
    fps: int = 30  # frames per second
    element_duration: float = 0.5  # seconds per element appearance
    transition_frames: int = 10  # frames for transitions
    width: int = 1920
    height: int = 1080
    background_color: str = "#1a1a2e"
    output_format: str = "png"  # png or jpg
    quality: int = 95  # for jpg


@dataclass
class Frame:
    """A single frame with metadata"""
    index: int
    timestamp: float  # seconds
    visible_elements: List[str]  # element IDs visible in this frame
    image_path: Optional[str] = None
    image_data: Optional[bytes] = None


class PNGFrameExporter:
    """
    Exports diagrams as PNG frames for video composition.

    Features:
    - Sequential frame generation
    - Configurable FPS and timing
    - Element-by-element reveal
    - Transition frames for smooth animations
    - Direct output to folder or memory
    """

    def __init__(
        self,
        theme: Optional[Theme] = None,
        config: Optional[FrameConfig] = None
    ):
        self.theme = theme
        self.config = config or FrameConfig()
        self._svg_exporter = SVGExporter(theme)
        self._frames: List[Frame] = []

    def export(
        self,
        diagram: Diagram,
        output_dir: Optional[str] = None
    ) -> List[Frame]:
        """
        Export diagram to PNG frames.

        Args:
            diagram: The diagram to export
            output_dir: Directory to save frames (creates temp dir if None)

        Returns:
            List of Frame objects with paths/data
        """
        if not HAS_CAIRO and not HAS_PIL:
            raise ImportError(
                "PNG export requires either cairosvg or Pillow. "
                "Install with: pip install cairosvg pillow"
            )

        # Get theme
        if self.theme:
            theme = self.theme
        else:
            theme = get_theme_manager().get(diagram.theme)

        # Create output directory
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        else:
            output_dir = tempfile.mkdtemp(prefix="viralify_frames_")

        self._frames = []

        # Build frame sequence
        frame_sequence = self._build_frame_sequence(diagram)

        # Render each frame
        for frame_info in frame_sequence:
            frame = self._render_frame(
                diagram,
                theme,
                frame_info,
                output_dir
            )
            self._frames.append(frame)

        return self._frames

    def _build_frame_sequence(
        self,
        diagram: Diagram
    ) -> List[Dict[str, Any]]:
        """Build the sequence of frames to render"""
        sequence = []
        fps = self.config.fps
        element_frames = int(self.config.element_duration * fps)
        transition_frames = self.config.transition_frames

        # Get ordered elements
        clusters = sorted(diagram.clusters, key=lambda c: c.order)
        nodes = sorted(diagram.nodes, key=lambda n: n.order)
        edges = sorted(diagram.edges, key=lambda e: e.order)

        all_elements = (
            [("cluster", c.id) for c in clusters] +
            [("node", n.id) for n in nodes] +
            [("edge", e.id) for e in edges]
        )

        current_frame = 0
        visible = []

        # Initial empty frame
        sequence.append({
            "index": current_frame,
            "timestamp": current_frame / fps,
            "visible": [],
            "transitioning": None,
            "progress": 1.0
        })
        current_frame += 1

        # Add each element with transition
        for elem_type, elem_id in all_elements:
            # Transition frames (element fading in)
            for t in range(transition_frames):
                progress = (t + 1) / transition_frames
                sequence.append({
                    "index": current_frame,
                    "timestamp": current_frame / fps,
                    "visible": visible.copy(),
                    "transitioning": elem_id,
                    "progress": progress
                })
                current_frame += 1

            # Add element to visible list
            visible.append(elem_id)

            # Hold frames (element fully visible)
            hold_frames = element_frames - transition_frames
            for _ in range(hold_frames):
                sequence.append({
                    "index": current_frame,
                    "timestamp": current_frame / fps,
                    "visible": visible.copy(),
                    "transitioning": None,
                    "progress": 1.0
                })
                current_frame += 1

        # Final hold frame
        for _ in range(fps):  # 1 second hold at end
            sequence.append({
                "index": current_frame,
                "timestamp": current_frame / fps,
                "visible": visible.copy(),
                "transitioning": None,
                "progress": 1.0
            })
            current_frame += 1

        return sequence

    def _render_frame(
        self,
        diagram: Diagram,
        theme: Theme,
        frame_info: Dict[str, Any],
        output_dir: str
    ) -> Frame:
        """Render a single frame"""
        import html

        visible = frame_info["visible"]
        transitioning = frame_info["transitioning"]
        progress = frame_info["progress"]

        # Build SVG for this frame
        svg = self._build_frame_svg(
            diagram,
            theme,
            visible,
            transitioning,
            progress
        )

        # Convert SVG to PNG
        frame_path = os.path.join(
            output_dir,
            f"frame_{frame_info['index']:06d}.{self.config.output_format}"
        )

        image_data = self._svg_to_png(svg)

        # Save to file
        with open(frame_path, "wb") as f:
            f.write(image_data)

        return Frame(
            index=frame_info["index"],
            timestamp=frame_info["timestamp"],
            visible_elements=visible,
            image_path=frame_path,
            image_data=image_data
        )

    def _build_frame_svg(
        self,
        diagram: Diagram,
        theme: Theme,
        visible: List[str],
        transitioning: Optional[str],
        progress: float
    ) -> str:
        """Build SVG for a specific frame"""
        import html

        width = self.config.width
        height = self.config.height

        # Scale diagram to fit frame
        scale_x = width / diagram.width
        scale_y = height / diagram.height
        scale = min(scale_x, scale_y) * 0.9  # 90% to add padding

        offset_x = (width - diagram.width * scale) / 2
        offset_y = (height - diagram.height * scale) / 2

        svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{width}"
     height="{height}"
     viewBox="0 0 {width} {height}">

  <defs>
    {self._svg_exporter._build_styles(theme)}
    {self._svg_exporter._build_markers(theme)}
    {self._svg_exporter._build_filters(theme)}
  </defs>

  <!-- Background -->
  <rect width="100%" height="100%" fill="{theme.colors.background}"/>

  <!-- Scaled Diagram Content -->
  <g transform="translate({offset_x}, {offset_y}) scale({scale})">
'''

        # Render visible clusters
        for cluster in diagram.clusters:
            if cluster.id in visible:
                opacity = 1.0
                if cluster.id == transitioning:
                    opacity = progress
                svg += self._render_element_with_opacity(
                    self._svg_exporter._render_cluster(cluster, theme),
                    opacity
                )

        # Render visible edges
        for edge in diagram.edges:
            if edge.id in visible:
                opacity = 1.0
                if edge.id == transitioning:
                    opacity = progress
                svg += self._render_element_with_opacity(
                    self._svg_exporter._render_edge(edge, diagram, theme),
                    opacity
                )

        # Render visible nodes
        for node in diagram.nodes:
            if node.id in visible:
                opacity = 1.0
                if node.id == transitioning:
                    opacity = progress
                svg += self._render_element_with_opacity(
                    self._svg_exporter._render_node(node, theme),
                    opacity
                )

        svg += '''  </g>
</svg>'''

        return svg

    def _render_element_with_opacity(
        self,
        svg_content: str,
        opacity: float
    ) -> str:
        """Wrap element with opacity"""
        if opacity >= 1.0:
            return svg_content

        # Wrap in group with opacity
        return f'<g opacity="{opacity}">\n{svg_content}</g>\n'

    def _svg_to_png(self, svg: str) -> bytes:
        """Convert SVG to PNG bytes"""
        if HAS_CAIRO:
            return cairosvg.svg2png(
                bytestring=svg.encode('utf-8'),
                output_width=self.config.width,
                output_height=self.config.height
            )
        elif HAS_PIL:
            # Fallback using PIL (requires svglib or similar)
            try:
                from svglib.svglib import renderSVG
                from reportlab.graphics import renderPM

                drawing = renderSVG.renderSVG(io.BytesIO(svg.encode('utf-8')))
                img_data = io.BytesIO()
                renderPM.drawToFile(drawing, img_data, fmt='PNG')
                return img_data.getvalue()
            except ImportError:
                # Ultimate fallback: return placeholder
                return self._create_placeholder_png()
        else:
            raise ImportError("No SVG rendering library available")

    def _create_placeholder_png(self) -> bytes:
        """Create a placeholder PNG when no renderer is available"""
        if HAS_PIL:
            img = Image.new(
                'RGB',
                (self.config.width, self.config.height),
                color=self.config.background_color
            )
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            return buffer.getvalue()
        else:
            # Return minimal valid PNG (1x1 transparent)
            return (
                b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
                b'\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
                b'\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01'
                b'\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
            )

    def get_frames(self) -> List[Frame]:
        """Get all rendered frames"""
        return self._frames

    def get_total_duration(self) -> float:
        """Get total video duration in seconds"""
        if not self._frames:
            return 0
        return self._frames[-1].timestamp

    def get_frame_count(self) -> int:
        """Get total number of frames"""
        return len(self._frames)

    def export_frame_manifest(self) -> Dict[str, Any]:
        """
        Export manifest with frame information for video composition.

        Returns a dict with:
        - total_frames: Total number of frames
        - fps: Frames per second
        - duration: Total duration in seconds
        - resolution: (width, height)
        - frames: List of frame metadata
        """
        return {
            "total_frames": len(self._frames),
            "fps": self.config.fps,
            "duration": self.get_total_duration(),
            "resolution": {
                "width": self.config.width,
                "height": self.config.height
            },
            "format": self.config.output_format,
            "frames": [
                {
                    "index": f.index,
                    "timestamp": f.timestamp,
                    "path": f.image_path,
                    "visible_elements": f.visible_elements
                }
                for f in self._frames
            ]
        }

    def create_video(
        self,
        output_path: str,
        audio_path: Optional[str] = None
    ) -> str:
        """
        Create video from frames using FFmpeg.

        Args:
            output_path: Output video path
            audio_path: Optional audio track path

        Returns:
            Path to created video
        """
        import subprocess

        if not self._frames:
            raise ValueError("No frames to create video from")

        # Get frame directory from first frame
        frame_dir = os.path.dirname(self._frames[0].image_path)
        frame_pattern = os.path.join(
            frame_dir,
            f"frame_%06d.{self.config.output_format}"
        )

        # Build FFmpeg command
        cmd = [
            "ffmpeg",
            "-y",  # Overwrite output
            "-framerate", str(self.config.fps),
            "-i", frame_pattern,
        ]

        if audio_path:
            cmd.extend(["-i", audio_path])

        cmd.extend([
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",  # High quality
        ])

        if audio_path:
            cmd.extend([
                "-c:a", "aac",
                "-shortest"  # Match video to audio length
            ])

        cmd.append(output_path)

        # Run FFmpeg
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg failed: {result.stderr}")

        return output_path
