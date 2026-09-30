"""Update all job_portal tasks to workspace — they're generator improvements, not app-specific."""
import json
from pathlib import Path

path = Path("discussion_tracker/data/discussions.json")
entries = json.loads(path.read_text(encoding="utf-8"))

updated = 0
for e in entries:
    if e.get("app") == "job_portal" and e.get("category") == "task":
        e["app"] = "workspace"
        updated += 1

path.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Updated {updated} tasks from job_portal → workspace")
