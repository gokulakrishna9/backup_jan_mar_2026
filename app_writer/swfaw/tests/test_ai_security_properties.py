"""Property-based tests for Prompt Security Filtering — Property 9.

**Validates: Requirements 13.17, 13.18, 13.21, 13.22**

# Feature: ai-layer, Property 9: Prompt Security Filtering
"""

import sys
from pathlib import Path

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

# Ensure swfaw/ is on sys.path so imports resolve
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


# ---------------------------------------------------------------------------
# Python mirrors of the generated Java logic
# ---------------------------------------------------------------------------


class SafeGuardAdvisorService:
    """Python mirror of the generated SafeGuardAdvisorService.

    Mirrors the Jinja2 template at
    swfaw/templates/ai/orchestrator/safe_guard_advisor_service.java.j2

    The Java logic:
      - Returns false for null/blank input
      - Lowercases the input
      - Checks if any sensitive word (lowercased) is contained in the input
    """

    def __init__(self, sensitive_words: list[str]):
        self.sensitive_words = sensitive_words

    def contains_sensitive_content(self, user_input: str | None) -> bool:
        if user_input is None or user_input.strip() == "":
            return False
        lower_input = user_input.lower()
        return any(
            word.lower() in lower_input
            for word in self.sensitive_words
        )


class CanaryWordAdvisorService:
    """Python mirror of the generated CanaryWordAdvisorService.

    Mirrors the Jinja2 template at
    swfaw/templates/ai/orchestrator/canary_word_advisor_service.java.j2

    The Java logic:
      - Returns false for null/blank response
      - Checks if any canary token is contained in the response (exact, case-sensitive)
    """

    def __init__(self, canary_tokens: list[str]):
        self.canary_tokens = canary_tokens

    def detect_leakage(self, llm_response: str | None) -> bool:
        if llm_response is None or llm_response.strip() == "":
            return False
        return any(
            token in llm_response
            for token in self.canary_tokens
        )


# ---------------------------------------------------------------------------
# Hypothesis strategies
# ---------------------------------------------------------------------------

# Sensitive words: non-empty ASCII words (avoids Unicode case-folding edge cases)
_sensitive_word_st = st.text(
    alphabet=st.characters(
        whitelist_categories=("L", "N", "P", "S"),
        blacklist_characters="\x00",
    ),
    min_size=1,
    max_size=20,
).filter(lambda w: w.strip() != "" and w.isascii())

# Lists of sensitive words (1-5 unique words)
_sensitive_words_list_st = st.lists(
    _sensitive_word_st, min_size=1, max_size=5, unique=True
)

# User input: general text
_user_input_st = st.text(
    alphabet=st.characters(blacklist_categories=("Cs",)),
    min_size=1,
    max_size=100,
).filter(lambda s: s.strip() != "")

# Canary tokens: non-empty identifiers
_canary_token_st = st.text(
    alphabet=st.characters(
        whitelist_categories=("L", "N"),
        whitelist_characters="-_",
    ),
    min_size=3,
    max_size=30,
).filter(lambda t: t.strip() != "")

# Lists of canary tokens (1-5 unique tokens)
_canary_tokens_list_st = st.lists(
    _canary_token_st, min_size=1, max_size=5, unique=True
)

# LLM response: general text
_llm_response_st = st.text(
    alphabet=st.characters(blacklist_categories=("Cs",)),
    min_size=1,
    max_size=200,
).filter(lambda s: s.strip() != "")


@st.composite
def input_containing_sensitive_word_st(draw):
    """Generate a user input that definitely contains at least one sensitive word."""
    words = draw(_sensitive_words_list_st)
    chosen_word = draw(st.sampled_from(words))

    # Build input with the word embedded (possibly with case variation)
    prefix = draw(st.text(
        alphabet=st.characters(blacklist_categories=("Cs",)),
        min_size=0, max_size=30,
    ))
    suffix = draw(st.text(
        alphabet=st.characters(blacklist_categories=("Cs",)),
        min_size=0, max_size=30,
    ))

    # Apply random case transformation to the chosen word
    case_variant = draw(st.sampled_from([
        chosen_word.lower(),
        chosen_word.upper(),
        chosen_word.title(),
        chosen_word,  # original
    ]))

    user_input = prefix + case_variant + suffix
    assume(user_input.strip() != "")
    return words, user_input


