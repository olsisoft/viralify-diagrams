"""
Theme System for Viralify Diagrams

Supports:
- Built-in themes (dark, light, gradient, ocean)
- User-uploaded custom themes (JSON format)
- Theme inheritance and overrides
"""

import json
import os
from dataclasses import dataclass, field
from typing import Dict, Optional, Any, List
from pathlib import Path


@dataclass
class ThemeColors:
    """Color palette for a theme"""
    # Background
    background: str = "#1a1a2e"
    background_secondary: str = "#16213e"

    # Text
    text_primary: str = "#ffffff"
    text_secondary: str = "#a0a0a0"
    text_label: str = "#e0e0e0"

    # Nodes
    node_fill: str = "#0f3460"
    node_stroke: str = "#e94560"
    node_stroke_width: int = 2

    # Edges
    edge_color: str = "#e94560"
    edge_width: int = 2
    edge_arrow_color: str = "#e94560"

    # Clusters
    cluster_fill: str = "#16213e"
    cluster_stroke: str = "#0f3460"
    cluster_stroke_width: int = 2
    cluster_label_color: str = "#ffffff"

    # Highlights
    highlight_primary: str = "#e94560"
    highlight_secondary: str = "#00d9ff"
    highlight_success: str = "#00ff88"
    highlight_warning: str = "#ffaa00"
    highlight_error: str = "#ff4444"

    # Shadows and effects
    shadow_color: str = "rgba(0,0,0,0.3)"
    shadow_blur: int = 10
    glow_color: str = "#e94560"
    glow_blur: int = 15

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "background": self.background,
            "background_secondary": self.background_secondary,
            "text_primary": self.text_primary,
            "text_secondary": self.text_secondary,
            "text_label": self.text_label,
            "node_fill": self.node_fill,
            "node_stroke": self.node_stroke,
            "node_stroke_width": self.node_stroke_width,
            "edge_color": self.edge_color,
            "edge_width": self.edge_width,
            "edge_arrow_color": self.edge_arrow_color,
            "cluster_fill": self.cluster_fill,
            "cluster_stroke": self.cluster_stroke,
            "cluster_stroke_width": self.cluster_stroke_width,
            "cluster_label_color": self.cluster_label_color,
            "highlight_primary": self.highlight_primary,
            "highlight_secondary": self.highlight_secondary,
            "highlight_success": self.highlight_success,
            "highlight_warning": self.highlight_warning,
            "highlight_error": self.highlight_error,
            "shadow_color": self.shadow_color,
            "shadow_blur": self.shadow_blur,
            "glow_color": self.glow_color,
            "glow_blur": self.glow_blur,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThemeColors":
        """Create from dictionary"""
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})


@dataclass
class ThemeTypography:
    """Typography settings for a theme"""
    font_family: str = "Inter, Arial, sans-serif"
    font_size_title: int = 24
    font_size_label: int = 14
    font_size_small: int = 10
    font_weight_title: str = "bold"
    font_weight_label: str = "normal"
    letter_spacing: float = 0.5

    def to_dict(self) -> Dict[str, Any]:
        return {
            "font_family": self.font_family,
            "font_size_title": self.font_size_title,
            "font_size_label": self.font_size_label,
            "font_size_small": self.font_size_small,
            "font_weight_title": self.font_weight_title,
            "font_weight_label": self.font_weight_label,
            "letter_spacing": self.letter_spacing,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThemeTypography":
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})


@dataclass
class ThemeSpacing:
    """Spacing and sizing for a theme"""
    node_width: int = 120
    node_height: int = 80
    node_padding: int = 12
    node_margin: int = 20
    node_border_radius: int = 8

    cluster_padding: int = 30
    cluster_margin: int = 20
    cluster_border_radius: int = 12

    edge_curve_strength: float = 0.3
    arrow_size: int = 10

    icon_size: int = 48
    icon_padding: int = 8

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_width": self.node_width,
            "node_height": self.node_height,
            "node_padding": self.node_padding,
            "node_margin": self.node_margin,
            "node_border_radius": self.node_border_radius,
            "cluster_padding": self.cluster_padding,
            "cluster_margin": self.cluster_margin,
            "cluster_border_radius": self.cluster_border_radius,
            "edge_curve_strength": self.edge_curve_strength,
            "arrow_size": self.arrow_size,
            "icon_size": self.icon_size,
            "icon_padding": self.icon_padding,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ThemeSpacing":
        return cls(**{k: v for k, v in data.items() if hasattr(cls, k)})


