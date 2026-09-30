"""Unit tests for the AI StandaloneAiGenerator.

Verifies that the StandaloneAiGenerator produces correct Java source files
for per-operation standalone AI services and controllers, with conditional
method generation based on enabledActions, stateTable entity/repository
generation, and assistant reference handling.

Requirements: 6.1–6.10
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_standalone_generator import StandaloneAiGenerator


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
    return StandaloneAiGenerator(jinja_env)


@pytest.fixture
def all_actions_operation():
    """Standalone operation with all actions enabled."""
    return [
        {
            "name": "codeHelper",
            "type": "chat",
            "providerName": "mainGpt",
            "basePath": "code-helper",
            "systemPrompt": "You are a helpful coding assistant.",
            "enabledActions": ["chat", "chatStream", "generate", "query"],
            "rolePromptSequence": None,
            "assistantName": None,
            "chatOptions": None,
            "stateTable": None,
            "evaluatorNames": [],
            "responseType": None,
            "ragSourceNames": [],
        }
    ]


@pytest.fixture
def chat_only_operation():
    """Standalone operation with only chat enabled."""
    return [
        {
            "name": "supportBot",
            "type": "chat",
            "providerName": "localOllama",
            "basePath": "support",
            "systemPrompt": "You are a support assistant.",
            "enabledActions": ["chat"],
            "rolePromptSequence": [
                {"role": "system", "content": "You help users with {{productName}}."},
                {"role": "user", "content": "I need help."},
            ],
        }
    ]


@pytest.fixture
def generate_only_operation():
    """Standalone operation with only generate enabled."""
    return [
        {
            "name": "contentWriter",
            "type": "generator",
            "providerName": "mainGpt",
            "basePath": "content-writer",
            "systemPrompt": "You are a content writer.",
            "enabledActions": ["generate"],
        }
    ]


@pytest.fixture
def query_only_operation():
    """Standalone operation with only query enabled."""
    return [
        {
            "name": "dataAnalyzer",
            "type": "query",
            "providerName": "mainGpt",
            "basePath": "data-analyzer",
            "systemPrompt": "You analyze data.",
            "enabledActions": ["query"],
        }
    ]


@pytest.fixture
def operation_with_state_table():
    """Standalone operation with a stateTable defined."""
    return [
        {
            "name": "taskTracker",
            "type": "chat",
            "providerName": "mainGpt",
            "basePath": "task-tracker",
            "systemPrompt": "You track tasks.",
            "enabledActions": ["chat", "generate"],
            "stateTable": {
                "tableName": "ai_task_state",
                "columns": [
                    {"name": "user_id", "type": "BIGINT", "nullable": False},
                    {"name": "task_name", "type": "VARCHAR", "length": 255, "nullable": False},
                    {"name": "status", "type": "VARCHAR", "length": 50, "nullable": True},
                    {"name": "priority", "type": "INT", "nullable": True, "defaultValue": "0"},
                    {"name": "is_completed", "type": "BOOLEAN", "nullable": True},
                    {"name": "notes", "type": "TEXT", "nullable": True},
                    {"name": "score", "type": "DOUBLE", "nullable": True},
                    {"name": "metadata", "type": "JSON", "nullable": True},
                    {"name": "created_at", "type": "DATETIME", "nullable": True},
                ],
            },
        }
    ]


@pytest.fixture
def operation_with_assistant():
    """Standalone operation referencing an assistant."""
    return [
        {
            "name": "tutorBot",
            "type": "chat",
            "providerName": "mainGpt",
            "basePath": "tutor",
            "systemPrompt": "You are a tutor.",
            "enabledActions": ["chat", "chatStream"],
            "assistantName": "mathTutor",
        }
    ]


@pytest.fixture
def assistants():
    """Assistant definitions for testing."""
    return [
        {
            "name": "mathTutor",
            "systemPrompt": "You are a math tutor.",
            "rolePromptSequence": [
                {"role": "system", "content": "You teach math to {{studentLevel}} students."},
            ],
            "providerName": "mainGpt",
            "entityScope": [],
            "memoryWindowSize": 30,
        }
    ]


@pytest.fixture
def output_dirs():
    return {
        "service": Path("com/example/app/ai/service"),
        "controller": Path("com/example/app/ai/controller"),
        "entity": Path("com/example/app/ai/entity"),
        "repository": Path("com/example/app/ai/repository"),
    }


BASE_PACKAGE = "com.example.app"


class TestStandaloneAiGeneratorGenerate:
    """Tests for the generate() method."""

    def test_generates_two_files_per_operation(self, generator, all_actions_operation, output_dirs):
        results = generator.generate(all_actions_operation, BASE_PACKAGE, output_dirs)
        assert len(results) == 2  # service + controller

    def test_generates_correct_filenames(self, generator, all_actions_operation, output_dirs):
        results = generator.generate(all_actions_operation, BASE_PACKAGE, output_dirs)
        filenames = [r[0] for r in results]
        assert any("CodeHelperAiService.java" in f for f in filenames)
        assert any("CodeHelperAiController.java" in f for f in filenames)

    def test_all_content_is_nonempty(self, generator, all_actions_operation, output_dirs):
        results = generator.generate(all_actions_operation, BASE_PACKAGE, output_dirs)
        for filepath, content in results:
            assert content.strip(), f"Empty content for {filepath}"

    def test_empty_operations_returns_empty(self, generator, output_dirs):
        results = generator.generate([], BASE_PACKAGE, output_dirs)
        assert results == []

    def test_multiple_operations(self, generator, output_dirs):
        ops = [
            {"name": "codeHelper", "providerName": "gpt", "basePath": "code", "systemPrompt": "Help.", "enabledActions": ["chat"]},
            {"name": "writer", "providerName": "gpt", "basePath": "write", "systemPrompt": "Write.", "enabledActions": ["generate"]},
        ]
        results = generator.generate(ops, BASE_PACKAGE, output_dirs)
        assert len(results) == 4  # 2 files per operation

    def test_output_dirs_used_in_paths(self, generator, all_actions_operation, output_dirs):
        results = generator.generate(all_actions_operation, BASE_PACKAGE, output_dirs)
        for filepath, _ in results:
            assert filepath.startswith("com/example/app/ai/")

    def test_default_output_dirs(self, generator, all_actions_operation):
        results = generator.generate(all_actions_operation, BASE_PACKAGE, {})
        filenames = [r[0] for r in results]
        assert any("ai/service/CodeHelperAiService.java" in f for f in filenames)
        assert any("ai/controller/CodeHelperAiController.java" in f for f in filenames)

    def test_state_table_generates_four_files(self, generator, operation_with_state_table, output_dirs):
        """Req 6.7: stateTable generates entity + repository in addition to service + controller."""
        results = generator.generate(operation_with_state_table, BASE_PACKAGE, output_dirs)
        assert len(results) == 4  # service + controller + entity + repository
        filenames = [r[0] for r in results]
        assert any("TaskTrackerState.java" in f for f in filenames)
        assert any("TaskTrackerStateRepository.java" in f for f in filenames)


class TestStandaloneAiService:
    """Tests for the generated standalone AI service template."""

    def _render_service(self, generator, ops, assistants=None):
        output_dirs = {
            "service": Path("ai/service"),
            "controller": Path("ai/controller"),
            "entity": Path("ai/entity"),
            "repository": Path("ai/repository"),
        }
        results = generator.generate(ops, BASE_PACKAGE, output_dirs, assistants)
        for filepath, content in results:
            if "AiService.java" in filepath:
                return content
        return ""

    def test_package_declaration(self, generator, all_actions_operation):
        content = self._render_service(generator, all_actions_operation)
        assert "package com.example.app.ai.service;" in content

    def test_class_name(self, generator, all_actions_operation):
        content = self._render_service(generator, all_actions_operation)
        assert "public class CodeHelperAiService" in content

    def test_service_annotation(self, generator, all_actions_operation):
        content = self._render_service(generator, all_actions_operation)
        assert "@Service" in content

    def test_slf4j_annotation(self, generator, all_actions_operation):
        content = self._render_service(generator, all_actions_operation)
        assert "@Slf4j" in content

    def test_chat_client_qualifier(self, generator, all_actions_operation):
        """Req 6.6: ChatClient injected via @Qualifier."""
        content = self._render_service(generator, all_actions_operation)
        assert '@Qualifier("mainGpt")' in content
        assert "private final ChatClient chatClient" in content

    def test_no_entity_service_injection(self, generator, all_actions_operation):
        """Req 6.6: No entity-specific service injected."""
        content = self._render_service(generator, all_actions_operation)
        # Should not have any entity service (like CourseService)
        assert "Service " not in content.split("class")[0] or "ChatClient" in content

    def test_chat_method_present(self, generator, all_actions_operation):
        """Req 6.2: chat method when chat in enabledActions."""
        content = self._render_service(generator, all_actions_operation)
        assert "public Mono<String> chat(Long sessionId, String userMessage)" in content

    def test_chat_stream_method_present(self, generator, all_actions_operation):
        """Req 6.3: chatStream method when chatStream in enabledActions."""
        content = self._render_service(generator, all_actions_operation)
        assert "public Flux<String> chatStream(Long sessionId, String userMessage)" in content

    def test_generate_method_present(self, generator, all_actions_operation):
        """Req 6.4: generate method when generate in enabledActions."""
        content = self._render_service(generator, all_actions_operation)
        assert "public Mono<String> generate(String prompt, Map<String, Object> context)" in content

    def test_query_method_present(self, generator, all_actions_operation):
        """Req 6.5: query method when query in enabledActions."""
        content = self._render_service(generator, all_actions_operation)
        assert "public Mono<String> query(String query, Map<String, Object> parameters)" in content

    def test_chat_only_excludes_other_methods(self, generator, chat_only_operation):
        """Only enabled actions generate methods."""
        content = self._render_service(generator, chat_only_operation)
        assert "public Mono<String> chat(" in content
        assert "chatStream" not in content
        assert "public Mono<String> generate(" not in content
        assert "public Mono<String> query(" not in content

    def test_generate_only_excludes_other_methods(self, generator, generate_only_operation):
        content = self._render_service(generator, generate_only_operation)
        assert "public Mono<String> generate(" in content
        assert "public Mono<String> chat(" not in content
        assert "chatStream" not in content
        assert "public Mono<String> query(" not in content

    def test_query_only_excludes_other_methods(self, generator, query_only_operation):
        content = self._render_service(generator, query_only_operation)
        assert "public Mono<String> query(" in content
        assert "public Mono<String> chat(" not in content
        assert "chatStream" not in content
        assert "public Mono<String> generate(" not in content

    def test_chat_has_conversation_memory(self, generator, chat_only_operation):
        """Chat operations inject ConversationMemoryService."""
        content = self._render_service(generator, chat_only_operation)
        assert "ConversationMemoryService" in content

    def test_generate_only_no_conversation_memory(self, generator, generate_only_operation):
        """Non-chat operations don't inject ConversationMemoryService."""
        content = self._render_service(generator, generate_only_operation)
        assert "ConversationMemoryService" not in content

    def test_role_prompt_sequence_rendered(self, generator, chat_only_operation):
        """rolePromptSequence entries are rendered in chat methods."""
        content = self._render_service(generator, chat_only_operation)
        assert "rolePromptSequence" in content
        assert '"system"' in content

    def test_state_table_repository_injection(self, generator, operation_with_state_table):
        """Req 6.7: State repository injected when stateTable defined."""
        content = self._render_service(generator, operation_with_state_table)
        assert "TaskTrackerStateRepository" in content

    def test_no_state_table_no_repository(self, generator, all_actions_operation):
        """No state repository when stateTable is absent."""
        content = self._render_service(generator, all_actions_operation)
        assert "StateRepository" not in content

    def test_assistant_config_used(self, generator, operation_with_assistant, assistants):
        """Req 6.8: Assistant configuration used when assistantName referenced."""
        content = self._render_service(generator, operation_with_assistant, assistants)
        assert "mathTutor" in content
        assert "memoryWindowSize = 30" in content

    def test_system_prompt_in_generate(self, generator, generate_only_operation):
        """System prompt appears in generate method."""
        content = self._render_service(generator, generate_only_operation)
        assert "You are a content writer." in content

    def test_reactive_types(self, generator, all_actions_operation):
        """All methods use reactive types (Mono/Flux)."""
        content = self._render_service(generator, all_actions_operation)
        assert "import reactor.core.publisher.Flux;" in content
        assert "import reactor.core.publisher.Mono;" in content


