#!/usr/bin/env python3
"""
Dependency Security Scanner — checks npm and Maven dependencies against OSV.dev
for known vulnerabilities, malware, and supply chain compromises.

Usage:
    python dep_scanner/scan.py --app <app_name>
    python dep_scanner/scan.py --path <dir_containing_package.json_or_pom.xml>
    python dep_scanner/scan.py --app <app_name> --json
"""

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Tuple
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# ── Constants ──────────────────────────────────────────────────────────────
OSV_QUERY_URL = "https://api.osv.dev/v1/querybatch"
OSV_VULN_URL = "https://api.osv.dev/v1/vulns"
GENERATED_APP_DIR = "generated_application"
BATCH_SIZE = 50  # OSV recommends batching

# ANSI colors
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"
DIM = "\033[2m"


# ── Dependency Parsers ─────────────────────────────────────────────────────

def parse_package_json(path: str) -> List[Dict]:
    """Extract npm dependencies from package.json."""
    deps = []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for section in ("dependencies", "devDependencies"):
        for name, version_spec in data.get(section, {}).items():
            # Strip range chars: ^, ~, >=, etc. to get base version
            version = re.sub(r"^[\^~>=<]*", "", version_spec).strip()
            if version:
                deps.append({
                    "name": name,
                    "version": version,
                    "ecosystem": "npm",
                    "section": section,
                    "source": path,
                })
    return deps


def parse_package_lock(path: str) -> List[Dict]:
    """Extract resolved npm versions from package-lock.json."""
    deps = []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # lockfileVersion 2/3 uses "packages"
    packages = data.get("packages", {})
    for pkg_path, info in packages.items():
        if not pkg_path:  # root entry
            continue
        name = info.get("name") or pkg_path.split("node_modules/")[-1]
        version = info.get("version", "")
        if name and version:
            deps.append({
                "name": name,
                "version": version,
                "ecosystem": "npm",
                "section": "resolved",
                "source": path,
            })

    # lockfileVersion 1 uses "dependencies"
    if not packages:
        for name, info in data.get("dependencies", {}).items():
            version = info.get("version", "")
            if version:
                deps.append({
                    "name": name,
                    "version": version,
                    "ecosystem": "npm",
                    "section": "resolved",
                    "source": path,
                })
    return deps


POM_NS = "{http://maven.apache.org/POM/4.0.0}"


def parse_pom_xml(path: str) -> List[Dict]:
    """Extract Maven dependencies from pom.xml."""
    deps = []
    tree = ET.parse(path)
    root = tree.getroot()

    def _find(parent_el, tag):
        """Find child element with or without namespace."""
        el = parent_el.find(f"{POM_NS}{tag}")
        if el is None:
            el = parent_el.find(tag)
        return el

    # Collect properties for variable substitution
    props = {}
    props_el = _find(root, "properties")
    if props_el is not None:
        for child in props_el:
            tag = child.tag.replace(POM_NS, "")
            props[tag] = child.text or ""

    # Also grab parent version
    parent = _find(root, "parent")
    if parent is not None:
        pv = _find(parent, "version")
        if pv is not None and pv.text:
            props["project.parent.version"] = pv.text

    for dep_tag in ("dependencies", "dependencyManagement"):
        section = _find(root, dep_tag)
        if section is None:
            continue
        dep_container = section
        if dep_tag == "dependencyManagement":
            dep_container = _find(section, "dependencies")
            if dep_container is None:
                continue

        for dep in (dep_container.findall(f"{POM_NS}dependency") or dep_container.findall("dependency")):
            gid_el = _find(dep, "groupId")
            aid_el = _find(dep, "artifactId")
            ver_el = _find(dep, "version")

            if gid_el is None or aid_el is None:
                continue

            group_id = gid_el.text or ""
            artifact_id = aid_el.text or ""
            version = (ver_el.text if ver_el is not None else "") or ""

            # Resolve ${...} properties
            prop_match = re.match(r"^\$\{(.+)\}$", version)
            if prop_match:
                version = props.get(prop_match.group(1), version)

            if version and not version.startswith("$"):
                deps.append({
                    "name": f"{group_id}:{artifact_id}",
                    "version": version,
                    "ecosystem": "Maven",
                    "section": dep_tag,
                    "source": path,
                })
    return deps


# ── OSV API Client ─────────────────────────────────────────────────────────

def _osv_post(url: str, payload: dict) -> dict:
    """POST JSON to OSV API and return parsed response."""
    data = json.dumps(payload).encode("utf-8")
    req = Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"  {RED}OSV API error {e.code}: {body[:200]}{RESET}", file=sys.stderr)
        return {}
    except URLError as e:
        print(f"  {RED}Network error: {e.reason}{RESET}", file=sys.stderr)
        return {}


