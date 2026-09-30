"""Property-based tests for DefinitionLoader.

**Validates: Requirement 7.4**
"""

import json
import sys
import tempfile
from pathlib import Path

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

# Ensure swfaw/ is on sys.path so `from version import ...` works
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.definition_loader import (
    DefinitionBundle,
    load_all_definitions,
    OPTIONAL_FILE_KEYS,
)


# ---------------------------------------------------------------------------
# Helpers — build minimal valid definition files
# ---------------------------------------------------------------------------

# Mapping from optional key → filename on disk
OPTIONAL_KEY_TO_FILENAME = {
    "query_layer": "webflux_query_layer.json",
    "filter_layer": "webflux_filter_layer.json",
    "security_layer": "webflux_security_layer.json",
    "config_layer": "webflux_config_layer.json",
    "custom_queries_layer": "webflux_custom_queries_layer.json",
    "group_definition_layer": "webflux_group_definition_layer.json",
    "authorization_layer": "webflux_authorization_layer.json",
    "audit_logging_layer": "webflux_audit_logging_layer.json",
    "exception_layer": "webflux_exception_layer.json",
    "document_storage_layer": "webflux_document_storage_layer.json",
    "ai_layer": "webflux_ai_layer.json",
}


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


def _minimal_manifest(optional_keys_present: set[str] | None = None):
    """Build a manifest with required files and selected optional files."""
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
    if optional_keys_present:
        for key in optional_keys_present:
            files[key] = OPTIONAL_KEY_TO_FILENAME[key]
    return {"version": "2.5", "format": "split", "files": files}


def _write_json(directory: Path, filename: str, data: dict):
    with open(directory / filename, "w", encoding="utf-8") as f:
        json.dump(data, f)


def _setup_app_dir(tmp: Path, optional_keys_present: set[str]) -> Path:
    """Write required definition files + selected optional files."""
    app_dir = tmp / "test_app"
    app_dir.mkdir(parents=True, exist_ok=True)

    _write_json(app_dir, "webflux_manifest.json", _minimal_manifest(optional_keys_present))
    _write_json(app_dir, "webflux_project_metadata.json", {"projectMetadata": {"database": {"name": "test_db"}}})
    _write_json(app_dir, "webflux_entity_layer.json", _minimal_entity_layer())
    _write_json(app_dir, "webflux_entities.json", {"entities": [{"name": "users", "columns": []}]})
    _write_json(app_dir, "webflux_relationships.json", {"relationships": []})
    _write_json(app_dir, "webflux_repository_layer.json", {"repositories": []})
    _write_json(app_dir, "webflux_service_layer.json", {"services": []})
    _write_json(app_dir, "webflux_controller_layer.json", {"controllers": []})
    _write_json(app_dir, "webflux_dto_layer.json", {"dtos": []})

    # Write the selected optional layer files
    for key in optional_keys_present:
        filename = OPTIONAL_KEY_TO_FILENAME[key]
        _write_json(app_dir, filename, {key: "test_data"})

    return app_dir


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Generate a random subset of optional layer keys
_optional_subset_st = st.frozensets(
    st.sampled_from(OPTIONAL_FILE_KEYS),
    min_size=0,
    max_size=len(OPTIONAL_FILE_KEYS),
)


# ---------------------------------------------------------------------------
# Property 21: Optional layer handling
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(present_keys=_optional_subset_st)
def test_optional_layer_handling(present_keys: frozenset[str]) -> None:
    """Property 21: Optional layer handling

    For any combination of present/absent optional Layer_Files,
    DefinitionLoader sets corresponding DefinitionBundle fields to None
    for absent files without error.

    **Validates: Requirement 7.4**
    """
    with tempfile.TemporaryDirectory() as tmp:
        app_dir = _setup_app_dir(Path(tmp), set(present_keys))
        bundle = load_all_definitions(app_dir)

        # Verify: present optional layers are loaded (not None)
        for key in present_keys:
            value = getattr(bundle, key)
            assert value is not None, (
                f"Optional layer '{key}' was present on disk but "
                f"DefinitionBundle.{key} is None"
            )

        # Verify: absent optional layers are None
        absent_keys = set(OPTIONAL_FILE_KEYS) - set(present_keys)
        for key in absent_keys:
            value = getattr(bundle, key)
            assert value is None, (
                f"Optional layer '{key}' was absent on disk but "
                f"DefinitionBundle.{key} is {value!r} (expected None)"
            )

        # Verify: required fields are always loaded regardless of optional layers
        assert bundle.app_name == "test_app"
        assert bundle.manifest is not None
        assert bundle.project_metadata is not None
        assert bundle.entity_layer is not None
        assert bundle.entities is not None
        assert bundle.relationships is not None
        assert bundle.repository_layer is not None
        assert bundle.service_layer is not None
        assert bundle.controller_layer is not None
        assert bundle.dto_layer is not None


