"""Property-based tests for DependencyMapper.

**Validates: Requirements 6.2, 6.3, 7.3, 7.4**
"""

import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

# Ensure swfaw/ is on sys.path so `from utils.dependency_mapper import ...` works
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.dependency_mapper import DependencyMapper, AffectedOutputs
from utils.definition_loader import DefinitionBundle


# ---------------------------------------------------------------------------
# Helpers — build minimal DefinitionBundle in-memory (no disk I/O)
# ---------------------------------------------------------------------------

_ENTITY_NAMES = ["User", "Product", "Order"]


def _make_bundle(entity_names: list[str]) -> DefinitionBundle:
    """Build a minimal DefinitionBundle with the given entity classNames."""
    entities_list = [
        {
            "tableName": name.lower() + "s",
            "className": name,
            "fields": [
                {
                    "columnName": "id",
                    "fieldName": "id",
                    "javaType": "Long",
                    "isPrimaryKey": True,
                    "isNullable": False,
                    "columnDefinition": "BIGINT UNSIGNED",
                },
            ],
        }
        for name in entity_names
    ]
    return DefinitionBundle(
        app_name="test_app",
        definitions_dir=Path("/tmp/fake"),
        manifest={"version": "2.5", "format": "split", "files": {}},
        project_metadata={"projectMetadata": {"database": {"name": "test_db"}}},
        entity_layer={"entities": entities_list},
        entities={"entities": []},
        relationships={"relationships": []},
        repository_layer={"repositories": []},
        service_layer={"services": []},
        controller_layer={"controllers": []},
        dto_layer={"dtos": []},
    )


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# All keys in DEPENDENCY_MAP
_ALL_DEP_MAP_KEYS = list(DependencyMapper.DEPENDENCY_MAP.keys())

# Generate a random non-empty subset of DEPENDENCY_MAP keys as dirty files
_dirty_files_st = st.frozensets(
    st.sampled_from(_ALL_DEP_MAP_KEYS),
    min_size=1,
    max_size=len(_ALL_DEP_MAP_KEYS),
)

# Generate 1-3 entity names from the fixed pool
_entity_names_st = st.lists(
    st.sampled_from(_ENTITY_NAMES),
    min_size=1,
    max_size=3,
    unique=True,
)


# ---------------------------------------------------------------------------
# Property 15: Dependency map resolution
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(dirty_files=_dirty_files_st, entity_names=_entity_names_st)
def test_dependency_map_resolution(
    dirty_files: frozenset[str], entity_names: list[str]
) -> None:
    """Property 15: Dependency map resolution

    For any set of dirty definition files, DependencyMapper resolves
    affected file types per DEPENDENCY_MAP, and sets regenerate_sql to
    true when entity_layer/entities/relationships/project_metadata are
    dirty.

    **Validates: Requirements 6.2, 6.3**
    """
    mapper = DependencyMapper()
    bundle = _make_bundle(entity_names)
    result = mapper.resolve_affected_outputs(list(dirty_files), bundle)

    # --- Property 1: regenerate_sql is True iff any dirty file maps to "sql" ---
    sql_trigger_files = DependencyMapper._SQL_TRIGGER_FILES
    expected_sql = bool(dirty_files & sql_trigger_files)
    assert result.regenerate_sql == expected_sql, (
        f"regenerate_sql should be {expected_sql} for dirty_files={dirty_files}, "
        f"but got {result.regenerate_sql}"
    )

    # --- Property 2: affected_file_types contains all non-sql types from DEPENDENCY_MAP ---
    # Collect expected non-sql file types across all dirty files
    expected_code_types: set[str] = set()
    for df in dirty_files:
        file_types = DependencyMapper.DEPENDENCY_MAP.get(df, [])
        expected_code_types.update(ft for ft in file_types if ft != "sql")

    # For each entity, the affected_file_types should contain all expected code types
    if expected_code_types:
        for entity_name in entity_names:
            actual_types = result.affected_file_types.get(entity_name, set())
            assert expected_code_types.issubset(actual_types), (
                f"Entity '{entity_name}' missing file types: "
                f"{expected_code_types - actual_types}. "
                f"Expected at least {expected_code_types}, got {actual_types}"
            )

    # --- Property 3: all entities are affected when dirty files have code types ---
    if expected_code_types:
        assert result.affected_entities == set(entity_names), (
            f"Expected all entities {set(entity_names)} to be affected, "
            f"but got {result.affected_entities}"
        )


