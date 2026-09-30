"""Discussion Tracker — structured log of conversations, decisions, and future tasks."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional


DATA_DIR = Path("discussion_tracker/data")
DISCUSSIONS_FILE = DATA_DIR / "discussions.json"


def _ensure_data():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DISCUSSIONS_FILE.exists():
        DISCUSSIONS_FILE.write_text("[]", encoding="utf-8")


def _load() -> list[dict]:
    _ensure_data()
    return json.loads(DISCUSSIONS_FILE.read_text(encoding="utf-8"))


def _save(entries: list[dict]):
    _ensure_data()
    DISCUSSIONS_FILE.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")


def _next_id(entries: list[dict]) -> int:
    if not entries:
        return 1
    return max(e.get("id", 0) for e in entries) + 1


def log_discussion(topic: str, query: str, response: str,
                   category: str = "discussion", tags: list[str] = None,
                   related_entities: list[str] = None, app: str = None) -> dict:
    """Log a discussion entry."""
    entries = _load()
    entry = {
        "id": _next_id(entries),
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "category": category,
        "query": query,
        "response": response,
        "status": "noted",
        "tags": tags or [],
        "relatedEntities": related_entities or [],
        "app": app or "",
    }
    entries.append(entry)
    _save(entries)
    return entry


def log_task(topic: str, description: str, context: str = "",
             priority: str = "normal", tags: list[str] = None,
             related_entities: list[str] = None, app: str = None) -> dict:
    """Log a future task / earmarked item."""
    entries = _load()
    entry = {
        "id": _next_id(entries),
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "category": "task",
        "query": description,
        "response": context,
        "status": "open",
        "priority": priority,
        "tags": tags or [],
        "relatedEntities": related_entities or [],
        "app": app or "",
    }
    entries.append(entry)
    _save(entries)
    return entry


def log_decision(topic: str, decision: str, reasoning: str = "",
                 tags: list[str] = None, related_entities: list[str] = None,
                 app: str = None) -> dict:
    """Log a decision made during conversation."""
    entries = _load()
    entry = {
        "id": _next_id(entries),
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "category": "decision",
        "query": decision,
        "response": reasoning,
        "status": "decided",
        "tags": tags or [],
        "relatedEntities": related_entities or [],
        "app": app or "",
    }
    entries.append(entry)
    _save(entries)
    return entry


def start_task(task_id: int, notes: str = "") -> Optional[dict]:
    """Mark a task as in-progress."""
    entries = _load()
    for e in entries:
        if e["id"] == task_id:
            e["status"] = "in_progress"
            e["startedAt"] = datetime.now().isoformat()
            if notes:
                e["startNotes"] = notes
            _save(entries)
            return e
    return None


def complete_task(task_id: int, notes: str = "") -> Optional[dict]:
    """Mark a task as completed."""
    entries = _load()
    for e in entries:
        if e["id"] == task_id:
            e["status"] = "completed"
            e["completedAt"] = datetime.now().isoformat()
            if notes:
                e["completionNotes"] = notes
            _save(entries)
            return e
    return None


def defer_task(task_id: int, reason: str = "") -> Optional[dict]:
    """Defer a task."""
    entries = _load()
    for e in entries:
        if e["id"] == task_id:
            e["status"] = "deferred"
            if reason:
                e["deferReason"] = reason
            _save(entries)
            return e
    return None


def list_entries(category: str = None, status: str = None,
                 tag: str = None, app: str = None, limit: int = 50) -> list[dict]:
    """List entries with optional filters."""
    entries = _load()
    if category:
        entries = [e for e in entries if e.get("category") == category]
    if status:
        entries = [e for e in entries if e.get("status") == status]
    if tag:
        entries = [e for e in entries if tag in e.get("tags", [])]
    if app:
        entries = [e for e in entries if e.get("app") == app]
    return entries[-limit:]


def search(keyword: str) -> list[dict]:
    """Search entries by keyword in topic, query, response, tags."""
    entries = _load()
    kw = keyword.lower()
    return [e for e in entries if
            kw in e.get("topic", "").lower() or
            kw in e.get("query", "").lower() or
            kw in e.get("response", "").lower() or
            kw in " ".join(e.get("tags", [])).lower()]


def get_entry(entry_id: int) -> Optional[dict]:
    """Get a single entry by ID."""
    entries = _load()
    for e in entries:
        if e["id"] == entry_id:
            return e
    return None
