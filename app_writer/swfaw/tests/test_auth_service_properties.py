"""Property-based tests for community group auto-creation at registration (Property 13).

Uses hypothesis to verify correctness properties of the generated
AuthService Java code against the simplified authorization layer design.

Feature: simplified-authorization-layer
Property 13: Community group auto-creation at registration
"""

import sys
import importlib.util
from pathlib import Path

import pytest
from hypothesis import given, settings, assume
from hypothesis.strategies import (
    text,
    composite,
)

# ---------------------------------------------------------------------------
# Direct-import auth_service_templates, bypassing generators/__init__.py
# ---------------------------------------------------------------------------
_SWFAW_ROOT = Path(__file__).resolve().parent.parent

_tpl_spec = importlib.util.spec_from_file_location(
    "auth_service_templates",
    _SWFAW_ROOT / "templates" / "auth_service_templates.py",
)
_tpl_mod = importlib.util.module_from_spec(_tpl_spec)
sys.modules["templates.auth_service_templates"] = _tpl_mod
_tpl_spec.loader.exec_module(_tpl_mod)

AuthServiceTemplates = _tpl_mod.AuthServiceTemplates

from jinja2 import Template

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

_IDENT_CHARS = "abcdefghijklmnopqrstuvwxyz"
usernames = text(
    alphabet=_IDENT_CHARS, min_size=3, max_size=20
).filter(lambda s: s[0].isalpha())


def _render_auth_service() -> str:
    """Render the AuthService template."""
    context = {
        "packageName": "com.example.service",
        "entityPackage": "com.example.entity",
        "repositoryPackage": "com.example.repository",
        "authPackage": "com.example.auth",
    }
    template = Template(AuthServiceTemplates.AUTH_SERVICE)
    return template.render(context)


# ===================================================================
# Feature: simplified-authorization-layer
# Property 13: Community group auto-creation at registration
# Validates: Requirements 15.1, 15.2, 15.3
# ===================================================================


class TestProperty13CommunityGroupAutoCreation:
    """Property 13: Community group auto-creation at registration.

    For any newly registered user, the registration flow should create a
    query_group with group_type='COMMUNITY' and owner_auth_user_id set to
    the new user, add the user as a member of that group, and populate
    the group with community-default queries from the app definition.
    """

    @settings(max_examples=20)
    @given(username=usernames)
    def test_registration_creates_community_query_group(self, username: str) -> None:
        """**Validates: Requirements 15.1**

        Registration must create a QueryGroup with group_type COMMUNITY.
        """
        code = _render_auth_service()
        assert "QueryGroup.builder()" in code, (
            "Registration must build a QueryGroup"
        )
        assert 'groupType("COMMUNITY")' in code, (
            "Registration must set groupType to COMMUNITY"
        )

    @settings(max_examples=20)
    @given(username=usernames)
    def test_community_group_has_owner_set_to_new_user(self, username: str) -> None:
        """**Validates: Requirements 15.1**

        The Community group must have ownerAuthUserId set to the
        newly registered user's ID.
        """
        code = _render_auth_service()
        assert "ownerAuthUserId(savedUser.getAuthUserId())" in code, (
            "Community group must set ownerAuthUserId to the new user's ID"
        )

    @settings(max_examples=20)
    @given(username=usernames)
    def test_community_group_saved_via_repository(self, username: str) -> None:
        """**Validates: Requirements 15.1**

        The Community group must be saved via queryGroupRepository.
        """
        code = _render_auth_service()
        assert "queryGroupRepository.save(communityGroup)" in code, (
            "Community group must be saved via queryGroupRepository"
        )

    @settings(max_examples=20)
    @given(username=usernames)
    def test_user_added_as_member_of_community_group(self, username: str) -> None:
        """**Validates: Requirements 15.2**

        The newly registered user must be added as a member of the
        Community group via queryGroupMemberRepository.
        """
        code = _render_auth_service()
        assert "QueryGroupMember.builder()" in code, (
            "Registration must build a QueryGroupMember"
        )
        assert "queryGroupMemberRepository.save(member)" in code, (
            "Registration must save the member via queryGroupMemberRepository"
        )

    @settings(max_examples=20)
    @given(username=usernames)
    def test_member_links_to_correct_group_and_user(self, username: str) -> None:
        """**Validates: Requirements 15.2**

        The QueryGroupMember must link the correct group ID and user ID.
        """
        code = _render_auth_service()
        assert "savedGroup.getQueryGroupId()" in code, (
            "Member must reference the saved group's ID"
        )
        assert "savedUser.getAuthUserId()" in code, (
            "Member must reference the saved user's ID"
        )

    @settings(max_examples=20)
    @given(username=usernames)
    def test_community_group_populated_with_default_queries(self, username: str) -> None:
        """**Validates: Requirements 15.3**

        The Community group must be populated with community-default
        queries from the app definition via queryGroupQueryRepository.
        """
        code = _render_auth_service()
        assert "populateCommunityDefaultQueries" in code, (
            "Registration must call populateCommunityDefaultQueries"
        )
        assert "QueryGroupQuery.builder()" in code, (
            "populateCommunityDefaultQueries must build QueryGroupQuery entries"
        )
        assert "queryGroupQueryRepository.save(groupQuery)" in code, (
            "populateCommunityDefaultQueries must save via queryGroupQueryRepository"
        )

    @settings(max_examples=20)
    @given(username=usernames)
    def test_login_response_does_not_include_is_super_user(self, username: str) -> None:
        """**Validates: Requirements 15.1**

        LoginResponse must not include isSuperUser field.
        """
        code = _render_auth_service()
        # Find the LoginResponse record definition
        lr_idx = code.index("public record LoginResponse(")
        lr_end = code.index(")", lr_idx)
        lr_def = code[lr_idx:lr_end]
        assert "isSuperUser" not in lr_def, (
            "LoginResponse must not include isSuperUser field"
        )

    @settings(max_examples=20)
    @given(username=usernames)
    def test_no_is_super_user_in_user_builder(self, username: str) -> None:
        """**Validates: Requirements 15.1**

        The AuthUser builder in registration must not set isSuperUser.
        """
        code = _render_auth_service()
        # Find the register method's user builder
        reg_idx = code.index("public Mono<RegisterResponse> register(")
        reg_section = code[reg_idx:reg_idx + 2000]
        assert ".isSuperUser(" not in reg_section, (
            "Registration user builder must not set isSuperUser"
        )
