"""Property-based tests for CRUDManager.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 9.1, 9.2, 9.3, 9.4, 9.5**
"""

import json
import os
import tempfile
from pathlib import Path

from hypothesis import given, settings, assume
from hypothesis import strategies as st

from app_def_manager.scaffolder import Scaffolder, _to_snake_case, _to_camel_case
from app_def_manager.crud import CRUDManager, ENTITY_LAYER_FILES, FIELD_LAYER_FILES


# --- Strategies ---

_java_types = st.sampled_from([
    "Long", "Integer", "String", "Boolean", "LocalDate", "LocalDateTime",
    "BigDecimal", "Double",
])

_field_name_st = st.from_regex(r"[a-z][a-zA-Z]{1,10}", fullmatch=True)
_entity_name_st = st.from_regex(r"[A-Z][a-zA-Z]{2,10}", fullmatch=True)

_field_st = st.fixed_dictionaries({
    "name": _field_name_st,
    "type": _java_types,
})

_entity_st = st.fixed_dictionaries({
    "name": _entity_name_st,
    "fields": st.lists(_field_st, min_size=1, max_size=3, unique_by=lambda f: f["name"]),
})

# Initial entities for scaffolding (1-2 entities)
_initial_entities_st = st.lists(
    _entity_st, min_size=1, max_size=2, unique_by=lambda e: e["name"]
)

# New entity to add (must have a different name from initial)
_new_entity_st = _entity_st


def _scaffold_app(tmp_dir: str, app_name: str, entities: list[dict]) -> Path:
    """Scaffold an app in a temp directory and return the app_dir."""
    os.chdir(tmp_dir)
    scaffolder = Scaffolder()
    return scaffolder.scaffold_application(app_name, entities, force=True)


def _load_json(app_dir: Path, filename: str) -> dict:
    with open(app_dir / filename, "r", encoding="utf-8") as f:
        return json.load(f)


# --- Property 9: CRUD add/remove entity cross-layer consistency ---


@settings(max_examples=20)
@given(
    initial_entities=_initial_entities_st,
    new_entity=_new_entity_st,
)
def test_crud_add_remove_entity_cross_layer_consistency(
    initial_entities: list[dict], new_entity: dict
) -> None:
    """Property 9: CRUD add/remove entity cross-layer consistency

    After add_entity(), entity exists in all 6 layer files with standard
    CRUD entries; after remove_entity(), entity is absent from all 6 files.

    **Validates: Requirements 3.1, 3.2, 9.1, 9.2, 9.5**
    """
    # Ensure new entity name doesn't collide with initial entities
    existing_names = {e["name"] for e in initial_entities}
    assume(new_entity["name"] not in existing_names)

    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            app_dir = _scaffold_app(tmp, "test_app", initial_entities)
            crud = CRUDManager("test_app")
            new_name = new_entity["name"]
            new_table = _to_snake_case(new_name)

            # --- ADD entity ---
            dirty = crud.add_entity(new_name, new_entity["fields"])
            assert set(dirty) == set(ENTITY_LAYER_FILES)

            # Verify entity_layer
            el = _load_json(app_dir, "webflux_entity_layer.json")
            el_names = {e["className"] for e in el["entities"]}
            assert new_name in el_names

            # Verify entities
            ent = _load_json(app_dir, "webflux_entities.json")
            ent_names = {e["name"] for e in ent["entities"]}
            assert new_table in ent_names

            # Verify repository_layer
            repo = _load_json(app_dir, "webflux_repository_layer.json")
            repo_names = {r["entityName"] for r in repo["repositories"]}
            assert new_name in repo_names

            # Verify service_layer
            svc = _load_json(app_dir, "webflux_service_layer.json")
            svc_names = {s["entityName"] for s in svc["services"]}
            assert new_name in svc_names

            # Verify controller_layer
            ctrl = _load_json(app_dir, "webflux_controller_layer.json")
            ctrl_names = {c["entityName"] for c in ctrl["controllers"]}
            assert new_name in ctrl_names

            # Verify dto_layer (Input, Output, Filter)
            dto = _load_json(app_dir, "webflux_dto_layer.json")
            dto_entries = {(d["entityName"], d["dtoType"]) for d in dto["dtos"]}
            for dtype in ("Input", "Output", "Filter"):
                assert (new_name, dtype) in dto_entries

            # --- REMOVE entity ---
            dirty = crud.remove_entity(new_name)
            assert set(dirty) == set(ENTITY_LAYER_FILES)

            # Verify entity is gone from all layers
            el = _load_json(app_dir, "webflux_entity_layer.json")
            assert new_name not in {e["className"] for e in el["entities"]}

            ent = _load_json(app_dir, "webflux_entities.json")
            assert new_table not in {e["name"] for e in ent["entities"]}

            repo = _load_json(app_dir, "webflux_repository_layer.json")
            assert new_name not in {r["entityName"] for r in repo["repositories"]}

            svc = _load_json(app_dir, "webflux_service_layer.json")
            assert new_name not in {s["entityName"] for s in svc["services"]}

            ctrl = _load_json(app_dir, "webflux_controller_layer.json")
            assert new_name not in {c["entityName"] for c in ctrl["controllers"]}

            dto = _load_json(app_dir, "webflux_dto_layer.json")
            assert new_name not in {d["entityName"] for d in dto["dtos"]}

            # Original entities still intact
            for orig in initial_entities:
                assert orig["name"] in {e["className"] for e in el["entities"]}

        finally:
            os.chdir(original_cwd)


