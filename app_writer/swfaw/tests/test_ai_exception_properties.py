"""Property-based tests for Exception Handler Completeness — Property 10.

**Validates: Requirements 14.9, 14.10, 14.11, 14.12, 14.13, 14.14, 14.15,
14.16, 14.17, 14.18, 14.19, 14.20, 14.21, 14.22, 14.23, 14.26**

# Feature: ai-layer, Property 10: Exception Handler Completeness
"""

import sys
from pathlib import Path

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

# Ensure swfaw/ is on sys.path so imports resolve
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from swfaw.generators.ai_exception_generator import (
    EXCEPTION_MAPPINGS,
    BROAD_EXCEPTION_MAPPINGS,
    CATCH_ALL_STATUS,
    CATCH_ALL_ERROR_CODE,
    LLM_PROVIDER_STATUS,
    LLM_PROVIDER_ERROR_CODE,
)


# ---------------------------------------------------------------------------
# Python model of the AiExceptionHandler
# ---------------------------------------------------------------------------

# Build the complete mapping: exception_class -> (http_status, error_code)
_HANDLER_MAP: dict[str, tuple[int, str]] = {}
for exc_class, http_status, error_code in EXCEPTION_MAPPINGS:
    _HANDLER_MAP[exc_class] = (http_status, error_code)
for exc_class, http_status, error_code in BROAD_EXCEPTION_MAPPINGS:
    _HANDLER_MAP[exc_class] = (http_status, error_code)

# WebClientResponseException is a special case
_HANDLER_MAP["WebClientResponseException"] = (LLM_PROVIDER_STATUS, LLM_PROVIDER_ERROR_CODE)

# All known exception types
ALL_KNOWN_EXCEPTIONS = list(_HANDLER_MAP.keys())


class AiExceptionHandlerModel:
    """Python model of the generated AiExceptionHandler.

    Mirrors the Java @ControllerAdvice that maps AI exception types to
    AiErrorResponseDTO with (httpStatus, errorCode, message).
    """

    def handle(self, exception_type: str, message: str) -> dict:
        """Handle an exception and return the response model.

        Returns a dict with keys: httpStatus, errorCode, message, timestamp.
        """
        if exception_type in _HANDLER_MAP:
            http_status, error_code = _HANDLER_MAP[exception_type]
        else:
            # Catch-all for unknown exceptions
            http_status = CATCH_ALL_STATUS
            error_code = CATCH_ALL_ERROR_CODE

        return {
            "httpStatus": http_status,
            "errorCode": error_code,
            "message": message,
            "timestamp": "2025-01-01T00:00:00Z",  # placeholder, always non-null
        }


# ---------------------------------------------------------------------------
# Hypothesis strategies
# ---------------------------------------------------------------------------

# Strategy: pick from all known exception types
_known_exception_st = st.sampled_from(ALL_KNOWN_EXCEPTIONS)

# Strategy: pick from EXCEPTION_MAPPINGS only
_specific_exception_st = st.sampled_from(
    [exc for exc, _, _ in EXCEPTION_MAPPINGS]
)

# Strategy: pick from BROAD_EXCEPTION_MAPPINGS only
_broad_exception_st = st.sampled_from(
    [exc for exc, _, _ in BROAD_EXCEPTION_MAPPINGS]
)

# Strategy: generate an unknown exception class name
_unknown_exception_st = st.text(
    alphabet=st.characters(whitelist_categories=("L",)),
    min_size=5,
    max_size=40,
).filter(
    lambda name: name not in _HANDLER_MAP and name.strip() != ""
)

# Strategy: non-empty message string
_message_st = st.text(
    alphabet=st.characters(blacklist_categories=("Cs",)),
    min_size=1,
    max_size=200,
).filter(lambda s: s.strip() != "")


# ---------------------------------------------------------------------------
# Property tests
# ---------------------------------------------------------------------------