def query_osv_batch(deps: List[Dict]) -> List[List[Dict]]:
    """Query OSV for vulnerabilities in batches. Returns list of vuln lists per dep."""
    all_results = [[] for _ in deps]

    for batch_start in range(0, len(deps), BATCH_SIZE):
        batch = deps[batch_start:batch_start + BATCH_SIZE]
        queries = []
        for dep in batch:
            queries.append({
                "package": {
                    "name": dep["name"],
                    "ecosystem": dep["ecosystem"],
                },
                "version": dep["version"],
            })

        resp = _osv_post(OSV_QUERY_URL, {"queries": queries})
        results = resp.get("results", [])

        for i, result in enumerate(results):
            vulns = result.get("vulns", [])
            if vulns:
                all_results[batch_start + i] = vulns

    return all_results


def fetch_vuln_details(vuln_id: str) -> dict:
    """Fetch full vulnerability details from OSV."""
    try:
        req = Request(f"{OSV_VULN_URL}/{vuln_id}", headers={"Content-Type": "application/json"})
        with urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return {}


def classify_severity(vuln: dict) -> str:
    """Classify a vulnerability as critical/high/medium/low based on available data."""
    summary = (vuln.get("summary", "") + " " + vuln.get("details", "")).lower()

    # Malware / supply chain indicators
    malware_keywords = ["malware", "supply chain", "trojan", "rat", "backdoor",
                        "compromised", "hijack", "malicious"]
    if any(kw in summary for kw in malware_keywords):
        return "CRITICAL"

    # Check severity from affected entries
    for affected in vuln.get("affected", []):
        eco_specific = affected.get("ecosystem_specific", {})
        severity = eco_specific.get("severity", "").upper()
        if severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
            return severity

    # Check database_specific
    for affected in vuln.get("affected", []):
        db_specific = affected.get("database_specific", {})
        severity = db_specific.get("severity", "").upper()
        if severity in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
            return severity

    # Check CVSS from severity array
    for sev in vuln.get("severity", []):
        score_str = sev.get("score", "")
        # Try to extract CVSS base score
        match = re.search(r"CVSS:\d\.\d/AV:.*/.*", score_str)
        if match:
            # Rough classification from vector
            if "AV:N" in score_str:
                return "HIGH"

    return "UNKNOWN"


# ── Discovery ──────────────────────────────────────────────────────────────

def discover_files(search_dir: str) -> Tuple[List[str], List[str], List[str]]:
    """Find package.json, package-lock.json, and pom.xml files in a directory tree."""
    pkg_jsons = []
    lock_jsons = []
    pom_xmls = []

    for root, dirs, files in os.walk(search_dir):
        # Skip node_modules and target dirs
        dirs[:] = [d for d in dirs if d not in ("node_modules", "target", ".git", "__pycache__")]
        for f in files:
            full = os.path.join(root, f)
            if f == "package.json":
                pkg_jsons.append(full)
            elif f == "package-lock.json":
                lock_jsons.append(full)
            elif f == "pom.xml":
                pom_xmls.append(full)

    return pkg_jsons, lock_jsons, pom_xmls


def resolve_app_path(app_name: str) -> str:
    """Resolve app name to generated_application/<app> path."""
    path = os.path.join(GENERATED_APP_DIR, app_name)
    if not os.path.isdir(path):
        print(f"{RED}Error: App directory not found: {path}{RESET}", file=sys.stderr)
        sys.exit(1)
    return path


# ── Reporting ──────────────────────────────────────────────────────────────

SEVERITY_COLOR = {
    "CRITICAL": RED,
    "HIGH": RED,
    "MEDIUM": YELLOW,
    "LOW": DIM,
    "UNKNOWN": YELLOW,
}

SEVERITY_ICON = {
    "CRITICAL": "🔴",
    "HIGH": "🟠",
    "MEDIUM": "🟡",
    "LOW": "🔵",
    "UNKNOWN": "⚪",
}


