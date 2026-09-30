"""Unit tests for the AI ExceptionGenerator.

Verifies that the ExceptionGenerator produces correct Java source files
for AiExceptionHandler, AiErrorResponseDTO, and additional exception
classes (PromptSecurityViolationException, ModerationException,
TokenBudgetExceededException, etc.).

Requirements: 14.9–14.26
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_exception_generator import (
    ExceptionGenerator,
    EXCEPTION_MAPPINGS,
    BROAD_EXCEPTION_MAPPINGS,
    CATCH_ALL_STATUS,
    CATCH_ALL_ERROR_CODE,
    LLM_PROVIDER_STATUS,
    LLM_PROVIDER_ERROR_CODE,
)


@pytest.fixture
def jinja_env():
    """Create a Jinja2 environment pointing at the swfaw/templates directory."""
    templates_dir = Path(__file__).resolve().parent.parent / "templates"
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(templates_dir)),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )


@pytest.fixture
def generator(jinja_env):
    return ExceptionGenerator(jinja_env)


@pytest.fixture
def output_dirs():
    return {
        "controller": Path("com/example/app/ai/controller"),
        "dto": Path("com/example/app/ai/dto"),
        "provider": Path("com/example/app/ai/provider"),
    }


BASE_PACKAGE = "com.example.app"


# --- AI Layer fixtures ---

@pytest.fixture
def minimal_ai_layer():
    """Minimal AI layer with just providers — no optional features."""
    return {
        "schemaVersion": "1.0",
        "providers": [
            {"name": "gpt4", "type": "openai", "model": "gpt-4",
             "apiKeyEnvVar": "OPENAI_KEY"},
        ],
        "entityCapabilities": [],
        "standaloneOperations": [],
        "promptTemplates": [],
        "assistants": [],
        "ragSources": [],
        "evaluators": [],
        "vectorStore": None,
        "documentIngestion": None,
        "documentProcessing": None,
        "orchestrator": None,
        "mcpServers": [],
        "observability": None,
        "rateLimiting": None,
        "tokenBudget": None,
        "chatSessionCleanup": None,
        "auditLog": None,
    }


@pytest.fixture
def full_ai_layer():
    """AI layer with all optional features enabled."""
    return {
        "schemaVersion": "1.0",
        "providers": [
            {"name": "gpt4", "type": "openai", "model": "gpt-4",
             "apiKeyEnvVar": "OPENAI_KEY"},
        ],
        "entityCapabilities": [],
        "standaloneOperations": [],
        "promptTemplates": [],
        "assistants": [],
        "ragSources": [],
        "evaluators": [],
        "vectorStore": {"type": "milvus", "host": "localhost", "port": 19530},
        "documentIngestion": {"enabled": True, "allowedMimeTypes": ["application/pdf"]},
        "documentProcessing": {"enabled": True, "tasks": []},
        "orchestrator": {
            "providerName": "gpt4",
            "promptSecurity": {
                "safeGuardAdvisor": {"enabled": True, "sensitiveWords": ["secret"]},
            },
            "moderation": {"enabled": True, "providerName": "gpt4", "categories": ["hate"]},
        },
        "mcpServers": [{"name": "test-mcp", "transportType": "stdio", "enabled": True}],
        "observability": None,
        "rateLimiting": {"defaultRpm": 20},
        "tokenBudget": {"enabled": True, "defaultDailyLimitPerUser": 10000},
        "chatSessionCleanup": None,
        "auditLog": None,
    }


# =====================================================================
# Test: generate() method
# =====================================================================

class TestExceptionGeneratorGenerate:
    """Tests for the generate() method output structure."""

    def test_generates_three_core_files_plus_exceptions(
        self, generator, minimal_ai_layer, output_dirs
    ):
        """Should generate handler, DTO, and 7 exception classes = 9 files."""
        results = generator.generate(minimal_ai_layer, BASE_PACKAGE, output_dirs)
        assert len(results) == 9

    def test_first_file_is_exception_handler(
        self, generator, minimal_ai_layer, output_dirs
    ):
        results = generator.generate(minimal_ai_layer, BASE_PACKAGE, output_dirs)
        filepath, _ = results[0]
        assert filepath.endswith("AiExceptionHandler.java")

    def test_second_file_is_error_response_dto(
        self, generator, minimal_ai_layer, output_dirs
    ):
        results = generator.generate(minimal_ai_layer, BASE_PACKAGE, output_dirs)
        filepath, _ = results[1]
        assert filepath.endswith("AiErrorResponseDTO.java")

    def test_exception_class_files_generated(
        self, generator, minimal_ai_layer, output_dirs
    ):
        results = generator.generate(minimal_ai_layer, BASE_PACKAGE, output_dirs)
        filenames = [Path(fp).name for fp, _ in results]
        assert "PromptSecurityViolationException.java" in filenames
        assert "ModerationException.java" in filenames
        assert "TokenBudgetExceededException.java" in filenames
        assert "RateLimitExceededException.java" in filenames
        assert "InvalidDocumentTypeException.java" in filenames
        assert "DocumentTooLargeException.java" in filenames
        assert "McpServerException.java" in filenames

    def test_all_content_is_nonempty(
        self, generator, minimal_ai_layer, output_dirs
    ):
        results = generator.generate(minimal_ai_layer, BASE_PACKAGE, output_dirs)
        for filepath, content in results:
            assert content.strip(), f"Empty content for {filepath}"

    def test_output_dirs_used_in_paths(
        self, generator, minimal_ai_layer, output_dirs
    ):
        results = generator.generate(minimal_ai_layer, BASE_PACKAGE, output_dirs)
        handler_path = results[0][0]
        dto_path = results[1][0]
        assert "com/example/app/ai/controller" in handler_path
        assert "com/example/app/ai/dto" in dto_path

    def test_exception_classes_in_provider_dir(
        self, generator, minimal_ai_layer, output_dirs
    ):
        results = generator.generate(minimal_ai_layer, BASE_PACKAGE, output_dirs)
        # Exception classes start at index 2
        for filepath, _ in results[2:]:
            assert "com/example/app/ai/provider" in filepath


# =====================================================================
# Test: AiExceptionHandler template output
# =====================================================================

class TestAiExceptionHandler:
    """Tests for the generated AiExceptionHandler Java class."""

    def _get_handler(self, generator, ai_layer, output_dirs):
        results = generator.generate(ai_layer, BASE_PACKAGE, output_dirs)
        return results[0][1]

    def test_package_declaration(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.controller;" in content

    def test_controller_advice_annotation(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert f'@ControllerAdvice(basePackages = "{BASE_PACKAGE}.ai")' in content

    def test_class_name(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "public class AiExceptionHandler" in content

    def test_returns_ai_error_response_dto(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "ResponseEntity<AiErrorResponseDTO>" in content

    def test_imports_ai_error_response_dto(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert f"import {BASE_PACKAGE}.ai.dto.AiErrorResponseDTO;" in content

    def test_handler_for_unsupported_role(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "@ExceptionHandler(UnsupportedRoleException.class)" in content
        assert "UNSUPPORTED_ROLE" in content

    def test_handler_for_unsupported_parameter(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "@ExceptionHandler(UnsupportedParameterException.class)" in content
        assert "UNSUPPORTED_PARAMETER" in content

    def test_handler_for_deserialization_error(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "@ExceptionHandler(TypedResponseDeserializationException.class)" in content
        assert "LLM_RESPONSE_PARSE_ERROR" in content

    def test_handler_for_circuit_open(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "@ExceptionHandler(ProviderCircuitOpenException.class)" in content
        assert "PROVIDER_CIRCUIT_OPEN" in content

    def test_handler_for_prompt_security_violation(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "@ExceptionHandler(PromptSecurityViolationException.class)" in content
        assert "PROMPT_SECURITY_VIOLATION" in content

    def test_handler_for_moderation(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "@ExceptionHandler(ModerationException.class)" in content
        assert "CONTENT_MODERATION_BLOCKED" in content

    def test_handler_for_token_budget_exceeded(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "@ExceptionHandler(TokenBudgetExceededException.class)" in content
        assert "TOKEN_BUDGET_EXCEEDED" in content

    def test_handler_for_rate_limit_exceeded(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "@ExceptionHandler(RateLimitExceededException.class)" in content
        assert "RATE_LIMIT_EXCEEDED" in content
        assert "Retry-After" in content

    def test_handler_for_access_denied(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "@ExceptionHandler(AccessDeniedException.class)" in content
        assert "AI_ACCESS_DENIED" in content

    def test_handler_for_invalid_document_type(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "@ExceptionHandler(InvalidDocumentTypeException.class)" in content
        assert "INVALID_DOCUMENT_TYPE" in content

    def test_handler_for_document_too_large(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "@ExceptionHandler(DocumentTooLargeException.class)" in content
        assert "DOCUMENT_TOO_LARGE" in content

    def test_handler_for_mcp_server_error(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "@ExceptionHandler(McpServerException.class)" in content
        assert "MCP_SERVER_ERROR" in content

    def test_handler_for_llm_provider_error(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "@ExceptionHandler(WebClientResponseException.class)" in content
        assert "LLM_PROVIDER_ERROR" in content

    def test_catch_all_handler(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "@ExceptionHandler(Exception.class)" in content
        assert "AI_INTERNAL_ERROR" in content

    def test_logging_imports(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "import org.slf4j.Logger;" in content
        assert "import org.slf4j.LoggerFactory;" in content

    def test_timestamp_in_response(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "Instant.now().toString()" in content

    def test_build_response_helper(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_handler(generator, minimal_ai_layer, output_dirs)
        assert "private ResponseEntity<AiErrorResponseDTO> buildResponse(" in content


# =====================================================================
# Test: AiErrorResponseDTO template output
# =====================================================================

class TestAiErrorResponseDTO:
    """Tests for the generated AiErrorResponseDTO Java record."""

    def _get_dto(self, generator, ai_layer, output_dirs):
        results = generator.generate(ai_layer, BASE_PACKAGE, output_dirs)
        return results[1][1]

    def test_is_record(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_dto(generator, minimal_ai_layer, output_dirs)
        assert "public record AiErrorResponseDTO(" in content

    def test_package_declaration(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_dto(generator, minimal_ai_layer, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.dto;" in content

    def test_has_error_code_field(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_dto(generator, minimal_ai_layer, output_dirs)
        assert "String errorCode" in content

    def test_has_message_field(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_dto(generator, minimal_ai_layer, output_dirs)
        assert "String message" in content

    def test_has_details_field(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_dto(generator, minimal_ai_layer, output_dirs)
        assert "Map<String, Object> details" in content

    def test_has_timestamp_field(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_dto(generator, minimal_ai_layer, output_dirs)
        assert "String timestamp" in content

    def test_imports_map(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_dto(generator, minimal_ai_layer, output_dirs)
        assert "import java.util.Map;" in content


# =====================================================================
# Test: Exception classes
# =====================================================================

class TestPromptSecurityViolationException:
    """Tests for the generated PromptSecurityViolationException."""

    def _get_exception(self, generator, ai_layer, output_dirs):
        results = generator.generate(ai_layer, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "PromptSecurityViolationException.java" in fp:
                return content
        return None

    def test_package_declaration(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.provider;" in content

    def test_extends_runtime_exception(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "extends RuntimeException" in content

    def test_has_violation_type_field(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "violationType" in content

    def test_has_getter(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "getViolationType()" in content


class TestModerationException:
    """Tests for the generated ModerationException."""

    def _get_exception(self, generator, ai_layer, output_dirs):
        results = generator.generate(ai_layer, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if fp.endswith("ModerationException.java"):
                return content
        return None

    def test_package_declaration(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.provider;" in content

    def test_extends_runtime_exception(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "extends RuntimeException" in content

    def test_has_flagged_categories(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "flaggedCategories" in content

    def test_has_action_field(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "getAction()" in content

    def test_imports_list(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "import java.util.List;" in content


class TestTokenBudgetExceededException:
    """Tests for the generated TokenBudgetExceededException."""

    def _get_exception(self, generator, ai_layer, output_dirs):
        results = generator.generate(ai_layer, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "TokenBudgetExceededException.java" in fp:
                return content
        return None

    def test_package_declaration(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.provider;" in content

    def test_extends_runtime_exception(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "extends RuntimeException" in content

    def test_has_provider_name(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "providerName" in content

    def test_has_current_usage(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "currentUsage" in content

    def test_has_limit(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "getLimit()" in content

    def test_has_period(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "getPeriod()" in content


class TestRateLimitExceededException:
    """Tests for the generated RateLimitExceededException."""

    def _get_exception(self, generator, ai_layer, output_dirs):
        results = generator.generate(ai_layer, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "RateLimitExceededException.java" in fp:
                return content
        return None

    def test_package_declaration(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.provider;" in content

    def test_has_retry_after_seconds(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "retryAfterSeconds" in content


class TestInvalidDocumentTypeException:
    """Tests for the generated InvalidDocumentTypeException."""

    def _get_exception(self, generator, ai_layer, output_dirs):
        results = generator.generate(ai_layer, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "InvalidDocumentTypeException.java" in fp:
                return content
        return None

    def test_package_declaration(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.provider;" in content

    def test_has_mime_type(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "mimeType" in content


class TestDocumentTooLargeException:
    """Tests for the generated DocumentTooLargeException."""

    def _get_exception(self, generator, ai_layer, output_dirs):
        results = generator.generate(ai_layer, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "DocumentTooLargeException.java" in fp:
                return content
        return None

    def test_package_declaration(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.provider;" in content

    def test_has_file_size(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "fileSize" in content

    def test_has_max_size(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "maxSize" in content


class TestMcpServerException:
    """Tests for the generated McpServerException."""

    def _get_exception(self, generator, ai_layer, output_dirs):
        results = generator.generate(ai_layer, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "McpServerException.java" in fp:
                return content
        return None

    def test_package_declaration(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.provider;" in content

    def test_has_server_name(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "serverName" in content

    def test_has_cause_constructor(self, generator, minimal_ai_layer, output_dirs):
        content = self._get_exception(generator, minimal_ai_layer, output_dirs)
        assert "Throwable cause" in content


# =====================================================================
# Test: _build_context
# =====================================================================

class TestBuildContext:
    """Tests for the _build_context method."""

    def test_base_package(self, generator, minimal_ai_layer):
        ctx = generator._build_context(minimal_ai_layer, BASE_PACKAGE)
        assert ctx["base_package"] == BASE_PACKAGE

    def test_no_orchestrator(self, generator, minimal_ai_layer):
        ctx = generator._build_context(minimal_ai_layer, BASE_PACKAGE)
        assert ctx["has_orchestrator"] is False
        assert ctx["has_moderation"] is False
        assert ctx["has_prompt_security"] is False

    def test_with_orchestrator(self, generator, full_ai_layer):
        ctx = generator._build_context(full_ai_layer, BASE_PACKAGE)
        assert ctx["has_orchestrator"] is True
        assert ctx["has_moderation"] is True
        assert ctx["has_prompt_security"] is True

    def test_no_document_features(self, generator, minimal_ai_layer):
        ctx = generator._build_context(minimal_ai_layer, BASE_PACKAGE)
        assert ctx["has_document_ingestion"] is False
        assert ctx["has_document_processing"] is False

    def test_with_document_features(self, generator, full_ai_layer):
        ctx = generator._build_context(full_ai_layer, BASE_PACKAGE)
        assert ctx["has_document_ingestion"] is True
        assert ctx["has_document_processing"] is True

    def test_no_mcp(self, generator, minimal_ai_layer):
        ctx = generator._build_context(minimal_ai_layer, BASE_PACKAGE)
        assert ctx["has_mcp"] is False

    def test_with_mcp(self, generator, full_ai_layer):
        ctx = generator._build_context(full_ai_layer, BASE_PACKAGE)
        assert ctx["has_mcp"] is True

    def test_no_token_budget(self, generator, minimal_ai_layer):
        ctx = generator._build_context(minimal_ai_layer, BASE_PACKAGE)
        assert ctx["has_token_budget"] is False

    def test_with_token_budget(self, generator, full_ai_layer):
        ctx = generator._build_context(full_ai_layer, BASE_PACKAGE)
        assert ctx["has_token_budget"] is True

    def test_no_rate_limiting(self, generator, minimal_ai_layer):
        ctx = generator._build_context(minimal_ai_layer, BASE_PACKAGE)
        assert ctx["has_rate_limiting"] is False

    def test_with_rate_limiting(self, generator, full_ai_layer):
        ctx = generator._build_context(full_ai_layer, BASE_PACKAGE)
        assert ctx["has_rate_limiting"] is True

    def test_exception_mappings_present(self, generator, minimal_ai_layer):
        ctx = generator._build_context(minimal_ai_layer, BASE_PACKAGE)
        assert ctx["exception_mappings"] == EXCEPTION_MAPPINGS

    def test_broad_mappings_present(self, generator, minimal_ai_layer):
        ctx = generator._build_context(minimal_ai_layer, BASE_PACKAGE)
        assert ctx["broad_exception_mappings"] == BROAD_EXCEPTION_MAPPINGS

    def test_catch_all_values(self, generator, minimal_ai_layer):
        ctx = generator._build_context(minimal_ai_layer, BASE_PACKAGE)
        assert ctx["catch_all_status"] == 500
        assert ctx["catch_all_error_code"] == "AI_INTERNAL_ERROR"

    def test_llm_provider_values(self, generator, minimal_ai_layer):
        ctx = generator._build_context(minimal_ai_layer, BASE_PACKAGE)
        assert ctx["llm_provider_status"] == 502
        assert ctx["llm_provider_error_code"] == "LLM_PROVIDER_ERROR"


# =====================================================================
# Test: Module-level constants
# =====================================================================

class TestModuleConstants:
    """Tests for module-level constants."""

    def test_exception_mappings_count(self):
        assert len(EXCEPTION_MAPPINGS) == 8

    def test_broad_exception_mappings_count(self):
        assert len(BROAD_EXCEPTION_MAPPINGS) == 4

    def test_catch_all_status(self):
        assert CATCH_ALL_STATUS == 500

    def test_catch_all_error_code(self):
        assert CATCH_ALL_ERROR_CODE == "AI_INTERNAL_ERROR"

    def test_llm_provider_status(self):
        assert LLM_PROVIDER_STATUS == 502

    def test_llm_provider_error_code(self):
        assert LLM_PROVIDER_ERROR_CODE == "LLM_PROVIDER_ERROR"

    def test_unsupported_role_mapping(self):
        mapping = EXCEPTION_MAPPINGS[0]
        assert mapping == ("UnsupportedRoleException", 400, "UNSUPPORTED_ROLE")

    def test_unsupported_parameter_mapping(self):
        mapping = EXCEPTION_MAPPINGS[1]
        assert mapping == ("UnsupportedParameterException", 400, "UNSUPPORTED_PARAMETER")

    def test_deserialization_mapping(self):
        mapping = EXCEPTION_MAPPINGS[2]
        assert mapping == ("TypedResponseDeserializationException", 502, "LLM_RESPONSE_PARSE_ERROR")

    def test_circuit_open_mapping(self):
        mapping = EXCEPTION_MAPPINGS[3]
        assert mapping == ("ProviderCircuitOpenException", 503, "PROVIDER_CIRCUIT_OPEN")

    def test_prompt_security_mapping(self):
        mapping = EXCEPTION_MAPPINGS[4]
        assert mapping == ("PromptSecurityViolationException", 422, "PROMPT_SECURITY_VIOLATION")

    def test_moderation_mapping(self):
        mapping = EXCEPTION_MAPPINGS[5]
        assert mapping == ("ModerationException", 422, "CONTENT_MODERATION_BLOCKED")

    def test_token_budget_mapping(self):
        mapping = EXCEPTION_MAPPINGS[6]
        assert mapping == ("TokenBudgetExceededException", 429, "TOKEN_BUDGET_EXCEEDED")

    def test_rate_limit_mapping(self):
        mapping = EXCEPTION_MAPPINGS[7]
        assert mapping == ("RateLimitExceededException", 429, "RATE_LIMIT_EXCEEDED")

    def test_access_denied_broad_mapping(self):
        mapping = BROAD_EXCEPTION_MAPPINGS[0]
        assert mapping == ("AccessDeniedException", 403, "AI_ACCESS_DENIED")

    def test_invalid_document_broad_mapping(self):
        mapping = BROAD_EXCEPTION_MAPPINGS[1]
        assert mapping == ("InvalidDocumentTypeException", 400, "INVALID_DOCUMENT_TYPE")

    def test_document_too_large_broad_mapping(self):
        mapping = BROAD_EXCEPTION_MAPPINGS[2]
        assert mapping == ("DocumentTooLargeException", 413, "DOCUMENT_TOO_LARGE")

    def test_mcp_server_broad_mapping(self):
        mapping = BROAD_EXCEPTION_MAPPINGS[3]
        assert mapping == ("McpServerException", 502, "MCP_SERVER_ERROR")
