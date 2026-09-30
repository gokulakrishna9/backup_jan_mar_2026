"""Unit tests for the AI TypedResponseGenerator.

Verifies that the TypedResponseGenerator produces correct Java source files
for TypedResponseResult<T>, TypedResponseDeserializer, ParameterizedTypeReference
constants, and TypedResponseDeserializationException, with conditional generation
based on responseType configuration.

Requirements: 7.1–7.18
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_typed_response_generator import TypedResponseGenerator


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
    return TypedResponseGenerator(jinja_env)


@pytest.fixture
def output_dirs():
    return {
        "dto": Path("com/example/app/ai/dto"),
        "service": Path("com/example/app/ai/service"),
        "provider": Path("com/example/app/ai/provider"),
    }


BASE_PACKAGE = "com.example.app"


@pytest.fixture
def entity_with_response_type():
    """Entity capability with responseType configured."""
    return [
        {
            "entityName": "Course",
            "providerName": "mainGpt",
            "enabledOperations": ["search", "classify"],
            "searchableFields": ["title"],
            "responseType": {
                "className": "CourseOutputDTO",
                "wrapper": "list",
                "fallbackBehavior": "raw_string",
            },
        }
    ]


@pytest.fixture
def entity_with_default_classname():
    """Entity capability with responseType but no explicit className (defaults to DTO)."""
    return [
        {
            "entityName": "Article",
            "providerName": "mainGpt",
            "enabledOperations": ["search"],
            "searchableFields": ["title"],
            "responseType": {
                "wrapper": "none",
                "fallbackBehavior": "throw",
            },
        }
    ]


@pytest.fixture
def standalone_with_response_type():
    """Standalone operation with responseType configured."""
    return [
        {
            "name": "dataAnalyzer",
            "providerName": "mainGpt",
            "basePath": "data-analyzer",
            "systemPrompt": "Analyze data.",
            "enabledActions": ["query"],
            "responseType": {
                "className": "AnalysisResultDTO",
                "wrapper": "none",
                "fallbackBehavior": "default_object",
            },
        }
    ]


@pytest.fixture
def entity_no_response_type():
    """Entity capability without responseType."""
    return [
        {
            "entityName": "Course",
            "providerName": "mainGpt",
            "enabledOperations": ["search"],
            "searchableFields": ["title"],
        }
    ]


@pytest.fixture
def standalone_no_response_type():
    """Standalone operation without responseType."""
    return [
        {
            "name": "codeHelper",
            "providerName": "mainGpt",
            "basePath": "code-helper",
            "systemPrompt": "Help.",
            "enabledActions": ["chat"],
        }
    ]


class TestTypedResponseGeneratorGenerate:
    """Tests for the generate() method."""

    def test_generates_four_files_when_response_type_present(
        self, generator, entity_with_response_type, output_dirs
    ):
        """Req 7.14: Generates all typed response files."""
        results = generator.generate(
            entity_with_response_type, [], BASE_PACKAGE, output_dirs,
        )
        assert len(results) == 4

    def test_generates_correct_filenames(
        self, generator, entity_with_response_type, output_dirs
    ):
        results = generator.generate(
            entity_with_response_type, [], BASE_PACKAGE, output_dirs,
        )
        filenames = [r[0] for r in results]
        assert any("TypedResponseResult.java" in f for f in filenames)
        assert any("TypedResponseDeserializer.java" in f for f in filenames)
        assert any("TypedResponseDeserializationException.java" in f for f in filenames)
        assert any("AiTypeReferences.java" in f for f in filenames)

    def test_all_content_is_nonempty(
        self, generator, entity_with_response_type, output_dirs
    ):
        results = generator.generate(
            entity_with_response_type, [], BASE_PACKAGE, output_dirs,
        )
        for filepath, content in results:
            assert content.strip(), f"Empty content for {filepath}"

    def test_no_files_when_no_response_type(
        self, generator, entity_no_response_type, standalone_no_response_type, output_dirs
    ):
        """Req 7.17: No typed response files when responseType not configured."""
        results = generator.generate(
            entity_no_response_type, standalone_no_response_type,
            BASE_PACKAGE, output_dirs,
        )
        assert results == []

    def test_empty_inputs_returns_empty(self, generator, output_dirs):
        results = generator.generate([], [], BASE_PACKAGE, output_dirs)
        assert results == []

    def test_standalone_response_type_generates_files(
        self, generator, standalone_with_response_type, output_dirs
    ):
        """Req 7.2: Standalone operations with responseType generate files."""
        results = generator.generate(
            [], standalone_with_response_type, BASE_PACKAGE, output_dirs,
        )
        assert len(results) == 4

    def test_combined_entity_and_standalone(
        self, generator, entity_with_response_type,
        standalone_with_response_type, output_dirs,
    ):
        """Both entity and standalone responseTypes produce files."""
        results = generator.generate(
            entity_with_response_type, standalone_with_response_type,
            BASE_PACKAGE, output_dirs,
        )
        assert len(results) == 4  # Still 4 files, but constants include both types

    def test_output_dirs_used_in_paths(
        self, generator, entity_with_response_type, output_dirs
    ):
        results = generator.generate(
            entity_with_response_type, [], BASE_PACKAGE, output_dirs,
        )
        for filepath, _ in results:
            assert filepath.startswith("com/example/app/ai/")

    def test_default_output_dirs(self, generator, entity_with_response_type):
        results = generator.generate(
            entity_with_response_type, [], BASE_PACKAGE, {},
        )
        filenames = [r[0] for r in results]
        assert any("ai/dto/TypedResponseResult.java" in f for f in filenames)
        assert any("ai/service/TypedResponseDeserializer.java" in f for f in filenames)
        assert any("ai/provider/TypedResponseDeserializationException.java" in f for f in filenames)
        assert any("ai/service/AiTypeReferences.java" in f for f in filenames)

    def test_deduplicates_same_response_type(self, generator, output_dirs):
        """Same className+wrapper from different sources is deduplicated."""
        entities = [
            {
                "entityName": "Course",
                "providerName": "gpt",
                "enabledOperations": ["search"],
                "searchableFields": ["title"],
                "responseType": {"className": "SharedDTO", "wrapper": "list", "fallbackBehavior": "throw"},
            },
            {
                "entityName": "Article",
                "providerName": "gpt",
                "enabledOperations": ["search"],
                "searchableFields": ["body"],
                "responseType": {"className": "SharedDTO", "wrapper": "list", "fallbackBehavior": "raw_string"},
            },
        ]
        results = generator.generate(entities, [], BASE_PACKAGE, output_dirs)
        # Find the AiTypeReferences content
        for filepath, content in results:
            if "AiTypeReferences" in filepath:
                # Should have only one constant for SharedDTO list
                assert content.count("SHARED_D_T_O_LIST_TYPE") == 1


class TestTypedResponseResult:
    """Tests for the generated TypedResponseResult<T> DTO template."""

    def _render_dto(self, generator, entities, standalone=None):
        output_dirs = {
            "dto": Path("ai/dto"),
            "service": Path("ai/service"),
            "provider": Path("ai/provider"),
        }
        results = generator.generate(
            entities, standalone or [], BASE_PACKAGE, output_dirs,
        )
        for filepath, content in results:
            if "TypedResponseResult.java" in filepath:
                return content
        return ""

    def test_package_declaration(self, generator, entity_with_response_type):
        content = self._render_dto(generator, entity_with_response_type)
        assert "package com.example.app.ai.dto;" in content

    def test_class_name(self, generator, entity_with_response_type):
        content = self._render_dto(generator, entity_with_response_type)
        assert "public class TypedResponseResult<T>" in content

    def test_success_field(self, generator, entity_with_response_type):
        content = self._render_dto(generator, entity_with_response_type)
        assert "private boolean success;" in content

    def test_data_field(self, generator, entity_with_response_type):
        content = self._render_dto(generator, entity_with_response_type)
        assert "private T data;" in content

    def test_raw_response_field(self, generator, entity_with_response_type):
        """Req 7.9: rawResponse field for raw_string fallback."""
        content = self._render_dto(generator, entity_with_response_type)
        assert "private String rawResponse;" in content

    def test_error_field(self, generator, entity_with_response_type):
        content = self._render_dto(generator, entity_with_response_type)
        assert "private String error;" in content

    def test_success_factory_method(self, generator, entity_with_response_type):
        content = self._render_dto(generator, entity_with_response_type)
        assert "public static <T> TypedResponseResult<T> success(T data)" in content

    def test_raw_string_fallback_factory(self, generator, entity_with_response_type):
        """Req 7.9: Factory method for raw_string fallback."""
        content = self._render_dto(generator, entity_with_response_type)
        assert "rawStringFallback" in content

    def test_default_object_fallback_factory(self, generator, entity_with_response_type):
        """Req 7.10: Factory method for default_object fallback."""
        content = self._render_dto(generator, entity_with_response_type)
        assert "defaultObjectFallback" in content

    def test_lombok_annotations(self, generator, entity_with_response_type):
        content = self._render_dto(generator, entity_with_response_type)
        assert "@Data" in content
        assert "@Builder" in content
        assert "@NoArgsConstructor" in content
        assert "@AllArgsConstructor" in content


class TestTypedResponseDeserializer:
    """Tests for the generated TypedResponseDeserializer template."""

    def _render_deserializer(self, generator, entities, standalone=None):
        output_dirs = {
            "dto": Path("ai/dto"),
            "service": Path("ai/service"),
            "provider": Path("ai/provider"),
        }
        results = generator.generate(
            entities, standalone or [], BASE_PACKAGE, output_dirs,
        )
        for filepath, content in results:
            if "TypedResponseDeserializer.java" in filepath:
                return content
        return ""

    def test_package_declaration(self, generator, entity_with_response_type):
        content = self._render_deserializer(generator, entity_with_response_type)
        assert "package com.example.app.ai.service;" in content

    def test_class_name(self, generator, entity_with_response_type):
        content = self._render_deserializer(generator, entity_with_response_type)
        assert "public class TypedResponseDeserializer" in content

    def test_component_annotation(self, generator, entity_with_response_type):
        content = self._render_deserializer(generator, entity_with_response_type)
        assert "@Component" in content

    def test_object_mapper_configured(self, generator, entity_with_response_type):
        """Req 7.13: FAIL_ON_UNKNOWN_PROPERTIES = false."""
        content = self._render_deserializer(generator, entity_with_response_type)
        assert "FAIL_ON_UNKNOWN_PROPERTIES" in content
        assert "false" in content

    def test_deserialize_method(self, generator, entity_with_response_type):
        content = self._render_deserializer(generator, entity_with_response_type)
        assert "public <T> Mono<TypedResponseResult<T>> deserialize(" in content

    def test_deserialize_with_retry_method(self, generator, entity_with_response_type):
        """Req 7.11: Retry support method."""
        content = self._render_deserializer(generator, entity_with_response_type)
        assert "public <T> Mono<TypedResponseResult<T>> deserializeWithRetry(" in content

    def test_json_start_validation(self, generator, entity_with_response_type):
        """Req 7.12: Validates response starts with { or [."""
        content = self._render_deserializer(generator, entity_with_response_type)
        assert 'startsWith("{")' in content
        assert 'startsWith("[")' in content

    def test_throw_fallback_handling(self, generator, entity_with_response_type):
        """Req 7.8: throw fallback creates TypedResponseDeserializationException."""
        content = self._render_deserializer(generator, entity_with_response_type)
        assert "TypedResponseDeserializationException" in content
        assert "Mono.error" in content

    def test_raw_string_fallback_handling(self, generator, entity_with_response_type):
        """Req 7.9: raw_string fallback returns TypedResponseResult."""
        content = self._render_deserializer(generator, entity_with_response_type)
        assert '"raw_string"' in content
        assert "rawStringFallback" in content

    def test_default_object_fallback_handling(self, generator, entity_with_response_type):
        """Req 7.10: default_object fallback returns default instance."""
        content = self._render_deserializer(generator, entity_with_response_type)
        assert '"default_object"' in content
        assert "getDeclaredConstructor().newInstance()" in content

    def test_retry_correction_prompt(self, generator, entity_with_response_type):
        """Req 7.11: Retry sends correction prompt to LLM."""
        content = self._render_deserializer(generator, entity_with_response_type)
        assert "correction" in content.lower() or "Retrying deserialization" in content

    def test_reactive_types(self, generator, entity_with_response_type):
        content = self._render_deserializer(generator, entity_with_response_type)
        assert "import reactor.core.publisher.Mono;" in content


class TestTypedResponseDeserializationException:
    """Tests for the generated exception class template."""

    def _render_exception(self, generator, entities, standalone=None):
        output_dirs = {
            "dto": Path("ai/dto"),
            "service": Path("ai/service"),
            "provider": Path("ai/provider"),
        }
        results = generator.generate(
            entities, standalone or [], BASE_PACKAGE, output_dirs,
        )
        for filepath, content in results:
            if "TypedResponseDeserializationException.java" in filepath:
                return content
        return ""

    def test_package_declaration(self, generator, entity_with_response_type):
        content = self._render_exception(generator, entity_with_response_type)
        assert "package com.example.app.ai.provider;" in content

    def test_class_name(self, generator, entity_with_response_type):
        content = self._render_exception(generator, entity_with_response_type)
        assert "public class TypedResponseDeserializationException extends RuntimeException" in content

    def test_target_type_name_field(self, generator, entity_with_response_type):
        content = self._render_exception(generator, entity_with_response_type)
        assert "targetTypeName" in content
        assert "getTargetTypeName()" in content

    def test_raw_response_field(self, generator, entity_with_response_type):
        content = self._render_exception(generator, entity_with_response_type)
        assert "rawResponse" in content
        assert "getRawResponse()" in content

    def test_constructor(self, generator, entity_with_response_type):
        content = self._render_exception(generator, entity_with_response_type)
        assert "TypedResponseDeserializationException(" in content
        assert "super(" in content


class TestAiTypeReferences:
    """Tests for the generated ParameterizedTypeReference constants class."""

    def _render_type_refs(self, generator, entities, standalone=None):
        output_dirs = {
            "dto": Path("ai/dto"),
            "service": Path("ai/service"),
            "provider": Path("ai/provider"),
        }
        results = generator.generate(
            entities, standalone or [], BASE_PACKAGE, output_dirs,
        )
        for filepath, content in results:
            if "AiTypeReferences.java" in filepath:
                return content
        return ""

    def test_package_declaration(self, generator, entity_with_response_type):
        content = self._render_type_refs(generator, entity_with_response_type)
        assert "package com.example.app.ai.service;" in content

    def test_class_name(self, generator, entity_with_response_type):
        content = self._render_type_refs(generator, entity_with_response_type)
        assert "public final class AiTypeReferences" in content

    def test_private_constructor(self, generator, entity_with_response_type):
        content = self._render_type_refs(generator, entity_with_response_type)
        assert "private AiTypeReferences()" in content

    def test_list_wrapper_constant(self, generator, entity_with_response_type):
        """Req 7.3, 7.4: ParameterizedTypeReference for List<CourseOutputDTO>."""
        content = self._render_type_refs(generator, entity_with_response_type)
        assert "COURSE_OUTPUT_D_T_O_LIST_TYPE" in content
        assert "ParameterizedTypeReference<List<CourseOutputDTO>>" in content

    def test_none_wrapper_constant(self, generator, standalone_with_response_type):
        """Req 7.3, 7.6: ParameterizedTypeReference for AnalysisResultDTO."""
        content = self._render_type_refs(generator, [], standalone_with_response_type)
        assert "ANALYSIS_RESULT_D_T_O_TYPE" in content
        assert "ParameterizedTypeReference<AnalysisResultDTO>" in content

    def test_map_wrapper_constant(self, generator, output_dirs):
        """Req 7.3: ParameterizedTypeReference for Map<String, SomeDTO>."""
        entities = [
            {
                "entityName": "Product",
                "providerName": "gpt",
                "enabledOperations": ["search"],
                "searchableFields": ["name"],
                "responseType": {
                    "className": "ProductDTO",
                    "wrapper": "map",
                    "fallbackBehavior": "throw",
                },
            }
        ]
        results = generator.generate(entities, [], BASE_PACKAGE, output_dirs)
        for filepath, content in results:
            if "AiTypeReferences" in filepath:
                assert "PRODUCT_D_T_O_MAP_TYPE" in content
                assert "ParameterizedTypeReference<Map<String, ProductDTO>>" in content

    def test_parameterized_type_reference_import(self, generator, entity_with_response_type):
        content = self._render_type_refs(generator, entity_with_response_type)
        assert "import org.springframework.core.ParameterizedTypeReference;" in content

    def test_multiple_constants(self, generator, output_dirs):
        """Multiple unique responseTypes produce multiple constants."""
        entities = [
            {
                "entityName": "Course",
                "providerName": "gpt",
                "enabledOperations": ["search"],
                "searchableFields": ["title"],
                "responseType": {"className": "CourseDTO", "wrapper": "list", "fallbackBehavior": "throw"},
            },
        ]
        standalone = [
            {
                "name": "analyzer",
                "providerName": "gpt",
                "basePath": "analyze",
                "systemPrompt": "Analyze.",
                "enabledActions": ["query"],
                "responseType": {"className": "AnalysisDTO", "wrapper": "none", "fallbackBehavior": "raw_string"},
            },
        ]
        results = generator.generate(entities, standalone, BASE_PACKAGE, output_dirs)
        for filepath, content in results:
            if "AiTypeReferences" in filepath:
                assert "COURSE_D_T_O_LIST_TYPE" in content
                assert "ANALYSIS_D_T_O_TYPE" in content

    def test_entity_default_classname_constant(
        self, generator, entity_with_default_classname
    ):
        """Req 7.1: className defaults to entity's output DTO when not specified."""
        output_dirs = {
            "dto": Path("ai/dto"),
            "service": Path("ai/service"),
            "provider": Path("ai/provider"),
        }
        results = generator.generate(
            entity_with_default_classname, [], BASE_PACKAGE, output_dirs,
        )
        for filepath, content in results:
            if "AiTypeReferences" in filepath:
                assert "ArticleOutputDTO" in content


class TestBuildJavaType:
    """Tests for the _build_java_type static method."""

    def test_none_wrapper(self):
        assert TypedResponseGenerator._build_java_type("MyDTO", "none") == "MyDTO"

    def test_list_wrapper(self):
        assert TypedResponseGenerator._build_java_type("MyDTO", "list") == "List<MyDTO>"

    def test_map_wrapper(self):
        assert TypedResponseGenerator._build_java_type("MyDTO", "map") == "Map<String, MyDTO>"


class TestBuildConstantName:
    """Tests for the _build_constant_name static method."""

    def test_simple_class_none_wrapper(self):
        assert TypedResponseGenerator._build_constant_name("MyDTO", "none") == "MY_D_T_O_TYPE"

    def test_simple_class_list_wrapper(self):
        assert TypedResponseGenerator._build_constant_name("MyDTO", "list") == "MY_D_T_O_LIST_TYPE"

    def test_simple_class_map_wrapper(self):
        assert TypedResponseGenerator._build_constant_name("MyDTO", "map") == "MY_D_T_O_MAP_TYPE"

    def test_multi_word_class(self):
        assert TypedResponseGenerator._build_constant_name("CourseOutputDTO", "none") == "COURSE_OUTPUT_D_T_O_TYPE"

    def test_single_word(self):
        assert TypedResponseGenerator._build_constant_name("Result", "none") == "RESULT_TYPE"


class TestCollectResponseTypes:
    """Tests for the _collect_response_types method."""

    def test_empty_inputs(self, generator):
        result = generator._collect_response_types([], [])
        assert result == []

    def test_none_inputs(self, generator):
        result = generator._collect_response_types(None, None)
        assert result == []

    def test_entity_with_response_type(self, generator, entity_with_response_type):
        result = generator._collect_response_types(entity_with_response_type, [])
        assert len(result) == 1
        assert result[0]["className"] == "CourseOutputDTO"
        assert result[0]["wrapper"] == "list"
        assert result[0]["fallbackBehavior"] == "raw_string"

    def test_entity_default_classname(self, generator, entity_with_default_classname):
        """Req 7.1: className defaults to <EntityName>OutputDTO."""
        result = generator._collect_response_types(entity_with_default_classname, [])
        assert len(result) == 1
        assert result[0]["className"] == "ArticleOutputDTO"

    def test_standalone_with_response_type(self, generator, standalone_with_response_type):
        result = generator._collect_response_types([], standalone_with_response_type)
        assert len(result) == 1
        assert result[0]["className"] == "AnalysisResultDTO"

    def test_standalone_missing_classname_skipped(self, generator):
        """Req 7.2: className is required for standalone; skip if missing."""
        ops = [
            {
                "name": "broken",
                "responseType": {"wrapper": "none", "fallbackBehavior": "throw"},
            }
        ]
        result = generator._collect_response_types([], ops)
        assert result == []

    def test_deduplication(self, generator):
        """Same className+wrapper from different sources is deduplicated."""
        entities = [
            {
                "entityName": "A",
                "responseType": {"className": "SharedDTO", "wrapper": "list", "fallbackBehavior": "throw"},
            },
            {
                "entityName": "B",
                "responseType": {"className": "SharedDTO", "wrapper": "list", "fallbackBehavior": "raw_string"},
            },
        ]
        result = generator._collect_response_types(entities, [])
        assert len(result) == 1

    def test_different_wrappers_not_deduplicated(self, generator):
        """Same className with different wrappers are separate entries."""
        entities = [
            {
                "entityName": "A",
                "responseType": {"className": "MyDTO", "wrapper": "list", "fallbackBehavior": "throw"},
            },
            {
                "entityName": "B",
                "responseType": {"className": "MyDTO", "wrapper": "none", "fallbackBehavior": "throw"},
            },
        ]
        result = generator._collect_response_types(entities, [])
        assert len(result) == 2

    def test_entities_without_response_type_ignored(self, generator, entity_no_response_type):
        result = generator._collect_response_types(entity_no_response_type, [])
        assert result == []

    def test_default_fallback_behavior(self, generator):
        """Req 7.1: fallbackBehavior defaults to 'throw'."""
        entities = [
            {
                "entityName": "X",
                "responseType": {"className": "XDto", "wrapper": "none"},
            }
        ]
        result = generator._collect_response_types(entities, [])
        assert result[0]["fallbackBehavior"] == "throw"

    def test_default_wrapper(self, generator):
        """Req 7.1: wrapper defaults to 'none'."""
        entities = [
            {
                "entityName": "X",
                "responseType": {"className": "XDto"},
            }
        ]
        result = generator._collect_response_types(entities, [])
        assert result[0]["wrapper"] == "none"


class TestToPascalCase:
    """Tests for the _to_pascal_case static method."""

    def test_already_pascal(self):
        assert TypedResponseGenerator._to_pascal_case("Course") == "Course"

    def test_snake_case(self):
        assert TypedResponseGenerator._to_pascal_case("user_profile") == "UserProfile"

    def test_single_word_lower(self):
        assert TypedResponseGenerator._to_pascal_case("article") == "Article"

    def test_empty_string(self):
        assert TypedResponseGenerator._to_pascal_case("") == ""
