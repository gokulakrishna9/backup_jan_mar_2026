"""Unit tests for the AI AiPomGenerator.

Verifies that the AiPomGenerator produces correct Maven dependency XML
entries based on which AI features are enabled in the AI_Layer definition.

Requirements: 2.30, 2.34, 8.10, 11.9, 13.40, 15.5
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_pom_generator import AiPomGenerator


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
    return AiPomGenerator(jinja_env)


# ======================================================================
# Helper: minimal AI layer builders
# ======================================================================

def _minimal_ai_layer():
    """Minimal AI layer with one provider — no optional features."""
    return {
        "providers": [
            {"name": "gpt", "type": "openai", "model": "gpt-4"},
        ],
    }


def _ai_layer_with_openai_and_ollama():
    return {
        "providers": [
            {"name": "gpt", "type": "openai", "model": "gpt-4"},
            {"name": "llama", "type": "ollama", "model": "llama3"},
        ],
    }


def _ai_layer_with_tika():
    return {
        "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4"}],
        "documentIngestion": {"enabled": True},
    }


def _ai_layer_with_milvus_explicit():
    return {
        "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4"}],
        "vectorStore": {"type": "milvus", "host": "localhost", "port": 19530},
    }


def _ai_layer_with_milvus_implicit():
    """No explicit vectorStore but a semantic RAG source — implies Milvus."""
    return {
        "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4"}],
        "ragSources": [
            {"name": "docs", "type": "semantic", "enabled": True, "providerName": "gpt"},
        ],
    }


def _ai_layer_with_mcp_stdio():
    return {
        "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4"}],
        "mcpServers": [
            {"name": "fs", "transportType": "stdio", "enabled": True, "command": "node"},
        ],
    }


def _ai_layer_with_mcp_sse():
    return {
        "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4"}],
        "mcpServers": [
            {"name": "web", "transportType": "sse", "enabled": True, "url": "http://localhost:3000"},
        ],
    }


def _ai_layer_with_prometheus():
    return {
        "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4"}],
        "observability": {
            "enabled": True,
            "prometheus": {"endpointPath": "/actuator/prometheus"},
        },
    }


def _ai_layer_all_features():
    """AI layer with every feature that triggers a dependency."""
    return {
        "providers": [
            {"name": "gpt", "type": "openai", "model": "gpt-4"},
            {"name": "llama", "type": "ollama", "model": "llama3"},
        ],
        "documentIngestion": {"enabled": True},
        "vectorStore": {"type": "milvus", "host": "localhost", "port": 19530},
        "mcpServers": [
            {"name": "fs", "transportType": "stdio", "enabled": True, "command": "node"},
            {"name": "web", "transportType": "sse", "enabled": True, "url": "http://localhost:3000"},
        ],
        "observability": {
            "enabled": True,
            "prometheus": {"endpointPath": "/actuator/prometheus"},
        },
    }


# ======================================================================
# Test: No generation when no AI layer
# ======================================================================


class TestNoGeneration:
    def test_none_ai_layer(self, generator):
        assert generator.generate(None) == []

    def test_empty_dict(self, generator):
        # Empty dict is a valid (minimal) AI layer — generates base deps
        result = generator.generate({})
        assert len(result) == 1
        content = result[0][1]
        assert "spring-ai-starter" in content


# ======================================================================
# Test: Always-present dependencies
# ======================================================================


class TestAlwaysPresent:
    def test_spring_ai_starter_always_present(self, generator):
        result = generator.generate(_minimal_ai_layer())
        content = result[0][1]
        assert "spring-ai-starter" in content

    def test_resilience4j_always_present(self, generator):
        result = generator.generate(_minimal_ai_layer())
        content = result[0][1]
        assert "resilience4j-spring-boot3" in content
        assert "resilience4j-reactor" in content


# ======================================================================
# Test: Conditional OpenAI / Ollama starters (Req 2.34)
# ======================================================================


class TestProviderStarters:
    def test_openai_starter_when_openai_provider(self, generator):
        result = generator.generate(_minimal_ai_layer())
        content = result[0][1]
        assert "spring-ai-openai-spring-boot-starter" in content

    def test_no_ollama_starter_when_only_openai(self, generator):
        result = generator.generate(_minimal_ai_layer())
        content = result[0][1]
        assert "spring-ai-ollama-spring-boot-starter" not in content

    def test_both_starters_when_both_providers(self, generator):
        result = generator.generate(_ai_layer_with_openai_and_ollama())
        content = result[0][1]
        assert "spring-ai-openai-spring-boot-starter" in content
        assert "spring-ai-ollama-spring-boot-starter" in content

    def test_ollama_only(self, generator):
        layer = {
            "providers": [{"name": "llama", "type": "ollama", "model": "llama3"}],
        }
        result = generator.generate(layer)
        content = result[0][1]
        assert "spring-ai-ollama-spring-boot-starter" in content
        assert "spring-ai-openai-spring-boot-starter" not in content


# ======================================================================
# Test: Tika dependencies (Req 11.9)
# ======================================================================


class TestTikaDependency:
    def test_tika_when_ingestion_enabled(self, generator):
        result = generator.generate(_ai_layer_with_tika())
        content = result[0][1]
        assert "tika-core" in content
        assert "tika-parsers-standard-package" in content

    def test_no_tika_when_ingestion_absent(self, generator):
        result = generator.generate(_minimal_ai_layer())
        content = result[0][1]
        assert "tika-core" not in content

    def test_no_tika_when_ingestion_disabled(self, generator):
        layer = {
            "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4"}],
            "documentIngestion": {"enabled": False},
        }
        result = generator.generate(layer)
        content = result[0][1]
        assert "tika-core" not in content


# ======================================================================
# Test: Milvus SDK (Req 8.10)
# ======================================================================


class TestMilvusDependency:
    def test_milvus_when_explicit_milvus(self, generator):
        result = generator.generate(_ai_layer_with_milvus_explicit())
        content = result[0][1]
        assert "milvus-sdk-java" in content

    def test_milvus_when_implicit_semantic_rag(self, generator):
        result = generator.generate(_ai_layer_with_milvus_implicit())
        content = result[0][1]
        assert "milvus-sdk-java" in content

    def test_no_milvus_when_no_vectorstore_no_rag(self, generator):
        result = generator.generate(_minimal_ai_layer())
        content = result[0][1]
        assert "milvus-sdk-java" not in content

    def test_no_milvus_when_qdrant(self, generator):
        layer = {
            "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4"}],
            "vectorStore": {"type": "qdrant", "host": "localhost", "port": 6333},
        }
        result = generator.generate(layer)
        content = result[0][1]
        assert "milvus-sdk-java" not in content

    def test_no_milvus_when_rag_disabled(self, generator):
        layer = {
            "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4"}],
            "ragSources": [
                {"name": "docs", "type": "semantic", "enabled": False, "providerName": "gpt"},
            ],
        }
        result = generator.generate(layer)
        content = result[0][1]
        assert "milvus-sdk-java" not in content


# ======================================================================
# Test: MCP starters (Req 13.40)
# ======================================================================


class TestMcpDependencies:
    def test_stdio_mcp_starter(self, generator):
        result = generator.generate(_ai_layer_with_mcp_stdio())
        content = result[0][1]
        assert "spring-ai-mcp-client-spring-boot-starter" in content
        assert "spring-ai-mcp-client-webflux-spring-boot-starter" not in content

    def test_sse_mcp_starter(self, generator):
        result = generator.generate(_ai_layer_with_mcp_sse())
        content = result[0][1]
        assert "spring-ai-mcp-client-webflux-spring-boot-starter" in content
        assert "spring-ai-mcp-client-spring-boot-starter" not in content

    def test_no_mcp_when_disabled(self, generator):
        layer = {
            "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4"}],
            "mcpServers": [
                {"name": "fs", "transportType": "stdio", "enabled": False, "command": "node"},
            ],
        }
        result = generator.generate(layer)
        content = result[0][1]
        assert "mcp-client" not in content

    def test_no_mcp_when_absent(self, generator):
        result = generator.generate(_minimal_ai_layer())
        content = result[0][1]
        assert "mcp-client" not in content


# ======================================================================
# Test: Prometheus (Req 15.5)
# ======================================================================


class TestPrometheusDependency:
    def test_prometheus_when_observability_enabled(self, generator):
        result = generator.generate(_ai_layer_with_prometheus())
        content = result[0][1]
        assert "micrometer-registry-prometheus" in content

    def test_no_prometheus_when_observability_absent(self, generator):
        result = generator.generate(_minimal_ai_layer())
        content = result[0][1]
        assert "micrometer-registry-prometheus" not in content

    def test_no_prometheus_when_observability_disabled(self, generator):
        layer = {
            "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4"}],
            "observability": {"enabled": False},
        }
        result = generator.generate(layer)
        content = result[0][1]
        assert "micrometer-registry-prometheus" not in content

    def test_no_prometheus_when_no_prometheus_section(self, generator):
        layer = {
            "providers": [{"name": "gpt", "type": "openai", "model": "gpt-4"}],
            "observability": {"enabled": True},
        }
        result = generator.generate(layer)
        content = result[0][1]
        assert "micrometer-registry-prometheus" not in content


# ======================================================================
# Test: All features combined
# ======================================================================


class TestAllFeatures:
    def test_all_dependencies_present(self, generator):
        result = generator.generate(_ai_layer_all_features())
        content = result[0][1]
        assert "spring-ai-starter" in content
        assert "spring-ai-openai-spring-boot-starter" in content
        assert "spring-ai-ollama-spring-boot-starter" in content
        assert "resilience4j-spring-boot3" in content
        assert "resilience4j-reactor" in content
        assert "tika-core" in content
        assert "tika-parsers-standard-package" in content
        assert "milvus-sdk-java" in content
        assert "spring-ai-mcp-client-spring-boot-starter" in content
        assert "spring-ai-mcp-client-webflux-spring-boot-starter" in content
        assert "micrometer-registry-prometheus" in content

    def test_output_is_valid_xml_fragment(self, generator):
        result = generator.generate(_ai_layer_all_features())
        content = result[0][1]
        assert content.strip().startswith("<!--") or content.strip().startswith("<dependencies>")
        assert content.strip().endswith("</dependencies>")


# ======================================================================
# Test: Output path
# ======================================================================


class TestOutputPath:
    def test_default_output_path(self, generator):
        result = generator.generate(_minimal_ai_layer())
        assert result[0][0] == "ai_dependencies.xml"

    def test_custom_output_path(self, generator):
        result = generator.generate(_minimal_ai_layer(), output_path="custom/deps.xml")
        assert result[0][0] == "custom/deps.xml"
