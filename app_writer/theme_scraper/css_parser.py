"""CSS parser — extracts custom properties and design tokens from raw CSS text.

Uses tinycss2 if available, falls back to regex-based extraction.
"""

import re
from typing import Dict, List, Tuple


def _try_tinycss2(css_text: str) -> Dict[str, str]:
    """Extract CSS custom properties using tinycss2."""
    try:
        import tinycss2
    except ImportError:
        return {}

    variables = {}
    rules = tinycss2.parse_stylesheet(css_text, skip_whitespace=True)
    for rule in rules:
        if hasattr(rule, "prelude") and hasattr(rule, "content"):
            # Check if selector is :root or html
            selector = tinycss2.serialize(rule.prelude).strip()
            if selector in (":root", "html", ":root, html"):
                declarations = tinycss2.parse_declaration_list(rule.content)
                for decl in declarations:
                    if hasattr(decl, "name") and decl.name.startswith("--"):
                        value = tinycss2.serialize(decl.value).strip()
                        variables[decl.name] = value
    return variables


def _regex_extract_variables(css_text: str) -> Dict[str, str]:
    """Fallback regex extraction of CSS custom properties."""
    variables = {}
    # Match --variable-name: value; inside :root or html blocks
    root_blocks = re.findall(
        r'(?::root|html)\s*\{([^}]+)\}', css_text, re.DOTALL
    )
    for block in root_blocks:
        for match in re.finditer(r'(--[\w-]+)\s*:\s*([^;]+);', block):
            variables[match.group(1).strip()] = match.group(2).strip()
    return variables


def extract_variables_from_css(css_texts: List[str]) -> Dict[str, str]:
    """Extract all CSS custom properties from a list of CSS text contents.

    Tries tinycss2 first, falls back to regex.

    Args:
        css_texts: List of raw CSS strings (from stylesheets and inline styles).

    Returns:
        Dict of variable name → value.
    """
    all_vars: Dict[str, str] = {}
    for css in css_texts:
        # Try tinycss2 first
        parsed = _try_tinycss2(css)
        if parsed:
            all_vars.update(parsed)
        else:
            all_vars.update(_regex_extract_variables(css))
    return all_vars


def extract_color_values(css_texts: List[str]) -> List[str]:
    """Extract all color values (hex, rgb, rgba, hsl, hsla) from CSS text."""
    colors = set()
    for css in css_texts:
        # Hex colors
        for m in re.finditer(r'#(?:[0-9a-fA-F]{3,8})\b', css):
            colors.add(m.group(0))
        # rgb/rgba/hsl/hsla
        for m in re.finditer(r'(?:rgba?|hsla?)\([^)]+\)', css):
            colors.add(m.group(0))
    return sorted(colors)
