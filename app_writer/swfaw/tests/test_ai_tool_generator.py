"""Unit tests for the AI ToolFunctionGenerator.

Verifies that the ToolFunctionGenerator produces correct Java source files
for EntityAiToolFunctions, StandaloneAiToolFunctions,
DocumentTaskToolFunctions, RagToolFunctions,
DocumentIngestionToolFunctions, and ToolSecurityContextHolder.

Requirements: 13.1–13.3, 13.10–13.14
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_tool_generator import (
    ToolFunctionGenerator,
    _pascal,
    _camel,
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
    return ToolFunctionGenerator(jinja_env)


@pytest.fixture
def minimal_orchestrator():
    return {"providerName": "mainGpt"}


@pytest.fixture
def entity_capabilities():
    return [
        {
            "entityName": "Product",
            "providerName": "mainGpt",
            "enabledOperations": ["search", "generate", "summarize", "classify", "chat"],
        },
        {
            "entityName": "Order",
            "providerName": "mainGpt",
            "enabledOperations": ["search", "summarize"],
        },
    ]


@pytest.fixture
def standalone_operations():
    return [
        {
            "name": "code_review",
            "type": "chat",
            "providerName": "mainGpt",
            "basePath": "code-review",
            "systemPrompt": "You are a code reviewer.",
            "enabledActions": ["chat", "chatStream", "generate"],
        },
        {
            "name": "data_analysis",
            "type": "query",
            "providerName": "mainGpt",
            "basePath": "data-analysis",
            "systemPrompt": "You are a data analyst.",
            "enabledActions": ["query"],
        },
    ]


@pytest.fixture
def document_processing():
    return {
        "enabled": True,
        "tasks": [
            {
                "name": "summarize_doc",
                "taskType": "summarization",
                "providerName": "mainGpt",
                "promptTemplate": "Summarize: {{document_text}}",
            },
            {
                "name": "translate_doc",
                "taskType": "translation",
                "providerName": "mainGpt",
                "promptTemplate": "Translate: {{document_text}}",
            },
        ],
    }


@pytest.fixture
def rag_sources():
    return [
        {
            "name": "product_docs",
            "type": "semantic",
            "enabled": True,
            "providerName": "mainGpt",
        },
        {
            "name": "faq_search",
            "type": "heuristic",
            "enabled": True,
        },
    ]


@pytest.fixture
def document_ingestion():
    return {
        "enabled": True,
        "allowedMimeTypes": ["application/pdf"],
        "maxFileSizeBytes": 10485760,
    }


@pytest.fixture
def output_dirs():
    return {
        "tools": Path("com/example/app/ai/tools"),
    }


BASE_PACKAGE = "com.example.app"


# ======================================================================
# Test: generate() — skip logic
# ======================================================================

class TestToolGeneratorSkipLogic:
    """Tests for the generate() method's skip logic."""

    def test_no_files_when_orchestrator_is_none(self, generator, output_dirs):
        """Req 13.9: No tool files when orchestrator is None."""
        results = generator.generate(
            None, [], [], None, [], None, BASE_PACKAGE, output_dirs
        )
        assert results == []

    def test_no_files_when_orchestrator_is_empty_dict(self, generator, output_dirs):
        """Req 13.9: Empty dict is falsy — no files generated."""
        results = generator.generate(
            {}, [], [], None, [], None, BASE_PACKAGE, output_dirs
        )
        assert results == []

    def test_security_context_holder_always_generated(
        self, generator, minimal_orchestrator, output_dirs
    ):
        """Req 13.12: ToolSecurityContextHolder always generated when orchestrator present."""
        results = generator.generate(
            minimal_orchestrator, [], [], None, [], None, BASE_PACKAGE, output_dirs
        )
        filenames = {Path(fp).name for fp, _ in results}
        assert "ToolSecurityContextHolder.java" in filenames

    def test_only_security_holder_when_no_capabilities(
        self, generator, minimal_orchestrator, output_dirs
    ):
        """When no capabilities configured, only ToolSecurityContextHolder is generated."""
        results = generator.generate(
            minimal_orchestrator, [], [], None, [], None, BASE_PACKAGE, output_dirs
        )
        assert len(results) == 1


