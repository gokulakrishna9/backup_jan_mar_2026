"""Unit tests for java_properties.py — independent of Jinja2.

Validates: Requirements 12.5.1, 12.5.3, 12.5.5
"""

import pytest

from workspace_web_app.engine.template_helpers.java_properties import (
    field_declaration,
    getter_signature,
    setter_signature,
    import_statement,
    annotation_string,
    constructor_param,
    repository_method_signature,
)


# ---------------------------------------------------------------------------
# field_declaration
# ---------------------------------------------------------------------------

class TestFieldDeclaration:
    """Tests for field_declaration()."""

    def test_simple_string_field(self):
        field = {
            "fieldName": "name",
            "javaType": "String",
            "columnName": "name",
            "isPrimaryKey": False,
            "isNullable": True,
        }
        result = field_declaration(field)
        assert '@Column("name")' in result
        assert "private String name;" in result
        assert "@Id" not in result

    def test_primary_key_field(self):
        field = {
            "fieldName": "id",
            "javaType": "Long",
            "columnName": "id",
            "isPrimaryKey": True,
            "isNullable": False,
        }
        result = field_declaration(field)
        assert "@Id" in result
        assert '@Column("id")' in result
        assert "private Long id;" in result

    def test_snake_case_column_name(self):
        field = {
            "fieldName": "createdAt",
            "javaType": "LocalDateTime",
            "columnName": "created_at",
            "isPrimaryKey": False,
        }
        result = field_declaration(field)
        assert '@Column("created_at")' in result
        assert "private LocalDateTime createdAt;" in result

    def test_id_annotation_comes_before_column(self):
        field = {
            "fieldName": "id",
            "javaType": "Long",
            "columnName": "id",
            "isPrimaryKey": True,
        }
        result = field_declaration(field)
        id_pos = result.index("@Id")
        col_pos = result.index("@Column")
        assert id_pos < col_pos


# ---------------------------------------------------------------------------
# getter_signature
# ---------------------------------------------------------------------------

class TestGetterSignature:
    """Tests for getter_signature()."""

    def test_string_getter(self):
        field = {"fieldName": "name", "javaType": "String"}
        assert getter_signature(field) == "public String getName()"

    def test_boolean_primitive_uses_is_prefix(self):
        field = {"fieldName": "active", "javaType": "boolean"}
        assert getter_signature(field) == "public boolean isActive()"

    def test_boolean_wrapper_uses_is_prefix(self):
        field = {"fieldName": "enabled", "javaType": "Boolean"}
        assert getter_signature(field) == "public Boolean isEnabled()"

    def test_long_getter(self):
        field = {"fieldName": "id", "javaType": "Long"}
        assert getter_signature(field) == "public Long getId()"

    def test_datetime_getter(self):
        field = {"fieldName": "createdAt", "javaType": "LocalDateTime"}
        assert getter_signature(field) == "public LocalDateTime getCreatedAt()"


# ---------------------------------------------------------------------------
# setter_signature
# ---------------------------------------------------------------------------

class TestSetterSignature:
    """Tests for setter_signature()."""

    def test_string_setter(self):
        field = {"fieldName": "name", "javaType": "String"}
        assert setter_signature(field) == "public void setName(String name)"

    def test_boolean_setter_uses_set_prefix(self):
        field = {"fieldName": "active", "javaType": "boolean"}
        assert setter_signature(field) == "public void setActive(boolean active)"

    def test_long_setter(self):
        field = {"fieldName": "id", "javaType": "Long"}
        assert setter_signature(field) == "public void setId(Long id)"


# ---------------------------------------------------------------------------
# import_statement
# ---------------------------------------------------------------------------

class TestImportStatement:
    """Tests for import_statement()."""

    def test_standard_import(self):
        result = import_statement("LocalDateTime", "java.time")
        assert result == "import java.time.LocalDateTime;"

    def test_spring_import(self):
        result = import_statement("Repository", "org.springframework.stereotype")
        assert result == "import org.springframework.stereotype.Repository;"

    def test_entity_import(self):
        result = import_statement("User", "com.example.entity")
        assert result == "import com.example.entity.User;"


