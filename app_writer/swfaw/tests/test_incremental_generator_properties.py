"""Property-based tests for IncrementalGenerator.

**Validates: Requirements 6.4, 6.7**
"""

import sys
import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

# Ensure swfaw/ is on sys.path so generator imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generators.incremental_generator import IncrementalGenerator
from utils.dependency_mapper import AffectedOutputs
from utils.definition_loader import DefinitionBundle


# ---------------------------------------------------------------------------
# Helpers — build a realistic DefinitionBundle with multiple entities
# ---------------------------------------------------------------------------

_ALL_ENTITIES = ["User", "Product", "Order", "Category", "Review"]
_BASE_PACKAGE = "com.example"

# File types that map to per-entity generated files
_ENTITY_FILE_TYPES = {"entity", "dto_input", "dto_output", "dto_filter",
                      "repository", "service", "controller"}


def _make_entity_def(name: str) -> dict:
    """Build a minimal entity definition dict."""
    return {
        "tableName": name.lower() + "s",
        "className": name,
        "packageName": f"{_BASE_PACKAGE}.entity",
        "isRootEntity": False,
        "parentEntity": None,
        "hasPublicFlag": False,
        "hasAuditFields": False,
        "hasSoftDelete": False,
        "relationships": [],
        "fields": [
            {
                "columnName": "id",
                "fieldName": "id",
                "javaType": "Long",
                "isPrimaryKey": True,
                "isNullable": False,
                "columnDefinition": "BIGINT UNSIGNED",
            },
            {
                "columnName": "name",
                "fieldName": "name",
                "javaType": "String",
                "isPrimaryKey": False,
                "isNullable": True,
                "columnDefinition": "VARCHAR(255)",
            },
        ],
    }


def _make_repo_def(name: str) -> dict:
    return {
        "entityName": name,
        "className": f"{name}Repository",
        "packageName": f"{_BASE_PACKAGE}.repository",
        "idType": "Long",
        "hasCustomQueries": False,
        "customQueries": [],
        "hasSoftDelete": False,
        "hasAuthorization": False,
    }


def _make_service_def(name: str) -> dict:
    return {
        "entityName": name,
        "className": f"{name}Service",
        "packageName": f"{_BASE_PACKAGE}.service",
        "repositoryName": f"{name}Repository",
        "isRootEntity": False,
        "hasAuthorization": False,
    }


def _make_controller_def(name: str) -> dict:
    return {
        "entityName": name,
        "className": f"{name}Controller",
        "packageName": f"{_BASE_PACKAGE}.controller",
        "serviceName": f"{name}Service",
        "basePath": f"/api/{name.lower()}s",
        "isRootEntity": False,
        "endpoints": {},
        "customEndpoints": [],
        "corsConfig": {},
    }


def _make_dto_def(name: str, dto_type: str) -> dict:
    suffix = {"Input": "InputDTO", "Output": "OutputDTO", "Filter": "FilterDTO"}
    return {
        "entityName": name,
        "className": f"{name}{suffix[dto_type]}",
        "packageName": f"{_BASE_PACKAGE}.dto",
        "dtoType": dto_type,
        "isRootEntity": False,
        "fields": [
            {
                "columnName": "name",
                "fieldName": "name",
                "javaType": "String",
                "isPrimaryKey": False,
                "isNullable": True,
                "columnDefinition": "VARCHAR(255)",
            },
        ],
        "fieldConfigs": [],
        "customValidators": [],
        "excludeSensitiveFields": [],
        "includeRelationships": False,
    }


