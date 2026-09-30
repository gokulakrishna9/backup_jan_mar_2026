"""Property-based tests for WidgetGenerator conditional file generation.

**Validates: Requirements 7.2, 7.4**
"""

import os
import sys
import tempfile
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.react_definition_models import (
    ComponentMapping, FieldMapping, ReactAppDefinition,
)
from generators.phase2.widget_generator import WidgetGenerator, WIDGET_TYPE_MAP


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

_widget_component_types = list(WIDGET_TYPE_MAP.keys())
_widget_subsets = st.frozensets(st.sampled_from(_widget_component_types), min_size=0, max_size=4)


# ---------------------------------------------------------------------------
# Property 6: Widget generator produces files only for used widgets
# ---------------------------------------------------------------------------

@settings(max_examples=100)
@given(used_widgets=_widget_subsets)
def test_widget_generator_conditional_files(used_widgets: frozenset) -> None:
    """Property 6: WidgetGenerator produces files only for used widget types."""
    fields = [
        FieldMapping(fieldName=f"field{i}", componentType=ct, javaType="String", includeInDTO=True)
        for i, ct in enumerate(used_widgets)
    ]
    # Add a standard field to ensure it doesn't trigger widget generation
    fields.append(FieldMapping(fieldName="normalField", componentType="InputText", javaType="String", includeInDTO=True))

    react_def = ReactAppDefinition(
        component_mappings=[ComponentMapping(entityName="Test", fields=fields)],
    )

    with tempfile.TemporaryDirectory() as tmp:
        result = WidgetGenerator.generate(react_def, tmp)

        expected_files = {WIDGET_TYPE_MAP[ct][0] for ct in used_widgets}
        actual_files = {os.path.basename(p) for p in result}

        assert actual_files == expected_files, (
            f"Expected files {expected_files}, got {actual_files}"
        )

        # All returned paths should exist on disk
        for p in result:
            assert os.path.exists(p), f"Generated file should exist: {p}"
            assert os.path.getsize(p) > 0, f"Generated file should be non-empty: {p}"


def test_widget_generator_no_widgets_produces_nothing() -> None:
    """When no widget componentTypes are used, zero files generated."""
    react_def = ReactAppDefinition(
        component_mappings=[ComponentMapping(
            entityName="Test",
            fields=[FieldMapping(fieldName="name", componentType="InputText", javaType="String", includeInDTO=True)],
        )],
    )

    with tempfile.TemporaryDirectory() as tmp:
        result = WidgetGenerator.generate(react_def, tmp)
        assert result == [], f"Expected empty list, got {result}"
