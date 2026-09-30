"""Audit log sub-generator for the AI Layer.

Generates AiAuditService (async fire-and-forget), AiAuditCleanupScheduler,
AiAuditController, AiAuditLog entity/repository, and DTOs
(AiAuditEventDTO, AiAuditStatsDTO, AiAuditPageDTO).

Requirements: 15.34–15.47
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2

# Default configuration values
DEFAULT_RETENTION_DAYS = 90
DEFAULT_CLEANUP_CRON = "0 0 3 * * *"
VALID_EVENT_TYPES = frozenset({
    "orchestrator_request",
    "tool_invocation",
    "moderation_flag",
    "security_violation",
    "budget_exceeded",
    "session_created",
    "document_ingested",
    "provider_error",
    "circuit_breaker_state_change",
})
CLEANUP_BATCH_SIZE = 5000


class AuditGenerator:
    """Generates audit log Java files from the AI_Layer definition.

    Follows the same sub-generator pattern as TokenBudgetGenerator:
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
        audit_log: dict | None,
        base_package: str,
        output_dirs: dict[str, Path],
    ) -> list[tuple[str, str]]:
        """Generate audit log Java files.

        Returns a list of ``(filepath, content)`` tuples where *filepath*
        is relative to the project source root.

        Req 15.43: When auditLog is absent or ``enabled`` is false,
        no audit files are generated.
        """
        if not audit_log or not audit_log.get("enabled", False):
            return []

        results: list[tuple[str, str]] = []

        audit_dir = output_dirs.get("audit", Path("ai/audit"))
        controller_dir = output_dirs.get("controller", Path("ai/controller"))
        dto_dir = output_dirs.get("dto", Path("ai/dto"))
        entity_dir = output_dirs.get("entity", Path("ai/entity"))
        repository_dir = output_dirs.get("repository", Path("ai/repository"))

        # Build template context
        ctx = self._build_context(audit_log, base_package)

        # 1. AiAuditService (Req 15.34, 15.35, 15.44, 15.45, 15.47)
        results.append((
            str(audit_dir / "AiAuditService.java"),
            self._render("audit/ai_audit_service.java.j2", ctx),
        ))

        # 2. AiAuditCleanupScheduler (Req 15.38)
        results.append((
            str(audit_dir / "AiAuditCleanupScheduler.java"),
            self._render("audit/ai_audit_cleanup_scheduler.java.j2", ctx),
        ))

        # 3. AiAuditController (Req 15.39)
        results.append((
            str(controller_dir / "AiAuditController.java"),
            self._render("controller/audit_controller.java.j2", ctx),
        ))

        # 4. AiAuditLog entity (Req 15.41)
        results.append((
            str(entity_dir / "AiAuditLog.java"),
            self._render("entity/ai_audit_log.java.j2", {"base_package": base_package}),
        ))

        # 5. AiAuditLogRepository (Req 15.41)
        results.append((
            str(repository_dir / "AiAuditLogRepository.java"),
            self._render("repository/ai_audit_log_repository.java.j2", {"base_package": base_package}),
        ))

        # 6. AiAuditEventDTO (Req 15.40)
        results.append((
            str(dto_dir / "AiAuditEventDTO.java"),
            self._render("dto/ai_audit_event_dto.java.j2", {"base_package": base_package}),
        ))

        # 7. AiAuditStatsDTO (Req 15.40)
        results.append((
            str(dto_dir / "AiAuditStatsDTO.java"),
            self._render("dto/ai_audit_stats_dto.java.j2", {"base_package": base_package}),
        ))

        # 8. AiAuditPageDTO (Req 15.40)
        results.append((
            str(dto_dir / "AiAuditPageDTO.java"),
            self._render("dto/ai_audit_page_dto.java.j2", {"base_package": base_package}),
        ))

        return results

    # ------------------------------------------------------------------
    # Context builders
    # ------------------------------------------------------------------

    def _build_context(self, audit_log: dict, base_package: str) -> dict:
        """Build the Jinja2 template context from the auditLog config."""
        logged_events = audit_log.get("loggedEvents") or []

        return {
            "base_package": base_package,
            "retention_days": audit_log.get(
                "retentionDays", DEFAULT_RETENTION_DAYS
            ),
            "cleanup_cron": audit_log.get(
                "cleanupCronExpression", DEFAULT_CLEANUP_CRON
            ),
            "logged_events": logged_events,
            "log_all_events": len(logged_events) == 0,
            "cleanup_batch_size": CLEANUP_BATCH_SIZE,
        }

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _render(self, template_name: str, ctx: dict) -> str:
        """Render a Jinja2 template under the ai/ prefix."""
        template = self.jinja_env.get_template(f"ai/{template_name}")
        return template.render(**ctx)
