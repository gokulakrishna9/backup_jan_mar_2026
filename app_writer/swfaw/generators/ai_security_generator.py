"""Security sub-generator for the AI Layer.

Generates SafeGuardAdvisorService, CanaryWordAdvisorService,
InputSanitizationService, OutputFilteringService, and ModerationService.

Requirements: 13.17–13.28, 14.1–14.8
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2

# Valid moderation failure actions
VALID_FAILURE_ACTIONS = {"block", "warn", "log"}

# Default moderation categories
DEFAULT_MODERATION_CATEGORIES = [
    "hate", "violence", "sexual", "self_harm",
]


class SecurityGenerator:
    """Generates prompt security and moderation Java files.

    Follows the same sub-generator pattern as OrchestratorGenerator:
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
        """Generate security-related Java files.

        Returns a list of ``(filepath, content)`` tuples where *filepath*
        is relative to the project source root.

        When the orchestrator is absent or neither promptSecurity nor
        moderation is configured, no security files are generated.
        """
        if not orchestrator:
            return []

        prompt_security = orchestrator.get("promptSecurity")
        moderation = orchestrator.get("moderation")

        # If neither section is configured, nothing to generate
        if not prompt_security and not moderation:
            return []

        results: list[tuple[str, str]] = []

        orchestrator_dir = output_dirs.get(
            "orchestrator", Path("ai/orchestrator")
        )
        dto_dir = output_dirs.get("dto", Path("ai/dto"))

        # --- Prompt Security Advisors ---
        if prompt_security:
            results.extend(
                self._generate_prompt_security(
                    prompt_security, base_package, orchestrator_dir, dto_dir
                )
            )

        # --- Content Moderation ---
        if moderation and moderation.get("enabled", False):
            results.extend(
                self._generate_moderation(
                    moderation, base_package, orchestrator_dir, dto_dir
                )
            )

        return results

    # ------------------------------------------------------------------
    # Prompt Security generation
    # ------------------------------------------------------------------

    def _generate_prompt_security(
        self,
        prompt_security: dict,
        base_package: str,
        orchestrator_dir: Path,
        dto_dir: Path,
    ) -> list[tuple[str, str]]:
        """Generate prompt security advisor services."""
        results: list[tuple[str, str]] = []

        safeguard = prompt_security.get("safeGuardAdvisor", {})
        canary = prompt_security.get("canaryWordAdvisor", {})
        input_san = prompt_security.get("inputSanitization", {})
        output_filt = prompt_security.get("outputFiltering", {})

        # Track whether we need the PromptSecurityViolationDTO
        needs_violation_dto = False

        # 1. SafeGuardAdvisorService (Req 13.17, 13.21)
        if safeguard.get("enabled", False):
            sensitive_words = safeguard.get("sensitiveWords", [])
            results.append((
                str(orchestrator_dir / "SafeGuardAdvisorService.java"),
                self._render(
                    "orchestrator/safe_guard_advisor_service.java.j2",
                    {
                        "base_package": base_package,
                        "sensitive_words": sensitive_words,
                    },
                ),
            ))
            needs_violation_dto = True

        # 2. CanaryWordAdvisorService (Req 13.18, 13.22)
        if canary.get("enabled", False):
            canary_tokens = canary.get("canaryTokens", [])
            results.append((
                str(orchestrator_dir / "CanaryWordAdvisorService.java"),
                self._render(
                    "orchestrator/canary_word_advisor_service.java.j2",
                    {
                        "base_package": base_package,
                        "canary_tokens": canary_tokens,
                    },
                ),
            ))
            needs_violation_dto = True

        # 3. InputSanitizationService (Req 13.19)
        if input_san.get("enabled", False):
            rules = input_san.get("rules", [])
            results.append((
                str(orchestrator_dir / "InputSanitizationService.java"),
                self._render(
                    "orchestrator/input_sanitization_service.java.j2",
                    {
                        "base_package": base_package,
                        "sanitization_rules": rules,
                    },
                ),
            ))

        # 4. OutputFilteringService (Req 13.20)
        if output_filt.get("enabled", False):
            rules = output_filt.get("rules", [])
            results.append((
                str(orchestrator_dir / "OutputFilteringService.java"),
                self._render(
                    "orchestrator/output_filtering_service.java.j2",
                    {
                        "base_package": base_package,
                        "filtering_rules": rules,
                    },
                ),
            ))

        # 5. PromptSecurityViolationDTO (Req 13.27)
        if needs_violation_dto:
            results.append((
                str(dto_dir / "PromptSecurityViolationDTO.java"),
                self._render(
                    "dto/prompt_security_violation_dto.java.j2",
                    {"base_package": base_package},
                ),
            ))

        return results

    # ------------------------------------------------------------------
    # Moderation generation
    # ------------------------------------------------------------------

    def _generate_moderation(
        self,
        moderation: dict,
        base_package: str,
        orchestrator_dir: Path,
        dto_dir: Path,
    ) -> list[tuple[str, str]]:
        """Generate moderation service and DTOs."""
        results: list[tuple[str, str]] = []

        ctx = self._build_moderation_context(moderation, base_package)

        # 1. ModerationService (Req 13.23–13.26, 13.28)
        results.append((
            str(orchestrator_dir / "ModerationService.java"),
            self._render(
                "orchestrator/moderation_service.java.j2", ctx
            ),
        ))

        # 2. ModerationResultDTO (Req 13.26, 13.27)
        results.append((
            str(dto_dir / "ModerationResultDTO.java"),
            self._render(
                "dto/moderation_result_dto.java.j2",
                {"base_package": base_package},
            ),
        ))

        # 3. ModerationErrorResponseDTO (Req 13.27)
        results.append((
            str(dto_dir / "ModerationErrorResponseDTO.java"),
            self._render(
                "dto/moderation_error_response_dto.java.j2",
                {"base_package": base_package},
            ),
        ))

        return results

    # ------------------------------------------------------------------
    # Context builders
    # ------------------------------------------------------------------

    def _build_moderation_context(
        self, moderation: dict, base_package: str
    ) -> dict:
        """Build Jinja2 context for moderation templates."""
        provider_name = moderation.get("providerName", "")
        categories = moderation.get("categories", DEFAULT_MODERATION_CATEGORIES[:])
        pre_moderation = moderation.get("preModeration", True)
        post_moderation = moderation.get("postModeration", True)
        failure_action = moderation.get("failureAction", "block")

        return {
            "base_package": base_package,
            "provider_name": provider_name,
            "categories": categories,
            "pre_moderation": pre_moderation,
            "post_moderation": post_moderation,
            "failure_action": failure_action,
        }

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _render(self, template_name: str, ctx: dict) -> str:
        """Render a Jinja2 template under the ai/ prefix."""
        template = self.jinja_env.get_template(f"ai/{template_name}")
        return template.render(**ctx)