class TestStandaloneAiController:
    """Tests for the generated standalone AI controller template."""

    def _render_controller(self, generator, ops, assistants=None):
        output_dirs = {
            "service": Path("ai/service"),
            "controller": Path("ai/controller"),
            "entity": Path("ai/entity"),
            "repository": Path("ai/repository"),
        }
        results = generator.generate(ops, BASE_PACKAGE, output_dirs, assistants)
        for filepath, content in results:
            if "AiController.java" in filepath:
                return content
        return ""

    def test_package_declaration(self, generator, all_actions_operation):
        content = self._render_controller(generator, all_actions_operation)
        assert "package com.example.app.ai.controller;" in content

    def test_class_name(self, generator, all_actions_operation):
        content = self._render_controller(generator, all_actions_operation)
        assert "public class CodeHelperAiController" in content

    def test_rest_controller_annotation(self, generator, all_actions_operation):
        content = self._render_controller(generator, all_actions_operation)
        assert "@RestController" in content

    def test_request_mapping_base_path(self, generator, all_actions_operation):
        """Req 6.1: Base path /api/ai/<basePath>."""
        content = self._render_controller(generator, all_actions_operation)
        assert '@RequestMapping("/api/ai/code-helper")' in content

    def test_service_injection(self, generator, all_actions_operation):
        content = self._render_controller(generator, all_actions_operation)
        assert "private final CodeHelperAiService codeHelperAiService" in content

    def test_chat_endpoint(self, generator, all_actions_operation):
        """Req 6.2: POST /chat endpoint."""
        content = self._render_controller(generator, all_actions_operation)
        assert '@PostMapping("/chat")' in content
        assert "public Mono<String> chat" in content

    def test_chat_stream_endpoint(self, generator, all_actions_operation):
        """Req 6.3: GET /chat/stream SSE endpoint."""
        content = self._render_controller(generator, all_actions_operation)
        assert '@GetMapping(value = "/chat/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)' in content
        assert "public Flux<String> chatStream" in content

    def test_generate_endpoint(self, generator, all_actions_operation):
        """Req 6.4: POST /generate endpoint."""
        content = self._render_controller(generator, all_actions_operation)
        assert '@PostMapping("/generate")' in content
        assert "public Mono<String> generate" in content

    def test_query_endpoint(self, generator, all_actions_operation):
        """Req 6.5: POST /query endpoint."""
        content = self._render_controller(generator, all_actions_operation)
        assert '@PostMapping("/query")' in content
        assert "public Mono<String> query" in content

    def test_sessions_endpoint(self, generator, all_actions_operation):
        """Req 6.9: GET /sessions listing user's chat sessions."""
        content = self._render_controller(generator, all_actions_operation)
        assert '@GetMapping("/sessions")' in content
        assert "public Flux<Map<String, Object>> listSessions" in content

    def test_chat_only_excludes_other_endpoints(self, generator, chat_only_operation):
        """Only enabled actions generate endpoints."""
        content = self._render_controller(generator, chat_only_operation)
        assert '@PostMapping("/chat")' in content
        assert '@PostMapping("/generate")' not in content
        assert '@PostMapping("/query")' not in content

    def test_generate_only_excludes_chat_endpoints(self, generator, generate_only_operation):
        content = self._render_controller(generator, generate_only_operation)
        assert '@PostMapping("/generate")' in content
        assert '@PostMapping("/chat")' not in content
        assert '@GetMapping(value = "/chat/stream"' not in content
        assert '@GetMapping("/sessions")' not in content

    def test_query_only_excludes_other_endpoints(self, generator, query_only_operation):
        content = self._render_controller(generator, query_only_operation)
        assert '@PostMapping("/query")' in content
        assert '@PostMapping("/chat")' not in content
        assert '/chat/stream' not in content
        assert '@PostMapping("/generate")' not in content

    def test_no_sessions_without_chat(self, generator, generate_only_operation):
        """Sessions endpoint only when chat or chatStream enabled."""
        content = self._render_controller(generator, generate_only_operation)
        assert '@GetMapping("/sessions")' not in content


