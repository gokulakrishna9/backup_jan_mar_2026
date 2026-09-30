"""Unit tests for react_properties.py — independent of Jinja2.

Validates: Requirements 12.5.2, 12.5.3, 12.5.5
"""

import pytest

from workspace_web_app.engine.template_helpers.react_properties import (
    jsx_element,
    prop_type_declaration,
    form_input,
    api_endpoint_path,
    column_header,
    route_path,
)


# ---------------------------------------------------------------------------
# jsx_element
# ---------------------------------------------------------------------------

class TestJsxElement:
    """Tests for jsx_element()."""

    def test_self_closing_no_children(self):
        result = jsx_element("InputText", {"id": "name"})
        assert result == '<InputText id="name" />'

    def test_with_children(self):
        result = jsx_element("div", {"className": "card"}, "Hello")
        assert result == '<div className="card">Hello</div>'

    def test_boolean_true_prop(self):
        result = jsx_element("InputText", {"id": "name", "disabled": True})
        assert result == '<InputText id="name" disabled />'

    def test_boolean_false_prop_omitted(self):
        result = jsx_element("InputText", {"id": "name", "disabled": False})
        assert result == '<InputText id="name" />'

    def test_none_prop_omitted(self):
        result = jsx_element("InputText", {"id": "name", "value": None})
        assert result == '<InputText id="name" />'

    def test_expression_prop(self):
        result = jsx_element("Button", {"label": "Save", "onClick": "{handleSave}"})
        assert result == '<Button label="Save" onClick={handleSave} />'

    def test_numeric_prop(self):
        result = jsx_element("InputTextarea", {"rows": 3})
        assert result == "<InputTextarea rows={3} />"

    def test_empty_props(self):
        result = jsx_element("br", {})
        assert result == "<br />"

    def test_empty_props_with_children(self):
        result = jsx_element("span", {}, "text")
        assert result == "<span>text</span>"


# ---------------------------------------------------------------------------
# prop_type_declaration
# ---------------------------------------------------------------------------

class TestPropTypeDeclaration:
    """Tests for prop_type_declaration()."""

    def test_required_func(self):
        result = prop_type_declaration("onSave", "func")
        assert result == "onSave: PropTypes.func.isRequired,"

    def test_optional_object(self):
        result = prop_type_declaration("data", "object", required=False)
        assert result == "data: PropTypes.object,"

    def test_required_string(self):
        result = prop_type_declaration("name", "string")
        assert result == "name: PropTypes.string.isRequired,"

    def test_optional_bool(self):
        result = prop_type_declaration("showForm", "bool", required=False)
        assert result == "showForm: PropTypes.bool,"

    def test_required_number(self):
        result = prop_type_declaration("count", "number")
        assert result == "count: PropTypes.number.isRequired,"


# ---------------------------------------------------------------------------
# form_input
# ---------------------------------------------------------------------------