# ---------------------------------------------------------------------------
# Property 12: Dependency mapper includes document storage layer
# ---------------------------------------------------------------------------

# Strategy: dirty file lists that always include the document storage layer file,
# plus a random subset of other DEPENDENCY_MAP keys.
_other_dep_keys = [k for k in _ALL_DEP_MAP_KEYS if k != "webflux_document_storage_layer.json"]

_dirty_files_with_doc_storage_st = st.builds(
    lambda others: frozenset(others) | {"webflux_document_storage_layer.json"},
    st.frozensets(
        st.sampled_from(_other_dep_keys) if _other_dep_keys else st.nothing(),
        min_size=0,
        max_size=min(5, len(_other_dep_keys)),
    ),
)


@settings(max_examples=20)
@given(dirty_files=_dirty_files_with_doc_storage_st, entity_names=_entity_names_st)
def test_dependency_mapper_includes_document_storage_layer(
    dirty_files: frozenset[str], entity_names: list[str]
) -> None:
    """Property 12: Dependency mapper includes document storage layer

    For any dirty file list containing `webflux_document_storage_layer.json`,
    `resolve_affected_outputs()` sets `regenerate_sql = True` and includes
    `file_storage`, `json_converter`, `document_collection` in affected file
    types for at least one entity.

    **Validates: Requirements 7.3, 7.4**
    """
    mapper = DependencyMapper()
    bundle = _make_bundle(entity_names)
    result = mapper.resolve_affected_outputs(list(dirty_files), bundle)

    # regenerate_sql must be True (document_storage_layer.json is in _SQL_TRIGGER_FILES)
    assert result.regenerate_sql is True, (
        f"regenerate_sql should be True when dirty_files contains "
        f"'webflux_document_storage_layer.json', but got False. "
        f"dirty_files={dirty_files}"
    )

    # file_storage, json_converter, document_collection must appear in affected file types
    expected_types = {"file_storage", "json_converter", "document_collection"}
    for entity_name in entity_names:
        actual_types = result.affected_file_types.get(entity_name, set())
        assert expected_types.issubset(actual_types), (
            f"Entity '{entity_name}' missing document storage file types: "
            f"{expected_types - actual_types}. "
            f"Expected at least {expected_types}, got {actual_types}"
        )


# ---------------------------------------------------------------------------
# AI Layer dependency mapper tests
# ---------------------------------------------------------------------------

# Expected AI output types (non-sql) from DEPENDENCY_MAP for webflux_ai_layer.json
_AI_CODE_TYPES = {
    "ai_service", "ai_controller", "ai_entity", "ai_config",
    "ai_dto", "ai_repository", "ai_provider", "ai_rag",
    "ai_evaluator", "ai_ingestion", "ai_processing",
    "ai_vectorstore", "ai_orchestrator", "ai_tools", "ai_mcp",
    "ai_observability", "ai_budget", "ai_audit",
}

# Strategy: dirty file lists that always include the AI layer file,
# plus a random subset of other DEPENDENCY_MAP keys.
_other_dep_keys_no_ai = [k for k in _ALL_DEP_MAP_KEYS if k != "webflux_ai_layer.json"]

_dirty_files_with_ai_layer_st = st.builds(
    lambda others: frozenset(others) | {"webflux_ai_layer.json"},
    st.frozensets(
        st.sampled_from(_other_dep_keys_no_ai) if _other_dep_keys_no_ai else st.nothing(),
        min_size=0,
        max_size=min(5, len(_other_dep_keys_no_ai)),
    ),
)


@settings(max_examples=20)
@given(dirty_files=_dirty_files_with_ai_layer_st, entity_names=_entity_names_st)
def test_dependency_mapper_ai_layer_triggers_sql(
    dirty_files: frozenset[str], entity_names: list[str]
) -> None:
    """AI layer in dirty files triggers SQL regeneration.

    When `webflux_ai_layer.json` is dirty, `regenerate_sql` must be True
    because AI tables (chat sessions, messages, evaluations, etc.) need
    DDL regeneration.

    **Validates: Requirements 17.1–17.5**
    """
    mapper = DependencyMapper()
    bundle = _make_bundle(entity_names)
    result = mapper.resolve_affected_outputs(list(dirty_files), bundle)

    assert result.regenerate_sql is True, (
        f"regenerate_sql should be True when dirty_files contains "
        f"'webflux_ai_layer.json', but got False. dirty_files={dirty_files}"
    )


