"""Unified CLI for validating generated applications.

Usage:
    py app_validator/validate.py frontend --url http://localhost:5173 --app-dir <react_app_path>
    py app_validator/validate.py backend  --url http://localhost:8081
    py app_validator/validate.py simulate --url http://localhost:5173 --definitions <app_definitions_path>
    py app_validator/validate.py api-coverage --definitions <app_definitions_path>
    py app_validator/validate.py all      --backend-url http://localhost:8081 --frontend-url http://localhost:5173 --app-dir <react_app_path>

Options:
    --headed        Show browser window (frontend only)
    --max-routes N  Max routes per page type (frontend, default: 5)
    --max-endpoints N  Max API endpoints per HTTP method (backend, default: 5)
    --timeout N     Timeout in ms (default: 15000)
    --json          Output results as JSON
"""

import argparse
import json
import os
import sys
from dataclasses import asdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend_validator import run_backend_validation, print_backend_summary
from frontend_validator import (
    run_frontend_validation, print_frontend_summary,
    start_vite, stop_vite,
)
from interaction_validator import (
    run_interaction_validation, print_interaction_summary,
)
from api_coverage_validator import (
    run_api_coverage_validation, print_api_coverage_summary,
)


def cmd_frontend(args):
    """Run frontend validation."""
    vite_proc = None
    base_url = args.url
    app_dir = args.app_dir

    try:
        if app_dir and not base_url:
            app_dir = os.path.abspath(app_dir)
            print(f"Starting Vite dev server in {app_dir}...")
            vite_proc, base_url = start_vite(app_dir)
            print(f"Vite running at {base_url}")

        report = run_frontend_validation(
            base_url,
            getattr(args, 'definitions', None),
            app_dir,
            args.max_routes,
            args.timeout,
            headed=not getattr(args, 'headless', False),
            video=not args.no_video,
            video_dir=args.video_dir,
        )

        if args.json:
            print(json.dumps(asdict(report), indent=2))
        else:
            print_frontend_summary(report)

        return 1 if report.failed > 0 else 0
    finally:
        if vite_proc:
            print("Stopping Vite...")
            stop_vite(vite_proc)


def cmd_backend(args):
    """Run backend validation."""
    report = run_backend_validation(args.url, args.max_endpoints, args.timeout)

    if args.json:
        print(json.dumps(asdict(report), indent=2))
    else:
        print_backend_summary(report)

    return 1 if report.failed > 0 else 0


def cmd_all(args):
    """Run both backend and frontend validation."""
    exit_code = 0
    vite_proc = None
    frontend_url = args.frontend_url
    app_dir = args.app_dir

    # Backend
    print("\n" + "=" * 60)
    print("  PHASE 1: Backend Validation")
    print("=" * 60)
    backend_report = run_backend_validation(args.backend_url, args.max_endpoints, args.timeout)
    if not args.json:
        print_backend_summary(backend_report)
    if backend_report.failed > 0:
        exit_code = 1

    # Frontend
    try:
        if app_dir and not frontend_url:
            app_dir = os.path.abspath(app_dir)
            print(f"Starting Vite dev server in {app_dir}...")
            vite_proc, frontend_url = start_vite(app_dir)
            print(f"Vite running at {frontend_url}")

        print("\n" + "=" * 60)
        print("  PHASE 2: Frontend Validation")
        print("=" * 60)
        frontend_report = run_frontend_validation(
            frontend_url,
            getattr(args, 'definitions', None),
            app_dir,
            args.max_routes,
            args.timeout,
            headed=not getattr(args, 'headless', False),
            video=not getattr(args, 'no_video', False),
            video_dir=getattr(args, 'video_dir', None),
        )
        if not args.json:
            print_frontend_summary(frontend_report)
        if frontend_report.failed > 0:
            exit_code = 1

    finally:
        if vite_proc:
            print("Stopping Vite...")
            stop_vite(vite_proc)

    # Combined summary
    if args.json:
        combined = {
            "backend": asdict(backend_report),
            "frontend": asdict(frontend_report),
        }
        print(json.dumps(combined, indent=2))
    else:
        print("\n" + "=" * 60)
        print("  COMBINED RESULTS")
        print("=" * 60)
        b = backend_report
        f = frontend_report
        print(f"  Backend:  {b.passed} passed, {b.failed} failed, {b.warned} warnings")
        print(f"  Frontend: {f.passed} passed, {f.failed} failed, {f.warned} warnings")
        total_pass = b.passed + f.passed
        total_fail = b.failed + f.failed
        total_warn = b.warned + f.warned
        print(f"  Total:    {total_pass} passed, {total_fail} failed, {total_warn} warnings")
        print("=" * 60)
        if total_fail == 0:
            print("\n  🎉 Full stack validation passed.\n")
        else:
            print("\n  ⚡ Some checks need attention.\n")

    return exit_code