class TestFormInput:
    """Tests for form_input()."""

    def test_input_text_field(self):
        field = {
            "fieldName": "email",
            "fieldLabel": "Email",
            "componentType": "InputText",
            "validation": {"required": True},
        }
        result = form_input(field)
        assert 'label htmlFor="email"' in result
        assert "Email" in result
        assert "InputText" in result
        assert "p-error" in result  # required asterisk

    def test_input_number_field(self):
        field = {
            "fieldName": "age",
            "fieldLabel": "Age",
            "componentType": "InputNumber",
            "validation": None,
        }
        result = form_input(field)
        assert "InputNumber" in result
        assert 'id="age"' in result

    def test_textarea_field(self):
        field = {
            "fieldName": "description",
            "fieldLabel": "Description",
            "componentType": "InputTextarea",
        }
        result = form_input(field)
        assert "InputTextarea" in result
        assert "rows={3}" in result

    def test_calendar_field(self):
        field = {
            "fieldName": "startDate",
            "fieldLabel": "Start Date",
            "componentType": "Calendar",
        }
        result = form_input(field)
        assert "Calendar" in result

    def test_checkbox_field(self):
        field = {
            "fieldName": "active",
            "fieldLabel": "Active",
            "componentType": "Checkbox",
        }
        result = form_input(field)
        assert "Checkbox" in result
        assert "checked" in result

    def test_dropdown_field(self):
        field = {
            "fieldName": "status",
            "fieldLabel": "Status",
            "componentType": "Dropdown",
        }
        result = form_input(field)
        assert "Dropdown" in result

    def test_autocomplete_field(self):
        field = {
            "fieldName": "userId",
            "fieldLabel": "User",
            "componentType": "AutoComplete",
        }
        result = form_input(field)
        assert "AutoComplete" in result

    def test_unknown_component_falls_back_to_input_text(self):
        field = {
            "fieldName": "custom",
            "fieldLabel": "Custom",
            "componentType": "UnknownWidget",
        }
        result = form_input(field)
        assert "InputText" in result

    def test_non_required_field_no_asterisk(self):
        field = {
            "fieldName": "notes",
            "fieldLabel": "Notes",
            "componentType": "InputText",
            "validation": {"required": False},
        }
        result = form_input(field)
        assert "p-error" not in result.split("<label")[1].split("</label>")[0] or \
               '<span className="p-error">*</span>' not in result


# ---------------------------------------------------------------------------
# api_endpoint_path
# ---------------------------------------------------------------------------

class TestApiEndpointPath:
    """Tests for api_endpoint_path()."""

    def test_get_all(self):
        assert api_endpoint_path("UserProfile", "getAll") == "/api/userprofile"

    def test_create(self):
        assert api_endpoint_path("UserProfile", "create") == "/api/userprofile"

    def test_get_by_id(self):
        assert api_endpoint_path("UserProfile", "getById") == "/api/userprofile/${id}"

    def test_update(self):
        assert api_endpoint_path("UserProfile", "update") == "/api/userprofile/${id}"

    def test_delete(self):
        assert api_endpoint_path("UserProfile", "delete") == "/api/userprofile/${id}"

    def test_me_endpoint(self):
        assert api_endpoint_path("UserProfile", "me") == "/api/userprofile/me"

    def test_custom_action(self):
        assert api_endpoint_path("Order", "export") == "/api/order/export"

    def test_entity_name_lowercased(self):
        result = api_endpoint_path("JobApplication", "getAll")
        assert result == "/api/jobapplication"


# ---------------------------------------------------------------------------
# column_header
# ---------------------------------------------------------------------------

class TestColumnHeader:
    """Tests for column_header()."""

    def test_explicit_label(self):
        field = {"fieldName": "email", "fieldLabel": "Email Address"}
        assert column_header(field) == "Email Address"

    def test_camel_case_to_title(self):
        field = {"fieldName": "firstName"}
        assert column_header(field) == "First Name"

    def test_primary_key_id(self):
        field = {"fieldName": "id", "isPrimaryKey": True}
        assert column_header(field) == "ID"

    def test_primary_key_with_prefix(self):
        field = {"fieldName": "userId", "isPrimaryKey": True}
        assert column_header(field) == "ID"

    def test_non_pk_id_field(self):
        field = {"fieldName": "userId", "isPrimaryKey": False}
        assert column_header(field) == "User Id"

    def test_single_word(self):
        field = {"fieldName": "name"}
        assert column_header(field) == "Name"

    def test_multi_word_camel(self):
        field = {"fieldName": "createdAt"}
        assert column_header(field) == "Created At"


# ---------------------------------------------------------------------------
# route_path
# ---------------------------------------------------------------------------

class TestRoutePath:
    """Tests for route_path()."""

    def test_simple_entity(self):
        assert route_path("UserProfile") == "/userprofile"

    def test_single_word(self):
        assert route_path("Order") == "/order"

    def test_mixed_case(self):
        assert route_path("JobApplication") == "/jobapplication"
