"""Remove soft-delete from all job_portal definitions."""
import json
from pathlib import Path

app_dir = Path("application_definitions/job_portal")

# Entity layer: hasSoftDelete=false, remove isDeleted field
el_path = app_dir / "webflux_entity_layer.json"
el = json.loads(el_path.read_text(encoding="utf-8"))
for ent in el.get("entities", []):
    ent["hasSoftDelete"] = False
    ent["fields"] = [f for f in ent["fields"] if f.get("fieldName") != "isDeleted" and f.get("columnName") != "is_deleted"]
el_path.write_text(json.dumps(el, indent=2, ensure_ascii=False), encoding="utf-8")
print("Fixed entity layer")

# Entities (column view): remove is_deleted
ent_path = app_dir / "webflux_entities.json"
ent = json.loads(ent_path.read_text(encoding="utf-8"))
for e in ent.get("entities", []):
    e["columns"] = [c for c in e["columns"] if c.get("name") != "is_deleted"]
ent_path.write_text(json.dumps(ent, indent=2, ensure_ascii=False), encoding="utf-8")
print("Fixed entities")

# Repository layer: hasSoftDelete=false
repo_path = app_dir / "webflux_repository_layer.json"
repo = json.loads(repo_path.read_text(encoding="utf-8"))
for r in repo.get("repositories", []):
    r["hasSoftDelete"] = False
repo_path.write_text(json.dumps(repo, indent=2, ensure_ascii=False), encoding="utf-8")
print("Fixed repository layer")

# DTO layer: remove isDeleted from Output DTOs
dto_path = app_dir / "webflux_dto_layer.json"
dto = json.loads(dto_path.read_text(encoding="utf-8"))
for d in dto.get("dtos", []):
    d["fields"] = [f for f in d["fields"] if f.get("fieldName") != "isDeleted"]
dto_path.write_text(json.dumps(dto, indent=2, ensure_ascii=False), encoding="utf-8")
print("Fixed DTO layer")

print("Done!")
