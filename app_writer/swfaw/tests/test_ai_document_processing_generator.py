"""Unit tests for the AI DocumentProcessingGenerator.

Verifies that the DocumentProcessingGenerator produces correct Java source files
for DocumentProcessingService, AiDocumentTaskResult entity,
AiDocumentTaskResultRepository, DocumentProcessingController, and related DTOs.

Requirements: 11.14–11.28
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_document_processing_generator import (
    DocumentProcessingGenerator,
    _pascal_case,
    _camel_case,
    VALID_TASK_TYPES,
    VALID_TARGET_SCOPES,
    TASK_TYPE_REQUIRES_TARGET_LANGUAGE,
    TASK_TYPE_REQUIRES_CATEGORIES,
    TASK_TYPE_REQUIRES_SECOND_DOCUMENT,
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
    return DocumentProcessingGenerator(jinja_env)


@pytest.fixture
def single_task_config():
    """Document processing config with a single summarization task."""
    return {
        "enabled": True,
        "defaultProviderName": "gpt4",
        "tasks": [
            {
                "name": "docSummary",
                "taskType": "summarization",
                "providerName": "gpt4",
                "promptTemplate": "Summarize: {{document_text}}",
            },
        ],
    }


@pytest.fixture
def multi_task_config():
    """Document processing config with multiple task types."""
    return {
        "enabled": True,
        "defaultProviderName": "gpt4",
        "tasks": [
            {
                "name": "docSummary",
                "taskType": "summarization",
                "providerName": "gpt4",
                "promptTemplate": "Summarize: {{document_text}}",
            },
            {
                "name": "docTranslate",
                "taskType": "translation",
                "providerName": "gpt4",
                "targetLanguage": "es",
                "promptTemplate": "Translate to Spanish: {{document_text}}",
            },
            {
                "name": "docClassify",
                "taskType": "classification",
                "providerName": "gpt4",
                "categories": ["legal", "financial", "technical"],
                "promptTemplate": "Classify: {{document_text}}",
            },
            {
                "name": "docCompare",
                "taskType": "comparison",
                "providerName": "gpt4",
                "requiresSecondDocument": True,
                "promptTemplate": "Compare: {{document_text}} {{user_instruction}}",
            },
            {
                "name": "docQuery",
                "taskType": "querying",
                "providerName": "gpt4",
                "promptTemplate": "Answer: {{user_instruction}} based on {{document_text}}",
            },
        ],
    }


@pytest.fixture
def eligible_providers_config():
    """Config with eligible providers for runtime model selection."""
    return {
        "enabled": True,
        "defaultProviderName": "gpt4",
        "tasks": [
            {
                "name": "flexSummary",
                "taskType": "summarization",
                "providerName": "gpt4",
                "eligibleProviders": ["gpt4", "claude", "llama"],
                "promptTemplate": "Summarize: {{document_text}}",
            },
        ],
    }


@pytest.fixture
def disabled_config():
    """Document processing config that is disabled."""
    return {
        "enabled": False,
        "tasks": [],
    }


@pytest.fixture
def output_dirs():
    return {
        "processing": Path("com/example/app/ai/processing"),
        "controller": Path("com/example/app/ai/controller"),
        "dto": Path("com/example/app/ai/dto"),
        "entity": Path("com/example/app/ai/entity"),
        "repository": Path("com/example/app/ai/repository"),
    }


BASE_PACKAGE = "com.example.app"


# ======================================================================
# Helper function tests
# ======================================================================

class TestHelperFunctions:
    def test_pascal_case_camel(self):
        assert _pascal_case("docSummary") == "DocSummary"

    def test_pascal_case_snake(self):
        assert _pascal_case("doc_summary") == "DocSummary"

    def test_pascal_case_single(self):
        assert _pascal_case("summary") == "Summary"

    def test_pascal_case_empty(self):
        assert _pascal_case("") == ""

    def test_camel_case(self):
        assert _camel_case("DocSummary") == "docSummary"

    def test_camel_case_snake(self):
        assert _camel_case("doc_summary") == "docSummary"

    def test_valid_task_types_count(self):
        assert len(VALID_TASK_TYPES) == 12

    def test_valid_task_types_contains_all(self):
        expected = {
            "summarization", "composition", "querying", "translation",
            "key_info_extraction", "sentiment_analysis", "classification",
            "comparison", "redaction_suggestions", "action_item_extraction",
            "table_extraction", "outline_generation",
        }
        assert VALID_TASK_TYPES == expected

    def test_valid_target_scopes(self):
        assert VALID_TARGET_SCOPES == {"full_document", "page_range", "section"}

    def test_translation_requires_target_language(self):
        assert "translation" in TASK_TYPE_REQUIRES_TARGET_LANGUAGE

    def test_classification_requires_categories(self):
        assert "classification" in TASK_TYPE_REQUIRES_CATEGORIES

    def test_comparison_requires_second_document(self):
        assert "comparison" in TASK_TYPE_REQUIRES_SECOND_DOCUMENT


# ======================================================================
# Generate method — conditional generation
# ======================================================================

class TestDocumentProcessingGeneratorGenerate:
    """Req 11.17: When documentProcessing is absent or not enabled, no files."""

    def test_no_files_when_none(self, generator, output_dirs):
        results = generator.generate(None, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_no_files_when_disabled(self, generator, disabled_config, output_dirs):
        results = generator.generate(disabled_config, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_no_files_when_empty_dict(self, generator, output_dirs):
        results = generator.generate({}, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_single_task_generates_six_files(self, generator, single_task_config, output_dirs):
        results = generator.generate(single_task_config, BASE_PACKAGE, output_dirs)
        assert len(results) == 6

    def test_multi_task_generates_six_files(self, generator, multi_task_config, output_dirs):
        results = generator.generate(multi_task_config, BASE_PACKAGE, output_dirs)
        assert len(results) == 6

    def test_all_content_is_nonempty(self, generator, single_task_config, output_dirs):
        results = generator.generate(single_task_config, BASE_PACKAGE, output_dirs)
        for filepath, content in results:
            assert content.strip(), f"Empty content for {filepath}"

    def test_output_dirs_used_in_paths(self, generator, single_task_config, output_dirs):
        results = generator.generate(single_task_config, BASE_PACKAGE, output_dirs)
        paths = [fp for fp, _ in results]
        assert any("ai/dto" in p for p in paths)
        assert any("ai/entity" in p for p in paths)
        assert any("ai/repository" in p for p in paths)
        assert any("ai/processing" in p for p in paths)
        assert any("ai/controller" in p for p in paths)

    def test_correct_filenames(self, generator, single_task_config, output_dirs):
        results = generator.generate(single_task_config, BASE_PACKAGE, output_dirs)
        filenames = [Path(fp).name for fp, _ in results]
        assert "DocumentTaskRequestDTO.java" in filenames
        assert "DocumentTaskResultDTO.java" in filenames
        assert "AiDocumentTaskResult.java" in filenames
        assert "AiDocumentTaskResultRepository.java" in filenames
        assert "DocumentProcessingService.java" in filenames
        assert "DocumentProcessingController.java" in filenames


# ======================================================================
# DocumentTaskRequestDTO
# ======================================================================

class TestDocumentTaskRequestDTO:
    """Req 11.20: DocumentTaskRequestDTO."""

    def _get_dto(self, generator, config, output_dirs):
        results = generator.generate(config, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "DocumentTaskRequestDTO" in fp:
                return content
        raise AssertionError("DocumentTaskRequestDTO not found")

    def test_is_record(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "public record DocumentTaskRequestDTO" in content

    def test_package_declaration(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.dto;" in content

    def test_has_provider_name(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "providerName" in content

    def test_has_user_instruction(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "userInstruction" in content

    def test_has_target_scope(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "targetScope" in content

    def test_has_task_names(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "taskNames" in content

    def test_has_second_document_id(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "secondDocumentId" in content


# ======================================================================
# DocumentTaskResultDTO
# ======================================================================

class TestDocumentTaskResultDTO:
    """Req 11.20: DocumentTaskResultDTO."""

    def _get_dto(self, generator, config, output_dirs):
        results = generator.generate(config, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "DocumentTaskResultDTO" in fp:
                return content
        raise AssertionError("DocumentTaskResultDTO not found")

    def test_is_record(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "public record DocumentTaskResultDTO" in content

    def test_package_declaration(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.dto;" in content

    def test_has_id(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "Long id" in content

    def test_has_document_id(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "Long documentId" in content

    def test_has_task_name(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "String taskName" in content

    def test_has_task_type(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "String taskType" in content

    def test_has_provider_name(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "String providerName" in content

    def test_has_output_text(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "String outputText" in content

    def test_has_status(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "String status" in content

    def test_has_error_message(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "String errorMessage" in content

    def test_has_execution_duration(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "Long executionDurationMs" in content

    def test_has_prompt_tokens(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "Integer promptTokens" in content

    def test_has_completion_tokens(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "Integer completionTokens" in content

    def test_has_chained_from_result_id(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "Long chainedFromResultId" in content

    def test_has_timestamps(self, generator, single_task_config, output_dirs):
        content = self._get_dto(generator, single_task_config, output_dirs)
        assert "LocalDateTime createdAt" in content
        assert "LocalDateTime updatedAt" in content


# ======================================================================
# AiDocumentTaskResult entity
# ======================================================================

class TestAiDocumentTaskResultEntity:
    """Req 11.21: AiDocumentTaskResult entity."""

    def _get_entity(self, generator, config, output_dirs):
        results = generator.generate(config, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "AiDocumentTaskResult.java" in fp and "Repository" not in fp:
                return content
        raise AssertionError("AiDocumentTaskResult entity not found")

    def test_package_declaration(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.entity;" in content

    def test_table_annotation(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '@Table("ai_document_task_result")' in content

    def test_has_id(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert "@Id" in content
        assert "private Long id;" in content

    def test_has_document_id(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '"document_id"' in content

    def test_has_user_id(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '"user_id"' in content

    def test_has_task_name(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '"task_name"' in content

    def test_has_task_type(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '"task_type"' in content

    def test_has_provider_name(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '"provider_name"' in content

    def test_has_input_text(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '"input_text"' in content

    def test_has_input_section(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '"input_section"' in content

    def test_has_output_text(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '"output_text"' in content

    def test_has_status(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '"status"' in content

    def test_has_error_message(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '"error_message"' in content

    def test_has_execution_duration_ms(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '"execution_duration_ms"' in content

    def test_has_prompt_tokens(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '"prompt_tokens"' in content

    def test_has_completion_tokens(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '"completion_tokens"' in content

    def test_has_chained_from_result_id(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '"chained_from_result_id"' in content

    def test_has_metadata(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '"metadata"' in content

    def test_has_timestamps(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert '"created_at"' in content
        assert '"updated_at"' in content

    def test_lombok_annotations(self, generator, single_task_config, output_dirs):
        content = self._get_entity(generator, single_task_config, output_dirs)
        assert "@Data" in content
        assert "@Builder" in content
        assert "@NoArgsConstructor" in content
        assert "@AllArgsConstructor" in content


# ======================================================================
# AiDocumentTaskResultRepository
# ======================================================================

class TestAiDocumentTaskResultRepository:
    """Req 11.21: AiDocumentTaskResultRepository."""

    def _get_repo(self, generator, config, output_dirs):
        results = generator.generate(config, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "AiDocumentTaskResultRepository" in fp:
                return content
        raise AssertionError("AiDocumentTaskResultRepository not found")

    def test_package_declaration(self, generator, single_task_config, output_dirs):
        content = self._get_repo(generator, single_task_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.repository;" in content

    def test_repository_annotation(self, generator, single_task_config, output_dirs):
        content = self._get_repo(generator, single_task_config, output_dirs)
        assert "@Repository" in content

    def test_extends_reactive_crud(self, generator, single_task_config, output_dirs):
        content = self._get_repo(generator, single_task_config, output_dirs)
        assert "ReactiveCrudRepository<AiDocumentTaskResult, Long>" in content

    def test_find_by_document_id(self, generator, single_task_config, output_dirs):
        content = self._get_repo(generator, single_task_config, output_dirs)
        assert "findByDocumentIdOrderByCreatedAtDesc" in content

    def test_find_by_document_and_task_name(self, generator, single_task_config, output_dirs):
        content = self._get_repo(generator, single_task_config, output_dirs)
        assert "findByDocumentIdAndTaskNameOrderByCreatedAtDesc" in content

    def test_find_by_user_and_task_type(self, generator, single_task_config, output_dirs):
        content = self._get_repo(generator, single_task_config, output_dirs)
        assert "findByUserIdAndTaskTypeOrderByCreatedAtDesc" in content

    def test_find_by_status(self, generator, single_task_config, output_dirs):
        content = self._get_repo(generator, single_task_config, output_dirs)
        assert "findByStatusOrderByCreatedAtDesc" in content

    def test_find_by_id_and_user(self, generator, single_task_config, output_dirs):
        content = self._get_repo(generator, single_task_config, output_dirs)
        assert "findByIdAndUserId" in content


# ======================================================================
# DocumentProcessingService
# ======================================================================

class TestDocumentProcessingService:
    """Req 11.14, 11.17, 11.18: DocumentProcessingService."""

    def _get_service(self, generator, config, output_dirs):
        results = generator.generate(config, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "DocumentProcessingService" in fp:
                return content
        raise AssertionError("DocumentProcessingService not found")

    def test_package_declaration(self, generator, single_task_config, output_dirs):
        content = self._get_service(generator, single_task_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.processing;" in content

    def test_service_annotation(self, generator, single_task_config, output_dirs):
        content = self._get_service(generator, single_task_config, output_dirs)
        assert "@Service" in content

    def test_execute_task_method(self, generator, single_task_config, output_dirs):
        content = self._get_service(generator, single_task_config, output_dirs)
        assert "executeTask" in content

    def test_chain_tasks_method(self, generator, single_task_config, output_dirs):
        content = self._get_service(generator, single_task_config, output_dirs)
        assert "chainTasks" in content

    def test_task_types_map(self, generator, single_task_config, output_dirs):
        content = self._get_service(generator, single_task_config, output_dirs)
        assert "TASK_TYPES" in content
        assert '"docSummary"' in content
        assert '"summarization"' in content

    def test_task_providers_map(self, generator, single_task_config, output_dirs):
        content = self._get_service(generator, single_task_config, output_dirs)
        assert "TASK_PROVIDERS" in content
        assert '"gpt4"' in content

    def test_prompt_template_constant(self, generator, single_task_config, output_dirs):
        content = self._get_service(generator, single_task_config, output_dirs)
        assert "PROMPT_DOCSUMMARY" in content

    def test_chat_client_injection(self, generator, single_task_config, output_dirs):
        content = self._get_service(generator, single_task_config, output_dirs)
        assert '@Qualifier("gpt4")' in content
        assert "ChatClient" in content

    def test_repository_injection(self, generator, single_task_config, output_dirs):
        content = self._get_service(generator, single_task_config, output_dirs)
        assert "AiDocumentTaskResultRepository" in content

    def test_document_repository_injection(self, generator, single_task_config, output_dirs):
        content = self._get_service(generator, single_task_config, output_dirs)
        assert "AiIngestedDocumentRepository" in content

    def test_provider_eligibility_check(self, generator, eligible_providers_config, output_dirs):
        content = self._get_service(generator, eligible_providers_config, output_dirs)
        assert "isProviderEligible" in content
        assert "ELIGIBLE_PROVIDERS_FLEXSUMMARY" in content

    def test_no_eligible_providers_when_not_configured(self, generator, single_task_config, output_dirs):
        content = self._get_service(generator, single_task_config, output_dirs)
        assert "ELIGIBLE_PROVIDERS_" not in content

    def test_target_scope_handling(self, generator, single_task_config, output_dirs):
        content = self._get_service(generator, single_task_config, output_dirs)
        assert "resolveInputText" in content
        assert "page_range" in content
        assert "section" in content
        assert "full_document" in content

    def test_multi_task_all_types_present(self, generator, multi_task_config, output_dirs):
        content = self._get_service(generator, multi_task_config, output_dirs)
        assert '"docSummary"' in content
        assert '"docTranslate"' in content
        assert '"docClassify"' in content
        assert '"docCompare"' in content
        assert '"docQuery"' in content

    def test_multi_task_all_task_types(self, generator, multi_task_config, output_dirs):
        content = self._get_service(generator, multi_task_config, output_dirs)
        assert '"summarization"' in content
        assert '"translation"' in content
        assert '"classification"' in content
        assert '"comparison"' in content
        assert '"querying"' in content

    def test_chain_stops_on_failure(self, generator, single_task_config, output_dirs):
        content = self._get_service(generator, single_task_config, output_dirs)
        assert '"failed"' in content

    def test_execution_duration_tracked(self, generator, single_task_config, output_dirs):
        content = self._get_service(generator, single_task_config, output_dirs)
        assert "executionDurationMs" in content

    def test_get_available_task_types(self, generator, single_task_config, output_dirs):
        content = self._get_service(generator, single_task_config, output_dirs)
        assert "getAvailableTaskTypes" in content

    def test_eligible_providers_in_task_types(self, generator, eligible_providers_config, output_dirs):
        content = self._get_service(generator, eligible_providers_config, output_dirs)
        assert "eligibleProviders" in content
        assert '"gpt4"' in content
        assert '"claude"' in content
        assert '"llama"' in content


# ======================================================================
# DocumentProcessingController
# ======================================================================

class TestDocumentProcessingController:
    """Req 11.23: DocumentProcessingController."""

    def _get_controller(self, generator, config, output_dirs):
        results = generator.generate(config, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "DocumentProcessingController" in fp:
                return content
        raise AssertionError("DocumentProcessingController not found")

    def test_package_declaration(self, generator, single_task_config, output_dirs):
        content = self._get_controller(generator, single_task_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.controller;" in content

    def test_rest_controller_annotation(self, generator, single_task_config, output_dirs):
        content = self._get_controller(generator, single_task_config, output_dirs)
        assert "@RestController" in content

    def test_base_path(self, generator, single_task_config, output_dirs):
        content = self._get_controller(generator, single_task_config, output_dirs)
        assert '"/api/ai/document-processing"' in content

    def test_execute_task_endpoint(self, generator, single_task_config, output_dirs):
        content = self._get_controller(generator, single_task_config, output_dirs)
        assert '@PostMapping("/{documentId}/tasks/{taskName}")' in content

    def test_chain_tasks_endpoint(self, generator, single_task_config, output_dirs):
        content = self._get_controller(generator, single_task_config, output_dirs)
        assert '@PostMapping("/{documentId}/tasks/chain")' in content

    def test_list_task_results_endpoint(self, generator, single_task_config, output_dirs):
        content = self._get_controller(generator, single_task_config, output_dirs)
        assert '@GetMapping("/{documentId}/tasks")' in content

    def test_get_task_result_endpoint(self, generator, single_task_config, output_dirs):
        content = self._get_controller(generator, single_task_config, output_dirs)
        assert '@GetMapping("/tasks/{resultId}")' in content

    def test_get_task_types_endpoint(self, generator, single_task_config, output_dirs):
        content = self._get_controller(generator, single_task_config, output_dirs)
        assert '@GetMapping("/tasks/types")' in content

    def test_delete_task_result_endpoint(self, generator, single_task_config, output_dirs):
        content = self._get_controller(generator, single_task_config, output_dirs)
        assert '@DeleteMapping("/tasks/{resultId}")' in content
        assert "HttpStatus.NO_CONTENT" in content

    def test_http_400_for_bad_task(self, generator, single_task_config, output_dirs):
        content = self._get_controller(generator, single_task_config, output_dirs)
        assert "BAD_REQUEST" in content

    def test_http_404_for_missing_document(self, generator, single_task_config, output_dirs):
        content = self._get_controller(generator, single_task_config, output_dirs)
        assert "NOT_FOUND" in content

    def test_service_injection(self, generator, single_task_config, output_dirs):
        content = self._get_controller(generator, single_task_config, output_dirs)
        assert "DocumentProcessingService" in content

    def test_comparison_comment_when_present(self, generator, multi_task_config, output_dirs):
        content = self._get_controller(generator, multi_task_config, output_dirs)
        assert "Comparison tasks require a secondDocumentId" in content

    def test_no_comparison_comment_when_absent(self, generator, single_task_config, output_dirs):
        content = self._get_controller(generator, single_task_config, output_dirs)
        assert "Comparison tasks" not in content
