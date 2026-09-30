"""Property-based tests for controller annotations (Properties 8, 9).

Uses hypothesis to verify correctness properties of the generated
controller Java code against the simplified authorization layer design.

Feature: simplified-authorization-layer
Property 8: Controller annotations match table and operation
Property 9: Access level determines annotation and auth behavior per query
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
    composite,
    booleans,
    integers,
    fixed_dictionaries,
    just,
    one_of,
)

# ---------------------------------------------------------------------------
# Direct-import controller_templates, bypassing generators/__init__.py
# which pulls in unrelated dependencies (pypika, etc.).
# ---------------------------------------------------------------------------
_SWFAW_ROOT = Path(__file__).resolve().parent.parent

_tpl_spec = importlib.util.spec_from_file_location(
    "controller_templates",
    _SWFAW_ROOT / "templates" / "controller_templates.py",
)
_tpl_mod = importlib.util.module_from_spec(_tpl_spec)
sys.modules["templates.controller_templates"] = _tpl_mod
_tpl_spec.loader.exec_module(_tpl_mod)

ControllerTemplates = _tpl_mod.ControllerTemplates

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

query_names = text(
    alphabet=_TABLE_NAME_CHARS, min_size=2, max_size=30
).filter(lambda s: s[0].isalpha() and not s.endswith("_") and "__" not in s)

ACCESS_LEVELS = ["GLOBAL", "PUBLIC", "ROLE_BASED"]
access_levels = sampled_from(ACCESS_LEVELS)

HTTP_METHODS = ["get", "post", "put", "delete"]
http_methods = sampled_from(HTTP_METHODS)



@composite
def custom_endpoints(draw, access_level=None):
    """Generate a custom endpoint dict with a given or random access level."""
    al = access_level if access_level is not None else draw(access_levels)
    qn = draw(query_names)
    method = draw(http_methods)
    method_name = draw(text(alphabet=_IDENT_CHARS, min_size=2, max_size=15).filter(lambda s: s[0].isalpha()))
    return {
        "description": f"Custom query {qn}",
        "queryName": qn,
        "accessLevel": al,
        "httpMethod": method,
        "path": f"/custom/{qn}",
        "methodName": method_name,
    }


def _render_controller(table_name: str, entity_name: str, custom_eps=None):
    """Render the controller template with the given parameters."""
    if custom_eps is None:
        custom_eps = []
    context = {
        "packageName": "com.example.controller",
        "dtoPackage": "com.example.dto",
        "servicePackage": "com.example.service",
        "exceptionPackage": "com.example.exception",
        "securityPackage": "com.example.security",
        "entityName": entity_name,
        "className": f"{entity_name}Controller",
        "serviceName": f"{entity_name}Service",
        "basePath": f"/api/{entity_name.lower()}s",
        "isRootEntity": True,
        "endpoints": {
            "create": {"enabled": True, "path": ""},
            "getById": {"enabled": True, "path": "/{id}"},
            "getAll": {"enabled": True, "path": "", "defaultPageSize": 20},
            "update": {"enabled": True, "path": "/{id}"},
            "delete": {"enabled": True, "path": "/{id}"},
        },
        "customEndpoints": custom_eps,
        "corsConfig": {"enabled": False},
        "hasActivityTracking": False,
        "tableName": table_name,
    }
    template = Template(ControllerTemplates.CONTROLLER_TEMPLATE)
    return template.render(context)


# ===================================================================
# Feature: simplified-authorization-layer
# Property 8: Controller annotations match table and operation
# Validates: Requirements 9.1, 9.2, 9.3
# ===================================================================


class TestProperty8ControllerAnnotationsMatchTableAndOperation:
    """Property 8: Controller annotations match table and operation.

    For any generated controller for a business table, the class should carry
    @EntityTable("table_name") where table_name matches the entity's database
    table, each CRUD method should carry @TableAccess(operation=...) with the
    correct operation string, and each ROLE_BASED custom query method should
    carry @QueryAccess(queryName="...") with the correct query name.
    """

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_entity_table_annotation_matches_table_name(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 9.1**

        The generated controller class must carry @EntityTable("table_name")
        where table_name matches the entity's database table name.
        """
        code = _render_controller(table_name, entity_name)
        expected = f'@EntityTable("{table_name}")'
        assert expected in code, (
            f"Controller must have {expected}, got:\n{code[:500]}"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_create_endpoint_has_create_table_access(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 9.2**

        The create endpoint must carry @TableAccess(operation = "CREATE").
        """
        code = _render_controller(table_name, entity_name)
        assert '@TableAccess(operation = "CREATE")' in code, (
            "Create endpoint must have @TableAccess(operation = \"CREATE\")"
        )
        # Verify it appears before @PostMapping
        create_pos = code.index('@TableAccess(operation = "CREATE")')
        post_pos = code.index("@PostMapping", create_pos)
        assert create_pos < post_pos, (
            "@TableAccess(CREATE) must appear before @PostMapping"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_read_endpoints_have_read_table_access(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 9.2**

        The findById and findAll endpoints must carry @TableAccess(operation = "READ").
        """
        code = _render_controller(table_name, entity_name)
        read_occurrences = code.count('@TableAccess(operation = "READ")')
        assert read_occurrences >= 2, (
            f"Expected at least 2 @TableAccess(READ) annotations (findById + findAll), "
            f"found {read_occurrences}"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_update_endpoint_has_update_table_access(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 9.2**

        The update endpoint must carry @TableAccess(operation = "UPDATE").
        """
        code = _render_controller(table_name, entity_name)
        assert '@TableAccess(operation = "UPDATE")' in code, (
            "Update endpoint must have @TableAccess(operation = \"UPDATE\")"
        )
        update_pos = code.index('@TableAccess(operation = "UPDATE")')
        put_pos = code.index("@PutMapping", update_pos)
        assert update_pos < put_pos, (
            "@TableAccess(UPDATE) must appear before @PutMapping"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_delete_endpoints_have_delete_table_access(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 9.2**

        The delete and deleteWithJustification endpoints must carry
        @TableAccess(operation = "DELETE").
        """
        code = _render_controller(table_name, entity_name)
        delete_occurrences = code.count('@TableAccess(operation = "DELETE")')
        assert delete_occurrences >= 2, (
            f"Expected at least 2 @TableAccess(DELETE) annotations "
            f"(delete + deleteWithJustification), found {delete_occurrences}"
        )

    @settings(max_examples=20)
    @given(
        table_name=table_names,
        entity_name=entity_names,
        ep=custom_endpoints(access_level="ROLE_BASED"),
    )
    def test_role_based_custom_endpoint_has_query_access(
        self, table_name: str, entity_name: str, ep: dict
    ) -> None:
        """**Validates: Requirements 9.3**

        Each ROLE_BASED custom query endpoint must carry
        @QueryAccess(queryName = "query_name") with the correct query name.
        """
        code = _render_controller(table_name, entity_name, custom_eps=[ep])
        expected = f'@QueryAccess(queryName = "{ep["queryName"]}")'
        assert expected in code, (
            f"ROLE_BASED endpoint must have {expected}"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_imports_include_annotation_classes(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 9.1, 9.2, 9.3**

        The generated controller must import EntityTable, TableAccess,
        and QueryAccess annotation classes.
        """
        code = _render_controller(table_name, entity_name)
        assert "import com.example.security.EntityTable;" in code, (
            "Controller must import EntityTable"
        )
        assert "import com.example.security.TableAccess;" in code, (
            "Controller must import TableAccess"
        )
        assert "import com.example.security.QueryAccess;" in code, (
            "Controller must import QueryAccess"
        )

    @settings(max_examples=20)
    @given(table_name=table_names, entity_name=entity_names)
    def test_all_crud_operations_present(
        self, table_name: str, entity_name: str
    ) -> None:
        """**Validates: Requirements 9.2**

        All four CRUD operations (CREATE, READ, UPDATE, DELETE) must appear
        as @TableAccess annotations in the generated controller.
        """
        code = _render_controller(table_name, entity_name)
        for op in ["CREATE", "READ", "UPDATE", "DELETE"]:
            assert f'@TableAccess(operation = "{op}")' in code, (
                f"Controller must have @TableAccess(operation = \"{op}\")"
            )


# ===================================================================
# Feature: simplified-authorization-layer
# Property 9: Access level determines annotation and auth behavior per query
# Validates: Requirements 14.3, 14.4, 14.5
# ===================================================================


class TestProperty9AccessLevelDeterminesAnnotationBehavior:
    """Property 9: Access level determines annotation and auth behavior per query.

    For any custom query with a given access level (GLOBAL, PUBLIC, or
    ROLE_BASED), the generated controller endpoint should: omit @QueryAccess
    for GLOBAL, require JWT but omit @QueryAccess for PUBLIC, and include
    @QueryAccess for ROLE_BASED.
    """

    @settings(max_examples=20)
    @given(
        table_name=table_names,
        entity_name=entity_names,
        ep=custom_endpoints(access_level="GLOBAL"),
    )
    def test_global_endpoint_omits_query_access(
        self, table_name: str, entity_name: str, ep: dict
    ) -> None:
        """**Validates: Requirements 14.3**

        GLOBAL endpoints must NOT have @QueryAccess annotation — no auth needed.
        """
        code = _render_controller(table_name, entity_name, custom_eps=[ep])
        # Find the custom endpoint section (after the CRUD methods)
        method_name = ep["methodName"]
        method_pos = code.index(f"public Mono<{entity_name}OutputDTO> {method_name}")
        # Look backwards from the method to find the annotation area
        section_before_method = code[max(0, method_pos - 300):method_pos]
        assert f'@QueryAccess(queryName = "{ep["queryName"]}")' not in section_before_method, (
            "GLOBAL endpoint must NOT have @QueryAccess annotation"
        )

    @settings(max_examples=20)
    @given(
        table_name=table_names,
        entity_name=entity_names,
        ep=custom_endpoints(access_level="PUBLIC"),
    )
    def test_public_endpoint_omits_query_access(
        self, table_name: str, entity_name: str, ep: dict
    ) -> None:
        """**Validates: Requirements 14.4**

        PUBLIC endpoints must NOT have @QueryAccess annotation — JWT required
        but no role-based checks.
        """
        code = _render_controller(table_name, entity_name, custom_eps=[ep])
        method_name = ep["methodName"]
        method_pos = code.index(f"public Mono<{entity_name}OutputDTO> {method_name}")
        section_before_method = code[max(0, method_pos - 300):method_pos]
        assert f'@QueryAccess(queryName = "{ep["queryName"]}")' not in section_before_method, (
            "PUBLIC endpoint must NOT have @QueryAccess annotation"
        )

    @settings(max_examples=20)
    @given(
        table_name=table_names,
        entity_name=entity_names,
        ep=custom_endpoints(access_level="ROLE_BASED"),
    )
    def test_role_based_endpoint_includes_query_access(
        self, table_name: str, entity_name: str, ep: dict
    ) -> None:
        """**Validates: Requirements 14.5**

        ROLE_BASED endpoints must have @QueryAccess(queryName = "...") annotation.
        """
        code = _render_controller(table_name, entity_name, custom_eps=[ep])
        expected = f'@QueryAccess(queryName = "{ep["queryName"]}")'
        assert expected in code, (
            f"ROLE_BASED endpoint must have {expected}"
        )

    @settings(max_examples=20)
    @given(
        table_name=table_names,
        entity_name=entity_names,
        ep=custom_endpoints(access_level="ROLE_BASED"),
    )
    def test_role_based_query_access_before_mapping(
        self, table_name: str, entity_name: str, ep: dict
    ) -> None:
        """**Validates: Requirements 14.5**

        The @QueryAccess annotation must appear before the HTTP method mapping
        annotation on ROLE_BASED endpoints.
        """
        code = _render_controller(table_name, entity_name, custom_eps=[ep])
        qa_pos = code.index(f'@QueryAccess(queryName = "{ep["queryName"]}")')
        mapping_str = f"@{ep['httpMethod'].capitalize()}Mapping"
        mapping_pos = code.index(mapping_str, qa_pos)
        assert qa_pos < mapping_pos, (
            "@QueryAccess must appear before the HTTP method mapping annotation"
        )

    @settings(max_examples=20)
    @given(
        table_name=table_names,
        entity_name=entity_names,
        access_level=access_levels,
        qn=query_names,
    )
    def test_access_level_annotation_presence_is_deterministic(
        self, table_name: str, entity_name: str, access_level: str, qn: str
    ) -> None:
        """**Validates: Requirements 14.3, 14.4, 14.5**

        For any access level, the presence or absence of @QueryAccess is
        deterministic: present only for ROLE_BASED, absent for GLOBAL and PUBLIC.
        """
        method_name = "customQuery"
        ep = {
            "description": f"Custom query {qn}",
            "queryName": qn,
            "accessLevel": access_level,
            "httpMethod": "get",
            "path": f"/custom/{qn}",
            "methodName": method_name,
        }
        code = _render_controller(table_name, entity_name, custom_eps=[ep])
        qa_annotation = f'@QueryAccess(queryName = "{qn}")'

        if access_level == "ROLE_BASED":
            assert qa_annotation in code, (
                f"ROLE_BASED endpoint must have {qa_annotation}"
            )
        else:
            assert qa_annotation not in code, (
                f"{access_level} endpoint must NOT have {qa_annotation}"
            )

    @settings(max_examples=20)
    @given(
        table_name=table_names,
        entity_name=entity_names,
        eps=lists(custom_endpoints(), min_size=1, max_size=5),
    )
    def test_mixed_access_levels_each_handled_correctly(
        self, table_name: str, entity_name: str, eps: list
    ) -> None:
        """**Validates: Requirements 14.3, 14.4, 14.5**

        When multiple custom endpoints with different access levels are
        present, each one must be handled according to its own access level.
        """
        # Ensure unique method names to avoid template collisions
        seen_names = set()
        unique_eps = []
        for ep in eps:
            if ep["methodName"] not in seen_names:
                seen_names.add(ep["methodName"])
                unique_eps.append(ep)
        assume(len(unique_eps) >= 1)

        code = _render_controller(table_name, entity_name, custom_eps=unique_eps)

        for ep in unique_eps:
            qa_annotation = f'@QueryAccess(queryName = "{ep["queryName"]}")'
            if ep["accessLevel"] == "ROLE_BASED":
                assert qa_annotation in code, (
                    f"ROLE_BASED endpoint {ep['methodName']} must have {qa_annotation}"
                )
            # For GLOBAL/PUBLIC, we verify the annotation is NOT in the
            # section immediately before the method declaration
            elif ep["accessLevel"] in ("GLOBAL", "PUBLIC"):
                method_sig = f"public Mono<{entity_name}OutputDTO> {ep['methodName']}"
                if method_sig in code:
                    method_pos = code.index(method_sig)
                    section = code[max(0, method_pos - 200):method_pos]
                    assert qa_annotation not in section, (
                        f"{ep['accessLevel']} endpoint {ep['methodName']} "
                        f"must NOT have {qa_annotation}"
                    )
