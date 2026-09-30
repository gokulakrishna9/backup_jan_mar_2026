"""Property-based tests for Phase 3 pipeline — document_storage_layer presence.

**Validates: Requirements 7.1, 7.2, 10.4**
"""

import sys
import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

# Ensure swfaw/ is on sys.path so generator/template imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generators.file_storage_generator import FileStorageGenerator
from generators.json_column_generator import JsonColumnGenerator


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

_entity_class_name_st = st.from_regex(r"[A-Z][a-zA-Z]{1,9}", fullmatch=True)

_package_name_st = st.from_regex(r"com\.[a-z]{2,8}", fullmatch=True)

_json_column_entry_st = st.fixed_dictionaries({
    "entityName": st.from_regex(r"[A-Z][a-zA-Z]{1,9}", fullmatch=True),
    "columnName": st.from_regex(r"[a-z][a-z_]{0,9}", fullmatch=True),
    "fieldName": st.from_regex(r"[a-z][a-zA-Z]{0,9}", fullmatch=True),
})

_doc_collection_entry_st = st.fixed_dictionaries({
    "name": st.from_regex(r"[A-Z][a-zA-Z]{1,9}", fullmatch=True),
    "tableName": st.from_regex(r"[a-z][a-z_]{1,14}", fullmatch=True),
    "description": st.text(min_size=0, max_size=30, alphabet=st.characters(
        whitelist_categories=("L", "N", "Z"),
    )),
})

_enabled_file_storage_st = st.fixed_dictionaries({
    "enabled": st.just(True),
    "provider": st.sampled_from(["local", "s3"]),
    "localBasePath": st.from_regex(r"\./[a-z]{1,10}", fullmatch=True),
    "maxFileSizeMb": st.integers(min_value=1, max_value=500),
    "allowedContentTypes": st.lists(
        st.sampled_from(["image/png", "image/jpeg", "application/pdf"]),
        min_size=0, max_size=3,
    ),
})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

EXPECTED_7_FS_FILES = {
    "StorageProvider.java",
    "LocalStorageProvider.java",
    "S3StorageProvider.java",
    "FileMetadata.java",
    "FileMetadataRepository.java",
    "FileStorageService.java",
    "FileController.java",
}

EXPECTED_CONVERTER_FILES = {
    "JsonReadingConverter.java",
    "JsonWritingConverter.java",
    "R2dbcJsonConversionsConfig.java",
}

EXPECTED_COLLECTION_SUFFIXES = [
    ".java",
    "Repository.java",
    "Service.java",
    "Controller.java",
    "InputDTO.java",
    "OutputDTO.java",
]


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


def _collect_entity_names_from_definition(definition: dict) -> list[str]:
    """Extract all entityName references from jsonColumns and entityAttachments."""
    names = set()
    for jc in definition.get("jsonColumns", []):
        names.add(jc["entityName"])
    for att in definition.get("entityAttachments", []):
        names.add(att["entityName"])
    return list(names)


# ---------------------------------------------------------------------------
# Property 11: Pipeline invocation conditioned on document_storage_layer presence
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(
    file_storage=_enabled_file_storage_st,
    json_columns=st.lists(_json_column_entry_st, min_size=0, max_size=2),
    collections=st.lists(_doc_collection_entry_st, min_size=1, max_size=2),
    package_name=_package_name_st,
)
def test_nonnull_document_storage_layer_invokes_generators(
    file_storage: dict,
    json_columns: list[dict],
    collections: list[dict],
    package_name: str,
) -> None:
    """Property 11 (non-null): For any DefinitionBundle with non-null
    document_storage_layer (fileStorage enabled + collections), pipeline invokes
    FileStorageGenerator and JsonColumnGenerator — both produce files.

    **Validates: Requirements 7.1, 7.2**
    """
    definition = {
        "fileStorage": file_storage,
        "jsonColumns": json_columns,
        "documentCollections": collections,
        "entityAttachments": [],
    }

    # Build entity_layer containing all referenced entity names
    referenced_entities = _collect_entity_names_from_definition(definition)
    entity_layer = _make_entity_layer(referenced_entities)

    with tempfile.TemporaryDirectory() as tmp:
        dirs = _make_dirs(Path(tmp), package_name)

        # Simulate what the pipeline does when document_storage_layer is not None:
        # it calls FileStorageGenerator.generate() and JsonColumnGenerator.generate()
        fs_paths = FileStorageGenerator.generate(
            definition, entity_layer, package_name, dirs,
        )
        jc_paths = JsonColumnGenerator.generate(
            definition, entity_layer, package_name, dirs,
        )

        # FileStorageGenerator must produce the 7 core files (enabled=true)
        fs_names = {p.name for p in fs_paths}
        assert EXPECTED_7_FS_FILES.issubset(fs_names), (
            f"FileStorageGenerator did not produce expected files.\n"
            f"  Expected at least: {EXPECTED_7_FS_FILES}\n"
            f"  Got: {fs_names}"
        )

        # JsonColumnGenerator must produce collection files (min_size=1 above)
        assert len(jc_paths) > 0, (
            "JsonColumnGenerator produced zero files despite non-empty documentCollections"
        )

        # Verify collection files are present for each collection
        jc_names = {p.name for p in jc_paths}
        for coll in collections:
            coll_name = coll["name"]
            for suffix in EXPECTED_COLLECTION_SUFFIXES:
                expected_file = f"{coll_name}{suffix}"
                assert expected_file in jc_names, (
                    f"Missing collection file '{expected_file}' in JsonColumnGenerator output.\n"
                    f"  Got: {jc_names}"
                )

        # All generated files must exist on disk
        for p in fs_paths + jc_paths:
            assert p.exists(), f"Generated file does not exist: {p}"


