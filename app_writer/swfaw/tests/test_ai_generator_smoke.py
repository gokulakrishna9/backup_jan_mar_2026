"""Smoke tests for the full AI generation pipeline.

Tests that AiGenerator.generate() and regenerate() produce the expected
files with correct package structure and no generation errors when given
a comprehensive AI_Layer definition.

Requirements: All
"""

import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from swfaw.generators.ai_generator import AiGenerator


# ---------------------------------------------------------------------------
# Minimal DefinitionBundle stub
# ---------------------------------------------------------------------------

BASE_PACKAGE = "com.example.app"


@dataclass
class _StubBundle:
    """Minimal DefinitionBundle stub for smoke tests."""

    project_metadata: dict
    entity_layer: dict
    controller_layer: dict
    ai_layer: dict | None = None


def _make_bundle(ai_layer: dict | None) -> _StubBundle:
    """Build a stub bundle with the given AI layer."""
    return _StubBundle(
        project_metadata={
            "projectMetadata": {"groupId": BASE_PACKAGE, "artifactId": "test-app"}
        },
        entity_layer={
            "entities": [
                {
                    "tableName": "course",
                    "className": "Course",
                    "fields": [
                        {"columnName": "id", "fieldName": "id", "javaType": "Long"},
                        {"columnName": "title", "fieldName": "title", "javaType": "String"},
                    ],
                }
            ]
        },
        controller_layer={
            "controllers": [
                {"entityName": "Course", "basePath": "/api/courses"}
            ]
        },
        ai_layer=ai_layer,
    )


# ---------------------------------------------------------------------------
# Comprehensive AI_Layer definition exercising all features
# ---------------------------------------------------------------------------

