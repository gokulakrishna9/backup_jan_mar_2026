"""React frontend smoke-test validator (headless Chromium via Playwright).

Loads the React app, navigates sample routes, captures console errors,
and verifies that key PrimeReact components render.

Moved from reaw/tools/validate_react_app.py to be a standalone module.
"""

import json
import os
import re
import subprocess
import time
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Tuple

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PwTimeout
except ImportError:
    sync_playwright = None
    PwTimeout = Exception


# ─── Data classes ───────────────────────────────────────────────────────────

@dataclass
class RouteResult:
    path: str
    page_type: str  # entity, filter, query, auth, root
    status: str     # pass, fail, warn
    load_time_ms: int = 0
    console_errors: List[str] = field(default_factory=list)
    console_warnings: List[str] = field(default_factory=list)
    missing_elements: List[str] = field(default_factory=list)
    found_elements: List[str] = field(default_factory=list)
    error_detail: Optional[str] = None


@dataclass
class FrontendReport:
    base_url: str
    total_routes: int = 0
    passed: int = 0
    failed: int = 0
    warned: int = 0
    results: List[RouteResult] = field(default_factory=list)
    global_errors: List[str] = field(default_factory=list)
    video_dir: Optional[str] = None


# ─── Route extraction ──────────────────────────────────────────────────────

def extract_routes_from_definitions(definitions_path: str) -> List[Tuple[str, str]]:
    """Load routes from react_routes.json definition file."""
    routes_file = os.path.join(definitions_path, "react_routes.json")
    if not os.path.isfile(routes_file):
        return []

    with open(routes_file, "r", encoding="utf-8") as f:
        routes_data = json.load(f)

    routes = []
    for r in routes_data:
        path = r.get("path", "")
        page_type = r.get("pageType", "entity")
        if path and path != "/":
            routes.append((path, page_type))

    return routes


# ─── Vite management ───────────────────────────────────────────────────────

def start_vite(app_dir: str) -> Tuple[subprocess.Popen, str]:
    """Start Vite dev server and return (process, url)."""
    env = os.environ.copy()
    proc = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=app_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
        shell=True,
    )

    url = None
    deadline = time.time() + 30
    while time.time() < deadline:
        line = proc.stdout.readline()
        if not line:
            time.sleep(0.1)
            continue
        m = re.search(r"Local:\s+(http://[^\s]+)", line)
        if m:
            url = m.group(1).rstrip("/")
            break

    if not url:
        proc.kill()
        raise RuntimeError("Vite did not start within 30 seconds")

    time.sleep(1)
    return proc, url


def stop_vite(proc: subprocess.Popen):
    """Gracefully stop Vite."""
    try:
        proc.terminate()
        proc.wait(timeout=5)
    except Exception:
        proc.kill()


# ─── Validation logic ──────────────────────────────────────────────────────

IGNORE_PATTERNS = [
    r"Download the React DevTools",
    r"React Router Future Flag Warning",
    r"DevTools",
    r"\[HMR\]",
    r"\[vite\]",
    r"Vite.*hmr",
    r"favicon\.ico",
]

def is_noise(msg: str) -> bool:
    return any(re.search(p, msg, re.IGNORECASE) for p in IGNORE_PATTERNS)


PAGE_EXPECTATIONS = {
    "auth": {
        "selectors": ["[data-pc-name='inputtext'], input.p-inputtext", "[data-pc-name='button'], button.p-button"],
        "labels": ["input field", "button"],
    },
    "entity": {
        "selectors": [
            "[data-pc-name='datatable'], .p-datatable",
            "[data-pc-name='inputtext'], .p-inputtext, .p-fluid",
        ],
        "labels": ["data table", "form/input"],
    },
    "filter": {
        "selectors": [
            "[data-pc-name='datatable'], .p-datatable",
            "[data-pc-name='dropdown'], .p-dropdown",
        ],
        "labels": ["data table", "filter dropdown"],
    },
    "query": {
        "selectors": [
            "[data-pc-name='accordion'], .p-accordion",
            "[data-pc-name='button'], button.p-button",
        ],
        "labels": ["accordion/query section", "execute button"],
    },
}


