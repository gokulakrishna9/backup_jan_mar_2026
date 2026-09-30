#!/usr/bin/env python3
"""CLI for the GitHub Crawler tool."""

import argparse
import json
import sys

from github_crawler import api


def cmd_list_repos(args):
    repos = api.list_repos(args.user, args.token)
    if args.json:
        print(json.dumps(repos, indent=2))
        return
    if not repos:
        print(f"No public repositories found for '{args.user}'.")
        return
    print(f"\n📦 Public repositories for {args.user} ({len(repos)} repos):\n")
    for r in repos:
        fork_tag = " [fork]" if r["fork"] else ""
        topics = f'  Topics: {", ".join(r["topics"])}' if r["topics"] else ""
        print(f'  ⭐ {r["stars"]:>3}  {r["name"]}{fork_tag}')
        print(f'        {r["description"][:100] if r["description"] else "(no description)"}')
        print(f'        Language: {r["language"]}  |  Updated: {r["updated_at"][:10]}')
        if topics:
            print(f"      {topics}")
        print()


def cmd_repo_info(args):
    info = api.repo_info(args.owner, args.repo, args.token)
    if args.json:
        print(json.dumps(info, indent=2))
        return
    print(f'\n📂 {info["full_name"]}')
    print(f'   {info["description"]}')
    print(f'   Language: {info["language"]}  |  ⭐ {info["stars"]}  |  🍴 {info["forks"]}')
    print(f'   License: {info["license"]}  |  Size: {info["size_kb"]} KB')
    print(f'   Created: {info["created_at"][:10]}  |  Updated: {info["updated_at"][:10]}')
    if info["topics"]:
        print(f'   Topics: {", ".join(info["topics"])}')
    print(f'   URL: {info["url"]}')
    print()


def cmd_tree(args):
    info = api.repo_info(args.owner, args.repo, args.token)
    branch = args.branch or info["default_branch"]
    tree = api.repo_tree(args.owner, args.repo, branch, args.token)
    if args.json:
        print(json.dumps(tree, indent=2))
        return
    print(f'\n🌳 File tree for {args.owner}/{args.repo} ({branch}):\n')
    for item in tree:
        prefix = "📁" if item["type"] == "tree" else "📄"
        size = f'  ({item["size"]} B)' if item["type"] == "blob" and item["size"] else ""
        print(f'  {prefix} {item["path"]}{size}')
    print(f"\n  Total: {len(tree)} items\n")


def cmd_read_file(args):
    info = api.repo_info(args.owner, args.repo, args.token)
    branch = args.branch or info["default_branch"]
    content = api.read_file(args.owner, args.repo, args.path, branch, args.token)
    print(content)


def cmd_summarize(args):
    """Generate a markdown summary of all repos for a user."""
    repos = api.list_repos(args.user, args.token)
    if not repos:
        print(f"No public repositories found for '{args.user}'.")
        return

    lines = [f"# GitHub Repositories: {args.user}\n"]
    lines.append(f"Total public repositories: {len(repos)}\n")

    for r in repos:
        lines.append(f'## [{r["name"]}]({r["url"]})\n')
        if r["description"]:
            lines.append(f'{r["description"]}\n')

        lines.append(f'- **Language:** {r["language"]}')
        lines.append(f'- **Stars:** {r["stars"]}  |  **Forks:** {r["forks"]}')
        lines.append(f'- **Updated:** {r["updated_at"][:10]}')
        if r["fork"]:
            lines.append("- *(forked repository)*")
        if r["topics"]:
            lines.append(f'- **Topics:** {", ".join(r["topics"])}')

        # Try to fetch README for richer context
        if not args.skip_readme:
            owner = r["full_name"].split("/")[0]
            readme = api.read_readme(owner, r["name"], args.token)
            if readme:
                # Take first ~500 chars of README as excerpt
                excerpt = readme.strip()[:500]
                if len(readme.strip()) > 500:
                    excerpt += "..."
                lines.append(f"\n### README Excerpt\n")
                lines.append(f"```\n{excerpt}\n```\n")
            else:
                lines.append("\n*(No README found)*\n")
        lines.append("")

    output = "\n".join(lines)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"✅ Summary written to {args.output}")
    else:
        print(output)


def main():
    parser = argparse.ArgumentParser(
        prog="github_crawler",
        description="GitHub repository crawler using the GitHub REST API",
    )
    parser.add_argument("--token", help="GitHub personal access token (or set GITHUB_TOKEN env var)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    # list-repos
    p_list = sub.add_parser("list-repos", help="List public repos for a user/org")
    p_list.add_argument("--user", required=True, help="GitHub username or org")
    p_list.set_defaults(func=cmd_list_repos)

    # repo-info
    p_info = sub.add_parser("repo-info", help="Get detailed info for a repo")
    p_info.add_argument("--owner", required=True, help="Repository owner")
    p_info.add_argument("--repo", required=True, help="Repository name")
    p_info.set_defaults(func=cmd_repo_info)

    # tree
    p_tree = sub.add_parser("tree", help="Browse the file tree of a repo")
    p_tree.add_argument("--owner", required=True, help="Repository owner")
    p_tree.add_argument("--repo", required=True, help="Repository name")
    p_tree.add_argument("--branch", help="Branch name (default: repo default branch)")
    p_tree.set_defaults(func=cmd_tree)

    # read-file
    p_read = sub.add_parser("read-file", help="Read a file from a repo")
    p_read.add_argument("--owner", required=True, help="Repository owner")
    p_read.add_argument("--repo", required=True, help="Repository name")
    p_read.add_argument("--path", required=True, help="File path in the repo")
    p_read.add_argument("--branch", help="Branch name (default: repo default branch)")
    p_read.set_defaults(func=cmd_read_file)

    # summarize
    p_sum = sub.add_parser("summarize", help="Generate markdown summary of all repos")
    p_sum.add_argument("--user", required=True, help="GitHub username or org")
    p_sum.add_argument("--output", "-o", help="Output file path (prints to stdout if omitted)")
    p_sum.add_argument("--skip-readme", action="store_true", help="Skip fetching README excerpts")
    p_sum.set_defaults(func=cmd_summarize)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
