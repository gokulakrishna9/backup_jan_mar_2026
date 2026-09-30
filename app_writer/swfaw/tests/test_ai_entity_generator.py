"""Unit tests for the AI EntityAiGenerator.

Verifies that the EntityAiGenerator produces correct Java source files
for per-entity AI services and controllers, with conditional method
generation based on enabledOperations.

Requirements: 5.1–5.9
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_entity_generator import EntityAiGenerator


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
    return EntityAiGenerator(jinja_env)


@pytest.fixture
def all_ops_capability():
    """Entity capability with all operations enabled."""
    return [
        {
            "entityName": "Course",
            "providerName": "mainGpt",
            "enabledOperations": ["search", "generate", "summarize", "classify", "chat", "chatStream"],
            "searchableFields": ["title", "description", "category"],
            "evaluatorNames": [],
            "chatOptions": None,
            "rolePromptSequence": None,
            "responseType": None,
            "ragSourceNames": [],
        }
    ]


@pytest.fixture
def search_only_capability():
    """Entity capability with only search enabled."""
    return [
        {
            "entityName": "Article",
            "providerName": "localOllama",
            "enabledOperations": ["search"],
            "searchableFields": ["title", "body"],
        }
    ]


@pytest.fixture
def chat_only_capability():
    """Entity capability with only chat/chatStream enabled."""
    return [
        {
            "entityName": "UserProfile",
            "providerName": "mainGpt",
            "enabledOperations": ["chat", "chatStream"],
            "searchableFields": [],
            "rolePromptSequence": [
                {"role": "system", "content": "You are a profile assistant for {{userName}}."},
                {"role": "user", "content": "Help me with my profile."},
            ],
        }
    ]


@pytest.fixture
def output_dirs():
    return {
        "service": Path("com/example/app/ai/service"),
        "controller": Path("com/example/app/ai/controller"),
    }


@pytest.fixture
def controller_layer():
    return {
        "controllers": [
            {"entityName": "Course", "basePath": "/api/courses"},
            {"entityName": "Article", "basePath": "/api/articles"},
            {"entityName": "UserProfile", "basePath": "/api/user-profiles"},
        ]
    }


BASE_PACKAGE = "com.example.app"


class TestEntityAiGeneratorGenerate:
    """Tests for the generate() method."""

    def test_generates_two_files_per_entity(self, generator, all_ops_capability, output_dirs, controller_layer):
        results = generator.generate(all_ops_capability, BASE_PACKAGE, output_dirs, controller_layer)
        assert len(results) == 2  # service + controller

    def test_generates_correct_filenames(self, generator, all_ops_capability, output_dirs, controller_layer):
        results = generator.generate(all_ops_capability, BASE_PACKAGE, output_dirs, controller_layer)
        filenames = [r[0] for r in results]
        assert any("CourseAiService.java" in f for f in filenames)
        assert any("CourseAiController.java" in f for f in filenames)

    def test_all_content_is_nonempty(self, generator, all_ops_capability, output_dirs, controller_layer):
        results = generator.generate(all_ops_capability, BASE_PACKAGE, output_dirs, controller_layer)
        for filepath, content in results:
            assert content.strip(), f"Empty content for {filepath}"

    def test_empty_capabilities_returns_empty(self, generator, output_dirs):
        results = generator.generate([], BASE_PACKAGE, output_dirs)
        assert results == []

    def test_multiple_entities(self, generator, output_dirs, controller_layer):
        caps = [
            {"entityName": "Course", "providerName": "gpt", "enabledOperations": ["search"], "searchableFields": ["title"]},
            {"entityName": "Article", "providerName": "gpt", "enabledOperations": ["summarize"], "searchableFields": []},
        ]
        results = generator.generate(caps, BASE_PACKAGE, output_dirs, controller_layer)
        assert len(results) == 4  # 2 files per entity

    def test_output_dirs_used_in_paths(self, generator, all_ops_capability, output_dirs, controller_layer):
        results = generator.generate(all_ops_capability, BASE_PACKAGE, output_dirs, controller_layer)
        for filepath, _ in results:
            assert filepath.startswith("com/example/app/ai/")

    def test_default_output_dirs(self, generator, all_ops_capability, controller_layer):
        results = generator.generate(all_ops_capability, BASE_PACKAGE, {}, controller_layer)
        filenames = [r[0] for r in results]
        assert any("ai/service/CourseAiService.java" in f for f in filenames)
        assert any("ai/controller/CourseAiController.java" in f for f in filenames)


class TestEntityAiService:
    """Tests for the generated entity AI service template."""

    def _render_service(self, generator, caps, controller_layer=None):
        output_dirs = {"service": Path("ai/service"), "controller": Path("ai/controller")}
        results = generator.generate(caps, BASE_PACKAGE, output_dirs, controller_layer)
        # Return the service content (first result)
        for filepath, content in results:
            if "AiService.java" in filepath:
                return content
        return ""

    def test_package_declaration(self, generator, all_ops_capability):
        content = self._render_service(generator, all_ops_capability)
        assert "package com.example.app.ai.service;" in content

    def test_class_name(self, generator, all_ops_capability):
        content = self._render_service(generator, all_ops_capability)
        assert "public class CourseAiService" in content

    def test_service_annotation(self, generator, all_ops_capability):
        content = self._render_service(generator, all_ops_capability)
        assert "@Service" in content

    def test_slf4j_annotation(self, generator, all_ops_capability):
        content = self._render_service(generator, all_ops_capability)
        assert "@Slf4j" in content

    def test_chat_client_qualifier(self, generator, all_ops_capability):
        """Req 5.7: ChatClient injected via @Qualifier."""
        content = self._render_service(generator, all_ops_capability)
        assert '@Qualifier("mainGpt")' in content
        assert "private final ChatClient chatClient" in content

    def test_entity_service_injection(self, generator, all_ops_capability):
        """Req 5.7: Entity service injected."""
        content = self._render_service(generator, all_ops_capability)
        assert "private final CourseService courseService" in content

    def test_search_method_present(self, generator, all_ops_capability):
        """Req 5.2: aiSearch method when search enabled."""
        content = self._render_service(generator, all_ops_capability)
        assert "public Flux<String> aiSearch(String naturalLanguageQuery)" in content

    def test_generate_method_present(self, generator, all_ops_capability):
        """Req 5.3: generateContent method when generate enabled."""
        content = self._render_service(generator, all_ops_capability)
        assert "public Mono<String> generateContent(String fieldName, Map<String, Object> context)" in content

    def test_summarize_method_present(self, generator, all_ops_capability):
        """Req 5.4: summarize method when summarize enabled."""
        content = self._render_service(generator, all_ops_capability)
        assert "public Mono<String> summarize(Long entityId)" in content

    def test_classify_method_present(self, generator, all_ops_capability):
        """Req 5.5: classify method when classify enabled."""
        content = self._render_service(generator, all_ops_capability)
        assert "public Mono<String> classify(Long entityId, List<String> categories)" in content

    def test_chat_method_present(self, generator, all_ops_capability):
        """Req 5.6: chat method when chat enabled."""
        content = self._render_service(generator, all_ops_capability)
        assert "public Mono<String> chat(Long sessionId, String userMessage)" in content

    def test_chat_stream_method_present(self, generator, all_ops_capability):
        """Req 5.6: chatStream method when chatStream enabled."""
        content = self._render_service(generator, all_ops_capability)
        assert "public Flux<String> chatStream(Long sessionId, String userMessage)" in content

    def test_search_only_excludes_other_methods(self, generator, search_only_capability):
        """Req 5.8: Only enabled operations generate methods."""
        content = self._render_service(generator, search_only_capability)
        assert "aiSearch" in content
        assert "generateContent" not in content
        assert "summarize" not in content
        assert "classify" not in content
        assert "public Mono<String> chat(" not in content
        assert "chatStream" not in content

    def test_chat_only_has_conversation_memory(self, generator, chat_only_capability):
        """Chat operations inject ConversationMemoryService."""
        content = self._render_service(generator, chat_only_capability)
        assert "ConversationMemoryService" in content

    def test_search_only_no_conversation_memory(self, generator, search_only_capability):
        """Non-chat operations don't inject ConversationMemoryService."""
        content = self._render_service(generator, search_only_capability)
        assert "ConversationMemoryService" not in content

    def test_searchable_fields_in_prompt(self, generator, all_ops_capability):
        """Searchable fields appear in the search system prompt."""
        content = self._render_service(generator, all_ops_capability)
        assert "title, description, category" in content

    def test_role_prompt_sequence_rendered(self, generator, chat_only_capability):
        """rolePromptSequence entries are rendered in chat methods."""
        content = self._render_service(generator, chat_only_capability)
        assert "rolePromptSequence" in content
        assert '"system"' in content

    def test_reactive_types(self, generator, all_ops_capability):
        """All methods use reactive types (Mono/Flux)."""
        content = self._render_service(generator, all_ops_capability)
        assert "import reactor.core.publisher.Flux;" in content
        assert "import reactor.core.publisher.Mono;" in content


