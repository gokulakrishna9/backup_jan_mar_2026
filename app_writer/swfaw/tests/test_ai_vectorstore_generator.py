"""Unit tests for the AI VectorStoreGenerator.

Verifies that the VectorStoreGenerator produces correct Java source files
for the VectorStore interface, backend implementations, config, initializer,
and security filter builder.

Requirements: 8.1–8.21
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_vectorstore_generator import (
    VectorStoreGenerator,
    SUPPORTED_TYPES,
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
    return VectorStoreGenerator(jinja_env)


@pytest.fixture
def milvus_config():
    """Default Milvus vector store config."""
    return {
        "type": "milvus",
        "host": "milvus.example.com",
        "port": 19530,
        "collectionPrefix": "app_",
        "maxConnections": 10,
        "connectTimeoutMs": 5000,
        "idleTimeoutMs": 60000,
    }


@pytest.fixture
def qdrant_config():
    return {"type": "qdrant", "host": "qdrant.local", "port": 6333}


@pytest.fixture
def pgvector_config():
    return {"type": "pgvector", "host": "pg.local", "port": 5432}


@pytest.fixture
def in_memory_config():
    return {"type": "in_memory"}


@pytest.fixture
def semantic_rag_sources():
    """RAG sources with one enabled semantic source."""
    return [
        {"name": "courseEmbeddings", "type": "semantic", "enabled": True, "providerName": "mainGpt"},
        {"name": "articleSearch", "type": "heuristic", "enabled": True},
        {"name": "disabledSemantic", "type": "semantic", "enabled": False},
    ]


@pytest.fixture
def no_semantic_rag_sources():
    """RAG sources with no semantic sources."""
    return [
        {"name": "articleSearch", "type": "heuristic", "enabled": True},
    ]


@pytest.fixture
def output_dirs():
    return {
        "vectorstore": Path("com/example/app/ai/vectorstore"),
        "config": Path("com/example/app/ai/config"),
    }


BASE_PACKAGE = "com.example.app"


# ======================================================================
# Test: generate() — file count and skip logic
# ======================================================================

class TestVectorStoreGeneratorGenerate:
    """Tests for the generate() method's file output and skip logic."""

    def test_generates_six_files_for_milvus(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        results = generator.generate(milvus_config, semantic_rag_sources, BASE_PACKAGE, output_dirs)
        assert len(results) == 6

    def test_generates_six_files_for_qdrant(self, generator, qdrant_config, semantic_rag_sources, output_dirs):
        results = generator.generate(qdrant_config, semantic_rag_sources, BASE_PACKAGE, output_dirs)
        assert len(results) == 6

    def test_generates_six_files_for_pgvector(self, generator, pgvector_config, semantic_rag_sources, output_dirs):
        results = generator.generate(pgvector_config, semantic_rag_sources, BASE_PACKAGE, output_dirs)
        assert len(results) == 6

    def test_generates_six_files_for_in_memory(self, generator, in_memory_config, semantic_rag_sources, output_dirs):
        results = generator.generate(in_memory_config, semantic_rag_sources, BASE_PACKAGE, output_dirs)
        assert len(results) == 6

    def test_no_files_when_no_config_and_no_semantic_rag(self, generator, no_semantic_rag_sources, output_dirs):
        """Req 8.7: No vector store files when absent and no semantic RAG."""
        results = generator.generate(None, no_semantic_rag_sources, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_no_files_when_no_config_and_no_rag(self, generator, output_dirs):
        results = generator.generate(None, None, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_no_files_when_no_config_and_empty_rag(self, generator, output_dirs):
        results = generator.generate(None, [], BASE_PACKAGE, output_dirs)
        assert results == []

    def test_default_milvus_when_no_config_but_semantic_rag(self, generator, semantic_rag_sources, output_dirs):
        """Req 8.11: Default Milvus when vectorStore absent but semantic RAG exists."""
        results = generator.generate(None, semantic_rag_sources, BASE_PACKAGE, output_dirs)
        assert len(results) == 6
        filenames = [Path(fp).name for fp, _ in results]
        assert "MilvusVectorStore.java" in filenames

    def test_unsupported_type_raises_value_error(self, generator, semantic_rag_sources, output_dirs):
        """Req 8.12: Unsupported type raises ValueError."""
        bad_config = {"type": "weaviate"}
        with pytest.raises(ValueError, match="Unsupported vectorStore type 'weaviate'"):
            generator.generate(bad_config, semantic_rag_sources, BASE_PACKAGE, output_dirs)

    def test_all_content_is_nonempty(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        results = generator.generate(milvus_config, semantic_rag_sources, BASE_PACKAGE, output_dirs)
        for filepath, content in results:
            assert content.strip(), f"Empty content for {filepath}"

    def test_output_dirs_used_in_paths(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        results = generator.generate(milvus_config, semantic_rag_sources, BASE_PACKAGE, output_dirs)
        for filepath, _ in results:
            assert filepath.startswith("com/example/app/ai/")

    def test_correct_filenames_milvus(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        results = generator.generate(milvus_config, semantic_rag_sources, BASE_PACKAGE, output_dirs)
        filenames = {Path(fp).name for fp, _ in results}
        expected = {
            "VectorStore.java",
            "VectorSearchResult.java",
            "MilvusVectorStore.java",
            "VectorStoreConfig.java",
            "VectorStoreInitializer.java",
            "VectorSecurityFilterBuilder.java",
        }
        assert filenames == expected

    def test_correct_filenames_in_memory(self, generator, in_memory_config, semantic_rag_sources, output_dirs):
        results = generator.generate(in_memory_config, semantic_rag_sources, BASE_PACKAGE, output_dirs)
        filenames = {Path(fp).name for fp, _ in results}
        assert "InMemoryVectorStore.java" in filenames
        assert "MilvusVectorStore.java" not in filenames


# ======================================================================
# Test: VectorStore interface template
# ======================================================================

class TestVectorStoreInterface:
    """Tests for the generated VectorStore interface."""

    def _get_interface(self, generator, config, rag_sources, output_dirs):
        results = generator.generate(config, rag_sources, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if "VectorStore.java" == Path(fp).name)

    def test_package_declaration(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_interface(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.vectorstore;" in content

    def test_is_interface(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_interface(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "public interface VectorStore" in content

    def test_store_method(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        """Req 8.1: store(...) returning Mono<Void>."""
        content = self._get_interface(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "Mono<Void> store(" in content

    def test_search_method(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        """Req 8.1: search(...) returning Flux<VectorSearchResult>."""
        content = self._get_interface(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "Flux<VectorSearchResult> search(" in content

    def test_delete_method(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        """Req 8.1: delete(...) returning Mono<Void>."""
        content = self._get_interface(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "Mono<Void> delete(" in content

    def test_delete_by_filter_method(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        """Req 8.1: deleteByFilter(...) returning Mono<Long>."""
        content = self._get_interface(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "Mono<Long> deleteByFilter(" in content

    def test_collection_exists_method(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        """Req 8.1: collectionExists(...) returning Mono<Boolean>."""
        content = self._get_interface(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "Mono<Boolean> collectionExists(" in content

    def test_reactive_imports(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        """Req 8.18: All operations use reactive types."""
        content = self._get_interface(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "import reactor.core.publisher.Flux;" in content
        assert "import reactor.core.publisher.Mono;" in content


# ======================================================================
# Test: VectorSearchResult record
# ======================================================================

class TestVectorSearchResult:
    """Tests for the generated VectorSearchResult record."""

    def _get_result(self, generator, config, rag_sources, output_dirs):
        results = generator.generate(config, rag_sources, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if "VectorSearchResult.java" == Path(fp).name)

    def test_is_record(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_result(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "public record VectorSearchResult(" in content

    def test_has_id_field(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        """Req 8.2."""
        content = self._get_result(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "String id" in content

    def test_has_text_field(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_result(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "String text" in content

    def test_has_score_field(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_result(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "double score" in content

    def test_has_metadata_field(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_result(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "Map<String, Object> metadata" in content


# ======================================================================
# Test: Backend implementations
# ======================================================================

class TestMilvusVectorStore:
    """Tests for the generated MilvusVectorStore implementation."""

    def _get_milvus(self, generator, config, rag_sources, output_dirs):
        results = generator.generate(config, rag_sources, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if "MilvusVectorStore.java" == Path(fp).name)

    def test_implements_interface(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_milvus(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "implements VectorStore" in content

    def test_component_annotation(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_milvus(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "@Component" in content

    def test_milvus_sdk_import(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        """Req 8.3: Uses Milvus Java SDK."""
        content = self._get_milvus(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "import io.milvus" in content

    def test_reactive_types(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        """Req 8.18."""
        content = self._get_milvus(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "Mono<Void> store(" in content
        assert "Flux<VectorSearchResult> search(" in content

    def test_security_filter_expression(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        """Req 8.15: Milvus expression filter for security."""
        content = self._get_milvus(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "buildMilvusFilter" in content

    def test_connect_timeout_from_config(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_milvus(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "connect-timeout-ms" in content


class TestQdrantVectorStore:
    def _get_qdrant(self, generator, config, rag_sources, output_dirs):
        results = generator.generate(config, rag_sources, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if "QdrantVectorStore.java" == Path(fp).name)

    def test_implements_interface(self, generator, qdrant_config, semantic_rag_sources, output_dirs):
        """Req 8.4: Qdrant placeholder."""
        content = self._get_qdrant(generator, qdrant_config, semantic_rag_sources, output_dirs)
        assert "implements VectorStore" in content

    def test_placeholder_throws(self, generator, qdrant_config, semantic_rag_sources, output_dirs):
        content = self._get_qdrant(generator, qdrant_config, semantic_rag_sources, output_dirs)
        assert "UnsupportedOperationException" in content


class TestPgVectorStore:
    def _get_pgvector(self, generator, config, rag_sources, output_dirs):
        results = generator.generate(config, rag_sources, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if "PgVectorStore.java" == Path(fp).name)

    def test_implements_interface(self, generator, pgvector_config, semantic_rag_sources, output_dirs):
        """Req 8.5: PgVector placeholder."""
        content = self._get_pgvector(generator, pgvector_config, semantic_rag_sources, output_dirs)
        assert "implements VectorStore" in content

    def test_placeholder_throws(self, generator, pgvector_config, semantic_rag_sources, output_dirs):
        content = self._get_pgvector(generator, pgvector_config, semantic_rag_sources, output_dirs)
        assert "UnsupportedOperationException" in content


class TestInMemoryVectorStore:
    def _get_inmem(self, generator, config, rag_sources, output_dirs):
        results = generator.generate(config, rag_sources, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if "InMemoryVectorStore.java" == Path(fp).name)

    def test_implements_interface(self, generator, in_memory_config, semantic_rag_sources, output_dirs):
        """Req 8.6: InMemory with ConcurrentHashMap."""
        content = self._get_inmem(generator, in_memory_config, semantic_rag_sources, output_dirs)
        assert "implements VectorStore" in content

    def test_concurrent_hash_map(self, generator, in_memory_config, semantic_rag_sources, output_dirs):
        content = self._get_inmem(generator, in_memory_config, semantic_rag_sources, output_dirs)
        assert "ConcurrentHashMap" in content

    def test_cosine_similarity(self, generator, in_memory_config, semantic_rag_sources, output_dirs):
        content = self._get_inmem(generator, in_memory_config, semantic_rag_sources, output_dirs)
        assert "cosineSimilarity" in content


# ======================================================================
# Test: VectorStoreConfig
# ======================================================================

class TestVectorStoreConfig:
    def _get_config(self, generator, config, rag_sources, output_dirs):
        results = generator.generate(config, rag_sources, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if "VectorStoreConfig.java" == Path(fp).name)

    def test_configuration_annotation(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_config(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "@Configuration" in content

    def test_conditional_on_property(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        """Req 8.7: @ConditionalOnProperty to select implementation."""
        content = self._get_config(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "@ConditionalOnProperty" in content

    def test_milvus_bean(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_config(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "milvusVectorStore" in content

    def test_in_memory_bean(self, generator, in_memory_config, semantic_rag_sources, output_dirs):
        content = self._get_config(generator, in_memory_config, semantic_rag_sources, output_dirs)
        assert "inMemoryVectorStore" in content

    def test_config_package(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_config(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.config;" in content


# ======================================================================
# Test: VectorStoreInitializer
# ======================================================================

class TestVectorStoreInitializer:
    def _get_initializer(self, generator, config, rag_sources, output_dirs):
        results = generator.generate(config, rag_sources, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if "VectorStoreInitializer.java" == Path(fp).name)

    def test_component_annotation(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_initializer(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "@Component" in content

    def test_application_ready_event(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        """Req 8.8: Creates collections on startup."""
        content = self._get_initializer(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "ApplicationReadyEvent" in content

    def test_collection_prefix(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_initializer(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "collection-prefix" in content

    def test_semantic_source_names_present(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_initializer(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert '"courseEmbeddings"' in content

    def test_no_disabled_sources(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_initializer(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "disabledSemantic" not in content


# ======================================================================
# Test: VectorSecurityFilterBuilder
# ======================================================================

class TestVectorSecurityFilterBuilder:
    def _get_builder(self, generator, config, rag_sources, output_dirs):
        results = generator.generate(config, rag_sources, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if "VectorSecurityFilterBuilder.java" == Path(fp).name)

    def test_component_annotation(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_builder(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "@Component" in content

    def test_build_filter_method(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        """Req 8.17: Constructs filters from Authentication objects."""
        content = self._get_builder(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert "buildFilter(Authentication" in content

    def test_user_id_in_filter(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        """Req 8.13: Includes user_id in filter."""
        content = self._get_builder(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert '"user_id"' in content

    def test_security_groups_in_filter(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        """Req 8.13: Includes security_groups in filter."""
        content = self._get_builder(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert '"security_groups"' in content

    def test_public_returns_null(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        """Req 8.16: Returns null for public sources."""
        content = self._get_builder(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert '"public"' in content
        assert "return null" in content

    def test_package_declaration(self, generator, milvus_config, semantic_rag_sources, output_dirs):
        content = self._get_builder(generator, milvus_config, semantic_rag_sources, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.vectorstore;" in content


# ======================================================================
# Test: Helper methods
# ======================================================================

class TestHelperMethods:
    def test_has_semantic_rag_true(self):
        sources = [{"name": "s1", "type": "semantic", "enabled": True}]
        assert VectorStoreGenerator._has_semantic_rag(sources) is True

    def test_has_semantic_rag_false_disabled(self):
        sources = [{"name": "s1", "type": "semantic", "enabled": False}]
        assert VectorStoreGenerator._has_semantic_rag(sources) is False

    def test_has_semantic_rag_false_heuristic(self):
        sources = [{"name": "s1", "type": "heuristic", "enabled": True}]
        assert VectorStoreGenerator._has_semantic_rag(sources) is False

    def test_has_semantic_rag_none(self):
        assert VectorStoreGenerator._has_semantic_rag(None) is False

    def test_has_semantic_rag_empty(self):
        assert VectorStoreGenerator._has_semantic_rag([]) is False

    def test_get_semantic_source_names(self):
        sources = [
            {"name": "a", "type": "semantic", "enabled": True},
            {"name": "b", "type": "semantic", "enabled": False},
            {"name": "c", "type": "heuristic", "enabled": True},
        ]
        assert VectorStoreGenerator._get_semantic_source_names(sources) == ["a"]

    def test_get_semantic_source_names_empty(self):
        assert VectorStoreGenerator._get_semantic_source_names(None) == []

    def test_merge_defaults_none(self):
        merged = VectorStoreGenerator._merge_defaults(None)
        assert merged["type"] == "milvus"
        assert merged["host"] == "localhost"
        assert merged["collectionPrefix"] == "ai_"

    def test_merge_defaults_overrides(self):
        merged = VectorStoreGenerator._merge_defaults({"type": "qdrant", "host": "custom"})
        assert merged["type"] == "qdrant"
        assert merged["host"] == "custom"
        assert merged["port"] == 19530  # default preserved

    def test_impl_for_type_all_supported(self):
        for t in SUPPORTED_TYPES:
            filename, template = VectorStoreGenerator._impl_for_type(t)
            assert filename.endswith(".java")
            assert template.endswith(".j2")
