"""Property-based tests for Scaffolder completeness.

**Validates: Requirements 1.2, 1.4, 2.1, 2.4, 2.6**
"""

import json
import os
import tempfile
from pathlib import Path

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from app_def_manager.scaffolder import Scaffolder, DEFINITION_FILES


# --- Strategies ---

# Valid Java types the scaffolder knows about
_java_types = st.sampled_from([
    "Long", "Integer", "Short", "Byte", "String", "Boolean",
    "LocalDate", "LocalDateTime", "LocalTime", "BigDecimal",
    "Float", "Double", "UUID",
])

# Field name: PascalCase or camelCase identifiers
_field_name_st = st.from_regex(r"[a-z][a-zA-Z]{0,12}", fullmatch=True)

# Entity name: PascalCase identifiers
_entity_name_st = st.from_regex(r"[A-Z][a-zA-Z]{1,12}", fullmatch=True)

# App name: lowercase with underscores
_app_name_st = st.from_regex(r"[a-z][a-z0-9_]{1,15}", fullmatch=True)

# A single field description
_field_st = st.fixed_dictionaries({
    "name": _field_name_st,
    "type": _java_types,
})

# A single entity description with 1-4 unique fields
_entity_st = st.fixed_dictionaries({
    "name": _entity_name_st,
    "fields": st.lists(_field_st, min_size=1, max_size=4, unique_by=lambda f: f["name"]),
})

# Non-empty list of entity descriptions with unique names (1-3 entities)
_entity_descriptions_st = st.lists(
    _entity_st, min_size=1, max_size=3, unique_by=lambda e: e["name"]
)


# The 10 required files (9 definition + _generation_status.json)
REQUIRED_FILES = DEFINITION_FILES + ["_generation_status.json"]

# The 6 layer files where every entity must appear
LAYER_FILES_WITH_ENTITIES = [
    "webflux_entity_layer.json",
    "webflux_entities.json",
    "webflux_repository_layer.json",
    "webflux_service_layer.json",
    "webflux_controller_layer.json",
    "webflux_dto_layer.json",
]


# --- Property 6: Scaffold completeness ---


@settings(max_examples=20)
@given(app_name=_app_name_st, entity_descriptions=_entity_descriptions_st)
def test_scaffold_completeness(app_name: str, entity_descriptions: list[dict]) -> None:
    """Property 6: Scaffold completeness

    For any app name and non-empty entity descriptions, scaffold_application()
    creates all 10 required files, every entity appears in all 6 layer files
    with Input/Output/Filter DTOs, and all files are marked dirty.

    **Validates: Requirements 1.2, 1.4, 2.1, 2.4, 2.6**
    """
    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp)

            scaffolder = Scaffolder()
            result_dir = scaffolder.scaffold_application(
                app_name, entity_descriptions, force=True
            )

            entity_names = [e["name"] for e in entity_descriptions]

            # --- 1. All 10 required files exist (Req 1.2, 1.4) ---
            for fname in REQUIRED_FILES:
                assert (result_dir / fname).exists(), (
                    f"Missing required file: {fname}"
                )

            # --- 2. Every entity appears in all 6 layer files (Req 2.1, 2.6) ---

            # entity_layer: check className
            with open(result_dir / "webflux_entity_layer.json") as f:
                entity_layer = json.load(f)
            el_names = {e["className"] for e in entity_layer["entities"]}
            assert set(entity_names) == el_names

            # entities: check name (snake_case table name)
            with open(result_dir / "webflux_entities.json") as f:
                entities = json.load(f)
            # Each entity should have an entry
            assert len(entities["entities"]) == len(entity_names)

            # repository_layer: check entityName
            with open(result_dir / "webflux_repository_layer.json") as f:
                repo_layer = json.load(f)
            repo_names = {r["entityName"] for r in repo_layer["repositories"]}
            assert set(entity_names) == repo_names

            # service_layer: check entityName
            with open(result_dir / "webflux_service_layer.json") as f:
                svc_layer = json.load(f)
            svc_names = {s["entityName"] for s in svc_layer["services"]}
            assert set(entity_names) == svc_names

            # controller_layer: check entityName
            with open(result_dir / "webflux_controller_layer.json") as f:
                ctrl_layer = json.load(f)
            ctrl_names = {c["entityName"] for c in ctrl_layer["controllers"]}
            assert set(entity_names) == ctrl_names

            # dto_layer: check Input/Output/Filter DTOs per entity (Req 2.6)
            with open(result_dir / "webflux_dto_layer.json") as f:
                dto_layer = json.load(f)
            dto_entries = {
                (d["entityName"], d["dtoType"]) for d in dto_layer["dtos"]
            }
            for ename in entity_names:
                for dtype in ("Input", "Output", "Filter"):
                    assert (ename, dtype) in dto_entries, (
                        f"Missing DTO: entity={ename}, type={dtype}"
                    )

            # --- 3. All 9 definition files are marked dirty (Req 2.4) ---
            with open(result_dir / "_generation_status.json") as f:
                status = json.load(f)
            for def_file in DEFINITION_FILES:
                assert def_file in status["files"], (
                    f"File {def_file} not tracked in _generation_status.json"
                )
                assert status["files"][def_file]["status"] == "dirty", (
                    f"File {def_file} should be dirty, got "
                    f"{status['files'][def_file]['status']}"
                )

        finally:
            os.chdir(original_cwd)

# --- Property 7: Scaffold auto-generated fields ---


