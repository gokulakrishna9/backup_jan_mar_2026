"""Fix application definitions: remove audit/soft-delete fields from Input DTOs and entity layer.

1. Remove createdAt, updatedAt, isDeleted from Input DTO fields in webflux_dto_layer.json
2. Remove isDeleted from entity layer fields in webflux_entity_layer.json
   (createdAt/updatedAt stay in entity layer — service generator already excludes them)
"""
import json
from pathlib import Path

app_dir = Path("application_definitions/job_portal")

# Fields to remove from Input DTOs
INPUT_EXCLUDE = {"createdAt", "updatedAt", "isDeleted"}

# Fields to remove from entity layer (isDeleted only — auto-added by hasSoftDelete as deletedAt)
ENTITY_EXCLUDE = {"isDeleted"}

# Fix DTO layer
dto_path = app_dir / "webflux_dto_layer.json"
dto_data = json.loads(dto_path.read_text(encoding="utf-8"))
dto_fixed = 0
for dto in dto_data.get("dtos", []):
    if dto.get("dtoType") == "Input":
        before = len(dto["fields"])
        dto["fields"] = [f for f in dto["fields"] if f.get("fieldName") not in INPUT_EXCLUDE]
        removed = before - len(dto["fields"])
        if removed:
            dto_fixed += 1
            print(f"  Input DTO {dto['entityName']}: removed {removed} audit fields")
dto_path.write_text(json.dumps(dto_data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Fixed {dto_fixed} Input DTOs")

# Fix entity layer
el_path = app_dir / "webflux_entity_layer.json"
el_data = json.loads(el_path.read_text(encoding="utf-8"))
el_fixed = 0
for ent in el_data.get("entities", []):
    before = len(ent["fields"])
    ent["fields"] = [f for f in ent["fields"] if f.get("fieldName") not in ENTITY_EXCLUDE]
    removed = before - len(ent["fields"])
    if removed:
        el_fixed += 1
el_path.write_text(json.dumps(el_data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Fixed {el_fixed} entities in entity layer (removed isDeleted field)")

# Also fix webflux_entities.json (column-level view)
ent_path = app_dir / "webflux_entities.json"
ent_data = json.loads(ent_path.read_text(encoding="utf-8"))
for ent in ent_data.get("entities", []):
    ent["columns"] = [c for c in ent["columns"] if c.get("name") != "is_deleted"]
ent_path.write_text(json.dumps(ent_data, indent=2, ensure_ascii=False), encoding="utf-8")
print("Fixed webflux_entities.json (removed is_deleted columns)")

print("\nDone!")