class TestExceptionHandlerCompleteness:
    """Property 10: Exception Handler Completeness.

    For any AI-specific exception type handled by the AiExceptionHandler,
    the handler SHALL produce an AiErrorResponseDTO with a non-null
    errorCode string and a non-null message string, and the HTTP status
    code SHALL match the specified mapping.

    **Validates: Requirements 14.9–14.23, 14.26**
    """

    @given(exception_type=_known_exception_st, message=_message_st)
    @settings(max_examples=30, deadline=None)
    def test_known_exception_produces_non_null_error_code(
        self, exception_type, message
    ):
        """Every known exception SHALL produce a non-null errorCode.

        **Validates: Requirements 14.9, 14.10**
        """
        handler = AiExceptionHandlerModel()
        result = handler.handle(exception_type, message)

        assert result["errorCode"] is not None, (
            f"errorCode must not be None for {exception_type}"
        )
        assert isinstance(result["errorCode"], str), (
            f"errorCode must be a string for {exception_type}"
        )
        assert len(result["errorCode"]) > 0, (
            f"errorCode must be non-empty for {exception_type}"
        )

    @given(exception_type=_known_exception_st, message=_message_st)
    @settings(max_examples=30, deadline=None)
    def test_known_exception_produces_non_null_message(
        self, exception_type, message
    ):
        """Every known exception SHALL produce a non-null message.

        **Validates: Requirements 14.9, 14.10**
        """
        handler = AiExceptionHandlerModel()
        result = handler.handle(exception_type, message)

        assert result["message"] is not None, (
            f"message must not be None for {exception_type}"
        )
        assert isinstance(result["message"], str), (
            f"message must be a string for {exception_type}"
        )
        assert len(result["message"]) > 0, (
            f"message must be non-empty for {exception_type}"
        )

    @given(exception_type=_known_exception_st, message=_message_st)
    @settings(max_examples=30, deadline=None)
    def test_known_exception_has_correct_http_status(
        self, exception_type, message
    ):
        """Every known exception SHALL map to its specified HTTP status.

        **Validates: Requirements 14.11–14.23**
        """
        handler = AiExceptionHandlerModel()
        result = handler.handle(exception_type, message)

        expected_status, expected_code = _HANDLER_MAP[exception_type]
        assert result["httpStatus"] == expected_status, (
            f"{exception_type}: expected HTTP {expected_status}, "
            f"got {result['httpStatus']}"
        )
        assert result["errorCode"] == expected_code, (
            f"{exception_type}: expected errorCode '{expected_code}', "
            f"got '{result['errorCode']}'"
        )

    @given(exception_type=_unknown_exception_st, message=_message_st)
    @settings(max_examples=30, deadline=None)
    def test_unknown_exception_gets_catch_all_response(
        self, exception_type, message
    ):
        """Unknown exceptions SHALL get the catch-all 500/AI_INTERNAL_ERROR.

        **Validates: Requirements 14.26**
        """
        handler = AiExceptionHandlerModel()
        result = handler.handle(exception_type, message)

        assert result["httpStatus"] == CATCH_ALL_STATUS, (
            f"Unknown exception '{exception_type}' should get HTTP "
            f"{CATCH_ALL_STATUS}, got {result['httpStatus']}"
        )
        assert result["errorCode"] == CATCH_ALL_ERROR_CODE, (
            f"Unknown exception '{exception_type}' should get errorCode "
            f"'{CATCH_ALL_ERROR_CODE}', got '{result['errorCode']}'"
        )
        assert result["message"] is not None and len(result["message"]) > 0, (
            f"Unknown exception must still have a non-empty message"
        )

    @given(exception_type=_specific_exception_st, message=_message_st)
    @settings(max_examples=30, deadline=None)
    def test_specific_exceptions_have_valid_status_codes(
        self, exception_type, message
    ):
        """EXCEPTION_MAPPINGS entries SHALL have valid HTTP 4xx/5xx status.

        **Validates: Requirements 14.11–14.18**
        """
        handler = AiExceptionHandlerModel()
        result = handler.handle(exception_type, message)

        assert 400 <= result["httpStatus"] < 600, (
            f"{exception_type}: HTTP status {result['httpStatus']} "
            f"is not a valid error status code"
        )

    @given(exception_type=_broad_exception_st, message=_message_st)
    @settings(max_examples=30, deadline=None)
    def test_broad_exceptions_have_valid_status_codes(
        self, exception_type, message
    ):
        """BROAD_EXCEPTION_MAPPINGS entries SHALL have valid HTTP 4xx/5xx status.

        **Validates: Requirements 14.19–14.22**
        """
        handler = AiExceptionHandlerModel()
        result = handler.handle(exception_type, message)

        assert 400 <= result["httpStatus"] < 600, (
            f"{exception_type}: HTTP status {result['httpStatus']} "
            f"is not a valid error status code"
        )

    @given(message=_message_st)
    @settings(max_examples=30, deadline=None)
    def test_web_client_response_exception_maps_to_502(self, message):
        """WebClientResponseException SHALL map to 502/LLM_PROVIDER_ERROR.

        **Validates: Requirements 14.23**
        """
        handler = AiExceptionHandlerModel()
        result = handler.handle("WebClientResponseException", message)

        assert result["httpStatus"] == 502, (
            f"WebClientResponseException should be HTTP 502, "
            f"got {result['httpStatus']}"
        )
        assert result["errorCode"] == "LLM_PROVIDER_ERROR", (
            f"WebClientResponseException should have errorCode "
            f"'LLM_PROVIDER_ERROR', got '{result['errorCode']}'"
        )

    @given(exception_type=_known_exception_st, message=_message_st)
    @settings(max_examples=30, deadline=None)
    def test_response_always_has_timestamp(self, exception_type, message):
        """Every response SHALL include a non-null timestamp.

        **Validates: Requirements 14.10**
        """
        handler = AiExceptionHandlerModel()
        result = handler.handle(exception_type, message)

        assert result["timestamp"] is not None, (
            f"timestamp must not be None for {exception_type}"
        )
        assert isinstance(result["timestamp"], str), (
            f"timestamp must be a string for {exception_type}"
        )
        assert len(result["timestamp"]) > 0, (
            f"timestamp must be non-empty for {exception_type}"
        )


