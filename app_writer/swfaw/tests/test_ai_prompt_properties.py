"""Property-based tests for PromptTemplateEngine — Correctness Properties.

**Validates: Requirements 3.13, 3.14, 3.15, 3.19, 3.20, 3.21, 3.22**

# Feature: ai-layer, Property 6: PromptTemplateEngine Correctness
"""

import re
import sys
from pathlib import Path

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

# Ensure swfaw/ is on sys.path so imports resolve
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# ---------------------------------------------------------------------------
# Placeholder regex — mirrors the Java template
# ---------------------------------------------------------------------------

PLACEHOLDER_PATTERN = re.compile(r"\{\{([^{}]+)\}\}")


# ---------------------------------------------------------------------------
# Python mirror of PromptTemplateEngine.interpolate() logic
# ---------------------------------------------------------------------------

class PromptTemplateEngine:
    """Python mirror of the generated Java PromptTemplateEngine.interpolate().

    Mirrors the Jinja2 template at
    swfaw/templates/ai/service/prompt_template_engine.java.j2
    """

    def interpolate(self, template: str | None, values: dict[str, object] | None) -> str:
        """Interpolate all {{placeholder}} patterns in the template.

        Single-pass replacement — values containing {{...}} are NOT
        recursively interpolated.

        Args:
            template: The template string (may be None or empty).
            values: The value map (may be None or empty).

        Returns:
            The interpolated string, or "" if template is None/empty.
        """
        if template is None:
            return ""
        if template == "":
            return ""
        if values is None or len(values) == 0:
            return template

        result: list[str] = []
        last_end = 0

        for match in PLACEHOLDER_PATTERN.finditer(template):
            key = match.group(1).strip()
            result.append(template[last_end:match.start()])
            if key in values:
                result.append(str(values[key]))
            else:
                # Leave unresolved placeholder unchanged
                result.append(match.group(0))
            last_end = match.end()

        result.append(template[last_end:])
        return "".join(result)


# ---------------------------------------------------------------------------
# Hypothesis strategies
# ---------------------------------------------------------------------------

# Alphanumeric placeholder names (valid identifiers)
_placeholder_name_st = st.from_regex(r"[a-zA-Z][a-zA-Z0-9_]{0,15}", fullmatch=True)

# Simple value strings (no placeholder patterns)
_simple_value_st = st.text(
    alphabet=st.characters(blacklist_categories=("Cs",), blacklist_characters="{}"),
    min_size=0,
    max_size=30,
)

# Value strings that may contain {{...}} patterns (for single-pass testing)
_value_with_placeholders_st = st.one_of(
    _simple_value_st,
    _placeholder_name_st.map(lambda n: "{{" + n + "}}"),
    st.tuples(_simple_value_st, _placeholder_name_st, _simple_value_st).map(
        lambda t: t[0] + "{{" + t[1] + "}}" + t[2]
    ),
)

# General value types (mirroring String.valueOf for non-strings)
_value_st = st.one_of(
    _simple_value_st,
    st.integers(min_value=-10000, max_value=10000).map(str),
    st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False).map(str),
    st.booleans().map(str),
)


@st.composite
def template_and_full_values_st(draw):
    """Generate a template with {{placeholders}} and a value map covering ALL keys.

    Returns (template_string, value_map, placeholder_names).
    """
    # Generate 1-5 unique placeholder names
    names = draw(st.lists(_placeholder_name_st, min_size=1, max_size=5, unique=True))

    # Build a template by interleaving text segments and placeholders
    segments: list[str] = []
    for name in names:
        prefix = draw(st.text(
            alphabet=st.characters(blacklist_categories=("Cs",), blacklist_characters="{}"),
            min_size=0,
            max_size=15,
        ))
        segments.append(prefix)
        segments.append("{{" + name + "}}")

    # Optional trailing text
    suffix = draw(st.text(
        alphabet=st.characters(blacklist_categories=("Cs",), blacklist_characters="{}"),
        min_size=0,
        max_size=15,
    ))
    segments.append(suffix)

    template = "".join(segments)

    # Build value map with ALL placeholder keys
    values = {}
    for name in names:
        values[name] = draw(_value_st)

    return template, values, names


