"""Browser-based style scraper using Playwright.

Visits a target URL, extracts computed styles from key DOM elements,
downloads linked stylesheets, and extracts CSS custom properties.
"""

import re
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

try:
    from playwright.sync_api import sync_playwright, Page
except ImportError:
    sync_playwright = None
    Page = None

try:
    import requests
except ImportError:
    requests = None


@dataclass
class ScrapedStyles:
    """Raw scraped data from a target website."""
    url: str
    css_variables: Dict[str, str] = field(default_factory=dict)
    element_styles: Dict[str, Dict[str, str]] = field(default_factory=dict)
    stylesheet_contents: List[str] = field(default_factory=list)
    fonts_used: List[str] = field(default_factory=list)
    scrape_time_ms: int = 0


# Elements to sample computed styles from, keyed by a semantic role name.
# Each entry is (css_selector, list_of_css_properties_to_read).
_ELEMENT_TARGETS: List[Tuple[str, str, List[str]]] = [
    ("body", "body", [
        "backgroundColor", "color", "fontFamily", "fontSize", "lineHeight",
    ]),
    ("heading_h1", "h1", [
        "fontFamily", "fontSize", "fontWeight", "color", "lineHeight",
    ]),
    ("heading_h2", "h2", [
        "fontFamily", "fontSize", "fontWeight", "color",
    ]),
    ("button_primary", "button, [role='button'], .btn, .p-button, a.btn-primary, button[type='submit']", [
        "backgroundColor", "color", "borderRadius", "borderColor", "borderWidth",
        "fontFamily", "fontSize", "fontWeight", "padding", "boxShadow",
    ]),
    ("input", "input[type='text'], input[type='email'], input[type='password'], .p-inputtext, textarea", [
        "backgroundColor", "color", "borderRadius", "borderColor", "borderWidth",
        "fontFamily", "fontSize", "padding",
    ]),
    ("nav", "nav, [role='navigation'], .sidebar, .navbar, header nav", [
        "backgroundColor", "color", "fontFamily", "fontSize",
    ]),
    ("card", ".card, .p-card, [class*='card'], article", [
        "backgroundColor", "borderRadius", "boxShadow", "padding",
    ]),
    ("table_header", "th, .p-datatable-thead th, thead th", [
        "backgroundColor", "color", "fontWeight", "fontSize",
    ]),
    ("table_row", "td, .p-datatable-tbody td, tbody td", [
        "backgroundColor", "color", "fontSize", "padding",
    ]),
    ("link", "a, a:not([role='button'])", [
        "color", "fontWeight", "textDecoration",
    ]),
    ("sidebar", ".sidebar, aside, [class*='sidebar'], [class*='sidenav']", [
        "backgroundColor", "color", "width",
    ]),
]


def _extract_computed_styles(page: Page) -> Dict[str, Dict[str, str]]:
    """Use page.evaluate to read getComputedStyle for target elements."""
    # Build a JS script that queries each selector and reads properties
    js_targets = []
    for role, selector, props in _ELEMENT_TARGETS:
        props_js = ", ".join(f'"{p}"' for p in props)
        js_targets.append(f'{{ role: "{role}", selector: `{selector}`, props: [{props_js}] }}')

    js_script = """
    () => {
        const targets = [%s];
        const results = {};
        for (const t of targets) {
            const el = document.querySelector(t.selector);
            if (!el) continue;
            const cs = window.getComputedStyle(el);
            const styles = {};
            for (const p of t.props) {
                const val = cs.getPropertyValue(p) || cs[p];
                if (val) styles[p] = val;
            }
            if (Object.keys(styles).length > 0) results[t.role] = styles;
        }
        return results;
    }
    """ % ",\n            ".join(js_targets)

    return page.evaluate(js_script)


def _extract_css_variables(page: Page) -> Dict[str, str]:
    """Extract all CSS custom properties defined on :root or html."""
    js = """
    () => {
        const vars = {};
        for (const sheet of document.styleSheets) {
            try {
                for (const rule of sheet.cssRules) {
                    if (rule.selectorText === ':root' || rule.selectorText === 'html') {
                        for (let i = 0; i < rule.style.length; i++) {
                            const name = rule.style[i];
                            if (name.startsWith('--')) {
                                vars[name] = rule.style.getPropertyValue(name).trim();
                            }
                        }
                    }
                }
            } catch (e) {
                // Cross-origin stylesheet, skip
            }
        }
        return vars;
    }
    """
    return page.evaluate(js)


def _extract_fonts(page: Page) -> List[str]:
    """Extract unique font families used across the page."""
    js = """
    () => {
        const fonts = new Set();
        const els = document.querySelectorAll('body, h1, h2, h3, p, a, button, input, th, td, nav, li');
        for (const el of els) {
            const ff = window.getComputedStyle(el).fontFamily;
            if (ff) fonts.add(ff);
        }
        return [...fonts];
    }
    """
    return page.evaluate(js)


def _download_stylesheets(page: Page, base_url: str) -> List[str]:
    """Download external stylesheet contents."""
    # Get all <link rel="stylesheet"> hrefs
    hrefs = page.evaluate("""
    () => {
        const links = document.querySelectorAll('link[rel="stylesheet"]');
        return [...links].map(l => l.href).filter(h => h);
    }
    """)

    contents = []
    for href in hrefs:
        try:
            resp = requests.get(href, timeout=10)
            if resp.status_code == 200 and len(resp.text) < 500_000:
                contents.append(resp.text)
        except Exception:
            pass

    # Also grab inline <style> blocks
    inline = page.evaluate("""
    () => {
        const styles = document.querySelectorAll('style');
        return [...styles].map(s => s.textContent).filter(t => t.trim());
    }
    """)
    contents.extend(inline)

    return contents


def scrape_site(url: str, timeout: int = 30000, headed: bool = False) -> ScrapedStyles:
    """Scrape design tokens from a target website.

    Args:
        url: Target URL to scrape.
        timeout: Page load timeout in ms.
        headed: Show browser window.

    Returns:
        ScrapedStyles with all extracted raw data.
    """
    if sync_playwright is None:
        raise ImportError("playwright is required: py -m pip install playwright && py -m playwright install chromium")
    if requests is None:
        raise ImportError("requests is required: py -m pip install requests")

    result = ScrapedStyles(url=url)
    start = time.time()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            ignore_https_errors=True,
        )
        page = context.new_page()

        try:
            page.goto(url, wait_until="networkidle", timeout=timeout)
            page.wait_for_timeout(3000)  # Let JS-rendered styles settle
        except Exception as e:
            print(f"  Warning: Page load issue: {e}")

        # 1. CSS custom properties
        result.css_variables = _extract_css_variables(page)

        # 2. Computed styles from key elements
        result.element_styles = _extract_computed_styles(page)

        # 3. Fonts
        result.fonts_used = _extract_fonts(page)

        # 4. Stylesheets
        result.stylesheet_contents = _download_stylesheets(page, url)

        browser.close()

    result.scrape_time_ms = int((time.time() - start) * 1000)
    return result
