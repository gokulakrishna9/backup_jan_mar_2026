"""Evaluator sub-generator for the AI Layer.

Generates EvaluationPipelineService, EvaluationResultDTO,
AiResponseWithEvaluationDTO, EvaluationStatsDTO, EvaluatorBreakdownDTO,
AiEvaluationResult entity, AiEvaluationResultRepository, and
EvaluationController.

Requirements: 10.1–10.12
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2

# Valid evaluator types and scoring mechanisms
VALID_EVALUATOR_TYPES = {"relevancy", "correctness", "safety", "custom"}
VALID_SCORING_MECHANISMS = {"numeric", "pass_fail", "categorical"}
VALID_FAILURE_ACTIONS = {"none", "retry", "warn"}
VALID_MODES = {"sync", "async"}


def _pascal_case(name: str) -> str:
    """Convert a camelCase or snake_case name to PascalCase."""
    if "_" in name:
        return "".join(part.capitalize() for part in name.split("_"))
    return name[0].upper() + name[1:] if name else name


def _camel_case(name: str) -> str:
    """Convert a name to camelCase."""
    pascal = _pascal_case(name)
    return pascal[0].lower() + pascal[1:] if pascal else pascal


class EvaluatorGenerator:
    """Generates evaluator Java files from the AI_Layer definition."""

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        evaluators: list[dict] | None,
        base_package: str,
        output_dirs: dict[str, Path],
    ) -> list[tuple[str, str]]:
        """Generate evaluator Java files.

        Returns a list of ``(filepath, content)`` tuples where *filepath* is
        relative to the project source root.

        Req 10.3: When no evaluators are configured, no evaluator files are
        generated.
        """
        if not evaluators:
            return []

        results: list[tuple[str, str]] = []

        evaluator_dir = output_dirs.get("evaluator", Path("ai/evaluator"))
        controller_dir = output_dirs.get("controller", Path("ai/controller"))
        dto_dir = output_dirs.get("dto", Path("ai/dto"))
        entity_dir = output_dirs.get("entity", Path("ai/entity"))
        repository_dir = output_dirs.get("repository", Path("ai/repository"))

        # 1. EvaluationResultDTO (Req 10.9)
        results.append((
            str(dto_dir / "EvaluationResultDTO.java"),
            self._render("dto/evaluation_result_dto.java.j2", {
                "base_package": base_package,
            }),
        ))

        # 2. AiResponseWithEvaluationDTO (Req 10.8)
        results.append((
            str(dto_dir / "AiResponseWithEvaluationDTO.java"),
            self._render("dto/ai_response_with_evaluation_dto.java.j2", {
                "base_package": base_package,
            }),
        ))

        # 3. EvaluationStatsDTO (Req 10.9)
        results.append((
            str(dto_dir / "EvaluationStatsDTO.java"),
            self._render("dto/evaluation_stats_dto.java.j2", {
                "base_package": base_package,
            }),
        ))

        # 4. EvaluatorBreakdownDTO (Req 10.9)
        results.append((
            str(dto_dir / "EvaluatorBreakdownDTO.java"),
            self._render("dto/evaluator_breakdown_dto.java.j2", {
                "base_package": base_package,
            }),
        ))

        # 5. AiEvaluationResult entity (Req 10.9)
        results.append((
            str(entity_dir / "AiEvaluationResult.java"),
            self._render("entity/ai_evaluation_result.java.j2", {
                "base_package": base_package,
            }),
        ))

        # 6. AiEvaluationResultRepository (Req 10.9)
        results.append((
            str(repository_dir / "AiEvaluationResultRepository.java"),
            self._render("repository/ai_evaluation_result_repository.java.j2", {
                "base_package": base_package,
            }),
        ))

        # 7. EvaluationPipelineService (Req 10.3)
        ctx = self._build_pipeline_context(evaluators, base_package)
        results.append((
            str(evaluator_dir / "EvaluationPipelineService.java"),
            self._render("evaluator/evaluation_pipeline_service.java.j2", ctx),
        ))

        # 8. EvaluationController (Req 10.10)
        results.append((
            str(controller_dir / "EvaluationController.java"),
            self._render("controller/evaluation_controller.java.j2", {
                "base_package": base_package,
            }),
        ))

        return results

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_pipeline_context(
        self, evaluators: list[dict], base_package: str
    ) -> dict:
        """Build Jinja2 context for the EvaluationPipelineService template."""
        processed = []
        has_retry = False
        for ev in evaluators:
            failure_action = ev.get("failureAction", "none")
            mode = ev.get("mode", "async")
            if failure_action == "retry":
                has_retry = True
            processed.append({
                "name": ev["name"],
                "name_pascal": _pascal_case(ev["name"]),
                "name_camel": _camel_case(ev["name"]),
                "type": ev.get("type", "custom"),
                "provider_name": ev.get("providerName", ""),
                "evaluation_prompt": ev.get("evaluationPrompt", ""),
                "scoring_mechanism": ev.get("scoringMechanism", "numeric"),
                "threshold": ev.get("threshold", 0.5),
                "categories": ev.get("categories", []),
                "failure_action": failure_action,
                "max_retries": ev.get("maxRetries", 1),
                "mode": mode,
            })

        return {
            "base_package": base_package,
            "evaluators": processed,
            "has_retry_evaluators": has_retry,
        }

    def _render(self, template_name: str, ctx: dict) -> str:
        """Render a Jinja2 template under the ai/ prefix."""
        template = self.jinja_env.get_template(f"ai/{template_name}")
        return template.render(**ctx)
