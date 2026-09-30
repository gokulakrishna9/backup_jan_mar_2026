"""Property-based tests for FileStorageGenerator.

**Validates: Requirements 3.1–3.7, 3.8, 3.9, 3.10, 1.8**
"""

import sys
import tempfile
from pathlib import Path

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

# Ensure swfaw/ is on sys.path so generator/template imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generators.file_storage_generator import FileStorageGenerator


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# fileStorage section — always enabled
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

# fileStorage section — always disabled
_disabled_file_storage_st = st.fixed_dictionaries({
    "enabled": st.just(False),
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

# Entity class name strategy (valid Java class names)
_entity_class_name_st = st.from_regex(r"[A-Z][a-zA-Z]{1,9}", fullmatch=True)

# Package name strategy
_package_name_st = st.from_regex(r"com\.[a-z]{2,8}", fullmatch=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

EXPECTED_7_FILES = {
    "StorageProvider.java",
    "LocalStorageProvider.java",
    "S3StorageProvider.java",
    "FileMetadata.java",
    "FileMetadataRepository.java",
    "FileStorageService.java",
    "FileController.java",
}


def _make_dirs(tmp_path: Path, package_name: str) -> dict:
    """Create a minimal dirs dict with src_main_java pointing to a temp path."""
    pkg_path = package_name.replace(".", "/")
    src_main_java = tmp_path / "src" / "main" / "java" / pkg_path
    src_main_java.mkdir(parents=True, exist_ok=True)
    return {"src_main_java": src_main_java}


def _make_entity_layer(entity_names: list[str]) -> dict:
    """Build a minimal entity_layer with the given class names."""
    return {
        "entities": [
            {
                "className": name,
                "tableName": name.lower() + "s",
                "fields": [
                    {
                        "columnName": "id",
                        "fieldName": "id",
                        "javaType": "Long",
                        "isPrimaryKey": True,
                        "isNullable": False,
                        "columnDefinition": "BIGINT UNSIGNED",
                    }
                ],
            }
            for name in entity_names
        ]
    }


# ---------------------------------------------------------------------------
# Property 5: File storage generation completeness
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(
    file_storage=_enabled_file_storage_st,
    json_columns=st.lists(_json_column_entry_st, min_size=0, max_size=2),
    collections=st.lists(_doc_collection_entry_st, min_size=0, max_size=2),
    package_name=_package_name_st,
)
def test_enabled_file_storage_generates_7_files(
    file_storage: dict,
    json_columns: list[dict],
    collections: list[dict],
    package_name: str,
) -> None:
    """Property 5 (enabled): For any definition with fileStorage.enabled=true,
    generate() returns paths for exactly 7 Java files.

    **Validates: Requirements 3.1–3.7, 3.10**
    """
    definition = {
        "fileStorage": file_storage,
        "jsonColumns": json_columns,
        "documentCollections": collections,
        "entityAttachments": [],
    }
    entity_layer = _make_entity_layer([])

    with tempfile.TemporaryDirectory() as tmp:
        dirs = _make_dirs(Path(tmp), package_name)
        result = FileStorageGenerator.generate(definition, entity_layer, package_name, dirs)

        # Exactly 7 base files (no entity attachments)
        result_names = {p.name for p in result}
        assert result_names == EXPECTED_7_FILES, (
            f"Expected exactly 7 files {EXPECTED_7_FILES}, "
            f"but got {result_names}"
        )
        assert len(result) == 7, (
            f"Expected 7 paths but got {len(result)}"
        )


@settings(max_examples=20)
@given(
    file_storage=_disabled_file_storage_st,
    json_columns=st.lists(_json_column_entry_st, min_size=0, max_size=2),
    collections=st.lists(_doc_collection_entry_st, min_size=0, max_size=2),
    package_name=_package_name_st,
)
def test_disabled_file_storage_returns_empty(
    file_storage: dict,
    json_columns: list[dict],
    collections: list[dict],
    package_name: str,
) -> None:
    """Property 5 (disabled): When fileStorage.enabled=false, returns empty list.

    **Validates: Requirements 3.10**
    """
    definition = {
        "fileStorage": file_storage,
        "jsonColumns": json_columns,
        "documentCollections": collections,
        "entityAttachments": [],
    }
    entity_layer = _make_entity_layer([])

    with tempfile.TemporaryDirectory() as tmp:
        dirs = _make_dirs(Path(tmp), package_name)
        result = FileStorageGenerator.generate(definition, entity_layer, package_name, dirs)

        assert result == [], (
            f"Expected empty list when fileStorage.enabled=false, "
            f"but got {[str(p) for p in result]}"
        )


# ---------------------------------------------------------------------------
# Property 6: File size and content type validation in generated service
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(
    max_file_size_mb=st.integers(min_value=1, max_value=500),
    allowed_content_types=st.lists(
        st.sampled_from([
            "image/png", "image/jpeg", "application/pdf",
            "text/plain", "application/json", "image/gif",
            "application/zip", "text/csv",
        ]),
        min_size=0,
        max_size=5,
    ),
    package_name=_package_name_st,
)
def test_file_size_and_content_type_validation_in_service(
    max_file_size_mb: int,
    allowed_content_types: list[str],
    package_name: str,
) -> None:
    """Property 6: For any maxFileSizeMb M and allowedContentTypes list L,
    generated FileStorageService code contains size check against M * 1024 * 1024
    and (when L non-empty) content type check against elements of L.

    **Validates: Requirements 3.8, 3.9**
    """
    definition = {
        "fileStorage": {
            "enabled": True,
            "provider": "local",
            "localBasePath": "./uploads",
            "maxFileSizeMb": max_file_size_mb,
            "allowedContentTypes": allowed_content_types,
        },
        "jsonColumns": [],
        "documentCollections": [],
        "entityAttachments": [],
    }
    entity_layer = _make_entity_layer([])

    with tempfile.TemporaryDirectory() as tmp:
        dirs = _make_dirs(Path(tmp), package_name)
        result = FileStorageGenerator.generate(definition, entity_layer, package_name, dirs)

        # Find the generated FileStorageService.java
        service_path = None
        for p in result:
            if p.name == "FileStorageService.java":
                service_path = p
                break

        assert service_path is not None, "FileStorageService.java not found in generated files"
        assert service_path.exists(), f"FileStorageService.java does not exist at {service_path}"

        service_code = service_path.read_text(encoding="utf-8")

        # Check file size validation: M * 1024 * 1024
        expected_max_bytes = max_file_size_mb * 1024 * 1024
        assert str(expected_max_bytes) in service_code, (
            f"Expected max bytes {expected_max_bytes} (from {max_file_size_mb} MB) "
            f"not found in FileStorageService code"
        )

        # Check content type validation when list is non-empty
        if allowed_content_types:
            for ct in allowed_content_types:
                assert f'"{ct}"' in service_code, (
                    f"Content type '{ct}' not found in FileStorageService code"
                )


# ---------------------------------------------------------------------------
# Property 3: Non-existent entity reference raises ValueError
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(
    known_entities=st.lists(
        _entity_class_name_st, min_size=1, max_size=4, unique=True,
    ),
    bad_entity=_entity_class_name_st,
    package_name=_package_name_st,
)
def test_nonexistent_entity_attachment_raises_value_error(
    known_entities: list[str],
    bad_entity: str,
    package_name: str,
) -> None:
    """Property 3: For any entityAttachments entry whose entityName does not
    appear in entity_layer's entities[].className, FileStorageGenerator.generate()
    raises ValueError identifying the missing entity.

    **Validates: Requirements 1.8**
    """
    # Ensure bad_entity is NOT in the known entities set
    assume(bad_entity not in known_entities)

    definition = {
        "fileStorage": {
            "enabled": True,
            "provider": "local",
            "localBasePath": "./uploads",
            "maxFileSizeMb": 50,
            "allowedContentTypes": [],
        },
        "jsonColumns": [],
        "documentCollections": [],
        "entityAttachments": [
            {"entityName": bad_entity, "foreignKeyColumn": "fk_id"},
        ],
    }
    entity_layer = _make_entity_layer(known_entities)

    with tempfile.TemporaryDirectory() as tmp:
        dirs = _make_dirs(Path(tmp), package_name)

        with pytest.raises(ValueError) as exc_info:
            FileStorageGenerator.generate(definition, entity_layer, package_name, dirs)

        # Error message must identify the missing entity
        assert bad_entity in str(exc_info.value), (
            f"ValueError message does not mention the missing entity '{bad_entity}'.\n"
            f"  Actual message: {exc_info.value}"
        )
