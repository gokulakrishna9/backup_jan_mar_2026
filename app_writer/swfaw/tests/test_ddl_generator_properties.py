"""Property-based tests for DDLGenerator.

**Validates: Requirements 5.2, 5.3**
"""

import re
import sys
from pathlib import Path

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

# Ensure swfaw/ is on sys.path so generator imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generators.ddl_generator import DDLGenerator


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# All known Java types in the fallback map
KNOWN_JAVA_TYPES = list(DDLGenerator.JAVA_TO_SQL_FALLBACK.keys())

# An unknown type that is NOT in the fallback map
UNKNOWN_JAVA_TYPE = "CustomObject"


def _minimal_project_metadata(db_name: str = "test_db") -> dict:
    return {"projectMetadata": {"database": {"name": db_name}}}


def _empty_relationships() -> dict:
    return {"relationships": []}


def _build_entity_layer(entities: list[dict]) -> dict:
    return {"entities": entities}


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Snake_case identifiers for table/column names
_snake_ident_st = st.from_regex(r"[a-z][a-z0-9]*(_[a-z0-9]+){0,3}", fullmatch=True).filter(
    lambda s: 2 <= len(s) <= 40
)

# Non-empty column definition strings (verbatim SQL types)
_column_def_st = st.sampled_from([
    "BIGINT UNSIGNED",
    "VARCHAR(100)",
    "TEXT",
    "DECIMAL(10,2)",
    "TINYINT(1)",
    "MEDIUMTEXT",
    "INT NOT NULL DEFAULT 0",
])

# Java types: mix of known and unknown
_java_type_st = st.one_of(
    st.sampled_from(KNOWN_JAVA_TYPES),
    st.just(UNKNOWN_JAVA_TYPE),
)

# Whether a field has a non-empty columnDefinition or empty
_has_col_def_st = st.booleans()


@st.composite
def _field_st(draw):
    """Generate a single field definition dict."""
    col_name = draw(_snake_ident_st)
    field_name = draw(st.from_regex(r"[a-z][a-zA-Z0-9]{1,20}", fullmatch=True))
    java_type = draw(_java_type_st)
    has_col_def = draw(_has_col_def_st)
    col_def = draw(_column_def_st) if has_col_def else ""
    is_pk = draw(st.booleans())
    is_nullable = draw(st.booleans())

    return {
        "columnName": col_name,
        "fieldName": field_name,
        "javaType": java_type,
        "columnDefinition": col_def,
        "isPrimaryKey": is_pk,
        "isNullable": is_nullable,
    }


@st.composite
def _entity_st(draw):
    """Generate a single entity definition with unique column names."""
    table_name = draw(_snake_ident_st)
    fields = draw(st.lists(_field_st(), min_size=1, max_size=6))

    # Ensure unique column names within the entity
    seen = set()
    unique_fields = []
    for f in fields:
        if f["columnName"] not in seen:
            seen.add(f["columnName"])
            unique_fields.append(f)
    assume(len(unique_fields) >= 1)

    return {
        "tableName": table_name,
        "className": table_name.title().replace("_", ""),
        "fields": unique_fields,
    }


