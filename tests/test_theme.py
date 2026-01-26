"""Tests for theme system"""

import pytest
import json
from viralify_diagrams import Theme, ThemeManager
from viralify_diagrams.core.theme import ThemeColors, ThemeTypography, ThemeSpacing


class TestTheme:
    """Tests for Theme class"""

    def test_create_theme(self):
        """Test creating a theme"""
        theme = Theme(
            name="test-theme",
            colors=ThemeColors(),
            typography=ThemeTypography(),
            spacing=ThemeSpacing()
        )

        assert theme.name == "test-theme"
        assert theme.colors is not None
        assert theme.typography is not None
        assert theme.spacing is not None

    def test_theme_from_json(self):
        """Test creating theme from JSON"""
        json_str = '''
        {
            "name": "custom",
            "colors": {
                "background": "#ff0000",
                "node_fill": "#00ff00"
            }
        }
        '''
        theme = Theme.from_json(json_str)

        assert theme.name == "custom"
        assert theme.colors.background == "#ff0000"
        assert theme.colors.node_fill == "#00ff00"

    def test_theme_to_json(self):
        """Test exporting theme to JSON"""
        theme = Theme(
            name="export-test",
            colors=ThemeColors(background="#123456"),
            typography=ThemeTypography(),
            spacing=ThemeSpacing()
        )

        json_str = theme.to_json()
        data = json.loads(json_str)

        assert data["name"] == "export-test"
        assert data["colors"]["background"] == "#123456"

    def test_theme_partial_json(self):
        """Test creating theme from partial JSON (should use defaults)"""
        json_str = '{"name": "minimal"}'
        theme = Theme.from_json(json_str)

        assert theme.name == "minimal"
        # Should have default colors
        assert theme.colors.background == "#1a1a2e"


class TestThemeColors:
    """Tests for ThemeColors class"""

    def test_default_colors(self):
        """Test default color values"""
        colors = ThemeColors()

        assert colors.background == "#1a1a2e"
        assert colors.node_fill == "#16213e"
        assert colors.node_stroke == "#4a9eff"

    def test_custom_colors(self):
        """Test custom color values"""
        colors = ThemeColors(
            background="#000000",
            node_fill="#ffffff",
            edge_color="#ff0000"
        )

        assert colors.background == "#000000"
        assert colors.node_fill == "#ffffff"
        assert colors.edge_color == "#ff0000"


class TestThemeManager:
    """Tests for ThemeManager class"""

    def test_get_builtin_theme(self):
        """Test getting built-in themes"""
        manager = ThemeManager()

        dark = manager.get("dark")
        assert dark is not None
        assert dark.name == "dark"

        light = manager.get("light")
        assert light is not None
        assert light.name == "light"

    def test_register_custom_theme(self):
        """Test registering custom themes"""
        manager = ThemeManager()
        custom = Theme(
            name="my-custom",
            colors=ThemeColors(),
            typography=ThemeTypography(),
            spacing=ThemeSpacing()
        )

        manager.register(custom)
        retrieved = manager.get("my-custom")

        assert retrieved is not None
        assert retrieved.name == "my-custom"

    def test_list_themes(self):
        """Test listing available themes"""
        manager = ThemeManager()
        themes = manager.list_themes()

        assert "dark" in themes
        assert "light" in themes
        assert "corporate" in themes

    def test_get_missing_theme_returns_default(self):
        """Test that missing theme returns default"""
        manager = ThemeManager()
        theme = manager.get("nonexistent-theme")

        # Should return default (dark) theme
        assert theme is not None
        assert theme.name == "dark"