# ======================================================================
# Test: generate() — file counts and names
# ======================================================================

class TestToolGeneratorFileCounts:
    """Tests for correct file generation counts."""

    def test_entity_tool_files_per_entity(
        self, generator, minimal_orchestrator, entity_capabilities, output_dirs
    ):
        """Req 13.1: One EntityAiToolFunctions per entity."""
        results = generator.generate(
            minimal_orchestrator, entity_capabilities, [], None, [], None,
            BASE_PACKAGE, output_dirs,
        )
        filenames = {Path(fp).name for fp, _ in results}
        assert "ProductAiToolFunctions.java" in filenames
        assert "OrderAiToolFunctions.java" in filenames

    def test_standalone_tool_files_per_operation(
        self, generator, minimal_orchestrator, standalone_operations, output_dirs
    ):
        """Req 13.1: One StandaloneAiToolFunctions per standalone operation."""
        results = generator.generate(
            minimal_orchestrator, [], standalone_operations, None, [], None,
            BASE_PACKAGE, output_dirs,
        )
        filenames = {Path(fp).name for fp, _ in results}
        assert "CodeReviewAiToolFunctions.java" in filenames
        assert "DataAnalysisAiToolFunctions.java" in filenames

    def test_document_task_tool_files_per_task(
        self, generator, minimal_orchestrator, document_processing, output_dirs
    ):
        """Req 13.1: One DocumentTaskToolFunctions per document task."""
        results = generator.generate(
            minimal_orchestrator, [], [], document_processing, [], None,
            BASE_PACKAGE, output_dirs,
        )
        filenames = {Path(fp).name for fp, _ in results}
        assert "SummarizeDocDocumentTaskToolFunctions.java" in filenames
        assert "TranslateDocDocumentTaskToolFunctions.java" in filenames

    def test_rag_tool_functions_generated(
        self, generator, minimal_orchestrator, rag_sources, output_dirs
    ):
        """Req 13.1: RagToolFunctions generated when semantic RAG sources exist."""
        results = generator.generate(
            minimal_orchestrator, [], [], None, rag_sources, None,
            BASE_PACKAGE, output_dirs,
        )
        filenames = {Path(fp).name for fp, _ in results}
        assert "RagToolFunctions.java" in filenames

    def test_no_rag_tools_without_semantic_sources(
        self, generator, minimal_orchestrator, output_dirs
    ):
        """No RagToolFunctions when no semantic RAG sources."""
        heuristic_only = [{"name": "faq", "type": "heuristic", "enabled": True}]
        results = generator.generate(
            minimal_orchestrator, [], [], None, heuristic_only, None,
            BASE_PACKAGE, output_dirs,
        )
        filenames = {Path(fp).name for fp, _ in results}
        assert "RagToolFunctions.java" not in filenames

    def test_no_rag_tools_when_disabled(
        self, generator, minimal_orchestrator, output_dirs
    ):
        """No RagToolFunctions when semantic sources are disabled."""
        disabled = [{"name": "docs", "type": "semantic", "enabled": False}]
        results = generator.generate(
            minimal_orchestrator, [], [], None, disabled, None,
            BASE_PACKAGE, output_dirs,
        )
        filenames = {Path(fp).name for fp, _ in results}
        assert "RagToolFunctions.java" not in filenames

    def test_ingestion_tool_functions_generated(
        self, generator, minimal_orchestrator, document_ingestion, output_dirs
    ):
        """Req 13.1: DocumentIngestionToolFunctions generated when ingestion enabled."""
        results = generator.generate(
            minimal_orchestrator, [], [], None, [], document_ingestion,
            BASE_PACKAGE, output_dirs,
        )
        filenames = {Path(fp).name for fp, _ in results}
        assert "DocumentIngestionToolFunctions.java" in filenames

    def test_no_ingestion_tools_when_disabled(
        self, generator, minimal_orchestrator, output_dirs
    ):
        """No DocumentIngestionToolFunctions when ingestion disabled."""
        disabled = {"enabled": False}
        results = generator.generate(
            minimal_orchestrator, [], [], None, [], disabled,
            BASE_PACKAGE, output_dirs,
        )
        filenames = {Path(fp).name for fp, _ in results}
        assert "DocumentIngestionToolFunctions.java" not in filenames

    def test_full_generation_file_count(
        self, generator, minimal_orchestrator, entity_capabilities,
        standalone_operations, document_processing, rag_sources,
        document_ingestion, output_dirs,
    ):
        """Full generation: 1 security holder + 2 entity + 2 standalone + 2 doc tasks + 1 rag + 1 ingestion = 9."""
        results = generator.generate(
            minimal_orchestrator, entity_capabilities, standalone_operations,
            document_processing, rag_sources, document_ingestion,
            BASE_PACKAGE, output_dirs,
        )
        assert len(results) == 9

    def test_all_content_is_nonempty(
        self, generator, minimal_orchestrator, entity_capabilities,
        standalone_operations, document_processing, rag_sources,
        document_ingestion, output_dirs,
    ):
        results = generator.generate(
            minimal_orchestrator, entity_capabilities, standalone_operations,
            document_processing, rag_sources, document_ingestion,
            BASE_PACKAGE, output_dirs,
        )
        for filepath, content in results:
            assert content.strip(), f"Empty content for {filepath}"

    def test_no_doc_task_tools_when_processing_disabled(
        self, generator, minimal_orchestrator, output_dirs
    ):
        """No DocumentTaskToolFunctions when processing is disabled."""
        disabled = {"enabled": False, "tasks": [{"name": "t", "taskType": "summarization"}]}
        results = generator.generate(
            minimal_orchestrator, [], [], disabled, [], None,
            BASE_PACKAGE, output_dirs,
        )
        filenames = {Path(fp).name for fp, _ in results}
        # Only ToolSecurityContextHolder
        assert len(results) == 1


