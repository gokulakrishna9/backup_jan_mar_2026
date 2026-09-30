"""Document Processing sub-generator for the AI Layer.

Generates DocumentProcessingService, AiDocumentTaskResult entity,
AiDocumentTaskResultRepository, DocumentProcessingController,
and related DTOs.

Requirements: 11.14–11.28
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2

# All 12 valid task types (Req 11.14)
VALID_TASK_TYPES = frozenset({
    "summarization",
    "composition",
    "querying",
    "translation",
    "key_info_extraction",
    "sentiment_analysis",
    "classification",
    "comparison",
    "redaction_suggestions",
    "action_item_extraction",
    "table_extraction",
    "outline_generation",
})

# Task types requiring specific config
TASK_TYPE_REQUIRES_TARGET_LANGUAGE = {"translation"}
TASK_TYPE_REQUIRES_CATEGORIES = {"classification"}
TASK_TYPE_REQUIRES_SECOND_DOCUMENT = {"comparison"}

# Valid target scopes (Req 11.18)
VALID_TARGET_SCOPES = {"full_document", "page_range", "section"}


def _pascal_case(name: str) -> str:
    """Convert a camelCase or snake_case name to PascalCase."""
    if "_" in name:
        return "".join(part.capitalize() for part in name.split("_"))
    return name[0].upper() + name[1:] if name else name


def _camel_case(name: str) -> str:
    """Convert a name to camelCase."""
    pascal = _pascal_case(name)
    return pascal[0].lower() + pascal[1:] if pascal else pascal


class DocumentProcessingGenerator:
    """Generates document processing Java files from the AI_Layer definition."""

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        document_processing: dict | None,
        base_package: str,
        output_dirs: dict[str, Path],
    ) -> list[tuple[str, str]]:
        """Generate document processing Java files.

        Returns a list of ``(filepath, content)`` tuples where *filepath* is
        relative to the project source root.

        Req 11.17: When documentProcessing is absent or not enabled, no
        processing files are generated.
        """
        if not document_processing or not document_processing.get("enabled", False):
            return []

        results: list[tuple[str, str]] = []

        processing_dir = output_dirs.get("processing", Path("ai/processing"))
        controller_dir = output_dirs.get("controller", Path("ai/controller"))
        dto_dir = output_dirs.get("dto", Path("ai/dto"))
        entity_dir = output_dirs.get("entity", Path("ai/entity"))
        repository_dir = output_dirs.get("repository", Path("ai/repository"))

        ctx = self._build_processing_context(document_processing, base_package)

        # 1. DocumentTaskRequestDTO (Req 11.20)
        results.append((
            str(dto_dir / "DocumentTaskRequestDTO.java"),
            self._render("dto/document_task_request_dto.java.j2", {
                "base_package": base_package,
            }),
        ))

        # 2. DocumentTaskResultDTO (Req 11.20)
        results.append((
            str(dto_dir / "DocumentTaskResultDTO.java"),
            self._render("dto/document_task_result_dto.java.j2", {
                "base_package": base_package,
            }),
        ))

        # 3. AiDocumentTaskResult entity (Req 11.21)
        results.append((
            str(entity_dir / "AiDocumentTaskResult.java"),
            self._render("entity/ai_document_task_result.java.j2", {
                "base_package": base_package,
            }),
        ))

        # 4. AiDocumentTaskResultRepository (Req 11.21)
        results.append((
            str(repository_dir / "AiDocumentTaskResultRepository.java"),
            self._render("repository/ai_document_task_result_repository.java.j2", {
                "base_package": base_package,
            }),
        ))

        # 5. DocumentProcessingService (Req 11.17)
        results.append((
            str(processing_dir / "DocumentProcessingService.java"),
            self._render("processing/document_processing_service.java.j2", ctx),
        ))

        # 6. DocumentProcessingController (Req 11.23)
        results.append((
            str(controller_dir / "DocumentProcessingController.java"),
            self._render("controller/document_processing_controller.java.j2", ctx),
        ))

        return results

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_processing_context(
        self, document_processing: dict, base_package: str
    ) -> dict:
        """Build Jinja2 context for processing templates."""
        tasks = document_processing.get("tasks", [])
        default_provider_name = document_processing.get("defaultProviderName")

        processed_tasks = []
        has_comparison = False
        has_translation = False
        has_classification = False
        has_querying = False

        for task in tasks:
            task_type = task.get("taskType", "")
            if task_type == "comparison":
                has_comparison = True
            if task_type == "translation":
                has_translation = True
            if task_type == "classification":
                has_classification = True
            if task_type == "querying":
                has_querying = True

            processed_tasks.append({
                "name": task.get("name", ""),
                "name_pascal": _pascal_case(task.get("name", "")),
                "name_camel": _camel_case(task.get("name", "")),
                "task_type": task_type,
                "provider_name": task.get("providerName", default_provider_name or ""),
                "eligible_providers": task.get("eligibleProviders", []),
                "prompt_template": task.get("promptTemplate", ""),
                "chat_options": task.get("chatOptions"),
                "response_format": task.get("responseFormat"),
                "target_scope": task.get("targetScope"),
                # Task-type-specific config
                "target_language": task.get("targetLanguage", ""),
                "categories": task.get("categories", []),
                "requires_second_document": task.get("requiresSecondDocument", False),
            })

        return {
            "base_package": base_package,
            "tasks": processed_tasks,
            "default_provider_name": default_provider_name,
            "has_comparison_task": has_comparison,
            "has_translation_task": has_translation,
            "has_classification_task": has_classification,
            "has_querying_task": has_querying,
        }

    def _render(self, template_name: str, ctx: dict) -> str:
        """Render a Jinja2 template under the ai/ prefix."""
        template = self.jinja_env.get_template(f"ai/{template_name}")
        return template.render(**ctx)
