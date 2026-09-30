"""Standalone AI sub-generator for the AI Layer.

Generates per-operation Standalone_AI_Service and Standalone_AI_Controller
classes for entries in ``standaloneOperations``.  Each service conditionally
includes methods based on ``enabledActions`` (chat, chatStream, generate,
query) and injects a ``ChatClient`` bean via ``@Qualifier("<providerName>")``.

When a ``stateTable`` is defined, a corresponding R2DBC entity class and
repository are also generated.

When an ``assistantName`` is referenced, the assistant's configuration
(rolePromptSequence, systemPrompt, memoryWindowSize) is used.

Requirements: 6.1–6.10
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2

# SQL type → Java type mapping for stateTable columns
_SQL_TO_JAVA_TYPE: dict[str, str] = {
    "VARCHAR": "String",
    "TEXT": "String",
    "INT": "Integer",
    "BIGINT": "Long",
    "BOOLEAN": "Boolean",
    "DATETIME": "java.time.LocalDateTime",
    "JSON": "String",
    "DOUBLE": "Double",
}


class StandaloneAiGenerator:
    """Generates per-operation Standalone_AI_Service and Standalone_AI_Controller classes."""

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        standalone_operations: list[dict],
        base_package: str,
        output_dirs: dict[str, Path],
        assistants: list[dict] | None = None,
    ) -> list[tuple[str, str]]:
        """Generate standalone AI service, controller, and optional state files.

        Returns a list of ``(filepath, content)`` tuples where *filepath* is
        relative to the project source root.

        Req 6.1: When ``standaloneOperations`` is empty, no code is generated.
        """
        if not standalone_operations:
            return []

        results: list[tuple[str, str]] = []

        service_dir = output_dirs.get("service", Path("ai/service"))
        controller_dir = output_dirs.get("controller", Path("ai/controller"))
        entity_dir = output_dirs.get("entity", Path("ai/entity"))
        repository_dir = output_dirs.get("repository", Path("ai/repository"))

        assistant_map = self._build_assistant_map(assistants)

        for op in standalone_operations:
            op_name: str = op.get("name", "")
            if not op_name:
                continue

            pascal_name = self._to_pascal_case(op_name)
            camel_name = pascal_name[0].lower() + pascal_name[1:] if pascal_name else ""

            ctx = self._build_template_context(
                op, base_package, pascal_name, camel_name, assistant_map,
            )

            # 1. Standalone_AI_Service (Req 6.1, 6.2–6.6)
            content = self._render_service(ctx)
            results.append(
                (str(service_dir / f"{pascal_name}AiService.java"), content)
            )

            # 2. Standalone_AI_Controller (Req 6.1, 6.9, 6.10)
            content = self._render_controller(ctx)
            results.append(
                (str(controller_dir / f"{pascal_name}AiController.java"), content)
            )

            # 3. State entity + repository (Req 6.7) — only when stateTable defined
            state_table = op.get("stateTable")
            if state_table:
                state_ctx = self._build_state_context(
                    state_table, base_package, pascal_name, op_name,
                )
                content = self._render_state_entity(state_ctx)
                results.append(
                    (str(entity_dir / f"{pascal_name}State.java"), content)
                )
                content = self._render_state_repository(state_ctx)
                results.append(
                    (str(repository_dir / f"{pascal_name}StateRepository.java"), content)
                )

        return results

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_template_context(
        self,
        op: dict,
        base_package: str,
        pascal_name: str,
        camel_name: str,
        assistant_map: dict[str, dict],
    ) -> dict:
        """Build the Jinja2 template context for a single standalone operation."""
        enabled_actions: list[str] = op.get("enabledActions", [])
        provider_name: str = op.get("providerName", "")
        base_path: str = op.get("basePath", "")
        system_prompt: str = op.get("systemPrompt", "")
        role_prompt_sequence: list[dict] | None = op.get("rolePromptSequence")
        assistant_name: str | None = op.get("assistantName")
        chat_options: dict | None = op.get("chatOptions")
        state_table: dict | None = op.get("stateTable")
        evaluator_names: list[str] = op.get("evaluatorNames", [])
        response_type: dict | None = op.get("responseType")
        rag_source_names: list[str] = op.get("ragSourceNames", [])

        # Req 6.8: Resolve assistant configuration if referenced
        assistant_config: dict | None = None
        if assistant_name and assistant_name in assistant_map:
            assistant_config = assistant_map[assistant_name]

        return {
            "base_package": base_package,
            "operation_name": pascal_name,
            "operation_name_camel": camel_name,
            "operation_raw_name": op.get("name", ""),
            "provider_name": provider_name,
            "base_path": base_path,
            "system_prompt": system_prompt,
            "enabled_actions": enabled_actions,
            "has_chat": "chat" in enabled_actions,
            "has_chat_stream": "chatStream" in enabled_actions,
            "has_generate": "generate" in enabled_actions,
            "has_query": "query" in enabled_actions,
            "role_prompt_sequence": role_prompt_sequence,
            "assistant_name": assistant_name,
            "assistant_config": assistant_config,
            "chat_options": chat_options,
            "state_table": state_table,
            "evaluator_names": evaluator_names,
            "response_type": response_type,
            "rag_source_names": rag_source_names,
        }

    def _build_state_context(
        self,
        state_table: dict,
        base_package: str,
        pascal_name: str,
        raw_name: str,
    ) -> dict:
        """Build the Jinja2 template context for a stateTable entity/repository."""
        table_name: str = state_table.get("tableName", "")
        columns: list[dict] = state_table.get("columns", [])

        mapped_columns = []
        for col in columns:
            col_name: str = col.get("name", "")
            col_type: str = col.get("type", "VARCHAR")
            java_type = _SQL_TO_JAVA_TYPE.get(col_type, "String")
            java_field = self._to_camel_case(col_name)
            mapped_columns.append({
                "name": col_name,
                "type": col_type,
                "java_type": java_type,
                "java_field": java_field,
                "nullable": col.get("nullable", True),
                "length": col.get("length"),
                "defaultValue": col.get("defaultValue"),
            })

        return {
            "base_package": base_package,
            "operation_name": pascal_name,
            "operation_raw_name": raw_name,
            "table_name": table_name,
            "columns": mapped_columns,
        }

    def _render_service(self, ctx: dict) -> str:
        """Render the standalone AI service template.

        Req 6.1: Named ``<OperationName>AiService`` in ``<basePackage>.ai.service``.
        Req 6.2: ``chat`` when chat in enabledActions.
        Req 6.3: ``chatStream`` when chatStream in enabledActions.
        Req 6.4: ``generate`` when generate in enabledActions.
        Req 6.5: ``query`` when query in enabledActions.
        Req 6.6: Injects ChatClient via @Qualifier, no entity service.
        Req 6.8: Uses assistant config when assistantName referenced.
        """
        template = self.jinja_env.get_template(
            "ai/service/standalone_ai_service.java.j2"
        )
        return template.render(**ctx)

    def _render_controller(self, ctx: dict) -> str:
        """Render the standalone AI controller template.

        Req 6.1: Named ``<OperationName>AiController`` in ``<basePackage>.ai.controller``
                 with base path ``/api/ai/<basePath>``.
        Req 6.9: GET /sessions listing user's chat sessions.
        Req 6.10: JWT authentication and rate limiting.
        """
        template = self.jinja_env.get_template(
            "ai/controller/standalone_ai_controller.java.j2"
        )
        return template.render(**ctx)

    def _render_state_entity(self, ctx: dict) -> str:
        """Render the standalone state entity template.

        Req 6.7: R2DBC entity class for the stateTable.
        """
        template = self.jinja_env.get_template(
            "ai/entity/standalone_state_entity.java.j2"
        )
        return template.render(**ctx)

    def _render_state_repository(self, ctx: dict) -> str:
        """Render the standalone state repository template.

        Req 6.7: Repository for the stateTable entity.
        """
        template = self.jinja_env.get_template(
            "ai/repository/standalone_state_repository.java.j2"
        )
        return template.render(**ctx)

    @staticmethod
    def _build_assistant_map(assistants: list[dict] | None) -> dict[str, dict]:
        """Build a mapping from assistant name → assistant config dict."""
        if not assistants:
            return {}
        return {
            a["name"]: a
            for a in assistants
            if "name" in a
        }

    @staticmethod
    def _to_pascal_case(name: str) -> str:
        """Convert an operation name to PascalCase.

        Handles names that are already PascalCase, camelCase, or snake_case.
        Examples: ``"codeHelper"`` → ``"CodeHelper"``,
                  ``"code_helper"`` → ``"CodeHelper"``.
        """
        if "_" in name:
            return "".join(word.capitalize() for word in name.split("_"))
        # camelCase or PascalCase — ensure first letter is upper
        return name[0].upper() + name[1:] if name else ""

    @staticmethod
    def _to_camel_case(name: str) -> str:
        """Convert a snake_case column name to camelCase.

        Examples: ``"user_id"`` → ``"userId"``,
                  ``"created_at"`` → ``"createdAt"``.
        """
        if "_" not in name:
            return name
        parts = name.split("_")
        return parts[0] + "".join(word.capitalize() for word in parts[1:])
