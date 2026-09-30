"""Theme mapper — converts extracted tokens into a react_theme.json-compatible dict.

Ensures all required fields are present with sensible defaults, and normalizes
values to match the ThemeDefinition schema expected by REAW Phase 2.
"""

from datetime import datetime, timezone
from typing import Any, Dict


# Default values for any tokens not extracted
_DEFAULTS = {
    "colorPalette": {
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
    },
    "typography": {
        "fontFamily": "Inter, system-ui, sans-serif",
        "fontSize": "14px",
        "fontSizeSmall": "12px",
        "fontSizeLarge": "18px",
        "headingFontFamily": None,
        "headingFontWeight": "600",
        "lineHeight": "1.5",
    },
    "spacing": {
        "unit": "8px",
        "small": "4px",
        "medium": "8px",
        "large": "16px",
        "xlarge": "24px",
    },
    "borders": {
        "radius": "6px",
        "radiusLarge": "12px",
        "width": "1px",
        "color": "#dee2e6",
    },
    "shadows": {
        "small": "0 1px 2px rgba(0,0,0,0.05)",
        "medium": "0 4px 6px rgba(0,0,0,0.1)",
        "large": "0 10px 15px rgba(0,0,0,0.1)",
    },
}


def map_to_theme_definition(tokens: Dict[str, Any]) -> Dict[str, Any]:
    """Map extracted tokens to a complete react_theme.json structure.

    Fills in defaults for any missing values and adds animation settings.

    Args:
        tokens: Raw tokens from token_extractor.extract_tokens().

    Returns:
        Dict matching the ThemeDefinition schema, ready to write as JSON.
    """
    theme: Dict[str, Any] = {}

    # Color palette — merge extracted over defaults
    palette = dict(_DEFAULTS["colorPalette"])
    palette.update(tokens.get("colorPalette", {}))
    theme["colorPalette"] = palette

    # Typography — merge extracted over defaults
    typo = dict(_DEFAULTS["typography"])
    extracted_typo = tokens.get("typography", {})
    for k, v in extracted_typo.items():
        if v is not None and v != "":
            typo[k] = v
    theme["typography"] = typo

    # Spacing
    spacing = dict(_DEFAULTS["spacing"])
    spacing.update({k: v for k, v in tokens.get("spacing", {}).items() if v})
    theme["spacing"] = spacing

    # Borders
    borders = dict(_DEFAULTS["borders"])
    borders.update({k: v for k, v in tokens.get("borders", {}).items() if v})
    theme["borders"] = borders

    # Shadows
    shadows = dict(_DEFAULTS["shadows"])
    shadows.update({k: v for k, v in tokens.get("shadows", {}).items() if v})
    theme["shadows"] = shadows

    # Component tokens (no defaults — only what was scraped)
    theme["components"] = tokens.get("components", {
        "button": {}, "input": {}, "card": {}, "table": {}, "sidebar": {},
    })

    # Animations — keep defaults (scraper doesn't extract these)
    theme["animationsEnabled"] = True
    theme["animationStyle"] = {
        "transitionDuration": "200ms",
        "easingFunction": "ease-out",
        "hover": {"type": "background-shift", "intensity": "subtle"},
        "focus": {"type": "outline", "intensity": "mild"},
        "click": {"type": "scale", "intensity": "subtle"},
        "selection": {"type": "fade", "intensity": "mild"},
    }

    # Source metadata
    source = tokens.get("source", {})
    source["scrapedAt"] = datetime.now(timezone.utc).isoformat()
    theme["source"] = source

    return theme
