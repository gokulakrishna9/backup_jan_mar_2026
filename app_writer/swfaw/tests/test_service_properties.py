"""Property-based tests for service record ownership and role-based filtering (Properties 6, 10, 11).

Uses hypothesis to verify correctness properties of the generated
service Java code against the simplified authorization layer design.

Feature: simplified-authorization-layer
Property 6: USER role access is scoped to owned records
Property 10: Record ownership lifecycle
Property 11: Admin roles see unfiltered paginated results
"""

import sys
import importlib.util
from pathlib import Path

import pytest
from hypothesis import given, settings, assume
from hypothesis.strategies import (
    text,
    sampled_from,
    booleans,
    composite,
    lists,
    just,
)

# ---------------------------------------------------------------------------
# Direct-import service_templates, bypassing generators/__init__.py
# which pulls in unrelated dependencies (pypika, etc.).
# ---------------------------------------------------------------------------
_SWFAW_ROOT = Path(__file__).resolve().parent.parent

_tpl_spec = importlib.util.spec_from_file_location(
    "service_templates",
    _SWFAW_ROOT / "templates" / "service_templates.py",
)
_tpl_mod = importlib.util.module_from_spec(_tpl_spec)
sys.modules["templates.service_templates"] = _tpl_mod
_tpl_spec.loader.exec_module(_tpl_mod)

ServiceTemplates = _tpl_mod.ServiceTemplates

from jinja2 import Template

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

_TABLE_NAME_CHARS = "abcdefghijklmnopqrstuvwxyz_"
table_names = text(
    alphabet=_TABLE_NAME_CHARS, min_size=2, max_size=30
).filter(lambda s: s[0].isalpha() and not s.endswith("_") and "__" not in s)

_IDENT_CHARS = "abcdefghijklmnopqrstuvwxyz"
entity_names = text(
    alphabet=_IDENT_CHARS, min_size=2, max_size=20
).filter(lambda s: s[0].isalpha()).map(lambda s: s.capitalize())


def _render_service(
    table_name: str,
    entity_name: str,
    has_authorization: bool = True,
    has_soft_delete: bool = False,
    has_activity_tracking: bool = False,
    has_audit_fields: bool = False,
):
    """Render the service template with the given parameters."""
    id_field = f"{entity_name[0].lower()}{entity_name[1:]}Id"
    id_field_cap = f"{entity_name}Id"
    context = {
        "packageName": "com.example.service",
        "entityPackage": "com.example.entity",
        "dtoPackage": "com.example.dto",
        "repositoryPackage": "com.example.repository",
        "exceptionPackage": "com.example.exception",
        "servicePackage": "com.example.service",
        "securityPackage": "com.example.security",
        "entityName": entity_name,
        "className": f"{entity_name}Service",
        "repositoryName": f"{entity_name}Repository",
        "tableName": table_name,
        "idFieldCapitalized": id_field_cap,
        "hasAuthorization": has_authorization,
        "hasSoftDelete": has_soft_delete,
        "hasActivityTracking": has_activity_tracking,
        "hasAuditFields": has_audit_fields,
        "fields": [
            {"fieldName": "name", "fieldNameCapitalized": "Name"},
            {"fieldName": "description", "fieldNameCapitalized": "Description"},
        ],
        "outputFields": [
            {"fieldName": "name", "fieldNameCapitalized": "Name"},
            {"fieldName": "description", "fieldNameCapitalized": "Description"},
        ],
    }
    template = Template(ServiceTemplates.SERVICE_TEMPLATE)
    return template.render(context)


# ===================================================================
# Feature: simplified-authorization-layer
# Property 6: USER role access is scoped to owned records
# Validates: Requirements 5.8, 10.4
# ===================================================================


