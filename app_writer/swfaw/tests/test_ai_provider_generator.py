"""Unit tests for the AI ProviderGenerator.

Verifies that the ProviderGenerator produces correct Java source files
for ChatClientConfig, ChatOptionsResolver, RoleValidationAdvisor,
ProviderResilienceConfig, and exception classes.
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_provider_generator import ProviderGenerator


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
    return ProviderGenerator(jinja_env)


@pytest.fixture
def single_openai_provider():
    return [
        {
            "name": "mainGpt",
            "type": "openai",
            "model": "gpt-4o",
            "embeddingModel": "text-embedding-3-small",
            "temperature": 0.7,
            "maxTokens": 2048,
            "apiKeyEnvVar": "OPENAI_API_KEY",
            "supportedRoles": ["system", "user", "assistant"],
            "supportedParameters": ["topP", "frequencyPenalty", "presencePenalty", "seed", "stop"],
            "parameterFallbacks": {"topK": "skip", "repeatPenalty": "error"},
            "roleFallbacks": {"tool": "merge_to_system"},
            "chatOptions": {"topP": 0.9},
            "resilience": {
                "retry": {"maxAttempts": 3, "backoffMs": 1000, "retryableStatuses": [429, 503], "retryOnTimeout": True},
                "circuitBreaker": {"failureRateThreshold": 50, "waitDurationMs": 30000, "slidingWindowSize": 10, "minimumNumberOfCalls": 5},
            },
        }
    ]


@pytest.fixture
def multi_providers():
    return [
        {
            "name": "gptProvider",
            "type": "openai",
            "model": "gpt-4o",
            "temperature": 0.5,
            "maxTokens": 4096,
            "apiKeyEnvVar": "OPENAI_API_KEY",
            "supportedRoles": ["system", "user", "assistant"],
            "supportedParameters": ["topP", "frequencyPenalty"],
            "parameterFallbacks": {},
            "roleFallbacks": {},
        },
        {
            "name": "localOllama",
            "type": "ollama",
            "model": "llama3",
            "temperature": 0.8,
            "maxTokens": 1024,
            "supportedRoles": ["system", "user", "assistant"],
            "supportedParameters": ["topP", "topK", "repeatPenalty", "numCtx"],
            "parameterFallbacks": {"seed": "skip"},
            "roleFallbacks": {"tool": "skip"},
        },
    ]


@pytest.fixture
def output_dirs():
    return {
        "config": Path("com/example/app/ai/config"),
        "provider": Path("com/example/app/ai/provider"),
    }


BASE_PACKAGE = "com.example.app"


class TestProviderGeneratorGenerate:
    """Tests for the generate() method."""

    def test_empty_providers_returns_empty(self, generator, output_dirs):
        result = generator.generate([], BASE_PACKAGE, output_dirs)
        assert result == []

    def test_single_openai_generates_all_files(self, generator, single_openai_provider, output_dirs):
        result = generator.generate(single_openai_provider, BASE_PACKAGE, output_dirs)
        filenames = [fp for fp, _ in result]

        # Should have: ChatClientConfig, ChatOptionsResolver, RoleValidationAdvisor,
        # ProviderResilienceConfig, + 4 exception classes = 8 files
        assert len(result) == 8
        assert any("ChatClientConfig.java" in f for f in filenames)
        assert any("ChatOptionsResolver.java" in f for f in filenames)
        assert any("RoleValidationAdvisor.java" in f for f in filenames)
        assert any("ProviderResilienceConfig.java" in f for f in filenames)
        assert any("UnsupportedRoleException.java" in f for f in filenames)
        assert any("UnsupportedParameterException.java" in f for f in filenames)
        assert any("TypedResponseDeserializationException.java" in f for f in filenames)
        assert any("ProviderCircuitOpenException.java" in f for f in filenames)

    def test_multi_providers_generates_all_files(self, generator, multi_providers, output_dirs):
        result = generator.generate(multi_providers, BASE_PACKAGE, output_dirs)
        filenames = [fp for fp, _ in result]
        assert len(result) == 8
        assert any("ChatClientConfig.java" in f for f in filenames)

    def test_all_content_is_nonempty(self, generator, single_openai_provider, output_dirs):
        result = generator.generate(single_openai_provider, BASE_PACKAGE, output_dirs)
        for filepath, content in result:
            assert content.strip(), f"Empty content for {filepath}"


class TestChatClientConfig:
    """Tests for the ChatClientConfig template rendering."""

    def test_single_openai_has_primary(self, generator, single_openai_provider):
        content = generator._render_chat_client_config(single_openai_provider, BASE_PACKAGE)
        assert "@Primary" in content
        assert "@Configuration" in content
        assert "OpenAiChatModel" in content
        assert "OpenAiEmbeddingModel" in content
        assert '@Qualifier("mainGpt")' in content

    def test_single_openai_package(self, generator, single_openai_provider):
        content = generator._render_chat_client_config(single_openai_provider, BASE_PACKAGE)
        assert "package com.example.app.ai.config;" in content

    def test_multi_providers_no_primary(self, generator, multi_providers):
        content = generator._render_chat_client_config(multi_providers, BASE_PACKAGE)
        assert "@Primary" not in content

    def test_multi_providers_both_types(self, generator, multi_providers):
        content = generator._render_chat_client_config(multi_providers, BASE_PACKAGE)
        assert "OpenAiChatModel" in content
        assert "OllamaChatModel" in content
        assert '@Qualifier("gptProvider")' in content
        assert '@Qualifier("localOllama")' in content

    def test_ollama_uses_ollama_models(self, generator):
        providers = [{"name": "local", "type": "ollama", "model": "llama3", "temperature": 0.7, "maxTokens": 2048}]
        content = generator._render_chat_client_config(providers, BASE_PACKAGE)
        assert "OllamaChatModel" in content
        assert "OllamaEmbeddingModel" in content
        assert "@Primary" in content  # single provider


class TestChatOptionsResolver:
    """Tests for the ChatOptionsResolver template rendering."""

    def test_contains_resolve_method(self, generator, single_openai_provider):
        content = generator._render_chat_options_resolver(single_openai_provider, BASE_PACKAGE)
        assert "public Map<String, Object> resolve(" in content

    def test_contains_provider_types(self, generator, multi_providers):
        content = generator._render_chat_options_resolver(multi_providers, BASE_PACKAGE)
        assert '"gptProvider", "openai"' in content
        assert '"localOllama", "ollama"' in content

    def test_parameter_fallbacks_rendered(self, generator, single_openai_provider):
        content = generator._render_chat_options_resolver(single_openai_provider, BASE_PACKAGE)
        assert '"topK", "skip"' in content
        assert '"repeatPenalty", "error"' in content

    def test_package_declaration(self, generator, single_openai_provider):
        content = generator._render_chat_options_resolver(single_openai_provider, BASE_PACKAGE)
        assert "package com.example.app.ai.provider;" in content


class TestRoleValidationAdvisor:
    """Tests for the RoleValidationAdvisor template rendering."""

    def test_contains_validate_method(self, generator, single_openai_provider):
        content = generator._render_role_validation_advisor(single_openai_provider, BASE_PACKAGE)
        assert "public List<Message> validate(" in content

    def test_role_fallbacks_rendered(self, generator, single_openai_provider):
        content = generator._render_role_validation_advisor(single_openai_provider, BASE_PACKAGE)
        assert '"tool", "merge_to_system"' in content

    def test_supported_roles_rendered(self, generator, single_openai_provider):
        content = generator._render_role_validation_advisor(single_openai_provider, BASE_PACKAGE)
        assert "system,user,assistant" in content


class TestResilienceConfig:
    """Tests for the ProviderResilienceConfig template rendering."""

    def test_contains_retry_bean(self, generator, single_openai_provider):
        content = generator._render_resilience_config(single_openai_provider, BASE_PACKAGE)
        assert "public Retry mainGptRetry()" in content
        assert "ai-retry-mainGpt" in content

    def test_contains_circuit_breaker_bean(self, generator, single_openai_provider):
        content = generator._render_resilience_config(single_openai_provider, BASE_PACKAGE)
        assert "public CircuitBreaker mainGptCircuitBreaker()" in content
        assert "ai-cb-mainGpt" in content

    def test_default_resilience_values(self, generator):
        """Provider without explicit resilience should get defaults."""
        providers = [{"name": "basic", "type": "openai", "model": "gpt-4o"}]
        content = generator._render_resilience_config(providers, BASE_PACKAGE)
        # Defaults: maxAttempts=3, backoffMs=1000, failureRateThreshold=50
        assert "max-attempts:3" in content
        assert "backoff-ms:1000" in content
        assert "failure-rate-threshold:50" in content

    def test_retry_logging(self, generator, single_openai_provider):
        content = generator._render_resilience_config(single_openai_provider, BASE_PACKAGE)
        assert "log.warn" in content
        assert "retry attempt" in content

    def test_circuit_breaker_open_logging(self, generator, single_openai_provider):
        content = generator._render_resilience_config(single_openai_provider, BASE_PACKAGE)
        assert "log.error" in content
        assert "circuit breaker OPEN" in content


class TestExceptionClasses:
    """Tests for the exception class generation."""

    def test_generates_four_exceptions(self, generator):
        result = generator._render_exception_classes(BASE_PACKAGE)
        filenames = [fn for fn, _ in result]
        assert len(result) == 4
        assert "UnsupportedRoleException.java" in filenames
        assert "UnsupportedParameterException.java" in filenames
        assert "TypedResponseDeserializationException.java" in filenames
        assert "ProviderCircuitOpenException.java" in filenames

    def test_unsupported_role_exception_fields(self, generator):
        result = generator._render_exception_classes(BASE_PACKAGE)
        content = dict(result)["UnsupportedRoleException.java"]
        assert "providerName" in content
        assert "unsupportedRole" in content
        assert "supportedRoles" in content
        assert "package com.example.app.ai.provider;" in content

    def test_unsupported_parameter_exception_fields(self, generator):
        result = generator._render_exception_classes(BASE_PACKAGE)
        content = dict(result)["UnsupportedParameterException.java"]
        assert "providerName" in content
        assert "unsupportedParameter" in content
        assert "supportedParameters" in content

    def test_typed_response_exception_fields(self, generator):
        result = generator._render_exception_classes(BASE_PACKAGE)
        content = dict(result)["TypedResponseDeserializationException.java"]
        assert "expectedType" in content
        assert "rawResponse" in content

    def test_circuit_open_exception_fields(self, generator):
        result = generator._render_exception_classes(BASE_PACKAGE)
        content = dict(result)["ProviderCircuitOpenException.java"]
        assert "providerName" in content
        assert "failureRate" in content
        assert "PROVIDER_CIRCUIT_OPEN" not in content  # That's in the handler, not here