# ---------------------------------------------------------------------------
# Property 2: Invalid JSON raises ValueError
# ---------------------------------------------------------------------------


def _is_valid_json_text(text: str) -> bool:
    """Return True if text is valid JSON."""
    try:
        json.loads(text)
        return True
    except (json.JSONDecodeError, ValueError):
        return False


@settings(max_examples=20)
@given(bad_content=st.text(min_size=1, max_size=200))
def test_invalid_json_raises_value_error(bad_content: str) -> None:
    """Property 2: Invalid JSON raises ValueError

    For any text string that is not valid JSON, passing it as content of
    webflux_document_storage_layer.json raises ValueError with file path
    in message.

    **Validates: Requirements 1.6**
    """
    assume(not _is_valid_json_text(bad_content))

    with tempfile.TemporaryDirectory() as tmp:
        # Set up app dir with document_storage_layer in manifest
        app_dir = _setup_app_dir(Path(tmp), {"document_storage_layer"})

        # Overwrite the document_storage_layer file with invalid JSON content
        dsl_path = app_dir / "webflux_document_storage_layer.json"
        with open(dsl_path, "w", encoding="utf-8") as f:
            f.write(bad_content)

        with pytest.raises(ValueError) as exc_info:
            load_all_definitions(app_dir)

        # Error message must contain the file path
        assert str(dsl_path) in str(exc_info.value), (
            f"ValueError message does not contain file path.\n"
            f"  Expected path: {dsl_path}\n"
            f"  Actual message: {exc_info.value}"
        )


from utils.definition_loader import reconstruct_database_definition
from models.database_definition import DatabaseDefinition


# ---------------------------------------------------------------------------
# Strategies for Property 19
# ---------------------------------------------------------------------------

# Valid SQL column types for generated columns
_sql_types = st.sampled_from([
    "BIGINT UNSIGNED", "INT", "VARCHAR(255)", "BOOLEAN", "DATE",
    "TIMESTAMP", "DECIMAL(19,4)", "TEXT", "BLOB",
])

# Column strategy: each column has name, type, primaryKey, nullable
_column_st = st.fixed_dictionaries({
    "name": st.from_regex(r"[a-z][a-z0-9_]{0,19}", fullmatch=True),
    "type": _sql_types,
    "primaryKey": st.booleans(),
    "nullable": st.booleans(),
})

# Entity strategy: name + at least one column
_entity_st = st.fixed_dictionaries({
    "name": st.from_regex(r"[a-z][a-z0-9_]{0,19}", fullmatch=True),
    "columns": st.lists(_column_st, min_size=1, max_size=5),
})

# List of entities with unique names
_entities_list_st = st.lists(
    _entity_st, min_size=1, max_size=5
).filter(lambda ents: len({e["name"] for e in ents}) == len(ents))

# Valid project metadata dict that passes Pydantic validation
_project_metadata_st = st.fixed_dictionaries({
    "projectMetadata": st.fixed_dictionaries({
        "name": st.from_regex(r"[a-z][a-z0-9_]{0,9}", fullmatch=True),
        "applicationName": st.from_regex(r"[A-Z][a-zA-Z0-9]{0,9}", fullmatch=True),
        "groupId": st.just("com.example"),
        "artifactId": st.from_regex(r"[a-z][a-z0-9-]{0,9}", fullmatch=True),
        "version": st.just("1.0.0"),
        "port": st.integers(min_value=1024, max_value=65535),
        "database": st.fixed_dictionaries({
            "type": st.just("mysql"),
            "host": st.just("localhost"),
            "port": st.just(3306),
            "name": st.from_regex(r"[a-z][a-z0-9_]{0,9}", fullmatch=True),
            "username": st.just("root"),
            "password": st.just("password"),
        }),
    }),
})


# ---------------------------------------------------------------------------
# Property 19: DefinitionBundle reconstruction correctness
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(entities=_entities_list_st, proj_meta=_project_metadata_st)
def test_definition_bundle_reconstruction_correctness(
    entities: list[dict], proj_meta: dict
) -> None:
    """Property 19: DefinitionBundle reconstruction correctness

    For any valid DefinitionBundle, reconstruct_database_definition()
    produces a DatabaseDefinition that passes Pydantic validation and
    has the same table count as entities.

    **Validates: Requirements 11.2, 11.3**
    """
    # Build a DefinitionBundle in-memory (no disk I/O)
    bundle = DefinitionBundle(
        app_name="test_app",
        definitions_dir=Path("/tmp/fake"),
        manifest={"version": "2.5", "format": "split", "files": {}},
        project_metadata=proj_meta,
        entity_layer={"entities": []},
        entities={"entities": entities},
        relationships={"relationships": []},
        repository_layer={"repositories": []},
        service_layer={"services": []},
        controller_layer={"controllers": []},
        dto_layer={"dtos": []},
    )

    # Reconstruct — should not raise
    db_def = reconstruct_database_definition(bundle)

    # Property: result is a valid DatabaseDefinition (Pydantic validated)
    assert isinstance(db_def, DatabaseDefinition)

    # Property: table count matches entity count
    assert len(db_def.tables) == len(entities), (
        f"Expected {len(entities)} tables but got {len(db_def.tables)}"
    )


