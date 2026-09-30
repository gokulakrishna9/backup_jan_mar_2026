"""GitHub REST API client for crawling public repositories."""

import os
import time
import base64
import urllib.request
import urllib.error
import json
from typing import Optional


API_BASE = "https://api.github.com"


def _headers(token: Optional[str] = None) -> dict:
    token = token or os.environ.get("GITHUB_TOKEN")
    h = {"Accept": "application/vnd.github.v3+json", "User-Agent": "github-crawler/1.0"}
    if token:
        h["Authorization"] = f"token {token}"
    return h


def _get(url: str, token: Optional[str] = None) -> dict | list:
    """Make a GET request to the GitHub API with basic retry."""
    req = urllib.request.Request(url, headers=_headers(token))
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 403 and "rate limit" in e.read().decode().lower():
                if attempt < 2:
                    time.sleep(5 * (attempt + 1))
                    continue
            raise
        except urllib.error.URLError:
            if attempt < 2:
                time.sleep(2)
                continue
            raise


def _get_paginated(url: str, token: Optional[str] = None, max_pages: int = 10) -> list:
    """Fetch all pages of a paginated GitHub API endpoint."""
    results = []
    page = 1
    while page <= max_pages:
        sep = "&" if "?" in url else "?"
        page_url = f"{url}{sep}per_page=100&page={page}"
        data = _get(page_url, token)
        if not data:
            break
        results.extend(data)
        if len(data) < 100:
            break
        page += 1
    return results


def list_repos(user: str, token: Optional[str] = None) -> list[dict]:
    """List all public repositories for a user."""
    url = f"{API_BASE}/users/{user}/repos?type=public&sort=updated"
    repos = _get_paginated(url, token)
    return [
        {
            "name": r["name"],
            "full_name": r["full_name"],
            "description": r.get("description") or "",
            "language": r.get("language") or "N/A",
            "stars": r.get("stargazers_count", 0),
            "forks": r.get("forks_count", 0),
            "url": r["html_url"],
            "topics": r.get("topics", []),
            "updated_at": r.get("updated_at", ""),
            "default_branch": r.get("default_branch", "main"),
            "fork": r.get("fork", False),
        }
        for r in repos
    ]


def repo_info(owner: str, repo: str, token: Optional[str] = None) -> dict:
    """Get detailed info for a single repository."""
    url = f"{API_BASE}/repos/{owner}/{repo}"
    r = _get(url, token)
    return {
        "name": r["name"],
        "full_name": r["full_name"],
        "description": r.get("description") or "",
        "language": r.get("language") or "N/A",
        "stars": r.get("stargazers_count", 0),
        "forks": r.get("forks_count", 0),
        "url": r["html_url"],
        "topics": r.get("topics", []),
        "updated_at": r.get("updated_at", ""),
        "created_at": r.get("created_at", ""),
        "default_branch": r.get("default_branch", "main"),
        "fork": r.get("fork", False),
        "open_issues": r.get("open_issues_count", 0),
        "license": (r.get("license") or {}).get("spdx_id", "None"),
        "size_kb": r.get("size", 0),
    }


def repo_tree(owner: str, repo: str, branch: str = "main",
              token: Optional[str] = None) -> list[dict]:
    """Get the full file tree of a repository."""
    url = f"{API_BASE}/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
    data = _get(url, token)
    return [
        {"path": item["path"], "type": item["type"], "size": item.get("size", 0)}
        for item in data.get("tree", [])
    ]


def read_file(owner: str, repo: str, path: str, branch: str = "main",
              token: Optional[str] = None) -> str:
    """Read a file's contents from a repository."""
    url = f"{API_BASE}/repos/{owner}/{repo}/contents/{path}?ref={branch}"
    data = _get(url, token)
    if data.get("encoding") == "base64":
        return base64.b64decode(data["content"]).decode("utf-8", errors="replace")
    return data.get("content", "")


def read_readme(owner: str, repo: str, token: Optional[str] = None) -> str:
    """Try to read the README file from a repository."""
    try:
        url = f"{API_BASE}/repos/{owner}/{repo}/readme"
        data = _get(url, token)
        if data.get("encoding") == "base64":
            return base64.b64decode(data["content"]).decode("utf-8", errors="replace")
        return data.get("content", "")
    except urllib.error.HTTPError:
        return ""
