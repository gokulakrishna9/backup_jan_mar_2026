"""Template helper modules for code generation property isolation.

This package provides dedicated Python methods for constructing code strings
that would otherwise be built inline within Jinja2 templates. Each method
encapsulates format rules and constraints for a specific code property,
making them independently unit-testable without the Jinja2 template engine.

Modules:
    java_properties: Methods for Java code string construction (swfaw).
    react_properties: Methods for React code string construction (REAW).

Design Principle:
    Templates contain layout only, not logic. All code string construction
    is delegated to these helper methods via the template context.
"""

from workspace_web_app.engine.template_helpers.java_properties import (
    field_declaration,
    getter_signature,
    setter_signature,
    import_statement,
    annotation_string,
    constructor_param,
    repository_method_signature,
)

from workspace_web_app.engine.template_helpers.react_properties import (
    jsx_element,
    prop_type_declaration,
    form_input,
    api_endpoint_path,
    column_header,
    route_path,
)

__all__ = [
    # Java helpers
    "field_declaration",
    "getter_signature",
    "setter_signature",
    "import_statement",
    "annotation_string",
    "constructor_param",
    "repository_method_signature",
    # React helpers
    "jsx_element",
    "prop_type_declaration",
    "form_input",
    "api_endpoint_path",
    "column_header",
    "route_path",
]