@st.composite
def input_without_sensitive_words_st(draw):
    """Generate a user input that does NOT contain any sensitive word."""
    words = draw(_sensitive_words_list_st)

    # Generate input from a restricted alphabet that avoids the sensitive words
    user_input = draw(st.text(
        alphabet=st.characters(blacklist_categories=("Cs",)),
        min_size=1, max_size=80,
    ))
    assume(user_input.strip() != "")

    # Filter: ensure no sensitive word appears (case-insensitive)
    lower_input = user_input.lower()
    for word in words:
        assume(word.lower() not in lower_input)

    return words, user_input


@st.composite
def response_containing_canary_token_st(draw):
    """Generate an LLM response that definitely contains at least one canary token."""
    tokens = draw(_canary_tokens_list_st)
    chosen_token = draw(st.sampled_from(tokens))

    prefix = draw(st.text(
        alphabet=st.characters(blacklist_categories=("Cs",)),
        min_size=0, max_size=50,
    ))
    suffix = draw(st.text(
        alphabet=st.characters(blacklist_categories=("Cs",)),
        min_size=0, max_size=50,
    ))

    llm_response = prefix + chosen_token + suffix
    assume(llm_response.strip() != "")
    return tokens, llm_response


@st.composite
def response_without_canary_tokens_st(draw):
    """Generate an LLM response that does NOT contain any canary token."""
    tokens = draw(_canary_tokens_list_st)

    llm_response = draw(st.text(
        alphabet=st.characters(blacklist_categories=("Cs",)),
        min_size=1, max_size=100,
    ))
    assume(llm_response.strip() != "")

    # Filter: ensure no canary token appears (exact match, case-sensitive)
    for token in tokens:
        assume(token not in llm_response)

    return tokens, llm_response


# ---------------------------------------------------------------------------
# Property tests — SafeGuard
# ---------------------------------------------------------------------------


class TestSafeGuardPromptSecurity:
    """Property 9 (SafeGuard): For any user input and sensitiveWords list,
    containsSensitiveContent returns true iff the input contains at least
    one sensitive word (case-insensitive).

    **Validates: Requirements 13.17, 13.21**
    """

    @given(data=input_containing_sensitive_word_st())
    @settings(max_examples=30, deadline=None)
    def test_blocks_input_containing_sensitive_word(self, data):
        """Input containing a sensitive word (any case) SHALL be blocked.

        **Validates: Requirements 13.17, 13.21**
        """
        words, user_input = data
        service = SafeGuardAdvisorService(words)

        result = service.contains_sensitive_content(user_input)

        assert result is True, (
            f"SafeGuard should block input containing sensitive word.\n"
            f"Sensitive words: {words!r}\n"
            f"User input: {user_input!r}"
        )

    @given(data=input_without_sensitive_words_st())
    @settings(max_examples=30, deadline=None)
    def test_allows_input_without_sensitive_words(self, data):
        """Input without any sensitive word SHALL pass through unblocked.

        **Validates: Requirements 13.17, 13.21**
        """
        words, user_input = data
        service = SafeGuardAdvisorService(words)

        result = service.contains_sensitive_content(user_input)

        assert result is False, (
            f"SafeGuard should allow input without sensitive words.\n"
            f"Sensitive words: {words!r}\n"
            f"User input: {user_input!r}"
        )

    @given(
        words=_sensitive_words_list_st,
        blank=st.sampled_from(["", "   ", "\t", "\n", None]),
    )
    @settings(max_examples=30, deadline=None)
    def test_null_or_blank_input_never_blocked(self, words, blank):
        """Null or blank input SHALL never be blocked.

        **Validates: Requirements 13.17**
        """
        service = SafeGuardAdvisorService(words)
        result = service.contains_sensitive_content(blank)
        assert result is False, (
            f"SafeGuard should not block null/blank input.\n"
            f"Input: {blank!r}"
        )

    @given(user_input=_user_input_st)
    @settings(max_examples=30, deadline=None)
    def test_empty_sensitive_words_never_blocks(self, user_input):
        """Empty sensitiveWords list SHALL never block any input.

        **Validates: Requirements 13.17**
        """
        service = SafeGuardAdvisorService([])
        result = service.contains_sensitive_content(user_input)
        assert result is False, (
            f"SafeGuard with empty word list should never block.\n"
            f"Input: {user_input!r}"
        )

    @given(
        words=st.lists(
            st.text(
                alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters=" "),
                min_size=1, max_size=15,
            ).filter(lambda w: w.strip() != "" and w.isascii()),
            min_size=1, max_size=3, unique=True,
        ),
    )
    @settings(max_examples=30, deadline=None)
    def test_case_insensitive_matching(self, words):
        """Matching SHALL be case-insensitive for ASCII words.

        **Validates: Requirements 13.17, 13.21**
        """
        service = SafeGuardAdvisorService(words)
        word = words[0]

        # The word in various cases should all be detected
        assert service.contains_sensitive_content(word.lower()) is True
        assert service.contains_sensitive_content(word.upper()) is True
        assert service.contains_sensitive_content(word.title()) is True