# --- Property 10: CRUD field operations cross-layer consistency ---


@settings(max_examples=20)
@given(
    initial_entities=_initial_entities_st,
    new_field=_field_st,
)
def test_crud_field_operations_cross_layer_consistency(
    initial_entities: list[dict], new_field: dict
) -> None:
    """Property 10: CRUD field operations cross-layer consistency

    After add_field(), field appears in entity_layer, entities, dto_layer;
    after remove_field(), field is absent from all 3; after modify_field(),
    updated properties reflected in all 3.

    **Validates: Requirements 3.3, 3.4, 3.5, 9.3**
    """
    # Ensure new field name doesn't collide with existing fields
    target_entity = initial_entities[0]
    existing_field_names = {f["name"] for f in target_entity["fields"]}
    assume(new_field["name"] not in existing_field_names)
    # Avoid collision with auto-generated field names
    assume(new_field["name"] not in ("id", "createdAt", "updatedAt", "isDeleted"))

    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            app_dir = _scaffold_app(tmp, "test_app", initial_entities)
            crud = CRUDManager("test_app")
            entity_name = target_entity["name"]
            table_name = _to_snake_case(entity_name)
            col_name = _to_snake_case(new_field["name"])
            camel_name = _to_camel_case(new_field["name"])

            # --- ADD field ---
            dirty = crud.add_field(entity_name, new_field)
            assert set(dirty) == set(FIELD_LAYER_FILES)

            # Verify entity_layer
            el = _load_json(app_dir, "webflux_entity_layer.json")
            entity_def = next(e for e in el["entities"] if e["className"] == entity_name)
            el_cols = {f["columnName"] for f in entity_def["fields"]}
            assert col_name in el_cols

            # Verify entities
            ent = _load_json(app_dir, "webflux_entities.json")
            ent_def = next(e for e in ent["entities"] if e["name"] == table_name)
            ent_cols = {c["name"] for c in ent_def["columns"]}
            assert col_name in ent_cols

            # Verify dto_layer
            dto = _load_json(app_dir, "webflux_dto_layer.json")
            for dtype in ("Input", "Output", "Filter"):
                dto_def = next(
                    d for d in dto["dtos"]
                    if d["entityName"] == entity_name and d["dtoType"] == dtype
                )
                dto_fields = {f["fieldName"] for f in dto_def["fields"]}
                assert camel_name in dto_fields, f"Field missing from {dtype} DTO"

            # --- REMOVE field ---
            dirty = crud.remove_field(entity_name, new_field["name"])
            assert set(dirty) == set(FIELD_LAYER_FILES)

            el = _load_json(app_dir, "webflux_entity_layer.json")
            entity_def = next(e for e in el["entities"] if e["className"] == entity_name)
            assert col_name not in {f["columnName"] for f in entity_def["fields"]}

            ent = _load_json(app_dir, "webflux_entities.json")
            ent_def = next(e for e in ent["entities"] if e["name"] == table_name)
            assert col_name not in {c["name"] for c in ent_def["columns"]}

            dto = _load_json(app_dir, "webflux_dto_layer.json")
            for dtype in ("Input", "Output", "Filter"):
                dto_def = next(
                    d for d in dto["dtos"]
                    if d["entityName"] == entity_name and d["dtoType"] == dtype
                )
                assert camel_name not in {f["fieldName"] for f in dto_def["fields"]}

        finally:
            os.chdir(original_cwd)


