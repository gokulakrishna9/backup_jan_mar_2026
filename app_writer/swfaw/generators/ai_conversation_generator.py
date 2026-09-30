"""Conversation sub-generator for the AI Layer.

Generates ConversationMemoryService, AiChatSession/AiChatMessage entities,
and their repositories from the AI_Layer definition.

Requirements: 3.1–3.12, 4.1–4.9
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2


class ConversationGenerator:
    """Generates ConversationMemoryService, AiChatSession, AiChatMessage,
    and their repositories."""

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        assistants: list[dict],
        base_package: str,
        output_dirs: dict[str, Path],
    ) -> list[tuple[str, str]]:
        """Generate all conversation-related Java files.

        Returns a list of ``(filepath, content)`` tuples where *filepath* is
        relative to the project source root.
        """
        results: list[tuple[str, str]] = []

        entity_dir = output_dirs.get("entity", Path("ai/entity"))
        repository_dir = output_dirs.get("repository", Path("ai/repository"))
        service_dir = output_dirs.get("service", Path("ai/service"))

        # Derive default memoryWindowSize from assistants (use first or 20)
        default_memory_window_size = self._resolve_default_memory_window_size(
            assistants
        )

        # 1. AiChatSession entity (Req 4.1)
        content = self._render_entity(
            "ai/entity/ai_chat_session.java.j2", base_package
        )
        results.append((str(entity_dir / "AiChatSession.java"), content))

        # 2. AiChatMessage entity (Req 4.2)
        content = self._render_entity(
            "ai/entity/ai_chat_message.java.j2", base_package
        )
        results.append((str(entity_dir / "AiChatMessage.java"), content))

        # 3. AiChatSessionRepository (Req 4.3)
        content = self._render_entity(
            "ai/repository/ai_chat_session_repository.java.j2", base_package
        )
        results.append(
            (str(repository_dir / "AiChatSessionRepository.java"), content)
        )

        # 4. AiChatMessageRepository (Req 4.4)
        content = self._render_entity(
            "ai/repository/ai_chat_message_repository.java.j2", base_package
        )
        results.append(
            (str(repository_dir / "AiChatMessageRepository.java"), content)
        )

        # 5. ConversationMemoryService (Req 3.1–3.12, 4.5–4.9)
        content = self._render_conversation_memory_service(
            base_package, default_memory_window_size
        )
        results.append(
            (str(service_dir / "ConversationMemoryService.java"), content)
        )

        return results

    # ------------------------------------------------------------------
    # Private render helpers
    # ------------------------------------------------------------------

    def _render_entity(self, template_path: str, base_package: str) -> str:
        """Render a simple entity/repository template with base_package."""
        template = self.jinja_env.get_template(template_path)
        return template.render(base_package=base_package)

    def _render_conversation_memory_service(
        self, base_package: str, default_memory_window_size: int
    ) -> str:
        """Render the ConversationMemoryService.

        Req 3.1: rolePromptSequence ordering preserved during interpolation.
        Req 3.2–3.7: Session creation, message storage, sliding-window context.
        Req 3.8: rolePromptSequence ordering preserved.
        Req 3.9–3.11: Role validation integration (via RoleValidationAdvisor).
        Req 3.12: Conversation context building with role ordering.
        Req 4.5–4.9: Memory window, session queries, message storage.
        """
        template = self.jinja_env.get_template(
            "ai/service/conversation_memory_service.java.j2"
        )
        return template.render(
            base_package=base_package,
            default_memory_window_size=default_memory_window_size,
        )

    @staticmethod
    def _resolve_default_memory_window_size(
        assistants: list[dict],
    ) -> int:
        """Resolve the default memoryWindowSize.

        Uses the first assistant's memoryWindowSize if available,
        otherwise falls back to 20 (the spec default).
        """
        if assistants:
            return assistants[0].get("memoryWindowSize", 20)
        return 20
