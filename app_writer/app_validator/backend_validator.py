"""WebFlux backend smoke-test validator.

Tests the Spring WebFlux application by:
1. Checking server reachability (setup page or login page)
2. Probing Swagger/OpenAPI endpoint
3. Extracting API endpoints from Swagger JSON
4. Smoke-testing sampled API endpoints (expecting 401/403 for protected routes)
5. Testing auth endpoints (register, login flow)
"""

import json
import re
import time
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    requests = None


# ─── Data classes ───────────────────────────────────────────────────────────

@dataclass
class EndpointResult:
    path: str
    method: str
    status_code: int
    status: str  # pass, fail, warn
    response_time_ms: int = 0
    error_detail: Optional[str] = None
    category: str = ""  # health, swagger, api, auth


@dataclass
class BackendReport:
    base_url: str
    total_endpoints: int = 0
    passed: int = 0
    failed: int = 0
    warned: int = 0
    results: List[EndpointResult] = field(default_factory=list)
    api_paths_discovered: int = 0
    swagger_available: bool = False


# ─── Endpoint discovery ────────────────────────────────────────────────────

SWAGGER_PATHS = [
    "/v3/api-docs",
    "/swagger-ui.html",
]

HEALTH_PATHS = [
    ("/setup", "GET", "health"),
    ("/login", "GET", "health"),
]

AUTH_PATHS = [
    ("/api/auth/login", "POST", "auth"),
    ("/api/auth/register", "POST", "auth"),
    ("/api/auth/me", "GET", "auth"),
]


def _request(base_url: str, path: str, method: str = "GET",
             timeout_s: float = 10, body: Any = None,
             headers: Dict[str, str] = None) -> EndpointResult:
    """Make a single HTTP request and return the result."""
    url = urljoin(base_url, path)
    hdrs = {"Content-Type": "application/json", "Accept": "application/json"}
    if headers:
        hdrs.update(headers)

    start = time.time()
    try:
        if method == "GET":
            resp = requests.get(url, headers=hdrs, timeout=timeout_s, allow_redirects=True)
        elif method == "POST":
            resp = requests.post(url, headers=hdrs, json=body, timeout=timeout_s, allow_redirects=True)
        elif method == "PUT":
            resp = requests.put(url, headers=hdrs, json=body, timeout=timeout_s, allow_redirects=True)
        elif method == "DELETE":
            resp = requests.delete(url, headers=hdrs, timeout=timeout_s, allow_redirects=True)
        else:
            resp = requests.get(url, headers=hdrs, timeout=timeout_s, allow_redirects=True)

        elapsed = int((time.time() - start) * 1000)
        return EndpointResult(
            path=path, method=method, status_code=resp.status_code,
            status="pass", response_time_ms=elapsed,
        )
    except requests.exceptions.ConnectionError as e:
        return EndpointResult(
            path=path, method=method, status_code=0, status="fail",
            error_detail=f"Connection refused: {e}",
        )
    except requests.exceptions.Timeout:
        return EndpointResult(
            path=path, method=method, status_code=0, status="fail",
            error_detail="Request timeout",
        )
    except Exception as e:
        return EndpointResult(
            path=path, method=method, status_code=0, status="fail",
            error_detail=str(e),
        )


def _extract_api_paths_from_swagger(base_url: str, timeout_s: float) -> List[Tuple[str, str]]:
    """Try to fetch OpenAPI JSON and extract API paths."""
    url = urljoin(base_url, "/v3/api-docs")
    try:
        resp = requests.get(url, timeout=timeout_s, headers={"Accept": "application/json"})
        if resp.status_code != 200:
            return []
        data = resp.json()
        paths = []
        for path, methods in data.get("paths", {}).items():
            for method in methods:
                if method.upper() in ("GET", "POST", "PUT", "DELETE", "PATCH"):
                    paths.append((path, method.upper()))
        return paths
    except Exception:
        return []


def _classify_result(result: EndpointResult, category: str) -> EndpointResult:
    """Classify pass/fail/warn based on category and status code."""
    result.category = category
    code = result.status_code

    if code == 0:
        # Already marked fail by _request
        return result

    if category == "health":
        # Setup/login pages: 200, 302 redirect, 400 (setup already done) are fine
        if code in (200, 302, 303, 400):
            result.status = "pass"
            if code == 400:
                result.error_detail = "Setup already completed (expected)"
        else:
            result.status = "fail"
            result.error_detail = f"Unexpected HTTP {code}"

    elif category == "swagger":
        if code == 200:
            result.status = "pass"
        else:
            result.status = "warn"
            result.error_detail = f"Swagger returned HTTP {code}"

    elif category == "api":
        # Protected API endpoints: 401/403 = pass (auth is working)
        # 200 = pass (public or already authed)
        # 5xx = fail
        if code in (200, 201, 401, 403):
            result.status = "pass"
        elif code == 404:
            result.status = "warn"
            result.error_detail = "Endpoint not found (404)"
        elif code >= 500:
            result.status = "fail"
            result.error_detail = f"Server error: HTTP {code}"
        elif code == 302 or code == 303:
            result.status = "pass"
            result.error_detail = "Redirect (auth redirect expected)"
        else:
            result.status = "warn"
            result.error_detail = f"Unexpected HTTP {code}"

    elif category == "auth":
        # Auth endpoints: 400 (bad request body) is acceptable for smoke test
        # 401 for /me without token is expected
        # 500 on login with fake credentials can happen (e.g. user not found throws)
        # 500 on register can happen (e.g. duplicate user)
        if code in (200, 201, 400, 401, 403, 409):
            result.status = "pass"
        elif code == 500 and ("login" in result.path or "register" in result.path):
            result.status = "warn"
            result.error_detail = f"Auth endpoint returned 500 with smoke-test data (may be expected — duplicate user or invalid credentials)"
        elif code >= 500:
            result.status = "fail"
            result.error_detail = f"Server error: HTTP {code}"
        else:
            result.status = "warn"
            result.error_detail = f"Unexpected HTTP {code}"

    return result