def cmd_simulate(args):
    """Run interactive E2E simulation driven by React definitions."""
    vite_proc = None
    base_url = args.url
    app_dir = args.app_dir

    try:
        if app_dir and not base_url:
            app_dir = os.path.abspath(app_dir)
            print(f"Starting Vite dev server in {app_dir}...")
            vite_proc, base_url = start_vite(app_dir)
            print(f"Vite running at {base_url}")

        report = run_interaction_validation(
            base_url=base_url,
            app_def_path=os.path.abspath(args.definitions),
            max_entities=args.max_entities,
            timeout=args.timeout,
            headed=args.headed,
            video=not args.no_video,
            video_dir=args.video_dir,
        )

        if args.json:
            print(json.dumps(asdict(report), indent=2))
        else:
            print_interaction_summary(report)

        return 1 if report.failed > 0 else 0
    finally:
        if vite_proc:
            print("Stopping Vite...")
            stop_vite(vite_proc)


def cmd_api_coverage(args):
    """Run API coverage validation (definition-only, optionally with live backend tests)."""
    definitions_path = os.path.abspath(args.definitions)
    report = run_api_coverage_validation(
        definitions_path,
        backend_url=getattr(args, 'backend_url', None),
        username=getattr(args, 'username', None),
        password=getattr(args, 'password', None),
        max_live_entities=getattr(args, 'max_entities', 5),
        timeout_ms=getattr(args, 'timeout', 15000),
    )

    if args.json:
        from dataclasses import asdict as _asdict
        print(json.dumps(_asdict(report), indent=2))
    else:
        print_api_coverage_summary(report)

    return 1 if report.errors > 0 else 0


