"""Unit tests for the AI TokenBudgetGenerator.

Verifies that the TokenBudgetGenerator produces correct Java source files
for TokenBudgetService, TokenBudgetController, and token budget DTOs
(TokenUsageDTO, TokenUsageSummaryDTO, TokenBudgetExceededResponseDTO).

Requirements: 15.17–15.33
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_token_budget_generator import (
    TokenBudgetGenerator,
    DEFAULT_ENFORCEMENT_ACTION,
    DEFAULT_WARNING_THRESHOLD_PERCENT,
    VALID_ENFORCEMENT_ACTIONS,
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
    return TokenBudgetGenerator(jinja_env)


@pytest.fixture
def output_dirs():
    return {
        "budget": Path("com/example/app/ai/budget"),
        "controller": Path("com/example/app/ai/controller"),
        "dto": Path("com/example/app/ai/dto"),
    }


# --- Token budget fixtures ---

@pytest.fixture
def budget_disabled():
    """Token budget with enabled=false."""
    return {"enabled": False}


@pytest.fixture
def budget_none():
    """Token budget is None."""
    return None


@pytest.fixture
def budget_minimal():
    """Token budget enabled with defaults only."""
    return {"enabled": True}


@pytest.fixture
def budget_with_daily_limit():
    """Token budget with daily limit."""
    return {
        "enabled": True,
        "defaultDailyLimitPerUser": 100000,
    }


@pytest.fixture
def budget_with_monthly_limit():
    """Token budget with monthly limit."""
    return {
        "enabled": True,
        "defaultMonthlyLimitPerUser": 2000000,
    }


@pytest.fixture
def budget_with_provider_overrides():
    """Token budget with provider-specific overrides."""
    return {
        "enabled": True,
        "defaultDailyLimitPerUser": 100000,
        "defaultMonthlyLimitPerUser": 2000000,
        "providerOverrides": {
            "openaiPrimary": {"dailyLimit": 50000, "monthlyLimit": 1000000},
            "ollamaLocal": {"dailyLimit": 200000, "monthlyLimit": 5000000},
        },
    }


@pytest.fixture
def budget_full():
    """Full token budget configuration."""
    return {
        "enabled": True,
        "defaultDailyLimitPerUser": 100000,
        "defaultMonthlyLimitPerUser": 2000000,
        "providerOverrides": {
            "openaiPrimary": {"dailyLimit": 50000, "monthlyLimit": 1000000},
        },
        "warningThresholdPercent": 75,
        "enforcementAction": "warn",
    }


@pytest.fixture
def budget_log_enforcement():
    """Token budget with log enforcement action."""
    return {
        "enabled": True,
        "defaultDailyLimitPerUser": 100000,
        "enforcementAction": "log",
    }


@pytest.fixture
def budget_tracking_only():
    """Token budget enabled but no limits (tracking-only mode)."""
    return {
        "enabled": True,
        "warningThresholdPercent": 90,
        "enforcementAction": "block",
    }


# =====================================================================
# Test: generate() — file count and conditional generation
# =====================================================================

class TestTokenBudgetGeneratorGenerate:
    """Tests for the generate() method output."""

    def test_no_files_when_budget_is_none(self, generator, output_dirs):
        """Req 15.29: No files when tokenBudget is None."""
        assert generator.generate(None, "com.example.app", output_dirs) == []

    def test_no_files_when_budget_disabled(self, generator, budget_disabled, output_dirs):
        """Req 15.29: No files when tokenBudget.enabled is false."""
        assert generator.generate(budget_disabled, "com.example.app", output_dirs) == []

    def test_no_files_when_empty_dict(self, generator, output_dirs):
        """Req 15.29: No files when tokenBudget is empty dict."""
        assert generator.generate({}, "com.example.app", output_dirs) == []

    def test_minimal_generates_5_files(self, generator, budget_minimal, output_dirs):
        """Minimal config generates service + controller + 3 DTOs = 5 files."""
        results = generator.generate(budget_minimal, "com.example.app", output_dirs)
        assert len(results) == 5

    def test_full_config_generates_5_files(self, generator, budget_full, output_dirs):
        """Full config also generates exactly 5 files."""
        results = generator.generate(budget_full, "com.example.app", output_dirs)
        assert len(results) == 5

    def test_all_content_is_nonempty(self, generator, budget_full, output_dirs):
        """All generated files have non-empty content."""
        results = generator.generate(budget_full, "com.example.app", output_dirs)
        for filepath, content in results:
            assert content.strip(), f"Empty content for {filepath}"

    def test_output_dirs_used_in_paths(self, generator, budget_full, output_dirs):
        """Output directory paths are used in generated file paths."""
        results = generator.generate(budget_full, "com.example.app", output_dirs)
        paths = [fp for fp, _ in results]
        assert any("com/example/app/ai/budget" in p for p in paths)
        assert any("com/example/app/ai/controller" in p for p in paths)
        assert any("com/example/app/ai/dto" in p for p in paths)

    def test_correct_filenames(self, generator, budget_full, output_dirs):
        """Correct Java class filenames are generated."""
        results = generator.generate(budget_full, "com.example.app", output_dirs)
        filenames = [Path(fp).name for fp, _ in results]
        assert "TokenBudgetService.java" in filenames
        assert "TokenBudgetController.java" in filenames
        assert "TokenUsageDTO.java" in filenames
        assert "TokenUsageSummaryDTO.java" in filenames
        assert "TokenBudgetExceededResponseDTO.java" in filenames


# =====================================================================
# Test: TokenBudgetService template output
# =====================================================================

class TestTokenBudgetService:
    """Tests for the generated TokenBudgetService Java class."""

    def _get_service(self, generator, token_budget, output_dirs):
        results = generator.generate(token_budget, "com.example.app", output_dirs)
        for fp, content in results:
            if "TokenBudgetService.java" in fp:
                return content
        pytest.fail("TokenBudgetService.java not found in results")

    def test_package_declaration(self, generator, budget_minimal, output_dirs):
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert "package com.example.app.ai.budget;" in content

    def test_service_annotation(self, generator, budget_minimal, output_dirs):
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert "@Service" in content

    def test_class_name(self, generator, budget_minimal, output_dirs):
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert "class TokenBudgetService" in content

    def test_repository_injection(self, generator, budget_minimal, output_dirs):
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert "AiTokenUsageRepository" in content

    def test_enforcement_action_property(self, generator, budget_minimal, output_dirs):
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert "ai.token-budget.enforcement-action" in content

    def test_warning_threshold_property(self, generator, budget_minimal, output_dirs):
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert "ai.token-budget.warning-threshold-percent" in content

    def test_check_budget_method(self, generator, budget_minimal, output_dirs):
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert "checkBudget" in content

    def test_record_usage_method(self, generator, budget_minimal, output_dirs):
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert "recordUsage" in content

    def test_get_daily_usage_method(self, generator, budget_minimal, output_dirs):
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert "getDailyUsage" in content

    def test_get_monthly_usage_method(self, generator, budget_minimal, output_dirs):
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert "getMonthlyUsage" in content

    def test_reactive_mono_import(self, generator, budget_minimal, output_dirs):
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert "import reactor.core.publisher.Mono;" in content

    def test_token_budget_exceeded_exception_import(self, generator, budget_minimal, output_dirs):
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert "TokenBudgetExceededException" in content

    def test_block_enforcement_handling(self, generator, budget_minimal, output_dirs):
        """Req 15.20: block enforcement throws TokenBudgetExceededException."""
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert 'case "block"' in content
        assert "Mono.error(new TokenBudgetExceededException" in content

    def test_warn_enforcement_handling(self, generator, budget_minimal, output_dirs):
        """Req 15.21: warn enforcement allows but flags budgetWarning."""
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert 'case "warn"' in content
        assert "budgetWarning" in content

    def test_log_enforcement_handling(self, generator, budget_minimal, output_dirs):
        """Req 15.22: log enforcement allows and logs at WARN level."""
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert 'case "log"' in content
        assert "log.warn" in content

    def test_warning_threshold_check(self, generator, budget_minimal, output_dirs):
        """Req 15.23: Warning emitted at warningThresholdPercent."""
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert "warningThresholdPercent" in content

    def test_daily_limit_with_value(self, generator, budget_with_daily_limit, output_dirs):
        """Daily limit value appears in generated code."""
        content = self._get_service(generator, budget_with_daily_limit, output_dirs)
        assert "100000" in content

    def test_monthly_limit_with_value(self, generator, budget_with_monthly_limit, output_dirs):
        """Monthly limit value appears in generated code."""
        content = self._get_service(generator, budget_with_monthly_limit, output_dirs)
        assert "2000000" in content

    def test_provider_overrides_in_service(self, generator, budget_with_provider_overrides, output_dirs):
        """Provider override values appear in generated code."""
        content = self._get_service(generator, budget_with_provider_overrides, output_dirs)
        assert "openaiPrimary" in content
        assert "ollamaLocal" in content
        assert "50000" in content
        assert "200000" in content

    def test_tracking_only_mode(self, generator, budget_tracking_only, output_dirs):
        """Req 15.32: Tracking-only mode when no limits configured."""
        content = self._get_service(generator, budget_tracking_only, output_dirs)
        # Default daily/monthly limit should be 0 (no enforcement)
        assert "default-daily-limit-per-user:0" in content

    def test_non_blocking_usage_recording(self, generator, budget_minimal, output_dirs):
        """Req 15.31: Usage recording is non-blocking (returns Mono)."""
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert "public Mono<Void> recordUsage" in content

    def test_logging_annotation(self, generator, budget_minimal, output_dirs):
        content = self._get_service(generator, budget_minimal, output_dirs)
        assert "@Slf4j" in content


# =====================================================================
# Test: TokenBudgetController template output
# =====================================================================

class TestTokenBudgetController:
    """Tests for the generated TokenBudgetController Java class."""

    def _get_controller(self, generator, token_budget, output_dirs):
        results = generator.generate(token_budget, "com.example.app", output_dirs)
        for fp, content in results:
            if "TokenBudgetController.java" in fp:
                return content
        pytest.fail("TokenBudgetController.java not found in results")

    def test_package_declaration(self, generator, budget_minimal, output_dirs):
        content = self._get_controller(generator, budget_minimal, output_dirs)
        assert "package com.example.app.ai.controller;" in content

    def test_rest_controller_annotation(self, generator, budget_minimal, output_dirs):
        content = self._get_controller(generator, budget_minimal, output_dirs)
        assert "@RestController" in content

    def test_request_mapping(self, generator, budget_minimal, output_dirs):
        """Req 15.25: Base path /api/ai/budget."""
        content = self._get_controller(generator, budget_minimal, output_dirs)
        assert '@RequestMapping("/api/ai/budget")' in content

    def test_class_name(self, generator, budget_minimal, output_dirs):
        content = self._get_controller(generator, budget_minimal, output_dirs)
        assert "class TokenBudgetController" in content

    def test_usage_endpoint(self, generator, budget_minimal, output_dirs):
        """Req 15.25: GET /usage endpoint."""
        content = self._get_controller(generator, budget_minimal, output_dirs)
        assert '@GetMapping("/usage")' in content

    def test_usage_summary_endpoint(self, generator, budget_minimal, output_dirs):
        """Req 15.25: GET /usage/summary endpoint."""
        content = self._get_controller(generator, budget_minimal, output_dirs)
        assert '@GetMapping("/usage/summary")' in content

    def test_admin_usage_endpoint(self, generator, budget_minimal, output_dirs):
        """Req 15.25: GET /admin/usage admin-only endpoint."""
        content = self._get_controller(generator, budget_minimal, output_dirs)
        assert '@GetMapping("/admin/usage")' in content

    def test_admin_role_required(self, generator, budget_minimal, output_dirs):
        """Req 15.25: Admin endpoint requires ADMIN role."""
        content = self._get_controller(generator, budget_minimal, output_dirs)
        assert "hasRole('ADMIN')" in content

    def test_reactive_imports(self, generator, budget_minimal, output_dirs):
        content = self._get_controller(generator, budget_minimal, output_dirs)
        assert "import reactor.core.publisher.Flux;" in content
        assert "import reactor.core.publisher.Mono;" in content

    def test_token_usage_dto_import(self, generator, budget_minimal, output_dirs):
        content = self._get_controller(generator, budget_minimal, output_dirs)
        assert "TokenUsageDTO" in content

    def test_token_usage_summary_dto_import(self, generator, budget_minimal, output_dirs):
        content = self._get_controller(generator, budget_minimal, output_dirs)
        assert "TokenUsageSummaryDTO" in content

    def test_authentication_principal(self, generator, budget_minimal, output_dirs):
        """Req 15.25: Endpoints require JWT auth."""
        content = self._get_controller(generator, budget_minimal, output_dirs)
        assert "@AuthenticationPrincipal" in content


# =====================================================================
# Test: DTO template outputs
# =====================================================================

class TestTokenUsageDTO:
    """Tests for the generated TokenUsageDTO Java class."""

    def _get_dto(self, generator, token_budget, output_dirs):
        results = generator.generate(token_budget, "com.example.app", output_dirs)
        for fp, content in results:
            if fp.endswith("TokenUsageDTO.java"):
                return content
        pytest.fail("TokenUsageDTO.java not found in results")

    def test_package_declaration(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "package com.example.app.ai.dto;" in content

    def test_data_annotation(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "@Data" in content

    def test_builder_annotation(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "@Builder" in content

    def test_class_name(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "class TokenUsageDTO" in content

    def test_user_id_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "userId" in content

    def test_provider_name_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "providerName" in content

    def test_daily_usage_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "dailyUsage" in content

    def test_monthly_usage_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "monthlyUsage" in content

    def test_daily_limit_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "dailyLimit" in content

    def test_monthly_limit_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "monthlyLimit" in content

    def test_daily_percent_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "dailyPercent" in content

    def test_monthly_percent_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "monthlyPercent" in content


class TestTokenUsageSummaryDTO:
    """Tests for the generated TokenUsageSummaryDTO Java class."""

    def _get_dto(self, generator, token_budget, output_dirs):
        results = generator.generate(token_budget, "com.example.app", output_dirs)
        for fp, content in results:
            if "TokenUsageSummaryDTO.java" in fp:
                return content
        pytest.fail("TokenUsageSummaryDTO.java not found in results")

    def test_package_declaration(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "package com.example.app.ai.dto;" in content

    def test_class_name(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "class TokenUsageSummaryDTO" in content

    def test_providers_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "List<TokenUsageDTO> providers" in content

    def test_total_daily_usage_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "totalDailyUsage" in content

    def test_total_monthly_usage_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "totalMonthlyUsage" in content

    def test_warnings_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "List<String> warnings" in content


class TestTokenBudgetExceededResponseDTO:
    """Tests for the generated TokenBudgetExceededResponseDTO Java class."""

    def _get_dto(self, generator, token_budget, output_dirs):
        results = generator.generate(token_budget, "com.example.app", output_dirs)
        for fp, content in results:
            if "TokenBudgetExceededResponseDTO.java" in fp:
                return content
        pytest.fail("TokenBudgetExceededResponseDTO.java not found in results")

    def test_package_declaration(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "package com.example.app.ai.dto;" in content

    def test_class_name(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "class TokenBudgetExceededResponseDTO" in content

    def test_provider_name_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "providerName" in content

    def test_current_usage_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "currentUsage" in content

    def test_limit_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "long limit" in content

    def test_period_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "period" in content

    def test_message_field(self, generator, budget_minimal, output_dirs):
        content = self._get_dto(generator, budget_minimal, output_dirs)
        assert "message" in content


# =====================================================================
# Test: _build_context
# =====================================================================

class TestBuildContext:
    """Tests for the _build_context method."""

    def test_defaults_when_minimal(self, generator):
        ctx = generator._build_context({"enabled": True}, "com.example.app")
        assert ctx["base_package"] == "com.example.app"
        assert ctx["default_daily_limit"] is None
        assert ctx["default_monthly_limit"] is None
        assert ctx["provider_overrides"] == {}
        assert ctx["warning_threshold_percent"] == 80
        assert ctx["enforcement_action"] == "block"

    def test_custom_values(self, generator):
        budget = {
            "enabled": True,
            "defaultDailyLimitPerUser": 50000,
            "defaultMonthlyLimitPerUser": 1000000,
            "providerOverrides": {
                "gpt4": {"dailyLimit": 10000, "monthlyLimit": 200000},
            },
            "warningThresholdPercent": 90,
            "enforcementAction": "warn",
        }
        ctx = generator._build_context(budget, "com.test.pkg")
        assert ctx["base_package"] == "com.test.pkg"
        assert ctx["default_daily_limit"] == 50000
        assert ctx["default_monthly_limit"] == 1000000
        assert "gpt4" in ctx["provider_overrides"]
        assert ctx["provider_overrides"]["gpt4"]["dailyLimit"] == 10000
        assert ctx["warning_threshold_percent"] == 90
        assert ctx["enforcement_action"] == "warn"

    def test_null_provider_overrides_becomes_empty_dict(self, generator):
        budget = {"enabled": True, "providerOverrides": None}
        ctx = generator._build_context(budget, "com.example.app")
        assert ctx["provider_overrides"] == {}


# =====================================================================
# Test: Module constants
# =====================================================================

class TestModuleConstants:
    """Tests for module-level constants."""

    def test_default_enforcement_action(self):
        assert DEFAULT_ENFORCEMENT_ACTION == "block"

    def test_default_warning_threshold_percent(self):
        assert DEFAULT_WARNING_THRESHOLD_PERCENT == 80

    def test_valid_enforcement_actions(self):
        assert VALID_ENFORCEMENT_ACTIONS == {"block", "warn", "log"}