# ---------------------------------------------------------------------------
# Property 2: DDL column completeness and type resolution
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(entity=_entity_st())
def test_ddl_column_completeness_and_type_resolution(entity: dict) -> None:
    """Property 2: DDL column completeness and type resolution

    For any entity and field, generated DDL contains a column with
    f.columnName in the correct CREATE TABLE, and SQL type is
    columnDefinition verbatim when non-empty, else
    JAVA_TO_SQL_FALLBACK[javaType], else VARCHAR(255).

    **Validates: Requirements 5.2, 5.3**
    """
    gen = DDLGenerator()
    entity_layer = _build_entity_layer([entity])
    relationships = _empty_relationships()
    project_metadata = _minimal_project_metadata()

    ddl = gen.generate_schema(entity_layer, relationships, project_metadata)

    table_name = entity["tableName"]

    # Extract the CREATE TABLE block for this entity
    pattern = (
        r"CREATE TABLE IF NOT EXISTS `"
        + re.escape(table_name)
        + r"`\s*\((.*?)\)\s*ENGINE"
    )
    match = re.search(pattern, ddl, re.DOTALL)
    assert match is not None, (
        f"CREATE TABLE for `{table_name}` not found in DDL:\n{ddl}"
    )
    create_body = match.group(1)

    for field in entity["fields"]:
        col_name = field["columnName"]
        col_def = field.get("columnDefinition", "")
        java_type = field.get("javaType", "")

        # 1) Column must appear in the CREATE TABLE body
        assert f"`{col_name}`" in create_body, (
            f"Column `{col_name}` not found in CREATE TABLE `{table_name}`.\n"
            f"Body:\n{create_body}"
        )

        # 2) Determine expected SQL type per resolution priority
        if col_def and isinstance(col_def, str) and col_def.strip():
            expected_type = col_def.strip()
        elif java_type in DDLGenerator.JAVA_TO_SQL_FALLBACK:
            expected_type = DDLGenerator.JAVA_TO_SQL_FALLBACK[java_type]
        else:
            expected_type = "VARCHAR(255)"

        # 3) The resolved type must appear right after the column name
        col_line_pattern = re.escape(f"`{col_name}` {expected_type}")
        assert re.search(col_line_pattern, create_body), (
            f"Column `{col_name}` expected SQL type '{expected_type}' "
            f"not found in CREATE TABLE `{table_name}`.\n"
            f"Body:\n{create_body}"
        )


# ---------------------------------------------------------------------------
# Property 3: DDL constraint correctness
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(entity=_entity_st())
def test_ddl_constraint_correctness(entity: dict) -> None:
    """Property 3: DDL constraint correctness

    For any entity and field:
    - A field appears in PRIMARY KEY iff isPrimaryKey is true
    - A column has NOT NULL iff isNullable is false or isPrimaryKey is true

    **Validates: Requirements 5.5, 5.6**
    """
    gen = DDLGenerator()
    entity_layer = _build_entity_layer([entity])
    relationships = _empty_relationships()
    project_metadata = _minimal_project_metadata()

    ddl = gen.generate_schema(entity_layer, relationships, project_metadata)

    table_name = entity["tableName"]

    # Extract the CREATE TABLE block for this entity
    pattern = (
        r"CREATE TABLE IF NOT EXISTS `"
        + re.escape(table_name)
        + r"`\s*\((.*?)\)\s*ENGINE"
    )
    match = re.search(pattern, ddl, re.DOTALL)
    assert match is not None, (
        f"CREATE TABLE for `{table_name}` not found in DDL:\n{ddl}"
    )
    create_body = match.group(1)

    # Extract the PRIMARY KEY column list (if present)
    pk_match = re.search(r"PRIMARY KEY\s*\(([^)]+)\)", create_body)
    if pk_match:
        pk_columns = set(re.findall(r"`([^`]+)`", pk_match.group(1)))
    else:
        pk_columns = set()

    # Build a map of column name → its full column line
    col_lines: dict[str, str] = {}
    for line in create_body.split("\n"):
        line_stripped = line.strip().rstrip(",")
        col_match = re.match(r"^`([^`]+)`\s+", line_stripped)
        if col_match:
            col_lines[col_match.group(1)] = line_stripped

    for field in entity["fields"]:
        col_name = field["columnName"]
        is_pk = field.get("isPrimaryKey", False)
        is_nullable = field.get("isNullable", True)

        # 1) Field appears in PRIMARY KEY iff isPrimaryKey is true
        if is_pk:
            assert col_name in pk_columns, (
                f"Column `{col_name}` has isPrimaryKey=true but is NOT in "
                f"PRIMARY KEY constraint. PK columns: {pk_columns}\n"
                f"Body:\n{create_body}"
            )
        else:
            assert col_name not in pk_columns, (
                f"Column `{col_name}` has isPrimaryKey=false but IS in "
                f"PRIMARY KEY constraint. PK columns: {pk_columns}\n"
                f"Body:\n{create_body}"
            )

        # 2) Column has NOT NULL iff isNullable is false or isPrimaryKey is true
        #    Skip this check when columnDefinition is non-empty because the
        #    verbatim SQL may already contain NOT NULL (or omit it) and the
        #    generator uses it as-is — the isNullable/isPrimaryKey flags
        #    still add NOT NULL *after* the resolved type, but the verbatim
        #    definition itself may already include it, making string-based
        #    detection unreliable.
        col_def = field.get("columnDefinition", "")
        has_verbatim_def = bool(col_def and isinstance(col_def, str) and col_def.strip())

        if not has_verbatim_def:
            assert col_name in col_lines, (
                f"Column `{col_name}` not found in column lines.\n"
                f"Body:\n{create_body}"
            )
            col_line = col_lines[col_name]
            has_not_null = "NOT NULL" in col_line

            if not is_nullable or is_pk:
                assert has_not_null, (
                    f"Column `{col_name}` (isPrimaryKey={is_pk}, "
                    f"isNullable={is_nullable}) should have NOT NULL but "
                    f"doesn't.\nLine: {col_line}"
                )
            else:
                assert not has_not_null, (
                    f"Column `{col_name}` (isPrimaryKey={is_pk}, "
                    f"isNullable={is_nullable}) should NOT have NOT NULL but "
                    f"does.\nLine: {col_line}"
                )


