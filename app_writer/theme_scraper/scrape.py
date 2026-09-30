"""CLI entry point for the theme scraper.

Usage:
    py theme_scraper/scrape.py --url https://example.com --output <application_definitions_path>
    py theme_scraper/scrape.py --url https://example.com --output ./output --headed
    py theme_scraper/scrape.py --url https://example.com  (prints JSON to stdout)
"""

import argparse
import json
import os
import sys

# Ensure the workspace root is on the path so theme_scraper package resolves
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from theme_scraper.scraper import scrape_site
from theme_scraper.token_extractor import extract_tokens
from theme_scraper.theme_mapper import map_to_theme_definition


def main():
    parser = argparse.ArgumentParser(
        description="Theme Scraper — extract design tokens from a website and produce react_theme.json"
    )
    parser.add_argument("--url", required=True, help="Target website URL to scrape")
    parser.add_argument("--output", default=None,
                        help="Path to application_definitions/ folder (writes react_theme.json there). "
                             "If omitted, prints JSON to stdout.")
    parser.add_argument("--headed", action="store_true", help="Show browser window during scraping")
    parser.add_argument("--timeout", type=int, default=30000, help="Page load timeout in ms (default: 30000)")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output (default when writing to file)")
    parser.add_argument("--verbose", action="store_true", help="Print extraction details")

    args = parser.parse_args()

    url = args.url
    if not url.startswith("http"):
        url = "https://" + url

    # ── Phase 1: Scrape ──
    print(f"\n{'='*60}")
    print(f"  Theme Scraper")
    print(f"  Target: {url}")
    print(f"{'='*60}\n")

    print("  [1/3] Scraping website...")
    scraped = scrape_site(url, timeout=args.timeout, headed=args.headed)
    print(f"        Done in {scraped.scrape_time_ms}ms")
    print(f"        CSS variables found: {len(scraped.css_variables)}")
    print(f"        Elements styled: {len(scraped.element_styles)}")
    print(f"        Stylesheets downloaded: {len(scraped.stylesheet_contents)}")
    print(f"        Font families: {len(scraped.fonts_used)}")

    if args.verbose:
        print(f"\n        Elements: {', '.join(scraped.element_styles.keys())}")
        if scraped.css_variables:
            print(f"        Sample variables: {list(scraped.css_variables.items())[:5]}")

    # ── Phase 2: Extract tokens ──
    print("\n  [2/3] Extracting design tokens...")
    tokens = extract_tokens(scraped)
    palette = tokens.get("colorPalette", {})
    print(f"        Palette: {len(palette)} colors")
    print(f"        Font: {tokens.get('typography', {}).get('fontFamily', 'unknown')}")

    if args.verbose:
        for name, value in palette.items():
            print(f"          {name}: {value}")

    # ── Phase 3: Map to theme definition ──
    print("\n  [3/3] Mapping to react_theme.json schema...")
    theme_def = map_to_theme_definition(tokens)

    # ── Output ──
    if args.output:
        output_dir = os.path.abspath(args.output)
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "react_theme.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(theme_def, f, indent=2, ensure_ascii=False)
        print(f"\n  ✅ Written to: {output_path}")
    else:
        indent = 2 if args.pretty else None
        print(json.dumps(theme_def, indent=indent, ensure_ascii=False))

    print(f"\n{'='*60}")
    print(f"  Scrape complete. Source: {url}")
    if args.output:
        print(f"  Output: {os.path.join(args.output, 'react_theme.json')}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
