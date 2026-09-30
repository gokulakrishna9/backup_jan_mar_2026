"""Fix redux store thunk key: rename 'remove' to 'delete' in react_redux_store.json."""
import json
from pathlib import Path

path = Path("application_definitions/job_portal/react_redux_store.json")
data = json.loads(path.read_text(encoding="utf-8"))

for store in data:
    thunks = store.get("thunks", {})
    if "remove" in thunks:
        thunks["delete"] = thunks.pop("remove")

path.write_text(json.dumps(data, indent=2), encoding="utf-8")
print(f"Fixed {len(data)} stores: renamed 'remove' → 'delete' in thunks")
