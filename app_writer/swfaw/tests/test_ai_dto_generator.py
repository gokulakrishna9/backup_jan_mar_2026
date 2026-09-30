"""Unit tests for the AI AiDtoGenerator.

Verifies that the AiDtoGenerator produces correct Java source files
for shared AI DTOs: request/response DTOs, ClassificationResultDTO.

Requirements: 18.1–18.3
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_dto_generator import AiDtoGenerator


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
    return AiDtoGenerator(jinja_env)


@pytest.fixture
def output_dirs():
    return {
        "dto": Path("com/example/app/ai/dto"),
    }


BASE_PACKAGE = "com.example.app"


def _ai_layer_with_entity():
    """Minimal AI layer with one entity capability."""
    return {
        "entityCapabilities": [
            {"entityName": "Course", "providerName": "gpt", "enabledOperations": ["search"]},
        ],
        "standaloneOperations": [],
    }


def _ai_layer_with_standalone():
    """Minimal AI layer with one standalone operation."""
    return {
        "entityCapabilities": [],
        "standaloneOperations": [
            {"name": "helpBot", "type": "chat", "providerName": "gpt", "basePath": "help"},
        ],
    }


def _ai_layer_with_both():
    """AI layer with both entity capabilities and standalone operations."""
    return {
        "entityCapabilities": [
            {"entityName": "Course", "providerName": "gpt", "enabledOperations": ["search"]},
        ],
        "standaloneOperations": [
            {"name": "helpBot", "type": "chat", "providerName": "gpt", "basePath": "help"},
        ],
    }


def _ai_layer_empty():
    """AI layer with no features configured."""
    return {
        "entityCapabilities": [],
        "standaloneOperations": [],
    }


def _find_content(results, filename):
    """Find the content for a given filename in the results list."""
    for filepath, content in results:
        if filepath.endswith(filename):
            return content
    return None


# ======================================================================
# Test: No generation when no features configured
# ======================================================================


class TestNoGeneration:
    def test_empty_ai_layer_produces_no_files(self, generator, output_dirs):
        results = generator.generate(_ai_layer_empty(), BASE_PACKAGE, output_dirs)
        assert results == []

    def test_missing_keys_produces_no_files(self, generator, output_dirs):
        results = generator.generate({}, BASE_PACKAGE, output_dirs)
        assert results == []


# ======================================================================
# Test: File count and names
# ======================================================================


class TestFileGeneration:
    def test_entity_only_generates_9_files(self, generator, output_dirs):
        results = generator.generate(_ai_layer_with_entity(), BASE_PACKAGE, output_dirs)
        assert len(results) == 9

    def test_standalone_only_generates_9_files(self, generator, output_dirs):
        results = generator.generate(_ai_layer_with_standalone(), BASE_PACKAGE, output_dirs)
        assert len(results) == 9

    def test_both_generates_9_files(self, generator, output_dirs):
        results = generator.generate(_ai_layer_with_both(), BASE_PACKAGE, output_dirs)
        assert len(results) == 9

    def test_all_content_is_nonempty(self, generator, output_dirs):
        results = generator.generate(_ai_layer_with_both(), BASE_PACKAGE, output_dirs)
        for filepath, content in results:
            assert content.strip(), f"Empty content for {filepath}"

    def test_correct_filenames(self, generator, output_dirs):
        results = generator.generate(_ai_layer_with_entity(), BASE_PACKAGE, output_dirs)
        filenames = {Path(fp).name for fp, _ in results}
        expected = {
            "AiSearchRequestDTO.java",
            "AiGenerateRequestDTO.java",
            "AiClassifyRequestDTO.java",
            "AiChatRequestDTO.java",
            "AiChatResponseDTO.java",
            "StandaloneGenerateRequestDTO.java",
            "StandaloneQueryRequestDTO.java",
            "StandaloneQueryResponseDTO.java",
            "ClassificationResultDTO.java",
        }
        assert filenames == expected

    def test_output_dirs_used_in_paths(self, generator, output_dirs):
        results = generator.generate(_ai_layer_with_entity(), BASE_PACKAGE, output_dirs)
        for filepath, _ in results:
            assert filepath.startswith("com/example/app/ai/dto/")


# ======================================================================
# Test: AiSearchRequestDTO (Req 18.1)
# ======================================================================


class TestAiSearchRequestDTO:
    def _get(self, generator, output_dirs):
        results = generator.generate(_ai_layer_with_entity(), BASE_PACKAGE, output_dirs)
        return _find_content(results, "AiSearchRequestDTO.java")

    def test_is_record(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "public record AiSearchRequestDTO" in content

    def test_package_declaration(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "package com.example.app.ai.dto;" in content

    def test_has_query_field(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "String query" in content


# ======================================================================
# Test: AiGenerateRequestDTO (Req 18.1)
# ======================================================================


class TestAiGenerateRequestDTO:
    def _get(self, generator, output_dirs):
        results = generator.generate(_ai_layer_with_entity(), BASE_PACKAGE, output_dirs)
        return _find_content(results, "AiGenerateRequestDTO.java")

    def test_is_record(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "public record AiGenerateRequestDTO" in content

    def test_has_field_name(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "String fieldName" in content

    def test_has_context(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "Map<String, Object> context" in content

    def test_imports_map(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "import java.util.Map;" in content


# ======================================================================
# Test: AiClassifyRequestDTO (Req 18.1)
# ======================================================================


class TestAiClassifyRequestDTO:
    def _get(self, generator, output_dirs):
        results = generator.generate(_ai_layer_with_entity(), BASE_PACKAGE, output_dirs)
        return _find_content(results, "AiClassifyRequestDTO.java")

    def test_is_record(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "public record AiClassifyRequestDTO" in content

    def test_has_categories(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "List<String> categories" in content

    def test_imports_list(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "import java.util.List;" in content


# ======================================================================
# Test: AiChatRequestDTO (Req 18.1)
# ======================================================================


class TestAiChatRequestDTO:
    def _get(self, generator, output_dirs):
        results = generator.generate(_ai_layer_with_entity(), BASE_PACKAGE, output_dirs)
        return _find_content(results, "AiChatRequestDTO.java")

    def test_is_record(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "public record AiChatRequestDTO" in content

    def test_has_session_id(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "Long sessionId" in content

    def test_has_message(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "String message" in content


# ======================================================================
# Test: AiChatResponseDTO (Req 18.1)
# ======================================================================


class TestAiChatResponseDTO:
    def _get(self, generator, output_dirs):
        results = generator.generate(_ai_layer_with_entity(), BASE_PACKAGE, output_dirs)
        return _find_content(results, "AiChatResponseDTO.java")

    def test_is_record(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "public record AiChatResponseDTO" in content

    def test_has_session_id(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "Long sessionId" in content

    def test_has_response(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "String response" in content

    def test_has_timestamp(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "String timestamp" in content


# ======================================================================
# Test: StandaloneGenerateRequestDTO (Req 18.1)
# ======================================================================


class TestStandaloneGenerateRequestDTO:
    def _get(self, generator, output_dirs):
        results = generator.generate(_ai_layer_with_standalone(), BASE_PACKAGE, output_dirs)
        return _find_content(results, "StandaloneGenerateRequestDTO.java")

    def test_is_record(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "public record StandaloneGenerateRequestDTO" in content

    def test_has_prompt(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "String prompt" in content

    def test_has_context(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "Map<String, Object> context" in content


# ======================================================================
# Test: StandaloneQueryRequestDTO (Req 18.1)
# ======================================================================


class TestStandaloneQueryRequestDTO:
    def _get(self, generator, output_dirs):
        results = generator.generate(_ai_layer_with_standalone(), BASE_PACKAGE, output_dirs)
        return _find_content(results, "StandaloneQueryRequestDTO.java")

    def test_is_record(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "public record StandaloneQueryRequestDTO" in content

    def test_has_query(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "String query" in content

    def test_has_parameters(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "Map<String, Object> parameters" in content


# ======================================================================
# Test: StandaloneQueryResponseDTO (Req 18.1)
# ======================================================================


class TestStandaloneQueryResponseDTO:
    def _get(self, generator, output_dirs):
        results = generator.generate(_ai_layer_with_standalone(), BASE_PACKAGE, output_dirs)
        return _find_content(results, "StandaloneQueryResponseDTO.java")

    def test_is_record(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "public record StandaloneQueryResponseDTO" in content

    def test_has_result(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "String result" in content

    def test_has_metadata(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "Map<String, Object> metadata" in content

    def test_has_timestamp(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "String timestamp" in content


# ======================================================================
# Test: ClassificationResultDTO (Req 18.3)
# ======================================================================


class TestClassificationResultDTO:
    def _get(self, generator, output_dirs):
        results = generator.generate(_ai_layer_with_entity(), BASE_PACKAGE, output_dirs)
        return _find_content(results, "ClassificationResultDTO.java")

    def test_is_record(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "public record ClassificationResultDTO" in content

    def test_has_category(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "String category" in content

    def test_has_confidence(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "Double confidence" in content

    def test_has_reasoning(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "String reasoning" in content

    def test_package_declaration(self, generator, output_dirs):
        content = self._get(generator, output_dirs)
        assert "package com.example.app.ai.dto;" in content
