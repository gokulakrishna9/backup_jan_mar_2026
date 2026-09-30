"""Unit tests for the AI DocumentIngestionGenerator.

Verifies that the DocumentIngestionGenerator produces correct Java source files
for DocumentIngestionService, TikaExtractorService, AiIngestedDocument entity,
AiIngestedDocumentRepository, DocumentIngestionController, and related DTOs.

Requirements: 11.1–11.13
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_document_ingestion_generator import (
    DocumentIngestionGenerator,
    _pascal_case,
    _camel_case,
    VALID_SOURCE_TYPES,
    DEFAULT_MAX_FILE_SIZE_BYTES,
    DEFAULT_AUTO_INDEX_ON_UPLOAD,
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
    return DocumentIngestionGenerator(jinja_env)


@pytest.fixture
def rest_only_config():
    """Document ingestion config with only REST source."""
    return {
        "enabled": True,
        "allowedMimeTypes": ["application/pdf", "text/plain"],
        "maxFileSizeBytes": 10485760,
        "metadataFields": ["author", "department"],
        "autoIndexOnUpload": True,
        "targetRagSourceName": "docEmbeddings",
        "sources": [
            {"name": "restUpload", "type": "rest"},
        ],
    }


@pytest.fixture
def folder_config():
    """Document ingestion config with a folder source."""
    return {
        "enabled": True,
        "allowedMimeTypes": ["application/pdf"],
        "maxFileSizeBytes": 5242880,
        "metadataFields": [],
        "autoIndexOnUpload": False,
        "sources": [
            {
                "name": "sharedDocs",
                "type": "folder",
                "folderPath": "/data/shared-docs",
                "pollIntervalSeconds": 120,
            },
        ],
    }


@pytest.fixture
def database_config():
    """Document ingestion config with a database source."""
    return {
        "enabled": True,
        "allowedMimeTypes": ["application/pdf", "text/plain"],
        "maxFileSizeBytes": 10485760,
        "maxTotalStorageBytes": 1073741824,
        "metadataFields": ["category"],
        "autoIndexOnUpload": True,
        "targetRagSourceName": "docSearch",
        "sources": [
            {
                "name": "legacyDocs",
                "type": "database",
                "tableName": "legacy_documents",
                "blobColumn": "file_data",
                "filePathColumn": "file_path",
                "filenameColumn": "file_name",
                "filterClause": "status = 'active'",
            },
        ],
    }


@pytest.fixture
def mixed_config():
    """Document ingestion config with all three source types."""
    return {
        "enabled": True,
        "allowedMimeTypes": ["application/pdf", "text/plain", "text/html"],
        "maxFileSizeBytes": 20971520,
        "maxTotalStorageBytes": 5368709120,
        "metadataFields": ["author", "department", "category"],
        "autoIndexOnUpload": True,
        "targetRagSourceName": "allDocs",
        "sources": [
            {"name": "restUpload", "type": "rest"},
            {
                "name": "sharedDocs",
                "type": "folder",
                "folderPath": "/data/shared",
                "pollIntervalSeconds": 60,
            },
            {
                "name": "legacyDocs",
                "type": "database",
                "tableName": "legacy_documents",
                "blobColumn": "file_data",
                "filePathColumn": "file_path",
                "filenameColumn": "file_name",
                "filterClause": "active = 1",
            },
        ],
    }


@pytest.fixture
def disabled_config():
    """Document ingestion config that is disabled."""
    return {
        "enabled": False,
        "allowedMimeTypes": ["application/pdf"],
        "sources": [],
    }


@pytest.fixture
def output_dirs():
    return {
        "ingestion": Path("com/example/app/ai/ingestion"),
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
        assert _pascal_case("restUpload") == "RestUpload"

    def test_pascal_case_snake(self):
        assert _pascal_case("shared_docs") == "SharedDocs"

    def test_pascal_case_single(self):
        assert _pascal_case("docs") == "Docs"

    def test_pascal_case_empty(self):
        assert _pascal_case("") == ""

    def test_camel_case(self):
        assert _camel_case("RestUpload") == "restUpload"

    def test_camel_case_snake(self):
        assert _camel_case("shared_docs") == "sharedDocs"

    def test_valid_source_types(self):
        assert VALID_SOURCE_TYPES == {"rest", "folder", "database"}

    def test_default_max_file_size(self):
        assert DEFAULT_MAX_FILE_SIZE_BYTES == 10 * 1024 * 1024

    def test_default_auto_index(self):
        assert DEFAULT_AUTO_INDEX_ON_UPLOAD is True


# ======================================================================
# Generate method — conditional generation
# ======================================================================

class TestDocumentIngestionGeneratorGenerate:
    """Req 11.5: When documentIngestion is absent or not enabled, no files."""

    def test_no_files_when_none(self, generator, output_dirs):
        results = generator.generate(None, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_no_files_when_disabled(self, generator, disabled_config, output_dirs):
        results = generator.generate(disabled_config, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_no_files_when_empty_dict(self, generator, output_dirs):
        results = generator.generate({}, BASE_PACKAGE, output_dirs)
        assert results == []

    def test_rest_only_generates_seven_files(self, generator, rest_only_config, output_dirs):
        results = generator.generate(rest_only_config, BASE_PACKAGE, output_dirs)
        assert len(results) == 7

    def test_folder_config_generates_seven_files(self, generator, folder_config, output_dirs):
        results = generator.generate(folder_config, BASE_PACKAGE, output_dirs)
        assert len(results) == 7

    def test_database_config_generates_seven_files(self, generator, database_config, output_dirs):
        results = generator.generate(database_config, BASE_PACKAGE, output_dirs)
        assert len(results) == 7

    def test_mixed_config_generates_seven_files(self, generator, mixed_config, output_dirs):
        results = generator.generate(mixed_config, BASE_PACKAGE, output_dirs)
        assert len(results) == 7

    def test_all_content_is_nonempty(self, generator, rest_only_config, output_dirs):
        results = generator.generate(rest_only_config, BASE_PACKAGE, output_dirs)
        for filepath, content in results:
            assert content.strip(), f"Empty content for {filepath}"

    def test_output_dirs_used_in_paths(self, generator, rest_only_config, output_dirs):
        results = generator.generate(rest_only_config, BASE_PACKAGE, output_dirs)
        paths = [fp for fp, _ in results]
        assert any("ai/dto" in p for p in paths)
        assert any("ai/entity" in p for p in paths)
        assert any("ai/repository" in p for p in paths)
        assert any("ai/ingestion" in p for p in paths)
        assert any("ai/controller" in p for p in paths)

    def test_correct_filenames(self, generator, rest_only_config, output_dirs):
        results = generator.generate(rest_only_config, BASE_PACKAGE, output_dirs)
        filenames = [Path(fp).name for fp, _ in results]
        assert "TikaExtractionResultDTO.java" in filenames
        assert "IngestedDocumentDTO.java" in filenames
        assert "AiIngestedDocument.java" in filenames
        assert "AiIngestedDocumentRepository.java" in filenames
        assert "TikaExtractorService.java" in filenames
        assert "DocumentIngestionService.java" in filenames
        assert "DocumentIngestionController.java" in filenames


# ======================================================================
# TikaExtractionResultDTO
# ======================================================================

class TestTikaExtractionResultDTO:
    """Req 11.7: TikaExtractionResultDTO."""

    def _get_dto(self, generator, config, output_dirs):
        results = generator.generate(config, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "TikaExtractionResultDTO" in fp:
                return content
        raise AssertionError("TikaExtractionResultDTO not found")

    def test_is_record(self, generator, rest_only_config, output_dirs):
        content = self._get_dto(generator, rest_only_config, output_dirs)
        assert "public record TikaExtractionResultDTO" in content

    def test_package_declaration(self, generator, rest_only_config, output_dirs):
        content = self._get_dto(generator, rest_only_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.dto;" in content

    def test_has_extracted_text(self, generator, rest_only_config, output_dirs):
        content = self._get_dto(generator, rest_only_config, output_dirs)
        assert "extractedText" in content

    def test_has_detected_mime_type(self, generator, rest_only_config, output_dirs):
        content = self._get_dto(generator, rest_only_config, output_dirs)
        assert "detectedMimeType" in content

    def test_has_detected_language(self, generator, rest_only_config, output_dirs):
        content = self._get_dto(generator, rest_only_config, output_dirs)
        assert "detectedLanguage" in content

    def test_has_metadata(self, generator, rest_only_config, output_dirs):
        content = self._get_dto(generator, rest_only_config, output_dirs)
        assert "metadata" in content

    def test_has_error(self, generator, rest_only_config, output_dirs):
        content = self._get_dto(generator, rest_only_config, output_dirs)
        assert "error" in content


# ======================================================================
# IngestedDocumentDTO
# ======================================================================

class TestIngestedDocumentDTO:
    """Req 11.7: IngestedDocumentDTO."""

    def _get_dto(self, generator, config, output_dirs):
        results = generator.generate(config, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "IngestedDocumentDTO" in fp:
                return content
        raise AssertionError("IngestedDocumentDTO not found")

    def test_is_record(self, generator, rest_only_config, output_dirs):
        content = self._get_dto(generator, rest_only_config, output_dirs)
        assert "public record IngestedDocumentDTO" in content

    def test_package_declaration(self, generator, rest_only_config, output_dirs):
        content = self._get_dto(generator, rest_only_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.dto;" in content

    def test_has_id(self, generator, rest_only_config, output_dirs):
        content = self._get_dto(generator, rest_only_config, output_dirs)
        assert "Long id" in content

    def test_has_user_id(self, generator, rest_only_config, output_dirs):
        content = self._get_dto(generator, rest_only_config, output_dirs)
        assert "Long userId" in content

    def test_has_filename(self, generator, rest_only_config, output_dirs):
        content = self._get_dto(generator, rest_only_config, output_dirs)
        assert "String filename" in content

    def test_has_mime_type(self, generator, rest_only_config, output_dirs):
        content = self._get_dto(generator, rest_only_config, output_dirs)
        assert "String mimeType" in content

    def test_has_extraction_status(self, generator, rest_only_config, output_dirs):
        content = self._get_dto(generator, rest_only_config, output_dirs)
        assert "String extractionStatus" in content

    def test_has_rag_indexed(self, generator, rest_only_config, output_dirs):
        content = self._get_dto(generator, rest_only_config, output_dirs)
        assert "Boolean ragIndexed" in content


# ======================================================================
# AiIngestedDocument entity
# ======================================================================

class TestAiIngestedDocumentEntity:
    """Req 11.8: AiIngestedDocument entity."""

    def _get_entity(self, generator, config, output_dirs):
        results = generator.generate(config, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "AiIngestedDocument.java" in fp and "Repository" not in fp:
                return content
        raise AssertionError("AiIngestedDocument entity not found")

    def test_package_declaration(self, generator, rest_only_config, output_dirs):
        content = self._get_entity(generator, rest_only_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.entity;" in content

    def test_table_annotation(self, generator, rest_only_config, output_dirs):
        content = self._get_entity(generator, rest_only_config, output_dirs)
        assert '@Table("ai_ingested_document")' in content

    def test_has_id(self, generator, rest_only_config, output_dirs):
        content = self._get_entity(generator, rest_only_config, output_dirs)
        assert "@Id" in content
        assert "private Long id;" in content

    def test_has_user_id(self, generator, rest_only_config, output_dirs):
        content = self._get_entity(generator, rest_only_config, output_dirs)
        assert '"user_id"' in content

    def test_has_filename(self, generator, rest_only_config, output_dirs):
        content = self._get_entity(generator, rest_only_config, output_dirs)
        assert "private String filename;" in content

    def test_has_mime_type(self, generator, rest_only_config, output_dirs):
        content = self._get_entity(generator, rest_only_config, output_dirs)
        assert '"mime_type"' in content

    def test_has_file_size_bytes(self, generator, rest_only_config, output_dirs):
        content = self._get_entity(generator, rest_only_config, output_dirs)
        assert '"file_size_bytes"' in content

    def test_has_extracted_text(self, generator, rest_only_config, output_dirs):
        content = self._get_entity(generator, rest_only_config, output_dirs)
        assert '"extracted_text"' in content

    def test_has_extraction_status(self, generator, rest_only_config, output_dirs):
        content = self._get_entity(generator, rest_only_config, output_dirs)
        assert '"extraction_status"' in content

    def test_has_rag_source_name(self, generator, rest_only_config, output_dirs):
        content = self._get_entity(generator, rest_only_config, output_dirs)
        assert '"rag_source_name"' in content

    def test_has_rag_indexed(self, generator, rest_only_config, output_dirs):
        content = self._get_entity(generator, rest_only_config, output_dirs)
        assert '"rag_indexed"' in content

    def test_has_timestamps(self, generator, rest_only_config, output_dirs):
        content = self._get_entity(generator, rest_only_config, output_dirs)
        assert '"created_at"' in content
        assert '"updated_at"' in content

    def test_lombok_annotations(self, generator, rest_only_config, output_dirs):
        content = self._get_entity(generator, rest_only_config, output_dirs)
        assert "@Data" in content
        assert "@Builder" in content
        assert "@NoArgsConstructor" in content
        assert "@AllArgsConstructor" in content


# ======================================================================
# AiIngestedDocumentRepository
# ======================================================================

class TestAiIngestedDocumentRepository:
    """Req 11.8: AiIngestedDocumentRepository."""

    def _get_repo(self, generator, config, output_dirs):
        results = generator.generate(config, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "AiIngestedDocumentRepository" in fp:
                return content
        raise AssertionError("AiIngestedDocumentRepository not found")

    def test_package_declaration(self, generator, rest_only_config, output_dirs):
        content = self._get_repo(generator, rest_only_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.repository;" in content

    def test_repository_annotation(self, generator, rest_only_config, output_dirs):
        content = self._get_repo(generator, rest_only_config, output_dirs)
        assert "@Repository" in content

    def test_extends_reactive_crud(self, generator, rest_only_config, output_dirs):
        content = self._get_repo(generator, rest_only_config, output_dirs)
        assert "ReactiveCrudRepository<AiIngestedDocument, Long>" in content

    def test_find_by_user_id(self, generator, rest_only_config, output_dirs):
        content = self._get_repo(generator, rest_only_config, output_dirs)
        assert "findByUserIdOrderByCreatedAtDesc" in content

    def test_find_by_upload_source(self, generator, rest_only_config, output_dirs):
        content = self._get_repo(generator, rest_only_config, output_dirs)
        assert "findByUploadSourceOrderByCreatedAtDesc" in content

    def test_find_by_extraction_status(self, generator, rest_only_config, output_dirs):
        content = self._get_repo(generator, rest_only_config, output_dirs)
        assert "findByExtractionStatusOrderByCreatedAtDesc" in content

    def test_find_by_rag_source(self, generator, rest_only_config, output_dirs):
        content = self._get_repo(generator, rest_only_config, output_dirs)
        assert "findByRagSourceNameAndRagIndexedOrderByCreatedAtDesc" in content


# ======================================================================
# TikaExtractorService
# ======================================================================

class TestTikaExtractorService:
    """Req 11.6: TikaExtractorService."""

    def _get_service(self, generator, config, output_dirs):
        results = generator.generate(config, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "TikaExtractorService" in fp:
                return content
        raise AssertionError("TikaExtractorService not found")

    def test_package_declaration(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.ingestion;" in content

    def test_service_annotation(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "@Service" in content

    def test_extract_method(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "public Mono<TikaExtractionResultDTO> extract(byte[] documentBytes, String filename)" in content

    def test_tika_import(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "org.apache.tika" in content

    def test_returns_mono(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "Mono<TikaExtractionResultDTO>" in content

    def test_error_handling(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "catch (Exception e)" in content

    def test_bounded_elastic_scheduler(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "Schedulers.boundedElastic()" in content


# ======================================================================
# DocumentIngestionService
# ======================================================================

class TestDocumentIngestionService:
    """Req 11.1, 11.2, 11.3, 11.5: DocumentIngestionService."""

    def _get_service(self, generator, config, output_dirs):
        results = generator.generate(config, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "DocumentIngestionService" in fp:
                return content
        raise AssertionError("DocumentIngestionService not found")

    def test_package_declaration(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.ingestion;" in content

    def test_service_annotation(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "@Service" in content

    def test_ingest_from_rest_method(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "ingestFromRest" in content

    def test_re_extract_method(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "reExtract" in content

    def test_allowed_mime_types(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "application/pdf" in content
        assert "text/plain" in content

    def test_max_file_size(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "10485760L" in content

    def test_mime_validation(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "Unsupported MIME type" in content

    def test_size_validation(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "exceeds maximum" in content

    def test_auto_index_with_rag(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "RagIndexingService" in content
        assert "docEmbeddings" in content

    def test_no_auto_index_when_disabled(self, generator, folder_config, output_dirs):
        content = self._get_service(generator, folder_config, output_dirs)
        assert "RagIndexingService" not in content

    def test_folder_source_present(self, generator, folder_config, output_dirs):
        content = self._get_service(generator, folder_config, output_dirs)
        assert "ingestFromFolder" in content
        assert "/data/shared-docs" in content

    def test_no_folder_method_when_no_folder_source(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "ingestFromFolder" not in content

    def test_database_source_present(self, generator, database_config, output_dirs):
        content = self._get_service(generator, database_config, output_dirs)
        assert "ingestFromDatabase" in content
        assert "legacy_documents" in content

    def test_no_database_method_when_no_db_source(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "ingestFromDatabase" not in content

    def test_max_total_storage_when_configured(self, generator, database_config, output_dirs):
        content = self._get_service(generator, database_config, output_dirs)
        assert "MAX_TOTAL_STORAGE_BYTES" in content
        assert "1073741824L" in content

    def test_no_max_total_storage_when_absent(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "MAX_TOTAL_STORAGE_BYTES" not in content

    def test_mixed_sources_all_methods(self, generator, mixed_config, output_dirs):
        content = self._get_service(generator, mixed_config, output_dirs)
        assert "ingestFromRest" in content
        assert "ingestFromFolder" in content
        assert "ingestFromDatabase" in content

    def test_tika_extractor_injection(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "TikaExtractorService" in content

    def test_repository_injection(self, generator, rest_only_config, output_dirs):
        content = self._get_service(generator, rest_only_config, output_dirs)
        assert "AiIngestedDocumentRepository" in content


# ======================================================================
# DocumentIngestionController
# ======================================================================

class TestDocumentIngestionController:
    """Req 11.11: DocumentIngestionController."""

    def _get_controller(self, generator, config, output_dirs):
        results = generator.generate(config, BASE_PACKAGE, output_dirs)
        for fp, content in results:
            if "DocumentIngestionController" in fp:
                return content
        raise AssertionError("DocumentIngestionController not found")

    def test_package_declaration(self, generator, rest_only_config, output_dirs):
        content = self._get_controller(generator, rest_only_config, output_dirs)
        assert f"package {BASE_PACKAGE}.ai.controller;" in content

    def test_rest_controller_annotation(self, generator, rest_only_config, output_dirs):
        content = self._get_controller(generator, rest_only_config, output_dirs)
        assert "@RestController" in content

    def test_base_path(self, generator, rest_only_config, output_dirs):
        content = self._get_controller(generator, rest_only_config, output_dirs)
        assert '"/api/ai/documents"' in content

    def test_upload_endpoint(self, generator, rest_only_config, output_dirs):
        content = self._get_controller(generator, rest_only_config, output_dirs)
        assert '@PostMapping(value = "/upload"' in content
        assert "MULTIPART_FORM_DATA_VALUE" in content

    def test_list_endpoint(self, generator, rest_only_config, output_dirs):
        content = self._get_controller(generator, rest_only_config, output_dirs)
        assert "@GetMapping" in content
        assert "listDocuments" in content

    def test_get_by_id_endpoint(self, generator, rest_only_config, output_dirs):
        content = self._get_controller(generator, rest_only_config, output_dirs)
        assert '@GetMapping("/{documentId}")' in content

    def test_delete_endpoint(self, generator, rest_only_config, output_dirs):
        content = self._get_controller(generator, rest_only_config, output_dirs)
        assert '@DeleteMapping("/{documentId}")' in content
        assert "HttpStatus.NO_CONTENT" in content

    def test_re_extract_endpoint(self, generator, rest_only_config, output_dirs):
        content = self._get_controller(generator, rest_only_config, output_dirs)
        assert "re-extract" in content

    def test_folder_endpoint_present(self, generator, folder_config, output_dirs):
        content = self._get_controller(generator, folder_config, output_dirs)
        assert "ingest-folder" in content

    def test_no_folder_endpoint_when_no_folder_source(self, generator, rest_only_config, output_dirs):
        content = self._get_controller(generator, rest_only_config, output_dirs)
        assert "ingest-folder" not in content

    def test_database_endpoint_present(self, generator, database_config, output_dirs):
        content = self._get_controller(generator, database_config, output_dirs)
        assert "ingest-database" in content

    def test_no_database_endpoint_when_no_db_source(self, generator, rest_only_config, output_dirs):
        content = self._get_controller(generator, rest_only_config, output_dirs)
        assert "ingest-database" not in content

    def test_mixed_all_endpoints(self, generator, mixed_config, output_dirs):
        content = self._get_controller(generator, mixed_config, output_dirs)
        assert "upload" in content
        assert "ingest-folder" in content
        assert "ingest-database" in content

    def test_http_400_for_bad_mime(self, generator, rest_only_config, output_dirs):
        content = self._get_controller(generator, rest_only_config, output_dirs)
        assert "BAD_REQUEST" in content

    def test_http_413_for_oversized(self, generator, rest_only_config, output_dirs):
        content = self._get_controller(generator, rest_only_config, output_dirs)
        assert "PAYLOAD_TOO_LARGE" in content

    def test_service_injection(self, generator, rest_only_config, output_dirs):
        content = self._get_controller(generator, rest_only_config, output_dirs)
        assert "DocumentIngestionService" in content