@st.composite
def template_and_partial_values_st(draw):
    """Generate a template and a value map that may be missing some keys."""
    names = draw(st.lists(_placeholder_name_st, min_size=1, max_size=5, unique=True))

    segments: list[str] = []
    for name in names:
        prefix = draw(st.text(
            alphabet=st.characters(blacklist_categories=("Cs",), blacklist_characters="{}"),
            min_size=0,
            max_size=15,
        ))
        segments.append(prefix)
        segments.append("{{" + name + "}}")

    suffix = draw(st.text(
        alphabet=st.characters(blacklist_categories=("Cs",), blacklist_characters="{}"),
        min_size=0,
        max_size=15,
    ))
    segments.append(suffix)

    template = "".join(segments)

    # Only include a subset of keys
    included = draw(st.lists(st.sampled_from(names), unique=True, min_size=0, max_size=len(names)))
    values = {}
    for name in included:
        values[name] = draw(_value_st)

    return template, values, names, set(included)


@st.composite
def template_with_recursive_values_st(draw):
    """Generate a template where values themselves contain {{...}} patterns."""
    names = draw(st.lists(_placeholder_name_st, min_size=1, max_size=4, unique=True))

    segments: list[str] = []
    for name in names:
        prefix = draw(st.text(
            alphabet=st.characters(blacklist_categories=("Cs",), blacklist_characters="{}"),
            min_size=0,
            max_size=10,
        ))
        segments.append(prefix)
        segments.append("{{" + name + "}}")

    template = "".join(segments)

    # Build values where at least one contains a {{...}} pattern
    values = {}
    for i, name in enumerate(names):
        if i == 0:
            # First value always contains a placeholder pattern
            inner_name = draw(_placeholder_name_st)
            values[name] = "prefix_{{" + inner_name + "}}_suffix"
        else:
            values[name] = draw(_value_with_placeholders_st)

    return template, values, names


# ---------------------------------------------------------------------------
# Property tests
# ---------------------------------------------------------------------------

engine = PromptTemplateEngine()


