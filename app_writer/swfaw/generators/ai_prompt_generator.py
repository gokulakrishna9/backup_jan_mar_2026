"""Prompt sub-generator for the AI Layer.

Generates the PromptTemplateEngine utility class that handles
``{{placeholder}}`` interpolation in prompt template strings.

Requirements: 3.13–3.22
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2


class PromptGenerator:
    """Generates the PromptTemplateEngine utility class."""

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        base_package: str,
        output_dirs: dict[str, Path],
    ) -> list[tuple[str, str]]:
        """Generate the PromptTemplateEngine Java file.

        Returns a list of ``(filepath, content)`` tuples where *filepath* is
        relative to the project source root.
        """
        results: list[tuple[str, str]] = []

        service_dir = output_dirs.get("service", Path("ai/service"))

        content = self._render_prompt_template_engine(base_package)
        results.append((str(service_dir / "PromptTemplateEngine.java"), content))

        return results

    # ------------------------------------------------------------------
    # Private render helpers
    # ------------------------------------------------------------------

    def _render_prompt_template_engine(self, base_package: str) -> str:
        """Render the PromptTemplateEngine utility class.

        Req 3.13: Accept template string with ``{{placeholder}}`` and value map.
        Req 3.14: Replace each placeholder with corresponding map value.
        Req 3.15: Leave unresolved placeholders unchanged, log warning.
        Req 3.18: Synchronous utility, safe in reactive pipelines.
        Req 3.19: Single-pass replacement (no recursive interpolation).
        Req 3.20: Handle nested braces (``{{{value}}}``).
        Req 3.21: Handle templates with no placeholders (return unchanged).
        Req 3.22: Handle null/empty templates gracefully.
        """
        template = self.jinja_env.get_template(
            "ai/service/prompt_template_engine.java.j2"
        )
        return template.render(base_package=base_package)
