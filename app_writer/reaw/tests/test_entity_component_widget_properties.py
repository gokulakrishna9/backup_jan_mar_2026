"""Property-based tests for EntityComponentTransformer widget column handling.

**Validates: Requirements 11.1, 11.2, 11.3**
"""

import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.react_definition_models import (
    ApiEndpointDef, ApiServiceDefinition, ComponentMapping, FieldMapping, FormGrouping,
)
from transformers.phase2.entity_component_transformer import EntityComponentTransformer, WIDGET_NON_SORTABLE


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

_widget_types = st.sampled_from(["richText", "codeEditor", "markdown", "json"])
_field_names = st.from_regex(r"[a-z][a-zA-Z]{2,12}", fullmatch=True)
_component_types = st.sampled_from(["QuillEditor", "MonacoEditor", "MarkdownEditor"])


# ---------------------------------------------------------------------------
# Property 10: DataTable widget columns are non-sortable
# ---------------------------------------------------------------------------

@settings(max_examples=100)
@given(
    field_name=_field_names,
    field_widget=_widget_types,
    component_type=_component_types,
)
def test_datatable_widget_columns_non_sortable(
    field_name: str, field_widget: str, component_type: str,
) -> None:
    """Property 10: Widget columns have sortable=False and fieldWidget propagated."""
    mapping = ComponentMapping(
        entityName="TestEntity",
        fields=[FieldMapping(
            fieldName=field_name,
            componentType=component_type,
            javaType="String",
            props={"fieldWidget": field_widget},
            includeInDTO=True,
        )],
    )
    svc = ApiServiceDefinition(
        entityName="TestEntity",
        basePath="/api/test",
        endpoints={
            "getAll": ApiEndpointDef(enabled=True, supportsSorting=True),
        },
    )

    results = EntityComponentTransformer.transform([mapping], [svc], [])
    assert len(results) == 1
    _, table_props = results[0]
    assert len(table_props.columns) == 1

    col = table_props.columns[0]
    assert col.sortable is False, f"Widget column should not be sortable, got sortable={col.sortable}"
    assert col.fieldWidget == field_widget, f"Expected fieldWidget={field_widget!r}, got {col.fieldWidget!r}"


@settings(max_examples=100)
@given(field_name=_field_names)
def test_datatable_standard_columns_remain_sortable(field_name: str) -> None:
    """Standard (non-widget) columns remain sortable when sorting is enabled."""
    mapping = ComponentMapping(
        entityName="TestEntity",
        fields=[FieldMapping(
            fieldName=field_name,
            componentType="InputText",
            javaType="String",
            props={},
            includeInDTO=True,
        )],
    )
    svc = ApiServiceDefinition(
        entityName="TestEntity",
        basePath="/api/test",
        endpoints={
            "getAll": ApiEndpointDef(enabled=True, supportsSorting=True),
        },
    )

    results = EntityComponentTransformer.transform([mapping], [svc], [])
    _, table_props = results[0]
    col = table_props.columns[0]
    assert col.sortable is True, "Standard column should be sortable"
    assert col.fieldWidget is None
