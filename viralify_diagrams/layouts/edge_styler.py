"""
Edge Importance Scoring and Dynamic Styling

Provides visual hierarchy for edges based on:
- Connection weight/frequency
- Edge type/category
- Source/target node importance
- Custom scoring functions

Key features:
- Opacity scaling based on importance
- Stroke width variation
- Color gradients by importance
- Semantic coloring by edge type
- Highlight critical paths
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Any, Tuple
from enum import Enum
import math

from viralify_diagrams.core.diagram import Diagram, Node, Edge, Position


class ImportanceMetric(str, Enum):
    """Metrics for calculating edge importance"""
    WEIGHT = "weight"                 # Edge weight attribute
    FREQUENCY = "frequency"           # Number of similar connections
    CENTRALITY = "centrality"         # Based on node centrality
    CRITICALITY = "criticality"       # Part of critical path
    CUSTOM = "custom"                 # Custom scoring function


class ColorScheme(str, Enum):
    """Color schemes for edge styling"""
    MONOCHROME = "monochrome"         # Single color with opacity
    GRADIENT = "gradient"             # Color gradient by importance
    CATEGORICAL = "categorical"        # Color by edge type
    HEATMAP = "heatmap"               # Heat colors (blue to red)
    SEMANTIC = "semantic"             # Semantic meaning colors


@dataclass
class EdgeStyle:
    """Computed style for an edge"""
    stroke_color: str = "#718096"
    stroke_width: float = 1.5
    stroke_opacity: float = 1.0
    stroke_dasharray: Optional[str] = None
    glow: bool = False
    glow_color: Optional[str] = None
    glow_intensity: float = 0.5
    arrow_size: float = 8.0
    label_visible: bool = True
    z_index: int = 0                  # For layering


@dataclass
class StyleConfig:
    """Configuration for edge styling"""
    # Importance metric
    metric: ImportanceMetric = ImportanceMetric.WEIGHT
    custom_scorer: Optional[Callable[[Edge, Diagram], float]] = None

    # Color scheme
    color_scheme: ColorScheme = ColorScheme.MONOCHROME
    base_color: str = "#718096"
    highlight_color: str = "#3182CE"
    low_importance_color: str = "#E2E8F0"
    high_importance_color: str = "#2B6CB0"

    # Categorical colors (for CATEGORICAL scheme)
    category_colors: Dict[str, str] = field(default_factory=lambda: {
        "data_flow": "#3182CE",      # Blue
        "control_flow": "#38A169",    # Green
        "dependency": "#DD6B20",      # Orange
        "reference": "#805AD5",       # Purple
        "event": "#E53E3E",           # Red
        "default": "#718096",         # Gray
    })

    # Semantic colors (for SEMANTIC scheme)
    semantic_colors: Dict[str, str] = field(default_factory=lambda: {
        "read": "#3182CE",            # Blue - reading data
        "write": "#E53E3E",           # Red - writing data
        "call": "#38A169",            # Green - function calls
        "return": "#805AD5",          # Purple - return values
        "async": "#DD6B20",           # Orange - async operations
        "sync": "#2B6CB0",            # Dark blue - sync operations
    })

    # Width scaling
    min_stroke_width: float = 0.5
    max_stroke_width: float = 6.0
    scale_width: bool = True

    # Opacity scaling
    min_opacity: float = 0.15
    max_opacity: float = 1.0
    scale_opacity: bool = True

    # Glow for high importance
    enable_glow: bool = True
    glow_threshold: float = 0.8       # Importance threshold for glow

    # Dash patterns for edge types
    dash_patterns: Dict[str, str] = field(default_factory=lambda: {
        "optional": "4 4",
        "async": "8 4",
        "deprecated": "2 2",
        "weak": "1 3",
    })

    # Critical path highlighting
    highlight_critical_path: bool = True
    critical_path_width_multiplier: float = 1.5


@dataclass
class StyledEdge:
    """An edge with computed styling"""
    edge: Edge
    style: EdgeStyle
    importance: float                 # 0.0 to 1.0
    category: Optional[str] = None
    is_critical: bool = False


class EdgeStyler:
    """
    Dynamic edge styling based on importance scoring.

    Provides visual hierarchy for diagrams with many connections.

    Example:
        >>> styler = EdgeStyler(StyleConfig(
        ...     metric=ImportanceMetric.WEIGHT,
        ...     color_scheme=ColorScheme.HEATMAP
        ... ))
        >>> styled_edges = styler.style(diagram)
        >>> for se in styled_edges:
        ...     print(f"Edge importance: {se.importance:.2f}, width: {se.style.stroke_width}")
    """

    def __init__(self, config: Optional[StyleConfig] = None):
        self.config = config or StyleConfig()
        self._importance_cache: Dict[str, float] = {}

    def style(self, diagram: Diagram) -> List[StyledEdge]:
        """
        Compute styles for all edges in the diagram.

        Args:
            diagram: The diagram with nodes and edges

        Returns:
            List of styled edges with computed visual properties
        """
        if not diagram.edges:
            return []

        # Calculate importance scores
        importance_scores = self._calculate_importance(diagram)

        # Normalize scores to 0-1 range
        normalized = self._normalize_scores(importance_scores)

        # Find critical path if enabled
        critical_edges = set()
        if self.config.highlight_critical_path:
            critical_edges = self._find_critical_path(diagram, normalized)

        # Style each edge
        styled_edges = []
        for edge in diagram.edges:
            importance = normalized.get(edge.source + "_" + edge.target, 0.5)
            category = self._categorize_edge(edge)
            is_critical = (edge.source + "_" + edge.target) in critical_edges

            style = self._compute_style(edge, importance, category, is_critical)

            styled_edges.append(StyledEdge(
                edge=edge,
                style=style,
                importance=importance,
                category=category,
                is_critical=is_critical
            ))

        # Sort by z-index (low importance edges rendered first)
        styled_edges.sort(key=lambda e: e.style.z_index)

        return styled_edges

    def _calculate_importance(self, diagram: Diagram) -> Dict[str, float]:
        """Calculate raw importance scores for edges"""
        scores = {}

        if self.config.metric == ImportanceMetric.WEIGHT:
            scores = self._score_by_weight(diagram)

        elif self.config.metric == ImportanceMetric.FREQUENCY:
            scores = self._score_by_frequency(diagram)

        elif self.config.metric == ImportanceMetric.CENTRALITY:
            scores = self._score_by_centrality(diagram)

        elif self.config.metric == ImportanceMetric.CRITICALITY:
            scores = self._score_by_criticality(diagram)

        elif self.config.metric == ImportanceMetric.CUSTOM:
            if self.config.custom_scorer:
                for edge in diagram.edges:
                    key = edge.source + "_" + edge.target
                    scores[key] = self.config.custom_scorer(edge, diagram)

        return scores

    def _score_by_weight(self, diagram: Diagram) -> Dict[str, float]:
        """Score edges by their weight attribute"""
        scores = {}
        for edge in diagram.edges:
            key = edge.source + "_" + edge.target
            # Try to get weight from edge metadata or use default
            weight = getattr(edge, 'weight', None)
            if weight is None:
                weight = edge.metadata.get('weight', 1.0) if hasattr(edge, 'metadata') else 1.0
            scores[key] = float(weight)
        return scores

    def _score_by_frequency(self, diagram: Diagram) -> Dict[str, float]:
        """Score edges by connection frequency between node types"""
        # Count connections by source-target type pairs
        type_counts: Dict[Tuple[str, str], int] = {}
        edge_types: Dict[str, Tuple[str, str]] = {}

        node_types = {n.id: getattr(n, 'type', 'default') for n in diagram.nodes}

        for edge in diagram.edges:
            src_type = node_types.get(edge.source, 'default')
            tgt_type = node_types.get(edge.target, 'default')
            type_pair = (src_type, tgt_type)

            type_counts[type_pair] = type_counts.get(type_pair, 0) + 1
            edge_types[edge.source + "_" + edge.target] = type_pair

        # Score by frequency
        scores = {}
        for edge in diagram.edges:
            key = edge.source + "_" + edge.target
            type_pair = edge_types[key]
            scores[key] = float(type_counts[type_pair])

        return scores

    def _score_by_centrality(self, diagram: Diagram) -> Dict[str, float]:
        """Score edges by the centrality of connected nodes"""
        # Calculate node degree centrality
        in_degree: Dict[str, int] = {}
        out_degree: Dict[str, int] = {}

        for edge in diagram.edges:
            out_degree[edge.source] = out_degree.get(edge.source, 0) + 1
            in_degree[edge.target] = in_degree.get(edge.target, 0) + 1

        # Edge score = average of source out-degree and target in-degree
        scores = {}
        for edge in diagram.edges:
            key = edge.source + "_" + edge.target
            src_centrality = out_degree.get(edge.source, 0)
            tgt_centrality = in_degree.get(edge.target, 0)
            scores[key] = (src_centrality + tgt_centrality) / 2

        return scores

    def _score_by_criticality(self, diagram: Diagram) -> Dict[str, float]:
        """Score edges by their position in critical paths"""
        # Find longest paths and score edges on those paths higher
        scores = {e.source + "_" + e.target: 1.0 for e in diagram.edges}

        # Build adjacency list
        adj: Dict[str, List[str]] = {}
        for edge in diagram.edges:
            if edge.source not in adj:
                adj[edge.source] = []
            adj[edge.source].append(edge.target)

        # Find source nodes (no incoming edges)
        targets = {e.target for e in diagram.edges}
        sources = [n.id for n in diagram.nodes if n.id not in targets]

        # DFS to find longest paths
        for source in sources:
            path_lengths = self._dfs_longest_path(source, adj, {})
            for node, length in path_lengths.items():
                # Boost edges leading to high-length paths
                for edge in diagram.edges:
                    if edge.target == node:
                        key = edge.source + "_" + edge.target
                        scores[key] = max(scores.get(key, 0), length)

        return scores

    def _dfs_longest_path(
        self,
        node: str,
        adj: Dict[str, List[str]],
        memo: Dict[str, int]
    ) -> Dict[str, int]:
        """DFS to find longest path from each node"""
        if node in memo:
            return {node: memo[node]}

        if node not in adj or not adj[node]:
            memo[node] = 0
            return {node: 0}

        max_length = 0
        results = {node: 0}

        for neighbor in adj[node]:
            sub_paths = self._dfs_longest_path(neighbor, adj, memo)
            for n, length in sub_paths.items():
                if n not in results or length > results[n]:
                    results[n] = length
            neighbor_length = memo.get(neighbor, 0)
            max_length = max(max_length, 1 + neighbor_length)

        memo[node] = max_length
        results[node] = max_length

        return results

    def _normalize_scores(self, scores: Dict[str, float]) -> Dict[str, float]:
        """Normalize scores to 0-1 range"""
        if not scores:
            return {}

        min_score = min(scores.values())
        max_score = max(scores.values())
        score_range = max_score - min_score

        if score_range == 0:
            return {k: 0.5 for k in scores}

        return {
            k: (v - min_score) / score_range
            for k, v in scores.items()
        }

    def _find_critical_path(
        self,
        diagram: Diagram,
        normalized_scores: Dict[str, float]
    ) -> Set[str]:
        """Find edges on the critical path (highest importance path)"""
        critical = set()

        # Simple approach: edges above 80th percentile
        if not normalized_scores:
            return critical

        threshold = 0.8
        for key, score in normalized_scores.items():
            if score >= threshold:
                critical.add(key)

        return critical

    def _categorize_edge(self, edge: Edge) -> Optional[str]:
        """Determine edge category from label or metadata"""
        if edge.label:
            label_lower = edge.label.lower()

            # Check for common categories
            if any(kw in label_lower for kw in ['data', 'read', 'write', 'store']):
                return 'data_flow'
            if any(kw in label_lower for kw in ['call', 'invoke', 'request', 'api']):
                return 'control_flow'
            if any(kw in label_lower for kw in ['depend', 'require', 'import', 'use']):
                return 'dependency'
            if any(kw in label_lower for kw in ['event', 'emit', 'trigger', 'notify']):
                return 'event'
            if any(kw in label_lower for kw in ['ref', 'link', 'point']):
                return 'reference'

        return 'default'

    def _compute_style(
        self,
        edge: Edge,
        importance: float,
        category: Optional[str],
        is_critical: bool
    ) -> EdgeStyle:
        """Compute visual style for an edge"""
        style = EdgeStyle()

        # Color based on scheme
        style.stroke_color = self._get_color(importance, category)

        # Width scaling
        if self.config.scale_width:
            width_range = self.config.max_stroke_width - self.config.min_stroke_width
            style.stroke_width = self.config.min_stroke_width + importance * width_range
        else:
            style.stroke_width = (self.config.min_stroke_width + self.config.max_stroke_width) / 2

        # Opacity scaling
        if self.config.scale_opacity:
            opacity_range = self.config.max_opacity - self.config.min_opacity
            style.stroke_opacity = self.config.min_opacity + importance * opacity_range
        else:
            style.stroke_opacity = 1.0

        # Dash pattern
        if category and category in self.config.dash_patterns:
            style.stroke_dasharray = self.config.dash_patterns[category]

        # Glow for high importance
        if self.config.enable_glow and importance >= self.config.glow_threshold:
            style.glow = True
            style.glow_color = style.stroke_color
            style.glow_intensity = (importance - self.config.glow_threshold) / (1 - self.config.glow_threshold)

        # Critical path enhancement
        if is_critical:
            style.stroke_width *= self.config.critical_path_width_multiplier
            style.stroke_color = self.config.highlight_color
            style.glow = True
            style.glow_color = self.config.highlight_color
            style.glow_intensity = 0.8

        # Z-index based on importance (important edges on top)
        style.z_index = int(importance * 100)

        # Arrow size proportional to width
        style.arrow_size = 6 + style.stroke_width

        return style

    def _get_color(self, importance: float, category: Optional[str]) -> str:
        """Get edge color based on scheme and importance"""
        scheme = self.config.color_scheme

        if scheme == ColorScheme.MONOCHROME:
            return self.config.base_color

        elif scheme == ColorScheme.CATEGORICAL:
            return self.config.category_colors.get(category or 'default', self.config.base_color)

        elif scheme == ColorScheme.SEMANTIC:
            return self.config.semantic_colors.get(category or 'default', self.config.base_color)

        elif scheme == ColorScheme.GRADIENT:
            return self._interpolate_color(
                self.config.low_importance_color,
                self.config.high_importance_color,
                importance
            )

        elif scheme == ColorScheme.HEATMAP:
            return self._heatmap_color(importance)

        return self.config.base_color

    def _interpolate_color(self, color1: str, color2: str, t: float) -> str:
        """Interpolate between two hex colors"""
        r1, g1, b1 = self._hex_to_rgb(color1)
        r2, g2, b2 = self._hex_to_rgb(color2)

        r = int(r1 + t * (r2 - r1))
        g = int(g1 + t * (g2 - g1))
        b = int(b1 + t * (b2 - b1))

        return f"#{r:02x}{g:02x}{b:02x}"

    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _heatmap_color(self, value: float) -> str:
        """Generate heatmap color (blue -> green -> yellow -> red)"""
        if value < 0.25:
            # Blue to cyan
            t = value / 0.25
            return self._interpolate_color("#3182CE", "#38B2AC", t)
        elif value < 0.5:
            # Cyan to green
            t = (value - 0.25) / 0.25
            return self._interpolate_color("#38B2AC", "#38A169", t)
        elif value < 0.75:
            # Green to yellow
            t = (value - 0.5) / 0.25
            return self._interpolate_color("#38A169", "#D69E2E", t)
        else:
            # Yellow to red
            t = (value - 0.75) / 0.25
            return self._interpolate_color("#D69E2E", "#E53E3E", t)

    def build_svg_styles(self, styled_edges: List[StyledEdge]) -> str:
        """Build SVG style definitions for styled edges"""
        svg_parts = []

        # Glow filter definition
        svg_parts.append('''
        <defs>
            <filter id="edge-glow" x="-50%" y="-50%" width="200%" height="200%">
                <feGaussianBlur in="SourceAlpha" stdDeviation="3" result="blur"/>
                <feFlood flood-color="currentColor" flood-opacity="0.5" result="flood"/>
                <feComposite in="flood" in2="blur" operator="in" result="glow"/>
                <feMerge>
                    <feMergeNode in="glow"/>
                    <feMergeNode in="SourceGraphic"/>
                </feMerge>
            </filter>
        </defs>
        ''')

        # Generate CSS for each edge
        css_rules = []
        for i, se in enumerate(styled_edges):
            rule = f'''
            .edge-{i} {{
                stroke: {se.style.stroke_color};
                stroke-width: {se.style.stroke_width}px;
                stroke-opacity: {se.style.stroke_opacity};
                fill: none;
                {"stroke-dasharray: " + se.style.stroke_dasharray + ";" if se.style.stroke_dasharray else ""}
                {"filter: url(#edge-glow);" if se.style.glow else ""}
            }}
            '''
            css_rules.append(rule)

        svg_parts.append(f'<style>{" ".join(css_rules)}</style>')

        return '\n'.join(svg_parts)


def style_edges(
    diagram: Diagram,
    metric: ImportanceMetric = ImportanceMetric.WEIGHT,
    color_scheme: ColorScheme = ColorScheme.HEATMAP
) -> List[StyledEdge]:
    """
    Apply importance-based styling to diagram edges.

    Args:
        diagram: The diagram to style
        metric: Importance metric to use
        color_scheme: Color scheme for styling

    Returns:
        List of styled edges

    Example:
        >>> styled = style_edges(diagram, metric=ImportanceMetric.CENTRALITY)
        >>> for edge in styled:
        ...     print(f"Importance: {edge.importance:.2f}")
    """
    config = StyleConfig(metric=metric, color_scheme=color_scheme)
    styler = EdgeStyler(config)
    return styler.style(diagram)
