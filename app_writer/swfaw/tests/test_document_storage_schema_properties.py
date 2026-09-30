"""Property-based tests for DocumentStorageSchemaGenerator DDL generation.

**Validates: Requirements 6.1, 6.2, 6.3**
"""

import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

# Ensure swfaw/ is on sys.path so template/generator imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generators.document_storage_schema_generator import DocumentStorageSchemaGenerator


# ---------------------------------------------------------------------------
# Strategies
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

# documentCollections entry — tableName must be a valid SQL identifier
_doc_collection_entry_st = st.fixed_dictionaries({
    "name": st.from_regex(r"[A-Z][a-zA-Z]{0,9}", fullmatch=True),
    "tableName": st.from_regex(r"[a-z][a-z_]{0,14}", fullmatch=True),
    "description": st.text(min_size=0, max_size=30, alphabet=st.characters(
        whitelist_categories=("L", "N", "Z"),
    )),
})

# entityAttachments entry strategy (not used by DDL gen, but part of the definition)
_entity_attachment_entry_st = st.fixed_dictionaries({
    "entityName": st.from_regex(r"[A-Z][a-zA-Z]{0,9}", fullmatch=True),
    "foreignKeyColumn": st.from_regex(r"[a-z][a-z_]{0,14}_id", fullmatch=True),
})

# jsonColumns entry strategy (not used by DDL gen, but part of the definition)
_json_column_entry_st = st.fixed_dictionaries({
    "entityName": st.from_regex(r"[A-Z][a-zA-Z]{0,9}", fullmatch=True),
    "columnName": st.from_regex(r"[a-z][a-z_]{0,9}", fullmatch=True),
    "fieldName": st.from_regex(r"[a-z][a-zA-Z]{0,9}", fullmatch=True),
})

# Full document_storage_layer dict strategy
_document_storage_layer_st = st.fixed_dictionaries({
    "fileStorage": _file_storage_st,
    "jsonColumns": st.lists(_json_column_entry_st, min_size=0, max_size=3),
    "documentCollections": st.lists(_doc_collection_entry_st, min_size=0, max_size=3),
    "entityAttachments": st.lists(_entity_attachment_entry_st, min_size=0, max_size=3),
})

# Strategy that always has fileStorage.enabled=true
_enabled_file_storage_st = st.fixed_dictionaries({
    "enabled": st.just(True),
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

# Strategy with at least one collection
_nonempty_collections_st = st.lists(
    _doc_collection_entry_st, min_size=1, max_size=4
).filter(lambda cols: len({c["tableName"] for c in cols}) == len(cols))


# ---------------------------------------------------------------------------
# Property 10: DDL generation for document storage tables
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(
    file_storage=_enabled_file_storage_st,
    collections=st.lists(_doc_collection_entry_st, min_size=0, max_size=3),
    json_columns=st.lists(_json_column_entry_st, min_size=0, max_size=2),
    attachments=st.lists(_entity_attachment_entry_st, min_size=0, max_size=2),
)
def test_file_storage_enabled_produces_file_metadata_ddl(
    file_storage: dict,
    collections: list[dict],
    json_columns: list[dict],
    attachments: list[dict],
) -> None:
    """Property 10 (file_metadata): When fileStorage.enabled=true, DDL contains
    CREATE TABLE IF NOT EXISTS `file_metadata` with all specified columns and index.

    **Validates: Requirements 6.1, 6.3**
    """
    definition = {
        "fileStorage": file_storage,
        "jsonColumns": json_columns,
        "documentCollections": collections,
        "entityAttachments": attachments,
    }

    ddl = DocumentStorageSchemaGenerator.generate(definition)

    # Must contain the file_metadata CREATE TABLE
    assert "CREATE TABLE IF NOT EXISTS `file_metadata`" in ddl

    # All required columns must be present
    required_columns = [
        "`id`", "`file_name`", "`content_type`", "`file_size`",
        "`storage_path`", "`uploaded_at`", "`entity_type`",
        "`entity_id`", "`uploaded_by_user_id`",
    ]
    for col in required_columns:
        assert col in ddl, f"Missing column {col} in file_metadata DDL"

    # Index on (entity_type, entity_id) must be present
    assert "idx_file_metadata_entity" in ddl
    assert "`entity_type`, `entity_id`" in ddl


@settings(max_examples=20)
@given(
    collections=_nonempty_collections_st,
    json_columns=st.lists(_json_column_entry_st, min_size=0, max_size=2),
    attachments=st.lists(_entity_attachment_entry_st, min_size=0, max_size=2),
    file_enabled=st.booleans(),
)
def test_collection_tables_ddl_generated(
    collections: list[dict],
    json_columns: list[dict],
    attachments: list[dict],
    file_enabled: bool,
) -> None:
    """Property 10 (collections): For each collection with tableName T, DDL contains
    CREATE TABLE IF NOT EXISTS `T` with id, content JSON NOT NULL, created_at, updated_at.

    **Validates: Requirements 6.2**
    """
    file_storage = {"enabled": file_enabled, "provider": "local",
                    "localBasePath": "./uploads", "maxFileSizeMb": 50,
                    "allowedContentTypes": []}
    definition = {
        "fileStorage": file_storage,
        "jsonColumns": json_columns,
        "documentCollections": collections,
        "entityAttachments": attachments,
    }

    ddl = DocumentStorageSchemaGenerator.generate(definition)

    for collection in collections:
        table_name = collection["tableName"]

        # Must contain CREATE TABLE for this collection
        assert f"CREATE TABLE IF NOT EXISTS `{table_name}`" in ddl, (
            f"Missing CREATE TABLE for collection '{table_name}'"
        )

        # Extract the DDL block for this specific table to check columns
        # Find the block starting from CREATE TABLE `<table_name>` to the next semicolon
        start = ddl.index(f"CREATE TABLE IF NOT EXISTS `{table_name}`")
        end = ddl.index(";", start) + 1
        table_ddl = ddl[start:end]

        assert "`id`" in table_ddl, f"Missing `id` column in {table_name} DDL"
        assert "`content` JSON NOT NULL" in table_ddl, (
            f"Missing `content` JSON NOT NULL in {table_name} DDL"
        )
        assert "`created_at`" in table_ddl, f"Missing `created_at` in {table_name} DDL"
        assert "`updated_at`" in table_ddl, f"Missing `updated_at` in {table_name} DDL"


@settings(max_examples=20)
@given(
    json_columns=st.lists(_json_column_entry_st, min_size=0, max_size=2),
    attachments=st.lists(_entity_attachment_entry_st, min_size=0, max_size=2),
)
def test_disabled_file_storage_no_collections_produces_empty(
    json_columns: list[dict],
    attachments: list[dict],
) -> None:
    """Property 10 (empty case): When fileStorage.enabled=false and no collections,
    DDL is empty string.

    **Validates: Requirements 6.1, 6.2**
    """
    definition = {
        "fileStorage": {"enabled": False, "provider": "local",
                        "localBasePath": "./uploads", "maxFileSizeMb": 50,
                        "allowedContentTypes": []},
        "jsonColumns": json_columns,
        "documentCollections": [],
        "entityAttachments": attachments,
    }

    ddl = DocumentStorageSchemaGenerator.generate(definition)

    assert ddl == "", (
        f"Expected empty DDL when fileStorage disabled and no collections, "
        f"but got: {ddl!r}"
    )
