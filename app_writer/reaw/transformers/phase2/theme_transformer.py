"""Theme transformer (Phase 2) — produces ThemeProperties from ThemeDefinition."""

from models.property_objects import ThemeProperties
from models.react_definition_models import ThemeDefinition


class Phase2ThemeTransformer:
    """Transforms theme definition into template-ready theme properties."""

    @staticmethod
    def transform(theme: ThemeDefinition) -> ThemeProperties:
        """Produce theme properties for CSS variable and override templates.

        Args:
            theme: Theme definition from react_theme.json.

        Returns:
            ThemeProperties for template rendering.
        """
        return ThemeProperties(
            colorPalette=theme.colorPalette,
            typography=theme.typography,
            spacing=theme.spacing,
            borders=theme.borders,
            shadows=theme.shadows,
            components=theme.components,
            animationsEnabled=theme.animationsEnabled,
            animationStyle=theme.animationStyle if theme.animationsEnabled else None,
        )
