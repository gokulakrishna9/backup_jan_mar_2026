"""Vector Store sub-generator for the AI Layer.

Generates the VectorStore interface, backend-specific implementations
(Milvus, Qdrant placeholder, PgVector placeholder, InMemory),
VectorStoreConfig, VectorStoreInitializer, and VectorSecurityFilterBuilder.

Requirements: 8.1–8.21
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2

# Supported vector store types (Req 8.3–8.6, 8.12)
SUPPORTED_TYPES = {"milvus", "qdrant", "pgvector", "in_memory"}

# Default vector store settings (Req 1.9)
_DEFAULTS = {
    "type": "milvus",
    "host": "localhost",
    "port": 19530,
    "collectionPrefix": "ai_",
    "maxConnections": 10,
    "connectTimeoutMs": 5000,
    "idleTimeoutMs": 60000,
}


class VectorStoreGenerator:
    """Generates vector store Java files from the AI_Layer definition."""

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        vector_store_config: dict | None,
        rag_sources: list[dict] | None,
        base_package: str,
        output_dirs: dict[str, Path],
    ) -> list[tuple[str, str]]:
        """Generate vector store Java files.

        Returns a list of ``(filepath, content)`` tuples where *filepath* is
        relative to the project source root.

        Req 8.7: When ``vectorStore`` is absent and no semantic RAG sources
        exist, no vector store files are generated.
        Req 8.11: When ``vectorStore`` is absent but semantic RAG sources
        exist, use default Milvus settings.
        Req 8.12: Raises ``ValueError`` for unsupported types.
        """
        has_semantic_rag = self._has_semantic_rag(rag_sources)

        # When vectorStore is absent/None and no semantic RAG → skip
        if vector_store_config is None and not has_semantic_rag:
            return []

        # Merge with defaults (Req 8.11)
        vs_cfg = self._merge_defaults(vector_store_config)

        # Validate type (Req 8.12)
        vs_type = vs_cfg.get("type", "milvus")
        if vs_type not in SUPPORTED_TYPES:
            raise ValueError(
                f"Unsupported vectorStore type '{vs_type}'. "
                f"Supported types: {', '.join(sorted(SUPPORTED_TYPES))}"
            )

        results: list[tuple[str, str]] = []

        vectorstore_dir = output_dirs.get("vectorstore", Path("ai/vectorstore"))
        config_dir = output_dirs.get("config", Path("ai/config"))

        # Collect semantic RAG source names for the initializer
        semantic_source_names = self._get_semantic_source_names(rag_sources)

        # Build shared template context
        ctx = self._build_template_context(vs_cfg, base_package, semantic_source_names)

        # 1. VectorStore interface (Req 8.1)
        results.append((
            str(vectorstore_dir / "VectorStore.java"),
            self._render("vectorstore/vector_store_interface.java.j2", ctx),
        ))

        # 2. VectorSearchResult record (Req 8.2)
        results.append((
            str(vectorstore_dir / "VectorSearchResult.java"),
            self._render("vectorstore/vector_search_result.java.j2", ctx),
        ))

        # 3. Backend implementation (Req 8.3–8.6)
        impl_file, impl_template = self._impl_for_type(vs_type)
        results.append((
            str(vectorstore_dir / impl_file),
            self._render(impl_template, ctx),
        ))

        # 4. VectorStoreConfig (Req 8.7)
        results.append((
            str(config_dir / "VectorStoreConfig.java"),
            self._render("vectorstore/vector_store_config.java.j2", ctx),
        ))

        # 5. VectorStoreInitializer (Req 8.8)
        results.append((
            str(vectorstore_dir / "VectorStoreInitializer.java"),
            self._render("vectorstore/vector_store_initializer.java.j2", ctx),
        ))

        # 6. VectorSecurityFilterBuilder (Req 8.17)
        results.append((
            str(vectorstore_dir / "VectorSecurityFilterBuilder.java"),
            self._render("vectorstore/vector_security_filter_builder.java.j2", ctx),
        ))

        return results

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_template_context(
        self,
        vs_cfg: dict,
        base_package: str,
        semantic_source_names: list[str],
    ) -> dict:
        """Build the Jinja2 template context for vector store templates."""
        # Build Java source literal for semantic source names list
        if semantic_source_names:
            names_java = ", ".join(f'"{n}"' for n in semantic_source_names)
        else:
            names_java = ""

        return {
            "base_package": base_package,
            "vector_store_type": vs_cfg.get("type", "milvus"),
            "host": vs_cfg.get("host", "localhost"),
            "port": vs_cfg.get("port", 19530),
            "api_key": vs_cfg.get("apiKey"),
            "database": vs_cfg.get("database"),
            "collection_prefix": vs_cfg.get("collectionPrefix", "ai_"),
            "max_connections": vs_cfg.get("maxConnections", 10),
            "connect_timeout_ms": vs_cfg.get("connectTimeoutMs", 5000),
            "idle_timeout_ms": vs_cfg.get("idleTimeoutMs", 60000),
            "semantic_source_names": semantic_source_names,
            "semantic_source_names_java": names_java,
        }

    def _render(self, template_name: str, ctx: dict) -> str:
        """Render a Jinja2 template under the ai/ prefix."""
        template = self.jinja_env.get_template(f"ai/{template_name}")
        return template.render(**ctx)

    @staticmethod
    def _impl_for_type(vs_type: str) -> tuple[str, str]:
        """Return (filename, template_path) for the given vector store type."""
        mapping = {
            "milvus": ("MilvusVectorStore.java", "vectorstore/milvus_vector_store.java.j2"),
            "qdrant": ("QdrantVectorStore.java", "vectorstore/qdrant_vector_store.java.j2"),
            "pgvector": ("PgVectorStore.java", "vectorstore/pgvector_vector_store.java.j2"),
            "in_memory": ("InMemoryVectorStore.java", "vectorstore/in_memory_vector_store.java.j2"),
        }
        return mapping[vs_type]

    @staticmethod
    def _merge_defaults(config: dict | None) -> dict:
        """Merge user config with defaults. Returns a new dict."""
        merged = dict(_DEFAULTS)
        if config:
            merged.update({k: v for k, v in config.items() if v is not None})
        return merged

    @staticmethod
    def _has_semantic_rag(rag_sources: list[dict] | None) -> bool:
        """Check if any enabled semantic RAG source exists."""
        if not rag_sources:
            return False
        return any(
            s.get("type") == "semantic" and s.get("enabled", False)
            for s in rag_sources
        )

    @staticmethod
    def _get_semantic_source_names(rag_sources: list[dict] | None) -> list[str]:
        """Return names of all enabled semantic RAG sources."""
        if not rag_sources:
            return []
        return [
            s["name"]
            for s in rag_sources
            if s.get("type") == "semantic" and s.get("enabled", False) and "name" in s
        ]
