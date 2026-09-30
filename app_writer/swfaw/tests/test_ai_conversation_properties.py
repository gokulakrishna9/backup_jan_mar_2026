"""Property-based tests for ConversationMemoryService — Correctness Properties.

**Validates: Requirements 3.1, 3.8, 3.12**

# Feature: ai-layer, Property 7: Role Prompt Sequence Order Preservation
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
# (Reused from test_ai_prompt_properties.py)
# ---------------------------------------------------------------------------

class PromptTemplateEngine:
    """Python mirror of the generated Java PromptTemplateEngine.interpolate()."""

    def interpolate(self, template: str | None, values: dict[str, object] | None) -> str:
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
                result.append(match.group(0))
            last_end = match.end()

        result.append(template[last_end:])
        return "".join(result)


# ---------------------------------------------------------------------------
# Python mirror of buildRolePromptMessages() from ConversationMemoryService
# ---------------------------------------------------------------------------

_engine = PromptTemplateEngine()


def build_role_prompt_messages(
    role_prompt_sequence: list[dict[str, str]] | None,
    context_values: dict[str, object] | None,
) -> list[tuple[str, str]]:
    """Python mirror of ConversationMemoryService.buildRolePromptMessages().

    Takes a rolePromptSequence (list of {role, content} dicts) and a context
    values map.  For each entry, interpolates the content using the
    PromptTemplateEngine logic.  Returns a list of (role, interpolated_content)
    tuples preserving the original ordering.

    Mirrors the Java template at
    swfaw/templates/ai/service/conversation_memory_service.java.j2
    """
    if role_prompt_sequence is None or len(role_prompt_sequence) == 0:
        return []

    values = context_values if context_values is not None else {}
    messages: list[tuple[str, str]] = []

    for entry in role_prompt_sequence:
        role = entry.get("role")
        content = entry.get("content")
        interpolated = _engine.interpolate(content, values)
        messages.append((role, interpolated))

    return messages


# ---------------------------------------------------------------------------
# Hypothesis strategies
# ---------------------------------------------------------------------------

VALID_ROLES = ["system", "user", "assistant"]

_role_st = st.sampled_from(VALID_ROLES)

_placeholder_name_st = st.from_regex(r"[a-zA-Z][a-zA-Z0-9_]{0,15}", fullmatch=True)

_simple_text_st = st.text(
    alphabet=st.characters(blacklist_categories=("Cs",), blacklist_characters="{}"),
    min_size=0,
    max_size=30,
)

_value_st = st.one_of(
    _simple_text_st,
    st.integers(min_value=-10000, max_value=10000).map(str),
    st.booleans().map(str),
)


@st.composite
def role_prompt_entry_st(draw):
    """Generate a single rolePromptSequence entry with optional {{placeholders}}."""
    role = draw(_role_st)
    # Build content that may contain placeholders
    use_placeholder = draw(st.booleans())
    if use_placeholder:
        prefix = draw(_simple_text_st)
        name = draw(_placeholder_name_st)
        suffix = draw(_simple_text_st)
        content = prefix + "{{" + name + "}}" + suffix
    else:
        content = draw(_simple_text_st)
    return {"role": role, "content": content}


@st.composite
def role_prompt_sequence_and_context_st(draw):
    """Generate a rolePromptSequence array and a context values map.

    Returns (sequence, context_values).
    """
    sequence = draw(st.lists(role_prompt_entry_st(), min_size=1, max_size=10))

    # Collect all placeholder names from the sequence
    all_placeholders: set[str] = set()
    for entry in sequence:
        content = entry.get("content", "")
        for match in PLACEHOLDER_PATTERN.finditer(content):
            all_placeholders.add(match.group(1).strip())

    # Build context map — may cover all, some, or none of the placeholders
    context: dict[str, str] = {}
    for name in all_placeholders:
        if draw(st.booleans()):
            context[name] = draw(_value_st)

    # Optionally add extra keys not in any placeholder
    extra_keys = draw(st.lists(_placeholder_name_st, min_size=0, max_size=3, unique=True))
    for key in extra_keys:
        if key not in context:
            context[key] = draw(_value_st)

    return sequence, context


# ---------------------------------------------------------------------------
# Property tests
# ---------------------------------------------------------------------------


class TestRolePromptSequenceOrderPreservation:
    """Property 7: Role Prompt Sequence Order Preservation.

    For any valid rolePromptSequence array and context map, interpolating all
    {{placeholder}} variables in the content fields SHALL produce a list of
    messages whose role sequence is identical to the original rolePromptSequence
    role sequence.  Interpolation affects content only, never role ordering.

    **Validates: Requirements 3.1, 3.8, 3.12**
    """

    @given(data=role_prompt_sequence_and_context_st())
    @settings(max_examples=30, deadline=None)
    def test_role_order_preserved_after_interpolation(self, data):
        """Output role sequence is identical to input role sequence.

        **Validates: Requirements 3.1, 3.8, 3.12**
        """
        sequence, context = data

        result = build_role_prompt_messages(sequence, context)

        input_roles = [entry["role"] for entry in sequence]
        output_roles = [role for role, _ in result]

        assert output_roles == input_roles, (
            f"Role order changed after interpolation!\n"
            f"Input roles:  {input_roles}\n"
            f"Output roles: {output_roles}\n"
            f"Context: {context}"
        )

    @given(data=role_prompt_sequence_and_context_st())
    @settings(max_examples=30, deadline=None)
    def test_interpolation_only_affects_content(self, data):
        """Roles in output match roles in input — interpolation never mutates roles.

        **Validates: Requirements 3.1, 3.8**
        """
        sequence, context = data

        result = build_role_prompt_messages(sequence, context)

        for i, (out_role, _) in enumerate(result):
            assert out_role == sequence[i]["role"], (
                f"Role at index {i} changed from {sequence[i]['role']!r} "
                f"to {out_role!r} after interpolation."
            )

    def test_empty_sequence_returns_empty(self):
        """Empty rolePromptSequence produces empty output.

        **Validates: Requirements 3.1**
        """
        assert build_role_prompt_messages([], {"key": "val"}) == []

    def test_none_sequence_returns_empty(self):
        """None rolePromptSequence produces empty output.

        **Validates: Requirements 3.1**
        """
        assert build_role_prompt_messages(None, {"key": "val"}) == []

    @given(data=role_prompt_sequence_and_context_st())
    @settings(max_examples=30, deadline=None)
    def test_empty_context_leaves_content_unchanged(self, data):
        """Empty context map returns content unchanged (identity).

        **Validates: Requirements 3.12**
        """
        sequence, _ = data

        result = build_role_prompt_messages(sequence, {})

        for i, (role, content) in enumerate(result):
            assert content == sequence[i]["content"], (
                f"Content at index {i} changed with empty context.\n"
                f"Expected: {sequence[i]['content']!r}\n"
                f"Got:      {content!r}"
            )

    @given(data=role_prompt_sequence_and_context_st())
    @settings(max_examples=30, deadline=None)
    def test_output_count_equals_input_count(self, data):
        """Number of output messages equals number of input entries.

        **Validates: Requirements 3.1, 3.8**
        """
        sequence, context = data

        result = build_role_prompt_messages(sequence, context)

        assert len(result) == len(sequence), (
            f"Output count {len(result)} != input count {len(sequence)}"
        )