COMPREHENSIVE_AI_LAYER = {
    "schemaVersion": "1.0",
    "providers": [
        {
            "name": "mainGpt",
            "type": "openai",
            "model": "gpt-4o",
            "embeddingModel": "text-embedding-3-small",
            "apiKeyEnvVar": "OPENAI_API_KEY",
            "temperature": 0.7,
            "maxTokens": 2048,
            "supportedRoles": ["system", "user", "assistant"],
            "supportedParameters": ["topP", "frequencyPenalty", "presencePenalty"],
            "parameterFallbacks": {"topK": "skip"},
            "roleFallbacks": {"tool": "merge_to_system"},
            "chatOptions": {"topP": 0.9},
            "resilience": {
                "retry": {"maxAttempts": 3, "backoffMs": 1000, "retryableStatuses": [429, 503], "retryOnTimeout": True},
                "circuitBreaker": {"failureRateThreshold": 50, "waitDurationMs": 30000, "slidingWindowSize": 10, "minimumNumberOfCalls": 5},
            },
        },
        {
            "name": "localOllama",
            "type": "ollama",
            "model": "llama3",
            "apiKeyEnvVar": "OLLAMA_KEY",
            "temperature": 0.5,
            "maxTokens": 1024,
            "supportedRoles": ["system", "user", "assistant"],
            "supportedParameters": ["topP", "topK", "repeatPenalty"],
            "parameterFallbacks": {},
            "roleFallbacks": {},
        },
    ],
    "entityCapabilities": [
        {
            "entityName": "Course",
            "providerName": "mainGpt",
            "enabledOperations": ["search", "generate", "summarize", "classify", "chat", "chatStream"],
            "searchableFields": ["title"],
            "evaluatorNames": ["relevancyEval"],
            "ragSourceNames": ["courseRag"],
            "responseType": {
                "className": "CourseAiResult",
                "wrapper": "TypedResponseResult",
                "fallbackBehavior": "raw_string",
            },
        }
    ],
    "standaloneOperations": [
        {
            "name": "generalChat",
            "type": "chat",
            "providerName": "mainGpt",
            "basePath": "/api/ai/general-chat",
            "systemPrompt": "You are a helpful assistant.",
            "enabledActions": ["chat", "chatStream", "generate"],
            "assistantName": "defaultAssistant",
            "stateTable": {
                "tableName": "general_chat_state",
                "columns": [
                    {"name": "topic", "type": "VARCHAR", "length": 255, "nullable": True},
                    {"name": "turn_count", "type": "INT", "nullable": False, "defaultValue": "0"},
                ],
            },
        }
    ],
    "promptTemplates": [
        {
            "name": "searchPrompt",
            "operation": "search",
            "template": "Search for {{query}} in courses",
            "entityName": "Course",
        }
    ],
    "assistants": [
        {
            "name": "defaultAssistant",
            "systemPrompt": "You are a course assistant.",
            "providerName": "mainGpt",
            "entityScope": "Course",
            "memoryWindowSize": 20,
        }
    ],
    "ragSources": [
        {
            "name": "courseRag",
            "type": "semantic",
            "enabled": True,
            "providerName": "mainGpt",
            "targets": [{"entityName": "Course", "fields": ["title"]}],
            "chunkSize": 512,
            "chunkOverlap": 50,
            "topK": 5,
            "similarityThreshold": 0.7,
            "securityMode": "public",
        }
    ],
    "evaluators": [
        {
            "name": "relevancyEval",
            "type": "relevancy",
            "providerName": "mainGpt",
            "evaluationPrompt": "Rate relevancy of {{output}} to {{input}}",
            "scoringMechanism": "numeric",
            "threshold": 0.8,
            "failureAction": "warn",
            "mode": "sync",
        }
    ],
    "vectorStore": {
        "type": "milvus",
        "host": "localhost",
        "port": 19530,
        "collectionPrefix": "ai_",
        "maxConnections": 10,
        "connectTimeoutMs": 5000,
        "idleTimeoutMs": 60000,
    },
    "documentIngestion": {
        "enabled": True,
        "allowedMimeTypes": ["application/pdf", "text/plain"],
        "maxFileSizeBytes": 10485760,
        "metadataFields": ["author", "category"],
        "autoIndexOnUpload": True,
        "targetRagSourceName": "courseRag",
        "sources": [{"type": "rest"}],
    },
    "documentProcessing": {
        "enabled": True,
        "defaultProviderName": "mainGpt",
        "tasks": [
            {
                "name": "summarizeDoc",
                "taskType": "summarization",
                "providerName": "mainGpt",
                "promptTemplate": "Summarize: {{document_text}}",
            }
        ],
    },
    "orchestrator": {
        "providerName": "mainGpt",
        "systemPrompt": "You are an orchestrator.",
        "promptSecurity": {
            "safeGuardAdvisor": {"enabled": True, "sensitiveWords": ["hack"]},
            "canaryWordAdvisor": {"enabled": True, "canaryTokens": ["CANARY123"]},
            "inputSanitization": {"enabled": False, "rules": []},
            "outputFiltering": {"enabled": False, "rules": []},
        },
        "moderation": {
            "enabled": True,
            "providerName": "mainGpt",
            "categories": ["hate", "violence"],
            "preModeration": True,
            "postModeration": True,
            "failureAction": "block",
        },
    },
    "mcpServers": [
        {
            "name": "localMcp",
            "transportType": "stdio",
            "enabled": True,
            "requiredRoles": ["ADMIN"],
        }
    ],
    "observability": {
        "enabled": True,
        "prometheus": {"endpointPath": "/actuator/prometheus", "scrapeIntervalHint": "15s"},
        "grafana": {"url": "http://localhost:3000", "apiKeyEnvVar": "GRAFANA_KEY", "orgId": 1},
        "dashboards": [
            {
                "name": "aiOverview",
                "panels": [
                    {"title": "Request Count", "metricName": "ai_requests_total", "type": "graph", "span": 12}
                ],
            }
        ],
    },
    "rateLimiting": {"defaultRpm": 20},
    "tokenBudget": {
        "enabled": True,
        "defaultDailyLimitPerUser": 100000,
        "defaultMonthlyLimitPerUser": 2000000,
        "warningThresholdPercent": 80,
        "enforcementAction": "block",
    },
    "chatSessionCleanup": {
        "enabled": True,
        "defaultTtlDays": 30,
        "cleanupCronExpression": "0 0 2 * * *",
        "batchSize": 1000,
        "topicSummarization": {
            "enabled": True,
            "providerName": "mainGpt",
            "maxTopicsPerSession": 5,
        },
    },
    "auditLog": {
        "enabled": True,
        "retentionDays": 90,
        "cleanupCronExpression": "0 0 3 * * *",
        "loggedEvents": ["orchestrator_request", "tool_invocation", "moderation_flag"],
    },
}

# Minimal AI_Layer — just a provider, no features enabled
MINIMAL_AI_LAYER = {
    "schemaVersion": "1.0",
    "providers": [
        {
            "name": "simpleGpt",
            "type": "openai",
            "model": "gpt-4",
            "apiKeyEnvVar": "OPENAI_API_KEY",
            "temperature": 0.7,
            "maxTokens": 2048,
            "supportedRoles": ["system", "user", "assistant"],
        }
    ],
    "entityCapabilities": [],
    "standaloneOperations": [],
    "promptTemplates": [],
    "assistants": [],
    "ragSources": [],
    "evaluators": [],
    "mcpServers": [],
}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def output_dir():
    """Create a temporary output directory."""
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


@pytest.fixture
def generator():
    return AiGenerator()


# ---------------------------------------------------------------------------
# Test: Full generation with comprehensive definition
# ---------------------------------------------------------------------------

class TestFullGeneration:
    """Smoke tests for AiGenerator.generate() with a comprehensive definition."""

    def test_generate_produces_files(self, generator, output_dir):
        """Full generation with all features produces a non-empty file list."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        assert len(paths) > 0, "Expected at least one generated file"

    def test_all_files_exist_on_disk(self, generator, output_dir):
        """Every returned Path actually exists on disk."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        for p in paths:
            assert p.exists(), f"Generated file does not exist: {p}"

    def test_all_files_are_nonempty(self, generator, output_dir):
        """Every generated file has non-empty content."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        for p in paths:
            content = p.read_text(encoding="utf-8")
            assert len(content.strip()) > 0, f"Generated file is empty: {p}"

    def test_correct_package_structure(self, generator, output_dir):
        """Generated Java files live under the correct package directory."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        package_path = BASE_PACKAGE.replace(".", "/")
        java_files = [p for p in paths if str(p).endswith(".java")]
        for p in java_files:
            assert package_path in str(p), (
                f"Java file not under expected package path: {p}"
            )

    def test_provider_files_generated(self, generator, output_dir):
        """Provider-related files are generated (ChatClientConfig, etc.)."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        assert "ChatClientConfig.java" in filenames
        assert "ChatOptionsResolver.java" in filenames
        assert "RoleValidationAdvisor.java" in filenames
        assert "ProviderResilienceConfig.java" in filenames

    def test_entity_ai_files_generated(self, generator, output_dir):
        """Entity AI service and controller are generated for Course."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        assert "CourseAiService.java" in filenames
        assert "CourseAiController.java" in filenames

    def test_standalone_files_generated(self, generator, output_dir):
        """Standalone AI service, controller, and state files are generated."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        assert "GeneralChatAiService.java" in filenames
        assert "GeneralChatAiController.java" in filenames
        # State entity + repository for stateTable
        assert "GeneralChatState.java" in filenames
        assert "GeneralChatStateRepository.java" in filenames

    def test_prompt_template_engine_generated(self, generator, output_dir):
        """PromptTemplateEngine utility is generated."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        assert "PromptTemplateEngine.java" in filenames

    def test_conversation_files_generated(self, generator, output_dir):
        """Conversation entities and service are generated."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        assert "AiChatSession.java" in filenames
        assert "AiChatMessage.java" in filenames
        assert "ConversationMemoryService.java" in filenames

    def test_rag_files_generated(self, generator, output_dir):
        """RAG-related files are generated when RAG sources are enabled."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        # At least one RAG service file should exist
        rag_files = [f for f in filenames if "rag" in f.lower() or "Rag" in f]
        assert len(rag_files) > 0, "Expected RAG-related files"

    def test_evaluator_files_generated(self, generator, output_dir):
        """Evaluator pipeline files are generated."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        eval_files = [f for f in filenames if "valuat" in f.lower()]
        assert len(eval_files) > 0, "Expected evaluator-related files"

    def test_orchestrator_files_generated(self, generator, output_dir):
        """Orchestrator service and controller are generated."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        assert "AiOrchestratorService.java" in filenames
        assert "AiOrchestratorController.java" in filenames

    def test_security_files_generated(self, generator, output_dir):
        """Prompt security files are generated when orchestrator has security."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        security_files = [f for f in filenames if "SafeGuard" in f or "Canary" in f or "Moderation" in f]
        assert len(security_files) > 0, "Expected security-related files"

    def test_ddl_file_generated(self, generator, output_dir):
        """DDL SQL file is generated for AI tables."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        sql_files = [p for p in paths if str(p).endswith(".sql")]
        assert len(sql_files) > 0, "Expected at least one SQL DDL file"

    def test_pom_dependencies_generated(self, generator, output_dir):
        """Maven dependency XML is generated."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        xml_files = [p for p in paths if str(p).endswith(".xml")]
        assert len(xml_files) > 0, "Expected Maven dependency XML file"

    def test_app_properties_generated(self, generator, output_dir):
        """Application properties file is generated."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        props_files = [p for p in paths if "properties" in str(p)]
        assert len(props_files) > 0, "Expected application properties file"

    def test_observability_files_generated(self, generator, output_dir):
        """Observability files are generated when enabled."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        obs_files = [f for f in filenames if "Metrics" in f or "Health" in f or "Observability" in f or "Grafana" in f]
        assert len(obs_files) > 0, "Expected observability-related files"

    def test_token_budget_files_generated(self, generator, output_dir):
        """Token budget files are generated when enabled."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        budget_files = [f for f in filenames if "Budget" in f or "budget" in f.lower()]
        assert len(budget_files) > 0, "Expected token budget files"

    def test_audit_files_generated(self, generator, output_dir):
        """Audit log files are generated when enabled."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        audit_files = [f for f in filenames if "Audit" in f or "audit" in f.lower()]
        assert len(audit_files) > 0, "Expected audit log files"

    def test_session_cleanup_files_generated(self, generator, output_dir):
        """Session cleanup files are generated when enabled."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        cleanup_files = [f for f in filenames if "Cleanup" in f or "Topic" in f]
        assert len(cleanup_files) > 0, "Expected session cleanup files"

    def test_no_generation_errors(self, generator, output_dir):
        """Full generation completes without raising any exceptions."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        # Should not raise
        paths = generator.generate(bundle, output_dir)
        assert isinstance(paths, list)


# ---------------------------------------------------------------------------
# Test: Minimal definition (only providers, no features)
# ---------------------------------------------------------------------------

class TestMinimalGeneration:
    """Smoke tests with a minimal AI_Layer (providers only)."""

    def test_minimal_generates_provider_files(self, generator, output_dir):
        """Minimal definition still generates provider config files."""
        bundle = _make_bundle(MINIMAL_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        assert "ChatClientConfig.java" in filenames

    def test_minimal_no_entity_ai_files(self, generator, output_dir):
        """No entity AI files when entityCapabilities is empty."""
        bundle = _make_bundle(MINIMAL_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        assert "CourseAiService.java" not in filenames

    def test_minimal_no_standalone_files(self, generator, output_dir):
        """No standalone files when standaloneOperations is empty."""
        bundle = _make_bundle(MINIMAL_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        standalone_files = [f for f in filenames if "Standalone" in f or "GeneralChat" in f]
        assert len(standalone_files) == 0

    def test_minimal_no_orchestrator_files(self, generator, output_dir):
        """No orchestrator files when orchestrator is absent."""
        bundle = _make_bundle(MINIMAL_AI_LAYER)
        paths = generator.generate(bundle, output_dir)
        filenames = {p.name for p in paths}
        assert "AiOrchestratorService.java" not in filenames


# ---------------------------------------------------------------------------
# Test: None AI layer
# ---------------------------------------------------------------------------

class TestNoneAiLayer:
    """When ai_layer is None, no files are generated."""

    def test_none_ai_layer_returns_empty(self, generator, output_dir):
        bundle = _make_bundle(None)
        paths = generator.generate(bundle, output_dir)
        assert paths == []


# ---------------------------------------------------------------------------
# Test: Incremental regeneration
# ---------------------------------------------------------------------------

class TestRegeneration:
    """Smoke tests for AiGenerator.regenerate()."""

    def test_regenerate_produces_same_files(self, generator, output_dir):
        """regenerate() produces the same files as generate()."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        gen_paths = generator.generate(bundle, output_dir)
        gen_names = sorted(p.name for p in gen_paths)

        # Regenerate into the same directory
        regen_paths = generator.regenerate(bundle, output_dir)
        regen_names = sorted(p.name for p in regen_paths)

        assert gen_names == regen_names

    def test_regenerate_overwrites_existing(self, generator, output_dir):
        """regenerate() overwrites previously generated files."""
        bundle = _make_bundle(COMPREHENSIVE_AI_LAYER)
        paths = generator.generate(bundle, output_dir)

        # Corrupt a file
        if paths:
            paths[0].write_text("CORRUPTED", encoding="utf-8")

        # Regenerate should overwrite
        regen_paths = generator.regenerate(bundle, output_dir)
        if regen_paths:
            content = regen_paths[0].read_text(encoding="utf-8")
            assert content != "CORRUPTED"

    def test_regenerate_none_ai_layer_returns_empty(self, generator, output_dir):
        """regenerate() with None ai_layer returns empty list."""
        bundle = _make_bundle(None)
        paths = generator.regenerate(bundle, output_dir)
        assert paths == []
