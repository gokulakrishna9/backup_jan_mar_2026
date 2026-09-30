"""Add missing fields to entity layer definitions for generate_application compatibility."""
import json
from pathlib import Path

for dir_path in [
    Path("application_definitions/job_portal"),
    Path("generated_application/job_portal/application_definitions"),
]:
    el_path = dir_path / "webflux_entity_layer.json"
    if not el_path.exists():
        continue
    data = json.loads(el_path.read_text(encoding="utf-8"))
    for i, ent in enumerate(data.get("entities", [])):
        if "isRootEntity" not in ent:
            ent["isRootEntity"] = (i == 0)
        if "hasPublicFlag" not in ent:
            ent["hasPublicFlag"] = False
        if "parentEntity" not in ent:
            ent["parentEntity"] = None
    el_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Fixed {el_path}")

print("Done!")