def print_report(deps: List[Dict], vuln_results: List[List[Dict]], output_json: bool):
    """Print scan results."""
    findings = []
    clean_count = 0
    vuln_count = 0

    for dep, vulns in zip(deps, vuln_results):
        if not vulns:
            clean_count += 1
            continue

        # Fetch details for each vulnerability
        dep_findings = []
        for v in vulns:
            vid = v.get("id", "unknown")
            details = fetch_vuln_details(vid)
            severity = classify_severity(details) if details else "UNKNOWN"
            summary = details.get("summary", "No summary available")
            dep_findings.append({
                "id": vid,
                "severity": severity,
                "summary": summary,
                "details_url": f"https://osv.dev/vulnerability/{vid}",
            })
        vuln_count += 1
        findings.append({
            "package": dep["name"],
            "version": dep["version"],
            "ecosystem": dep["ecosystem"],
            "source": dep["source"],
            "vulnerabilities": dep_findings,
        })

    if output_json:
        print(json.dumps({
            "scanned": len(deps),
            "clean": clean_count,
            "vulnerable": vuln_count,
            "findings": findings,
        }, indent=2))
        return

    # Pretty print
    print()
    print(f"{BOLD}{'=' * 60}{RESET}")
    print(f"{BOLD}  Dependency Security Scan Results{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}")
    print(f"  Scanned: {len(deps)} dependencies")
    print(f"  Clean:   {GREEN}{clean_count}{RESET}")
    print(f"  Vulnerable: {RED if vuln_count else GREEN}{vuln_count}{RESET}")
    print(f"{BOLD}{'=' * 60}{RESET}")

    if not findings:
        print(f"\n  {GREEN}✅ No known vulnerabilities found.{RESET}\n")
        return

    # Sort by severity
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "UNKNOWN": 4}
    findings.sort(key=lambda f: min(
        severity_order.get(v["severity"], 5) for v in f["vulnerabilities"]
    ))

    for finding in findings:
        pkg = finding["package"]
        ver = finding["version"]
        eco = finding["ecosystem"]
        src = finding["source"]
        print(f"\n  {BOLD}{pkg}@{ver}{RESET} ({eco})")
        print(f"  {DIM}Source: {src}{RESET}")

        for v in finding["vulnerabilities"]:
            sev = v["severity"]
            color = SEVERITY_COLOR.get(sev, RESET)
            icon = SEVERITY_ICON.get(sev, "⚪")
            print(f"    {icon} {color}[{sev}]{RESET} {v['id']}")
            print(f"       {v['summary'][:120]}")
            print(f"       {CYAN}{v['details_url']}{RESET}")

    print(f"\n{BOLD}{'=' * 60}{RESET}")

    # Summary counts by severity
    sev_counts = {}
    for f in findings:
        for v in f["vulnerabilities"]:
            sev = v["severity"]
            sev_counts[sev] = sev_counts.get(sev, 0) + 1

    parts = []
    for sev in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"):
        if sev in sev_counts:
            color = SEVERITY_COLOR.get(sev, RESET)
            parts.append(f"{color}{sev_counts[sev]} {sev}{RESET}")
    print(f"  Total advisories: {', '.join(parts)}")
    print(f"{BOLD}{'=' * 60}{RESET}\n")


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Dependency Security Scanner — checks npm and Maven deps against OSV.dev"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--app", help="Application name (looks in generated_application/<app>)")
    group.add_argument("--path", help="Direct path to scan for package.json / pom.xml")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--lock", action="store_true",
                        help="Use package-lock.json for resolved versions (more accurate)")
    parser.add_argument("--skip-dev", action="store_true",
                        help="Skip devDependencies in package.json")
    args = parser.parse_args()

    search_dir = resolve_app_path(args.app) if args.app else args.path
    if not os.path.isdir(search_dir):
        print(f"{RED}Error: Directory not found: {search_dir}{RESET}", file=sys.stderr)
        sys.exit(1)

    if not args.json:
        print(f"\n  {BOLD}Scanning:{RESET} {search_dir}")

    # Discover dependency files
    pkg_jsons, lock_jsons, pom_xmls = discover_files(search_dir)

    if not args.json:
        print(f"  Found: {len(pkg_jsons)} package.json, {len(lock_jsons)} package-lock.json, {len(pom_xmls)} pom.xml")

    # Parse dependencies
    all_deps = []

    if args.lock and lock_jsons:
        for lj in lock_jsons:
            all_deps.extend(parse_package_lock(lj))
    else:
        for pj in pkg_jsons:
            parsed = parse_package_json(pj)
            if args.skip_dev:
                parsed = [d for d in parsed if d["section"] != "devDependencies"]
            all_deps.extend(parsed)

    for px in pom_xmls:
        all_deps.extend(parse_pom_xml(px))

    if not all_deps:
        if args.json:
            print(json.dumps({"scanned": 0, "clean": 0, "vulnerable": 0, "findings": []}))
        else:
            print(f"  {YELLOW}No dependencies found to scan.{RESET}\n")
        sys.exit(0)

    # Deduplicate (same name+version+ecosystem)
    seen = set()
    unique_deps = []
    for dep in all_deps:
        key = (dep["name"], dep["version"], dep["ecosystem"])
        if key not in seen:
            seen.add(key)
            unique_deps.append(dep)

    if not args.json:
        print(f"  Unique dependencies: {len(unique_deps)}")
        print(f"  Querying OSV.dev...\n")

    # Query OSV
    vuln_results = query_osv_batch(unique_deps)

    # Report
    print_report(unique_deps, vuln_results, args.json)

    # Exit code: 1 if any vulnerabilities found
    has_vulns = any(v for v in vuln_results if v)
    sys.exit(1 if has_vulns else 0)


if __name__ == "__main__":
    main()
