"""Theme transformer — generates default soft pastel theme configuration."""

from models.react_definition_models import (
    AnimationEffectDef,
    AnimationStyleDef,
    BordersDef,
    ComponentTokensDef,
    ShadowsDef,
    SpacingDef,
    ThemeDefinition,
    TypographyDef,
)


# Default soft, muted, pastel-like color palette
_DEFAULT_PALETTE = {
    "background-primary": "#f8f9fa",
    "background-secondary": "#ffffff",
    "surface": "#f1f3f5",
    "border": "#dee2e6",
    "text-primary": "#495057",
    "text-secondary": "#868e96",
    "accent": "#748ffc",
    "accent-hover": "#5c7cfa",
    "success": "#69db7c",
    "warning": "#ffd43b",
    "error": "#ff8787",
    "info": "#74c0fc",
}


class ThemeTransformer:
    """Generates default theme configuration."""

    @staticmethod
    def transform() -> ThemeDefinition:
        """Produce default ThemeDefinition with soft pastel palette and subtle animations.

        Returns:
            ThemeDefinition with default color palette, typography, spacing, and animation settings.
        """
        return ThemeDefinition(
            colorPalette=dict(_DEFAULT_PALETTE),
            typography=TypographyDef(),
            spacing=SpacingDef(),
            borders=BordersDef(),
            shadows=ShadowsDef(),
            components=ComponentTokensDef(),
            animationsEnabled=True,
            animationStyle=AnimationStyleDef(
                transitionDuration="200ms",
                easingFunction="ease-out",
                hover=AnimationEffectDef(type="background-shift", intensity="subtle"),
                focus=AnimationEffectDef(type="outline", intensity="mild"),
                click=AnimationEffectDef(type="scale", intensity="subtle"),
                selection=AnimationEffectDef(type="fade", intensity="mild"),
            ),
        )