def _make_bundle(entity_names: list[str]) -> DefinitionBundle:
    """Build a realistic DefinitionBundle with the given entity names."""
    entity_defs = [_make_entity_def(n) for n in entity_names]
    repo_defs = [_make_repo_def(n) for n in entity_names]
    service_defs = [_make_service_def(n) for n in entity_names]
    controller_defs = [_make_controller_def(n) for n in entity_names]
    dto_defs = []
    for n in entity_names:
        for dt in ("Input", "Output", "Filter"):
            dto_defs.append(_make_dto_def(n, dt))

    return DefinitionBundle(
        app_name="test_app",
        definitions_dir=Path("/tmp/fake"),
        manifest={"version": "2.5", "format": "split", "files": {}},
        project_metadata={
            "projectMetadata": {
                "groupId": _BASE_PACKAGE,
                "database": {"name": "test_db"},
            }
        },
        entity_layer={"entities": entity_defs},
        entities={"entities": []},
        relationships={"relationships": []},
        repository_layer={"repositories": repo_defs},
        service_layer={"services": service_defs},
        controller_layer={"controllers": controller_defs},
        dto_layer={"dtos": dto_defs},
    )


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Pick 2-4 entity names so we always have both affected and non-affected
_entity_names_st = st.lists(
    st.sampled_from(_ALL_ENTITIES),
    min_size=2,
    max_size=4,
    unique=True,
)

# Pick a non-empty strict subset of file types per affected entity
_file_types_st = st.frozensets(
    st.sampled_from(sorted(_ENTITY_FILE_TYPES)),
    min_size=1,
    max_size=len(_ENTITY_FILE_TYPES),
)


# ---------------------------------------------------------------------------
# Property 17: Incremental generation minimality
# ---------------------------------------------------------------------------


@settings(max_examples=20, deadline=None)
@given(
    entity_names=_entity_names_st,
    affected_ratio=st.floats(min_value=0.1, max_value=0.9),
    file_types=_file_types_st,
)
def test_incremental_generation_minimality(
    entity_names: list[str],
    affected_ratio: float,
    file_types: frozenset[str],
) -> None:
    """Property 17: Incremental generation minimality

    For any set of dirty/clean files, incremental generation regenerates
    only files for entities whose layers are dirty, and does not
    regenerate files for entities whose layers are all clean.

    **Validates: Requirements 6.4, 6.7**
    """
    # Split entities into affected and non-affected
    split_idx = max(1, int(len(entity_names) * affected_ratio))
    split_idx = min(split_idx, len(entity_names) - 1)  # ensure at least 1 non-affected
    affected_names = set(entity_names[:split_idx])
    non_affected_names = set(entity_names[split_idx:])

    assert affected_names, "Must have at least one affected entity"
    assert non_affected_names, "Must have at least one non-affected entity"

    # Build AffectedOutputs with only the affected subset
    affected = AffectedOutputs(
        regenerate_sql=False,
        affected_entities=affected_names,
        affected_file_types={name: set(file_types) for name in affected_names},
    )

    bundle = _make_bundle(entity_names)
    gen = IncrementalGenerator()

    with tempfile.TemporaryDirectory() as tmp_dir:
        output_dir = Path(tmp_dir)
        regenerated = gen.regenerate_affected(bundle, affected, output_dir)

        # --- Property: all regenerated paths reference ONLY affected entities ---
        for path in regenerated:
            # Use only the filename to avoid false matches on system paths
            # (e.g. C:\Users\ on Windows contains "User")
            fname = Path(path).name
            matches_affected = any(name in fname for name in affected_names)
            matches_non_affected = any(name in fname for name in non_affected_names)

            assert matches_affected, (
                f"Regenerated file '{fname}' does not reference any affected entity "
                f"{affected_names}"
            )
            assert not matches_non_affected, (
                f"Regenerated file '{fname}' references non-affected entity from "
                f"{non_affected_names} — violates minimality"
            )

        # --- Property: no files for non-affected entities exist on disk ---
        code_dir = output_dir / "webflux_app"
        if code_dir.exists():
            all_generated_files = list(code_dir.rglob("*.java"))
            for fpath in all_generated_files:
                fname = fpath.name
                for non_affected in non_affected_names:
                    assert non_affected not in fname, (
                        f"File '{fpath}' exists on disk for non-affected entity "
                        f"'{non_affected}' — violates minimality"
                    )

        # --- Property: regenerated count is non-zero ---
        assert len(regenerated) > 0, (
            "Expected at least one regenerated file for affected entities "
            f"{affected_names} with file types {file_types}"
        )
