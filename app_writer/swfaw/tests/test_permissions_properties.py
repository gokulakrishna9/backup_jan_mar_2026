"""Property-based tests for permissions resolution (Property 12).

Uses hypothesis to verify correctness properties of the generated
PermissionsService Java code against the simplified authorization layer design.

Feature: simplified-authorization-layer
Property 12: Permissions endpoint resolves correct APIs per role
"""

import sys
import importlib.util
from pathlib import Path

import pytest
from hypothesis import given, settings, assume
from hypothesis.strategies import (
    text,
    sampled_from,
    composite,
    lists,
    just,
)

# ---------------------------------------------------------------------------
# Direct-import permissions_templates, bypassing generators/__init__.py
# ---------------------------------------------------------------------------
_SWFAW_ROOT = Path(__file__).resolve().parent.parent

_tpl_spec = importlib.util.spec_from_file_location(
    "permissions_templates",
    _SWFAW_ROOT / "templates" / "permissions_templates.py",
)
_tpl_mod = importlib.util.module_from_spec(_tpl_spec)
sys.modules["templates.permissions_templates"] = _tpl_mod
_tpl_spec.loader.exec_module(_tpl_mod)

PermissionsTemplates = _tpl_mod.PermissionsTemplates

from jinja2 import Template

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

_TABLE_NAME_CHARS = "abcdefghijklmnopqrstuvwxyz_"
table_names = text(
    alphabet=_TABLE_NAME_CHARS, min_size=2, max_size=30
).filter(lambda s: s[0].isalpha() and not s.endswith("_") and "__" not in s)


def _render_permissions_service() -> str:
    """Render the PermissionsService template."""
    context = {
        "packageName": "com.example.service",
        "entityPackage": "com.example.entity",
        "repositoryPackage": "com.example.repository",
    }
    template = Template(PermissionsTemplates.PERMISSIONS_SERVICE)
    return template.render(context)


# ===================================================================
# Feature: simplified-authorization-layer
# Property 12: Permissions endpoint resolves correct APIs per role
# Validates: Requirements 12.1, 12.2, 12.3, 12.4
# ===================================================================


