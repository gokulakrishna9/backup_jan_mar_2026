"""Property-based tests for ScaffoldTransformer conditional widget npm dependencies.

**Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5**
"""

import re
import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from models.react_definition_models import (
    ComponentMapping, FieldMapping, ReactAppDefinition,
)
from transformers.phase2.scaffold_transformer import ScaffoldTransformer


# ---------------------------------------------------------------------------
# Expected dependency mapping
# ---------------------------------------------------------------------------

WIDGET_NPM_DEPS = {
    "QuillEditor": {"quill", "react-quill-new", "katex"},
    "MonacoEditor": {"@monaco-editor/react", "monaco-editor"},
    "MarkdownEditor": {"@monaco-editor/react", "monaco-editor", "marked", "dompurify"},
}

_SEMVER_RE = re.compile(r"^\^?\d+\.\d+\.\d+$")

_widget_component_types = list(WIDGET_NPM_DEPS.keys())
_widget_subsets = st.frozensets(st.sampled_from(_widget_component_types), min_size=0, max_size=3)


# ---------------------------------------------------------------------------
# Property 5: Conditional npm dependencies match used widget componentTypes
# ---------------------------------------------------------------------------

@settings(max_examples=100)
@given(used_widgets=_widget_subsets)
def test_scaffold_widget_dependencies_match_used_widgets(used_widgets: frozenset) -> None:
    """Property 5: ScaffoldTransformer produces widgetDependencies containing
    exactly the required npm packages for used widgets and no others.

    **Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5**
    """
    fields = [
        FieldMapping(fieldName=f"f{i}", componentType=ct, javaType="String", includeInDTO=True)
        for i, ct in enumerate(used_widgets)
    ]
    # Add a standard field
    fields.append(FieldMapping(fieldName="name", componentType="InputText", javaType="String", includeInDTO=True))

    react_def = ReactAppDefinition(
        component_mappings=[ComponentMapping(entityName="Test", fields=fields)],
    )

    scaffold, _ = ScaffoldTransformer.transform(react_def)

    # Compute expected package names
    expected_packages = set()
    for widget in used_widgets:
        expected_packages.update(WIDGET_NPM_DEPS[widget])

    actual_packages = set(scaffold.widgetDependencies.keys())
    assert actual_packages == expected_packages, (
        f"Used widgets: {used_widgets}\n"
        f"Expected packages: {expected_packages}\n"
        f"Actual packages: {actual_packages}"
    )

    # All version values should be valid semver ranges
    for dep, ver in scaffold.widgetDependencies.items():
        assert _SEMVER_RE.match(ver), f"Invalid semver for {dep}: {ver!r}"


def test_scaffold_no_widgets_no_deps() -> None:
    """When no widget componentTypes are used, widgetDependencies is empty."""
    react_def = ReactAppDefinition(
        component_mappings=[ComponentMapping(
            entityName="Test",
            fields=[FieldMapping(fieldName="name", componentType="InputText", javaType="String", includeInDTO=True)],
        )],
    )
    scaffold, _ = ScaffoldTransformer.transform(react_def)
    assert scaffold.widgetDependencies == {}