def main():
    parser = argparse.ArgumentParser(
        description="App Validator — smoke-test generated WebFlux + React applications"
    )
    subparsers = parser.add_subparsers(dest="command", help="Validation target")

    # Frontend subcommand
    fe = subparsers.add_parser("frontend", help="Validate React frontend (page load checks)")
    fe.add_argument("--url", default=None, help="Base URL of running React dev server")
    fe.add_argument("--definitions", default=None, help="Path to application_definitions/ folder (for route discovery)")
    fe.add_argument("--app-dir", default=None, help="Path to react_app/ folder (auto-starts Vite)")
    fe.add_argument("--max-routes", type=int, default=5, help="Max routes per page type")
    fe.add_argument("--timeout", type=int, default=15000, help="Timeout in ms")
    fe.add_argument("--headed", action="store_true", default=True, help="Show browser window (default: on)")
    fe.add_argument("--headless", action="store_true", help="Run headless (no browser window)")
    fe.add_argument("--no-video", action="store_true", help="Disable video recording")
    fe.add_argument("--video-dir", default=None, help="Custom video output directory")
    fe.add_argument("--json", action="store_true", help="JSON output")

    # Backend subcommand
    be = subparsers.add_parser("backend", help="Validate WebFlux backend (HTTP smoke tests)")
    be.add_argument("--url", required=True, help="Base URL of running WebFlux app")
    be.add_argument("--max-endpoints", type=int, default=5, help="Max API endpoints per HTTP method")
    be.add_argument("--timeout", type=int, default=15000, help="Timeout in ms")
    be.add_argument("--json", action="store_true", help="JSON output")

    # Simulate subcommand (interactive E2E)
    sim = subparsers.add_parser("simulate", help="Interactive E2E simulation (definition-driven)")
    sim.add_argument("--url", default=None, help="Base URL of running React dev server")
    sim.add_argument("--app-dir", default=None, help="Path to react_app/ folder (auto-starts Vite)")
    sim.add_argument("--definitions", required=True, help="Path to application_definitions/ folder")
    sim.add_argument("--max-entities", type=int, default=3, help="Max entities to test per page type")
    sim.add_argument("--timeout", type=int, default=15000, help="Timeout in ms")
    sim.add_argument("--headed", action="store_true", help="Show browser window (recommended)")
    sim.add_argument("--no-video", action="store_true", help="Disable video recording")
    sim.add_argument("--video-dir", default=None, help="Custom video output directory")
    sim.add_argument("--json", action="store_true", help="JSON output")

    # All subcommand
    al = subparsers.add_parser("all", help="Validate both backend and frontend")
    al.add_argument("--backend-url", required=True, help="Base URL of WebFlux app")
    al.add_argument("--frontend-url", default=None, help="Base URL of React dev server")
    al.add_argument("--definitions", default=None, help="Path to application_definitions/ folder (for route discovery)")
    al.add_argument("--app-dir", default=None, help="Path to react_app/ folder (auto-starts Vite)")
    al.add_argument("--max-routes", type=int, default=5, help="Max routes per page type")
    al.add_argument("--max-endpoints", type=int, default=5, help="Max API endpoints per HTTP method")
    al.add_argument("--timeout", type=int, default=15000, help="Timeout in ms")
    al.add_argument("--headed", action="store_true", default=True, help="Show browser window (default: on)")
    al.add_argument("--headless", action="store_true", help="Run headless (no browser window)")
    al.add_argument("--no-video", action="store_true", help="Disable video recording")
    al.add_argument("--video-dir", default=None, help="Custom video output directory")
    al.add_argument("--json", action="store_true", help="JSON output")

    # API Coverage subcommand (definition-only + optional live tests)
    ac = subparsers.add_parser("api-coverage", help="API coverage check (definitions + optional live CRUD + DB verification)")
    ac.add_argument("--definitions", required=True, help="Path to application_definitions/ folder")
    ac.add_argument("--backend-url", default=None, help="Base URL of running WebFlux app (enables live CRUD tests)")
    ac.add_argument("--username", default=None, help="Login username for live tests")
    ac.add_argument("--password", default=None, help="Login password for live tests")
    ac.add_argument("--max-entities", type=int, default=5, help="Max entities to test in live mode (default: 5)")
    ac.add_argument("--timeout", type=int, default=15000, help="Timeout in ms")
    ac.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "frontend":
        if not args.url and not args.app_dir:
            print("Error: Provide either --url or --app-dir", file=sys.stderr)
            sys.exit(1)
        sys.exit(cmd_frontend(args))

    elif args.command == "backend":
        sys.exit(cmd_backend(args))

    elif args.command == "simulate":
        if not args.url and not args.app_dir:
            print("Error: Provide either --url or --app-dir", file=sys.stderr)
            sys.exit(1)
        sys.exit(cmd_simulate(args))

    elif args.command == "all":
        if not args.frontend_url and not args.app_dir:
            print("Error: Provide either --frontend-url or --app-dir", file=sys.stderr)
            sys.exit(1)
        sys.exit(cmd_all(args))

    elif args.command == "api-coverage":
        sys.exit(cmd_api_coverage(args))


if __name__ == "__main__":
    main()