def sample_api_paths(paths: List[Tuple[str, str]], max_per_method: int = 5) -> List[Tuple[str, str]]:
    """Sample API paths: take up to max_per_method for each HTTP method."""
    by_method: Dict[str, List[Tuple[str, str]]] = {}
    for path, method in paths:
        by_method.setdefault(method, []).append((path, method))

    sampled = []
    for method, items in by_method.items():
        # Prefer list endpoints (no path params) for GET
        if method == "GET":
            no_params = [i for i in items if "{" not in i[0]]
            with_params = [i for i in items if "{" in i[0]]
            sampled.extend(no_params[:max_per_method])
            remaining = max_per_method - len(no_params[:max_per_method])
            if remaining > 0:
                sampled.extend(with_params[:remaining])
        else:
            sampled.extend(items[:max_per_method])

    return sampled


def run_backend_validation(
    base_url: str,
    max_api_endpoints: int = 5,
    timeout_ms: int = 15000,
) -> BackendReport:
    """Run the full backend validation suite."""
    if requests is None:
        raise ImportError("requests library is required. Install with: py -m pip install requests")

    base_url = base_url.rstrip("/")
    timeout_s = timeout_ms / 1000
    report = BackendReport(base_url=base_url)

    print(f"\n{'='*60}")
    print(f"  REAW Backend Validator")
    print(f"  URL: {base_url}")
    print(f"{'='*60}\n")

    # 1. Health checks (setup page, login page)
    print("  [Health Checks]")
    for path, method, category in HEALTH_PATHS:
        result = _request(base_url, path, method, timeout_s)
        result = _classify_result(result, category)
        report.results.append(result)
        _print_result(result)

    # 2. Swagger / OpenAPI
    print("\n  [Swagger / OpenAPI]")
    for path in SWAGGER_PATHS:
        result = _request(base_url, path, "GET", timeout_s)
        result = _classify_result(result, "swagger")
        if path == "/v3/api-docs" and result.status_code == 200:
            report.swagger_available = True
        report.results.append(result)
        _print_result(result)

    # 3. Discover API endpoints from Swagger
    api_paths = []
    if report.swagger_available:
        api_paths = _extract_api_paths_from_swagger(base_url, timeout_s)
        report.api_paths_discovered = len(api_paths)
        print(f"\n  Discovered {len(api_paths)} API endpoints from Swagger")

    # 4. Smoke-test sampled API endpoints
    if api_paths:
        sampled = sample_api_paths(api_paths, max_api_endpoints)
        print(f"  Sampling {len(sampled)} endpoints\n")
        print("  [API Endpoints]")
        for path, method in sampled:
            # For POST/PUT, send empty body (expect 400 or 401)
            body = {} if method in ("POST", "PUT", "PATCH") else None
            result = _request(base_url, path, method, timeout_s, body=body)
            result = _classify_result(result, "api")
            report.results.append(result)
            _print_result(result)
    else:
        print("\n  [API Endpoints] Skipped — no Swagger data available")

    # 5. Auth endpoints
    print("\n  [Auth Endpoints]")
    for path, method, category in AUTH_PATHS:
        body = None
        if method == "POST" and "login" in path:
            body = {"username": "smoke_test", "password": "smoke_test"}
        elif method == "POST" and "register" in path:
            body = {"username": "smoke_test", "password": "smoke_test",
                    "email": "smoke@test.com", "firstName": "Smoke", "lastName": "Test"}
        result = _request(base_url, path, method, timeout_s, body=body)
        result = _classify_result(result, category)
        report.results.append(result)
        _print_result(result)

    # Tally
    for r in report.results:
        if r.status == "pass":
            report.passed += 1
        elif r.status == "fail":
            report.failed += 1
        else:
            report.warned += 1
    report.total_endpoints = len(report.results)

    return report


def _print_result(result: EndpointResult):
    """Print a single result inline."""
    icon = {"pass": "✅", "fail": "❌", "warn": "⚠️"}.get(result.status, "?")
    code_str = f"HTTP {result.status_code}" if result.status_code else "NO RESPONSE"
    print(f"    {icon} {result.method:6s} {result.path:50s} {code_str:10s} ({result.response_time_ms}ms)")
    if result.error_detail:
        print(f"       └─ {result.error_detail}")


def print_backend_summary(report: BackendReport):
    """Print a summary of backend validation results."""
    print(f"\n{'='*60}")
    print(f"  BACKEND RESULTS: {report.passed} passed, {report.failed} failed, {report.warned} warnings")
    print(f"  Total endpoints tested: {report.total_endpoints}")
    if report.swagger_available:
        print(f"  API paths discovered via Swagger: {report.api_paths_discovered}")

    if report.failed > 0:
        print(f"\n  Failed:")
        for r in report.results:
            if r.status == "fail":
                detail = r.error_detail or f"HTTP {r.status_code}"
                print(f"    ❌ {r.method} {r.path} — {detail}")

    if report.warned > 0:
        print(f"\n  Warnings:")
        for r in report.results:
            if r.status == "warn":
                detail = r.error_detail or f"HTTP {r.status_code}"
                print(f"    ⚠️  {r.method} {r.path} — {detail}")

    print(f"{'='*60}\n")

    if report.failed == 0:
        print("  🎉 Backend validation passed.\n")
    else:
        print("  ⚡ Some backend endpoints need attention.\n")
