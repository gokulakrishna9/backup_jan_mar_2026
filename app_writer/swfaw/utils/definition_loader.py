"""Loader and validator for application definition files.

Reads all definition JSON files from an application_definitions/<app_name>/
directory, validates structure and manifest version, and returns a
DefinitionBundle containing all parsed data.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from models.database_definition import DatabaseDefinition
from version import SUPPORTED_MANIFEST_VERSIONS


@dataclass
class DefinitionBundle:
    """Container for all loaded definition data."""
    app_name: str
    definitions_dir: Path
    manifest: dict
    project_metadata: dict
    entity_layer: dict
    entities: dict
    relationships: dict
    repository_layer: dict
    service_layer: dict
    controller_layer: dict
    dto_layer: dict
    query_layer: dict | None = None
    filter_layer: dict | None = None
    security_layer: dict | None = None
    config_layer: dict | None = None
    custom_queries_layer: dict | None = None
    group_definition_layer: dict | None = None
    authorization_layer: dict | None = None
    audit_logging_layer: dict | None = None
    exception_layer: dict | None = None
    document_storage_layer: dict | None = None
    ai_layer: dict | None = None


# Required manifest file keys that MUST exist on disk
REQUIRED_FILE_KEYS = [
    "project_metadata",
    "entities",
    "relationships",
    "entity_layer",
    "repository_layer",
    "service_layer",
    "controller_layer",
    "dto_layer",
]

# Optional manifest file keys — set to None if absent
OPTIONAL_FILE_KEYS = [
    "query_layer",
    "filter_layer",
    "security_layer",
    "config_layer",
    "custom_queries_layer",
    "group_definition_layer",
    "authorization_layer",
    "audit_logging_layer",
    "exception_layer",
    "document_storage_layer",
    "ai_layer",
]


def _load_json_file(filepath: Path) -> dict:
    """Load and parse a JSON file.

    Raises:
        FileNotFoundError: if the file does not exist.
        ValueError: if the file contains invalid JSON.
    """
    if not filepath.exists():
        raise FileNotFoundError(f"Required definition file not found: {filepath}")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in definition file: {filepath} — {exc}"
        ) from exc
    except UnicodeDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in definition file: {filepath} — {exc}"
        ) from exc


def _validate_entity_layer(entity_layer: dict, filepath: Path) -> None:
    """Validate entity_layer structure per Requirement 7.6.

    Checks:
    - ``entities`` key exists and is a non-empty list
    - Each entity has ``tableName``, ``className``, and non-empty ``fields``
    - Each field has ``columnName``, ``fieldName``, ``javaType``
    """
    entities = entity_layer.get("entities")
    if not entities or not isinstance(entities, list):
        raise ValueError(
            f"entity_layer must contain a non-empty 'entities' list: {filepath}"
        )

    for idx, entity in enumerate(entities):
        prefix = f"entity_layer.entities[{idx}]"
        for key in ("tableName", "className"):
            if not entity.get(key):
                raise ValueError(f"{prefix} missing required key '{key}': {filepath}")

        fields = entity.get("fields")
        if not fields or not isinstance(fields, list):
            raise ValueError(
                f"{prefix} must have a non-empty 'fields' list: {filepath}"
            )

        for fidx, field in enumerate(fields):
            fprefix = f"{prefix}.fields[{fidx}]"
            for fkey in ("columnName", "fieldName", "javaType"):
                if not field.get(fkey):
                    raise ValueError(
                        f"{fprefix} missing required key '{fkey}': {filepath}"
                    )


def load_all_definitions(definitions_dir: Path) -> DefinitionBundle:
    """Load all definition files from application_definitions/<app_name>/.

    1. Reads ``webflux_manifest.json`` and validates its version.
    2. Loads every required file listed in the manifest (raises on missing).
    3. Loads optional layer files when present (sets ``None`` when absent).
    4. Validates entity_layer structure.

    Args:
        definitions_dir: Path to ``application_definitions/<app_name>/``.

    Returns:
        A fully-populated ``DefinitionBundle``.

    Raises:
        FileNotFoundError: if ``definitions_dir``, the manifest, or any
            required definition file is missing.
        ValueError: if JSON is malformed or the manifest version is
            unsupported.
    """
    definitions_dir = Path(definitions_dir)
    if not definitions_dir.is_dir():
        raise FileNotFoundError(
            f"Definitions directory not found: {definitions_dir}"
        )

    # --- 1. Load and validate manifest ---
    manifest_path = definitions_dir / "webflux_manifest.json"
    manifest = _load_json_file(manifest_path)

    version = manifest.get("version")
    if version not in SUPPORTED_MANIFEST_VERSIONS:
        raise ValueError(
            f"Unsupported manifest version '{version}' in {manifest_path}. "
            f"Supported versions: {SUPPORTED_MANIFEST_VERSIONS}"
        )

    files_map: dict[str, str] = manifest.get("files", {})

    # --- 2. Load required files ---
    required_data: dict[str, dict] = {}
    for key in REQUIRED_FILE_KEYS:
        filename = files_map.get(key)
        if not filename:
            raise ValueError(
                f"Manifest is missing required file entry '{key}': {manifest_path}"
            )
        required_data[key] = _load_json_file(definitions_dir / filename)

    # --- 3. Validate entity_layer ---
    entity_layer_filename = files_map.get("entity_layer", "webflux_entity_layer.json")
    _validate_entity_layer(
        required_data["entity_layer"],
        definitions_dir / entity_layer_filename,
    )

    # --- 4. Load optional files (None if absent) ---
    # Keys whose invalid-JSON errors must propagate (not be silenced).
    _STRICT_OPTIONAL_KEYS = {"document_storage_layer", "ai_layer"}

    optional_data: dict[str, dict | None] = {}
    for key in OPTIONAL_FILE_KEYS:
        filename = files_map.get(key)
        if filename:
            filepath = definitions_dir / filename
            if filepath.exists():
                try:
                    optional_data[key] = _load_json_file(filepath)
                except ValueError:
                    if key in _STRICT_OPTIONAL_KEYS:
                        raise
                    # Corrupt optional file — treat as absent with warning
                    print(f"Warning: skipping corrupt optional file {filepath}")
                    optional_data[key] = None
            else:
                optional_data[key] = None
        else:
            optional_data[key] = None

    # --- 5. Build and return bundle ---
    app_name = definitions_dir.name

    return DefinitionBundle(
        app_name=app_name,
        definitions_dir=definitions_dir,
        manifest=manifest,
        project_metadata=required_data["project_metadata"],
        entity_layer=required_data["entity_layer"],
        entities=required_data["entities"],
        relationships=required_data["relationships"],
        repository_layer=required_data["repository_layer"],
        service_layer=required_data["service_layer"],
        controller_layer=required_data["controller_layer"],
        dto_layer=required_data["dto_layer"],
        query_layer=optional_data.get("query_layer"),
        filter_layer=optional_data.get("filter_layer"),
        security_layer=optional_data.get("security_layer"),
        config_layer=optional_data.get("config_layer"),
        custom_queries_layer=optional_data.get("custom_queries_layer"),
        group_definition_layer=optional_data.get("group_definition_layer"),
        authorization_layer=optional_data.get("authorization_layer"),
        audit_logging_layer=optional_data.get("audit_logging_layer"),
        exception_layer=optional_data.get("exception_layer"),
        document_storage_layer=optional_data.get("document_storage_layer"),
        ai_layer=optional_data.get("ai_layer"),
    )


def reconstruct_database_definition(bundle: DefinitionBundle) -> DatabaseDefinition:
    """Reconstruct DatabaseDefinition from loaded definition files.

    Essentially what load_split_definition() does, but accepts a
    pre-loaded DefinitionBundle instead of reading from disk.

    Args:
        bundle: A fully-populated DefinitionBundle.

    Returns:
        A DatabaseDefinition that passes Pydantic validation and is
        accepted by generate_application().
    """
    tables = []
    for entity in bundle.entities["entities"]:
        entity_relationships = [
            rel for rel in bundle.relationships["relationships"]
            if rel["sourceTable"] == entity["name"]
        ]
        table = {
            "name": entity["name"],
            "columns": entity["columns"],
            "relationships": entity_relationships,
        }
        tables.append(table)

    complete_definition = {
        "projectMetadata": bundle.project_metadata["projectMetadata"],
        "tables": tables,
    }
    return DatabaseDefinition(**complete_definition)
