"""Token extractor — analyzes raw scraped data and produces normalized design tokens.

Takes ScrapedStyles (computed styles, CSS variables, stylesheet contents) and
produces a structured dict of design tokens: palette, typography, spacing,
borders, shadows, and component-specific overrides.
"""

import colorsys
import re
from typing import Any, Dict, List, Optional, Tuple

from theme_scraper.scraper import ScrapedStyles
from theme_scraper.css_parser import extract_variables_from_css


# ─── Color utilities ────────────────────────────────────────────────────────

def _parse_color_to_rgb(color: str) -> Optional[Tuple[int, int, int]]:
    """Parse a CSS color string to (r, g, b) tuple."""
    color = color.strip()

    # Hex
    m = re.match(r'^#([0-9a-fA-F]{3,8})$', color)
    if m:
        h = m.group(1)
        if len(h) == 3:
            r, g, b = int(h[0]*2, 16), int(h[1]*2, 16), int(h[2]*2, 16)
        elif len(h) >= 6:
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        else:
            return None
        return (r, g, b)

    # rgb(r, g, b) or rgba(r, g, b, a)
    m = re.match(r'rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)', color)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))

    return None


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"


def _color_distance(c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> float:
    """Simple Euclidean distance in RGB space."""
    return ((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2) ** 0.5


def _is_near_white(rgb: Tuple[int, int, int], threshold: int = 240) -> bool:
    return all(c >= threshold for c in rgb)


def _is_near_black(rgb: Tuple[int, int, int], threshold: int = 30) -> bool:
    return all(c <= threshold for c in rgb)


def _lightness(rgb: Tuple[int, int, int]) -> float:
    """HSL lightness 0-1."""
    r, g, b = rgb[0]/255, rgb[1]/255, rgb[2]/255
    _, l, _ = colorsys.rgb_to_hls(r, g, b)
    return l


def _saturation(rgb: Tuple[int, int, int]) -> float:
    r, g, b = rgb[0]/255, rgb[1]/255, rgb[2]/255
    _, _, s = colorsys.rgb_to_hls(r, g, b)
    return s


# ─── Color clustering ──────────────────────────────────────────────────────

def _cluster_colors(colors: List[Tuple[int, int, int]], threshold: float = 30) -> List[Tuple[int, int, int]]:
    """Simple greedy clustering: merge colors within threshold distance."""
    if not colors:
        return []
    clusters: List[List[Tuple[int, int, int]]] = []
    for c in colors:
        merged = False
        for cluster in clusters:
            if _color_distance(c, cluster[0]) < threshold:
                cluster.append(c)
                merged = True
                break
        if not merged:
            clusters.append([c])

    # Return the first (most representative) color from each cluster
    return [cl[0] for cl in clusters]


def _classify_palette(colors: List[Tuple[int, int, int]]) -> Dict[str, str]:
    """Classify clustered colors into semantic roles."""
    palette: Dict[str, str] = {}

    # Separate by characteristics
    whites = [c for c in colors if _is_near_white(c)]
    blacks = [c for c in colors if _is_near_black(c)]
    chromatic = [c for c in colors if not _is_near_white(c) and not _is_near_black(c)]

    # Sort chromatic by saturation (most saturated = likely accent/primary)
    chromatic.sort(key=lambda c: _saturation(c), reverse=True)

    # Backgrounds
    if whites:
        palette["background-primary"] = _rgb_to_hex(*whites[0])
        if len(whites) > 1:
            palette["background-secondary"] = _rgb_to_hex(*whites[1])
        palette["surface"] = _rgb_to_hex(*whites[-1])

    # Text
    if blacks:
        palette["text-primary"] = _rgb_to_hex(*blacks[0])
        if len(blacks) > 1:
            palette["text-secondary"] = _rgb_to_hex(*blacks[1])

    # Accent / primary color (most saturated chromatic)
    if chromatic:
        palette["accent"] = _rgb_to_hex(*chromatic[0])
        # Try to find a hover variant (slightly different)
        if len(chromatic) > 1:
            palette["accent-hover"] = _rgb_to_hex(*chromatic[1])

    # Try to identify semantic colors by hue
    for c in chromatic:
        r, g, b = c[0]/255, c[1]/255, c[2]/255
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        hue_deg = h * 360

        if s > 0.3:
            if 0 <= hue_deg <= 30 or 340 <= hue_deg <= 360:
                if "error" not in palette:
                    palette["error"] = _rgb_to_hex(*c)
            elif 30 < hue_deg <= 70:
                if "warning" not in palette:
                    palette["warning"] = _rgb_to_hex(*c)
            elif 90 < hue_deg <= 160:
                if "success" not in palette:
                    palette["success"] = _rgb_to_hex(*c)
            elif 190 < hue_deg <= 260:
                if "info" not in palette:
                    palette["info"] = _rgb_to_hex(*c)

    # Border color — look for a mid-gray
    grays = [c for c in colors if _saturation(c) < 0.1 and 0.3 < _lightness(c) < 0.9]
    if grays:
        # Pick the lightest gray as border
        grays.sort(key=lambda c: _lightness(c), reverse=True)
        palette["border"] = _rgb_to_hex(*grays[0])

    return palette


# ─── Main extraction ────────────────────────────────────────────────────────

def extract_tokens(scraped: ScrapedStyles) -> Dict[str, Any]:
    """Extract structured design tokens from raw scraped data.

    Returns a dict matching the react_theme.json schema:
    {colorPalette, typography, spacing, borders, shadows, components, source}
    """
    tokens: Dict[str, Any] = {}

    # ── 1. Color palette ──
    # Collect all colors from computed styles
    all_color_strings: List[str] = []
    for role, styles in scraped.element_styles.items():
        for prop in ("backgroundColor", "color", "borderColor"):
            val = styles.get(prop, "")
            if val and val != "rgba(0, 0, 0, 0)" and val != "transparent":
                all_color_strings.append(val)

    # Also from CSS variables
    for name, val in scraped.css_variables.items():
        if re.match(r'^(#|rgb|hsl)', val.strip()):
            all_color_strings.append(val)

    # Also from downloaded stylesheets
    stylesheet_vars = extract_variables_from_css(scraped.stylesheet_contents)
    for name, val in stylesheet_vars.items():
        if re.match(r'^(#|rgb|hsl)', val.strip()):
            all_color_strings.append(val)
        # Merge into css_variables for later use
        if name not in scraped.css_variables:
            scraped.css_variables[name] = val

    # Parse to RGB, cluster, classify
    rgb_colors = []
    for cs in all_color_strings:
        rgb = _parse_color_to_rgb(cs)
        if rgb:
            rgb_colors.append(rgb)

    clustered = _cluster_colors(rgb_colors)
    palette = _classify_palette(clustered)

    # Override with explicit CSS variable mappings if they exist
    var_mapping = {
        "--primary-color": "accent",
        "--primary": "accent",
        "--accent": "accent",
        "--bg-primary": "background-primary",
        "--bg-secondary": "background-secondary",
        "--background": "background-primary",
        "--surface": "surface",
        "--text-color": "text-primary",
        "--text-primary": "text-primary",
        "--text-secondary": "text-secondary",
        "--border-color": "border",
        "--success": "success",
        "--warning": "warning",
        "--danger": "error",
        "--error": "error",
        "--info": "info",
    }
    for css_var, token_name in var_mapping.items():
        if css_var in scraped.css_variables:
            palette[token_name] = scraped.css_variables[css_var]

    tokens["colorPalette"] = palette

    # ── 2. Typography ──
    body = scraped.element_styles.get("body", {})
    h1 = scraped.element_styles.get("heading_h1", {})
    h2 = scraped.element_styles.get("heading_h2", {})

    body_font = body.get("fontFamily", "Inter, system-ui, sans-serif")
    heading_font = h1.get("fontFamily", body_font)

    tokens["typography"] = {
        "fontFamily": _clean_font_family(body_font),
        "fontSize": body.get("fontSize", "14px"),
        "fontSizeSmall": "12px",
        "fontSizeLarge": h2.get("fontSize", "18px"),
        "headingFontFamily": _clean_font_family(heading_font) if heading_font != body_font else None,
        "headingFontWeight": h1.get("fontWeight", "600"),
        "lineHeight": body.get("lineHeight", "1.5"),
    }

    # ── 3. Spacing ──
    # Extract padding values from inputs and buttons to infer spacing scale
    btn = scraped.element_styles.get("button_primary", {})
    inp = scraped.element_styles.get("input", {})
    btn_padding = btn.get("padding", "")
    inp_padding = inp.get("padding", "")

    base_spacing = _extract_spacing_unit(btn_padding, inp_padding)
    tokens["spacing"] = {
        "unit": f"{base_spacing}px",
        "small": f"{max(base_spacing // 2, 2)}px",
        "medium": f"{base_spacing}px",
        "large": f"{base_spacing * 2}px",
        "xlarge": f"{base_spacing * 3}px",
    }

    # ── 4. Borders ──
    btn_radius = btn.get("borderRadius", "6px")
    card = scraped.element_styles.get("card", {})
    card_radius = card.get("borderRadius", "")
    inp_radius = inp.get("borderRadius", "")

    tokens["borders"] = {
        "radius": _first_valid(inp_radius, btn_radius, "6px"),
        "radiusLarge": _first_valid(card_radius, "12px"),
        "width": btn.get("borderWidth", inp.get("borderWidth", "1px")),
        "color": palette.get("border", "#dee2e6"),
    }

    # ── 5. Shadows ──
    card_shadow = card.get("boxShadow", "")
    btn_shadow = btn.get("boxShadow", "")

    tokens["shadows"] = {
        "small": _first_valid(btn_shadow, "0 1px 2px rgba(0,0,0,0.05)"),
        "medium": _first_valid(card_shadow, "0 4px 6px rgba(0,0,0,0.1)"),
        "large": "0 10px 15px rgba(0,0,0,0.1)",
    }
    # Clean "none" values
    for k, v in tokens["shadows"].items():
        if v == "none" or not v.strip():
            tokens["shadows"][k] = {"small": "0 1px 2px rgba(0,0,0,0.05)",
                                     "medium": "0 4px 6px rgba(0,0,0,0.1)",
                                     "large": "0 10px 15px rgba(0,0,0,0.1)"}[k]

    # ── 6. Component tokens ──
    sidebar = scraped.element_styles.get("sidebar", scraped.element_styles.get("nav", {}))
    table_header = scraped.element_styles.get("table_header", {})
    table_row = scraped.element_styles.get("table_row", {})

    tokens["components"] = {
        "button": _filter_empty({
            "borderRadius": btn.get("borderRadius", ""),
            "fontWeight": btn.get("fontWeight", ""),
            "padding": btn.get("padding", ""),
        }),
        "input": _filter_empty({
            "borderRadius": inp.get("borderRadius", ""),
            "borderColor": inp.get("borderColor", ""),
            "padding": inp.get("padding", ""),
        }),
        "card": _filter_empty({
            "borderRadius": card.get("borderRadius", ""),
            "shadow": card.get("boxShadow", ""),
        }),
        "table": _filter_empty({
            "headerBackground": table_header.get("backgroundColor", ""),
            "rowHoverBackground": "",  # Can't detect hover via computed styles
        }),
        "sidebar": _filter_empty({
            "background": sidebar.get("backgroundColor", ""),
            "textColor": sidebar.get("color", ""),
        }),
    }

    # ── 7. Source metadata ──
    tokens["source"] = {
        "url": scraped.url,
        "scrapedAt": "",  # Filled by caller
    }

    return tokens


# ─── Helpers ────────────────────────────────────────────────────────────────

def _clean_font_family(raw: str) -> str:
    """Clean up a computed fontFamily string."""
    if not raw:
        return "Inter, system-ui, sans-serif"
    # Remove extra quotes and normalize
    cleaned = raw.replace('"', "'")
    # Limit to first 3 families
    parts = [p.strip() for p in cleaned.split(",")]
    return ", ".join(parts[:3])


def _extract_spacing_unit(btn_padding: str, inp_padding: str) -> int:
    """Infer a base spacing unit from padding values."""
    for padding_str in (btn_padding, inp_padding):
        if not padding_str:
            continue
        nums = re.findall(r'(\d+(?:\.\d+)?)', padding_str)
        if nums:
            vals = [float(n) for n in nums]
            # Use the smallest non-zero value as the base unit
            non_zero = [v for v in vals if v > 0]
            if non_zero:
                return max(int(min(non_zero)), 4)
    return 8  # Default


def _first_valid(*values: str) -> str:
    """Return the first non-empty, non-'none' value."""
    for v in values:
        if v and v.strip() and v.strip().lower() != "none":
            return v.strip()
    return values[-1] if values else ""


def _filter_empty(d: Dict[str, str]) -> Dict[str, str]:
    """Remove empty or 'none' values from a dict."""
    return {k: v for k, v in d.items()
            if v and v.strip() and v.strip().lower() != "none"
            and v != "rgba(0, 0, 0, 0)" and v != "transparent"}