@dataclass
class Theme:
    """Complete theme configuration"""
    name: str
    description: str = ""
    version: str = "1.0.0"
    author: str = ""

    colors: ThemeColors = field(default_factory=ThemeColors)
    typography: ThemeTypography = field(default_factory=ThemeTypography)
    spacing: ThemeSpacing = field(default_factory=ThemeSpacing)

    # Custom properties for extensions
    custom: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Export theme as dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "colors": self.colors.to_dict(),
            "typography": self.typography.to_dict(),
            "spacing": self.spacing.to_dict(),
            "custom": self.custom,
        }

    def to_json(self, indent: int = 2) -> str:
        """Export theme as JSON string"""
        return json.dumps(self.to_dict(), indent=indent)

    def save(self, path: str) -> None:
        """Save theme to JSON file"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.to_json())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Theme":
        """Create theme from dictionary"""
        return cls(
            name=data.get("name", "custom"),
            description=data.get("description", ""),
            version=data.get("version", "1.0.0"),
            author=data.get("author", ""),
            colors=ThemeColors.from_dict(data.get("colors", {})),
            typography=ThemeTypography.from_dict(data.get("typography", {})),
            spacing=ThemeSpacing.from_dict(data.get("spacing", {})),
            custom=data.get("custom", {}),
        )

    @classmethod
    def from_json(cls, json_str: str) -> "Theme":
        """Create theme from JSON string"""
        return cls.from_dict(json.loads(json_str))

    @classmethod
    def load(cls, path: str) -> "Theme":
        """Load theme from JSON file"""
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_json(f.read())

    def merge_with(self, other: "Theme") -> "Theme":
        """Create new theme by merging with another (other overrides self)"""
        self_dict = self.to_dict()
        other_dict = other.to_dict()

        # Deep merge
        def deep_merge(base: dict, override: dict) -> dict:
            result = base.copy()
            for key, value in override.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = deep_merge(result[key], value)
                else:
                    result[key] = value
            return result

        merged = deep_merge(self_dict, other_dict)
        merged["name"] = f"{self.name}+{other.name}"
        return Theme.from_dict(merged)


class ThemeManager:
    """
    Manages theme loading, caching, and user theme uploads.
    """

    def __init__(self, themes_dir: Optional[str] = None):
        self.themes_dir = Path(themes_dir) if themes_dir else Path(__file__).parent.parent / "themes"
        self._cache: Dict[str, Theme] = {}
        self._load_builtin_themes()

    def _load_builtin_themes(self) -> None:
        """Load built-in themes"""
        self._cache["dark"] = self._create_dark_theme()
        self._cache["light"] = self._create_light_theme()
        self._cache["gradient"] = self._create_gradient_theme()
        self._cache["ocean"] = self._create_ocean_theme()
        self._cache["corporate"] = self._create_corporate_theme()
        self._cache["neon"] = self._create_neon_theme()

    def _create_dark_theme(self) -> Theme:
        """Create dark theme (default)"""
        return Theme(
            name="dark",
            description="Dark theme optimized for video presentations",
            author="Viralify",
            colors=ThemeColors(
                background="#1a1a2e",
                background_secondary="#16213e",
                text_primary="#ffffff",
                text_secondary="#a0a0a0",
                node_fill="#0f3460",
                node_stroke="#e94560",
                edge_color="#e94560",
                cluster_fill="#16213e",
                cluster_stroke="#0f3460",
                highlight_primary="#e94560",
                highlight_secondary="#00d9ff",
            ),
        )

    def _create_light_theme(self) -> Theme:
        """Create light theme"""
        return Theme(
            name="light",
            description="Light theme for bright presentations",
            author="Viralify",
            colors=ThemeColors(
                background="#ffffff",
                background_secondary="#f5f5f5",
                text_primary="#1a1a2e",
                text_secondary="#666666",
                node_fill="#e8e8e8",
                node_stroke="#3498db",
                edge_color="#3498db",
                cluster_fill="#f0f0f0",
                cluster_stroke="#cccccc",
                highlight_primary="#3498db",
                highlight_secondary="#e74c3c",
            ),
        )

    def _create_gradient_theme(self) -> Theme:
        """Create gradient theme"""
        return Theme(
            name="gradient",
            description="Gradient theme with modern aesthetics",
            author="Viralify",
            colors=ThemeColors(
                background="#0f0c29",
                background_secondary="#302b63",
                text_primary="#ffffff",
                text_secondary="#b8b8d1",
                node_fill="#24243e",
                node_stroke="#ff6b6b",
                edge_color="#4ecdc4",
                cluster_fill="#302b63",
                cluster_stroke="#24243e",
                highlight_primary="#ff6b6b",
                highlight_secondary="#4ecdc4",
                glow_color="#ff6b6b",
            ),
        )

    def _create_ocean_theme(self) -> Theme:
        """Create ocean theme"""
        return Theme(
            name="ocean",
            description="Ocean-inspired blue theme",
            author="Viralify",
            colors=ThemeColors(
                background="#0a1628",
                background_secondary="#0d2137",
                text_primary="#ffffff",
                text_secondary="#7eb8da",
                node_fill="#1a3a5c",
                node_stroke="#00b4d8",
                edge_color="#00b4d8",
                cluster_fill="#0d2137",
                cluster_stroke="#1a3a5c",
                highlight_primary="#00b4d8",
                highlight_secondary="#90e0ef",
                glow_color="#00b4d8",
            ),
        )

    def _create_corporate_theme(self) -> Theme:
        """Create corporate/professional theme"""
        return Theme(
            name="corporate",
            description="Professional corporate theme",
            author="Viralify",
            colors=ThemeColors(
                background="#ffffff",
                background_secondary="#f8f9fa",
                text_primary="#212529",
                text_secondary="#6c757d",
                node_fill="#ffffff",
                node_stroke="#0066cc",
                edge_color="#0066cc",
                cluster_fill="#f8f9fa",
                cluster_stroke="#dee2e6",
                highlight_primary="#0066cc",
                highlight_secondary="#28a745",
            ),
            typography=ThemeTypography(
                font_family="Segoe UI, Roboto, Arial, sans-serif",
            ),
        )

    def _create_neon_theme(self) -> Theme:
        """Create neon/cyberpunk theme"""
        return Theme(
            name="neon",
            description="Neon cyberpunk theme",
            author="Viralify",
            colors=ThemeColors(
                background="#0a0a0a",
                background_secondary="#1a1a1a",
                text_primary="#ffffff",
                text_secondary="#888888",
                node_fill="#1a1a1a",
                node_stroke="#ff00ff",
                edge_color="#00ffff",
                cluster_fill="#0f0f0f",
                cluster_stroke="#ff00ff",
                highlight_primary="#ff00ff",
                highlight_secondary="#00ffff",
                glow_color="#ff00ff",
                glow_blur=20,
            ),
        )

    def get(self, name: str) -> Theme:
        """Get a theme by name"""
        if name in self._cache:
            return self._cache[name]

        # Try loading from file
        theme_file = self.themes_dir / f"{name}.json"
        if theme_file.exists():
            theme = Theme.load(str(theme_file))
            self._cache[name] = theme
            return theme

        raise ValueError(f"Theme '{name}' not found")

    def register(self, theme: Theme) -> None:
        """Register a custom theme"""
        self._cache[theme.name] = theme

    def register_from_file(self, path: str) -> Theme:
        """Register a theme from a JSON file"""
        theme = Theme.load(path)
        self.register(theme)
        return theme

    def register_from_json(self, json_str: str) -> Theme:
        """Register a theme from a JSON string"""
        theme = Theme.from_json(json_str)
        self.register(theme)
        return theme

    def list_themes(self) -> List[str]:
        """List all available theme names"""
        themes = list(self._cache.keys())

        # Add themes from directory
        if self.themes_dir.exists():
            for f in self.themes_dir.glob("*.json"):
                name = f.stem
                if name not in themes:
                    themes.append(name)

        return sorted(themes)

    def export_theme(self, name: str, path: str) -> None:
        """Export a theme to a JSON file"""
        theme = self.get(name)
        theme.save(path)


# Global theme manager instance
_theme_manager: Optional[ThemeManager] = None


def get_theme_manager() -> ThemeManager:
    """Get the global theme manager instance"""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager
