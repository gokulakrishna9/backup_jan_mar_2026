"""Orchestrator sub-generator for the AI Layer.

Generates AiOrchestratorService, AiOrchestratorController, and
OrchestratorResponseDTO.

Requirements: 13.4–13.9, 13.15–13.16, 13.29–13.31
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2

# Default access denied message when none is configured
DEFAULT_ACCESS_DENIED_MESSAGE = (
    "You do not have permission to perform this action."
)


class OrchestratorGenerator:
    """Generates orchestrator Java files from the AI_Layer definition.

    Follows the same sub-generator pattern as EvaluatorGenerator:
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
        orchestrator: dict | None,
        base_package: str,
        output_dirs: dict[str, Path],
    ) -> list[tuple[str, str]]:
        """Generate orchestrator Java files.

        Returns a list of ``(filepath, content)`` tuples where *filepath*
        is relative to the project source root.

        Req 13.9: When the orchestrator object is absent/null, no
        orchestrator files are generated.
        """
        if not orchestrator:
            return []

        results: list[tuple[str, str]] = []

        orchestrator_dir = output_dirs.get(
            "orchestrator", Path("ai/orchestrator")
        )
        controller_dir = output_dirs.get(
            "controller", Path("ai/controller")
        )
        dto_dir = output_dirs.get("dto", Path("ai/dto"))

        # Build template context
        ctx = self._build_context(orchestrator, base_package)

        # 1. OrchestratorResponseDTO (Req 13.5)
        results.append((
            str(dto_dir / "OrchestratorResponseDTO.java"),
            self._render(
                "dto/orchestrator_response_dto.java.j2",
                {"base_package": base_package},
            ),
        ))

        # 2. AiOrchestratorService (Req 13.4, 13.5, 13.6, 13.7)
        results.append((
            str(orchestrator_dir / "AiOrchestratorService.java"),
            self._render(
                "orchestrator/ai_orchestrator_service.java.j2", ctx
            ),
        ))

        # 3. AiOrchestratorController (Req 13.8)
        results.append((
            str(controller_dir / "AiOrchestratorController.java"),
            self._render(
                "controller/orchestrator_controller.java.j2",
                {"base_package": base_package},
            ),
        ))

        return results

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_context(
        self, orchestrator: dict, base_package: str
    ) -> dict:
        """Build Jinja2 context for orchestrator templates."""
        provider_name = orchestrator.get("providerName", "")
        system_prompt = orchestrator.get("systemPrompt", "")
        chat_options = orchestrator.get("chatOptions")
        access_denied_message = orchestrator.get(
            "accessDeniedMessage", DEFAULT_ACCESS_DENIED_MESSAGE
        )

        return {
            "base_package": base_package,
            "provider_name": provider_name,
            "system_prompt": system_prompt,
            "chat_options": chat_options,
            "access_denied_message": access_denied_message,
        }

    def _render(self, template_name: str, ctx: dict) -> str:
        """Render a Jinja2 template under the ai/ prefix."""
        template = self.jinja_env.get_template(f"ai/{template_name}")
        return template.render(**ctx)
