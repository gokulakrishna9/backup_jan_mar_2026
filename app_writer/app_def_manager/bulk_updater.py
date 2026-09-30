"""Bulk updater — batch-update entity-level flags across definition layers.

Usage (CLI):
    python app_def_manager/bulk_updater.py --app <app> --entities <comma-separated> --set <key=value> [--set <key=value> ...]

Examples:
    # Enable authorization on all entities
    python app_def_manager/bulk_updater.py --app job_portal --entities ALL --set hasAuthorization=true

    # Enable singleRecordPerUser on specific entities
    python app_def_manager/bulk_updater.py --app job_portal --entities UserProfile,StudentProfile --set singleRecordPerUser=true

    # Enable auth + set roles on controller endpoints
    python app_def_manager/bulk_updater.py --app job_portal --entities ALL --set hasAuthorization=true --set requiresAuth=true --set roles=USER
"""

import json
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_def_manager.status_tracker import StatusTracker


def _parse_value(val: str):
    """Parse a string value into the appropriate Python type."""
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    try:
        return int(val)
    except ValueError:
        pass
    return val


def _get_all_entity_names(app_dir: Path) -> list[str]:
    """Read all entity names from the entity layer."""
    el_path = app_dir / "webflux_entity_layer.json"
    data = json.loads(el_path.read_text(encoding="utf-8"))
    return [e["className"] for e in data.get("entities", [])]


def bulk_update(app_name: str, entity_names: list[str], updates: dict[str, object]) -> dict[str, int]:
    """Apply updates to matching entities across service, repository, and controller layers.

    Args:
        app_name: Application name.
        entity_names: List of entity class names, or ["ALL"] for all entities.
        updates: Dict of key-value pairs to set on matching entries.

    Returns:
        Dict of {layer_file: count_of_updated_entries}.
    """
    app_dir = Path("application_definitions") / app_name
    if not app_dir.exists():
        raise FileNotFoundError(f"Application '{app_name}' not found at {app_dir}")

    if entity_names == ["ALL"]:
        entity_names = _get_all_entity_names(app_dir)

    target_set = set(entity_names)

    # Separate controller-endpoint-level keys from entity-level keys
    endpoint_keys = {"requiresAuth", "roles"}
    entity_updates = {k: v for k, v in updates.items() if k not in endpoint_keys}
    endpoint_updates = {k: v for k, v in updates.items() if k in endpoint_keys}

    results = {}
    dirty_files = []

    # Update service layer
    svc_path = app_dir / "webflux_service_layer.json"
    if svc_path.exists() and entity_updates:
        data = json.loads(svc_path.read_text(encoding="utf-8"))
        count = 0
        for s in data.get("services", []):
            if s.get("entityName") in target_set:
                for k, v in entity_updates.items():
                    s[k] = v
                count += 1
        svc_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        results["webflux_service_layer.json"] = count
        dirty_files.append("webflux_service_layer.json")

    # Update repository layer
    repo_path = app_dir / "webflux_repository_layer.json"
    if repo_path.exists() and entity_updates:
        data = json.loads(repo_path.read_text(encoding="utf-8"))
        count = 0
        for r in data.get("repositories", []):
            if r.get("entityName") in target_set:
                for k, v in entity_updates.items():
                    r[k] = v
                count += 1
        repo_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        results["webflux_repository_layer.json"] = count
        dirty_files.append("webflux_repository_layer.json")

    # Update controller layer (entity-level + endpoint-level)
    ctrl_path = app_dir / "webflux_controller_layer.json"
    if ctrl_path.exists() and (entity_updates or endpoint_updates):
        data = json.loads(ctrl_path.read_text(encoding="utf-8"))
        count = 0
        for c in data.get("controllers", []):
            if c.get("entityName") in target_set:
                # Entity-level updates (e.g. singleRecordPerUser)
                for k, v in entity_updates.items():
                    c[k] = v
                # Endpoint-level updates (e.g. requiresAuth, roles)
                if endpoint_updates:
                    for ep in c.get("endpoints", {}).values():
                        if isinstance(ep, dict):
                            for k, v in endpoint_updates.items():
                                if k == "roles" and isinstance(v, str):
                                    ep[k] = [v]
                                else:
                                    ep[k] = v
                count += 1
        ctrl_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        results["webflux_controller_layer.json"] = count
        dirty_files.append("webflux_controller_layer.json")

    # Mark dirty
    if dirty_files:
        tracker = StatusTracker(app_dir)
        tracker.mark_dirty(dirty_files)

    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Bulk update entity-level flags across definition layers")
    parser.add_argument("--app", required=True, help="Application name")
    parser.add_argument("--entities", required=True, help="Comma-separated entity names or ALL")
    parser.add_argument("--set", action="append", required=True, dest="sets",
                        help="key=value pair to set (can repeat)")
    args = parser.parse_args()

    entities = ["ALL"] if args.entities.upper() == "ALL" else [e.strip() for e in args.entities.split(",")]

    updates = {}
    for kv in args.sets:
        if "=" not in kv:
            print(f"  ❌ Invalid --set format: '{kv}' (expected key=value)", file=sys.stderr)
            sys.exit(1)
        key, val = kv.split("=", 1)
        updates[key] = _parse_value(val)

    results = bulk_update(args.app, entities, updates)
    for layer, count in results.items():
        print(f"  ✅ {layer}: updated {count} entries")


if __name__ == "__main__":
    main()
