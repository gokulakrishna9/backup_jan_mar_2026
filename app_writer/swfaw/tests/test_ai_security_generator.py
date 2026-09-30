"""Unit tests for the AI SecurityGenerator.

Verifies that the SecurityGenerator produces correct Java source files
for SafeGuardAdvisorService, CanaryWordAdvisorService,
InputSanitizationService, OutputFilteringService, ModerationService,
and related DTOs.

Requirements: 13.17–13.28, 14.1–14.8
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_security_generator import (
    SecurityGenerator,
    VALID_FAILURE_ACTIONS,
    DEFAULT_MODERATION_CATEGORIES,
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
    return SecurityGenerator(jinja_env)


@pytest.fixture
def output_dirs():
    return {
        "orchestrator": Path("com/example/app/ai/orchestrator"),
        "dto": Path("com/example/app/ai/dto"),
    }


# --- Orchestrator fixtures ---

@pytest.fixture
def orchestrator_no_security():
    """Orchestrator with no promptSecurity or moderation."""
    return {"providerName": "mainGpt"}


@pytest.fixture
def orchestrator_safeguard_only():
    """Orchestrator with only SafeGuard enabled."""
    return {
        "providerName": "mainGpt",
        "promptSecurity": {
            "safeGuardAdvisor": {
                "enabled": True,
                "sensitiveWords": ["password", "secret key"],
            },
        },
    }


@pytest.fixture
def orchestrator_canary_only():
    """Orchestrator with only CanaryWord enabled."""
    return {
        "providerName": "mainGpt",
        "promptSecurity": {
            "canaryWordAdvisor": {
                "enabled": True,
                "canaryTokens": ["CANARY-abc123", "CANARY-def456"],
            },
        },
    }


@pytest.fixture
def orchestrator_canary_auto_tokens():
    """Orchestrator with CanaryWord enabled but empty tokens (auto-generate)."""
    return {
        "providerName": "mainGpt",
        "promptSecurity": {
            "canaryWordAdvisor": {
                "enabled": True,
                "canaryTokens": [],
            },
        },
    }


@pytest.fixture
def orchestrator_input_sanitization():
    """Orchestrator with input sanitization enabled."""
    return {
        "providerName": "mainGpt",
        "promptSecurity": {
            "inputSanitization": {
                "enabled": True,
                "rules": [
                    {"pattern": "<script.*?>.*?</script>", "replacement": ""},
                    {"pattern": "\\\\bignore\\\\b", "replacement": "", "caseInsensitive": True},
                ],
            },
        },
    }


@pytest.fixture
def orchestrator_output_filtering():
    """Orchestrator with output filtering enabled."""
    return {
        "providerName": "mainGpt",
        "promptSecurity": {
            "outputFiltering": {
                "enabled": True,
                "rules": [
                    {"pattern": "\\\\b\\\\d{3}-\\\\d{2}-\\\\d{4}\\\\b", "replacement": "[REDACTED-SSN]"},
                ],
            },
        },
    }


@pytest.fixture
def orchestrator_moderation_only():
    """Orchestrator with only moderation enabled."""
    return {
        "providerName": "mainGpt",
        "moderation": {
            "enabled": True,
            "providerName": "moderationGpt",
            "categories": ["hate", "violence", "sexual"],
            "preModeration": True,
            "postModeration": True,
            "failureAction": "block",
        },
    }


@pytest.fixture
def orchestrator_moderation_warn():
    """Orchestrator with moderation using warn failure action."""
    return {
        "providerName": "mainGpt",
        "moderation": {
            "enabled": True,
            "providerName": "moderationGpt",
            "categories": ["hate", "violence"],
            "preModeration": True,
            "postModeration": False,
            "failureAction": "warn",
        },
    }


@pytest.fixture
def orchestrator_moderation_log():
    """Orchestrator with moderation using log failure action."""
    return {
        "providerName": "mainGpt",
        "moderation": {
            "enabled": True,
            "providerName": "moderationGpt",
            "categories": ["hate"],
            "preModeration": False,
            "postModeration": True,
            "failureAction": "log",
        },
    }


@pytest.fixture
def orchestrator_full_security():
    """Orchestrator with all security features enabled."""
    return {
        "providerName": "mainGpt",
        "promptSecurity": {
            "safeGuardAdvisor": {
                "enabled": True,
                "sensitiveWords": ["password", "secret"],
            },
            "canaryWordAdvisor": {
                "enabled": True,
                "canaryTokens": ["CANARY-xyz"],
            },
            "inputSanitization": {
                "enabled": True,
                "rules": [{"pattern": "<script>", "replacement": ""}],
            },
            "outputFiltering": {
                "enabled": True,
                "rules": [{"pattern": "SSN:\\\\d+", "replacement": "[REDACTED]"}],
            },
        },
        "moderation": {
            "enabled": True,
            "providerName": "moderationGpt",
            "categories": ["hate", "violence", "sexual", "self_harm"],
            "preModeration": True,
            "postModeration": True,
            "failureAction": "block",
        },
    }


BASE_PACKAGE = "com.example.app"


# ======================================================================
# Test: generate() — skip logic and file counts
# ======================================================================

class TestSecurityGeneratorGenerate:
    """Tests for the generate() method's skip logic and file counts."""

    def test_no_files_when_orchestrator_is_none(self, generator, output_dirs):
        results = generator.generate(None, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_no_files_when_orchestrator_is_empty_dict(self, generator, output_dirs):
        results = generator.generate({}, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_no_files_when_no_security_configured(
        self, generator, orchestrator_no_security, output_dirs
    ):
        results = generator.generate(orchestrator_no_security, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_safeguard_only_generates_2_files(
        self, generator, orchestrator_safeguard_only, output_dirs
    ):
        """SafeGuardAdvisorService + PromptSecurityViolationDTO."""
        results = generator.generate(orchestrator_safeguard_only, BASE_PACKAGE, output_dirs)
        assert len(results) == 2

    def test_canary_only_generates_2_files(
        self, generator, orchestrator_canary_only, output_dirs
    ):
        """CanaryWordAdvisorService + PromptSecurityViolationDTO."""
        results = generator.generate(orchestrator_canary_only, BASE_PACKAGE, output_dirs)
        assert len(results) == 2

    def test_input_sanitization_generates_1_file(
        self, generator, orchestrator_input_sanitization, output_dirs
    ):
        """InputSanitizationService only (no violation DTO needed)."""
        results = generator.generate(orchestrator_input_sanitization, BASE_PACKAGE, output_dirs)
        assert len(results) == 1

    def test_output_filtering_generates_1_file(
        self, generator, orchestrator_output_filtering, output_dirs
    ):
        """OutputFilteringService only."""
        results = generator.generate(orchestrator_output_filtering, BASE_PACKAGE, output_dirs)
        assert len(results) == 1

    def test_moderation_only_generates_3_files(
        self, generator, orchestrator_moderation_only, output_dirs
    ):
        """ModerationService + ModerationResultDTO + ModerationErrorResponseDTO."""
        results = generator.generate(orchestrator_moderation_only, BASE_PACKAGE, output_dirs)
        assert len(results) == 3

    def test_full_security_generates_all_files(
        self, generator, orchestrator_full_security, output_dirs
    ):
        """All 4 advisors + violation DTO + moderation service + 2 moderation DTOs = 8."""
        results = generator.generate(orchestrator_full_security, BASE_PACKAGE, output_dirs)
        assert len(results) == 8

    def test_all_content_is_nonempty(
        self, generator, orchestrator_full_security, output_dirs
    ):
        results = generator.generate(orchestrator_full_security, BASE_PACKAGE, output_dirs)
        for filepath, content in results:
            assert content.strip(), f"Empty content for {filepath}"

    def test_output_dirs_used_in_paths(
        self, generator, orchestrator_safeguard_only, output_dirs
    ):
        results = generator.generate(orchestrator_safeguard_only, BASE_PACKAGE, output_dirs)
        for filepath, _ in results:
            assert "com/example/app/ai/" in filepath

    def test_moderation_disabled_generates_no_moderation_files(
        self, generator, output_dirs
    ):
        """Moderation present but enabled=false should not generate moderation files."""
        orch = {
            "providerName": "mainGpt",
            "moderation": {
                "enabled": False,
                "providerName": "moderationGpt",
            },
        }
        results = generator.generate(orch, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_correct_filenames_safeguard(
        self, generator, orchestrator_safeguard_only, output_dirs
    ):
        results = generator.generate(orchestrator_safeguard_only, BASE_PACKAGE, output_dirs)
        filenames = [Path(fp).name for fp, _ in results]
        assert "SafeGuardAdvisorService.java" in filenames
        assert "PromptSecurityViolationDTO.java" in filenames

    def test_correct_filenames_moderation(
        self, generator, orchestrator_moderation_only, output_dirs
    ):
        results = generator.generate(orchestrator_moderation_only, BASE_PACKAGE, output_dirs)
        filenames = [Path(fp).name for fp, _ in results]
        assert "ModerationService.java" in filenames
        assert "ModerationResultDTO.java" in filenames
        assert "ModerationErrorResponseDTO.java" in filenames


# ======================================================================
# Test: SafeGuardAdvisorService template content
# ======================================================================

class TestSafeGuardAdvisorService:
    """Tests for the generated SafeGuardAdvisorService Java source."""

    def _get_service(self, generator, orchestrator, output_dirs):
        results = generator.generate(orchestrator, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "SafeGuardAdvisorService.java" in fp:
                return content
        pytest.fail("SafeGuardAdvisorService.java not found in results")

    def test_package_declaration(self, generator, orchestrator_safeguard_only, output_dirs):
        content = self._get_service(generator, orchestrator_safeguard_only, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.orchestrator;" in content

    def test_service_annotation(self, generator, orchestrator_safeguard_only, output_dirs):
        content = self._get_service(generator, orchestrator_safeguard_only, output_dirs)
        assert "@Service" in content

    def test_class_name(self, generator, orchestrator_safeguard_only, output_dirs):
        content = self._get_service(generator, orchestrator_safeguard_only, output_dirs)
        assert "class SafeGuardAdvisorService" in content

    def test_sensitive_words_present(self, generator, orchestrator_safeguard_only, output_dirs):
        content = self._get_service(generator, orchestrator_safeguard_only, output_dirs)
        assert '"password"' in content
        assert '"secret key"' in content

    def test_contains_sensitive_content_method(self, generator, orchestrator_safeguard_only, output_dirs):
        content = self._get_service(generator, orchestrator_safeguard_only, output_dirs)
        assert "containsSensitiveContent" in content

    def test_validate_method(self, generator, orchestrator_safeguard_only, output_dirs):
        content = self._get_service(generator, orchestrator_safeguard_only, output_dirs)
        assert "public Mono<String> validate" in content

    def test_rejection_response(self, generator, orchestrator_safeguard_only, output_dirs):
        content = self._get_service(generator, orchestrator_safeguard_only, output_dirs)
        assert "REJECTION_RESPONSE" in content

    def test_reactive_imports(self, generator, orchestrator_safeguard_only, output_dirs):
        content = self._get_service(generator, orchestrator_safeguard_only, output_dirs)
        assert "import reactor.core.publisher.Mono;" in content

    def test_logging(self, generator, orchestrator_safeguard_only, output_dirs):
        content = self._get_service(generator, orchestrator_safeguard_only, output_dirs)
        assert "@Slf4j" in content
        assert "log.warn" in content


# ======================================================================
# Test: CanaryWordAdvisorService template content
# ======================================================================

class TestCanaryWordAdvisorService:
    """Tests for the generated CanaryWordAdvisorService Java source."""

    def _get_service(self, generator, orchestrator, output_dirs):
        results = generator.generate(orchestrator, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "CanaryWordAdvisorService.java" in fp:
                return content
        pytest.fail("CanaryWordAdvisorService.java not found in results")

    def test_package_declaration(self, generator, orchestrator_canary_only, output_dirs):
        content = self._get_service(generator, orchestrator_canary_only, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.orchestrator;" in content

    def test_service_annotation(self, generator, orchestrator_canary_only, output_dirs):
        content = self._get_service(generator, orchestrator_canary_only, output_dirs)
        assert "@Service" in content

    def test_class_name(self, generator, orchestrator_canary_only, output_dirs):
        content = self._get_service(generator, orchestrator_canary_only, output_dirs)
        assert "class CanaryWordAdvisorService" in content

    def test_canary_tokens_present(self, generator, orchestrator_canary_only, output_dirs):
        content = self._get_service(generator, orchestrator_canary_only, output_dirs)
        assert '"CANARY-abc123"' in content
        assert '"CANARY-def456"' in content

    def test_auto_generated_tokens_when_empty(
        self, generator, orchestrator_canary_auto_tokens, output_dirs
    ):
        content = self._get_service(generator, orchestrator_canary_auto_tokens, output_dirs)
        assert "UUID.randomUUID()" in content

    def test_inject_canary_tokens_method(self, generator, orchestrator_canary_only, output_dirs):
        content = self._get_service(generator, orchestrator_canary_only, output_dirs)
        assert "injectCanaryTokens" in content

    def test_detect_leakage_method(self, generator, orchestrator_canary_only, output_dirs):
        content = self._get_service(generator, orchestrator_canary_only, output_dirs)
        assert "detectLeakage" in content

    def test_validate_method(self, generator, orchestrator_canary_only, output_dirs):
        content = self._get_service(generator, orchestrator_canary_only, output_dirs)
        assert "public Mono<String> validate" in content

    def test_reactive_imports(self, generator, orchestrator_canary_only, output_dirs):
        content = self._get_service(generator, orchestrator_canary_only, output_dirs)
        assert "import reactor.core.publisher.Mono;" in content

    def test_logging(self, generator, orchestrator_canary_only, output_dirs):
        content = self._get_service(generator, orchestrator_canary_only, output_dirs)
        assert "@Slf4j" in content
        assert "log.warn" in content


# ======================================================================
# Test: InputSanitizationService template content
# ======================================================================

class TestInputSanitizationService:
    """Tests for the generated InputSanitizationService Java source."""

    def _get_service(self, generator, orchestrator, output_dirs):
        results = generator.generate(orchestrator, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "InputSanitizationService.java" in fp:
                return content
        pytest.fail("InputSanitizationService.java not found in results")

    def test_package_declaration(self, generator, orchestrator_input_sanitization, output_dirs):
        content = self._get_service(generator, orchestrator_input_sanitization, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.orchestrator;" in content

    def test_service_annotation(self, generator, orchestrator_input_sanitization, output_dirs):
        content = self._get_service(generator, orchestrator_input_sanitization, output_dirs)
        assert "@Service" in content

    def test_class_name(self, generator, orchestrator_input_sanitization, output_dirs):
        content = self._get_service(generator, orchestrator_input_sanitization, output_dirs)
        assert "class InputSanitizationService" in content

    def test_sanitize_method(self, generator, orchestrator_input_sanitization, output_dirs):
        content = self._get_service(generator, orchestrator_input_sanitization, output_dirs)
        assert "public String sanitize" in content

    def test_sanitize_reactive_method(self, generator, orchestrator_input_sanitization, output_dirs):
        content = self._get_service(generator, orchestrator_input_sanitization, output_dirs)
        assert "public Mono<String> sanitizeReactive" in content

    def test_pattern_compiled(self, generator, orchestrator_input_sanitization, output_dirs):
        content = self._get_service(generator, orchestrator_input_sanitization, output_dirs)
        assert "Pattern.compile" in content

    def test_rules_applied(self, generator, orchestrator_input_sanitization, output_dirs):
        content = self._get_service(generator, orchestrator_input_sanitization, output_dirs)
        assert "RULE_1_PATTERN" in content
        assert "RULE_2_PATTERN" in content

    def test_case_insensitive_flag(self, generator, orchestrator_input_sanitization, output_dirs):
        content = self._get_service(generator, orchestrator_input_sanitization, output_dirs)
        assert "Pattern.CASE_INSENSITIVE" in content


# ======================================================================
# Test: OutputFilteringService template content
# ======================================================================

class TestOutputFilteringService:
    """Tests for the generated OutputFilteringService Java source."""

    def _get_service(self, generator, orchestrator, output_dirs):
        results = generator.generate(orchestrator, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "OutputFilteringService.java" in fp:
                return content
        pytest.fail("OutputFilteringService.java not found in results")

    def test_package_declaration(self, generator, orchestrator_output_filtering, output_dirs):
        content = self._get_service(generator, orchestrator_output_filtering, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.orchestrator;" in content

    def test_service_annotation(self, generator, orchestrator_output_filtering, output_dirs):
        content = self._get_service(generator, orchestrator_output_filtering, output_dirs)
        assert "@Service" in content

    def test_class_name(self, generator, orchestrator_output_filtering, output_dirs):
        content = self._get_service(generator, orchestrator_output_filtering, output_dirs)
        assert "class OutputFilteringService" in content

    def test_filter_method(self, generator, orchestrator_output_filtering, output_dirs):
        content = self._get_service(generator, orchestrator_output_filtering, output_dirs)
        assert "public String filter" in content

    def test_filter_reactive_method(self, generator, orchestrator_output_filtering, output_dirs):
        content = self._get_service(generator, orchestrator_output_filtering, output_dirs)
        assert "public Mono<String> filterReactive" in content

    def test_pattern_compiled(self, generator, orchestrator_output_filtering, output_dirs):
        content = self._get_service(generator, orchestrator_output_filtering, output_dirs)
        assert "Pattern.compile" in content

    def test_redacted_replacement(self, generator, orchestrator_output_filtering, output_dirs):
        content = self._get_service(generator, orchestrator_output_filtering, output_dirs)
        assert "[REDACTED-SSN]" in content


# ======================================================================
# Test: ModerationService template content
# ======================================================================

class TestModerationService:
    """Tests for the generated ModerationService Java source."""

    def _get_service(self, generator, orchestrator, output_dirs):
        results = generator.generate(orchestrator, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "ModerationService.java" in fp:
                return content
        pytest.fail("ModerationService.java not found in results")

    def test_package_declaration(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.orchestrator;" in content

    def test_service_annotation(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert "@Service" in content

    def test_class_name(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert "class ModerationService" in content

    def test_chat_client_qualifier(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert '@Qualifier("moderationGpt")' in content

    def test_categories_present(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert '"hate"' in content
        assert '"violence"' in content
        assert '"sexual"' in content

    def test_pre_moderation_enabled(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert "PRE_MODERATION_ENABLED = true" in content

    def test_post_moderation_enabled(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert "POST_MODERATION_ENABLED = true" in content

    def test_failure_action_block(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert 'FAILURE_ACTION = "block"' in content

    def test_failure_action_warn(self, generator, orchestrator_moderation_warn, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_warn, output_dirs)
        assert 'FAILURE_ACTION = "warn"' in content

    def test_failure_action_log(self, generator, orchestrator_moderation_log, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_log, output_dirs)
        assert 'FAILURE_ACTION = "log"' in content

    def test_pre_moderation_disabled(self, generator, orchestrator_moderation_log, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_log, output_dirs)
        assert "PRE_MODERATION_ENABLED = false" in content

    def test_post_moderation_disabled(self, generator, orchestrator_moderation_warn, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_warn, output_dirs)
        assert "POST_MODERATION_ENABLED = false" in content

    def test_moderate_method(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert "public Mono<ModerationResultDTO> moderate" in content

    def test_is_pre_moderation_enabled_method(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert "isPreModerationEnabled" in content

    def test_is_post_moderation_enabled_method(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert "isPostModerationEnabled" in content

    def test_get_failure_action_method(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert "getFailureAction" in content

    def test_get_categories_method(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert "getCategories" in content

    def test_imports_moderation_result_dto(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert "import com.example.app.ai.dto.ModerationResultDTO;" in content

    def test_reactive_imports(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert "import reactor.core.publisher.Mono;" in content

    def test_logging(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert "@Slf4j" in content

    def test_error_handling(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert "onErrorResume" in content

    def test_switch_on_failure_action(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_service(generator, orchestrator_moderation_only, output_dirs)
        assert '"block"' in content
        assert '"warn"' in content
        assert '"log"' in content


# ======================================================================
# Test: DTO template content
# ======================================================================

class TestPromptSecurityViolationDTO:
    """Tests for the generated PromptSecurityViolationDTO."""

    def _get_dto(self, generator, orchestrator, output_dirs):
        results = generator.generate(orchestrator, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "PromptSecurityViolationDTO.java" in fp:
                return content
        pytest.fail("PromptSecurityViolationDTO.java not found in results")

    def test_is_record(self, generator, orchestrator_safeguard_only, output_dirs):
        content = self._get_dto(generator, orchestrator_safeguard_only, output_dirs)
        assert "public record PromptSecurityViolationDTO" in content

    def test_package_declaration(self, generator, orchestrator_safeguard_only, output_dirs):
        content = self._get_dto(generator, orchestrator_safeguard_only, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.dto;" in content

    def test_has_violation_type(self, generator, orchestrator_safeguard_only, output_dirs):
        content = self._get_dto(generator, orchestrator_safeguard_only, output_dirs)
        assert "violationType" in content

    def test_has_message(self, generator, orchestrator_safeguard_only, output_dirs):
        content = self._get_dto(generator, orchestrator_safeguard_only, output_dirs)
        assert "String message" in content

    def test_has_timestamp(self, generator, orchestrator_safeguard_only, output_dirs):
        content = self._get_dto(generator, orchestrator_safeguard_only, output_dirs)
        assert "Instant timestamp" in content


class TestModerationResultDTO:
    """Tests for the generated ModerationResultDTO."""

    def _get_dto(self, generator, orchestrator, output_dirs):
        results = generator.generate(orchestrator, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "ModerationResultDTO.java" in fp:
                return content
        pytest.fail("ModerationResultDTO.java not found in results")

    def test_is_record(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_dto(generator, orchestrator_moderation_only, output_dirs)
        assert "public record ModerationResultDTO" in content

    def test_package_declaration(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_dto(generator, orchestrator_moderation_only, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.dto;" in content

    def test_has_flagged(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_dto(generator, orchestrator_moderation_only, output_dirs)
        assert "boolean flagged" in content

    def test_has_categories(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_dto(generator, orchestrator_moderation_only, output_dirs)
        assert "Map<String, Boolean> categories" in content

    def test_has_category_scores(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_dto(generator, orchestrator_moderation_only, output_dirs)
        assert "Map<String, Double> categoryScores" in content

    def test_has_action(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_dto(generator, orchestrator_moderation_only, output_dirs)
        assert "String action" in content


class TestModerationErrorResponseDTO:
    """Tests for the generated ModerationErrorResponseDTO."""

    def _get_dto(self, generator, orchestrator, output_dirs):
        results = generator.generate(orchestrator, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "ModerationErrorResponseDTO.java" in fp:
                return content
        pytest.fail("ModerationErrorResponseDTO.java not found in results")

    def test_is_record(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_dto(generator, orchestrator_moderation_only, output_dirs)
        assert "public record ModerationErrorResponseDTO" in content

    def test_package_declaration(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_dto(generator, orchestrator_moderation_only, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.dto;" in content

    def test_has_error_code(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_dto(generator, orchestrator_moderation_only, output_dirs)
        assert "errorCode" in content

    def test_has_message(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_dto(generator, orchestrator_moderation_only, output_dirs)
        assert "String message" in content

    def test_has_flagged_categories(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_dto(generator, orchestrator_moderation_only, output_dirs)
        assert "flaggedCategories" in content

    def test_has_action(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_dto(generator, orchestrator_moderation_only, output_dirs)
        assert "String action" in content

    def test_has_timestamp(self, generator, orchestrator_moderation_only, output_dirs):
        content = self._get_dto(generator, orchestrator_moderation_only, output_dirs)
        assert "Instant timestamp" in content


# ======================================================================
# Test: _build_moderation_context
# ======================================================================

class TestBuildModerationContext:
    """Tests for the _build_moderation_context helper."""

    def test_provider_name(self, generator):
        mod = {"providerName": "modGpt", "enabled": True}
        ctx = generator._build_moderation_context(mod, BASE_PACKAGE)
        assert ctx["provider_name"] == "modGpt"

    def test_default_categories(self, generator):
        mod = {"enabled": True}
        ctx = generator._build_moderation_context(mod, BASE_PACKAGE)
        assert ctx["categories"] == DEFAULT_MODERATION_CATEGORIES

    def test_custom_categories(self, generator):
        mod = {"enabled": True, "categories": ["hate", "violence"]}
        ctx = generator._build_moderation_context(mod, BASE_PACKAGE)
        assert ctx["categories"] == ["hate", "violence"]

    def test_default_pre_moderation(self, generator):
        mod = {"enabled": True}
        ctx = generator._build_moderation_context(mod, BASE_PACKAGE)
        assert ctx["pre_moderation"] is True

    def test_default_post_moderation(self, generator):
        mod = {"enabled": True}
        ctx = generator._build_moderation_context(mod, BASE_PACKAGE)
        assert ctx["post_moderation"] is True

    def test_default_failure_action(self, generator):
        mod = {"enabled": True}
        ctx = generator._build_moderation_context(mod, BASE_PACKAGE)
        assert ctx["failure_action"] == "block"

    def test_custom_failure_action(self, generator):
        mod = {"enabled": True, "failureAction": "warn"}
        ctx = generator._build_moderation_context(mod, BASE_PACKAGE)
        assert ctx["failure_action"] == "warn"

    def test_pre_moderation_false(self, generator):
        mod = {"enabled": True, "preModeration": False}
        ctx = generator._build_moderation_context(mod, BASE_PACKAGE)
        assert ctx["pre_moderation"] is False

    def test_post_moderation_false(self, generator):
        mod = {"enabled": True, "postModeration": False}
        ctx = generator._build_moderation_context(mod, BASE_PACKAGE)
        assert ctx["post_moderation"] is False

    def test_base_package(self, generator):
        mod = {"enabled": True}
        ctx = generator._build_moderation_context(mod, "org.test.pkg")
        assert ctx["base_package"] == "org.test.pkg"


# ======================================================================
# Test: Module-level constants
# ======================================================================

class TestModuleConstants:
    """Tests for module-level constants."""

    def test_valid_failure_actions(self):
        assert VALID_FAILURE_ACTIONS == {"block", "warn", "log"}

    def test_default_moderation_categories(self):
        assert "hate" in DEFAULT_MODERATION_CATEGORIES
        assert "violence" in DEFAULT_MODERATION_CATEGORIES
        assert "sexual" in DEFAULT_MODERATION_CATEGORIES
        assert "self_harm" in DEFAULT_MODERATION_CATEGORIES
