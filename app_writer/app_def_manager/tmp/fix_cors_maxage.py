"""Add maxAge to corsConfig in all controllers."""
import json
from pathlib import Path

for dir_path in [
    Path("application_definitions/job_portal"),
    Path("generated_application/job_portal/application_definitions"),
]:
    ctrl_path = dir_path / "webflux_controller_layer.json"
    if not ctrl_path.exists():
        continue
    data = json.loads(ctrl_path.read_text(encoding="utf-8"))
    for c in data.get("controllers", []):
        cors = c.get("corsConfig", {})
        if "maxAge" not in cors:
            cors["maxAge"] = 3600
            c["corsConfig"] = cors
    ctrl_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Fixed {ctrl_path}")
