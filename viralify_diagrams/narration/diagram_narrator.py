"""
Diagram Narrator

Generates narration scripts for diagram explanations.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json

from viralify_diagrams.core.diagram import Diagram, Node, Edge, Cluster


class NarrationStyle(str, Enum):
    """Narration styles"""
    EDUCATIONAL = "educational"  # Detailed explanations
    PROFESSIONAL = "professional"  # Concise, business-like
    CASUAL = "casual"  # Friendly, conversational
    TECHNICAL = "technical"  # Deep technical detail


@dataclass
class NarrationSegment:
    """A single narration segment"""
    element_id: str
    element_type: str  # node, edge, cluster, intro, conclusion
    start_time: float  # seconds
    duration: float  # estimated seconds for narration
    text: str  # the actual narration text
    emphasis_words: List[str] = field(default_factory=list)  # words to emphasize
    pause_after: float = 0.3  # pause after this segment


@dataclass
class NarrationScript:
    """Complete narration script for a diagram"""
    diagram_id: str
    title: str
    total_duration: float
    style: NarrationStyle
    segments: List[NarrationSegment]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_srt(self) -> str:
        """Export as SRT subtitle format"""
        srt_content = ""
        for i, segment in enumerate(self.segments, 1):
            start = self._format_srt_time(segment.start_time)
            end = self._format_srt_time(segment.start_time + segment.duration)
            srt_content += f"{i}\n{start} --> {end}\n{segment.text}\n\n"
        return srt_content

    def _format_srt_time(self, seconds: float) -> str:
        """Format seconds as SRT timestamp"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def to_json(self) -> str:
        """Export as JSON"""
        return json.dumps({
            "diagram_id": self.diagram_id,
            "title": self.title,
            "total_duration": self.total_duration,
            "style": self.style.value,
            "segments": [
                {
                    "element_id": s.element_id,
                    "element_type": s.element_type,
                    "start_time": s.start_time,
                    "duration": s.duration,
                    "text": s.text,
                    "emphasis_words": s.emphasis_words,
                    "pause_after": s.pause_after
                }
                for s in self.segments
            ],
            "metadata": self.metadata
        }, indent=2)

    def to_ssml(self) -> str:
        """Export as SSML for TTS systems"""
        ssml = '<speak>\n'
        for segment in self.segments:
            text = segment.text
            # Add emphasis markers
            for word in segment.emphasis_words:
                text = text.replace(
                    word,
                    f'<emphasis level="strong">{word}</emphasis>'
                )
            ssml += f'  <p>{text}</p>\n'
            if segment.pause_after > 0:
                pause_ms = int(segment.pause_after * 1000)
                ssml += f'  <break time="{pause_ms}ms"/>\n'
        ssml += '</speak>'
        return ssml