class TestEntityAiController:
    """Tests for the generated entity AI controller template."""

    def _render_controller(self, generator, caps, controller_layer=None):
        output_dirs = {"service": Path("ai/service"), "controller": Path("ai/controller")}
        results = generator.generate(caps, BASE_PACKAGE, output_dirs, controller_layer)
        for filepath, content in results:
            if "AiController.java" in filepath:
                return content
        return ""

    def test_package_declaration(self, generator, all_ops_capability, controller_layer):
        content = self._render_controller(generator, all_ops_capability, controller_layer)
        assert "package com.example.app.ai.controller;" in content

    def test_class_name(self, generator, all_ops_capability, controller_layer):
        content = self._render_controller(generator, all_ops_capability, controller_layer)
        assert "public class CourseAiController" in content

    def test_rest_controller_annotation(self, generator, all_ops_capability, controller_layer):
        content = self._render_controller(generator, all_ops_capability, controller_layer)
        assert "@RestController" in content

    def test_request_mapping_base_path(self, generator, all_ops_capability, controller_layer):
        """Req 5.1: Base path /api/<entityBasePath>/ai."""
        content = self._render_controller(generator, all_ops_capability, controller_layer)
        assert '@RequestMapping("/api/courses/ai")' in content

    def test_service_injection(self, generator, all_ops_capability, controller_layer):
        content = self._render_controller(generator, all_ops_capability, controller_layer)
        assert "private final CourseAiService courseAiService" in content

    def test_search_endpoint(self, generator, all_ops_capability, controller_layer):
        """Req 5.2: POST /search endpoint."""
        content = self._render_controller(generator, all_ops_capability, controller_layer)
        assert '@PostMapping("/search")' in content
        assert "public Flux<String> aiSearch" in content

    def test_generate_endpoint(self, generator, all_ops_capability, controller_layer):
        """Req 5.3: POST /generate endpoint."""
        content = self._render_controller(generator, all_ops_capability, controller_layer)
        assert '@PostMapping("/generate")' in content
        assert "public Mono<String> generateContent" in content

    def test_summarize_endpoint(self, generator, all_ops_capability, controller_layer):
        """Req 5.4: GET /{id}/summarize endpoint."""
        content = self._render_controller(generator, all_ops_capability, controller_layer)
        assert '@GetMapping("/{id}/summarize")' in content
        assert "public Mono<String> summarize" in content

    def test_classify_endpoint(self, generator, all_ops_capability, controller_layer):
        """Req 5.5: POST /{id}/classify endpoint."""
        content = self._render_controller(generator, all_ops_capability, controller_layer)
        assert '@PostMapping("/{id}/classify")' in content
        assert "public Mono<String> classify" in content

    def test_chat_endpoint(self, generator, all_ops_capability, controller_layer):
        """Req 5.6: POST /chat endpoint."""
        content = self._render_controller(generator, all_ops_capability, controller_layer)
        assert '@PostMapping("/chat")' in content
        assert "public Mono<String> chat" in content

    def test_chat_stream_endpoint(self, generator, all_ops_capability, controller_layer):
        """Req 5.6: GET /chat/stream SSE endpoint."""
        content = self._render_controller(generator, all_ops_capability, controller_layer)
        assert '@GetMapping(value = "/chat/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)' in content
        assert "public Flux<String> chatStream" in content

    def test_search_only_excludes_other_endpoints(self, generator, search_only_capability, controller_layer):
        """Req 5.8: Only enabled operations generate endpoints."""
        content = self._render_controller(generator, search_only_capability, controller_layer)
        assert '@PostMapping("/search")' in content
        assert '@PostMapping("/generate")' not in content
        assert '@GetMapping("/{id}/summarize")' not in content
        assert '@PostMapping("/{id}/classify")' not in content
        assert '@PostMapping("/chat")' not in content
        assert '/chat/stream' not in content

    def test_base_path_from_controller_layer(self, generator, controller_layer):
        """Base path resolved from controller_layer definition."""
        caps = [{"entityName": "Article", "providerName": "gpt", "enabledOperations": ["search"], "searchableFields": ["title"]}]
        content = self._render_controller(generator, caps, controller_layer)
        assert '@RequestMapping("/api/articles/ai")' in content

    def test_fallback_base_path_without_controller_layer(self, generator):
        """Fallback base path when controller_layer is not provided."""
        caps = [{"entityName": "Course", "providerName": "gpt", "enabledOperations": ["search"], "searchableFields": ["title"]}]
        content = self._render_controller(generator, caps, None)
        assert '@RequestMapping("/api/courses/ai")' in content