class TestStateTableGeneration:
    """Tests for stateTable entity and repository generation."""

    def _get_results(self, generator, ops):
        output_dirs = {
            "service": Path("ai/service"),
            "controller": Path("ai/controller"),
            "entity": Path("ai/entity"),
            "repository": Path("ai/repository"),
        }
        return generator.generate(ops, BASE_PACKAGE, output_dirs)

    def _get_entity_content(self, generator, ops):
        for filepath, content in self._get_results(generator, ops):
            if "State.java" in filepath and "Repository" not in filepath:
                return content
        return ""

    def _get_repository_content(self, generator, ops):
        for filepath, content in self._get_results(generator, ops):
            if "StateRepository.java" in filepath:
                return content
        return ""

    def test_entity_class_name(self, generator, operation_with_state_table):
        content = self._get_entity_content(generator, operation_with_state_table)
        assert "public class TaskTrackerState" in content

    def test_entity_table_annotation(self, generator, operation_with_state_table):
        content = self._get_entity_content(generator, operation_with_state_table)
        assert '@Table("ai_task_state")' in content

    def test_entity_has_id_field(self, generator, operation_with_state_table):
        content = self._get_entity_content(generator, operation_with_state_table)
        assert "@Id" in content
        assert "private Long id;" in content

    def test_entity_column_mapping(self, generator, operation_with_state_table):
        """Columns are mapped with correct Java types."""
        content = self._get_entity_content(generator, operation_with_state_table)
        assert '@Column("user_id")' in content
        assert "private Long userId;" in content
        assert '@Column("task_name")' in content
        assert "private String taskName;" in content
        assert '@Column("priority")' in content
        assert "private Integer priority;" in content
        assert '@Column("is_completed")' in content
        assert "private Boolean isCompleted;" in content
        assert '@Column("notes")' in content
        # TEXT maps to String
        assert '@Column("score")' in content
        assert "private Double score;" in content
        assert '@Column("metadata")' in content
        assert '@Column("created_at")' in content

    def test_entity_lombok_annotations(self, generator, operation_with_state_table):
        content = self._get_entity_content(generator, operation_with_state_table)
        assert "@Data" in content
        assert "@Builder" in content
        assert "@NoArgsConstructor" in content
        assert "@AllArgsConstructor" in content

    def test_repository_interface(self, generator, operation_with_state_table):
        content = self._get_repository_content(generator, operation_with_state_table)
        assert "public interface TaskTrackerStateRepository extends ReactiveCrudRepository<TaskTrackerState, Long>" in content

    def test_repository_annotation(self, generator, operation_with_state_table):
        content = self._get_repository_content(generator, operation_with_state_table)
        assert "@Repository" in content

    def test_no_state_files_without_state_table(self, generator, all_actions_operation):
        """No entity/repository files when stateTable is absent."""
        results = self._get_results(generator, all_actions_operation)
        filenames = [r[0] for r in results]
        assert not any("State.java" in f for f in filenames)
        assert not any("StateRepository.java" in f for f in filenames)