class DiagramNarrator:
    """
    Generates narration scripts for diagrams.

    Analyzes diagram structure and generates appropriate
    narration for each element in animation order.
    """

    # Words per minute for duration estimation
    WPM_BY_STYLE = {
        NarrationStyle.EDUCATIONAL: 130,
        NarrationStyle.PROFESSIONAL: 150,
        NarrationStyle.CASUAL: 140,
        NarrationStyle.TECHNICAL: 120,
    }

    # Transition phrases
    TRANSITIONS = {
        "intro": [
            "Let's look at",
            "Here we have",
            "This diagram shows",
            "We'll explore",
        ],
        "node": [
            "First, we have",
            "Next is",
            "Here we see",
            "This represents",
            "Moving on to",
        ],
        "edge": [
            "This connects to",
            "Which flows into",
            "This sends data to",
            "This communicates with",
        ],
        "cluster": [
            "This group contains",
            "Within this area,",
            "This section includes",
            "Grouped together are",
        ],
        "conclusion": [
            "To summarize,",
            "In conclusion,",
            "Overall,",
            "As we can see,",
        ],
    }

    def __init__(
        self,
        style: NarrationStyle = NarrationStyle.EDUCATIONAL,
        language: str = "en"
    ):
        self.style = style
        self.language = language
        self._transition_index = {}

    def generate_script(
        self,
        diagram: Diagram,
        element_duration: float = 2.0,
        include_intro: bool = True,
        include_conclusion: bool = True
    ) -> NarrationScript:
        """
        Generate a narration script for the diagram.

        Args:
            diagram: The diagram to narrate
            element_duration: Base duration per element
            include_intro: Include introduction segment
            include_conclusion: Include conclusion segment

        Returns:
            Complete NarrationScript
        """
        segments = []
        current_time = 0.0

        # Introduction
        if include_intro:
            intro_text = self._generate_intro(diagram)
            intro_duration = self._estimate_duration(intro_text)
            segments.append(NarrationSegment(
                element_id="intro",
                element_type="intro",
                start_time=current_time,
                duration=intro_duration,
                text=intro_text,
                emphasis_words=[diagram.title] if diagram.title else [],
                pause_after=0.5
            ))
            current_time += intro_duration + 0.5

        # Clusters (explain groupings first)
        for cluster in sorted(diagram.clusters, key=lambda c: c.order):
            text = self._generate_cluster_narration(cluster)
            duration = self._estimate_duration(text)
            segments.append(NarrationSegment(
                element_id=cluster.id,
                element_type="cluster",
                start_time=current_time,
                duration=duration,
                text=text,
                emphasis_words=[cluster.label],
                pause_after=0.3
            ))
            current_time += duration + 0.3

        # Nodes in order
        for node in sorted(diagram.nodes, key=lambda n: n.order):
            text = self._generate_node_narration(node, diagram)
            duration = self._estimate_duration(text)
            segments.append(NarrationSegment(
                element_id=node.id,
                element_type="node",
                start_time=current_time,
                duration=duration,
                text=text,
                emphasis_words=[node.label],
                pause_after=0.3
            ))
            current_time += duration + 0.3

        # Edges (explain relationships)
        for edge in sorted(diagram.edges, key=lambda e: e.order):
            text = self._generate_edge_narration(edge, diagram)
            if text:  # Some edges may not need narration
                duration = self._estimate_duration(text)
                segments.append(NarrationSegment(
                    element_id=edge.id,
                    element_type="edge",
                    start_time=current_time,
                    duration=duration,
                    text=text,
                    pause_after=0.2
                ))
                current_time += duration + 0.2

        # Conclusion
        if include_conclusion:
            conclusion_text = self._generate_conclusion(diagram)
            conclusion_duration = self._estimate_duration(conclusion_text)
            segments.append(NarrationSegment(
                element_id="conclusion",
                element_type="conclusion",
                start_time=current_time,
                duration=conclusion_duration,
                text=conclusion_text,
                pause_after=0.5
            ))
            current_time += conclusion_duration + 0.5

        return NarrationScript(
            diagram_id=diagram.id,
            title=diagram.title,
            total_duration=current_time,
            style=self.style,
            segments=segments,
            metadata={
                "language": self.language,
                "node_count": len(diagram.nodes),
                "edge_count": len(diagram.edges),
                "cluster_count": len(diagram.clusters)
            }
        )

    def _estimate_duration(self, text: str) -> float:
        """Estimate narration duration based on word count"""
        word_count = len(text.split())
        wpm = self.WPM_BY_STYLE.get(self.style, 140)
        return (word_count / wpm) * 60  # Convert to seconds

    def _get_transition(self, element_type: str) -> str:
        """Get a transition phrase, cycling through options"""
        if element_type not in self._transition_index:
            self._transition_index[element_type] = 0

        transitions = self.TRANSITIONS.get(element_type, [""])
        index = self._transition_index[element_type]
        phrase = transitions[index % len(transitions)]
        self._transition_index[element_type] = index + 1
        return phrase

    def _generate_intro(self, diagram: Diagram) -> str:
        """Generate introduction narration"""
        transition = self._get_transition("intro")

        if self.style == NarrationStyle.EDUCATIONAL:
            return (
                f"{transition} {diagram.title}. "
                f"{diagram.description} "
                f"We'll examine each component step by step."
            )
        elif self.style == NarrationStyle.PROFESSIONAL:
            return (
                f"{diagram.title}: {diagram.description}"
            )
        elif self.style == NarrationStyle.CASUAL:
            return (
                f"Hey! {transition} {diagram.title}. "
                f"Basically, {diagram.description.lower()}"
            )
        else:  # TECHNICAL
            return (
                f"{diagram.title}. "
                f"Architecture overview: {diagram.description} "
                f"Components and interactions follow."
            )

    def _generate_node_narration(self, node: Node, diagram: Diagram) -> str:
        """Generate narration for a node"""
        transition = self._get_transition("node")
        label = node.label
        desc = node.description or ""

        # Find connected nodes
        outgoing = [e for e in diagram.edges if e.source == node.id]
        incoming = [e for e in diagram.edges if e.target == node.id]

        if self.style == NarrationStyle.EDUCATIONAL:
            text = f"{transition} {label}."
            if desc:
                text += f" {desc}"
            if outgoing:
                targets = [diagram.get_node(e.target) for e in outgoing if diagram.get_node(e.target)]
                if targets:
                    target_names = ", ".join([t.label for t in targets[:3]])
                    text += f" It connects to {target_names}."
            return text

        elif self.style == NarrationStyle.PROFESSIONAL:
            text = f"{label}"
            if desc:
                text += f": {desc}"
            return text

        elif self.style == NarrationStyle.CASUAL:
            text = f"So here's {label}."
            if desc:
                text += f" It's basically {desc.lower()}"
            return text

        else:  # TECHNICAL
            text = f"{label}"
            if desc:
                text += f" - {desc}"
            if outgoing:
                text += f" Outbound connections: {len(outgoing)}."
            if incoming:
                text += f" Inbound connections: {len(incoming)}."
            return text

    def _generate_edge_narration(self, edge: Edge, diagram: Diagram) -> str:
        """Generate narration for an edge"""
        source = diagram.get_node(edge.source)
        target = diagram.get_node(edge.target)

        if not source or not target:
            return ""

        label = edge.label or ""

        if self.style == NarrationStyle.EDUCATIONAL:
            text = f"{source.label} connects to {target.label}"
            if label:
                text += f" through {label}"
            return text + "."

        elif self.style == NarrationStyle.PROFESSIONAL:
            if label:
                return f"{source.label} → {target.label}: {label}"
            return ""  # Skip unlabeled edges in professional style

        elif self.style == NarrationStyle.CASUAL:
            text = f"{source.label} talks to {target.label}"
            if label:
                text += f" using {label}"
            return text + "."

        else:  # TECHNICAL
            if label:
                return f"Connection: {source.label} to {target.label} via {label}."
            return ""  # Skip unlabeled edges

    def _generate_cluster_narration(self, cluster: Cluster) -> str:
        """Generate narration for a cluster"""
        transition = self._get_transition("cluster")
        label = cluster.label
        desc = cluster.description or ""

        if self.style == NarrationStyle.EDUCATIONAL:
            text = f"{transition} {label}."
            if desc:
                text += f" {desc}"
            return text

        elif self.style == NarrationStyle.PROFESSIONAL:
            text = label
            if desc:
                text += f": {desc}"
            return text

        elif self.style == NarrationStyle.CASUAL:
            text = f"This area is {label}."
            if desc:
                text += f" {desc}"
            return text

        else:  # TECHNICAL
            text = f"Group: {label}"
            if desc:
                text += f". {desc}"
            return text

    def _generate_conclusion(self, diagram: Diagram) -> str:
        """Generate conclusion narration"""
        transition = self._get_transition("conclusion")
        node_count = len(diagram.nodes)
        edge_count = len(diagram.edges)

        if self.style == NarrationStyle.EDUCATIONAL:
            return (
                f"{transition} we've explored {diagram.title}. "
                f"This architecture consists of {node_count} components "
                f"with {edge_count} connections between them. "
                f"Understanding these relationships is key to working with this system."
            )

        elif self.style == NarrationStyle.PROFESSIONAL:
            return (
                f"{transition} {diagram.title} comprises {node_count} components "
                f"and {edge_count} interactions."
            )

        elif self.style == NarrationStyle.CASUAL:
            return (
                f"And that's {diagram.title}! "
                f"Pretty cool how these {node_count} pieces work together, right?"
            )

        else:  # TECHNICAL
            return (
                f"Architecture summary: {node_count} nodes, {edge_count} edges. "
                f"Refer to documentation for implementation details."
            )

    def synchronize_with_animation(
        self,
        script: NarrationScript,
        animation_timeline: List[Dict[str, Any]]
    ) -> NarrationScript:
        """
        Synchronize narration script with animation timeline.

        Adjusts segment timings to match animation events.

        Args:
            script: The narration script to adjust
            animation_timeline: Timeline from AnimatedSVGExporter

        Returns:
            Adjusted NarrationScript
        """
        # Build timing map from animation
        timing_map = {}
        for event in animation_timeline:
            timing_map[event["id"]] = {
                "start": event["start"],
                "duration": event["duration"]
            }

        # Adjust segment timings
        adjusted_segments = []
        for segment in script.segments:
            if segment.element_id in timing_map:
                timing = timing_map[segment.element_id]
                # Start narration when element appears
                adjusted_segments.append(NarrationSegment(
                    element_id=segment.element_id,
                    element_type=segment.element_type,
                    start_time=timing["start"],
                    duration=max(segment.duration, timing["duration"]),
                    text=segment.text,
                    emphasis_words=segment.emphasis_words,
                    pause_after=segment.pause_after
                ))
            else:
                adjusted_segments.append(segment)

        # Recalculate total duration
        total = max(s.start_time + s.duration for s in adjusted_segments)

        return NarrationScript(
            diagram_id=script.diagram_id,
            title=script.title,
            total_duration=total,
            style=script.style,
            segments=adjusted_segments,
            metadata=script.metadata
        )
