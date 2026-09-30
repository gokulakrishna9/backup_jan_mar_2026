"""Property-based tests for ENTITY_FORM template widget rendering.

**Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5, 6.7**
"""

import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st
from jinja2 import Template

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.property_objects import EntityFormProperties, FormFieldProperties
from templates.entity_component_templates import ENTITY_FORM


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

WIDGET_COMPONENT_MAP = {
    "QuillEditor": "QuillEditorWidget",
    "MonacoEditor": "MonacoEditorWidget",
    "MarkdownEditor": "MarkdownEditorWidget",
    "FileUpload": "FileUploadWidget",
}

WIDGET_IMPORT_MAP = {
    "QuillEditor": "import QuillEditorWidget from",
    "MonacoEditor": "import MonacoEditorWidget from",
    "MarkdownEditor": "import MarkdownEditorWidget from",
    "FileUpload": "import FileUploadWidget from",
}


def _render_form(fields: list[FormFieldProperties], entity_name: str = "Test") -> str:
    """Render the ENTITY_FORM template with given fields."""
    form_props = EntityFormProperties(
        entityName=entity_name,
        entityNamePascal=entity_name,
        entityNameCamel=entity_name[0].lower() + entity_name[1:],
        basePath=f"/api/{entity_name.lower()}",
        pkField="id",
        fields=fields,
        isRootEntity=True,
        hasCreateEndpoint=True,
        hasUpdateEndpoint=True,
        hasDeleteEndpoint=False,
    )
    return Template(ENTITY_FORM).render(**form_props.model_dump())


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

_widget_types = st.sampled_from(["QuillEditor", "MonacoEditor", "MarkdownEditor", "FileUpload"])
_field_names = st.from_regex(r"[a-z][a-zA-Z]{2,10}", fullmatch=True)
_languages = st.sampled_from(["java", "python", "javascript", "json", "sql"])


# ---------------------------------------------------------------------------
# Property 3: Form template renders correct widget component for componentType
# ---------------------------------------------------------------------------

@settings(max_examples=100)
@given(
    component_type=_widget_types,
    field_name=_field_names,
    language=_languages,
)
def test_form_renders_widget_component(
    component_type: str, field_name: str, language: str,
) -> None:
    """Property 3: For any widget componentType, the rendered form contains
    the corresponding widget component tag with value, onChange, disabled props.

    **Validates: Requirements 6.2, 6.3, 6.4, 6.5**
    """
    props = {"fieldWidget": component_type.replace("Editor", "").lower()}
    if component_type == "MonacoEditor":
        props["language"] = language

    field = FormFieldProperties(
        fieldName=field_name,
        fieldLabel=field_name.capitalize(),
        componentType=component_type,
        javaType="String",
        props=props,
    )

    output = _render_form([field])

    widget_tag = WIDGET_COMPONENT_MAP[component_type]
    assert f"<{widget_tag}" in output, (
        f"Expected <{widget_tag} in rendered output for componentType={component_type}"
    )

    # All widget components should have onChange and disabled props
    assert "onChange" in output
    assert "disabled" in output or "isDisabled" in output


# ---------------------------------------------------------------------------
# Property 4: Conditional widget imports match used componentTypes
# ---------------------------------------------------------------------------

@settings(max_examples=100)
@given(
    used_widgets=st.frozensets(
        st.sampled_from(["QuillEditor", "MonacoEditor", "MarkdownEditor", "FileUpload"]),
        min_size=0,
        max_size=4,
    ),
)
def test_conditional_widget_imports(used_widgets: frozenset) -> None:
    """Property 4: The rendered template contains an import for a widget
    component iff at least one field uses that componentType.

    **Validates: Requirements 6.1, 6.7**
    """
    fields = []
    for i, ct in enumerate(used_widgets):
        fields.append(FormFieldProperties(
            fieldName=f"field{i}",
            fieldLabel=f"Field {i}",
            componentType=ct,
            javaType="String",
            props={"fieldWidget": "richText", "language": "javascript"},
        ))
    # Always add a standard field
    fields.append(FormFieldProperties(
        fieldName="normalField",
        fieldLabel="Normal",
        componentType="InputText",
        javaType="String",
    ))

    output = _render_form(fields)

    for widget_ct, import_str in WIDGET_IMPORT_MAP.items():
        if widget_ct in used_widgets:
            assert import_str in output, (
                f"Expected import for {widget_ct} when it's used, but not found"
            )
        else:
            assert import_str not in output, (
                f"Unexpected import for {widget_ct} when it's NOT used"
            )