class TestPromptTemplateEngineCorrectness:
    """Property 6: PromptTemplateEngine Correctness.

    For any valid template string containing {{placeholder}} patterns and a
    value map, the engine SHALL satisfy round-trip, identity, and single-pass
    properties.

    **Validates: Requirements 3.13, 3.14, 3.15, 3.19, 3.20, 3.21, 3.22**
    """

    @given(data=template_and_full_values_st())
    @settings(max_examples=30, deadline=None)
    def test_round_trip_all_placeholders_replaced(self, data):
        """When the map contains all referenced keys, no {{...}} remain.

        **Validates: Requirements 3.13, 3.14, 3.19**
        """
        template, values, names = data

        result = engine.interpolate(template, values)

        # No unreplaced placeholders should remain
        remaining = PLACEHOLDER_PATTERN.findall(result)
        # Filter to only placeholders that were in the original template
        original_placeholders = set(names)
        unresolved = [p.strip() for p in remaining if p.strip() in original_placeholders]
        assert len(unresolved) == 0, (
            f"Unreplaced placeholders found: {unresolved}\n"
            f"Template: {template!r}\n"
            f"Values: {values!r}\n"
            f"Result: {result!r}"
        )

    @given(data=template_and_full_values_st())
    @settings(max_examples=30, deadline=None)
    def test_round_trip_values_present_in_output(self, data):
        """Each value appears in the output at the correct position.

        **Validates: Requirements 3.13, 3.14**
        """
        template, values, names = data

        # Only check values that don't themselves look like placeholders
        # (to avoid confusion with single-pass behavior)
        safe_values = {k: v for k, v in values.items()
                       if "{{" not in v and "}}" not in v}
        assume(len(safe_values) > 0)

        result = engine.interpolate(template, values)

        for key, val in safe_values.items():
            assert val in result, (
                f"Value for '{key}' ({val!r}) not found in result.\n"
                f"Template: {template!r}\n"
                f"Result: {result!r}"
            )

    @given(template=st.text(min_size=1, max_size=100))
    @settings(max_examples=30, deadline=None)
    def test_identity_empty_map(self, template):
        """Empty value map returns the original template unchanged.

        **Validates: Requirements 3.20**
        """
        result = engine.interpolate(template, {})
        assert result == template, (
            f"Identity violated: expected template unchanged.\n"
            f"Template: {template!r}\n"
            f"Result: {result!r}"
        )

    @given(template=st.text(min_size=1, max_size=100))
    @settings(max_examples=30, deadline=None)
    def test_identity_none_map(self, template):
        """None value map returns the original template unchanged.

        **Validates: Requirements 3.20**
        """
        result = engine.interpolate(template, None)
        assert result == template, (
            f"Identity violated with None map.\n"
            f"Template: {template!r}\n"
            f"Result: {result!r}"
        )

    @given(data=template_with_recursive_values_st())
    @settings(max_examples=30, deadline=None)
    def test_single_pass_no_recursive_interpolation(self, data):
        """Values containing {{...}} are NOT recursively interpolated.

        **Validates: Requirements 3.19, 3.22**
        """
        template, values, names = data

        result = engine.interpolate(template, values)

        # The values that contain {{...}} should appear verbatim in the output
        for name in names:
            val = values[name]
            if "{{" in val:
                assert val in result, (
                    f"Value for '{name}' ({val!r}) should appear verbatim "
                    f"(single-pass), but not found in result.\n"
                    f"Template: {template!r}\n"
                    f"Result: {result!r}"
                )

    def test_null_template_returns_empty(self):
        """Null template returns empty string.

        **Validates: Requirements 3.22**
        """
        result = engine.interpolate(None, {"key": "value"})
        assert result == ""

    def test_empty_template_returns_empty(self):
        """Empty template returns empty string.

        **Validates: Requirements 3.22**
        """
        result = engine.interpolate("", {"key": "value"})
        assert result == ""

    @given(template=st.text(
        alphabet=st.characters(blacklist_categories=("Cs",), blacklist_characters="{}"),
        min_size=1,
        max_size=100,
    ))
    @settings(max_examples=30, deadline=None)
    def test_no_placeholders_returns_unchanged(self, template):
        """Template with no {{...}} patterns returns unchanged.

        **Validates: Requirements 3.13**
        """
        values = {"someKey": "someValue", "another": "val"}
        result = engine.interpolate(template, values)
        assert result == template, (
            f"Template without placeholders should be unchanged.\n"
            f"Template: {template!r}\n"
            f"Result: {result!r}"
        )

    @given(data=template_and_partial_values_st())
    @settings(max_examples=30, deadline=None)
    def test_unresolved_placeholders_left_unchanged(self, data):
        """Placeholders without map entries are left unchanged.

        **Validates: Requirements 3.15**
        """
        template, values, names, included_keys = data
        missing_keys = set(names) - included_keys
        assume(len(missing_keys) > 0)

        result = engine.interpolate(template, values)

        # Each missing key's placeholder should still be in the output
        for key in missing_keys:
            placeholder = "{{" + key + "}}"
            assert placeholder in result, (
                f"Unresolved placeholder '{placeholder}' should remain "
                f"in output but was not found.\n"
                f"Template: {template!r}\n"
                f"Values: {values!r}\n"
                f"Result: {result!r}"
            )

    @given(data=template_and_full_values_st())
    @settings(max_examples=30, deadline=None)
    def test_nested_braces_innermost_replaced(self, data):
        """Nested braces like {{{value}}} — only innermost {{value}} replaced.

        **Validates: Requirements 3.21**
        """
        template, values, names = data

        # Wrap each placeholder in an extra layer of braces
        nested_template = template
        for name in names:
            nested_template = nested_template.replace(
                "{{" + name + "}}",
                "{{{" + name + "}}}",
            )

        result = engine.interpolate(nested_template, values)

        # The innermost {{name}} should be replaced, leaving the outer { }
        for name in names:
            val = values[name]
            expected_fragment = "{" + val + "}"
            assert expected_fragment in result, (
                f"Nested braces: expected '{expected_fragment}' in result.\n"
                f"Nested template: {nested_template!r}\n"
                f"Result: {result!r}"
            )