# ---------------------------------------------------------------------------
# Strategies for Property 4: document_storage_layer round-trip
# ---------------------------------------------------------------------------

# fileStorage section strategy
_file_storage_st = st.fixed_dictionaries({
    "enabled": st.booleans(),
    "provider": st.sampled_from(["local", "s3"]),
    "localBasePath": st.from_regex(r"\./[a-z]{1,10}", fullmatch=True),
    "maxFileSizeMb": st.integers(min_value=1, max_value=500),
    "allowedContentTypes": st.lists(
        st.sampled_from([
            "image/png", "image/jpeg", "application/pdf",
            "text/plain", "application/json",
        ]),
        min_size=0,
        max_size=3,
    ),
})

# jsonColumns entry strategy
_json_column_entry_st = st.fixed_dictionaries({
    "entityName": st.from_regex(r"[A-Z][a-zA-Z]{0,9}", fullmatch=True),
    "columnName": st.from_regex(r"[a-z][a-z_]{0,9}", fullmatch=True),
    "fieldName": st.from_regex(r"[a-z][a-zA-Z]{0,9}", fullmatch=True),
})

# documentCollections entry strategy
_doc_collection_entry_st = st.fixed_dictionaries({
    "name": st.from_regex(r"[A-Z][a-zA-Z]{0,9}", fullmatch=True),
    "tableName": st.from_regex(r"[a-z][a-z_]{0,14}", fullmatch=True),
    "description": st.text(min_size=0, max_size=30, alphabet=st.characters(
        whitelist_categories=("L", "N", "Z"),
    )),
})

# entityAttachments entry strategy
_entity_attachment_entry_st = st.fixed_dictionaries({
    "entityName": st.from_regex(r"[A-Z][a-zA-Z]{0,9}", fullmatch=True),
    "foreignKeyColumn": st.from_regex(r"[a-z][a-z_]{0,14}_id", fullmatch=True),
})

# Full document_storage_layer dict strategy
_document_storage_layer_st = st.fixed_dictionaries({
    "fileStorage": _file_storage_st,
    "jsonColumns": st.lists(_json_column_entry_st, min_size=0, max_size=3),
    "documentCollections": st.lists(_doc_collection_entry_st, min_size=0, max_size=3),
    "entityAttachments": st.lists(_entity_attachment_entry_st, min_size=0, max_size=3),
})


# ---------------------------------------------------------------------------
# Property 4: Definition loader round-trip for document_storage_layer
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(dsl_dict=_document_storage_layer_st)
def test_document_storage_layer_round_trip(dsl_dict: dict) -> None:
    """Property 4: Definition loader round-trip for document_storage_layer

    For any valid document storage layer dict, writing it to
    webflux_document_storage_layer.json, adding the manifest reference,
    and loading via load_all_definitions() produces a DefinitionBundle
    whose document_storage_layer attribute equals the original dict.

    **Validates: Requirements 2.1, 2.3, 2.4**
    """
    with tempfile.TemporaryDirectory() as tmp:
        # Set up app dir WITH document_storage_layer in manifest
        app_dir = _setup_app_dir(Path(tmp), {"document_storage_layer"})

        # Overwrite the document_storage_layer file with our generated dict
        _write_json(app_dir, "webflux_document_storage_layer.json", dsl_dict)

        # Load via the real loader
        bundle = load_all_definitions(app_dir)

        # Round-trip: loaded dict must equal original
        assert bundle.document_storage_layer == dsl_dict, (
            f"Round-trip mismatch.\n"
            f"  Original: {dsl_dict!r}\n"
            f"  Loaded:   {bundle.document_storage_layer!r}"
        )


@settings(max_examples=20)
@given(present_keys=st.frozensets(
    st.sampled_from([k for k in OPTIONAL_FILE_KEYS if k != "document_storage_layer"]),
    min_size=0,
    max_size=len(OPTIONAL_FILE_KEYS) - 1,
))
def test_document_storage_layer_absent_is_none(present_keys: frozenset[str]) -> None:
    """Property 4 (absent case): When document_storage_layer file is absent,
    bundle.document_storage_layer is None.

    **Validates: Requirements 2.4**
    """
    with tempfile.TemporaryDirectory() as tmp:
        # Set up app dir WITHOUT document_storage_layer
        app_dir = _setup_app_dir(Path(tmp), set(present_keys))

        bundle = load_all_definitions(app_dir)

        assert bundle.document_storage_layer is None, (
            f"Expected document_storage_layer to be None when file is absent, "
            f"but got {bundle.document_storage_layer!r}"
        )
