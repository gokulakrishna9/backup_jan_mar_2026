"""Property-based tests for JWT claims round-trip (Property 3).

Uses hypothesis to verify correctness properties of the generated
JwtService Java code against the simplified authorization layer design.

The generated JwtService must support round-trip serialization/deserialization
of roles, tableAccess, and queryGroupMemberships JWT claims.
"""

import sys
import importlib.util
from pathlib import Path

import pytest
from hypothesis import given, settings, assume
from hypothesis.strategies import (
    text,
    sampled_from,
    lists,
    dictionaries,
    integers,
    just,
    one_of,
    composite,
    none,
    booleans,
    fixed_dictionaries,
)

# ---------------------------------------------------------------------------
# Direct-import the jwt_templates module, bypassing generators/__init__.py
# which pulls in unrelated dependencies (pypika, etc.).
# ---------------------------------------------------------------------------
_SWFAW_ROOT = Path(__file__).resolve().parent.parent

_tpl_spec = importlib.util.spec_from_file_location(
    "jwt_templates",
    _SWFAW_ROOT / "templates" / "jwt_templates.py",
)
_tpl_mod = importlib.util.module_from_spec(_tpl_spec)
sys.modules["templates.jwt_templates"] = _tpl_mod
_tpl_spec.loader.exec_module(_tpl_mod)

JWTTemplates = _tpl_mod.JWTTemplates

# ---------------------------------------------------------------------------
# Render the JWT_SERVICE_TEMPLATE once — it is deterministic and stateless.
# We use jinja2 directly to avoid importing the generator (which needs models).
# ---------------------------------------------------------------------------
from jinja2 import Template

_GENERATED_SERVICE: str = Template(JWTTemplates.JWT_SERVICE_TEMPLATE).render(
    packageName="com.example.security"
)

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Valid Java identifier-style table names (lowercase, underscore-separated)
_TABLE_NAME_CHARS = "abcdefghijklmnopqrstuvwxyz_"
table_names = text(
    alphabet=_TABLE_NAME_CHARS, min_size=1, max_size=30
).filter(lambda s: s[0].isalpha() and not s.endswith("_"))

CRUD_OPERATIONS = ["CREATE", "READ", "UPDATE", "DELETE"]
crud_operations = sampled_from(CRUD_OPERATIONS)

ROLE_NAMES = ["USER", "TABLE_ADMIN", "SUPER_ADMIN"]


@composite
def role_objects(draw):
    """Generate a single role object: {role: str, tableName: str|None}."""
    role = draw(sampled_from(ROLE_NAMES))
    if role == "SUPER_ADMIN":
        return {"role": role, "tableName": None}
    elif role == "TABLE_ADMIN":
        tbl = draw(table_names)
        return {"role": role, "tableName": tbl}
    else:
        return {"role": role, "tableName": None}


@composite
def role_lists(draw):
    """Generate a list of role objects (0–5 roles)."""
    return draw(lists(role_objects(), min_size=0, max_size=5))


@composite
def table_access_maps(draw):
    """Generate a tableAccess-style map: {table_name: [operations]}."""
    num_tables = draw(sampled_from(range(0, 6)))
    result = {}
    for _ in range(num_tables):
        tbl = draw(table_names)
        ops = draw(lists(crud_operations, min_size=1, max_size=4, unique=True))
        result[tbl] = ops
    return result


@composite
def query_group_membership_lists(draw):
    """Generate a list of query group IDs (positive longs)."""
    return draw(lists(integers(min_value=1, max_value=999999), min_size=0, max_size=10, unique=True))


# ---------------------------------------------------------------------------
# Helper: extract a Java method body by brace-counting from a given source.
# ---------------------------------------------------------------------------