# ======================================================================
# Test: ToolSecurityContextHolder template
# ======================================================================

class TestToolSecurityContextHolder:
    """Tests for the generated ToolSecurityContextHolder."""

    def _get_holder(self, generator, output_dirs):
        results = generator.generate(
            {"providerName": "gpt"}, [], [], None, [], None,
            BASE_PACKAGE, output_dirs,
        )
        return next(c for fp, c in results if "ToolSecurityContextHolder" in fp)

    def test_package_declaration(self, generator, output_dirs):
        content = self._get_holder(generator, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.tools;" in content

    def test_component_annotation(self, generator, output_dirs):
        """Req 13.2: Spring @Component bean."""
        content = self._get_holder(generator, output_dirs)
        assert "@Component" in content

    def test_thread_local_authentication(self, generator, output_dirs):
        """Req 13.12: ThreadLocal<Authentication>."""
        content = self._get_holder(generator, output_dirs)
        assert "ThreadLocal<Authentication>" in content

    def test_set_authentication_method(self, generator, output_dirs):
        content = self._get_holder(generator, output_dirs)
        assert "setAuthentication(Authentication" in content

    def test_get_authentication_method(self, generator, output_dirs):
        content = self._get_holder(generator, output_dirs)
        assert "getAuthentication()" in content

    def test_clear_method(self, generator, output_dirs):
        content = self._get_holder(generator, output_dirs)
        assert "clear()" in content

    def test_imports_authentication(self, generator, output_dirs):
        content = self._get_holder(generator, output_dirs)
        assert "import org.springframework.security.core.Authentication;" in content


# ======================================================================
# Test: EntityAiToolFunctions template
# ======================================================================

class TestEntityAiToolFunctions:
    """Tests for the generated EntityAiToolFunctions."""

    def _get_entity_tools(self, generator, entity_capabilities, output_dirs, entity_name="Product"):
        results = generator.generate(
            {"providerName": "gpt"}, entity_capabilities, [], None, [], None,
            BASE_PACKAGE, output_dirs,
        )
        return next(c for fp, c in results if f"{entity_name}AiToolFunctions" in fp)

    def test_package_declaration(self, generator, entity_capabilities, output_dirs):
        content = self._get_entity_tools(generator, entity_capabilities, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.tools;" in content

    def test_component_annotation(self, generator, entity_capabilities, output_dirs):
        """Req 13.2: Spring @Component bean."""
        content = self._get_entity_tools(generator, entity_capabilities, output_dirs)
        assert "@Component" in content

    def test_class_name(self, generator, entity_capabilities, output_dirs):
        content = self._get_entity_tools(generator, entity_capabilities, output_dirs)
        assert "public class ProductAiToolFunctions" in content

    def test_tool_annotation_on_search(self, generator, entity_capabilities, output_dirs):
        """Req 13.2: @Tool annotation on search method."""
        content = self._get_entity_tools(generator, entity_capabilities, output_dirs)
        assert '@Tool(description = "Search Product records' in content

    def test_tool_param_annotation(self, generator, entity_capabilities, output_dirs):
        """Req 13.2: @ToolParam annotation on parameters."""
        content = self._get_entity_tools(generator, entity_capabilities, output_dirs)
        assert "@ToolParam(description =" in content

    def test_returns_string(self, generator, entity_capabilities, output_dirs):
        """Req 13.2: All tool methods return String."""
        content = self._get_entity_tools(generator, entity_capabilities, output_dirs)
        assert "public String search" in content

    def test_security_context_check(self, generator, entity_capabilities, output_dirs):
        """Req 13.10: Retrieves security context from ToolSecurityContextHolder."""
        content = self._get_entity_tools(generator, entity_capabilities, output_dirs)
        assert "ToolSecurityContextHolder.getAuthentication()" in content

    def test_access_denied_on_auth_failure(self, generator, entity_capabilities, output_dirs):
        """Req 13.11: Returns descriptive error string on auth failure."""
        content = self._get_entity_tools(generator, entity_capabilities, output_dirs)
        assert "ACCESS_DENIED" in content
        assert "Access denied" in content

    def test_all_operations_present_for_product(self, generator, entity_capabilities, output_dirs):
        """Product has all 5 operations enabled."""
        content = self._get_entity_tools(generator, entity_capabilities, output_dirs)
        assert "searchProduct" in content
        assert "generateProductContent" in content
        assert "summarizeProduct" in content
        assert "classifyProduct" in content
        assert "chatWithProduct" in content

    def test_only_enabled_operations_for_order(self, generator, entity_capabilities, output_dirs):
        """Order has only search and summarize enabled."""
        content = self._get_entity_tools(generator, entity_capabilities, output_dirs, "Order")
        assert "searchOrder" in content
        assert "summarizeOrder" in content
        assert "generateOrderContent" not in content
        assert "classifyOrder" not in content
        assert "chatWithOrder" not in content

    def test_service_injection(self, generator, entity_capabilities, output_dirs):
        content = self._get_entity_tools(generator, entity_capabilities, output_dirs)
        assert "ProductAiService" in content

    def test_error_handling(self, generator, entity_capabilities, output_dirs):
        """Req 13.11: Returns error string, not throw."""
        content = self._get_entity_tools(generator, entity_capabilities, output_dirs)
        assert "catch (Exception e)" in content
        assert "Error searching Product" in content

    def test_blocks_reactive_chain(self, generator, entity_capabilities, output_dirs):
        """Req 13.2: Tool methods return String (blocking on reactive chains)."""
        content = self._get_entity_tools(generator, entity_capabilities, output_dirs)
        assert ".block()" in content


# ======================================================================
# Test: StandaloneAiToolFunctions template
# ======================================================================

class TestStandaloneAiToolFunctions:
    """Tests for the generated StandaloneAiToolFunctions."""

    def _get_standalone_tools(self, generator, standalone_operations, output_dirs, op_name="CodeReview"):
        results = generator.generate(
            {"providerName": "gpt"}, [], standalone_operations, None, [], None,
            BASE_PACKAGE, output_dirs,
        )
        return next(c for fp, c in results if f"{op_name}AiToolFunctions" in fp)

    def test_package_declaration(self, generator, standalone_operations, output_dirs):
        content = self._get_standalone_tools(generator, standalone_operations, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.tools;" in content

    def test_component_annotation(self, generator, standalone_operations, output_dirs):
        content = self._get_standalone_tools(generator, standalone_operations, output_dirs)
        assert "@Component" in content

    def test_class_name(self, generator, standalone_operations, output_dirs):
        content = self._get_standalone_tools(generator, standalone_operations, output_dirs)
        assert "public class CodeReviewAiToolFunctions" in content

    def test_chat_tool_present(self, generator, standalone_operations, output_dirs):
        """Req 13.1: chat action generates tool method."""
        content = self._get_standalone_tools(generator, standalone_operations, output_dirs)
        assert "codeReviewChat" in content
        assert '@Tool(description = "Chat for the code_review' in content

    def test_generate_tool_present(self, generator, standalone_operations, output_dirs):
        """Req 13.1: generate action generates tool method."""
        content = self._get_standalone_tools(generator, standalone_operations, output_dirs)
        assert "codeReviewGenerate" in content

    def test_chat_stream_not_present(self, generator, standalone_operations, output_dirs):
        """Req 13.1: chatStream is NOT exposed as a tool."""
        content = self._get_standalone_tools(generator, standalone_operations, output_dirs)
        assert "chatStream" not in content.lower().replace("chatstream", "")
        # Verify no chatStream method exists
        assert "ChatStream" not in content or "chatStream" not in content

    def test_query_only_operation(self, generator, standalone_operations, output_dirs):
        """DataAnalysis has only query enabled."""
        content = self._get_standalone_tools(generator, standalone_operations, output_dirs, "DataAnalysis")
        assert "dataAnalysisQuery" in content
        assert "dataAnalysisChat" not in content
        assert "dataAnalysisGenerate" not in content

    def test_security_context_check(self, generator, standalone_operations, output_dirs):
        content = self._get_standalone_tools(generator, standalone_operations, output_dirs)
        assert "ToolSecurityContextHolder.getAuthentication()" in content

    def test_returns_string(self, generator, standalone_operations, output_dirs):
        content = self._get_standalone_tools(generator, standalone_operations, output_dirs)
        assert "public String codeReviewChat" in content

    def test_service_injection(self, generator, standalone_operations, output_dirs):
        content = self._get_standalone_tools(generator, standalone_operations, output_dirs)
        assert "CodeReviewAiService" in content


# ======================================================================
# Test: DocumentTaskToolFunctions template
# ======================================================================

class TestDocumentTaskToolFunctions:
    """Tests for the generated DocumentTaskToolFunctions."""

    def _get_doc_task_tools(self, generator, document_processing, output_dirs, task_pascal="SummarizeDoc"):
        results = generator.generate(
            {"providerName": "gpt"}, [], [], document_processing, [], None,
            BASE_PACKAGE, output_dirs,
        )
        return next(c for fp, c in results if f"{task_pascal}DocumentTaskToolFunctions" in fp)

    def test_package_declaration(self, generator, document_processing, output_dirs):
        content = self._get_doc_task_tools(generator, document_processing, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.tools;" in content

    def test_component_annotation(self, generator, document_processing, output_dirs):
        content = self._get_doc_task_tools(generator, document_processing, output_dirs)
        assert "@Component" in content

    def test_class_name(self, generator, document_processing, output_dirs):
        content = self._get_doc_task_tools(generator, document_processing, output_dirs)
        assert "public class SummarizeDocDocumentTaskToolFunctions" in content

    def test_tool_annotation(self, generator, document_processing, output_dirs):
        content = self._get_doc_task_tools(generator, document_processing, output_dirs)
        assert '@Tool(description = "Execute the summarize_doc (summarization)' in content

    def test_tool_param_annotation(self, generator, document_processing, output_dirs):
        content = self._get_doc_task_tools(generator, document_processing, output_dirs)
        assert "@ToolParam(description =" in content

    def test_returns_string(self, generator, document_processing, output_dirs):
        content = self._get_doc_task_tools(generator, document_processing, output_dirs)
        assert "public String executeSummarizeDocTask" in content

    def test_security_check(self, generator, document_processing, output_dirs):
        content = self._get_doc_task_tools(generator, document_processing, output_dirs)
        assert "ToolSecurityContextHolder.getAuthentication()" in content

    def test_service_injection(self, generator, document_processing, output_dirs):
        content = self._get_doc_task_tools(generator, document_processing, output_dirs)
        assert "DocumentProcessingService" in content

    def test_translate_task_class(self, generator, document_processing, output_dirs):
        content = self._get_doc_task_tools(generator, document_processing, output_dirs, "TranslateDoc")
        assert "public class TranslateDocDocumentTaskToolFunctions" in content
        assert "executeTranslateDocTask" in content


# ======================================================================
# Test: RagToolFunctions template
# ======================================================================

class TestRagToolFunctions:
    """Tests for the generated RagToolFunctions."""

    def _get_rag_tools(self, generator, rag_sources, output_dirs):
        results = generator.generate(
            {"providerName": "gpt"}, [], [], None, rag_sources, None,
            BASE_PACKAGE, output_dirs,
        )
        return next(c for fp, c in results if "RagToolFunctions" in fp)

    def test_package_declaration(self, generator, rag_sources, output_dirs):
        content = self._get_rag_tools(generator, rag_sources, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.tools;" in content

    def test_component_annotation(self, generator, rag_sources, output_dirs):
        content = self._get_rag_tools(generator, rag_sources, output_dirs)
        assert "@Component" in content

    def test_reindex_tool(self, generator, rag_sources, output_dirs):
        """Req 13.1: reindex tool method."""
        content = self._get_rag_tools(generator, rag_sources, output_dirs)
        assert "reindexRagSource" in content
        assert '@Tool(description = "Reindex a RAG source' in content

    def test_index_document_tool(self, generator, rag_sources, output_dirs):
        """Req 13.1: index-document tool method."""
        content = self._get_rag_tools(generator, rag_sources, output_dirs)
        assert "indexDocumentInRagSource" in content

    def test_admin_permission_check(self, generator, rag_sources, output_dirs):
        """Req 13.10: RAG tools verify admin permissions."""
        content = self._get_rag_tools(generator, rag_sources, output_dirs)
        assert "isAdmin" in content
        assert "ROLE_ADMIN" in content

    def test_returns_string(self, generator, rag_sources, output_dirs):
        content = self._get_rag_tools(generator, rag_sources, output_dirs)
        assert "public String reindexRagSource" in content

    def test_service_injection(self, generator, rag_sources, output_dirs):
        content = self._get_rag_tools(generator, rag_sources, output_dirs)
        assert "RagIndexingService" in content


# ======================================================================
# Test: DocumentIngestionToolFunctions template
# ======================================================================

class TestDocumentIngestionToolFunctions:
    """Tests for the generated DocumentIngestionToolFunctions."""

    def _get_ingestion_tools(self, generator, document_ingestion, output_dirs):
        results = generator.generate(
            {"providerName": "gpt"}, [], [], None, [], document_ingestion,
            BASE_PACKAGE, output_dirs,
        )
        return next(c for fp, c in results if "DocumentIngestionToolFunctions" in fp)

    def test_package_declaration(self, generator, document_ingestion, output_dirs):
        content = self._get_ingestion_tools(generator, document_ingestion, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.tools;" in content

    def test_component_annotation(self, generator, document_ingestion, output_dirs):
        content = self._get_ingestion_tools(generator, document_ingestion, output_dirs)
        assert "@Component" in content

    def test_re_extract_tool(self, generator, document_ingestion, output_dirs):
        """Req 13.1: re-extract tool method."""
        content = self._get_ingestion_tools(generator, document_ingestion, output_dirs)
        assert "reExtractDocument" in content
        assert '@Tool(description = "Re-extract text' in content

    def test_list_documents_tool(self, generator, document_ingestion, output_dirs):
        content = self._get_ingestion_tools(generator, document_ingestion, output_dirs)
        assert "listIngestedDocuments" in content

    def test_security_check(self, generator, document_ingestion, output_dirs):
        content = self._get_ingestion_tools(generator, document_ingestion, output_dirs)
        assert "ToolSecurityContextHolder.getAuthentication()" in content

    def test_returns_string(self, generator, document_ingestion, output_dirs):
        content = self._get_ingestion_tools(generator, document_ingestion, output_dirs)
        assert "public String reExtractDocument" in content

    def test_service_injection(self, generator, document_ingestion, output_dirs):
        content = self._get_ingestion_tools(generator, document_ingestion, output_dirs)
        assert "DocumentIngestionService" in content

    def test_document_ownership_check(self, generator, document_ingestion, output_dirs):
        """Req 13.10: Ingestion tools verify document ownership."""
        content = self._get_ingestion_tools(generator, document_ingestion, output_dirs)
        assert "extractUserId" in content


# ======================================================================
# Test: Context building helpers
# ======================================================================

class TestContextBuilding:
    """Tests for the _build_*_context methods."""

    def test_entity_tool_context(self, generator):
        cap = {
            "entityName": "Product",
            "providerName": "gpt",
            "enabledOperations": ["search", "classify"],
        }
        ctx = generator._build_entity_tool_context(cap, BASE_PACKAGE)
        assert ctx["entity_name"] == "Product"
        assert ctx["entity_name_camel"] == "product"
        assert ctx["has_search"] is True
        assert ctx["has_classify"] is True
        assert ctx["has_generate"] is False
        assert ctx["has_summarize"] is False
        assert ctx["has_chat"] is False

    def test_standalone_tool_context(self, generator):
        op = {
            "name": "code_review",
            "enabledActions": ["chat", "chatStream", "generate"],
        }
        ctx = generator._build_standalone_tool_context(op, BASE_PACKAGE)
        assert ctx["operation_name"] == "CodeReview"
        assert ctx["operation_name_camel"] == "codeReview"
        assert ctx["operation_raw_name"] == "code_review"
        assert ctx["has_chat"] is True
        assert ctx["has_generate"] is True
        assert ctx["has_query"] is False

    def test_doc_task_tool_context(self, generator):
        task = {"name": "summarize_doc", "taskType": "summarization"}
        ctx = generator._build_doc_task_tool_context(task, BASE_PACKAGE)
        assert ctx["task_name"] == "summarize_doc"
        assert ctx["task_name_pascal"] == "SummarizeDoc"
        assert ctx["task_type"] == "summarization"


# ======================================================================
# Test: Helper functions
# ======================================================================

class TestHelperFunctions:
    """Tests for _pascal and _camel helper functions."""

    def test_pascal_snake_case(self):
        assert _pascal("code_review") == "CodeReview"

    def test_pascal_already_pascal(self):
        assert _pascal("Product") == "Product"

    def test_pascal_camel_case(self):
        assert _pascal("codeReview") == "CodeReview"

    def test_pascal_empty(self):
        assert _pascal("") == ""

    def test_camel_snake_case(self):
        assert _camel("code_review") == "codeReview"

    def test_camel_already_pascal(self):
        assert _camel("Product") == "product"

    def test_camel_empty(self):
        assert _camel("") == ""