class TestBuildBasePathMap:
    """Tests for the _build_base_path_map static method."""

    def test_none_controller_layer(self):
        assert EntityAiGenerator._build_base_path_map(None) == {}

    def test_empty_controllers(self):
        assert EntityAiGenerator._build_base_path_map({"controllers": []}) == {}

    def test_maps_entity_to_base_path(self):
        layer = {"controllers": [{"entityName": "Course", "basePath": "/api/courses"}]}
        result = EntityAiGenerator._build_base_path_map(layer)
        assert result == {"Course": "/api/courses"}

    def test_multiple_controllers(self):
        layer = {"controllers": [
            {"entityName": "Course", "basePath": "/api/courses"},
            {"entityName": "Article", "basePath": "/api/articles"},
        ]}
        result = EntityAiGenerator._build_base_path_map(layer)
        assert len(result) == 2
        assert result["Course"] == "/api/courses"
        assert result["Article"] == "/api/articles"


class TestToPascalCase:
    """Tests for the _to_pascal_case static method."""

    def test_already_pascal(self):
        assert EntityAiGenerator._to_pascal_case("Course") == "Course"

    def test_snake_case(self):
        assert EntityAiGenerator._to_pascal_case("user_profile") == "UserProfile"

    def test_single_word_lower(self):
        assert EntityAiGenerator._to_pascal_case("article") == "Article"

    def test_empty_string(self):
        assert EntityAiGenerator._to_pascal_case("") == ""