def validate_route(page, base_url: str, route_path: str, page_type: str, timeout: int) -> RouteResult:
    """Load a single route and validate it."""
    result = RouteResult(path=route_path, page_type=page_type, status="pass")
    console_errors = []
    console_warnings = []

    def on_console(msg):
        text = msg.text
        if is_noise(text):
            return
        if msg.type == "error":
            console_errors.append(text)
        elif msg.type == "warning":
            console_warnings.append(text)

    page.on("console", on_console)

    page_errors = []
    def on_page_error(error):
        page_errors.append(str(error))
    page.on("pageerror", on_page_error)

    url = f"{base_url}{route_path}"
    start = time.time()

    try:
        response = page.goto(url, wait_until="domcontentloaded", timeout=timeout)
        elapsed = int((time.time() - start) * 1000)
        result.load_time_ms = elapsed

        if response and response.status >= 400:
            result.status = "fail"
            result.error_detail = f"HTTP {response.status}"
            return result

        page.wait_for_timeout(1500)

    except PwTimeout:
        result.status = "fail"
        result.error_detail = "Page load timeout"
        return result
    except Exception as e:
        result.status = "fail"
        result.error_detail = str(e)
        return result

    result.console_errors = list(console_errors) + list(page_errors)
    result.console_warnings = list(console_warnings)

    # Check for React error boundary
    body_text = page.inner_text("body").strip()
    if "Something went wrong" in body_text or "Uncaught" in body_text:
        result.status = "fail"
        result.error_detail = "React error boundary triggered"
        return result

    # Check for auth redirect
    if page_type not in ("auth",):
        current_url = page.url
        h2_el = page.query_selector("h2")
        h2_text = h2_el.inner_text().strip() if h2_el else ""
        if "/login" in current_url or h2_text == "Login":
            result.status = "pass"
            result.error_detail = "auth redirect (expected — not logged in)"
            result.found_elements.append("auth redirect")
            page.remove_listener("console", on_console)
            page.remove_listener("pageerror", on_page_error)
            return result

    # Check for blank page
    root_el = page.query_selector("#root")
    if root_el:
        root_html = root_el.inner_html().strip()
        if len(root_html) < 10:
            has_network_errors = any(
                re.search(r"ERR_INSUFFICIENT_RESOURCES|ERR_NETWORK_CHANGED|net::", e)
                for e in console_errors + page_errors
            )
            if has_network_errors:
                result.status = "warn"
                result.error_detail = "Blank page (transient network error — retry)"
            else:
                result.status = "fail"
                result.error_detail = "Blank page — #root is empty"
            result.console_errors = list(console_errors) + list(page_errors)
            page.remove_listener("console", on_console)
            page.remove_listener("pageerror", on_page_error)
            return result

    # Check expected DOM elements
    expectations = PAGE_EXPECTATIONS.get(page_type, {})
    selectors = expectations.get("selectors", [])
    labels = expectations.get("labels", [])

    for selector, label in zip(selectors, labels):
        el = page.query_selector(selector)
        if el:
            result.found_elements.append(label)
        else:
            result.missing_elements.append(label)

    # Determine final status
    if result.console_errors:
        real_errors = [
            e for e in result.console_errors
            if not re.search(r"ERR_INSUFFICIENT_RESOURCES|ERR_NETWORK_CHANGED|net::", e)
        ]
        if real_errors:
            result.status = "fail"
        elif result.missing_elements:
            result.status = "warn"
            result.console_errors = []
    elif result.missing_elements:
        result.status = "warn"

    page.remove_listener("console", on_console)
    page.remove_listener("pageerror", on_page_error)

    return result


def sample_routes(routes: List[Tuple[str, str]], max_per_type: int) -> List[Tuple[str, str]]:
    """Sample up to max_per_type routes from each page type."""
    by_type = {}
    for path, ptype in routes:
        by_type.setdefault(ptype, []).append((path, ptype))

    sampled = []
    for ptype, items in by_type.items():
        sampled.extend(items[:max_per_type])

    return sampled


