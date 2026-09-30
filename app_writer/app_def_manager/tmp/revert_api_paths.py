"""Revert react_api_services.json basePaths to match the definition (snake_case)."""
import json
from pathlib import Path

# Read the controller layer definition (source of truth)
ctrl_data = json.loads(Path("application_definitions/job_portal/webflux_controller_layer.json").read_text(encoding="utf-8"))
ctrl_paths = {c["entityName"]: c["basePath"] for c in ctrl_data["controllers"]}

# Update react_api_services.json to match
api_path = Path("application_definitions/job_portal/react_api_services.json")
services = json.loads(api_path.read_text(encoding="utf-8"))
updated = 0
for svc in services:
    entity = svc["entityName"]
    if entity in ctrl_paths and svc["basePath"] != ctrl_paths[entity]:
        old = svc["basePath"]
        svc["basePath"] = ctrl_paths[entity]
        print(f"  {entity}: {old} -> {ctrl_paths[entity]}")
        updated += 1

api_path.write_text(json.dumps(services, indent=2), encoding="utf-8")
print(f"\nReverted {updated} paths to match definitions")