# --- Property 18: CRUD mutation return value accuracy ---


@settings(max_examples=20)
@given(
    initial_entities=_initial_entities_st,
    new_entity=_new_entity_st,
)
def test_crud_mutation_return_value_accuracy(
    initial_entities: list[dict], new_entity: dict
) -> None:
    """Property 18: CRUD mutation return value accuracy

    For any CRUDManager mutation, the returned list of dirty filenames
    exactly matches the set of files actually modified on disk.

    **Validates: Requirement 9.4**
    """
    existing_names = {e["name"] for e in initial_entities}
    assume(new_entity["name"] not in existing_names)

    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            app_dir = _scaffold_app(tmp, "test_app", initial_entities)

            # Snapshot file contents before mutation
            before = {}
            for fname in ENTITY_LAYER_FILES:
                with open(app_dir / fname, "r", encoding="utf-8") as f:
                    before[fname] = f.read()

            crud = CRUDManager("test_app")
            dirty = crud.add_entity(new_entity["name"], new_entity["fields"])

            # Check which files actually changed
            actually_changed = set()
            for fname in ENTITY_LAYER_FILES:
                with open(app_dir / fname, "r", encoding="utf-8") as f:
                    after = f.read()
                if after != before[fname]:
                    actually_changed.add(fname)

            # Property: returned dirty list matches actually changed files
            assert set(dirty) == actually_changed, (
                f"Returned dirty={set(dirty)}, actually changed={actually_changed}"
            )

        finally:
            os.chdir(original_cwd)


# --- Property 14: CRUDManager JSON column add/remove round-trip ---


@settings(max_examples=20)
@given(
    initial_entities=_initial_entities_st,
    entity_name=_entity_name_st,
    column_name=_field_name_st,
    field_name=_field_name_st,
)
def test_crud_json_column_add_remove_round_trip(
    initial_entities: list[dict],
    entity_name: str,
    column_name: str,
    field_name: str,
) -> None:
    """Property 14: CRUDManager JSON column add/remove round-trip

    For any valid entity name E, column name C, field name F, calling
    add_json_column(E, C, F) then remove_json_column(E, F) leaves
    jsonColumns in original state. After add, array contains matching
    entry and file is marked dirty.

    **Validates: Requirements 8.3, 8.4**
    """
    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            app_dir = _scaffold_app(tmp, "test_app", initial_entities)
            crud = CRUDManager("test_app")

            # Snapshot original jsonColumns
            dsl_before = _load_json(app_dir, "webflux_document_storage_layer.json")
            original_json_columns = dsl_before["jsonColumns"].copy()

            # --- ADD json column ---
            dirty = crud.add_json_column(entity_name, column_name, field_name)
            assert "webflux_document_storage_layer.json" in dirty

            # Verify entry exists after add
            dsl_after_add = _load_json(app_dir, "webflux_document_storage_layer.json")
            matching = [
                jc for jc in dsl_after_add["jsonColumns"]
                if jc["entityName"] == entity_name
                and jc["columnName"] == column_name
                and jc["fieldName"] == field_name
            ]
            assert len(matching) == 1, f"Expected 1 matching entry, got {len(matching)}"

            # --- REMOVE json column ---
            dirty = crud.remove_json_column(entity_name, field_name)
            assert "webflux_document_storage_layer.json" in dirty

            # Verify jsonColumns is back to original state
            dsl_after_remove = _load_json(app_dir, "webflux_document_storage_layer.json")
            assert dsl_after_remove["jsonColumns"] == original_json_columns

        finally:
            os.chdir(original_cwd)


