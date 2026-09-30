"""CLI for the Discussion Tracker.

Usage:
    python discussion_tracker/cli.py log --topic "..." --query "..." --response "..." [--category ...] [--tags ...] [--app ...]
    python discussion_tracker/cli.py task --topic "..." --description "..." [--context ...] [--priority ...] [--tags ...] [--app ...]
    python discussion_tracker/cli.py decision --topic "..." --decision "..." [--reasoning ...] [--tags ...] [--app ...]
    python discussion_tracker/cli.py complete --id N [--notes ...]
    python discussion_tracker/cli.py start --id N [--notes ...]
    python discussion_tracker/cli.py defer --id N [--reason ...]
    python discussion_tracker/cli.py list [--category ...] [--status ...] [--tag ...] [--app ...] [--limit N]
    python discussion_tracker/cli.py search --keyword "..."
    python discussion_tracker/cli.py show --id N
    python discussion_tracker/cli.py summary [--app ...]
"""

import argparse
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from discussion_tracker.tracker import (
    log_discussion, log_task, log_decision,
    start_task, complete_task, defer_task, list_entries,
    search, get_entry,
)


def _ensure_utf8():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def _format_entry(e: dict, verbose: bool = False) -> str:
    cat_icons = {"discussion": "💬", "task": "📋", "decision": "✅", "earmark": "📌"}
    status_icons = {"open": "🔴", "in_progress": "🟠", "completed": "🟢", "deferred": "🟡", "noted": "⚪", "decided": "🔵"}
    icon = cat_icons.get(e.get("category", ""), "📝")
    status_icon = status_icons.get(e.get("status", ""), "⚪")
    ts = e.get("timestamp", "")[:16].replace("T", " ")
    tags = ", ".join(e.get("tags", []))
    line = f"  {status_icon} #{e['id']:>3}  {icon} [{e.get('category', '?'):10}]  {e['topic']}"
    if tags:
        line += f"  [{tags}]"
    if e.get("app"):
        line += f"  ({e['app']})"
    if verbose:
        line += f"\n        Query:    {e.get('query', '')[:120]}"
        line += f"\n        Response: {e.get('response', '')[:120]}"
        line += f"\n        Date:     {ts}"
        if e.get("priority"):
            line += f"  Priority: {e['priority']}"
    return line


def _format_summary(entries: list[dict], app: str = None) -> str:
    total = len(entries)
    tasks = [e for e in entries if e.get("category") == "task"]
    open_tasks = [e for e in tasks if e.get("status") == "open"]
    in_progress = [e for e in tasks if e.get("status") == "in_progress"]
    completed = [e for e in tasks if e.get("status") == "completed"]
    decisions = [e for e in entries if e.get("category") == "decision"]
    discussions = [e for e in entries if e.get("category") == "discussion"]

    title = f"Discussion Tracker — {app}" if app else "Discussion Tracker — All"
    lines = [
        f"  {title}",
        f"  {'─' * 40}",
        f"  Total entries:    {total}",
        f"  Discussions:      {len(discussions)}",
        f"  Decisions:        {len(decisions)}",
        f"  Tasks:            {len(tasks)} ({len(open_tasks)} open, {len(in_progress)} in-progress, {len(completed)} completed)",
    ]
    if in_progress:
        lines.append(f"\n  🟠 Currently working on:")
        for t in in_progress:
            p = f" [{t['priority']}]" if t.get("priority") else ""
            started = t.get("startedAt", "")[:16].replace("T", " ")
            lines.append(f"    🔧 #{t['id']} {t['topic']}{p}  (started {started})")
    if open_tasks:
        lines.append(f"\n  Open tasks:")
        for t in open_tasks:
            p = f" [{t['priority']}]" if t.get("priority") else ""
            lines.append(f"    📋 #{t['id']} {t['topic']}{p}")
    return "\n".join(lines)


