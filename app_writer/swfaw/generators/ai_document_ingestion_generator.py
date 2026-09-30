"""Document Ingestion sub-generator for the AI Layer.

Generates DocumentIngestionService, TikaExtractorService,
AiIngestedDocument entity, AiIngestedDocumentRepository,
DocumentIngestionController, and related DTOs.

Requirements: 11.1–11.13
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2

# Valid source types for document ingestion
VALID_SOURCE_TYPES = {"rest", "folder", "database"}

# Default configuration values
DEFAULT_MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
DEFAULT_AUTO_INDEX_ON_UPLOAD = True


def _pascal_case(name: str) -> str:
    """Convert a camelCase or snake_case name to PascalCase."""
    if "_" in name:
        return "".join(part.capitalize() for part in name.split("_"))
    return name[0].upper() + name[1:] if name else name


def _camel_case(name: str) -> str:
    """Convert a name to camelCase."""
    pascal = _pascal_case(name)
    return pascal[0].lower() + pascal[1:] if pascal else pascal


class DocumentIngestionGenerator:
    """Generates document ingestion Java files from the AI_Layer definition."""

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        document_ingestion: dict | None,
        base_package: str,
        output_dirs: dict[str, Path],
    ) -> list[tuple[str, str]]:
        """Generate document ingestion Java files.

        Returns a list of ``(filepath, content)`` tuples where *filepath* is
        relative to the project source root.

        Req 11.5: When documentIngestion is absent or not enabled, no
        ingestion files are generated.
        """
        if not document_ingestion or not document_ingestion.get("enabled", False):
            return []

        results: list[tuple[str, str]] = []

        ingestion_dir = output_dirs.get("ingestion", Path("ai/ingestion"))
        controller_dir = output_dirs.get("controller", Path("ai/controller"))
        dto_dir = output_dirs.get("dto", Path("ai/dto"))
        entity_dir = output_dirs.get("entity", Path("ai/entity"))
        repository_dir = output_dirs.get("repository", Path("ai/repository"))

        ctx = self._build_ingestion_context(document_ingestion, base_package)

        # 1. TikaExtractionResultDTO (Req 11.7)
        results.append((
            str(dto_dir / "TikaExtractionResultDTO.java"),
            self._render("dto/tika_extraction_result_dto.java.j2", {
                "base_package": base_package,
            }),
        ))

        # 2. IngestedDocumentDTO (Req 11.7)
        results.append((
            str(dto_dir / "IngestedDocumentDTO.java"),
            self._render("dto/ingested_document_dto.java.j2", {
                "base_package": base_package,
            }),
        ))

        # 3. AiIngestedDocument entity (Req 11.8)
        results.append((
            str(entity_dir / "AiIngestedDocument.java"),
            self._render("entity/ai_ingested_document.java.j2", {
                "base_package": base_package,
            }),
        ))

        # 4. AiIngestedDocumentRepository (Req 11.8)
        results.append((
            str(repository_dir / "AiIngestedDocumentRepository.java"),
            self._render("repository/ai_ingested_document_repository.java.j2", {
                "base_package": base_package,
            }),
        ))

        # 5. TikaExtractorService (Req 11.6)
        results.append((
            str(ingestion_dir / "TikaExtractorService.java"),
            self._render("ingestion/tika_extractor_service.java.j2", {
                "base_package": base_package,
            }),
        ))

        # 6. DocumentIngestionService (Req 11.5)
        results.append((
            str(ingestion_dir / "DocumentIngestionService.java"),
            self._render("ingestion/document_ingestion_service.java.j2", ctx),
        ))

        # 7. DocumentIngestionController (Req 11.11)
        results.append((
            str(controller_dir / "DocumentIngestionController.java"),
            self._render("controller/document_ingestion_controller.java.j2", ctx),
        ))

        return results

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_ingestion_context(
        self, document_ingestion: dict, base_package: str
    ) -> dict:
        """Build Jinja2 context for ingestion templates."""
        sources = document_ingestion.get("sources", [])
        processed_sources = []
        has_folder = False
        has_database = False
        has_rest = False

        for src in sources:
            src_type = src.get("type", "rest")
            if src_type == "folder":
                has_folder = True
            elif src_type == "database":
                has_database = True
            elif src_type == "rest":
                has_rest = True

            processed_sources.append({
                "name": src.get("name", ""),
                "name_pascal": _pascal_case(src.get("name", "")),
                "name_camel": _camel_case(src.get("name", "")),
                "type": src_type,
                "folder_path": src.get("folderPath", ""),
                "poll_interval_seconds": src.get("pollIntervalSeconds", 60),
                "table_name": src.get("tableName", ""),
                "blob_column": src.get("blobColumn", ""),
                "file_path_column": src.get("filePathColumn", ""),
                "filename_column": src.get("filenameColumn", ""),
                "filter_clause": src.get("filterClause", ""),
            })

        allowed_mime_types = document_ingestion.get("allowedMimeTypes", [])
        max_file_size_bytes = document_ingestion.get(
            "maxFileSizeBytes", DEFAULT_MAX_FILE_SIZE_BYTES
        )
        max_total_storage_bytes = document_ingestion.get("maxTotalStorageBytes")
        metadata_fields = document_ingestion.get("metadataFields", [])
        auto_index_on_upload = document_ingestion.get(
            "autoIndexOnUpload", DEFAULT_AUTO_INDEX_ON_UPLOAD
        )
        target_rag_source_name = document_ingestion.get("targetRagSourceName")

        return {
            "base_package": base_package,
            "sources": processed_sources,
            "has_folder_source": has_folder,
            "has_database_source": has_database,
            "has_rest_source": has_rest,
            "allowed_mime_types": allowed_mime_types,
            "max_file_size_bytes": max_file_size_bytes,
            "max_total_storage_bytes": max_total_storage_bytes,
            "metadata_fields": metadata_fields,
            "auto_index_on_upload": auto_index_on_upload,
            "target_rag_source_name": target_rag_source_name,
        }

    def _render(self, template_name: str, ctx: dict) -> str:
        """Render a Jinja2 template under the ai/ prefix."""
        template = self.jinja_env.get_template(f"ai/{template_name}")
        return template.render(**ctx)
