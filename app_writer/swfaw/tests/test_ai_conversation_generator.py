"""Unit tests for the AI ConversationGenerator.

Verifies that the ConversationGenerator produces correct Java source files
for AiChatSession, AiChatMessage entities, their repositories, and the
ConversationMemoryService.
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_conversation_generator import ConversationGenerator


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
    return ConversationGenerator(jinja_env)


@pytest.fixture
def sample_assistants():
    return [
        {
            "name": "helpDesk",
            "systemPrompt": "You are a helpful assistant.",
            "providerName": "mainGpt",
            "entityScope": "all",
            "memoryWindowSize": 30,
        },
        {
            "name": "codeHelper",
            "systemPrompt": "You are a code assistant.",
            "providerName": "localOllama",
            "entityScope": "all",
            "memoryWindowSize": 10,
        },
    ]


@pytest.fixture
def empty_assistants():
    return []


@pytest.fixture
def output_dirs():
    return {
        "entity": Path("com/example/app/ai/entity"),
        "repository": Path("com/example/app/ai/repository"),
        "service": Path("com/example/app/ai/service"),
    }


BASE_PACKAGE = "com.example.app"


class TestConversationGeneratorGenerate:
    """Tests for the generate() method output structure."""

    def test_generates_five_files(self, generator, sample_assistants, output_dirs):
        result = generator.generate(sample_assistants, BASE_PACKAGE, output_dirs)
        assert len(result) == 5

    def test_generates_correct_filenames(self, generator, sample_assistants, output_dirs):
        result = generator.generate(sample_assistants, BASE_PACKAGE, output_dirs)
        filenames = [fp for fp, _ in result]
        assert any("AiChatSession.java" in f for f in filenames)
        assert any("AiChatMessage.java" in f for f in filenames)
        assert any("AiChatSessionRepository.java" in f for f in filenames)
        assert any("AiChatMessageRepository.java" in f for f in filenames)
        assert any("ConversationMemoryService.java" in f for f in filenames)

    def test_all_content_is_nonempty(self, generator, sample_assistants, output_dirs):
        result = generator.generate(sample_assistants, BASE_PACKAGE, output_dirs)
        for filepath, content in result:
            assert content.strip(), f"Empty content for {filepath}"

    def test_empty_assistants_still_generates(self, generator, empty_assistants, output_dirs):
        """Even with no assistants, conversation files are generated (default window=20)."""
        result = generator.generate(empty_assistants, BASE_PACKAGE, output_dirs)
        assert len(result) == 5

    def test_default_output_dirs(self, generator, sample_assistants):
        result = generator.generate(sample_assistants, BASE_PACKAGE, {})
        filenames = [fp for fp, _ in result]
        assert any("ai/entity/AiChatSession.java" in f for f in filenames)
        assert any("ai/entity/AiChatMessage.java" in f for f in filenames)
        assert any("ai/repository/AiChatSessionRepository.java" in f for f in filenames)
        assert any("ai/repository/AiChatMessageRepository.java" in f for f in filenames)
        assert any("ai/service/ConversationMemoryService.java" in f for f in filenames)

    def test_output_dirs_used_in_paths(self, generator, sample_assistants, output_dirs):
        result = generator.generate(sample_assistants, BASE_PACKAGE, output_dirs)
        filenames = [fp for fp, _ in result]
        assert any("com/example/app/ai/entity/AiChatSession.java" in f for f in filenames)
        assert any("com/example/app/ai/repository/AiChatSessionRepository.java" in f for f in filenames)
        assert any("com/example/app/ai/service/ConversationMemoryService.java" in f for f in filenames)


class TestAiChatSessionEntity:
    """Tests for the AiChatSession entity template rendering."""

    def _render(self, generator):
        return generator._render_entity("ai/entity/ai_chat_session.java.j2", BASE_PACKAGE)

    def test_package_declaration(self, generator):
        content = self._render(generator)
        assert "package com.example.app.ai.entity;" in content

    def test_class_declaration(self, generator):
        content = self._render(generator)
        assert "public class AiChatSession" in content

    def test_table_annotation(self, generator):
        content = self._render(generator)
        assert '@Table("ai_chat_session")' in content

    def test_required_fields(self, generator):
        """Req 4.1: id, userId, entityType, entityId, standaloneOperationName,
        assistantName, createdAt, lastMessageAt."""
        content = self._render(generator)
        assert "private Long id;" in content
        assert "private Long userId;" in content
        assert "private String entityType;" in content
        assert "private Long entityId;" in content
        assert "private String standaloneOperationName;" in content
        assert "private String assistantName;" in content
        assert "private LocalDateTime createdAt;" in content
        assert "private LocalDateTime lastMessageAt;" in content

    def test_lombok_annotations(self, generator):
        content = self._render(generator)
        assert "@Data" in content
        assert "@Builder" in content
        assert "@NoArgsConstructor" in content
        assert "@AllArgsConstructor" in content

    def test_id_annotation(self, generator):
        content = self._render(generator)
        assert "@Id" in content


class TestAiChatMessageEntity:
    """Tests for the AiChatMessage entity template rendering."""

    def _render(self, generator):
        return generator._render_entity("ai/entity/ai_chat_message.java.j2", BASE_PACKAGE)

    def test_package_declaration(self, generator):
        content = self._render(generator)
        assert "package com.example.app.ai.entity;" in content

    def test_class_declaration(self, generator):
        content = self._render(generator)
        assert "public class AiChatMessage" in content

    def test_table_annotation(self, generator):
        content = self._render(generator)
        assert '@Table("ai_chat_message")' in content

    def test_required_fields(self, generator):
        """Req 4.2: id, sessionId, role, content (TEXT), createdAt."""
        content = self._render(generator)
        assert "private Long id;" in content
        assert "private Long sessionId;" in content
        assert "private String role;" in content
        assert "private String content;" in content
        assert "private LocalDateTime createdAt;" in content


class TestAiChatSessionRepository:
    """Tests for the AiChatSessionRepository template rendering."""

    def _render(self, generator):
        return generator._render_entity(
            "ai/repository/ai_chat_session_repository.java.j2", BASE_PACKAGE
        )

    def test_package_declaration(self, generator):
        content = self._render(generator)
        assert "package com.example.app.ai.repository;" in content

    def test_interface_declaration(self, generator):
        content = self._render(generator)
        assert "public interface AiChatSessionRepository" in content
        assert "ReactiveCrudRepository<AiChatSession, Long>" in content

    def test_repository_annotation(self, generator):
        content = self._render(generator)
        assert "@Repository" in content

    def test_query_methods(self, generator):
        """Req 4.3: Required query methods."""
        content = self._render(generator)
        assert "findByUserIdOrderByLastMessageAtDesc" in content
        assert "findByUserIdAndEntityTypeAndEntityId" in content
        assert "findByUserIdAndStandaloneOperationName" in content


class TestAiChatMessageRepository:
    """Tests for the AiChatMessageRepository template rendering."""

    def _render(self, generator):
        return generator._render_entity(
            "ai/repository/ai_chat_message_repository.java.j2", BASE_PACKAGE
        )

    def test_package_declaration(self, generator):
        content = self._render(generator)
        assert "package com.example.app.ai.repository;" in content

    def test_interface_declaration(self, generator):
        content = self._render(generator)
        assert "public interface AiChatMessageRepository" in content
        assert "ReactiveCrudRepository<AiChatMessage, Long>" in content

    def test_query_method(self, generator):
        """Req 4.4: findBySessionIdOrderByCreatedAtAsc."""
        content = self._render(generator)
        assert "findBySessionIdOrderByCreatedAtAsc" in content


class TestConversationMemoryService:
    """Tests for the ConversationMemoryService template rendering."""

    def _render(self, generator, window_size=20):
        return generator._render_conversation_memory_service(BASE_PACKAGE, window_size)

    def test_package_declaration(self, generator):
        content = self._render(generator)
        assert "package com.example.app.ai.service;" in content

    def test_class_declaration(self, generator):
        content = self._render(generator)
        assert "public class ConversationMemoryService" in content

    def test_service_annotation(self, generator):
        content = self._render(generator)
        assert "@Service" in content

    def test_slf4j_annotation(self, generator):
        content = self._render(generator)
        assert "@Slf4j" in content

    def test_default_memory_window_size(self, generator):
        """Req 4.5: memoryWindowSize default 20."""
        content = self._render(generator, window_size=20)
        assert "DEFAULT_MEMORY_WINDOW_SIZE = 20" in content

    def test_custom_memory_window_size(self, generator):
        content = self._render(generator, window_size=30)
        assert "DEFAULT_MEMORY_WINDOW_SIZE = 30" in content

    def test_create_entity_session_method(self, generator):
        """Req 4.6: Session creation for entity-bound conversations."""
        content = self._render(generator)
        assert "createEntitySession(" in content

    def test_create_standalone_session_method(self, generator):
        """Req 4.7: Session creation for standalone conversations."""
        content = self._render(generator)
        assert "createStandaloneSession(" in content

    def test_store_message_method(self, generator):
        """Req 4.8: Message storage."""
        content = self._render(generator)
        assert "storeMessage(" in content

    def test_build_conversation_context_method(self, generator):
        """Req 3.1, 3.8, 3.12: Context building with role ordering."""
        content = self._render(generator)
        assert "buildConversationContext(" in content

    def test_build_role_prompt_messages_method(self, generator):
        """Req 3.1, 3.8: rolePromptSequence ordering preserved."""
        content = self._render(generator)
        assert "buildRolePromptMessages(" in content

    def test_list_user_sessions_method(self, generator):
        content = self._render(generator)
        assert "listUserSessions(" in content

    def test_list_sessions_by_operation_method(self, generator):
        """Req 4.9: Filter sessions by standaloneOperationName."""
        content = self._render(generator)
        assert "listSessionsByOperation(" in content

    def test_list_sessions_by_entity_method(self, generator):
        content = self._render(generator)
        assert "listSessionsByEntity(" in content

    def test_uses_prompt_template_engine(self, generator):
        """Req 3.8: Interpolation via PromptTemplateEngine."""
        content = self._render(generator)
        assert "promptTemplateEngine.interpolate(" in content

    def test_reactive_types(self, generator):
        """All methods use reactive types (Mono/Flux)."""
        content = self._render(generator)
        assert "Mono<" in content
        assert "Flux<" in content

    def test_sliding_window_logic(self, generator):
        """Req 4.5: Sliding window for recent messages."""
        content = self._render(generator)
        assert "windowSize" in content
        assert "Math.max(0," in content

    def test_spring_ai_message_types(self, generator):
        """Uses Spring AI message types for role mapping."""
        content = self._render(generator)
        assert "SystemMessage" in content
        assert "AssistantMessage" in content
        assert "UserMessage" in content

    def test_dependencies_injected(self, generator):
        content = self._render(generator)
        assert "AiChatSessionRepository" in content
        assert "AiChatMessageRepository" in content
        assert "PromptTemplateEngine" in content
        assert "@RequiredArgsConstructor" in content


class TestResolveDefaultMemoryWindowSize:
    """Tests for the _resolve_default_memory_window_size static method."""

    def test_empty_assistants_returns_20(self):
        assert ConversationGenerator._resolve_default_memory_window_size([]) == 20

    def test_first_assistant_window_size(self):
        assistants = [{"memoryWindowSize": 50}, {"memoryWindowSize": 10}]
        assert ConversationGenerator._resolve_default_memory_window_size(assistants) == 50

    def test_assistant_without_window_size_defaults_to_20(self):
        assistants = [{"name": "test"}]
        assert ConversationGenerator._resolve_default_memory_window_size(assistants) == 20
