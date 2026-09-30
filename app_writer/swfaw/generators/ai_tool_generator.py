"""Tool function sub-generator for the AI Layer.

Generates EntityAiToolFunctions, StandaloneAiToolFunctions,
DocumentTaskToolFunctions, RagToolFunctions,
DocumentIngestionToolFunctions, and ToolSecurityContextHolder.

Requirements: 13.1–13.3, 13.10–13.14
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2


def _pascal(name: str) -> str:
    """Convert a snake_case or camelCase name to PascalCase."""
    if "_" in name:
        return "".join(part.capitalize() for part in name.split("_"))
    if name:
        return name[0].upper() + name[1:]
    return name


def _camel(name: str) -> str:
    """Convert a name to camelCase."""
    pascal = _pascal(name)
    if pascal:
        return pascal[0].lower() + pascal[1:]
    return pascal


class ToolFunctionGenerator:
    """Generates tool function Java files from the AI_Layer definition.

    Follows the same sub-generator pattern as OrchestratorGenerator:
    receives parsed definition data, checks whether the feature is
    enabled, loads and renders Jinja2 templates, and returns a list
    of ``(filepath, content)`` tuples.

    Req 13.1: When the orchestrator is present, generate tool function
    classes for entity capabilities, standalone operations, document
    tasks, RAG sources, and document ingestion.

    Req 13.9: When the orchestrator is absent, no tool files are generated.
    """

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        orchestrator: dict | None,
        entity_capabilities: list[dict] | None,
        standalone_operations: list[dict] | None,
        document_processing: dict | None,
        rag_sources: list[dict] | None,
        document_ingestion: dict | None,
        base_package: str,
        output_dirs: dict[str, Path],
    ) -> list[tuple[str, str]]:
        """Generate tool function Java files.

        Returns a list of ``(filepath, content)`` tuples where *filepath*
        is relative to the project source root.

        Req 13.9: When the orchestrator object is absent/null, no
        tool files are generated.
        """
        if not orchestrator:
            return []

        results: list[tuple[str, str]] = []

        tools_dir = output_dirs.get("tools", Path("ai/tools"))

        # 1. ToolSecurityContextHolder (Req 13.12)
        results.append((
            str(tools_dir / "ToolSecurityContextHolder.java"),
            self._render(
                "tools/tool_security_context_holder.java.j2",
                {"base_package": base_package},
            ),
        ))

        # 2. EntityAiToolFunctions per entity (Req 13.1)
        for cap in (entity_capabilities or []):
            ctx = self._build_entity_tool_context(cap, base_package)
            results.append((
                str(tools_dir / f"{ctx['entity_name']}AiToolFunctions.java"),
                self._render(
                    "tools/entity_ai_tool_functions.java.j2", ctx
                ),
            ))

        # 3. StandaloneAiToolFunctions per operation (Req 13.1)
        for op in (standalone_operations or []):
            ctx = self._build_standalone_tool_context(op, base_package)
            results.append((
                str(tools_dir / f"{ctx['operation_name']}AiToolFunctions.java"),
                self._render(
                    "tools/standalone_ai_tool_functions.java.j2", ctx
                ),
            ))

        # 4. DocumentTaskToolFunctions per task (Req 13.1)
        if document_processing and document_processing.get("enabled"):
            for task in document_processing.get("tasks", []):
                ctx = self._build_doc_task_tool_context(task, base_package)
                results.append((
                    str(tools_dir / f"{ctx['task_name_pascal']}DocumentTaskToolFunctions.java"),
                    self._render(
                        "tools/document_task_tool_functions.java.j2", ctx
                    ),
                ))

        # 5. RagToolFunctions (Req 13.1) — only if RAG sources exist
        semantic_sources = [
            s for s in (rag_sources or [])
            if s.get("type") == "semantic" and s.get("enabled", False)
        ]
        if semantic_sources:
            results.append((
                str(tools_dir / "RagToolFunctions.java"),
                self._render(
                    "tools/rag_tool_functions.java.j2",
                    {"base_package": base_package},
                ),
            ))

        # 6. DocumentIngestionToolFunctions (Req 13.1)
        if document_ingestion and document_ingestion.get("enabled"):
            results.append((
                str(tools_dir / "DocumentIngestionToolFunctions.java"),
                self._render(
                    "tools/document_ingestion_tool_functions.java.j2",
                    {"base_package": base_package},
                ),
            ))

        return results

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_entity_tool_context(
        self, capability: dict, base_package: str
    ) -> dict:
        """Build Jinja2 context for entity tool function templates."""
        entity_name = _pascal(capability.get("entityName", ""))
        enabled_ops = capability.get("enabledOperations", [])
        return {
            "base_package": base_package,
            "entity_name": entity_name,
            "entity_name_camel": _camel(entity_name),
            "has_search": "search" in enabled_ops,
            "has_generate": "generate" in enabled_ops,
            "has_summarize": "summarize" in enabled_ops,
            "has_classify": "classify" in enabled_ops,
            "has_chat": "chat" in enabled_ops,
        }

    def _build_standalone_tool_context(
        self, operation: dict, base_package: str
    ) -> dict:
        """Build Jinja2 context for standalone tool function templates.

        Req 13.1: Standalone tools include chat, generate, query
        — NOT chatStream.
        """
        raw_name = operation.get("name", "")
        op_name = _pascal(raw_name)
        enabled_actions = operation.get("enabledActions", [])
        return {
            "base_package": base_package,
            "operation_name": op_name,
            "operation_name_camel": _camel(op_name),
            "operation_raw_name": raw_name,
            "has_chat": "chat" in enabled_actions,
            "has_generate": "generate" in enabled_actions,
            "has_query": "query" in enabled_actions,
        }

    def _build_doc_task_tool_context(
        self, task: dict, base_package: str
    ) -> dict:
        """Build Jinja2 context for document task tool function templates."""
        task_name = task.get("name", "")
        return {
            "base_package": base_package,
            "task_name": task_name,
            "task_name_pascal": _pascal(task_name),
            "task_type": task.get("taskType", ""),
        }

    def _render(self, template_name: str, ctx: dict) -> str:
        """Render a Jinja2 template under the ai/ prefix."""
        template = self.jinja_env.get_template(f"ai/{template_name}")
        return template.render(**ctx)
