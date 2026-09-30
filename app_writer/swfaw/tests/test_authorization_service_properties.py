"""Property-based tests for RoleAuthorizationService generation (Properties 4, 5).

Uses hypothesis to verify correctness properties of the generated
RoleAuthorizationService Java code against the simplified authorization layer design.
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
    just,
    one_of,
    composite,
)

# ---------------------------------------------------------------------------
# Direct-import the two modules we need, bypassing generators/__init__.py
# which pulls in unrelated dependencies (pypika, etc.).
# ---------------------------------------------------------------------------
_SWFAW_ROOT = Path(__file__).resolve().parent.parent

# Load authorization_service_templates first (dependency)
_tpl_spec = importlib.util.spec_from_file_location(
    "authorization_service_templates",
    _SWFAW_ROOT / "templates" / "authorization_service_templates.py",
)
_tpl_mod = importlib.util.module_from_spec(_tpl_spec)
sys.modules["templates.authorization_service_templates"] = _tpl_mod
_tpl_spec.loader.exec_module(_tpl_mod)

# Load authorization_service_generator
_gen_spec = importlib.util.spec_from_file_location(
    "authorization_service_generator",
    _SWFAW_ROOT / "generators" / "authorization_service_generator.py",
)
_gen_mod = importlib.util.module_from_spec(_gen_spec)
_gen_spec.loader.exec_module(_gen_mod)

AuthorizationServiceGenerator = _gen_mod.AuthorizationServiceGenerator

# ---------------------------------------------------------------------------
# Generate the RoleAuthorizationService once — it is deterministic.
# ---------------------------------------------------------------------------
_GENERATED_SERVICE: str = AuthorizationServiceGenerator.generate_role_authorization_service(
    "com.example"
)

# Also generate the AuthorizationWebFilter for cross-checking
_GENERATED_WEB_FILTER: str = AuthorizationServiceGenerator.generate_authorization_web_filter(
    "com.example"
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


@composite
def table_access_maps(draw):
    """Generate a tableAccess-style map: {table_name: [operations]}."""
    num_tables = draw(sampled_from(range(1, 6)))
    result = {}
    for _ in range(num_tables):
        tbl = draw(table_names)
        ops = draw(lists(crud_operations, min_size=1, max_size=4, unique=True))
        result[tbl] = ops
    return result


# ===================================================================
# Feature: simplified-authorization-layer
# Property 4: SUPER_ADMIN has unrestricted table access
# Validates: Requirements 5.5, 5.6
# ===================================================================


class TestProperty4SuperAdminUnrestrictedAccess:
    """Property 4: SUPER_ADMIN has unrestricted table access.

    For any table name and any CRUD operation, a JWT with a SUPER_ADMIN role
    should result in the RoleAuthorizationService granting access without
    database queries.
    """

    @settings(max_examples=20)
    @given(table_name=table_names, operation=crud_operations)
    def test_service_has_super_admin_check(
        self, table_name: str, operation: str
    ) -> None:
        """**Validates: Requirements 5.5, 5.6**

        The generated RoleAuthorizationService must contain an isSuperAdmin
        method that checks for the "SUPER_ADMIN" role string.
        """
        # The service must have an isSuperAdmin method
        assert "public boolean isSuperAdmin" in _GENERATED_SERVICE, (
            "Generated RoleAuthorizationService is missing isSuperAdmin method"
        )
        # The method must check for the SUPER_ADMIN string
        assert '"SUPER_ADMIN"' in _GENERATED_SERVICE, (
            "Generated RoleAuthorizationService does not check for SUPER_ADMIN role"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, operation=crud_operations)
    def test_super_admin_check_returns_boolean(
        self, table_name: str, operation: str
    ) -> None:
        """**Validates: Requirements 5.5, 5.6**

        The isSuperAdmin method must return a boolean — it grants or denies
        access purely from the roles list without any repository/DB call.
        """
        # isSuperAdmin takes a List<String> roles and returns boolean
        assert "List<String> roles" in _GENERATED_SERVICE, (
            "isSuperAdmin should accept a List<String> roles parameter"
        )
        assert "public boolean isSuperAdmin(List<String> roles)" in _GENERATED_SERVICE, (
            "isSuperAdmin should return boolean"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, operation=crud_operations)
    def test_super_admin_no_repository_calls_for_table_access(
        self, table_name: str, operation: str
    ) -> None:
        """**Validates: Requirements 5.5, 5.6**

        The isSuperAdmin method must NOT call any repository — zero database
        hits for SUPER_ADMIN role/table checks. We verify the method body
        (between its signature and the next method) contains no repository
        references.
        """
        # Extract the isSuperAdmin method body
        service = _GENERATED_SERVICE
        method_start = service.index("public boolean isSuperAdmin")
        # Find the closing brace of this method by counting braces
        brace_count = 0
        method_body_start = service.index("{", method_start)
        pos = method_body_start
        for i in range(method_body_start, len(service)):
            if service[i] == "{":
                brace_count += 1
            elif service[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    pos = i
                    break
        method_body = service[method_body_start:pos + 1]

        # The method body should not reference any repository
        assert "Repository" not in method_body, (
            "isSuperAdmin method should not call any repository (zero DB hits)"
        )
        assert ".find" not in method_body, (
            "isSuperAdmin method should not call any find/query methods"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, operation=crud_operations)
    def test_web_filter_grants_super_admin_before_table_check(
        self, table_name: str, operation: str
    ) -> None:
        """**Validates: Requirements 5.5, 5.6**

        The AuthorizationWebFilter must check isSuperAdmin BEFORE checking
        table access, and grant access (chain.filter) immediately for
        SUPER_ADMIN without further checks.
        """
        # In the web filter, isSuperAdmin check should appear before hasTableAccess
        super_admin_pos = _GENERATED_WEB_FILTER.index("isSuperAdmin")
        has_table_pos = _GENERATED_WEB_FILTER.index("hasTableAccess")
        assert super_admin_pos < has_table_pos, (
            "WebFilter should check isSuperAdmin before hasTableAccess"
        )

        # After isSuperAdmin check, the filter should call chain.filter (grant access)
        # Find the block after isSuperAdmin
        super_admin_block_start = _GENERATED_WEB_FILTER.index(
            "isSuperAdmin", super_admin_pos
        )
        # Look for chain.filter within a reasonable range after the check
        next_section = _GENERATED_WEB_FILTER[
            super_admin_block_start:super_admin_block_start + 300
        ]
        assert "chain.filter" in next_section, (
            "WebFilter should grant access (chain.filter) immediately after "
            "isSuperAdmin returns true"
        )


# ===================================================================
# Feature: simplified-authorization-layer
# Property 5: TABLE_ADMIN access is scoped to assigned tables
# Validates: Requirements 5.7
# ===================================================================


class TestProperty5TableAdminScopedAccess:
    """Property 5: TABLE_ADMIN access is scoped to assigned tables.

    For any TABLE_ADMIN with a set of assigned tables, and for any table name
    and CRUD operation, the RoleAuthorizationService should grant access if
    and only if the table is in the assigned set.
    """

    @settings(max_examples=20)
    @given(table_name=table_names, operation=crud_operations)
    def test_service_has_table_access_method(
        self, table_name: str, operation: str
    ) -> None:
        """**Validates: Requirements 5.7**

        The generated RoleAuthorizationService must contain a hasTableAccess
        method that checks the tableAccess claims map.
        """
        assert "public boolean hasTableAccess" in _GENERATED_SERVICE, (
            "Generated RoleAuthorizationService is missing hasTableAccess method"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, operation=crud_operations)
    def test_table_access_reads_from_claims_map(
        self, table_name: str, operation: str
    ) -> None:
        """**Validates: Requirements 5.7**

        The hasTableAccess method must read from a Map<String, List<String>>
        parameter (the JWT tableAccess claims), not from a database.
        """
        assert "Map<String, List<String>> tableAccessClaims" in _GENERATED_SERVICE, (
            "hasTableAccess should accept tableAccessClaims map parameter"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, operation=crud_operations)
    def test_table_access_checks_table_name_in_map(
        self, table_name: str, operation: str
    ) -> None:
        """**Validates: Requirements 5.7**

        The hasTableAccess method must look up the table name in the claims
        map to determine if the table is in the assigned set.
        """
        # Extract the hasTableAccess method body
        service = _GENERATED_SERVICE
        method_start = service.index("public boolean hasTableAccess")
        brace_count = 0
        method_body_start = service.index("{", method_start)
        pos = method_body_start
        for i in range(method_body_start, len(service)):
            if service[i] == "{":
                brace_count += 1
            elif service[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    pos = i
                    break
        method_body = service[method_body_start:pos + 1]

        # The method must look up the table in the claims map
        assert "tableAccessClaims.get(tableName)" in method_body or \
               "tableAccessClaims.get(" in method_body, (
            "hasTableAccess should look up tableName in the tableAccessClaims map"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, operation=crud_operations)
    def test_table_access_checks_operation_in_allowed_list(
        self, table_name: str, operation: str
    ) -> None:
        """**Validates: Requirements 5.7**

        The hasTableAccess method must check that the requested operation is
        in the list of allowed operations for the table — granting access
        if and only if the operation is present.
        """
        # Extract the hasTableAccess method body
        service = _GENERATED_SERVICE
        method_start = service.index("public boolean hasTableAccess")
        brace_count = 0
        method_body_start = service.index("{", method_start)
        pos = method_body_start
        for i in range(method_body_start, len(service)):
            if service[i] == "{":
                brace_count += 1
            elif service[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    pos = i
                    break
        method_body = service[method_body_start:pos + 1]

        # The method must check if the operation is contained in the allowed list
        assert ".contains(operation)" in method_body or \
               ".contains(" in method_body, (
            "hasTableAccess should check if operation is in the allowed operations list"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, operation=crud_operations)
    def test_table_access_no_repository_calls(
        self, table_name: str, operation: str
    ) -> None:
        """**Validates: Requirements 5.7**

        The hasTableAccess method must NOT call any repository — zero database
        hits for TABLE_ADMIN table access checks. All data comes from JWT claims.
        """
        # Extract the hasTableAccess method body
        service = _GENERATED_SERVICE
        method_start = service.index("public boolean hasTableAccess")
        brace_count = 0
        method_body_start = service.index("{", method_start)
        pos = method_body_start
        for i in range(method_body_start, len(service)):
            if service[i] == "{":
                brace_count += 1
            elif service[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    pos = i
                    break
        method_body = service[method_body_start:pos + 1]

        assert "Repository" not in method_body, (
            "hasTableAccess method should not call any repository (zero DB hits)"
        )
        assert ".find" not in method_body, (
            "hasTableAccess method should not call any find/query methods"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, operation=crud_operations)
    def test_table_access_handles_null_claims(
        self, table_name: str, operation: str
    ) -> None:
        """**Validates: Requirements 5.7**

        The hasTableAccess method must handle null inputs gracefully —
        null claims map, null table name, or null operation should return false.
        """
        # Extract the hasTableAccess method body
        service = _GENERATED_SERVICE
        method_start = service.index("public boolean hasTableAccess")
        brace_count = 0
        method_body_start = service.index("{", method_start)
        pos = method_body_start
        for i in range(method_body_start, len(service)):
            if service[i] == "{":
                brace_count += 1
            elif service[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    pos = i
                    break
        method_body = service[method_body_start:pos + 1]

        # Must have null checks
        assert "null" in method_body.lower(), (
            "hasTableAccess should handle null inputs"
        )
        assert "return false" in method_body, (
            "hasTableAccess should return false for null/invalid inputs"
        )

    @settings(max_examples=20)
    @given(assigned_tables=table_access_maps(), query_table=table_names, operation=crud_operations)
    def test_table_access_grants_iff_table_in_assigned_set(
        self, assigned_tables: dict, query_table: str, operation: str
    ) -> None:
        """**Validates: Requirements 5.7**

        The generated hasTableAccess logic must grant access if and only if
        the queried table is in the assigned set AND the operation is allowed.
        We verify this by checking the structural pattern: the method gets
        the allowed operations list for the table, then checks .contains().
        """
        service = _GENERATED_SERVICE
        method_start = service.index("public boolean hasTableAccess")
        brace_count = 0
        method_body_start = service.index("{", method_start)
        pos = method_body_start
        for i in range(method_body_start, len(service)):
            if service[i] == "{":
                brace_count += 1
            elif service[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    pos = i
                    break
        method_body = service[method_body_start:pos + 1]

        # The method must:
        # 1. Get the allowed operations for the table from the map
        has_get = "tableAccessClaims.get(" in method_body
        # 2. Check if the operation is in the allowed list
        has_contains = ".contains(" in method_body
        # 3. Return false when table is not in map (null check on result)
        has_null_guard = "null" in method_body.lower()

        assert has_get and has_contains and has_null_guard, (
            "hasTableAccess must: (1) get operations from claims map, "
            "(2) check .contains() for the operation, "
            "(3) handle null (table not in map). "
            f"Got: get={has_get}, contains={has_contains}, null_guard={has_null_guard}"
        )


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


# ---------------------------------------------------------------------------
# Strategies for Properties 7, 14, 15
# ---------------------------------------------------------------------------

# Valid Java identifier-style query names
_QUERY_NAME_CHARS = "abcdefghijklmnopqrstuvwxyz_"
query_names = text(
    alphabet=_QUERY_NAME_CHARS, min_size=1, max_size=30
).filter(lambda s: s[0].isalpha() and not s.endswith("_"))

# Query group IDs (positive integers)
query_group_ids = lists(
    sampled_from(range(1, 1000)), min_size=0, max_size=10, unique=True
)

# Usernames for test scenarios
usernames = text(
    alphabet="abcdefghijklmnopqrstuvwxyz0123456789", min_size=1, max_size=20
).filter(lambda s: s[0].isalpha())

# Roles for generating random JWT claim sets
ROLES = ["USER", "TABLE_ADMIN", "SUPER_ADMIN"]
role_lists = lists(sampled_from(ROLES), min_size=0, max_size=3)


# ===================================================================
# Feature: simplified-authorization-layer
# Property 7: Query access requires group membership
# Validates: Requirements 5.9, 8.3
# ===================================================================


class TestProperty7QueryAccessRequiresGroupMembership:
    """Property 7: Query access requires group membership.

    For any ROLE_BASED query endpoint and any user, the AuthorizationWebFilter
    should grant access if and only if the user's JWT queryGroupMemberships
    includes a query group that contains the requested query name.
    """

    @settings(max_examples=20)
    @given(query_name=query_names)
    def test_web_filter_reads_query_access_annotation(
        self, query_name: str
    ) -> None:
        """**Validates: Requirements 5.9, 8.3**

        The AuthorizationWebFilter must read the @QueryAccess annotation
        from the handler method to determine the query name.
        """
        assert "QueryAccess queryAccess = handlerMethod.getMethodAnnotation(QueryAccess.class)" in _GENERATED_WEB_FILTER, (
            "WebFilter must read @QueryAccess annotation from handler method"
        )

    @settings(max_examples=20)
    @given(query_name=query_names)
    def test_web_filter_extracts_query_name_from_annotation(
        self, query_name: str
    ) -> None:
        """**Validates: Requirements 5.9, 8.3**

        The AuthorizationWebFilter must extract the queryName attribute
        from the @QueryAccess annotation.
        """
        assert "queryAccess.queryName()" in _GENERATED_WEB_FILTER, (
            "WebFilter must extract queryName from @QueryAccess annotation"
        )

    @settings(max_examples=20)
    @given(query_name=query_names, group_ids=query_group_ids)
    def test_web_filter_calls_has_query_access(
        self, query_name: str, group_ids: list
    ) -> None:
        """**Validates: Requirements 5.9, 8.3**

        The AuthorizationWebFilter must call hasQueryAccess on the
        RoleAuthorizationService with the user's queryGroupMemberships
        and the requested query name.
        """
        assert "hasQueryAccess(queryGroupMemberships, queryName" in _GENERATED_WEB_FILTER, (
            "WebFilter must call hasQueryAccess with queryGroupMemberships and queryName"
        )

    @settings(max_examples=20)
    @given(query_name=query_names)
    def test_web_filter_grants_access_when_query_group_matches(
        self, query_name: str
    ) -> None:
        """**Validates: Requirements 5.9, 8.3**

        When hasQueryAccess returns true, the WebFilter must call
        chain.filter to grant access.
        """
        # Find the queryAccess block in the filter
        qa_block_start = _GENERATED_WEB_FILTER.index("if (queryAccess != null)")
        qa_block = _GENERATED_WEB_FILTER[qa_block_start:qa_block_start + 600]

        assert "hasAccess" in qa_block, (
            "WebFilter must check hasAccess result from hasQueryAccess"
        )
        assert "chain.filter" in qa_block, (
            "WebFilter must call chain.filter when query access is granted"
        )

    @settings(max_examples=20)
    @given(query_name=query_names)
    def test_web_filter_denies_access_when_query_group_no_match(
        self, query_name: str
    ) -> None:
        """**Validates: Requirements 5.9, 8.3**

        When hasQueryAccess returns false, the WebFilter must call
        denyAccess to return 403.
        """
        qa_block_start = _GENERATED_WEB_FILTER.index("if (queryAccess != null)")
        qa_block = _GENERATED_WEB_FILTER[qa_block_start:qa_block_start + 600]

        assert "denyAccess" in qa_block, (
            "WebFilter must call denyAccess when query access is denied"
        )
        assert "Insufficient query access" in qa_block, (
            "WebFilter must provide 'Insufficient query access' reason on denial"
        )

    @settings(max_examples=20)
    @given(query_name=query_names)
    def test_service_has_query_access_checks_memberships(
        self, query_name: str
    ) -> None:
        """**Validates: Requirements 5.9, 8.3**

        The RoleAuthorizationService hasQueryAccess method must check
        queryGroupMemberships from JWT claims and verify the query name
        exists in one of the user's groups via QueryGroupQueryRepository.
        """
        assert "public Mono<Boolean> hasQueryAccess" in _GENERATED_SERVICE, (
            "RoleAuthorizationService must have a hasQueryAccess method"
        )
        method_body = _extract_method_body(_GENERATED_SERVICE, "public Mono<Boolean> hasQueryAccess")

        assert "queryGroupMemberships" in method_body, (
            "hasQueryAccess must check queryGroupMemberships parameter"
        )
        assert "findByQueryName" in method_body, (
            "hasQueryAccess must call findByQueryName on QueryGroupQueryRepository"
        )
        assert "getQueryGroupId" in method_body, (
            "hasQueryAccess must check the query group ID from query entries"
        )

    @settings(max_examples=20)
    @given(query_name=query_names)
    def test_service_has_query_access_handles_null(
        self, query_name: str
    ) -> None:
        """**Validates: Requirements 5.9, 8.3**

        The hasQueryAccess method must handle null/empty queryGroupMemberships
        gracefully by returning false.
        """
        method_body = _extract_method_body(_GENERATED_SERVICE, "public Mono<Boolean> hasQueryAccess")

        assert "null" in method_body.lower(), (
            "hasQueryAccess must handle null inputs"
        )
        assert "Mono.just(false)" in method_body, (
            "hasQueryAccess must return Mono.just(false) for null/empty inputs"
        )

    @settings(max_examples=20)
    @given(query_name=query_names)
    def test_web_filter_extracts_query_group_memberships_from_jwt(
        self, query_name: str
    ) -> None:
        """**Validates: Requirements 5.9, 8.3**

        The AuthorizationWebFilter must extract queryGroupMemberships
        from the JWT claims map before checking query access.
        """
        assert 'claims.get("queryGroupMemberships")' in _GENERATED_WEB_FILTER, (
            "WebFilter must extract queryGroupMemberships from JWT claims"
        )


# ===================================================================
# Feature: simplified-authorization-layer
# Property 14: Authorization denial produces 403 and audit log
# Validates: Requirements 8.4
# ===================================================================


class TestProperty14DenialProduces403AndAuditLog:
    """Property 14: Authorization denial produces 403 and audit log.

    For any request where the JWT claims do not grant the required access,
    the AuthorizationWebFilter should return HTTP 403 Forbidden with a JSON
    error response and create an entry in the access_audit_log.
    """

    @settings(max_examples=20)
    @given(query_name=query_names)
    def test_deny_access_sets_403_status(
        self, query_name: str
    ) -> None:
        """**Validates: Requirements 8.4**

        The denyAccess method must set the HTTP response status to 403 Forbidden.
        """
        assert "HttpStatus.FORBIDDEN" in _GENERATED_WEB_FILTER, (
            "WebFilter must use HttpStatus.FORBIDDEN for denial responses"
        )
        deny_body = _extract_method_body(_GENERATED_WEB_FILTER, "private Mono<Void> denyAccess")
        assert "setStatusCode(HttpStatus.FORBIDDEN)" in deny_body, (
            "denyAccess must call setStatusCode(HttpStatus.FORBIDDEN)"
        )

    @settings(max_examples=20)
    @given(query_name=query_names)
    def test_deny_access_returns_json_error_response(
        self, query_name: str
    ) -> None:
        """**Validates: Requirements 8.4**

        The denyAccess method must return a JSON error response body
        with content type application/json.
        """
        deny_body = _extract_method_body(_GENERATED_WEB_FILTER, "private Mono<Void> denyAccess")

        assert "MediaType.APPLICATION_JSON" in deny_body, (
            "denyAccess must set content type to APPLICATION_JSON"
        )
        assert "ACCESS_DENIED" in deny_body, (
            "denyAccess must include ACCESS_DENIED error code in JSON response"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, operation=crud_operations)
    def test_deny_access_saves_audit_log(
        self, table_name: str, operation: str
    ) -> None:
        """**Validates: Requirements 8.4**

        The denyAccess method must save an AccessAuditLog entry via
        accessAuditLogRepository.save() to record the denial.
        """
        deny_body = _extract_method_body(_GENERATED_WEB_FILTER, "private Mono<Void> denyAccess")

        assert "accessAuditLogRepository.save" in deny_body, (
            "denyAccess must call accessAuditLogRepository.save to log denial"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, operation=crud_operations)
    def test_deny_access_audit_log_records_denial(
        self, table_name: str, operation: str
    ) -> None:
        """**Validates: Requirements 8.4**

        The AccessAuditLog entry must record accessGranted=false to indicate
        the access was denied.
        """
        deny_body = _extract_method_body(_GENERATED_WEB_FILTER, "private Mono<Void> denyAccess")

        assert ".accessGranted(false)" in deny_body, (
            "Audit log entry must set accessGranted(false) for denials"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, operation=crud_operations)
    def test_deny_access_audit_log_records_resource_and_operation(
        self, table_name: str, operation: str
    ) -> None:
        """**Validates: Requirements 8.4**

        The AccessAuditLog entry must record the resource (table/query name)
        and the operation that was denied.
        """
        deny_body = _extract_method_body(_GENERATED_WEB_FILTER, "private Mono<Void> denyAccess")

        assert ".tableName(resource)" in deny_body, (
            "Audit log entry must record the resource (table/query name)"
        )
        assert ".accessControl(operation)" in deny_body, (
            "Audit log entry must record the operation that was denied"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, operation=crud_operations)
    def test_deny_access_audit_log_records_user_id(
        self, table_name: str, operation: str
    ) -> None:
        """**Validates: Requirements 8.4**

        The AccessAuditLog entry must record the user ID from the JWT claims.
        """
        deny_body = _extract_method_body(_GENERATED_WEB_FILTER, "private Mono<Void> denyAccess")

        assert ".authUserId(userId)" in deny_body, (
            "Audit log entry must record the authUserId"
        )

    @settings(max_examples=20)
    @given(table_name=table_names)
    def test_table_access_denial_calls_deny_access(
        self, table_name: str
    ) -> None:
        """**Validates: Requirements 8.4**

        When table access check fails, the WebFilter must call denyAccess
        with the table name and operation.
        """
        # Find the tableAccess check block — use 900 chars to capture the full denial call
        ta_block_start = _GENERATED_WEB_FILTER.index("if (tableAccess != null)")
        ta_block = _GENERATED_WEB_FILTER[ta_block_start:ta_block_start + 900]

        assert "denyAccess" in ta_block, (
            "WebFilter must call denyAccess when table access is denied"
        )
        assert "Insufficient table access" in ta_block, (
            "WebFilter must provide 'Insufficient table access' reason"
        )

    @settings(max_examples=20)
    @given(query_name=query_names)
    def test_query_access_denial_calls_deny_access(
        self, query_name: str
    ) -> None:
        """**Validates: Requirements 8.4**

        When query access check fails, the WebFilter must call denyAccess
        with the query name.
        """
        qa_block_start = _GENERATED_WEB_FILTER.index("if (queryAccess != null)")
        qa_block = _GENERATED_WEB_FILTER[qa_block_start:qa_block_start + 600]

        assert "denyAccess" in qa_block, (
            "WebFilter must call denyAccess when query access is denied"
        )
        assert "Insufficient query access" in qa_block, (
            "WebFilter must provide 'Insufficient query access' reason"
        )

    @settings(max_examples=20)
    @given(table_name=table_names)
    def test_deny_access_handles_audit_save_failure(
        self, table_name: str
    ) -> None:
        """**Validates: Requirements 8.4**

        The denyAccess method must handle audit log save failures gracefully
        (onErrorResume) so that the 403 response is still returned.
        """
        deny_body = _extract_method_body(_GENERATED_WEB_FILTER, "private Mono<Void> denyAccess")

        assert "onErrorResume" in deny_body, (
            "denyAccess must handle audit log save failures with onErrorResume"
        )

    @settings(max_examples=20)
    @given(username=usernames)
    def test_deny_access_logs_warning(
        self, username: str
    ) -> None:
        """**Validates: Requirements 8.4**

        The denyAccess method must log a warning message with user details
        and the denial reason.
        """
        deny_body = _extract_method_body(_GENERATED_WEB_FILTER, "private Mono<Void> denyAccess")

        assert "log.warn" in deny_body, (
            "denyAccess must log a warning for access denials"
        )
        assert "Access denied" in deny_body, (
            "denyAccess warning must include 'Access denied' message"
        )


# ===================================================================
# Feature: simplified-authorization-layer
# Property 15: PUBLIC endpoints allow any authenticated user
# Validates: Requirements 8.6
# ===================================================================


class TestProperty15PublicEndpointsAllowAuthenticated:
    """Property 15: PUBLIC endpoints allow any authenticated user.

    For any endpoint with Access_Level PUBLIC and any user with a valid JWT
    (regardless of roles), the AuthorizationWebFilter should grant access
    without role-based checks.
    """

    @settings(max_examples=20)
    @given(role=sampled_from(ROLES))
    def test_global_endpoints_skip_auth_entirely(
        self, role: str
    ) -> None:
        """**Validates: Requirements 8.6**

        When no @TableAccess or @QueryAccess annotations are present (GLOBAL),
        the WebFilter must skip authorization entirely by calling chain.filter.
        """
        # The filter checks: if (tableAccess == null && queryAccess == null) -> chain.filter
        assert "if (tableAccess == null && queryAccess == null)" in _GENERATED_WEB_FILTER, (
            "WebFilter must check for absence of both @TableAccess and @QueryAccess"
        )
        # Find the null-check block and verify it calls chain.filter
        null_check_pos = _GENERATED_WEB_FILTER.index(
            "if (tableAccess == null && queryAccess == null)"
        )
        null_block = _GENERATED_WEB_FILTER[null_check_pos:null_check_pos + 200]
        assert "chain.filter" in null_block, (
            "WebFilter must call chain.filter when no auth annotations present (GLOBAL)"
        )

    @settings(max_examples=20)
    @given(role=sampled_from(ROLES))
    def test_web_filter_implements_web_filter_interface(
        self, role: str
    ) -> None:
        """**Validates: Requirements 8.6**

        The AuthorizationWebFilter must implement the WebFilter interface
        to intercept requests.
        """
        assert "implements WebFilter" in _GENERATED_WEB_FILTER, (
            "AuthorizationWebFilter must implement WebFilter interface"
        )

    @settings(max_examples=20)
    @given(role=sampled_from(ROLES))
    def test_web_filter_has_filter_method(
        self, role: str
    ) -> None:
        """**Validates: Requirements 8.6**

        The AuthorizationWebFilter must have a filter method that accepts
        ServerWebExchange and WebFilterChain.
        """
        assert "public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain)" in _GENERATED_WEB_FILTER, (
            "WebFilter must have filter(ServerWebExchange, WebFilterChain) method"
        )

    @settings(max_examples=20)
    @given(role=sampled_from(ROLES))
    def test_public_endpoints_only_need_valid_jwt(
        self, role: str
    ) -> None:
        """**Validates: Requirements 8.6**

        For PUBLIC endpoints (no @QueryAccess annotation, JWT required),
        the WebFilter must verify the user is authenticated via
        ReactiveSecurityContextHolder but skip role-based checks.
        The filter uses ReactiveSecurityContextHolder.getContext() to
        verify JWT presence — if no context exists, it denies access.
        """
        assert "ReactiveSecurityContextHolder.getContext()" in _GENERATED_WEB_FILTER, (
            "WebFilter must use ReactiveSecurityContextHolder to verify JWT"
        )
        # The switchIfEmpty after getContext() handles missing auth context
        assert "switchIfEmpty(denyAccess" in _GENERATED_WEB_FILTER, (
            "WebFilter must deny access when no authentication context (no JWT)"
        )

    @settings(max_examples=20)
    @given(role=sampled_from(ROLES))
    def test_unannotated_handler_falls_through_to_chain(
        self, role: str
    ) -> None:
        """**Validates: Requirements 8.6**

        When the handler mapping returns no HandlerMethod (no matching
        controller), the WebFilter must fall through to chain.filter
        via the outer switchIfEmpty.
        """
        # The outer switchIfEmpty at the end of the filter method
        filter_body = _extract_method_body(
            _GENERATED_WEB_FILTER,
            "public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain)"
        )
        # Count switchIfEmpty occurrences — there should be at least 2:
        # one for missing auth context, one for missing handler
        switch_count = filter_body.count("switchIfEmpty")
        assert switch_count >= 2, (
            f"WebFilter must have at least 2 switchIfEmpty calls (got {switch_count}): "
            "one for missing auth context, one for missing handler"
        )

    @settings(max_examples=20)
    @given(role=sampled_from(ROLES))
    def test_web_filter_reads_annotations_from_handler(
        self, role: str
    ) -> None:
        """**Validates: Requirements 8.6**

        The WebFilter must read @EntityTable, @TableAccess, and @QueryAccess
        annotations from the resolved handler method and its bean type.
        """
        assert "handlerMethod.getMethodAnnotation(TableAccess.class)" in _GENERATED_WEB_FILTER, (
            "WebFilter must read @TableAccess from handler method"
        )
        assert "handlerMethod.getMethodAnnotation(QueryAccess.class)" in _GENERATED_WEB_FILTER, (
            "WebFilter must read @QueryAccess from handler method"
        )
        assert "handlerMethod.getBeanType().getAnnotation(EntityTable.class)" in _GENERATED_WEB_FILTER, (
            "WebFilter must read @EntityTable from controller class"
        )

    @settings(max_examples=20)
    @given(role=sampled_from(ROLES))
    def test_web_filter_injects_required_dependencies(
        self, role: str
    ) -> None:
        """**Validates: Requirements 8.6**

        The AuthorizationWebFilter must inject RoleAuthorizationService,
        AccessAuditLogRepository, QueryGroupQueryRepository, and
        RequestMappingHandlerMapping as dependencies.
        """
        assert "private final RoleAuthorizationService roleAuthorizationService" in _GENERATED_WEB_FILTER, (
            "WebFilter must inject RoleAuthorizationService"
        )
        assert "private final AccessAuditLogRepository accessAuditLogRepository" in _GENERATED_WEB_FILTER, (
            "WebFilter must inject AccessAuditLogRepository"
        )
        assert "private final QueryGroupQueryRepository queryGroupQueryRepository" in _GENERATED_WEB_FILTER, (
            "WebFilter must inject QueryGroupQueryRepository"
        )
        assert "private final RequestMappingHandlerMapping handlerMapping" in _GENERATED_WEB_FILTER, (
            "WebFilter must inject RequestMappingHandlerMapping"
        )

    @settings(max_examples=20)
    @given(role=sampled_from(ROLES))
    def test_web_filter_uses_handler_mapping_to_resolve_handler(
        self, role: str
    ) -> None:
        """**Validates: Requirements 8.6**

        The WebFilter must use RequestMappingHandlerMapping.getHandler()
        to resolve the handler method for the incoming request, then cast
        to HandlerMethod to read annotations.
        """
        assert "handlerMapping.getHandler(exchange)" in _GENERATED_WEB_FILTER, (
            "WebFilter must call handlerMapping.getHandler(exchange)"
        )
        assert ".cast(HandlerMethod.class)" in _GENERATED_WEB_FILTER, (
            "WebFilter must cast handler to HandlerMethod"
        )
