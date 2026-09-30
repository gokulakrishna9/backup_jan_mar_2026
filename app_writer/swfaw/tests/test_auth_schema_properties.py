"""Property-based tests for auth schema generation (Properties 1, 2).

Uses hypothesis to verify correctness properties of the AuthSchemaGenerator
output against the simplified authorization layer design.
"""

import sys
import importlib.util
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis.strategies import sampled_from

# ---------------------------------------------------------------------------
# Direct-import the two modules we need, bypassing generators/__init__.py
# which pulls in unrelated dependencies (pypika, etc.).
# ---------------------------------------------------------------------------
_SWFAW_ROOT = Path(__file__).resolve().parent.parent

_tpl_spec = importlib.util.spec_from_file_location(
    "auth_schema_templates",
    _SWFAW_ROOT / "templates" / "auth_schema_templates.py",
)
_tpl_mod = importlib.util.module_from_spec(_tpl_spec)
sys.modules["templates.auth_schema_templates"] = _tpl_mod
_tpl_spec.loader.exec_module(_tpl_mod)

_gen_spec = importlib.util.spec_from_file_location(
    "auth_schema_generator",
    _SWFAW_ROOT / "generators" / "auth_schema_generator.py",
)
_gen_mod = importlib.util.module_from_spec(_gen_spec)
_gen_spec.loader.exec_module(_gen_mod)

AuthSchemaGenerator = _gen_mod.AuthSchemaGenerator

# ---------------------------------------------------------------------------
# Table name lists from the design document
# ---------------------------------------------------------------------------

REMOVED_TABLES = [
    "document_group_type",
    "document_group",
    "document_group_table_scope",
    "document_group_table_record_scope",
    "document_group_query_scope",
    "document_group_query_record_scope",
    "document_group_membership",
    "document_group_definition",
    "document_permission",
    "access_control",
    "user_group",
    "user_group_membership",
    "super_user_action_log",
]

RETAINED_TABLES = [
    "auth_user",
    "system_config",
    "access_audit_log",
    "oauth2_provider",
    "oauth2_linked_account",
]

NEW_TABLES = [
    "user_role",
    "record_owner",
    "query_group",
    "query_group_query",
    "query_group_member",
    "query_group_record",
]

# Generate DDL once — it is deterministic and stateless.
_GENERATED_DDL: str = AuthSchemaGenerator.generate()


# ===================================================================
# Feature: simplified-authorization-layer
# Property 1: Old authorization artifacts are excluded from generation
# Validates: Requirements 1.1, 3.1, 3.2, 13.6
# ===================================================================


@settings(max_examples=20)
@given(table_name=sampled_from(REMOVED_TABLES))
def test_property1_old_tables_excluded_from_ddl(table_name: str) -> None:
    """**Validates: Requirements 1.1, 3.1, 3.2, 13.6**

    For any table name in the removal list, the generated DDL should NOT
    contain a CREATE TABLE statement for it.
    """
    # Case-insensitive check for CREATE TABLE ... <table_name>
    ddl_upper = _GENERATED_DDL.upper()
    create_stmt = f"CREATE TABLE IF NOT EXISTS {table_name}".upper()
    create_stmt_alt = f"CREATE TABLE {table_name}".upper()

    assert create_stmt not in ddl_upper, (
        f"Generated DDL still contains CREATE TABLE for removed table '{table_name}'"
    )
    assert create_stmt_alt not in ddl_upper, (
        f"Generated DDL still contains CREATE TABLE for removed table '{table_name}'"
    )


@settings(max_examples=20)
@given(table_name=sampled_from(REMOVED_TABLES))
def test_property1_is_super_user_excluded(table_name: str) -> None:
    """**Validates: Requirements 1.1, 3.1, 3.2, 13.6**

    The is_super_user column should NOT appear anywhere in the generated DDL.
    This is an extension of Property 1 — old authorization artifacts are fully
    removed.
    """
    ddl_upper = _GENERATED_DDL.upper()
    assert "IS_SUPER_USER" not in ddl_upper, (
        "Generated DDL still contains the is_super_user column"
    )


# ===================================================================
# Feature: simplified-authorization-layer
# Property 2: Retained tables are preserved in generated DDL
# Validates: Requirements 1.4
# ===================================================================


@settings(max_examples=20)
@given(table_name=sampled_from(RETAINED_TABLES))
def test_property2_retained_tables_present_in_ddl(table_name: str) -> None:
    """**Validates: Requirements 1.4**

    For any table name in the retained list, the generated DDL should contain
    a CREATE TABLE statement for it.
    """
    ddl_upper = _GENERATED_DDL.upper()
    create_stmt = f"CREATE TABLE IF NOT EXISTS {table_name}".upper()

    assert create_stmt in ddl_upper, (
        f"Generated DDL is missing CREATE TABLE for retained table '{table_name}'"
    )


@settings(max_examples=20)
@given(table_name=sampled_from(NEW_TABLES))
def test_property2_new_tables_present_in_ddl(table_name: str) -> None:
    """**Validates: Requirements 1.4**

    For any table name in the new tables list, the generated DDL should
    contain a CREATE TABLE statement for it.
    """
    ddl_upper = _GENERATED_DDL.upper()
    create_stmt = f"CREATE TABLE IF NOT EXISTS {table_name}".upper()

    assert create_stmt in ddl_upper, (
        f"Generated DDL is missing CREATE TABLE for new table '{table_name}'"
    )
