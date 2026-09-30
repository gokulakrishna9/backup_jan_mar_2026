"""Property-based tests for JsonColumnGenerator.

**Validates: Requirements 4.1, 4.2, 4.3, 5.1–5.5, 1.7**
"""

import sys
import tempfile
from pathlib import Path

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

# Ensure swfaw/ is on sys.path so generator/template imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generators.json_column_generator import JsonColumnGenerator


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Entity class name strategy (valid Java class names)
_entity_class_name_st = st.from_regex(r"[A-Z][a-zA-Z]{1,9}", fullmatch=True)

# Package name strategy
_package_name_st = st.from_regex(r"com\.[a-z]{2,8}", fullmatch=True)

# jsonColumns entry strategy
_json_column_entry_st = st.fixed_dictionaries({
    "entityName": st.from_regex(r"[A-Z][a-zA-Z]{0,9}", fullmatch=True),
    "columnName": st.from_regex(r"[a-z][a-z_]{0,9}", fullmatch=True),
    "fieldName": st.from_regex(r"[a-z][a-zA-Z]{0,9}", fullmatch=True),
})

# documentCollections entry strategy — name must be at least 2 chars for lower_name logic
_doc_collection_entry_st = st.fixed_dictionaries({
    "name": st.from_regex(r"[A-Z][a-zA-Z]{1,9}", fullmatch=True),
    "tableName": st.from_regex(r"[a-z][a-z_]{1,14}", fullmatch=True),
    "description": st.text(min_size=0, max_size=30, alphabet=st.characters(
        whitelist_categories=("L", "N", "Z"),
    )),
})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Property 7: JSON converter generation completeness
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(
    json_columns=st.lists(_json_column_entry_st, min_size=1, max_size=3),
    collections=st.lists(_doc_collection_entry_st, min_size=0, max_size=2),
    package_name=_package_name_st,
)
def test_nonempty_json_columns_generates_converter_files(
    json_columns: list[dict],
    collections: list[dict],
    package_name: str,
) -> None:
    """Property 7 (non-empty jsonColumns): For any definition with non-empty
    jsonColumns, generate() produces JsonReadingConverter.java,
    JsonWritingConverter.java, R2dbcJsonConversionsConfig.java.

    **Validates: Requirements 4.1, 4.2, 4.3**
    """
    # Build entity_layer that contains all referenced entity names
    all_entity_names = list({jc["entityName"] for jc in json_columns})
    entity_layer = _make_entity_layer(all_entity_names)

    definition = {
        "fileStorage": {"enabled": False},
        "jsonColumns": json_columns,
        "documentCollections": collections,
        "entityAttachments": [],
    }

    with tempfile.TemporaryDirectory() as tmp:
        dirs = _make_dirs(Path(tmp), package_name)
        result = JsonColumnGenerator.generate(definition, entity_layer, package_name, dirs)

        result_names = {p.name for p in result}
        assert EXPECTED_CONVERTER_FILES.issubset(result_names), (
            f"Expected converter files {EXPECTED_CONVERTER_FILES} to be subset of "
            f"generated files, but got {result_names}"
        )


@settings(max_examples=20)
@given(package_name=_package_name_st)
def test_empty_json_columns_and_collections_returns_empty(
    package_name: str,
) -> None:
    """Property 7 (empty): When both jsonColumns and documentCollections are
    empty, generate() returns empty list.

    **Validates: Requirements 4.1, 4.2, 4.3**
    """
    definition = {
        "fileStorage": {"enabled": False},
        "jsonColumns": [],
        "documentCollections": [],
        "entityAttachments": [],
    }
    entity_layer = _make_entity_layer([])

    with tempfile.TemporaryDirectory() as tmp:
        dirs = _make_dirs(Path(tmp), package_name)
        result = JsonColumnGenerator.generate(definition, entity_layer, package_name, dirs)

        assert result == [], (
            f"Expected empty list when both jsonColumns and documentCollections "
            f"are empty, but got {[str(p) for p in result]}"
        )


# ---------------------------------------------------------------------------
# Property 9: Document collection generation completeness
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(
    collections=st.lists(
        _doc_collection_entry_st, min_size=1, max_size=3, unique_by=lambda c: c["name"],
    ),
    package_name=_package_name_st,
)
def test_document_collection_generates_6_files_per_collection(
    collections: list[dict],
    package_name: str,
) -> None:
    """Property 9: For any collection with name N and tableName T,
    generate() produces 6 Java files per collection with correct naming.

    **Validates: Requirements 5.1–5.5**
    """
    definition = {
        "fileStorage": {"enabled": False},
        "jsonColumns": [],
        "documentCollections": collections,
        "entityAttachments": [],
    }
    entity_layer = _make_entity_layer([])

    with tempfile.TemporaryDirectory() as tmp:
        dirs = _make_dirs(Path(tmp), package_name)
        result = JsonColumnGenerator.generate(definition, entity_layer, package_name, dirs)

        result_names = {p.name for p in result}

        for collection in collections:
            name = collection["name"]
            expected_files = {f"{name}{suffix}" for suffix in EXPECTED_COLLECTION_SUFFIXES}
            assert expected_files.issubset(result_names), (
                f"Expected 6 files for collection '{name}': {expected_files}, "
                f"but generated files are {result_names}"
            )

        # Total count: 6 files per collection (no converter files since jsonColumns is empty)
        assert len(result) == 6 * len(collections), (
            f"Expected {6 * len(collections)} files for {len(collections)} collections, "
            f"but got {len(result)}"
        )


# ---------------------------------------------------------------------------
# Property 3: Non-existent entity reference raises ValueError (jsonColumns)
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(
    known_entities=st.lists(
        _entity_class_name_st, min_size=1, max_size=4, unique=True,
    ),
    bad_entity=_entity_class_name_st,
    package_name=_package_name_st,
)
def test_nonexistent_json_column_entity_raises_value_error(
    known_entities: list[str],
    bad_entity: str,
    package_name: str,
) -> None:
    """Property 3: For any jsonColumns entry whose entityName does not appear
    in entity_layer's entities[].className, JsonColumnGenerator.generate()
    raises ValueError identifying the missing entity.

    **Validates: Requirements 1.7**
    """
    # Ensure bad_entity is NOT in the known entities set
    assume(bad_entity not in known_entities)

    definition = {
        "fileStorage": {"enabled": False},
        "jsonColumns": [
            {
                "entityName": bad_entity,
                "columnName": "metadata",
                "fieldName": "metadata",
            },
        ],
        "documentCollections": [],
        "entityAttachments": [],
    }
    entity_layer = _make_entity_layer(known_entities)

    with tempfile.TemporaryDirectory() as tmp:
        dirs = _make_dirs(Path(tmp), package_name)

        with pytest.raises(ValueError) as exc_info:
            JsonColumnGenerator.generate(definition, entity_layer, package_name, dirs)

        # Error message must identify the missing entity
        assert bad_entity in str(exc_info.value), (
            f"ValueError message does not mention the missing entity '{bad_entity}'.\n"
            f"  Actual message: {exc_info.value}"
        )