def run_frontend_validation(
    base_url: str,
    definitions_path: Optional[str],
    app_dir: Optional[str],
    max_routes: int,
    timeout: int,
    headed: bool = True,
    video: bool = True,
    video_dir: Optional[str] = None,
) -> FrontendReport:
    """Run the full frontend validation suite."""
    if sync_playwright is None:
        raise ImportError("playwright is required. Install with: py -m pip install playwright && py -m playwright install chromium")

    report = FrontendReport(base_url=base_url)

    # Extract routes from definition files
    if definitions_path:
        all_routes = extract_routes_from_definitions(definitions_path)
    else:
        all_routes = []

    # Always include auth routes
    auth_routes = [("/login", "auth"), ("/register", "auth")]
    route_paths = {r[0] for r in all_routes}
    for ar in auth_routes:
        if ar[0] not in route_paths:
            all_routes.insert(0, ar)

    report.total_routes = len(all_routes)
    sampled = sample_routes(all_routes, max_routes)

    # Resolve video directory
    actual_video_dir = None
    if video:
        if video_dir:
            actual_video_dir = os.path.abspath(video_dir)
        elif definitions_path:
            parent = os.path.dirname(os.path.abspath(definitions_path))
            ts = time.strftime("%Y%m%d_%H%M%S")
            actual_video_dir = os.path.join(parent, "validation_videos", f"frontend_{ts}")
        else:
            ts = time.strftime("%Y%m%d_%H%M%S")
            actual_video_dir = os.path.join(os.getcwd(), "validation_videos", f"frontend_{ts}")
        os.makedirs(actual_video_dir, exist_ok=True)
        report.video_dir = actual_video_dir

    print(f"\n{'='*60}")
    print(f"  REAW Frontend Validator")
    print(f"  URL: {base_url}")
    print(f"  Total routes found: {len(all_routes)}")
    print(f"  Sampling: {len(sampled)} routes ({max_routes} per type)")
    if actual_video_dir:
        print(f"  Video: {actual_video_dir}")
    print(f"{'='*60}\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not headed)
        ctx_opts = {
            "viewport": {"width": 1280, "height": 720},
            "ignore_https_errors": True,
        }
        if actual_video_dir:
            ctx_opts["record_video_dir"] = actual_video_dir
            ctx_opts["record_video_size"] = {"width": 1280, "height": 720}
        context = browser.new_context(**ctx_opts)
        page = context.new_page()

        # Warm up
        try:
            page.goto(base_url, wait_until="domcontentloaded", timeout=timeout)
            page.wait_for_timeout(2000)
        except Exception as e:
            report.global_errors.append(f"Failed to load root: {e}")
            browser.close()
            return report

        for route_path, page_type in sampled:
            result = validate_route(page, base_url, route_path, page_type, timeout)
            report.results.append(result)

            if result.status == "pass":
                report.passed += 1
            elif result.status == "fail":
                report.failed += 1
            else:
                report.warned += 1

            icon = {"pass": "✅", "fail": "❌", "warn": "⚠️"}.get(result.status, "?")
            print(f"  {icon} [{result.page_type:7s}] {result.path}")
            if result.error_detail:
                print(f"           └─ {result.error_detail}")
            for err in result.console_errors[:3]:
                print(f"           └─ console.error: {err[:120]}")
            if result.missing_elements:
                print(f"           └─ missing: {', '.join(result.missing_elements)}")

        context.close()
        browser.close()

    if report.video_dir:
        print(f"\n  🎬 Video saved to: {report.video_dir}")

    return report


def print_frontend_summary(report: FrontendReport):
    """Print a summary of frontend validation results."""
    total = report.passed + report.failed + report.warned
    print(f"\n{'='*60}")
    print(f"  FRONTEND RESULTS: {report.passed} passed, {report.failed} failed, {report.warned} warnings")
    print(f"  Total routes in app: {report.total_routes}")
    print(f"  Routes tested: {total}")

    if report.global_errors:
        print(f"\n  Global errors:")
        for e in report.global_errors:
            print(f"    ❌ {e}")

    if report.failed > 0:
        print(f"\n  Failed routes:")
        for r in report.results:
            if r.status == "fail":
                detail = r.error_detail or "; ".join(r.console_errors[:2])
                print(f"    ❌ {r.path} — {detail[:100]}")

    if report.warned > 0:
        print(f"\n  Warnings:")
        for r in report.results:
            if r.status == "warn":
                print(f"    ⚠️  {r.path} — missing: {', '.join(r.missing_elements)}")

    print(f"{'='*60}\n")

    if report.failed == 0 and not report.global_errors:
        print("  🎉 All sampled routes passed validation.\n")
    else:
        print("  ⚡ Some routes need attention.\n")