# ---------------------------------------------------------------------------
# annotation_string
# ---------------------------------------------------------------------------

class TestAnnotationString:
    """Tests for annotation_string()."""

    def test_simple_annotation(self):
        assert annotation_string("Override") == "@Override"

    def test_annotation_with_at_prefix(self):
        assert annotation_string("@Override") == "@Override"

    def test_no_params(self):
        assert annotation_string("Repository") == "@Repository"

    def test_empty_params(self):
        assert annotation_string("Repository", {}) == "@Repository"

    def test_single_value_param_shorthand(self):
        result = annotation_string("Query", {"value": "SELECT * FROM users"})
        assert result == '@Query("SELECT * FROM users")'

    def test_boolean_param(self):
        result = annotation_string("Column", {"nullable": False})
        assert result == "@Column(nullable = false)"

    def test_multiple_params_alphabetical(self):
        result = annotation_string(
            "ApiResponse",
            {"responseCode": "200", "description": "OK"},
        )
        assert result == '@ApiResponse(description = "OK", responseCode = "200")'

    def test_none_values_skipped(self):
        result = annotation_string("Column", {"nullable": False, "name": None})
        assert result == "@Column(nullable = false)"

    def test_numeric_param(self):
        result = annotation_string("Max", {"value": 100})
        assert result == "@Max(100)"

    def test_list_param(self):
        result = annotation_string("Tag", {"name": "Users", "description": "User APIs"})
        assert 'name = "Users"' in result
        assert 'description = "User APIs"' in result


# ---------------------------------------------------------------------------
# constructor_param
# ---------------------------------------------------------------------------

class TestConstructorParam:
    """Tests for constructor_param()."""

    def test_string_param(self):
        field = {"fieldName": "name", "javaType": "String", "isNullable": False}
        assert constructor_param(field) == "String name"

    def test_nullable_primitive_promoted_to_wrapper(self):
        field = {"fieldName": "count", "javaType": "int", "isNullable": True}
        assert constructor_param(field) == "Integer count"

    def test_non_nullable_primitive_stays_primitive(self):
        field = {"fieldName": "count", "javaType": "int", "isNullable": False}
        assert constructor_param(field) == "int count"

    def test_nullable_long_primitive(self):
        field = {"fieldName": "id", "javaType": "long", "isNullable": True}
        assert constructor_param(field) == "Long id"

    def test_wrapper_type_unchanged(self):
        field = {"fieldName": "id", "javaType": "Long", "isNullable": True}
        assert constructor_param(field) == "Long id"

    def test_default_nullable_true(self):
        """When isNullable is not specified, defaults to True."""
        field = {"fieldName": "count", "javaType": "int"}
        assert constructor_param(field) == "Integer count"


# ---------------------------------------------------------------------------
# repository_method_signature
# ---------------------------------------------------------------------------

class TestRepositoryMethodSignature:
    """Tests for repository_method_signature()."""

    def test_find_by_email(self):
        result = repository_method_signature(
            "findByEmail",
            "Mono<User>",
            [{"name": "email", "type": "String"}],
        )
        assert result == "Mono<User> findByEmail(String email);"

    def test_find_all_paged(self):
        result = repository_method_signature(
            "findAllPaged",
            "Flux<User>",
            [{"name": "size", "type": "int"}, {"name": "offset", "type": "long"}],
        )
        assert result == "Flux<User> findAllPaged(int size, long offset);"

    def test_count_method(self):
        result = repository_method_signature(
            "countAll",
            "Mono<Long>",
            [],
        )
        assert result == "Mono<Long> countAll();"

    def test_multiple_params(self):
        result = repository_method_signature(
            "findByEntityTypeAndEntityId",
            "Flux<Authorization>",
            [
                {"name": "entityType", "type": "String"},
                {"name": "entityId", "type": "Long"},
            ],
        )
        assert result == (
            "Flux<Authorization> findByEntityTypeAndEntityId"
            "(String entityType, Long entityId);"
        )
