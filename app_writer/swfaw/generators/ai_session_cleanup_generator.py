"""Session cleanup sub-generator for the AI Layer.

Generates ChatSessionCleanupScheduler with cron, batch processing, TTL logic,
TopicSummarizationService with LLM-based topic extraction and topic table upserts,
TopicAnalyticsController with user/global/admin endpoints, and topic DTOs and
entities (AiTopic, AiUserTopicHit, AiGlobalTopicHit).

Requirements: 4.10–4.25
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2

# Default configuration values (Req 1.17)
DEFAULT_TTL_DAYS = 30
DEFAULT_CLEANUP_CRON = "0 0 2 * * *"
DEFAULT_BATCH_SIZE = 1000
DEFAULT_MAX_TOPICS_PER_SESSION = 5


class SessionCleanupGenerator:
    """Generates session cleanup Java files from the AI_Layer definition.

    Follows the same sub-generator pattern as AuditGenerator:
    receives parsed definition data, checks whether the feature is
    enabled, loads and renders Jinja2 templates, and returns a list
    of ``(filepath, content)`` tuples.
    """

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        chat_session_cleanup: dict | None,
        base_package: str,
        output_dirs: dict[str, Path],
    ) -> list[tuple[str, str]]:
        """Generate session cleanup Java files.

        Returns a list of ``(filepath, content)`` tuples where *filepath*
        is relative to the project source root.

        Req 4.23: When chatSessionCleanup is absent or ``enabled`` is
        false, no cleanup files are generated.
        """
        if not chat_session_cleanup or not chat_session_cleanup.get("enabled", False):
            return []

        results: list[tuple[str, str]] = []

        scheduler_dir = output_dirs.get("scheduler", Path("ai/scheduler"))
        service_dir = output_dirs.get("service", Path("ai/service"))
        controller_dir = output_dirs.get("controller", Path("ai/controller"))
        dto_dir = output_dirs.get("dto", Path("ai/dto"))
        entity_dir = output_dirs.get("entity", Path("ai/entity"))
        repository_dir = output_dirs.get("repository", Path("ai/repository"))

        ctx = self._build_context(chat_session_cleanup, base_package)

        # 1. ChatSessionCleanupScheduler (Req 4.10–4.14, 4.19, 4.25)
        results.append((
            str(scheduler_dir / "ChatSessionCleanupScheduler.java"),
            self._render("scheduler/chat_session_cleanup_scheduler.java.j2", ctx),
        ))

        # Topic summarization files — only when topicSummarization is enabled
        if ctx["topic_summarization_enabled"]:
            # 2. TopicSummarizationService (Req 4.15–4.17, 4.19)
            results.append((
                str(service_dir / "TopicSummarizationService.java"),
                self._render("service/topic_summarization_service.java.j2", ctx),
            ))

            # 3. TopicAnalyticsController (Req 4.20)
            results.append((
                str(controller_dir / "TopicAnalyticsController.java"),
                self._render("controller/topic_analytics_controller.java.j2", ctx),
            ))

            # 4. AiTopic entity (Req 4.18)
            results.append((
                str(entity_dir / "AiTopic.java"),
                self._render("entity/ai_topic.java.j2", {"base_package": base_package}),
            ))

            # 5. AiUserTopicHit entity (Req 4.18)
            results.append((
                str(entity_dir / "AiUserTopicHit.java"),
                self._render("entity/ai_user_topic_hit.java.j2", {"base_package": base_package}),
            ))

            # 6. AiGlobalTopicHit entity (Req 4.18)
            results.append((
                str(entity_dir / "AiGlobalTopicHit.java"),
                self._render("entity/ai_global_topic_hit.java.j2", {"base_package": base_package}),
            ))

            # 7. AiTopicRepository (Req 4.17)
            results.append((
                str(repository_dir / "AiTopicRepository.java"),
                self._render("repository/ai_topic_repository.java.j2", {"base_package": base_package}),
            ))

            # 8. AiUserTopicHitRepository (Req 4.17, 4.20)
            results.append((
                str(repository_dir / "AiUserTopicHitRepository.java"),
                self._render("repository/ai_user_topic_hit_repository.java.j2", {"base_package": base_package}),
            ))

            # 9. AiGlobalTopicHitRepository (Req 4.17, 4.20)
            results.append((
                str(repository_dir / "AiGlobalTopicHitRepository.java"),
                self._render("repository/ai_global_topic_hit_repository.java.j2", {"base_package": base_package}),
            ))

            # 10. TopicDTO (Req 4.21)
            results.append((
                str(dto_dir / "TopicDTO.java"),
                self._render("dto/topic_dto.java.j2", {"base_package": base_package}),
            ))

            # 11. UserTopicHitDTO (Req 4.21)
            results.append((
                str(dto_dir / "UserTopicHitDTO.java"),
                self._render("dto/user_topic_hit_dto.java.j2", {"base_package": base_package}),
            ))

            # 12. GlobalTopicHitDTO (Req 4.21)
            results.append((
                str(dto_dir / "GlobalTopicHitDTO.java"),
                self._render("dto/global_topic_hit_dto.java.j2", {"base_package": base_package}),
            ))

            # 13. TopicAnalyticsResponseDTO (Req 4.21)
            results.append((
                str(dto_dir / "TopicAnalyticsResponseDTO.java"),
                self._render("dto/topic_analytics_response_dto.java.j2", {"base_package": base_package}),
            ))

        return results

    # ------------------------------------------------------------------
    # Context builders
    # ------------------------------------------------------------------

    def _build_context(self, cleanup: dict, base_package: str) -> dict:
        """Build the Jinja2 template context from the chatSessionCleanup config."""
        topic_cfg = cleanup.get("topicSummarization") or {}
        topic_enabled = topic_cfg.get("enabled", False)

        return {
            "base_package": base_package,
            "default_ttl_days": cleanup.get("defaultTtlDays", DEFAULT_TTL_DAYS),
            "cleanup_cron": cleanup.get(
                "cleanupCronExpression", DEFAULT_CLEANUP_CRON
            ),
            "batch_size": cleanup.get("batchSize", DEFAULT_BATCH_SIZE),
            "topic_summarization_enabled": topic_enabled,
            "topic_provider_name": topic_cfg.get("providerName", ""),
            "max_topics_per_session": topic_cfg.get(
                "maxTopicsPerSession", DEFAULT_MAX_TOPICS_PER_SESSION
            ),
        }

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _render(self, template_name: str, ctx: dict) -> str:
        """Render a Jinja2 template under the ai/ prefix."""
        template = self.jinja_env.get_template(f"ai/{template_name}")
        return template.render(**ctx)