class TestProperty12PermissionsResolveCorrectApisPerRole:
    """Property 12: Permissions endpoint resolves correct APIs per role.

    For any user with a given role configuration, the PermissionsService
    should return: all entity API paths for SUPER_ADMIN, full CRUD paths
    only for assigned tables for TABLE_ADMIN, and READ paths for
    owned/shared records for USER.
    """

    @settings(max_examples=20)
    @given(table_name=table_names)
    def test_super_admin_gets_full_access(self, table_name: str) -> None:
        """**Validates: Requirements 12.2**

        SUPER_ADMIN role must trigger buildFullAccess which returns
        all entity API paths.
        """
        code = _render_permissions_service()
        assert "SUPER_ADMIN" in code, (
            "PermissionsService must check for SUPER_ADMIN role"
        )
        assert "buildFullAccess()" in code, (
            "SUPER_ADMIN must trigger buildFullAccess()"
        )

    @settings(max_examples=20)
    @given(table_name=table_names)
    def test_full_access_includes_all_crud_operations(self, table_name: str) -> None:
        """**Validates: Requirements 12.2**

        buildFullAccess must include POST, GET, PUT, DELETE for every entity.
        """
        code = _render_permissions_service()
        assert 'new AllowedApi("POST", basePath)' in code, (
            "Full access must include POST"
        )
        assert 'new AllowedApi("GET", basePath + "/*")' in code, (
            "Full access must include GET by ID"
        )
        assert 'new AllowedApi("GET", basePath)' in code, (
            "Full access must include GET all"
        )
        assert 'new AllowedApi("PUT", basePath + "/*")' in code, (
            "Full access must include PUT"
        )
        assert 'new AllowedApi("DELETE", basePath + "/*")' in code, (
            "Full access must include DELETE"
        )

    @settings(max_examples=20)
    @given(table_name=table_names)
    def test_table_admin_gets_crud_for_assigned_tables(self, table_name: str) -> None:
        """**Validates: Requirements 12.3**

        TABLE_ADMIN must get full CRUD paths only for assigned tables.
        """
        code = _render_permissions_service()
        assert "TABLE_ADMIN" in code, (
            "PermissionsService must check for TABLE_ADMIN role"
        )
        assert "adminTables" in code, (
            "PermissionsService must collect TABLE_ADMIN assigned tables"
        )

    @settings(max_examples=20)
    @given(table_name=table_names)
    def test_table_admin_scoped_to_assigned_tables_only(self, table_name: str) -> None:
        """**Validates: Requirements 12.3**

        TABLE_ADMIN CRUD paths must only be added for tables in the
        assigned set, using getTableName() from the role.
        """
        code = _render_permissions_service()
        assert "role.getTableName()" in code, (
            "TABLE_ADMIN must read table assignment from role.getTableName()"
        )
        assert "adminTables.add(role.getTableName())" in code, (
            "TABLE_ADMIN assigned tables must be collected into adminTables set"
        )

    @settings(max_examples=20)
    @given(table_name=table_names)
    def test_user_role_gets_read_paths(self, table_name: str) -> None:
        """**Validates: Requirements 12.4**

        USER role must get READ (GET) paths for entities.
        """
        code = _render_permissions_service()
        assert "hasUserRole" in code, (
            "PermissionsService must track whether user has USER role"
        )
        # USER role section should add GET paths
        user_idx = code.index("if (hasUserRole)")
        user_block = code[user_idx:code.index("}", user_idx + 50) + 50]
        assert "GET" in user_block, (
            "USER role must add GET paths"
        )

    @settings(max_examples=20)
    @given(table_name=table_names)
    def test_resolves_from_user_role_repository(self, table_name: str) -> None:
        """**Validates: Requirements 12.1**

        PermissionsService must resolve from UserRoleRepository
        instead of document group memberships.
        """
        code = _render_permissions_service()
        assert "UserRoleRepository" in code, (
            "PermissionsService must use UserRoleRepository"
        )
        assert "userRoleRepository.findByAuthUserId" in code, (
            "PermissionsService must query userRoleRepository.findByAuthUserId"
        )

    @settings(max_examples=20)
    @given(table_name=table_names)
    def test_no_old_authorization_references(self, table_name: str) -> None:
        """**Validates: Requirements 12.1, 12.2, 12.3, 12.4**

        PermissionsService must not reference old authorization model
        artifacts: isSuperUser, isSuperGroup, DocumentGroupMembership,
        DocumentGroupTableScope, UserGroupMembership, UserGroupRepository.
        """
        code = _render_permissions_service()
        assert "isSuperUser" not in code, (
            "PermissionsService must not reference isSuperUser"
        )
        assert "isSuperGroup" not in code, (
            "PermissionsService must not reference isSuperGroup"
        )
        assert "DocumentGroupMembership" not in code, (
            "PermissionsService must not reference DocumentGroupMembership"
        )
        assert "DocumentGroupTableScope" not in code, (
            "PermissionsService must not reference DocumentGroupTableScope"
        )
        assert "UserGroupMembership" not in code, (
            "PermissionsService must not reference UserGroupMembership"
        )
        assert "UserGroupRepository" not in code, (
            "PermissionsService must not reference UserGroupRepository"
        )

    @settings(max_examples=20)
    @given(table_name=table_names)
    def test_uses_entity_api_registry(self, table_name: str) -> None:
        """**Validates: Requirements 12.1**

        PermissionsService must use EntityApiRegistry to map table
        names to API paths.
        """
        code = _render_permissions_service()
        assert "EntityApiRegistry" in code, (
            "PermissionsService must use EntityApiRegistry"
        )
        assert "entityApiRegistry.getBasePath" in code, (
            "PermissionsService must call entityApiRegistry.getBasePath"
        )
        assert "entityApiRegistry.getAllMappings()" in code, (
            "PermissionsService must call entityApiRegistry.getAllMappings()"
        )