# --- Property 15: CRUDManager document collection add/remove round-trip ---


@settings(max_examples=20)
@given(
    initial_entities=_initial_entities_st,
    collection_name=_entity_name_st,
    table_name=_field_name_st,
    description=st.text(min_size=0, max_size=50),
)
def test_crud_document_collection_add_remove_round_trip(
    initial_entities: list[dict],
    collection_name: str,
    table_name: str,
    description: str,
) -> None:
    """Property 15: CRUDManager document collection add/remove round-trip

    For any valid collection name N, table name T, description D, calling
    add_document_collection(N, T, D) then remove_document_collection(N)
    leaves documentCollections in original state. After add, array contains
    matching entry and file is marked dirty.

    **Validates: Requirements 8.5, 8.6**
    """
    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            app_dir = _scaffold_app(tmp, "test_app", initial_entities)
            crud = CRUDManager("test_app")

            # Snapshot original documentCollections
            dsl_before = _load_json(app_dir, "webflux_document_storage_layer.json")
            original_collections = dsl_before["documentCollections"].copy()

            # --- ADD document collection ---
            dirty = crud.add_document_collection(collection_name, table_name, description)
            assert "webflux_document_storage_layer.json" in dirty

            # Verify entry exists after add
            dsl_after_add = _load_json(app_dir, "webflux_document_storage_layer.json")
            matching = [
                dc for dc in dsl_after_add["documentCollections"]
                if dc["name"] == collection_name
                and dc["tableName"] == table_name
                and dc["description"] == description
            ]
            assert len(matching) == 1, f"Expected 1 matching entry, got {len(matching)}"

            # --- REMOVE document collection ---
            dirty = crud.remove_document_collection(collection_name)
            assert "webflux_document_storage_layer.json" in dirty

            # Verify documentCollections is back to original state
            dsl_after_remove = _load_json(app_dir, "webflux_document_storage_layer.json")
            assert dsl_after_remove["documentCollections"] == original_collections

        finally:
            os.chdir(original_cwd)


# --- Property 24: fieldWidget property preservation ---

_field_widget_st = st.sampled_from(["text", "richText", "codeEditor", "markdown", "json"])
_language_st = st.sampled_from(["java", "python", "sql", "javascript", "typescript", "go", "rust"])