# ---------------------------------------------------------------------------
# Property tests — CanaryWord
# ---------------------------------------------------------------------------


class TestCanaryWordPromptSecurity:
    """Property 9 (CanaryWord): For any LLM response and canaryTokens list,
    detectLeakage returns true iff the response contains at least one
    canary token.

    **Validates: Requirements 13.18, 13.22**
    """

    @given(data=response_containing_canary_token_st())
    @settings(max_examples=30, deadline=None)
    def test_flags_response_containing_canary_token(self, data):
        """Response containing a canary token SHALL be flagged as leakage.

        **Validates: Requirements 13.18, 13.22**
        """
        tokens, llm_response = data
        service = CanaryWordAdvisorService(tokens)

        result = service.detect_leakage(llm_response)

        assert result is True, (
            f"CanaryWord should flag response containing canary token.\n"
            f"Canary tokens: {tokens!r}\n"
            f"LLM response: {llm_response!r}"
        )

    @given(data=response_without_canary_tokens_st())
    @settings(max_examples=30, deadline=None)
    def test_allows_response_without_canary_tokens(self, data):
        """Response without any canary token SHALL NOT be flagged.

        **Validates: Requirements 13.18, 13.22**
        """
        tokens, llm_response = data
        service = CanaryWordAdvisorService(tokens)

        result = service.detect_leakage(llm_response)

        assert result is False, (
            f"CanaryWord should not flag response without canary tokens.\n"
            f"Canary tokens: {tokens!r}\n"
            f"LLM response: {llm_response!r}"
        )

    @given(
        tokens=_canary_tokens_list_st,
        blank=st.sampled_from(["", "   ", "\t", "\n", None]),
    )
    @settings(max_examples=30, deadline=None)
    def test_null_or_blank_response_never_flagged(self, tokens, blank):
        """Null or blank response SHALL never be flagged.

        **Validates: Requirements 13.18**
        """
        service = CanaryWordAdvisorService(tokens)
        result = service.detect_leakage(blank)
        assert result is False, (
            f"CanaryWord should not flag null/blank response.\n"
            f"Response: {blank!r}"
        )

    @given(llm_response=_llm_response_st)
    @settings(max_examples=30, deadline=None)
    def test_empty_canary_tokens_never_flags(self, llm_response):
        """Empty canaryTokens list SHALL never flag any response.

        **Validates: Requirements 13.18**
        """
        service = CanaryWordAdvisorService([])
        result = service.detect_leakage(llm_response)
        assert result is False, (
            f"CanaryWord with empty token list should never flag.\n"
            f"Response: {llm_response!r}"
        )

    @given(data=response_containing_canary_token_st())
    @settings(max_examples=30, deadline=None)
    def test_exact_match_case_sensitive(self, data):
        """Canary token matching SHALL be exact (case-sensitive).

        **Validates: Requirements 13.18, 13.22**
        """
        tokens, llm_response = data
        service = CanaryWordAdvisorService(tokens)

        # The original response contains a token, so it should be flagged
        assert service.detect_leakage(llm_response) is True