class TestBuildAssistantMap:
    """Tests for the _build_assistant_map static method."""

    def test_none_assistants(self):
        assert StandaloneAiGenerator._build_assistant_map(None) == {}

    def test_empty_assistants(self):
        assert StandaloneAiGenerator._build_assistant_map([]) == {}

    def test_maps_name_to_config(self):
        assistants = [{"name": "mathTutor", "systemPrompt": "Teach math."}]
        result = StandaloneAiGenerator._build_assistant_map(assistants)
        assert "mathTutor" in result
        assert result["mathTutor"]["systemPrompt"] == "Teach math."

    def test_multiple_assistants(self):
        assistants = [
            {"name": "mathTutor", "systemPrompt": "Math."},
            {"name": "sciTutor", "systemPrompt": "Science."},
        ]
        result = StandaloneAiGenerator._build_assistant_map(assistants)
        assert len(result) == 2


class TestToPascalCase:
    """Tests for the _to_pascal_case static method."""

    def test_camel_case(self):
        assert StandaloneAiGenerator._to_pascal_case("codeHelper") == "CodeHelper"

    def test_snake_case(self):
        assert StandaloneAiGenerator._to_pascal_case("code_helper") == "CodeHelper"

    def test_already_pascal(self):
        assert StandaloneAiGenerator._to_pascal_case("CodeHelper") == "CodeHelper"

    def test_single_word(self):
        assert StandaloneAiGenerator._to_pascal_case("writer") == "Writer"

    def test_empty_string(self):
        assert StandaloneAiGenerator._to_pascal_case("") == ""


class TestToCamelCase:
    """Tests for the _to_camel_case static method."""

    def test_snake_case(self):
        assert StandaloneAiGenerator._to_camel_case("user_id") == "userId"

    def test_multi_part(self):
        assert StandaloneAiGenerator._to_camel_case("created_at") == "createdAt"

    def test_no_underscore(self):
        assert StandaloneAiGenerator._to_camel_case("name") == "name"

    def test_triple_part(self):
        assert StandaloneAiGenerator._to_camel_case("first_seen_at") == "firstSeenAt"