def main():
    _ensure_utf8()
    parser = argparse.ArgumentParser(description="Discussion Tracker — log conversations, decisions, and tasks")
    sub = parser.add_subparsers(dest="command")
    sub.choices  # force subparsers to be recognized

    # Subcommand list for help text
    # log, task, decision, start, complete, defer, list, search, show, summary

    # log
    p_log = sub.add_parser("log", help="Log a discussion")
    p_log.add_argument("--topic", required=True)
    p_log.add_argument("--query", required=True)
    p_log.add_argument("--response", required=True)
    p_log.add_argument("--category", default="discussion")
    p_log.add_argument("--tags", default="", help="Comma-separated tags")
    p_log.add_argument("--entities", default="", help="Comma-separated related entities")
    p_log.add_argument("--app", default="")

    # task
    p_task = sub.add_parser("task", help="Log a future task")
    p_task.add_argument("--topic", required=True)
    p_task.add_argument("--description", required=True)
    p_task.add_argument("--context", default="")
    p_task.add_argument("--priority", default="normal", choices=["low", "normal", "high", "critical"])
    p_task.add_argument("--tags", default="")
    p_task.add_argument("--entities", default="")
    p_task.add_argument("--app", default="")

    # decision
    p_dec = sub.add_parser("decision", help="Log a decision")
    p_dec.add_argument("--topic", required=True)
    p_dec.add_argument("--decision", required=True)
    p_dec.add_argument("--reasoning", default="")
    p_dec.add_argument("--tags", default="")
    p_dec.add_argument("--entities", default="")
    p_dec.add_argument("--app", default="")

    # complete
    p_comp = sub.add_parser("complete", help="Mark task completed")
    p_comp.add_argument("--id", required=True, type=int)
    p_comp.add_argument("--notes", default="")

    # start
    p_start = sub.add_parser("start", help="Mark task as in-progress")
    p_start.add_argument("--id", required=True, type=int)
    p_start.add_argument("--notes", default="")

    # defer
    p_defer = sub.add_parser("defer", help="Defer a task")
    p_defer.add_argument("--id", required=True, type=int)
    p_defer.add_argument("--reason", default="")

    # list
    p_list = sub.add_parser("list", help="List entries")
    p_list.add_argument("--category", default=None)
    p_list.add_argument("--status", default=None)
    p_list.add_argument("--tag", default=None)
    p_list.add_argument("--app", default=None)
    p_list.add_argument("--limit", type=int, default=50)
    p_list.add_argument("--verbose", "-v", action="store_true")

    # search
    p_search = sub.add_parser("search", help="Search entries")
    p_search.add_argument("--keyword", required=True)

    # show
    p_show = sub.add_parser("show", help="Show single entry")
    p_show.add_argument("--id", required=True, type=int)

    # summary
    p_summary = sub.add_parser("summary", help="Show summary")
    p_summary.add_argument("--app", default=None)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmd = args.command

    if cmd == "log":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []
        entities = [e.strip() for e in args.entities.split(",") if e.strip()] if args.entities else []
        entry = log_discussion(args.topic, args.query, args.response,
                               category=args.category, tags=tags,
                               related_entities=entities, app=args.app)
        print(f"  ✅ Logged #{entry['id']}: {entry['topic']}")

    elif cmd == "task":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []
        entities = [e.strip() for e in args.entities.split(",") if e.strip()] if args.entities else []
        entry = log_task(args.topic, args.description, context=args.context,
                         priority=args.priority, tags=tags,
                         related_entities=entities, app=args.app)
        print(f"  📋 Task #{entry['id']}: {entry['topic']} [{entry['priority']}]")

    elif cmd == "decision":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []
        entities = [e.strip() for e in args.entities.split(",") if e.strip()] if args.entities else []
        entry = log_decision(args.topic, args.decision, reasoning=args.reasoning,
                             tags=tags, related_entities=entities, app=args.app)
        print(f"  ✅ Decision #{entry['id']}: {entry['topic']}")

    elif cmd == "complete":
        entry = complete_task(args.id, notes=args.notes)
        if entry:
            print(f"  🟢 Task #{entry['id']} completed: {entry['topic']}")
        else:
            print(f"  ❌ Task #{args.id} not found")

    elif cmd == "start":
        entry = start_task(args.id, notes=args.notes)
        if entry:
            print(f"  🟠 Task #{entry['id']} started: {entry['topic']}")
        else:
            print(f"  ❌ Task #{args.id} not found")

    elif cmd == "defer":
        entry = defer_task(args.id, reason=args.reason)
        if entry:
            print(f"  🟡 Task #{entry['id']} deferred: {entry['topic']}")
        else:
            print(f"  ❌ Task #{args.id} not found")

    elif cmd == "list":
        entries = list_entries(category=args.category, status=args.status,
                               tag=args.tag, app=args.app, limit=args.limit)
        if not entries:
            print("  No entries found")
        else:
            print(f"  {len(entries)} entries:")
            for e in entries:
                print(_format_entry(e, verbose=getattr(args, 'verbose', False)))

    elif cmd == "search":
        results = search(args.keyword)
        if not results:
            print(f"  No results for '{args.keyword}'")
        else:
            print(f"  {len(results)} results for '{args.keyword}':")
            for e in results:
                print(_format_entry(e, verbose=True))

    elif cmd == "show":
        entry = get_entry(args.id)
        if entry:
            print(json.dumps(entry, indent=2, ensure_ascii=False))
        else:
            print(f"  ❌ Entry #{args.id} not found")

    elif cmd == "summary":
        entries = list_entries(app=args.app, limit=9999)
        print(_format_summary(entries, app=args.app))


if __name__ == "__main__":
    main()
