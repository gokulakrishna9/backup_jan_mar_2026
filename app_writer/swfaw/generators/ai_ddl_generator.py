"""DDL sub-generator for the AI Layer.

Generates conditional MySQL CREATE TABLE statements for all AI-related
tables based on which features are enabled in the AI_Layer definition.

Tables generated (conditionally):
- ai_chat_session / ai_chat_message: when chat operations exist
- ai_document_chunk: when any RAG source is enabled
- ai_evaluation_result: when any evaluator is configured
- ai_ingested_document: when documentIngestion is enabled
- ai_document_task_result: when documentProcessing is enabled
- ai_token_usage: when tokenBudget is enabled
- ai_audit_log: when auditLog is enabled
- ai_topic / ai_user_topic_hit / ai_global_topic_hit: when
  chatSessionCleanup with topicSummarization is enabled
- Standalone state tables: for each standaloneOperation with stateTable

Requirements: 4.18, 8.20, 11.10, 11.22, 15.24, 15.37, 16.1–16.8
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2

# SQL type mapping for stateTable columns (mirrors ai_standalone_generator)
_SQL_TYPE_MAP: dict[str, str] = {
    "VARCHAR": "VARCHAR",
    "TEXT": "TEXT",
    "INT": "INT",
    "BIGINT": "BIGINT",
    "BOOLEAN": "TINYINT(1)",
    "DATETIME": "DATETIME",
    "JSON": "JSON",
    "DOUBLE": "DOUBLE",
}


class AiDdlGenerator:
    """Generates conditional DDL SQL for AI tables.

    Follows the same sub-generator pattern as other AI sub-generators:
    receives the full AI_Layer definition, inspects which features are
    enabled, loads and renders a Jinja2 template, and returns a list
    of ``(filepath, content)`` tuples.
    """

    def __init__(self, jinja_env: "jinja2.Environment"):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        ai_layer: dict | None,
        output_path: str = "ai_tables.sql",
    ) -> list[tuple[str, str]]:
        """Generate AI DDL SQL file.

        Returns a list of ``(filepath, content)`` tuples.  When no AI
        features require tables, an empty list is returned.
        """
        if not ai_layer:
            return []

        ctx = self._build_context(ai_layer)

        # If nothing needs a table, skip generation entirely
        if not ctx["has_any_table"]:
            return []

        content = self._render("ddl/ai_tables.sql.j2", ctx)
        return [(output_path, content)]

    # ------------------------------------------------------------------
    # Feature detection helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _has_chat_operations(ai_layer: dict) -> bool:
        """Req 16.1: chat tables when any chat/chatStream operation exists."""
        for cap in ai_layer.get("entityCapabilities", []):
            ops = cap.get("enabledOperations", [])
            if "chat" in ops or "chatStream" in ops:
                return True
        for op in ai_layer.get("standaloneOperations", []):
            actions = op.get("enabledActions", [])
            if "chat" in actions or "chatStream" in actions:
                return True
        return False

    @staticmethod
    def _has_enabled_rag_sources(ai_layer: dict) -> bool:
        """Req 16.4: document chunk table when any RAG source is enabled."""
        for src in ai_layer.get("ragSources", []):
            if src.get("enabled", False):
                return True
        return False

    @staticmethod
    def _has_evaluators(ai_layer: dict) -> bool:
        """Req 16.6: evaluation result table when evaluators configured."""
        return len(ai_layer.get("evaluators", [])) > 0

    @staticmethod
    def _has_document_ingestion(ai_layer: dict) -> bool:
        """Req 11.10: ingested document table when ingestion enabled."""
        ingestion = ai_layer.get("documentIngestion")
        return bool(ingestion and ingestion.get("enabled", False))

    @staticmethod
    def _has_document_processing(ai_layer: dict) -> bool:
        """Req 11.22: document task result table when processing enabled."""
        processing = ai_layer.get("documentProcessing")
        return bool(processing and processing.get("enabled", False))

    @staticmethod
    def _has_token_budget(ai_layer: dict) -> bool:
        """Req 15.24: token usage table when tokenBudget enabled."""
        budget = ai_layer.get("tokenBudget")
        return bool(budget and budget.get("enabled", False))

    @staticmethod
    def _has_audit_log(ai_layer: dict) -> bool:
        """Req 15.37: audit log table when auditLog enabled."""
        audit = ai_layer.get("auditLog")
        return bool(audit and audit.get("enabled", False))

    @staticmethod
    def _has_topic_tables(ai_layer: dict) -> bool:
        """Req 4.18: topic tables when chatSessionCleanup with topicSummarization."""
        cleanup = ai_layer.get("chatSessionCleanup")
        if not cleanup or not cleanup.get("enabled", False):
            return False
        topic = cleanup.get("topicSummarization") or {}
        return topic.get("enabled", False)

    @staticmethod
    def _get_state_tables(ai_layer: dict) -> list[dict]:
        """Req 16.3: standalone state tables for operations with stateTable."""
        tables: list[dict] = []
        for op in ai_layer.get("standaloneOperations", []):
            st = op.get("stateTable")
            if st:
                table_name = st.get("tableName", "")
                columns = st.get("columns", [])
                mapped_cols = []
                for col in columns:
                    col_name = col.get("name", "")
                    col_type = col.get("type", "VARCHAR")
                    sql_type = _SQL_TYPE_MAP.get(col_type, "VARCHAR(255)")
                    length = col.get("length")
                    nullable = col.get("nullable", True)
                    default_value = col.get("defaultValue")

                    # Build full SQL type string
                    if col_type == "VARCHAR":
                        full_type = f"VARCHAR({length})" if length else "VARCHAR(255)"
                    else:
                        full_type = sql_type

                    mapped_cols.append({
                        "name": col_name,
                        "full_type": full_type,
                        "nullable": nullable,
                        "default_value": default_value,
                    })

                tables.append({
                    "table_name": table_name,
                    "columns": mapped_cols,
                })
        return tables

    # ------------------------------------------------------------------
    # Context builder
    # ------------------------------------------------------------------

    def _build_context(self, ai_layer: dict) -> dict:
        """Build the Jinja2 template context from the AI_Layer definition."""
        chat = self._has_chat_operations(ai_layer)
        rag = self._has_enabled_rag_sources(ai_layer)
        evaluators = self._has_evaluators(ai_layer)
        ingestion = self._has_document_ingestion(ai_layer)
        processing = self._has_document_processing(ai_layer)
        budget = self._has_token_budget(ai_layer)
        audit = self._has_audit_log(ai_layer)
        topics = self._has_topic_tables(ai_layer)
        state_tables = self._get_state_tables(ai_layer)

        has_any = (
            chat or rag or evaluators or ingestion or processing
            or budget or audit or topics or len(state_tables) > 0
        )

        return {
            "has_any_table": has_any,
            "has_chat": chat,
            "has_rag": rag,
            "has_evaluators": evaluators,
            "has_ingestion": ingestion,
            "has_processing": processing,
            "has_token_budget": budget,
            "has_audit_log": audit,
            "has_topics": topics,
            "state_tables": state_tables,
        }

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _render(self, template_name: str, ctx: dict) -> str:
        """Render a Jinja2 template under the ai/ prefix."""
        template = self.jinja_env.get_template(f"ai/{template_name}")
        return template.render(**ctx)
