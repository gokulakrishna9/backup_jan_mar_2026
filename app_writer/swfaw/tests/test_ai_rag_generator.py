"""Unit tests for the AI RagGenerator.

Verifies that the RagGenerator produces correct Java source files
for SemanticRagService, HeuristicRagService, RagContextInjector,
RagIndexingService, RagIndexingController, and RagResultDTO.

Requirements: 9.1–9.15
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_rag_generator import (
    RagGenerator,
    _pascal_case,
    _camel_case,
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
    return RagGenerator(jinja_env)


@pytest.fixture
def semantic_source():
    """A single enabled semantic RAG source."""
    return {
        "name": "courseEmbeddings",
        "type": "semantic",
        "enabled": True,
        "providerName": "mainGpt",
        "chunkSize": 1024,
        "chunkOverlap": 100,
        "topK": 10,
        "similarityThreshold": 0.75,
        "securityMode": "public",
        "targets": [{"entityName": "Course", "fields": ["description"]}],
    }


@pytest.fixture
def heuristic_source():
    """A single enabled heuristic RAG source."""
    return {
        "name": "articleSearch",
        "type": "heuristic",
        "enabled": True,
        "maxResults": 20,
        "securityMode": "public",
        "rules": [
            {
                "ruleType": "keyword",
                "field": "title",
                "weight": 2.0,
                "targetTable": "article",
                "entityType": "Article",
            },
            {
                "ruleType": "field_match",
                "field": "category",
                "pattern": "%{query}%",
                "weight": 1.0,
                "targetTable": "article",
                "entityType": "Article",
            },
        ],
        "targets": [{"entityName": "Article", "fields": ["title", "body"]}],
    }


@pytest.fixture
def restricted_semantic_source():
    """A semantic source with role_restricted security."""
    return {
        "name": "secureData",
        "type": "semantic",
        "enabled": True,
        "providerName": "secureGpt",
        "securityMode": "role_restricted",
        "chunkSize": 512,
        "chunkOverlap": 50,
        "topK": 5,
        "similarityThreshold": 0.8,
    }


@pytest.fixture
def disabled_source():
    """A disabled RAG source."""
    return {
        "name": "disabledSource",
        "type": "semantic",
        "enabled": False,
        "providerName": "mainGpt",
    }


@pytest.fixture
def mixed_sources(semantic_source, heuristic_source, disabled_source):
    """Mix of enabled semantic, heuristic, and disabled sources."""
    return [semantic_source, heuristic_source, disabled_source]


@pytest.fixture
def vector_store_config():
    return {
        "type": "milvus",
        "collectionPrefix": "app_",
    }


@pytest.fixture
def output_dirs():
    return {
        "rag": Path("com/example/app/ai/rag"),
        "controller": Path("com/example/app/ai/controller"),
    }


BASE_PACKAGE = "com.example.app"


# ======================================================================
# Test: Helper functions
# ======================================================================

class TestHelperFunctions:
    def test_pascal_case_camel(self):
        assert _pascal_case("courseEmbeddings") == "CourseEmbeddings"

    def test_pascal_case_snake(self):
        assert _pascal_case("course_embeddings") == "CourseEmbeddings"

    def test_pascal_case_single(self):
        assert _pascal_case("course") == "Course"

    def test_pascal_case_empty(self):
        assert _pascal_case("") == ""

    def test_camel_case(self):
        assert _camel_case("CourseEmbeddings") == "courseEmbeddings"

    def test_camel_case_snake(self):
        assert _camel_case("course_embeddings") == "courseEmbeddings"

    def test_get_enabled_sources_none(self):
        assert RagGenerator._get_enabled_sources(None) == []

    def test_get_enabled_sources_empty(self):
        assert RagGenerator._get_enabled_sources([]) == []

    def test_get_enabled_sources_filters_disabled(self, disabled_source, semantic_source):
        result = RagGenerator._get_enabled_sources([disabled_source, semantic_source])
        assert len(result) == 1
        assert result[0]["name"] == "courseEmbeddings"


# ======================================================================
# Test: generate() — skip logic and file counts
# ======================================================================

class TestRagGeneratorGenerate:
    """Tests for the generate() method's file output and skip logic."""

    def test_no_files_when_no_sources(self, generator, output_dirs):
        """Req 9.1: No RAG files when ragSources is None."""
        results = generator.generate(None, None, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_no_files_when_empty_sources(self, generator, output_dirs):
        results = generator.generate([], None, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_no_files_when_all_disabled(self, generator, disabled_source, output_dirs):
        results = generator.generate([disabled_source], None, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_semantic_only_generates_correct_count(
        self, generator, semantic_source, vector_store_config, output_dirs
    ):
        """Semantic source: RagResultDTO + SemanticRagService + RagContextInjector
        + RagIndexingService + RagIndexingController = 5 files."""
        results = generator.generate(
            [semantic_source], vector_store_config, BASE_PACKAGE, output_dirs
        )
        assert len(results) == 5

    def test_heuristic_only_generates_correct_count(
        self, generator, heuristic_source, output_dirs
    ):
        """Heuristic source: RagResultDTO + HeuristicRagService + RagContextInjector
        + RagIndexingController = 4 files (no RagIndexingService without semantic)."""
        results = generator.generate(
            [heuristic_source], None, BASE_PACKAGE, output_dirs
        )
        assert len(results) == 4

    def test_mixed_sources_generate_correct_count(
        self, generator, mixed_sources, vector_store_config, output_dirs
    ):
        """Mixed: RagResultDTO + SemanticRagService + HeuristicRagService
        + RagContextInjector + RagIndexingService + RagIndexingController = 6 files."""
        results = generator.generate(
            mixed_sources, vector_store_config, BASE_PACKAGE, output_dirs
        )
        assert len(results) == 6

    def test_all_content_is_nonempty(
        self, generator, mixed_sources, vector_store_config, output_dirs
    ):
        results = generator.generate(
            mixed_sources, vector_store_config, BASE_PACKAGE, output_dirs
        )
        for filepath, content in results:
            assert content.strip(), f"Empty content for {filepath}"

    def test_output_dirs_used_in_paths(
        self, generator, semantic_source, vector_store_config, output_dirs
    ):
        results = generator.generate(
            [semantic_source], vector_store_config, BASE_PACKAGE, output_dirs
        )
        for filepath, _ in results:
            assert filepath.startswith("com/example/app/ai/")

    def test_correct_filenames_semantic(
        self, generator, semantic_source, vector_store_config, output_dirs
    ):
        results = generator.generate(
            [semantic_source], vector_store_config, BASE_PACKAGE, output_dirs
        )
        filenames = {Path(fp).name for fp, _ in results}
        expected = {
            "RagResultDTO.java",
            "CourseEmbeddingsSemanticRagService.java",
            "RagContextInjector.java",
            "RagIndexingService.java",
            "RagIndexingController.java",
        }
        assert filenames == expected

    def test_correct_filenames_heuristic(
        self, generator, heuristic_source, output_dirs
    ):
        results = generator.generate(
            [heuristic_source], None, BASE_PACKAGE, output_dirs
        )
        filenames = {Path(fp).name for fp, _ in results}
        expected = {
            "RagResultDTO.java",
            "ArticleSearchHeuristicRagService.java",
            "RagContextInjector.java",
            "RagIndexingController.java",
        }
        assert filenames == expected

    def test_correct_filenames_mixed(
        self, generator, mixed_sources, vector_store_config, output_dirs
    ):
        results = generator.generate(
            mixed_sources, vector_store_config, BASE_PACKAGE, output_dirs
        )
        filenames = {Path(fp).name for fp, _ in results}
        assert "CourseEmbeddingsSemanticRagService.java" in filenames
        assert "ArticleSearchHeuristicRagService.java" in filenames
        assert "RagResultDTO.java" in filenames
        assert "RagContextInjector.java" in filenames
        assert "RagIndexingService.java" in filenames
        assert "RagIndexingController.java" in filenames


# ======================================================================
# Test: RagResultDTO template
# ======================================================================

class TestRagResultDTO:
    """Tests for the generated RagResultDTO record."""

    def _get_dto(self, generator, sources, vs_config, output_dirs):
        results = generator.generate(sources, vs_config, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if Path(fp).name == "RagResultDTO.java")

    def test_is_record(self, generator, semantic_source, vector_store_config, output_dirs):
        content = self._get_dto(generator, [semantic_source], vector_store_config, output_dirs)
        assert "public record RagResultDTO(" in content

    def test_package_declaration(self, generator, semantic_source, vector_store_config, output_dirs):
        content = self._get_dto(generator, [semantic_source], vector_store_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.rag;" in content

    def test_has_source_text(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.6: sourceText field."""
        content = self._get_dto(generator, [semantic_source], vector_store_config, output_dirs)
        assert "String sourceText" in content

    def test_has_source_name(self, generator, semantic_source, vector_store_config, output_dirs):
        content = self._get_dto(generator, [semantic_source], vector_store_config, output_dirs)
        assert "String sourceName" in content

    def test_has_entity_type(self, generator, semantic_source, vector_store_config, output_dirs):
        content = self._get_dto(generator, [semantic_source], vector_store_config, output_dirs)
        assert "String entityType" in content

    def test_has_entity_id(self, generator, semantic_source, vector_store_config, output_dirs):
        content = self._get_dto(generator, [semantic_source], vector_store_config, output_dirs)
        assert "Long entityId" in content

    def test_has_score(self, generator, semantic_source, vector_store_config, output_dirs):
        content = self._get_dto(generator, [semantic_source], vector_store_config, output_dirs)
        assert "double score" in content

    def test_has_metadata(self, generator, semantic_source, vector_store_config, output_dirs):
        content = self._get_dto(generator, [semantic_source], vector_store_config, output_dirs)
        assert "Map<String, Object> metadata" in content


# ======================================================================
# Test: SemanticRagService template
# ======================================================================

class TestSemanticRagService:
    """Tests for the generated SemanticRagService."""

    def _get_service(self, generator, sources, vs_config, output_dirs, name="CourseEmbeddings"):
        results = generator.generate(sources, vs_config, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if Path(fp).name == f"{name}SemanticRagService.java")

    def test_package_declaration(self, generator, semantic_source, vector_store_config, output_dirs):
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.rag;" in content

    def test_service_annotation(self, generator, semantic_source, vector_store_config, output_dirs):
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "@Service" in content

    def test_class_name(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.1: <SourceNamePascalCase>SemanticRagService."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "public class CourseEmbeddingsSemanticRagService" in content

    def test_embedding_model_qualifier(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.2: Injects EmbeddingModel via @Qualifier."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert '@Qualifier("mainGpt")' in content
        assert "EmbeddingModel embeddingModel" in content

    def test_vector_store_injection(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.2: Injects VectorStore."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "VectorStore vectorStore" in content

    def test_search_method(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.1: search method returning Flux<RagResultDTO>."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "Flux<RagResultDTO> search(" in content

    def test_similarity_threshold_filter(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.3: Filters by similarityThreshold."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "similarityThreshold" in content
        assert ".filter(" in content

    def test_index_entity_method(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.1: indexEntity method."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "Mono<Void> indexEntity(" in content

    def test_delete_entity_embeddings_method(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.1: deleteEntityEmbeddings method."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "Mono<Void> deleteEntityEmbeddings(" in content

    def test_reindex_all_method(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.1: reindexAll method."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "Mono<Void> reindexAll()" in content

    def test_chunk_text_method(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.10: Text chunking with sliding window."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "chunkText(" in content

    def test_collection_prefix_from_config(self, generator, semantic_source, vector_store_config, output_dirs):
        """Uses collection prefix from vector store config."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "app_courseEmbeddings" in content

    def test_config_values(self, generator, semantic_source, vector_store_config, output_dirs):
        """Semantic config values are injected."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "chunk-size:1024" in content
        assert "chunk-overlap:100" in content
        assert "top-k:10" in content
        assert "similarity-threshold:0.75" in content

    def test_public_security_no_restriction(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 8.16: Public sources don't restrict searches."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        # Public mode should NOT have the role_restricted guard
        assert "No security context for role_restricted" not in content

    def test_role_restricted_security(self, generator, restricted_semantic_source, vector_store_config, output_dirs):
        """Req 8.13/8.14: role_restricted sources require security filter."""
        content = self._get_service(
            generator, [restricted_semantic_source], vector_store_config, output_dirs,
            name="SecureData"
        )
        assert "No security context for role_restricted" in content
        assert "return Flux.empty()" in content


# ======================================================================
# Test: HeuristicRagService template
# ======================================================================

class TestHeuristicRagService:
    """Tests for the generated HeuristicRagService."""

    def _get_service(self, generator, sources, output_dirs):
        results = generator.generate(sources, None, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if "HeuristicRagService.java" in Path(fp).name)

    def test_package_declaration(self, generator, heuristic_source, output_dirs):
        content = self._get_service(generator, [heuristic_source], output_dirs)
        assert f"package {BASE_PACKAGE}.ai.rag;" in content

    def test_service_annotation(self, generator, heuristic_source, output_dirs):
        content = self._get_service(generator, [heuristic_source], output_dirs)
        assert "@Service" in content

    def test_class_name(self, generator, heuristic_source, output_dirs):
        """Req 9.4: <SourceNamePascalCase>HeuristicRagService."""
        content = self._get_service(generator, [heuristic_source], output_dirs)
        assert "public class ArticleSearchHeuristicRagService" in content

    def test_search_method(self, generator, heuristic_source, output_dirs):
        """Req 9.4: search method returning Flux<RagResultDTO>."""
        content = self._get_service(generator, [heuristic_source], output_dirs)
        assert "Flux<RagResultDTO> search(" in content

    def test_no_llm_dependency(self, generator, heuristic_source, output_dirs):
        """Req 9.5: No LLM provider dependency."""
        content = self._get_service(generator, [heuristic_source], output_dirs)
        assert "EmbeddingModel" not in content
        assert "ChatClient" not in content

    def test_database_client_injection(self, generator, heuristic_source, output_dirs):
        """Uses DatabaseClient for SQL-based retrieval."""
        content = self._get_service(generator, [heuristic_source], output_dirs)
        assert "DatabaseClient databaseClient" in content

    def test_keyword_rule(self, generator, heuristic_source, output_dirs):
        """Req 9.5: keyword rule type with FULLTEXT."""
        content = self._get_service(generator, [heuristic_source], output_dirs)
        assert "MATCH" in content
        assert "BOOLEAN MODE" in content

    def test_field_match_rule(self, generator, heuristic_source, output_dirs):
        """Req 9.5: field_match rule type with LIKE."""
        content = self._get_service(generator, [heuristic_source], output_dirs)
        assert "LIKE" in content

    def test_weighted_scoring(self, generator, heuristic_source, output_dirs):
        """Req 9.5: Weighted scoring and sorting."""
        content = self._get_service(generator, [heuristic_source], output_dirs)
        assert ".sort(" in content
        assert "2.0" in content  # weight from keyword rule

    def test_max_results_limit(self, generator, heuristic_source, output_dirs):
        """Limits results to maxResults."""
        content = self._get_service(generator, [heuristic_source], output_dirs)
        assert ".take(maxResults)" in content

    def test_multiple_rules_merged(self, generator, heuristic_source, output_dirs):
        """Multiple rules are merged via Flux.merge."""
        content = self._get_service(generator, [heuristic_source], output_dirs)
        assert "Flux.merge(" in content
        assert "executeRule1(" in content
        assert "executeRule2(" in content


# ======================================================================
# Test: RagContextInjector template
# ======================================================================

class TestRagContextInjector:
    """Tests for the generated RagContextInjector."""

    def _get_injector(self, generator, sources, vs_config, output_dirs):
        results = generator.generate(sources, vs_config, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if Path(fp).name == "RagContextInjector.java")

    def test_package_declaration(self, generator, semantic_source, vector_store_config, output_dirs):
        content = self._get_injector(generator, [semantic_source], vector_store_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.rag;" in content

    def test_component_annotation(self, generator, semantic_source, vector_store_config, output_dirs):
        content = self._get_injector(generator, [semantic_source], vector_store_config, output_dirs)
        assert "@Component" in content

    def test_inject_context_method(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.8: injectContext method."""
        content = self._get_injector(generator, [semantic_source], vector_store_config, output_dirs)
        assert "List<Message> injectContext(" in content

    def test_source_attribution(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.8: Prepends context with source attribution."""
        content = self._get_injector(generator, [semantic_source], vector_store_config, output_dirs)
        assert "Source:" in content
        assert "Score:" in content

    def test_zero_results_warning(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.9: Logs warning when RAG returns zero results."""
        content = self._get_injector(generator, [semantic_source], vector_store_config, output_dirs)
        assert "RAG returned zero results" in content

    def test_system_message_injection(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.8: Injects into system role entry."""
        content = self._get_injector(generator, [semantic_source], vector_store_config, output_dirs)
        assert "SystemMessage" in content

    def test_extract_original_prompt(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.15: Round-trip property support."""
        content = self._get_injector(generator, [semantic_source], vector_store_config, output_dirs)
        assert "extractOriginalPrompt(" in content


# ======================================================================
# Test: RagIndexingService template
# ======================================================================

class TestRagIndexingService:
    """Tests for the generated RagIndexingService."""

    def _get_service(self, generator, sources, vs_config, output_dirs):
        results = generator.generate(sources, vs_config, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if Path(fp).name == "RagIndexingService.java")

    def test_package_declaration(self, generator, semantic_source, vector_store_config, output_dirs):
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.rag;" in content

    def test_service_annotation(self, generator, semantic_source, vector_store_config, output_dirs):
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "@Service" in content

    def test_index_entity_method(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.10: indexEntity method."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "Mono<Void> indexEntity(" in content

    def test_reindex_source_method(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.10: reindexSource method."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "Mono<Void> reindexSource(" in content

    def test_index_document_method(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.10: indexDocument method."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "Mono<Void> indexDocument(" in content

    def test_chunk_text_method(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.10: chunkText with sliding window."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "List<String> chunkText(" in content

    def test_on_entity_saved_method(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.11: Entity event listener for async re-indexing."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "onEntitySaved(" in content
        assert "Schedulers.boundedElastic()" in content

    def test_semantic_source_injection(self, generator, semantic_source, vector_store_config, output_dirs):
        """Injects per-source SemanticRagService."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert "CourseEmbeddingsSemanticRagService" in content

    def test_switch_routing(self, generator, semantic_source, vector_store_config, output_dirs):
        """Routes to correct source by name."""
        content = self._get_service(generator, [semantic_source], vector_store_config, output_dirs)
        assert '"courseEmbeddings"' in content


# ======================================================================
# Test: RagIndexingController template
# ======================================================================

class TestRagIndexingController:
    """Tests for the generated RagIndexingController."""

    def _get_controller(self, generator, sources, vs_config, output_dirs):
        results = generator.generate(sources, vs_config, BASE_PACKAGE, output_dirs)
        return next(c for fp, c in results if Path(fp).name == "RagIndexingController.java")

    def test_package_declaration(self, generator, semantic_source, vector_store_config, output_dirs):
        content = self._get_controller(generator, [semantic_source], vector_store_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.controller;" in content

    def test_rest_controller_annotation(self, generator, semantic_source, vector_store_config, output_dirs):
        content = self._get_controller(generator, [semantic_source], vector_store_config, output_dirs)
        assert "@RestController" in content

    def test_base_path(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.12: Base path /api/ai/rag."""
        content = self._get_controller(generator, [semantic_source], vector_store_config, output_dirs)
        assert '@RequestMapping("/api/ai/rag")' in content

    def test_list_sources_endpoint(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.12: GET /sources."""
        content = self._get_controller(generator, [semantic_source], vector_store_config, output_dirs)
        assert '@GetMapping("/sources")' in content
        assert "listSources()" in content

    def test_source_status_endpoint(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.12: GET /{sourceName}/status."""
        content = self._get_controller(generator, [semantic_source], vector_store_config, output_dirs)
        assert "/{sourceName}/status" in content
        assert "getSourceStatus(" in content

    def test_reindex_endpoint(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.12: POST /{sourceName}/reindex."""
        content = self._get_controller(generator, [semantic_source], vector_store_config, output_dirs)
        assert "/{sourceName}/reindex" in content
        assert "reindexSource(" in content

    def test_index_entity_endpoint(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.12: POST /{sourceName}/index-entity."""
        content = self._get_controller(generator, [semantic_source], vector_store_config, output_dirs)
        assert "/{sourceName}/index-entity" in content
        assert "indexEntity(" in content

    def test_index_document_endpoint(self, generator, semantic_source, vector_store_config, output_dirs):
        """Req 9.12: POST /{sourceName}/index-document."""
        content = self._get_controller(generator, [semantic_source], vector_store_config, output_dirs)
        assert "/{sourceName}/index-document" in content
        assert "indexDocument(" in content

    def test_source_listing_includes_source(self, generator, semantic_source, vector_store_config, output_dirs):
        """Controller lists configured sources."""
        content = self._get_controller(generator, [semantic_source], vector_store_config, output_dirs)
        assert '"courseEmbeddings"' in content
        assert '"semantic"' in content

    def test_rag_indexing_service_injection(self, generator, semantic_source, vector_store_config, output_dirs):
        """Injects RagIndexingService."""
        content = self._get_controller(generator, [semantic_source], vector_store_config, output_dirs)
        assert "RagIndexingService ragIndexingService" in content


# ======================================================================
# Test: Multiple semantic sources
# ======================================================================

class TestMultipleSemanticSources:
    """Tests for generating with multiple semantic sources."""

    def test_two_semantic_services(self, generator, vector_store_config, output_dirs):
        sources = [
            {"name": "courseEmbeddings", "type": "semantic", "enabled": True,
             "providerName": "gpt4", "securityMode": "public"},
            {"name": "userProfiles", "type": "semantic", "enabled": True,
             "providerName": "gpt3", "securityMode": "role_restricted"},
        ]
        results = generator.generate(sources, vector_store_config, BASE_PACKAGE, output_dirs)
        filenames = {Path(fp).name for fp, _ in results}
        assert "CourseEmbeddingsSemanticRagService.java" in filenames
        assert "UserProfilesSemanticRagService.java" in filenames

    def test_indexing_service_references_all_sources(self, generator, vector_store_config, output_dirs):
        sources = [
            {"name": "courseEmbeddings", "type": "semantic", "enabled": True,
             "providerName": "gpt4", "securityMode": "public"},
            {"name": "userProfiles", "type": "semantic", "enabled": True,
             "providerName": "gpt3", "securityMode": "public"},
        ]
        results = generator.generate(sources, vector_store_config, BASE_PACKAGE, output_dirs)
        indexing_content = next(c for fp, c in results if Path(fp).name == "RagIndexingService.java")
        assert "CourseEmbeddingsSemanticRagService" in indexing_content
        assert "UserProfilesSemanticRagService" in indexing_content
        assert '"courseEmbeddings"' in indexing_content
        assert '"userProfiles"' in indexing_content