# ---------------------------------------------------------------------------
# Property 5: DDL structural completeness
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(
    entities=st.lists(_entity_st(), min_size=1, max_size=4).filter(
        lambda ents: len({e["tableName"] for e in ents}) == len(ents)
    )
)
def test_ddl_structural_completeness(entities: list[dict]) -> None:
    """Property 5: DDL structural completeness

    For any valid entity_layer, DDL starts with CREATE DATABASE IF NOT EXISTS
    and USE, contains exactly one CREATE TABLE IF NOT EXISTS per entity, and
    uses IF NOT EXISTS on all CREATE statements.

    **Validates: Requirements 5.1, 5.2, 5.8, 5.9**
    """
    gen = DDLGenerator()
    entity_layer = _build_entity_layer(entities)
    relationships = _empty_relationships()
    project_metadata = _minimal_project_metadata()

    ddl = gen.generate_schema(entity_layer, relationships, project_metadata)

    # 1) DDL starts with CREATE DATABASE IF NOT EXISTS `test_db`;
    assert ddl.startswith("CREATE DATABASE IF NOT EXISTS `test_db`;"), (
        f"DDL does not start with CREATE DATABASE IF NOT EXISTS `test_db`;\n"
        f"First 200 chars:\n{ddl[:200]}"
    )

    # 2) DDL contains USE `test_db`;
    assert "USE `test_db`;" in ddl, (
        f"DDL does not contain USE `test_db`;\n"
        f"First 300 chars:\n{ddl[:300]}"
    )

    # 3) For each entity, exactly one CREATE TABLE IF NOT EXISTS `{tableName}`
    for entity in entities:
        table_name = entity["tableName"]
        token = f"CREATE TABLE IF NOT EXISTS `{table_name}`"
        count = ddl.count(token)
        assert count == 1, (
            f"Expected exactly 1 occurrence of '{token}' but found {count}\n"
            f"DDL:\n{ddl}"
        )

    # 4) Every CREATE TABLE in the DDL uses IF NOT EXISTS
    create_table_all = re.findall(r"CREATE TABLE\b[^(]*\(", ddl)
    for ct in create_table_all:
        assert "IF NOT EXISTS" in ct, (
            f"Found CREATE TABLE without IF NOT EXISTS: {ct!r}"
        )

    # 5) Every CREATE DATABASE in the DDL uses IF NOT EXISTS
    create_db_all = re.findall(r"CREATE DATABASE\b[^;]*;", ddl)
    for cd in create_db_all:
        assert "IF NOT EXISTS" in cd, (
            f"Found CREATE DATABASE without IF NOT EXISTS: {cd!r}"
        )
