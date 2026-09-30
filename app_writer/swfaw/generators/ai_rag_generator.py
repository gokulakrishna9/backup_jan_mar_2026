"""RAG sub-generator for the AI Layer.

Generates SemanticRagService (per source), HeuristicRagService (per source),
RagContextInjector, RagIndexingService, RagIndexingController, and RagResultDTO.

Requirements: 9.1–9.15
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2

# Default RAG source settings
_SEMANTIC_DEFAULTS = {
    "chunkSize": 512,
    "chunkOverlap": 50,
    "topK": 5,
    "similarityThreshold": 0.7,
}

_HEURISTIC_DEFAULTS = {
    "maxResults": 10,
}


def _pascal_case(name: str) -> str:
    """Convert a camelCase or snake_case name to PascalCase."""
    if "_" in name:
        return "".join(part.capitalize() for part in name.split("_"))
    return name[0].upper() + name[1:] if name else name


def _camel_case(name: str) -> str:
    """Convert a name to camelCase."""
    pascal = _pascal_case(name)
    return pascal[0].lower() + pascal[1:] if pascal else pascal


class RagGenerator:
    """Generates RAG Java files from the AI_Layer definition."""

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        rag_sources: list[dict] | None,
        vector_store_config: dict | None,
        base_package: str,
        output_dirs: dict[str, Path],
    ) -> list[tuple[str, str]]:
        """Generate RAG Java files.

        Returns a list of ``(filepath, content)`` tuples where *filepath* is
        relative to the project source root.

        Req 9.1: When no enabled RAG sources exist, no RAG files are generated.
        """
        enabled_sources = self._get_enabled_sources(rag_sources)
        if not enabled_sources:
            return []

        results: list[tuple[str, str]] = []

        rag_dir = output_dirs.get("rag", Path("ai/rag"))
        controller_dir = output_dirs.get("controller", Path("ai/controller"))

        semantic_sources = [s for s in enabled_sources if s.get("type") == "semantic"]
        heuristic_sources = [s for s in enabled_sources if s.get("type") == "heuristic"]

        # 1. RagResultDTO (Req 9.6) — always generated when any source is enabled
        results.append((
            str(rag_dir / "RagResultDTO.java"),
            self._render("rag/rag_result_dto.java.j2", {"base_package": base_package}),
        ))

        # 2. SemanticRagService per source (Req 9.1)
        for source in semantic_sources:
            ctx = self._build_semantic_context(source, vector_store_config, base_package)
            name_pascal = _pascal_case(source["name"])
            results.append((
                str(rag_dir / f"{name_pascal}SemanticRagService.java"),
                self._render("rag/semantic_rag_service.java.j2", ctx),
            ))

        # 3. HeuristicRagService per source (Req 9.4)
        for source in heuristic_sources:
            ctx = self._build_heuristic_context(source, base_package)
            name_pascal = _pascal_case(source["name"])
            results.append((
                str(rag_dir / f"{name_pascal}HeuristicRagService.java"),
                self._render("rag/heuristic_rag_service.java.j2", ctx),
            ))

        # 4. RagContextInjector (Req 9.8)
        results.append((
            str(rag_dir / "RagContextInjector.java"),
            self._render("rag/rag_context_injector.java.j2", {"base_package": base_package}),
        ))

        # 5. RagIndexingService (Req 9.10) — only when semantic sources exist
        if semantic_sources:
            ctx = self._build_indexing_service_context(semantic_sources, base_package)
            results.append((
                str(rag_dir / "RagIndexingService.java"),
                self._render("rag/rag_indexing_service.java.j2", ctx),
            ))

        # 6. RagIndexingController (Req 9.12)
        ctx = self._build_controller_context(enabled_sources, base_package)
        results.append((
            str(controller_dir / "RagIndexingController.java"),
            self._render("rag/rag_indexing_controller.java.j2", ctx),
        ))

        return results

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_semantic_context(
        self, source: dict, vector_store_config: dict | None, base_package: str
    ) -> dict:
        """Build Jinja2 context for a semantic RAG service template."""
        collection_prefix = "ai_"
        if vector_store_config:
            collection_prefix = vector_store_config.get("collectionPrefix", "ai_")

        return {
            "base_package": base_package,
            "source_name": source["name"],
            "source_name_pascal": _pascal_case(source["name"]),
            "provider_name": source.get("providerName", ""),
            "chunk_size": source.get("chunkSize", _SEMANTIC_DEFAULTS["chunkSize"]),
            "chunk_overlap": source.get("chunkOverlap", _SEMANTIC_DEFAULTS["chunkOverlap"]),
            "top_k": source.get("topK", _SEMANTIC_DEFAULTS["topK"]),
            "similarity_threshold": source.get(
                "similarityThreshold", _SEMANTIC_DEFAULTS["similarityThreshold"]
            ),
            "security_mode": source.get("securityMode", "public"),
            "collection_prefix": collection_prefix,
        }

    def _build_heuristic_context(self, source: dict, base_package: str) -> dict:
        """Build Jinja2 context for a heuristic RAG service template."""
        rules = source.get("rules", [])
        processed_rules = []
        for rule in rules:
            processed_rules.append({
                "rule_type": rule.get("ruleType", "keyword"),
                "field": rule.get("field", ""),
                "pattern": rule.get("pattern", ""),
                "sql_fragment": rule.get("sqlFragment", ""),
                "weight": rule.get("weight", 1.0),
                "target_table": rule.get("targetTable", ""),
                "entity_type": rule.get("entityType", ""),
            })

        return {
            "base_package": base_package,
            "source_name": source["name"],
            "source_name_pascal": _pascal_case(source["name"]),
            "max_results": source.get("maxResults", _HEURISTIC_DEFAULTS["maxResults"]),
            "rules": processed_rules,
            "security_mode": source.get("securityMode", "public"),
        }

    def _build_indexing_service_context(
        self, semantic_sources: list[dict], base_package: str
    ) -> dict:
        """Build Jinja2 context for the RagIndexingService template."""
        sources_ctx = []
        for s in semantic_sources:
            sources_ctx.append({
                "name": s["name"],
                "name_pascal": _pascal_case(s["name"]),
                "name_camel": _camel_case(s["name"]),
            })
        return {
            "base_package": base_package,
            "semantic_sources": sources_ctx,
        }

    def _build_controller_context(
        self, enabled_sources: list[dict], base_package: str
    ) -> dict:
        """Build Jinja2 context for the RagIndexingController template."""
        all_sources = []
        for s in enabled_sources:
            all_sources.append({
                "name": s["name"],
                "type": s.get("type", "semantic"),
                "enabled": s.get("enabled", False),
                "security_mode": s.get("securityMode", "public"),
            })
        return {
            "base_package": base_package,
            "all_sources": all_sources,
        }

    def _render(self, template_name: str, ctx: dict) -> str:
        """Render a Jinja2 template under the ai/ prefix."""
        template = self.jinja_env.get_template(f"ai/{template_name}")
        return template.render(**ctx)

    @staticmethod
    def _get_enabled_sources(rag_sources: list[dict] | None) -> list[dict]:
        """Return only enabled RAG sources."""
        if not rag_sources:
            return []
        return [s for s in rag_sources if s.get("enabled", False)]