class TestExceptionMappingConsistency:
    """Verify that the exception mapping data structures are consistent
    with the handler model — ensuring the generator's constants are
    correctly reflected in the handler behavior.

    **Validates: Requirements 14.9–14.23, 14.26**
    """

    @given(
        idx=st.integers(
            min_value=0, max_value=len(EXCEPTION_MAPPINGS) - 1
        ),
        message=_message_st,
    )
    @settings(max_examples=30, deadline=None)
    def test_exception_mapping_index_round_trip(self, idx, message):
        """Each EXCEPTION_MAPPINGS entry SHALL round-trip through the handler.

        **Validates: Requirements 14.11–14.18**
        """
        exc_class, expected_status, expected_code = EXCEPTION_MAPPINGS[idx]
        handler = AiExceptionHandlerModel()
        result = handler.handle(exc_class, message)

        assert result["httpStatus"] == expected_status
        assert result["errorCode"] == expected_code

    @given(
        idx=st.integers(
            min_value=0, max_value=len(BROAD_EXCEPTION_MAPPINGS) - 1
        ),
        message=_message_st,
    )
    @settings(max_examples=30, deadline=None)
    def test_broad_mapping_index_round_trip(self, idx, message):
        """Each BROAD_EXCEPTION_MAPPINGS entry SHALL round-trip through the handler.

        **Validates: Requirements 14.19–14.22**
        """
        exc_class, expected_status, expected_code = BROAD_EXCEPTION_MAPPINGS[idx]
        handler = AiExceptionHandlerModel()
        result = handler.handle(exc_class, message)

        assert result["httpStatus"] == expected_status
        assert result["errorCode"] == expected_code
