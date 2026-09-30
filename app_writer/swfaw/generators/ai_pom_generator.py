"""POM dependency sub-generator for the AI Layer.

Generates Maven dependency XML entries for all AI-related libraries
based on which features are enabled in the AI_Layer definition.

Dependencies generated (conditionally):
- spring-ai-starter: always when AI layer is present
- spring-ai-openai-spring-boot-starter: when any OpenAI provider exists
- spring-ai-ollama-spring-boot-starter: when any Ollama provider exists
- resilience4j-spring-boot3 + resilience4j-reactor: always (default resilience)
- tika-core + tika-parsers-standard-package: when documentIngestion enabled
- milvus-sdk-java: when vectorStore type is "milvus" or absent with semantic RAG
- spring-ai-mcp-client-spring-boot-starter: when any stdio MCP server enabled
- spring-ai-mcp-client-webflux-spring-boot-starter: when any SSE MCP server enabled
- micrometer-registry-prometheus: when observability.prometheus configured

Requirements: 2.30, 2.34, 8.10, 9.9 (Tika from 11.9), 13.40, 15.5
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2


class AiPomGenerator:
    """Generates Maven dependency XML entries from the AI_Layer definition.

    Follows the same sub-generator pattern as other AI sub-generators:
    receives the full AI_Layer definition, inspects which features are
    enabled, loads and renders a Jinja2 template, and returns a list
    of ``(filepath, content)`` tuples.
    """

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        ai_layer: dict | None,
        output_path: str = "ai_dependencies.xml",
    ) -> list[tuple[str, str]]:
        """Generate AI Maven dependency XML file.

        Returns a list of ``(filepath, content)`` tuples.  When no AI
        layer is configured, an empty list is returned.
        """
        if ai_layer is None:
            return []

        ctx = self._build_context(ai_layer)
        content = self._render("pom/ai_dependencies.xml.j2", ctx)
        return [(output_path, content)]

    # ------------------------------------------------------------------
    # Feature detection helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _has_openai_provider(ai_layer: dict) -> bool:
        """Req 2.34: OpenAI starter when any provider has type 'openai'."""
        for p in ai_layer.get("providers", []):
            if p.get("type") == "openai":
                return True
        return False

    @staticmethod
    def _has_ollama_provider(ai_layer: dict) -> bool:
        """Req 2.34: Ollama starter when any provider has type 'ollama'."""
        for p in ai_layer.get("providers", []):
            if p.get("type") == "ollama":
                return True
        return False

    @staticmethod
    def _has_document_ingestion(ai_layer: dict) -> bool:
        """Req 11.9: Tika dependencies when documentIngestion enabled."""
        ingestion = ai_layer.get("documentIngestion")
        return bool(ingestion and ingestion.get("enabled", False))

    @staticmethod
    def _needs_milvus(ai_layer: dict) -> bool:
        """Req 8.10: Milvus SDK when vectorStore type is 'milvus' or absent
        with at least one semantic RAG source enabled."""
        vs = ai_layer.get("vectorStore")
        if vs:
            return vs.get("type", "milvus") == "milvus"
        # No explicit vectorStore — check if any semantic RAG source is enabled
        for src in ai_layer.get("ragSources", []):
            if src.get("enabled", False) and src.get("type") == "semantic":
                return True
        return False

    @staticmethod
    def _has_stdio_mcp(ai_layer: dict) -> bool:
        """Req 13.40: stdio MCP starter when any enabled stdio MCP server."""
        for srv in ai_layer.get("mcpServers", []):
            if srv.get("enabled", False) and srv.get("transportType") == "stdio":
                return True
        return False

    @staticmethod
    def _has_sse_mcp(ai_layer: dict) -> bool:
        """Req 13.40: SSE MCP starter when any enabled SSE MCP server."""
        for srv in ai_layer.get("mcpServers", []):
            if srv.get("enabled", False) and srv.get("transportType") == "sse":
                return True
        return False

    @staticmethod
    def _has_prometheus(ai_layer: dict) -> bool:
        """Req 15.5: micrometer-prometheus when observability.prometheus configured."""
        obs = ai_layer.get("observability")
        if not obs or not obs.get("enabled", False):
            return False
        return obs.get("prometheus") is not None

    # ------------------------------------------------------------------
    # Context builder
    # ------------------------------------------------------------------

    def _build_context(self, ai_layer: dict) -> dict:
        """Build the Jinja2 template context from the AI_Layer definition."""
        return {
            "has_openai": self._has_openai_provider(ai_layer),
            "has_ollama": self._has_ollama_provider(ai_layer),
            "has_resilience": True,  # Req 2.30: always included (default resilience)
            "has_tika": self._has_document_ingestion(ai_layer),
            "has_milvus": self._needs_milvus(ai_layer),
            "has_stdio_mcp": self._has_stdio_mcp(ai_layer),
            "has_sse_mcp": self._has_sse_mcp(ai_layer),
            "has_prometheus": self._has_prometheus(ai_layer),
        }

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _render(self, template_name: str, ctx: dict) -> str:
        """Render a Jinja2 template under the ai/ prefix."""
        template = self.jinja_env.get_template(f"ai/{template_name}")
        return template.render(**ctx)
