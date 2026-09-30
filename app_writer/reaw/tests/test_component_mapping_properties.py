"""Property-based tests for ComponentMappingTransformer widget override.

Feature: react-field-widgets
Property 1: fieldWidget to componentType round-trip

**Validates: Requirements 1.1, 1.2, 1.4, 1.5, 1.6, 1.7, 1.8, 10.1, 10.3**
"""

import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

# Ensure reaw/ is on sys.path so transformer/model imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.definition_models import (
    DtoFieldDef,
    DtoLayerDef,
    DtoLayerEntry,
    EntityLayerDef,
    EntityLayerEntry,
    RelationshipsDef,
)
from transformers.phase1.component_mapping_transformer import (
    WIDGET_COMPONENT_MAP,
    ComponentMappingTransformer,
)

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

_field_widget_st = st.sampled_from(["richText", "codeEditor", "markdown", "json"])

_language_st = st.sampled_from(
    ["java", "python", "javascript", "sql", "json", "xml", "yaml"]
)

_entity_name_st = st.from_regex(r"[A-Z][a-zA-Z]{2,12}", fullmatch=True)

_field_name_st = st.from_regex(r"[a-z][a-zA-Z]{2,12}", fullmatch=True)