@settings(max_examples=20)
@given(dirty_files=_dirty_files_with_ai_layer_st, entity_names=_entity_names_st)
def test_dependency_mapper_ai_layer_includes_all_ai_types(
    dirty_files: frozenset[str], entity_names: list[str]
) -> None:
    """AI layer in dirty files includes all AI output types.

    When `webflux_ai_layer.json` is dirty, all AI code types (ai_service,
    ai_controller, ai_entity, ai_config, ai_dto, ai_repository, ai_provider,
    ai_rag, ai_evaluator, ai_ingestion, ai_processing, ai_vectorstore,
    ai_orchestrator, ai_tools, ai_mcp, ai_observability, ai_budget, ai_audit)
    must appear in affected_file_types for every entity.

    **Validates: Requirements 17.1–17.5**
    """
    mapper = DependencyMapper()
    bundle = _make_bundle(entity_names)
    result = mapper.resolve_affected_outputs(list(dirty_files), bundle)

    for entity_name in entity_names:
        actual_types = result.affected_file_types.get(entity_name, set())
        assert _AI_CODE_TYPES.issubset(actual_types), (
            f"Entity '{entity_name}' missing AI file types: "
            f"{_AI_CODE_TYPES - actual_types}. "
            f"Expected at least {_AI_CODE_TYPES}, got {actual_types}"
        )


@settings(max_examples=20)
@given(dirty_files=_dirty_files_with_ai_layer_st, entity_names=_entity_names_st)
def test_dependency_mapper_ai_layer_marks_all_entities_affected(
    dirty_files: frozenset[str], entity_names: list[str]
) -> None:
    """AI layer in dirty files marks all entities as affected.

    Since `webflux_ai_layer.json` is in `_ENTITY_SCOPED_FILES`, all entities
    should be marked affected when it is dirty (entity capabilities reference
    entities).

    **Validates: Requirements 17.1–17.5**
    """
    mapper = DependencyMapper()
    bundle = _make_bundle(entity_names)
    result = mapper.resolve_affected_outputs(list(dirty_files), bundle)

    assert result.affected_entities == set(entity_names), (
        f"Expected all entities {set(entity_names)} to be affected when "
        f"'webflux_ai_layer.json' is dirty, but got {result.affected_entities}"
    )


def test_ai_layer_in_dependency_map() -> None:
    """Verify webflux_ai_layer.json is registered in DEPENDENCY_MAP with correct types.

    **Validates: Requirements 17.1–17.5**
    """
    dep_map = DependencyMapper.DEPENDENCY_MAP
    assert "webflux_ai_layer.json" in dep_map, (
        "webflux_ai_layer.json must be in DEPENDENCY_MAP"
    )
    ai_types = set(dep_map["webflux_ai_layer.json"])
    expected = _AI_CODE_TYPES | {"sql"}
    assert ai_types == expected, (
        f"webflux_ai_layer.json types mismatch. Expected {expected}, got {ai_types}"
    )


def test_ai_layer_in_sql_trigger_files() -> None:
    """Verify webflux_ai_layer.json is in _SQL_TRIGGER_FILES.

    **Validates: Requirements 17.1–17.5**
    """
    assert "webflux_ai_layer.json" in DependencyMapper._SQL_TRIGGER_FILES, (
        "webflux_ai_layer.json must be in _SQL_TRIGGER_FILES"
    )


def test_ai_layer_in_entity_scoped_files() -> None:
    """Verify webflux_ai_layer.json is in _ENTITY_SCOPED_FILES.

    **Validates: Requirements 17.1–17.5**
    """
    from utils.dependency_mapper import _ENTITY_SCOPED_FILES
    assert "webflux_ai_layer.json" in _ENTITY_SCOPED_FILES, (
        "webflux_ai_layer.json must be in _ENTITY_SCOPED_FILES"
    )


def test_ai_layer_only_dirty_no_sql_from_others() -> None:
    """When only webflux_ai_layer.json is dirty, SQL is still triggered.

    **Validates: Requirements 17.1–17.5**
    """
    mapper = DependencyMapper()
    bundle = _make_bundle(["User"])
    result = mapper.resolve_affected_outputs(["webflux_ai_layer.json"], bundle)

    assert result.regenerate_sql is True
    actual_types = result.affected_file_types.get("User", set())
    assert _AI_CODE_TYPES.issubset(actual_types)
    assert result.affected_entities == {"User"}
