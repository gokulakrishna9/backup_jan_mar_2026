"""Property-based tests for ComponentMappingTransformer widget override.

**Validates: Requirements 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 10.1, 10.2, 10.3, 12.3, 12.4**
"""

import sys
from pathlib import Path

from hypothesis import given, settings, assume
from hypothesis import strategies as st

# Ensure reaw/ is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.definition_models import (
    DtoFieldDef, DtoLayerEntry, DtoLayerDef,
    EntityLayerEntry, EntityLayerDef, RelationshipsDef,
)
from transformers.phase1.component_mapping_transformer import (
    ComponentMappingTransformer, WIDGET_COMPONENT_MAP,
)
from utils.type_mapping import TypeMapper


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_inputs(field_name: str, java_type: str,
                  field_widget: str | None = None,
                  language: str | None = None):
    """Build minimal DtoLayerDef, RelationshipsDef, EntityLayerDef for one field."""
    dto_field = DtoFieldDef(
        fieldName=field_name,
        javaType=java_type,
        includeInDTO=True,
        fieldWidget=field_widget,
        language=language,
    )
    dto_layer = DtoLayerDef(dtos=[
        DtoLayerEntry(
            entityName="TestEntity",
            dtoType="Input",
            className="TestEntityInputDTO",
            packageName="com.example.dto",
            fields=[dto_field],
        ),
    ])
    entity_layer = EntityLayerDef(entities=[
        EntityLayerEntry(tableName="test_entity", className="TestEntity"),
    ])
    relationships = RelationshipsDef(relationships=[])
    return dto_layer, relationships, entity_layer


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

_widget_field_widgets = st.sampled_from(["richText", "codeEditor", "markdown", "json"])
_languages = st.sampled_from(["java", "python", "javascript", "sql", "json", "xml", "yaml", "go", "rust"])
_field_names = st.from_regex(r"[a-z][a-zA-Z]{2,12}", fullmatch=True)
_java_types = st.sampled_from(["String", "Long", "Integer", "Boolean", "LocalDate", "LocalDateTime", "BigDecimal"])

# Expected mapping table
EXPECTED_COMPONENT_TYPE = {
    "richText": "QuillEditor",
    "codeEditor": "MonacoEditor",
    "markdown": "MarkdownEditor",
    "json": "MonacoEditor",
}


# ---------------------------------------------------------------------------
# Property 1: fieldWidget to componentType round-trip
# ---------------------------------------------------------------------------

@settings(max_examples=100)
@given(
    field_widget=_widget_field_widgets,
    language=_languages,
    field_name=_field_names,
    java_type=_java_types,
)
def test_field_widget_to_component_type_round_trip(
    field_widget: str, language: str, field_name: str, java_type: str,
) -> None:
    """Property 1: For any valid fieldWidget, ComponentMappingTransformer
    produces the correct componentType and props.language.

    **Validates: Requirements 1.1, 1.2, 1.4, 1.5, 1.6, 1.7, 1.8, 10.1, 10.3**
    """
    dto_layer, rels, entity_layer = _build_inputs(
        field_name, java_type, field_widget,
        language if field_widget == "codeEditor" else None,
    )

    mappings = ComponentMappingTransformer.transform(dto_layer, rels, entity_layer)
    assert len(mappings) == 1
    assert len(mappings[0].fields) == 1

    fm = mappings[0].fields[0]

    # componentType matches the mapping table
    expected_ct = EXPECTED_COMPONENT_TYPE[field_widget]
    assert fm.componentType == expected_ct, (
        f"fieldWidget={field_widget!r} → expected componentType={expected_ct!r}, got {fm.componentType!r}"
    )

    # props.fieldWidget matches original
    assert fm.props.get("fieldWidget") == field_widget

    # props.language is correct per widget type
    if field_widget == "codeEditor":
        assert fm.props.get("language") == language
    elif field_widget == "json":
        assert fm.props.get("language") == "json"
    elif field_widget == "markdown":
        assert fm.props.get("language") == "markdown"
    elif field_widget == "richText":
        # richText has no language prop
        assert "language" not in fm.props


# ---------------------------------------------------------------------------
# Property 2: Backward compatibility — absent fieldWidget preserves TypeMapper
# ---------------------------------------------------------------------------

@settings(max_examples=100)
@given(
    field_name=_field_names,
    java_type=_java_types,
    field_widget=st.sampled_from([None, "text"]),
)
def test_absent_field_widget_preserves_type_mapper(
    field_name: str, java_type: str, field_widget: str | None,
) -> None:
    """Property 2: When fieldWidget is None or "text", ComponentMappingTransformer
    produces the same componentType as TypeMapper. No widget props present.

    **Validates: Requirements 1.3, 10.2, 12.3, 12.4**
    """
    dto_layer, rels, entity_layer = _build_inputs(field_name, java_type, field_widget)

    mappings = ComponentMappingTransformer.transform(dto_layer, rels, entity_layer)
    assert len(mappings) == 1
    assert len(mappings[0].fields) == 1

    fm = mappings[0].fields[0]

    # Should match TypeMapper output
    expected = TypeMapper.map_to_component(java_type=java_type, column_definition="")
    assert fm.componentType == expected.component_type, (
        f"java_type={java_type!r}, fieldWidget={field_widget!r} → "
        f"expected {expected.component_type!r}, got {fm.componentType!r}"
    )

    # No widget-related props
    assert "fieldWidget" not in fm.props
    assert "language" not in fm.props or fm.props.get("language") is None