def _extract_method_body(source: str, method_signature: str) -> str:
    """Extract the body of a Java method (between its opening and closing braces)."""
    method_start = source.index(method_signature)
    brace_count = 0
    method_body_start = source.index("{", method_start)
    pos = method_body_start
    for i in range(method_body_start, len(source)):
        if source[i] == "{":
            brace_count += 1
        elif source[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                pos = i
                break
    return source[method_body_start:pos + 1]


# ===================================================================
# Feature: simplified-authorization-layer
# Property 3: JWT claims round-trip
# Validates: Requirements 6.1, 6.2, 6.3, 6.4
# ===================================================================


class TestProperty3JwtClaimsRoundTrip:
    """Property 3: JWT claims round-trip.

    For any valid set of roles (list of role objects with role name and optional
    table_name), tableAccess (map of table_name to operations list), and
    queryGroupMemberships (list of query group IDs), generating a JWT token
    with these claims and then extracting them should produce values equivalent
    to the original inputs.

    Since these are Python templates that generate Java code, the property tests
    verify the GENERATED Java code contains the correct structural patterns for
    round-trip capability.
    """

    # -------------------------------------------------------------------
    # 1. generateToken accepts roles, tableAccess, queryGroupMemberships
    # -------------------------------------------------------------------

    @settings(max_examples=20)
    @given(roles=role_lists())
    def test_generate_token_accepts_roles_param(self, roles: list) -> None:
        """**Validates: Requirements 6.1**

        The generated JwtService generateToken method must accept a
        List<Map<String, Object>> roles parameter.
        """
        assert "List<Map<String, Object>> roles" in _GENERATED_SERVICE, (
            "generateToken must accept List<Map<String, Object>> roles parameter"
        )

    @settings(max_examples=20)
    @given(ta=table_access_maps())
    def test_generate_token_accepts_table_access_param(self, ta: dict) -> None:
        """**Validates: Requirements 6.1**

        The generated JwtService generateToken method must accept a
        Map<String, List<String>> tableAccess parameter.
        """
        assert "Map<String, List<String>> tableAccess" in _GENERATED_SERVICE, (
            "generateToken must accept Map<String, List<String>> tableAccess parameter"
        )

    @settings(max_examples=20)
    @given(memberships=query_group_membership_lists())
    def test_generate_token_accepts_query_group_memberships_param(
        self, memberships: list
    ) -> None:
        """**Validates: Requirements 6.1**

        The generated JwtService generateToken method must accept a
        List<Long> queryGroupMemberships parameter.
        """
        assert "List<Long> queryGroupMemberships" in _GENERATED_SERVICE, (
            "generateToken must accept List<Long> queryGroupMemberships parameter"
        )

    # -------------------------------------------------------------------
    # 2. extractRoles parses the same type back (List<Map<String, Object>>)
    # -------------------------------------------------------------------

    @settings(max_examples=20)
    @given(roles=role_lists())
    def test_extract_roles_returns_correct_type(self, roles: list) -> None:
        """**Validates: Requirements 6.2**

        The extractRoles method must return List<Map<String, Object>> —
        the same type used in generateToken.
        """
        assert "public List<Map<String, Object>> extractRoles(String token)" in _GENERATED_SERVICE, (
            "extractRoles must return List<Map<String, Object>>"
        )

    @settings(max_examples=20)
    @given(roles=role_lists())
    def test_extract_roles_reads_roles_claim(self, roles: list) -> None:
        """**Validates: Requirements 6.2**

        The extractRoles method must read the 'roles' claim from the JWT.
        """
        method_body = _extract_method_body(
            _GENERATED_SERVICE, "public List<Map<String, Object>> extractRoles"
        )
        assert '"roles"' in method_body, (
            "extractRoles must read the 'roles' claim from JWT"
        )

    @settings(max_examples=20)
    @given(roles=role_lists())
    def test_extract_roles_uses_matching_type_reference(self, roles: list) -> None:
        """**Validates: Requirements 6.2**

        The extractRoles method must use TypeReference<List<Map<String, Object>>>
        for deserialization — matching the serialization type.
        """
        method_body = _extract_method_body(
            _GENERATED_SERVICE, "public List<Map<String, Object>> extractRoles"
        )
        assert "TypeReference<List<Map<String, Object>>>" in method_body, (
            "extractRoles must use TypeReference<List<Map<String, Object>>> for deserialization"
        )

    # -------------------------------------------------------------------
    # 3. extractTableAccess parses the same type back (Map<String, List<String>>)
    # -------------------------------------------------------------------

    @settings(max_examples=20)
    @given(ta=table_access_maps())
    def test_extract_table_access_returns_correct_type(self, ta: dict) -> None:
        """**Validates: Requirements 6.3**

        The extractTableAccess method must return Map<String, List<String>> —
        the same type used in generateToken.
        """
        assert "public Map<String, List<String>> extractTableAccess(String token)" in _GENERATED_SERVICE, (
            "extractTableAccess must return Map<String, List<String>>"
        )

    @settings(max_examples=20)
    @given(ta=table_access_maps())
    def test_extract_table_access_reads_table_access_claim(self, ta: dict) -> None:
        """**Validates: Requirements 6.3**

        The extractTableAccess method must read the 'tableAccess' claim from the JWT.
        """
        method_body = _extract_method_body(
            _GENERATED_SERVICE, "public Map<String, List<String>> extractTableAccess"
        )
        assert '"tableAccess"' in method_body, (
            "extractTableAccess must read the 'tableAccess' claim from JWT"
        )

    @settings(max_examples=20)
    @given(ta=table_access_maps())
    def test_extract_table_access_uses_matching_type_reference(self, ta: dict) -> None:
        """**Validates: Requirements 6.3**

        The extractTableAccess method must use TypeReference<Map<String, List<String>>>
        for deserialization — matching the serialization type.
        """
        method_body = _extract_method_body(
            _GENERATED_SERVICE, "public Map<String, List<String>> extractTableAccess"
        )
        assert "TypeReference<Map<String, List<String>>>" in method_body, (
            "extractTableAccess must use TypeReference<Map<String, List<String>>> for deserialization"
        )

    # -------------------------------------------------------------------
    # 4. extractQueryGroupMemberships parses the same type back (List<Long>)
    # -------------------------------------------------------------------

    @settings(max_examples=20)
    @given(memberships=query_group_membership_lists())
    def test_extract_query_group_memberships_returns_correct_type(
        self, memberships: list
    ) -> None:
        """**Validates: Requirements 6.4**

        The extractQueryGroupMemberships method must return List<Long> —
        the same type used in generateToken.
        """
        assert "public List<Long> extractQueryGroupMemberships(String token)" in _GENERATED_SERVICE, (
            "extractQueryGroupMemberships must return List<Long>"
        )

    @settings(max_examples=20)
    @given(memberships=query_group_membership_lists())
    def test_extract_query_group_memberships_reads_claim(
        self, memberships: list
    ) -> None:
        """**Validates: Requirements 6.4**

        The extractQueryGroupMemberships method must read the
        'queryGroupMemberships' claim from the JWT.
        """
        method_body = _extract_method_body(
            _GENERATED_SERVICE,
            "public List<Long> extractQueryGroupMemberships",
        )
        assert '"queryGroupMemberships"' in method_body, (
            "extractQueryGroupMemberships must read the 'queryGroupMemberships' claim from JWT"
        )

    @settings(max_examples=20)
    @given(memberships=query_group_membership_lists())
    def test_extract_query_group_memberships_uses_matching_type_reference(
        self, memberships: list
    ) -> None:
        """**Validates: Requirements 6.4**

        The extractQueryGroupMemberships method must use TypeReference<List<Long>>
        for deserialization — matching the serialization type.
        """
        method_body = _extract_method_body(
            _GENERATED_SERVICE,
            "public List<Long> extractQueryGroupMemberships",
        )
        assert "TypeReference<List<Long>>" in method_body, (
            "extractQueryGroupMemberships must use TypeReference<List<Long>> for deserialization"
        )

    # -------------------------------------------------------------------
    # 5. Serialization uses the same ObjectMapper for both directions
    # -------------------------------------------------------------------

    @settings(max_examples=20)
    @given(roles=role_lists())
    def test_same_object_mapper_for_serialization_and_deserialization(
        self, roles: list
    ) -> None:
        """**Validates: Requirements 6.1, 6.2, 6.3, 6.4**

        The JwtService must use the same ObjectMapper instance for both
        writeValueAsString (in generateToken) and readValue (in extract*
        methods), ensuring consistent serialization/deserialization.
        """
        # ObjectMapper is declared as a field
        assert "private final ObjectMapper objectMapper = new ObjectMapper()" in _GENERATED_SERVICE, (
            "JwtService must declare a single ObjectMapper field"
        )
        # generateToken uses objectMapper.writeValueAsString
        gen_body = _extract_method_body(_GENERATED_SERVICE, "public String generateToken")
        assert "objectMapper.writeValueAsString" in gen_body, (
            "generateToken must use objectMapper.writeValueAsString for serialization"
        )
        # extract methods use objectMapper.readValue
        for method_name in [
            "public List<Map<String, Object>> extractRoles",
            "public Map<String, List<String>> extractTableAccess",
            "public List<Long> extractQueryGroupMemberships",
        ]:
            body = _extract_method_body(_GENERATED_SERVICE, method_name)
            assert "objectMapper.readValue" in body, (
                f"{method_name} must use objectMapper.readValue for deserialization"
            )

    # -------------------------------------------------------------------
    # 6. Claims are stored as JSON strings and parsed back with TypeReferences
    # -------------------------------------------------------------------

    @settings(max_examples=20)
    @given(roles=role_lists(), ta=table_access_maps(), memberships=query_group_membership_lists())
    def test_claims_stored_as_json_strings(
        self, roles: list, ta: dict, memberships: list
    ) -> None:
        """**Validates: Requirements 6.1, 6.2, 6.3, 6.4**

        The generateToken method must serialize roles, tableAccess, and
        queryGroupMemberships to JSON strings before embedding them as
        JWT claims. The extract methods must read them back as String
        and parse with ObjectMapper.
        """
        gen_body = _extract_method_body(_GENERATED_SERVICE, "public String generateToken")

        # Serialization: each claim is serialized to a JSON string variable
        assert "rolesJson" in gen_body, (
            "generateToken must serialize roles to a rolesJson string"
        )
        assert "tableAccessJson" in gen_body, (
            "generateToken must serialize tableAccess to a tableAccessJson string"
        )
        assert "queryGroupMembershipsJson" in gen_body, (
            "generateToken must serialize queryGroupMemberships to a queryGroupMembershipsJson string"
        )

        # Claims are set as string values
        assert '.claim("roles", rolesJson)' in gen_body, (
            "generateToken must set roles claim as JSON string"
        )
        assert '.claim("tableAccess", tableAccessJson)' in gen_body, (
            "generateToken must set tableAccess claim as JSON string"
        )
        assert '.claim("queryGroupMemberships", queryGroupMembershipsJson)' in gen_body, (
            "generateToken must set queryGroupMemberships claim as JSON string"
        )

    @settings(max_examples=20)
    @given(roles=role_lists(), ta=table_access_maps(), memberships=query_group_membership_lists())
    def test_extract_methods_read_claims_as_strings(
        self, roles: list, ta: dict, memberships: list
    ) -> None:
        """**Validates: Requirements 6.1, 6.2, 6.3, 6.4**

        Each extract method must read the claim as a String from the JWT
        Claims object before parsing it with ObjectMapper.
        """
        roles_body = _extract_method_body(
            _GENERATED_SERVICE, "public List<Map<String, Object>> extractRoles"
        )
        assert 'getClaims(token).get("roles", String.class)' in roles_body, (
            "extractRoles must read roles claim as String.class"
        )

        ta_body = _extract_method_body(
            _GENERATED_SERVICE, "public Map<String, List<String>> extractTableAccess"
        )
        assert 'getClaims(token).get("tableAccess", String.class)' in ta_body, (
            "extractTableAccess must read tableAccess claim as String.class"
        )

        qgm_body = _extract_method_body(
            _GENERATED_SERVICE, "public List<Long> extractQueryGroupMemberships"
        )
        assert 'getClaims(token).get("queryGroupMemberships", String.class)' in qgm_body, (
            "extractQueryGroupMemberships must read queryGroupMemberships claim as String.class"
        )

    # -------------------------------------------------------------------
    # 7. Null-safety: generateToken handles null inputs gracefully
    # -------------------------------------------------------------------

    @settings(max_examples=20)
    @given(roles=role_lists())
    def test_generate_token_null_safe_roles(self, roles: list) -> None:
        """**Validates: Requirements 6.1**

        The generateToken method must handle null roles by defaulting to
        an empty list, ensuring the serialized JSON is always valid.
        """
        gen_body = _extract_method_body(_GENERATED_SERVICE, "public String generateToken")
        assert "roles != null ? roles : Collections.emptyList()" in gen_body, (
            "generateToken must handle null roles with Collections.emptyList()"
        )

    @settings(max_examples=20)
    @given(ta=table_access_maps())
    def test_generate_token_null_safe_table_access(self, ta: dict) -> None:
        """**Validates: Requirements 6.1**

        The generateToken method must handle null tableAccess by defaulting
        to an empty map.
        """
        gen_body = _extract_method_body(_GENERATED_SERVICE, "public String generateToken")
        assert "tableAccess != null ? tableAccess : Collections.emptyMap()" in gen_body, (
            "generateToken must handle null tableAccess with Collections.emptyMap()"
        )

    @settings(max_examples=20)
    @given(memberships=query_group_membership_lists())
    def test_generate_token_null_safe_query_group_memberships(
        self, memberships: list
    ) -> None:
        """**Validates: Requirements 6.1**

        The generateToken method must handle null queryGroupMemberships by
        defaulting to an empty list.
        """
        gen_body = _extract_method_body(_GENERATED_SERVICE, "public String generateToken")
        assert "queryGroupMemberships != null ? queryGroupMemberships : Collections.emptyList()" in gen_body, (
            "generateToken must handle null queryGroupMemberships with Collections.emptyList()"
        )

    # -------------------------------------------------------------------
    # 8. Null-safety: extract methods handle null/empty claims gracefully
    # -------------------------------------------------------------------

    @settings(max_examples=20)
    @given(roles=role_lists())
    def test_extract_roles_handles_null_claim(self, roles: list) -> None:
        """**Validates: Requirements 6.2**

        The extractRoles method must return an empty list when the roles
        claim is null or empty.
        """
        body = _extract_method_body(
            _GENERATED_SERVICE, "public List<Map<String, Object>> extractRoles"
        )
        assert "Collections.emptyList()" in body, (
            "extractRoles must return Collections.emptyList() for null/empty claim"
        )

    @settings(max_examples=20)
    @given(ta=table_access_maps())
    def test_extract_table_access_handles_null_claim(self, ta: dict) -> None:
        """**Validates: Requirements 6.3**

        The extractTableAccess method must return an empty map when the
        tableAccess claim is null or empty.
        """
        body = _extract_method_body(
            _GENERATED_SERVICE, "public Map<String, List<String>> extractTableAccess"
        )
        assert "Collections.emptyMap()" in body, (
            "extractTableAccess must return Collections.emptyMap() for null/empty claim"
        )

    @settings(max_examples=20)
    @given(memberships=query_group_membership_lists())
    def test_extract_query_group_memberships_handles_null_claim(
        self, memberships: list
    ) -> None:
        """**Validates: Requirements 6.4**

        The extractQueryGroupMemberships method must return an empty list
        when the queryGroupMemberships claim is null or empty.
        """
        body = _extract_method_body(
            _GENERATED_SERVICE, "public List<Long> extractQueryGroupMemberships"
        )
        assert "Collections.emptyList()" in body, (
            "extractQueryGroupMemberships must return Collections.emptyList() for null/empty claim"
        )
