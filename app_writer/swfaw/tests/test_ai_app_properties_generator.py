"""Unit tests for the AI AiAppPropertiesGenerator.

Verifies that the AiAppPropertiesGenerator produces correct
application.properties entries for all AI configuration sections.

Requirements: 2.4, 2.29, 4.22, 8.9, 15.11, 15.28, 15.42
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from swfaw.generators.ai_app_properties_generator import (
    AiAppPropertiesGenerator,
)


@pytest.fixture
def generator():
    return AiAppPropertiesGenerator()


# ======================================================================
# Helper: AI layer builders
# ======================================================================

def _minimal_ai_layer():
    return {
        "providers": [
            {
                "name": "gpt",
                "type": "openai",
                "model": "gpt-4",
                "apiKeyEnvVar": "OPENAI_API_KEY",
            },
        ],
    }


def _provider_with_all_options():
    return {
        "providers": [
            {
                "name": "gpt",
                "type": "openai",
                "model": "gpt-4",
                "embeddingModel": "text-embedding-3-small",
                "baseUrl": "https://api.openai.com/v1",
                "apiKeyEnvVar": "OPENAI_API_KEY",
                "temperature": 0.5,
                "maxTokens": 4096,
                "chatOptions": {
                    "topP": 0.9,
                    "frequencyPenalty": 0.5,
                },
                "supportedParameters": ["temperature", "maxTokens", "topP"],
                "parameterFallbacks": {"topK": "skip", "repeatPenalty": "error"},
                "supportedRoles": ["system", "user", "assistant"],
                "roleFallbacks": {"tool": "skip"},
                "resilience": {
                    "retry": {
                        "maxAttempts": 5,
                        "backoffMs": 2000,
                        "retryableStatuses": [429, 500, 503],
                        "retryOnTimeout": False,
                    },
                    "circuitBreaker": {
                        "failureRateThreshold": 60,
                        "waitDurationMs": 45000,
                        "slidingWindowSize": 20,
                        "minimumNumberOfCalls": 10,
                    },
                },
            },
        ],
    }


def _ai_layer_with_cleanup():
    return {
        "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4", "apiKeyEnvVar": "KEY"}],
        "chatSessionCleanup": {
            "enabled": True,
            "defaultTtlDays": 14,
            "cleanupCronExpression": "0 0 3 * * *",
            "batchSize": 500,
            "topicSummarization": {
                "enabled": True,
                "providerName": "gpt",
                "maxTopicsPerSession": 3,
            },
        },
    }


def _ai_layer_with_vector_store():
    return {
        "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4", "apiKeyEnvVar": "KEY"}],
        "vectorStore": {
            "type": "milvus",
            "host": "milvus.local",
            "port": 19530,
            "apiKey": "secret",
            "database": "ai_db",
            "collectionPrefix": "app_",
            "maxConnections": 20,
            "connectTimeoutMs": 10000,
            "idleTimeoutMs": 120000,
        },
    }


def _ai_layer_with_observability():
    return {
        "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4", "apiKeyEnvVar": "KEY"}],
        "observability": {
            "enabled": True,
            "prometheus": {"endpointPath": "/metrics"},
            "grafana": {
                "url": "http://grafana:3000",
                "apiKeyEnvVar": "GRAFANA_KEY",
                "orgId": 2,
            },
        },
    }


def _ai_layer_with_token_budget():
    return {
        "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4", "apiKeyEnvVar": "KEY"}],
        "tokenBudget": {
            "enabled": True,
            "defaultDailyLimitPerUser": 100000,
            "defaultMonthlyLimitPerUser": 2000000,
            "warningThresholdPercent": 90,
            "enforcementAction": "warn",
            "providerOverrides": {
                "gpt": {"dailyLimit": 50000, "monthlyLimit": 1000000},
            },
        },
    }


def _ai_layer_with_audit():
    return {
        "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4", "apiKeyEnvVar": "KEY"}],
        "auditLog": {
            "enabled": True,
            "retentionDays": 60,
            "cleanupCronExpression": "0 0 4 * * *",
            "loggedEvents": ["orchestrator_request", "tool_invocation"],
        },
    }


# ======================================================================
# Test: No generation when no AI layer
# ======================================================================


class TestNoGeneration:
    def test_none_ai_layer(self, generator):
        assert generator.generate(None) == []


# ======================================================================
# Test: Provider properties (Req 2.4, 2.29)
# ======================================================================


class TestProviderProperties:
    def test_basic_provider_properties(self, generator):
        result = generator.generate(_minimal_ai_layer())
        content = result[0][1]
        assert "ai.providers.gpt.type=openai" in content
        assert "ai.providers.gpt.model=gpt-4" in content
        assert "ai.providers.gpt.api-key-env-var=OPENAI_API_KEY" in content

    def test_default_temperature_and_max_tokens(self, generator):
        result = generator.generate(_minimal_ai_layer())
        content = result[0][1]
        assert "ai.providers.gpt.temperature=0.7" in content
        assert "ai.providers.gpt.max-tokens=2048" in content

    def test_custom_temperature_and_max_tokens(self, generator):
        result = generator.generate(_provider_with_all_options())
        content = result[0][1]
        assert "ai.providers.gpt.temperature=0.5" in content
        assert "ai.providers.gpt.max-tokens=4096" in content

    def test_embedding_model(self, generator):
        result = generator.generate(_provider_with_all_options())
        content = result[0][1]
        assert "ai.providers.gpt.embedding-model=text-embedding-3-small" in content

    def test_base_url(self, generator):
        result = generator.generate(_provider_with_all_options())
        content = result[0][1]
        assert "ai.providers.gpt.base-url=https://api.openai.com/v1" in content

    def test_chat_options(self, generator):
        result = generator.generate(_provider_with_all_options())
        content = result[0][1]
        assert "ai.providers.gpt.chat-options.top-p=0.9" in content
        assert "ai.providers.gpt.chat-options.frequency-penalty=0.5" in content

    def test_supported_parameters(self, generator):
        result = generator.generate(_provider_with_all_options())
        content = result[0][1]
        assert "ai.providers.gpt.supported-parameters=temperature,maxTokens,topP" in content

    def test_parameter_fallbacks(self, generator):
        result = generator.generate(_provider_with_all_options())
        content = result[0][1]
        assert "ai.providers.gpt.parameter-fallbacks.top-k=skip" in content
        assert "ai.providers.gpt.parameter-fallbacks.repeat-penalty=error" in content

    def test_supported_roles(self, generator):
        result = generator.generate(_provider_with_all_options())
        content = result[0][1]
        assert "ai.providers.gpt.supported-roles=system,user,assistant" in content

    def test_role_fallbacks(self, generator):
        result = generator.generate(_provider_with_all_options())
        content = result[0][1]
        assert "ai.providers.gpt.role-fallbacks.tool=skip" in content

    def test_resilience_retry(self, generator):
        result = generator.generate(_provider_with_all_options())
        content = result[0][1]
        assert "ai.providers.gpt.resilience.retry.max-attempts=5" in content
        assert "ai.providers.gpt.resilience.retry.backoff-ms=2000" in content
        assert "ai.providers.gpt.resilience.retry.retryable-statuses=429,500,503" in content
        assert "ai.providers.gpt.resilience.retry.retry-on-timeout=false" in content

    def test_resilience_circuit_breaker(self, generator):
        result = generator.generate(_provider_with_all_options())
        content = result[0][1]
        assert "ai.providers.gpt.resilience.circuit-breaker.failure-rate-threshold=60" in content
        assert "ai.providers.gpt.resilience.circuit-breaker.wait-duration-ms=45000" in content
        assert "ai.providers.gpt.resilience.circuit-breaker.sliding-window-size=20" in content
        assert "ai.providers.gpt.resilience.circuit-breaker.minimum-number-of-calls=10" in content

    def test_no_provider_section_when_empty(self, generator):
        result = generator.generate({"providers": []})
        content = result[0][1]
        assert "ai.providers." not in content

    def test_multiple_providers(self, generator):
        layer = {
            "providers": [
                {"name": "gpt", "type": "openai", "model": "gpt-4", "apiKeyEnvVar": "KEY1"},
                {"name": "llama", "type": "ollama", "model": "llama3", "apiKeyEnvVar": "KEY2"},
            ],
        }
        result = generator.generate(layer)
        content = result[0][1]
        assert "ai.providers.gpt.type=openai" in content
        assert "ai.providers.llama.type=ollama" in content


# ======================================================================
# Test: Chat session cleanup properties (Req 4.22)
# ======================================================================


class TestCleanupProperties:
    def test_cleanup_properties_when_enabled(self, generator):
        result = generator.generate(_ai_layer_with_cleanup())
        content = result[0][1]
        assert "ai.chat-session-cleanup.enabled=true" in content
        assert "ai.chat-session-cleanup.default-ttl-days=14" in content
        assert "ai.chat-session-cleanup.cleanup-cron-expression=0 0 3 * * *" in content
        assert "ai.chat-session-cleanup.batch-size=500" in content

    def test_topic_summarization_properties(self, generator):
        result = generator.generate(_ai_layer_with_cleanup())
        content = result[0][1]
        assert "ai.chat-session-cleanup.topic-summarization.enabled=true" in content
        assert "ai.chat-session-cleanup.topic-summarization.provider-name=gpt" in content
        assert "ai.chat-session-cleanup.topic-summarization.max-topics-per-session=3" in content

    def test_no_cleanup_when_absent(self, generator):
        result = generator.generate(_minimal_ai_layer())
        content = result[0][1]
        assert "chat-session-cleanup" not in content

    def test_no_cleanup_when_disabled(self, generator):
        layer = {
            "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4", "apiKeyEnvVar": "KEY"}],
            "chatSessionCleanup": {"enabled": False},
        }
        result = generator.generate(layer)
        content = result[0][1]
        assert "chat-session-cleanup" not in content


# ======================================================================
# Test: Vector store properties (Req 8.9)
# ======================================================================


class TestVectorStoreProperties:
    def test_vector_store_properties(self, generator):
        result = generator.generate(_ai_layer_with_vector_store())
        content = result[0][1]
        assert "ai.vector-store.type=milvus" in content
        assert "ai.vector-store.host=milvus.local" in content
        assert "ai.vector-store.port=19530" in content
        assert "ai.vector-store.api-key=secret" in content
        assert "ai.vector-store.database=ai_db" in content
        assert "ai.vector-store.collection-prefix=app_" in content
        assert "ai.vector-store.max-connections=20" in content
        assert "ai.vector-store.connect-timeout-ms=10000" in content
        assert "ai.vector-store.idle-timeout-ms=120000" in content

    def test_no_vector_store_when_absent(self, generator):
        result = generator.generate(_minimal_ai_layer())
        content = result[0][1]
        assert "vector-store" not in content


# ======================================================================
# Test: Observability properties (Req 15.11)
# ======================================================================


class TestObservabilityProperties:
    def test_observability_properties(self, generator):
        result = generator.generate(_ai_layer_with_observability())
        content = result[0][1]
        assert "ai.observability.enabled=true" in content
        assert "ai.observability.prometheus.endpoint-path=/metrics" in content
        assert "ai.observability.grafana.url=http://grafana:3000" in content
        assert "ai.observability.grafana.api-key-env-var=GRAFANA_KEY" in content
        assert "ai.observability.grafana.org-id=2" in content

    def test_no_observability_when_absent(self, generator):
        result = generator.generate(_minimal_ai_layer())
        content = result[0][1]
        assert "ai.observability" not in content

    def test_no_observability_when_disabled(self, generator):
        layer = {
            "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4", "apiKeyEnvVar": "KEY"}],
            "observability": {"enabled": False},
        }
        result = generator.generate(layer)
        content = result[0][1]
        assert "ai.observability" not in content


# ======================================================================
# Test: Token budget properties (Req 15.28)
# ======================================================================


class TestTokenBudgetProperties:
    def test_token_budget_properties(self, generator):
        result = generator.generate(_ai_layer_with_token_budget())
        content = result[0][1]
        assert "ai.token-budget.enabled=true" in content
        assert "ai.token-budget.default-daily-limit-per-user=100000" in content
        assert "ai.token-budget.default-monthly-limit-per-user=2000000" in content
        assert "ai.token-budget.warning-threshold-percent=90" in content
        assert "ai.token-budget.enforcement-action=warn" in content

    def test_provider_overrides(self, generator):
        result = generator.generate(_ai_layer_with_token_budget())
        content = result[0][1]
        assert "ai.token-budget.provider-overrides.gpt.daily-limit=50000" in content
        assert "ai.token-budget.provider-overrides.gpt.monthly-limit=1000000" in content

    def test_no_token_budget_when_absent(self, generator):
        result = generator.generate(_minimal_ai_layer())
        content = result[0][1]
        assert "token-budget" not in content

    def test_no_token_budget_when_disabled(self, generator):
        layer = {
            "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4", "apiKeyEnvVar": "KEY"}],
            "tokenBudget": {"enabled": False},
        }
        result = generator.generate(layer)
        content = result[0][1]
        assert "token-budget" not in content


# ======================================================================
# Test: Audit log properties (Req 15.42)
# ======================================================================


class TestAuditLogProperties:
    def test_audit_log_properties(self, generator):
        result = generator.generate(_ai_layer_with_audit())
        content = result[0][1]
        assert "ai.audit-log.enabled=true" in content
        assert "ai.audit-log.retention-days=60" in content
        assert "ai.audit-log.cleanup-cron-expression=0 0 4 * * *" in content
        assert "ai.audit-log.logged-events=orchestrator_request,tool_invocation" in content

    def test_no_audit_when_absent(self, generator):
        result = generator.generate(_minimal_ai_layer())
        content = result[0][1]
        assert "audit-log" not in content

    def test_no_audit_when_disabled(self, generator):
        layer = {
            "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4", "apiKeyEnvVar": "KEY"}],
            "auditLog": {"enabled": False},
        }
        result = generator.generate(layer)
        content = result[0][1]
        assert "audit-log" not in content


# ======================================================================
# Test: Output path
# ======================================================================


class TestOutputPath:
    def test_default_output_path(self, generator):
        result = generator.generate(_minimal_ai_layer())
        assert result[0][0] == "ai-application.properties"

    def test_custom_output_path(self, generator):
        result = generator.generate(_minimal_ai_layer(), output_path="custom.properties")
        assert result[0][0] == "custom.properties"


# ======================================================================
# Test: camelCase to kebab-case utility
# ======================================================================


class TestCamelToKebab:
    def test_simple(self):
        assert AiAppPropertiesGenerator._camel_to_kebab("topP") == "top-p"

    def test_multi_word(self):
        assert AiAppPropertiesGenerator._camel_to_kebab("frequencyPenalty") == "frequency-penalty"

    def test_no_uppercase(self):
        assert AiAppPropertiesGenerator._camel_to_kebab("seed") == "seed"

    def test_leading_uppercase(self):
        assert AiAppPropertiesGenerator._camel_to_kebab("TopK") == "top-k"