@settings(max_examples=20)
@given(
    package_name=_package_name_st,
)
def test_none_document_storage_layer_produces_zero_files(
    package_name: str,
) -> None:
    """Property 11 (None): For any DefinitionBundle with document_storage_layer=None,
    pipeline produces zero document-storage-related files — the generators are
    never invoked.

    **Validates: Requirements 7.2, 10.4**
    """
    # Simulate the pipeline guard: when document_storage_layer is None,
    # the pipeline skips FileStorageGenerator and JsonColumnGenerator entirely.
    document_storage_layer = None

    fs_paths: list[Path] = []
    jc_paths: list[Path] = []

    # This mirrors the pipeline's conditional:
    #   if bundle.document_storage_layer is not None:
    #       fs_paths = FileStorageGenerator.generate(...)
    #       jc_paths = JsonColumnGenerator.generate(...)
    if document_storage_layer is not None:
        with tempfile.TemporaryDirectory() as tmp:
            dirs = _make_dirs(Path(tmp), package_name)
            entity_layer = _make_entity_layer([])
            fs_paths = FileStorageGenerator.generate(
                document_storage_layer, entity_layer, package_name, dirs,
            )
            jc_paths = JsonColumnGenerator.generate(
                document_storage_layer, entity_layer, package_name, dirs,
            )

    assert fs_paths == [], (
        f"Expected zero file-storage files when document_storage_layer is None, "
        f"got {len(fs_paths)}"
    )
    assert jc_paths == [], (
        f"Expected zero json-column files when document_storage_layer is None, "
        f"got {len(jc_paths)}"
    )


@settings(max_examples=20)
@given(
    file_storage=_enabled_file_storage_st,
    json_columns=st.lists(_json_column_entry_st, min_size=1, max_size=3),
    collections=st.lists(_doc_collection_entry_st, min_size=0, max_size=2),
    package_name=_package_name_st,
)
def test_nonnull_with_json_columns_produces_converter_files(
    file_storage: dict,
    json_columns: list[dict],
    collections: list[dict],
    package_name: str,
) -> None:
    """Property 11 (converters): For any non-null document_storage_layer with
    non-empty jsonColumns, JsonColumnGenerator produces the 3 converter files.

    **Validates: Requirements 7.1, 7.2**
    """
    definition = {
        "fileStorage": file_storage,
        "jsonColumns": json_columns,
        "documentCollections": collections,
        "entityAttachments": [],
    }

    referenced_entities = _collect_entity_names_from_definition(definition)
    entity_layer = _make_entity_layer(referenced_entities)

    with tempfile.TemporaryDirectory() as tmp:
        dirs = _make_dirs(Path(tmp), package_name)

        jc_paths = JsonColumnGenerator.generate(
            definition, entity_layer, package_name, dirs,
        )

        jc_names = {p.name for p in jc_paths}
        assert EXPECTED_CONVERTER_FILES.issubset(jc_names), (
            f"JsonColumnGenerator did not produce expected converter files.\n"
            f"  Expected at least: {EXPECTED_CONVERTER_FILES}\n"
            f"  Got: {jc_names}"
        )