@settings(max_examples=20)
@given(entity_descriptions=_entity_descriptions_st)
def test_scaffold_auto_generated_fields(entity_descriptions: list[dict]) -> None:
    """Property 7: Scaffold auto-generated fields

    For any entity description, the generated entity_layer entry contains
    id primary key, created_at, and updated_at fields plus
    all user-specified fields.

    **Validates: Requirement 2.2**
    """
    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp)

            scaffolder = Scaffolder()
            result_dir = scaffolder.scaffold_application(
                "test_app", entity_descriptions, force=True
            )

            with open(result_dir / "webflux_entity_layer.json") as f:
                entity_layer = json.load(f)

            for desc, entity_def in zip(entity_descriptions, entity_layer["entities"]):
                field_names = {f["columnName"] for f in entity_def["fields"]}
                field_map = {f["columnName"]: f for f in entity_def["fields"]}

                # Auto-generated id field (primary key)
                table_name = entity_def["tableName"]
                pk_col = f"{table_name}_id"
                assert pk_col in field_names, f"Missing auto-generated id field: {pk_col}"
                assert field_map[pk_col]["isPrimaryKey"] is True
                assert field_map[pk_col]["isNullable"] is False

                # Auto-generated audit fields
                assert "created_at" in field_names, "Missing created_at"
                assert "updated_at" in field_names, "Missing updated_at"

                # All user-specified fields present
                for user_field in desc["fields"]:
                    from app_def_manager.scaffolder import _to_snake_case
                    expected_col = _to_snake_case(user_field["name"])
                    assert expected_col in field_names, (
                        f"User field '{user_field['name']}' (column '{expected_col}') "
                        f"not found in entity_layer fields"
                    )

        finally:
            os.chdir(original_cwd)


# --- Property 8: Scaffold naming conventions ---


@settings(max_examples=20)
@given(entity_descriptions=_entity_descriptions_st)
def test_scaffold_naming_conventions(entity_descriptions: list[dict]) -> None:
    """Property 8: Scaffold naming conventions

    For any entity name and field name, tableName is snake_case of entity
    name, columnName is snake_case of field name.

    **Validates: Requirement 2.3**
    """
    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp)

            scaffolder = Scaffolder()
            result_dir = scaffolder.scaffold_application(
                "test_app", entity_descriptions, force=True
            )

            with open(result_dir / "webflux_entity_layer.json") as f:
                entity_layer = json.load(f)

            from app_def_manager.scaffolder import _to_snake_case

            for desc, entity_def in zip(entity_descriptions, entity_layer["entities"]):
                # tableName is snake_case of entity name
                expected_table = _to_snake_case(desc["name"])
                assert entity_def["tableName"] == expected_table, (
                    f"Entity '{desc['name']}': expected tableName='{expected_table}', "
                    f"got '{entity_def['tableName']}'"
                )

                # User field columnNames are snake_case of field names
                # Skip auto-generated fields (id, created_at, updated_at, is_deleted)
                auto_cols = {f"{expected_table}_id", "created_at", "updated_at"}
                user_fields_map = {
                    f["columnName"]: f for f in entity_def["fields"]
                    if f["columnName"] not in auto_cols
                }

                for user_field in desc["fields"]:
                    expected_col = _to_snake_case(user_field["name"])
                    assert expected_col in user_fields_map, (
                        f"Field '{user_field['name']}': expected columnName='{expected_col}' "
                        f"not found in entity fields"
                    )

        finally:
            os.chdir(original_cwd)


# --- Property 13: Scaffolder creates document storage layer with correct defaults ---


@settings(max_examples=20)
@given(app_name=_app_name_st, entity_descriptions=_entity_descriptions_st)
def test_scaffold_document_storage_layer_defaults(app_name: str, entity_descriptions: list[dict]) -> None:
    """Property 13: Scaffolder creates document storage layer with correct defaults

    For any scaffolded application, output directory contains
    webflux_document_storage_layer.json with fileStorage.enabled=false,
    empty jsonColumns, empty documentCollections, empty entityAttachments,
    and manifest contains document_storage_layer key.

    **Validates: Requirements 8.1, 8.2**
    """
    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp)

            scaffolder = Scaffolder()
            result_dir = scaffolder.scaffold_application(
                app_name, entity_descriptions, force=True
            )

            # --- 1. webflux_document_storage_layer.json exists ---
            dsl_path = result_dir / "webflux_document_storage_layer.json"
            assert dsl_path.exists(), "Missing webflux_document_storage_layer.json"

            # --- 2. Verify default contents ---
            with open(dsl_path) as f:
                dsl = json.load(f)

            assert dsl["fileStorage"]["enabled"] is False, (
                f"Expected fileStorage.enabled=false, got {dsl['fileStorage']['enabled']}"
            )
            assert dsl["jsonColumns"] == [], (
                f"Expected empty jsonColumns, got {dsl['jsonColumns']}"
            )
            assert dsl["documentCollections"] == [], (
                f"Expected empty documentCollections, got {dsl['documentCollections']}"
            )
            assert dsl["entityAttachments"] == [], (
                f"Expected empty entityAttachments, got {dsl['entityAttachments']}"
            )

            # --- 3. Manifest contains document_storage_layer key ---
            with open(result_dir / "webflux_manifest.json") as f:
                manifest = json.load(f)

            assert "document_storage_layer" in manifest["files"], (
                "Manifest files map missing 'document_storage_layer' key"
            )
            assert manifest["files"]["document_storage_layer"] == "webflux_document_storage_layer.json", (
                f"Expected manifest document_storage_layer to reference "
                f"'webflux_document_storage_layer.json', got "
                f"'{manifest['files']['document_storage_layer']}'"
            )

        finally:
            os.chdir(original_cwd)