@settings(max_examples=20)
@given(
    initial_entities=_initial_entities_st,
    new_field=_field_st,
    field_widget=_field_widget_st,
    language=_language_st,
)
def test_field_widget_property_preservation(
    initial_entities: list[dict],
    new_field: dict,
    field_widget: str,
    language: str,
) -> None:
    """Property 24: fieldWidget property preservation

    For any DTO field with fieldWidget in {"text", "richText", "codeEditor",
    "markdown", "json"}, value is preserved through add_field(), modify_field(),
    and definition file round-trip. When absent, defaults to "text". When
    "codeEditor", optional language property is also preserved.

    **Validates: Requirements 15.1, 15.8, 15.9, 15.10**
    """
    target_entity = initial_entities[0]
    existing_field_names = {f["name"] for f in target_entity["fields"]}
    assume(new_field["name"] not in existing_field_names)
    assume(new_field["name"] not in ("id", "createdAt", "updatedAt", "isDeleted"))

    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            app_dir = _scaffold_app(tmp, "test_app", initial_entities)
            crud = CRUDManager("test_app")
            entity_name = target_entity["name"]
            camel_name = _to_camel_case(new_field["name"])

            # --- ADD field with fieldWidget ---
            field_with_widget = dict(new_field)
            field_with_widget["fieldWidget"] = field_widget
            if field_widget == "codeEditor":
                field_with_widget["language"] = language

            crud.add_field(entity_name, field_with_widget)

            # Verify fieldWidget persisted in DTO layer
            dto = _load_json(app_dir, "webflux_dto_layer.json")
            for dtype in ("Input", "Output", "Filter"):
                dto_def = next(
                    d for d in dto["dtos"]
                    if d["entityName"] == entity_name and d["dtoType"] == dtype
                )
                dto_field = next(
                    f for f in dto_def["fields"] if f["fieldName"] == camel_name
                )
                assert dto_field["fieldWidget"] == field_widget, (
                    f"fieldWidget not preserved in {dtype} DTO: "
                    f"expected {field_widget!r}, got {dto_field.get('fieldWidget')!r}"
                )
                if field_widget == "codeEditor":
                    assert dto_field["language"] == language, (
                        f"language not preserved in {dtype} DTO: "
                        f"expected {language!r}, got {dto_field.get('language')!r}"
                    )
                else:
                    assert "language" not in dto_field, (
                        f"language should not be present for widget {field_widget!r}"
                    )

            # --- ADD field WITHOUT fieldWidget (default behavior) ---
            default_field = {
                "name": new_field["name"] + "def",
                "type": new_field.get("type", "String"),
            }
            assume(default_field["name"] not in existing_field_names)
            crud.add_field(entity_name, default_field)

            dto = _load_json(app_dir, "webflux_dto_layer.json")
            default_camel = _to_camel_case(default_field["name"])
            for dtype in ("Input", "Output", "Filter"):
                dto_def = next(
                    d for d in dto["dtos"]
                    if d["entityName"] == entity_name and d["dtoType"] == dtype
                )
                dto_field = next(
                    f for f in dto_def["fields"] if f["fieldName"] == default_camel
                )
                # When absent, fieldWidget should not be in the dict (defaults to "text")
                assert "fieldWidget" not in dto_field, (
                    f"fieldWidget should not be present when not specified"
                )

            # --- MODIFY field: change fieldWidget ---
            new_widget = "markdown" if field_widget != "markdown" else "json"
            modify_updates = {"fieldWidget": new_widget}
            crud.modify_field(entity_name, new_field["name"], modify_updates)

            dto = _load_json(app_dir, "webflux_dto_layer.json")
            for dtype in ("Input", "Output", "Filter"):
                dto_def = next(
                    d for d in dto["dtos"]
                    if d["entityName"] == entity_name and d["dtoType"] == dtype
                )
                dto_field = next(
                    f for f in dto_def["fields"] if f["fieldName"] == camel_name
                )
                assert dto_field["fieldWidget"] == new_widget, (
                    f"fieldWidget not updated in {dtype} DTO after modify_field: "
                    f"expected {new_widget!r}, got {dto_field.get('fieldWidget')!r}"
                )
                # language should be removed since new widget is not codeEditor
                assert "language" not in dto_field, (
                    f"language should be removed when widget changed to {new_widget!r}"
                )

            # --- MODIFY field: change to codeEditor with language ---
            crud.modify_field(entity_name, new_field["name"], {
                "fieldWidget": "codeEditor",
                "language": "python",
            })

            dto = _load_json(app_dir, "webflux_dto_layer.json")
            for dtype in ("Input", "Output", "Filter"):
                dto_def = next(
                    d for d in dto["dtos"]
                    if d["entityName"] == entity_name and d["dtoType"] == dtype
                )
                dto_field = next(
                    f for f in dto_def["fields"] if f["fieldName"] == camel_name
                )
                assert dto_field["fieldWidget"] == "codeEditor"
                assert dto_field["language"] == "python"

        finally:
            os.chdir(original_cwd)


# --- Property 7: CRUDManager add_field propagates fieldWidget and language ---