class TestProperty6UserRoleScopedToOwnedRecords:
    """Property 6: USER role access is scoped to owned records.

    For any USER role and any record, the service layer should include the
    record in findAllPaged results if and only if the user owns the record
    (via record_owner) or the record is shared with the user via a query
    group (via query_group_record).
    """

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_find_all_paged_checks_user_roles(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 5.8**

        When hasAuthorization=True, findAllPaged must check user roles
        to determine filtering behavior.
        """
        code = _render_service(table_name, entity_name, has_authorization=True)
        assert "user.getRoles()" in code, (
            "findAllPaged must call user.getRoles() to check role"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_find_all_paged_queries_group_member_for_user_role(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 10.4**

        For USER role, findAllPaged must query queryGroupMemberRepository
        to find the user's group memberships for ownership/sharing filtering.
        """
        code = _render_service(table_name, entity_name, has_authorization=True)
        assert "queryGroupMemberRepository.findByAuthUserId" in code, (
            "USER role findAllPaged must query queryGroupMemberRepository.findByAuthUserId"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_find_all_paged_filters_by_owned_or_shared(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 5.8, 10.4**

        For USER role, findAllPaged must filter by ownership (record_owner)
        OR query group sharing (query_group_record).
        """
        code = _render_service(table_name, entity_name, has_authorization=True)
        # The template uses OwnedOrShared methods for USER role filtering
        assert "OwnedOrShared" in code, (
            "USER role findAllPaged must use OwnedOrShared repository methods"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_find_all_paged_passes_table_name_for_filtering(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 10.4**

        The USER role filtering must pass the correct table name to the
        repository methods for record ownership lookup.
        """
        code = _render_service(table_name, entity_name, has_authorization=True)
        assert f'"{table_name}"' in code, (
            f"Service must pass tableName \"{table_name}\" for record ownership filtering"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_no_authorization_skips_role_filtering(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 5.8**

        When hasAuthorization=False, findAllPaged must NOT include
        role-based filtering logic.
        """
        code = _render_service(table_name, entity_name, has_authorization=False)
        assert "getRoles" not in code, (
            "Without authorization, findAllPaged must not check roles"
        )
        assert "queryGroupMemberRepository" not in code, (
            "Without authorization, findAllPaged must not query group memberships"
        )


# ===================================================================
# Feature: simplified-authorization-layer
# Property 10: Record ownership lifecycle
# Validates: Requirements 10.2, 10.3
# ===================================================================


class TestProperty10RecordOwnershipLifecycle:
    """Property 10: Record ownership lifecycle.

    For any record created via a service's create method, a corresponding
    row should exist in record_owner linking the authenticated user to the
    record. When the record is deleted, the record_owner row should also
    be deleted.
    """

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_create_saves_record_owner(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 10.2**

        When hasAuthorization=True, the create method must save a
        RecordOwner after saving the entity.
        """
        code = _render_service(table_name, entity_name, has_authorization=True)
        assert "RecordOwner.builder()" in code, (
            "Create method must build a RecordOwner"
        )
        assert "recordOwnerRepository.save(recordOwner)" in code, (
            "Create method must save the RecordOwner via recordOwnerRepository"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_create_record_owner_uses_correct_table_name(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 10.2**

        The RecordOwner created during entity creation must use the
        correct table name matching the entity's database table.
        """
        code = _render_service(table_name, entity_name, has_authorization=True)
        assert f'.tableName("{table_name}")' in code, (
            f"RecordOwner must use tableName(\"{table_name}\")"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_create_record_owner_links_auth_user(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 10.2**

        The RecordOwner must link the authenticated user's ID to the record.
        """
        code = _render_service(table_name, entity_name, has_authorization=True)
        assert ".authUserId(user.getAuthUserId())" in code, (
            "RecordOwner must set authUserId from the authenticated user"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_delete_removes_record_owner(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 10.3**

        When hasAuthorization=True, the delete method must remove the
        corresponding record_owner row.
        """
        code = _render_service(table_name, entity_name, has_authorization=True)
        assert f'recordOwnerRepository.deleteByTableNameAndRecordId("{table_name}"' in code, (
            "Delete method must call recordOwnerRepository.deleteByTableNameAndRecordId"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_delete_with_justification_removes_record_owner(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 10.3**

        When hasAuthorization=True, the deleteWithJustification method
        must also remove the corresponding record_owner row.
        """
        code = _render_service(table_name, entity_name, has_authorization=True)
        # deleteByTableNameAndRecordId should appear at least twice
        # (once for delete, once for deleteWithJustification)
        occurrences = code.count(
            f'recordOwnerRepository.deleteByTableNameAndRecordId("{table_name}"'
        )
        assert occurrences >= 2, (
            f"Expected at least 2 calls to deleteByTableNameAndRecordId "
            f"(delete + deleteWithJustification), found {occurrences}"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_no_authorization_skips_record_owner(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 10.2, 10.3**

        When hasAuthorization=False, the service must NOT reference
        RecordOwner or recordOwnerRepository.
        """
        code = _render_service(table_name, entity_name, has_authorization=False)
        assert "RecordOwner" not in code, (
            "Without authorization, service must not reference RecordOwner"
        )
        assert "recordOwnerRepository" not in code, (
            "Without authorization, service must not reference recordOwnerRepository"
        )


# ===================================================================
# Feature: simplified-authorization-layer
# Property 11: Admin roles see unfiltered paginated results
# Validates: Requirements 10.5
# ===================================================================


class TestProperty11AdminRolesSeeUnfilteredResults:
    """Property 11: Admin roles see unfiltered paginated results.

    For any TABLE_ADMIN or SUPER_ADMIN user, the service findAllPaged
    method should return paginated results from the full table without
    ownership filtering.
    """

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_find_all_paged_has_admin_check(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 10.5**

        When hasAuthorization=True, findAllPaged must check if the user
        is an admin (SUPER_ADMIN or TABLE_ADMIN).
        """
        code = _render_service(table_name, entity_name, has_authorization=True)
        assert "isAdmin" in code, (
            "findAllPaged must have an isAdmin check"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_admin_check_includes_super_admin(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 10.5**

        The admin check must include SUPER_ADMIN role.
        """
        code = _render_service(table_name, entity_name, has_authorization=True)
        assert '"SUPER_ADMIN"' in code, (
            "Admin check must reference SUPER_ADMIN"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_admin_check_includes_table_admin(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 10.5**

        The admin check must include TABLE_ADMIN role.
        """
        code = _render_service(table_name, entity_name, has_authorization=True)
        assert '"TABLE_ADMIN"' in code, (
            "Admin check must reference TABLE_ADMIN"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_admin_gets_unfiltered_paginated_results(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 10.5**

        For admin users, findAllPaged must use the standard (unfiltered)
        pagination methods, not the OwnedOrShared variants.
        """
        code = _render_service(table_name, entity_name, has_authorization=True)
        # The admin branch should use findAllPaged (not findAllPagedOwnedOrShared)
        # and countAll (not countOwnedOrShared)
        # Find the isAdmin branch — it should contain standard pagination
        admin_idx = code.index("if (isAdmin)")
        # Find the else branch for non-admin
        else_idx = code.index("} else {", admin_idx)
        admin_branch = code[admin_idx:else_idx]
        # Admin branch should use standard pagination (findAllPaged or countAll)
        has_standard = (
            "findAllPaged" in admin_branch or "countAll" in admin_branch
            or "findAllPagedByDeletedAtIsNull" in admin_branch
            or "countByDeletedAtIsNull" in admin_branch
        )
        assert has_standard, (
            "Admin branch must use standard (unfiltered) pagination methods"
        )
        # Admin branch should NOT use OwnedOrShared methods
        assert "OwnedOrShared" not in admin_branch, (
            "Admin branch must NOT use OwnedOrShared filtering methods"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_non_admin_uses_ownership_filtering(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 10.5**

        For non-admin (USER role) users, findAllPaged must use the
        OwnedOrShared filtering methods.
        """
        code = _render_service(table_name, entity_name, has_authorization=True)
        admin_idx = code.index("if (isAdmin)")
        else_idx = code.index("} else {", admin_idx)
        # Get the else branch (non-admin / USER role)
        # Find the closing of the else block
        non_admin_branch = code[else_idx:]
        assert "OwnedOrShared" in non_admin_branch, (
            "Non-admin branch must use OwnedOrShared filtering methods"
        )
