"""Unit tests for definition loader AI layer integration.

Tests loading valid AI JSON, missing file (None), invalid JSON (ValueError),
and manifest integration for the ai_layer field on DefinitionBundle.

**Validates: Requirements 1.32–1.35**
"""

import json
import sys
import tempfile
from pathlib import Path

import pytest

# Ensure swfaw/ is on sys.path so `from version import ...` works
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.definition_loader import load_all_definitions


# ---------------------------------------------------------------------------
# Helpers — reuse patterns from test_definition_loader_properties.py
# ---------------------------------------------------------------------------

def _minimal_entity_layer():
    return {
        "entities": [
            {
                "tableName": "users",
                "className": "User",
                "fields": [
                    {
                        "columnName": "user_id",
                        "fieldName": "userId",
                        "javaType": "Long",
                        "isPrimaryKey": True,
                        "isNullable": False,
                        "columnDefinition": "BIGINT UNSIGNED",
                    },
                ],
            }
        ]
    }


def _minimal_manifest(include_ai_layer: bool = False):
    """Build a manifest with required files and optionally ai_layer."""
    files = {
        "project_metadata": "webflux_project_metadata.json",
        "entities": "webflux_entities.json",
        "relationships": "webflux_relationships.json",
        "entity_layer": "webflux_entity_layer.json",
        "repository_layer": "webflux_repository_layer.json",
        "service_layer": "webflux_service_layer.json",
        "controller_layer": "webflux_controller_layer.json",
        "dto_layer": "webflux_dto_layer.json",
    }
    if include_ai_layer:
        files["ai_layer"] = "webflux_ai_layer.json"
    return {"version": "2.5", "format": "split", "files": files}


def _write_json(directory: Path, filename: str, data):
    with open(directory / filename, "w", encoding="utf-8") as f:
        json.dump(data, f)


def _setup_app_dir(tmp: Path, include_ai_layer: bool = False) -> Path:
    """Write required definition files and optionally the AI layer file."""
    app_dir = tmp / "test_app"
    app_dir.mkdir(parents=True, exist_ok=True)

    _write_json(app_dir, "webflux_manifest.json", _minimal_manifest(include_ai_layer))
    _write_json(app_dir, "webflux_project_metadata.json", {"projectMetadata": {"database": {"name": "test_db"}}})
    _write_json(app_dir, "webflux_entity_layer.json", _minimal_entity_layer())
    _write_json(app_dir, "webflux_entities.json", {"entities": [{"name": "users", "columns": []}]})
    _write_json(app_dir, "webflux_relationships.json", {"relationships": []})
    _write_json(app_dir, "webflux_repository_layer.json", {"repositories": []})
    _write_json(app_dir, "webflux_service_layer.json", {"services": []})
    _write_json(app_dir, "webflux_controller_layer.json", {"controllers": []})
    _write_json(app_dir, "webflux_dto_layer.json", {"dtos": []})

    return app_dir


# ---------------------------------------------------------------------------
# Test: Loading valid AI JSON (Requirement 1.32, 1.34)
# ---------------------------------------------------------------------------

def test_load_valid_ai_layer():
    """When webflux_ai_layer.json contains valid AI config and the manifest
    references it, bundle.ai_layer should be the parsed dict."""
    ai_config = {
        "schemaVersion": "1.0",
        "providers": [
            {"name": "gpt4", "type": "openai", "model": "gpt-4"}
        ],
        "entityCapabilities": [],
        "standaloneOperations": [],
    }

    with tempfile.TemporaryDirectory() as tmp:
        app_dir = _setup_app_dir(Path(tmp), include_ai_layer=True)
        _write_json(app_dir, "webflux_ai_layer.json", ai_config)

        bundle = load_all_definitions(app_dir)

        assert bundle.ai_layer is not None
        assert bundle.ai_layer == ai_config


# ---------------------------------------------------------------------------
# Test: Missing file sets ai_layer to None (Requirement 1.33, 1.35)
# ---------------------------------------------------------------------------

def test_missing_ai_layer_is_none():
    """When ai_layer is NOT in the manifest, bundle.ai_layer should be None
    and loading should succeed without error."""
    with tempfile.TemporaryDirectory() as tmp:
        app_dir = _setup_app_dir(Path(tmp), include_ai_layer=False)

        bundle = load_all_definitions(app_dir)

        assert bundle.ai_layer is None


# ---------------------------------------------------------------------------
# Test: Invalid JSON raises ValueError (Requirement 1.32, related to 1.26)
# ---------------------------------------------------------------------------

def test_invalid_ai_json_raises_value_error():
    """When webflux_ai_layer.json contains invalid JSON, loading should
    raise ValueError with the file path in the message."""
    with tempfile.TemporaryDirectory() as tmp:
        app_dir = _setup_app_dir(Path(tmp), include_ai_layer=True)

        # Write invalid JSON content
        ai_path = app_dir / "webflux_ai_layer.json"
        with open(ai_path, "w", encoding="utf-8") as f:
            f.write("{not valid json at all!!!")

        with pytest.raises(ValueError) as exc_info:
            load_all_definitions(app_dir)

        assert str(ai_path) in str(exc_info.value)


# ---------------------------------------------------------------------------
# Test: Manifest integration — ai_layer key resolves file (Req 1.34)
# ---------------------------------------------------------------------------

def test_manifest_integration_resolves_ai_layer_file():
    """When the manifest's files map contains an ai_layer key, the loader
    resolves and loads the referenced file correctly."""
    ai_config = {
        "schemaVersion": "1.0",
        "providers": [],
        "entityCapabilities": [],
        "ragSources": [{"name": "docs", "type": "semantic"}],
    }

    with tempfile.TemporaryDirectory() as tmp:
        app_dir = _setup_app_dir(Path(tmp), include_ai_layer=True)
        _write_json(app_dir, "webflux_ai_layer.json", ai_config)

        bundle = load_all_definitions(app_dir)

        # Verify the loaded ai_layer matches what we wrote
        assert bundle.ai_layer is not None
        assert bundle.ai_layer["schemaVersion"] == "1.0"
        assert bundle.ai_layer["ragSources"] == ai_config["ragSources"]
        # Verify other required fields still loaded correctly
        assert bundle.app_name == "test_app"
        assert bundle.manifest is not None
        assert bundle.entity_layer is not None