@settings(max_examples=100)
@given(
    initial_entities=_initial_entities_st,
    new_field=_field_st,
    field_widget=_field_widget_st,
    language=_language_st,
)
def test_add_field_propagates_field_widget(
    initial_entities: list[dict],
    new_field: dict,
    field_widget: str,
    language: str,
) -> None:
    """Property 7: add_field stores fieldWidget and language on DTO entry.
    When fieldWidget absent, DTO entry has no fieldWidget key.

    **Validates: Requirements 9.1, 9.3, 9.5**
    """
    target_entity = initial_entities[0]
    existing_field_names = {f["name"] for f in target_entity["fields"]}
    assume(new_field["name"] not in existing_field_names)
    assume(new_field["name"] not in ("id", "createdAt", "updatedAt", "isDeleted"))

    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            app_dir = _scaffold_app(tmp, "test_app", initial_entities)
            crud = CRUDManager("test_app")
            entity_name = target_entity["name"]
            camel_name = _to_camel_case(new_field["name"])

            # Add with fieldWidget
            field_desc = dict(new_field)
            field_desc["fieldWidget"] = field_widget
            if field_widget == "codeEditor":
                field_desc["language"] = language
            crud.add_field(entity_name, field_desc)

            dto = _load_json(app_dir, "webflux_dto_layer.json")
            input_dto = next(d for d in dto["dtos"] if d["entityName"] == entity_name and d["dtoType"] == "Input")
            dto_field = next(f for f in input_dto["fields"] if f["fieldName"] == camel_name)

            assert dto_field.get("fieldWidget") == field_widget
            if field_widget == "codeEditor":
                assert dto_field.get("language") == language
            else:
                assert "language" not in dto_field

        finally:
            os.chdir(original_cwd)


# --- Property 8: CRUDManager modify_field cleans up language ---

@settings(max_examples=100)
@given(
    initial_entities=_initial_entities_st,
    new_field=_field_st,
    new_widget=st.sampled_from(["richText", "markdown", "json", "text"]),
)
def test_modify_field_cleans_up_language(
    initial_entities: list[dict],
    new_field: dict,
    new_widget: str,
) -> None:
    """Property 8: Modifying from codeEditor to another widget removes language.

    **Validates: Requirements 9.2, 9.4**
    """
    target_entity = initial_entities[0]
    existing_field_names = {f["name"] for f in target_entity["fields"]}
    assume(new_field["name"] not in existing_field_names)
    assume(new_field["name"] not in ("id", "createdAt", "updatedAt", "isDeleted"))

    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            app_dir = _scaffold_app(tmp, "test_app", initial_entities)
            crud = CRUDManager("test_app")
            entity_name = target_entity["name"]
            camel_name = _to_camel_case(new_field["name"])

            # Add field with codeEditor + language
            field_desc = dict(new_field)
            field_desc["fieldWidget"] = "codeEditor"
            field_desc["language"] = "java"
            crud.add_field(entity_name, field_desc)

            # Modify to a different widget
            crud.modify_field(entity_name, new_field["name"], {"fieldWidget": new_widget})

            dto = _load_json(app_dir, "webflux_dto_layer.json")
            input_dto = next(d for d in dto["dtos"] if d["entityName"] == entity_name and d["dtoType"] == "Input")
            dto_field = next(f for f in input_dto["fields"] if f["fieldName"] == camel_name)

            assert dto_field["fieldWidget"] == new_widget
            if new_widget != "codeEditor":
                assert "language" not in dto_field, "language should be removed for non-codeEditor widget"

        finally:
            os.chdir(original_cwd)


# --- Property 9: CRUDManager rejects invalid fieldWidget values ---

@settings(max_examples=100)
@given(
    initial_entities=_initial_entities_st,
    new_field=_field_st,
    bad_widget=st.text(min_size=1, max_size=20).filter(
        lambda s: s not in {"text", "richText", "codeEditor", "markdown", "json"}
    ),
)
def test_invalid_field_widget_raises_value_error(
    initial_entities: list[dict],
    new_field: dict,
    bad_widget: str,
) -> None:
    """Property 9: Invalid fieldWidget values raise ValueError.

    **Validates: Requirements 9.6**
    """
    import pytest

    target_entity = initial_entities[0]
    existing_field_names = {f["name"] for f in target_entity["fields"]}
    assume(new_field["name"] not in existing_field_names)
    assume(new_field["name"] not in ("id", "createdAt", "updatedAt", "isDeleted"))

    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            app_dir = _scaffold_app(tmp, "test_app", initial_entities)
            crud = CRUDManager("test_app")
            entity_name = target_entity["name"]

            field_desc = dict(new_field)
            field_desc["fieldWidget"] = bad_widget

            with pytest.raises(ValueError) as exc_info:
                crud.add_field(entity_name, field_desc)

            assert bad_widget in str(exc_info.value)

        finally:
            os.chdir(original_cwd)
