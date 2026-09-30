"""Application properties sub-generator for the AI Layer.

Generates Spring Boot ``application.properties`` entries for all AI
configuration sections based on the AI_Layer definition.

Sections generated (conditionally):
- ai.providers.<name>.*: per-provider config (model, baseUrl, apiKey,
  temperature, maxTokens, chatOptions, supportedParameters,
  parameterFallbacks, supportedRoles, roleFallbacks, resilience)
- ai.chat-session-cleanup.*: when chatSessionCleanup enabled
- ai.vector-store.*: when vectorStore configured
- ai.observability.*: when observability enabled
- ai.token-budget.*: when tokenBudget enabled
- ai.audit-log.*: when auditLog enabled

Requirements: 2.4, 2.29, 4.22, 8.9, 15.11, 15.28, 15.42
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2


class AiAppPropertiesGenerator:
    """Generates application.properties entries from the AI_Layer definition.

    Follows the same sub-generator pattern as other AI sub-generators:
    receives the full AI_Layer definition, inspects which features are
    configured, and returns a list of ``(filepath, content)`` tuples
    containing the properties text.
    """

    def __init__(self, jinja_env: "jinja2.Environment" | None = None):
        self.jinja_env = jinja_env

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        ai_layer: dict | None,
        output_path: str = "ai-application.properties",
    ) -> list[tuple[str, str]]:
        """Generate AI application.properties file.

        Returns a list of ``(filepath, content)`` tuples.  When no AI
        layer is configured, an empty list is returned.
        """
        if ai_layer is None:
            return []

        lines: list[str] = []
        lines.append("# ============================================")
        lines.append("# AI Layer Configuration (auto-generated)")
        lines.append("# ============================================")
        lines.append("")

        self._emit_provider_properties(ai_layer, lines)
        self._emit_chat_session_cleanup_properties(ai_layer, lines)
        self._emit_vector_store_properties(ai_layer, lines)
        self._emit_observability_properties(ai_layer, lines)
        self._emit_token_budget_properties(ai_layer, lines)
        self._emit_audit_log_properties(ai_layer, lines)

        # Strip trailing blank lines, ensure final newline
        while lines and lines[-1] == "":
            lines.pop()
        content = "\n".join(lines) + "\n"

        return [(output_path, content)]

    # ------------------------------------------------------------------
    # Provider properties (Req 2.4, 2.29)
    # ------------------------------------------------------------------

    def _emit_provider_properties(
        self, ai_layer: dict, lines: list[str]
    ) -> None:
        """Emit ai.providers.<name>.* entries for each Named_Provider."""
        providers = ai_layer.get("providers", [])
        if not providers:
            return

        lines.append("# --- Provider Configuration (Req 2.4) ---")
        for provider in providers:
            name = provider.get("name", "")
            prefix = f"ai.providers.{name}"

            lines.append(f"{prefix}.type={provider.get('type', '')}")
            lines.append(f"{prefix}.model={provider.get('model', '')}")

            embedding_model = provider.get("embeddingModel")
            if embedding_model:
                lines.append(f"{prefix}.embedding-model={embedding_model}")

            base_url = provider.get("baseUrl")
            if base_url:
                lines.append(f"{prefix}.base-url={base_url}")

            api_key_env = provider.get("apiKeyEnvVar", "")
            lines.append(f"{prefix}.api-key-env-var={api_key_env}")

            temp = provider.get("temperature", 0.7)
            lines.append(f"{prefix}.temperature={temp}")

            max_tokens = provider.get("maxTokens", 2048)
            lines.append(f"{prefix}.max-tokens={max_tokens}")

            # Chat options
            chat_options = provider.get("chatOptions")
            if chat_options:
                for key, value in chat_options.items():
                    prop_key = self._camel_to_kebab(key)
                    lines.append(f"{prefix}.chat-options.{prop_key}={value}")

            # Supported parameters
            supported_params = provider.get("supportedParameters")
            if supported_params:
                lines.append(
                    f"{prefix}.supported-parameters="
                    + ",".join(supported_params)
                )

            # Parameter fallbacks
            param_fallbacks = provider.get("parameterFallbacks")
            if param_fallbacks:
                for param, action in param_fallbacks.items():
                    prop_key = self._camel_to_kebab(param)
                    lines.append(
                        f"{prefix}.parameter-fallbacks.{prop_key}={action}"
                    )

            # Supported roles
            supported_roles = provider.get("supportedRoles")
            if supported_roles:
                lines.append(
                    f"{prefix}.supported-roles=" + ",".join(supported_roles)
                )

            # Role fallbacks
            role_fallbacks = provider.get("roleFallbacks")
            if role_fallbacks:
                for role, action in role_fallbacks.items():
                    lines.append(
                        f"{prefix}.role-fallbacks.{role}={action}"
                    )

            # Resilience (Req 2.29)
            resilience = provider.get("resilience")
            if resilience:
                retry = resilience.get("retry", {})
                if retry:
                    rp = f"{prefix}.resilience.retry"
                    lines.append(
                        f"{rp}.max-attempts="
                        f"{retry.get('maxAttempts', 3)}"
                    )
                    lines.append(
                        f"{rp}.backoff-ms="
                        f"{retry.get('backoffMs', 1000)}"
                    )
                    statuses = retry.get("retryableStatuses", [429, 503])
                    lines.append(
                        f"{rp}.retryable-statuses="
                        + ",".join(str(s) for s in statuses)
                    )
                    lines.append(
                        f"{rp}.retry-on-timeout="
                        f"{str(retry.get('retryOnTimeout', True)).lower()}"
                    )

                cb = resilience.get("circuitBreaker", {})
                if cb:
                    cbp = f"{prefix}.resilience.circuit-breaker"
                    lines.append(
                        f"{cbp}.failure-rate-threshold="
                        f"{cb.get('failureRateThreshold', 50)}"
                    )
                    lines.append(
                        f"{cbp}.wait-duration-ms="
                        f"{cb.get('waitDurationMs', 30000)}"
                    )
                    lines.append(
                        f"{cbp}.sliding-window-size="
                        f"{cb.get('slidingWindowSize', 10)}"
                    )
                    lines.append(
                        f"{cbp}.minimum-number-of-calls="
                        f"{cb.get('minimumNumberOfCalls', 5)}"
                    )

            lines.append("")

    # ------------------------------------------------------------------
    # Chat session cleanup properties (Req 4.22)
    # ------------------------------------------------------------------

    def _emit_chat_session_cleanup_properties(
        self, ai_layer: dict, lines: list[str]
    ) -> None:
        cleanup = ai_layer.get("chatSessionCleanup")
        if not cleanup or not cleanup.get("enabled", False):
            return

        lines.append("# --- Chat Session Cleanup (Req 4.22) ---")
        prefix = "ai.chat-session-cleanup"
        lines.append(f"{prefix}.enabled=true")
        lines.append(
            f"{prefix}.default-ttl-days="
            f"{cleanup.get('defaultTtlDays', 30)}"
        )
        lines.append(
            f"{prefix}.cleanup-cron-expression="
            f"{cleanup.get('cleanupCronExpression', '0 0 2 * * *')}"
        )
        lines.append(
            f"{prefix}.batch-size={cleanup.get('batchSize', 1000)}"
        )

        topic = cleanup.get("topicSummarization")
        if topic and topic.get("enabled", False):
            tp = f"{prefix}.topic-summarization"
            lines.append(f"{tp}.enabled=true")
            provider = topic.get("providerName", "")
            lines.append(f"{tp}.provider-name={provider}")
            lines.append(
                f"{tp}.max-topics-per-session="
                f"{topic.get('maxTopicsPerSession', 5)}"
            )

        lines.append("")

    # ------------------------------------------------------------------
    # Vector store properties (Req 8.9)
    # ------------------------------------------------------------------

    def _emit_vector_store_properties(
        self, ai_layer: dict, lines: list[str]
    ) -> None:
        vs = ai_layer.get("vectorStore")
        if not vs:
            return

        lines.append("# --- Vector Store (Req 8.9) ---")
        prefix = "ai.vector-store"
        lines.append(f"{prefix}.type={vs.get('type', 'milvus')}")
        lines.append(f"{prefix}.host={vs.get('host', 'localhost')}")
        lines.append(f"{prefix}.port={vs.get('port', 19530)}")

        api_key = vs.get("apiKey")
        if api_key:
            lines.append(f"{prefix}.api-key={api_key}")

        database = vs.get("database")
        if database:
            lines.append(f"{prefix}.database={database}")

        lines.append(
            f"{prefix}.collection-prefix="
            f"{vs.get('collectionPrefix', 'ai_')}"
        )
        lines.append(
            f"{prefix}.max-connections="
            f"{vs.get('maxConnections', 10)}"
        )
        lines.append(
            f"{prefix}.connect-timeout-ms="
            f"{vs.get('connectTimeoutMs', 5000)}"
        )
        lines.append(
            f"{prefix}.idle-timeout-ms="
            f"{vs.get('idleTimeoutMs', 60000)}"
        )
        lines.append("")

    # ------------------------------------------------------------------
    # Observability properties (Req 15.11)
    # ------------------------------------------------------------------

    def _emit_observability_properties(
        self, ai_layer: dict, lines: list[str]
    ) -> None:
        obs = ai_layer.get("observability")
        if not obs or not obs.get("enabled", False):
            return

        lines.append("# --- Observability (Req 15.11) ---")
        prefix = "ai.observability"
        lines.append(f"{prefix}.enabled=true")

        prometheus = obs.get("prometheus")
        if prometheus:
            lines.append(
                f"{prefix}.prometheus.endpoint-path="
                f"{prometheus.get('endpointPath', '/actuator/prometheus')}"
            )

        grafana = obs.get("grafana")
        if grafana:
            lines.append(
                f"{prefix}.grafana.url={grafana.get('url', '')}"
            )
            lines.append(
                f"{prefix}.grafana.api-key-env-var="
                f"{grafana.get('apiKeyEnvVar', '')}"
            )
            lines.append(
                f"{prefix}.grafana.org-id={grafana.get('orgId', 1)}"
            )

        lines.append("")

    # ------------------------------------------------------------------
    # Token budget properties (Req 15.28)
    # ------------------------------------------------------------------

    def _emit_token_budget_properties(
        self, ai_layer: dict, lines: list[str]
    ) -> None:
        budget = ai_layer.get("tokenBudget")
        if not budget or not budget.get("enabled", False):
            return

        lines.append("# --- Token Budget (Req 15.28) ---")
        prefix = "ai.token-budget"
        lines.append(f"{prefix}.enabled=true")

        daily = budget.get("defaultDailyLimitPerUser")
        if daily is not None:
            lines.append(f"{prefix}.default-daily-limit-per-user={daily}")

        monthly = budget.get("defaultMonthlyLimitPerUser")
        if monthly is not None:
            lines.append(
                f"{prefix}.default-monthly-limit-per-user={monthly}"
            )

        lines.append(
            f"{prefix}.warning-threshold-percent="
            f"{budget.get('warningThresholdPercent', 80)}"
        )
        lines.append(
            f"{prefix}.enforcement-action="
            f"{budget.get('enforcementAction', 'block')}"
        )

        overrides = budget.get("providerOverrides")
        if overrides:
            for prov_name, limits in overrides.items():
                op = f"{prefix}.provider-overrides.{prov_name}"
                d = limits.get("dailyLimit")
                if d is not None:
                    lines.append(f"{op}.daily-limit={d}")
                m = limits.get("monthlyLimit")
                if m is not None:
                    lines.append(f"{op}.monthly-limit={m}")

        lines.append("")

    # ------------------------------------------------------------------
    # Audit log properties (Req 15.42)
    # ------------------------------------------------------------------

    def _emit_audit_log_properties(
        self, ai_layer: dict, lines: list[str]
    ) -> None:
        audit = ai_layer.get("auditLog")
        if not audit or not audit.get("enabled", False):
            return

        lines.append("# --- Audit Log (Req 15.42) ---")
        prefix = "ai.audit-log"
        lines.append(f"{prefix}.enabled=true")
        lines.append(
            f"{prefix}.retention-days="
            f"{audit.get('retentionDays', 90)}"
        )
        lines.append(
            f"{prefix}.cleanup-cron-expression="
            f"{audit.get('cleanupCronExpression', '0 0 3 * * *')}"
        )

        events = audit.get("loggedEvents")
        if events:
            lines.append(
                f"{prefix}.logged-events=" + ",".join(events)
            )

        lines.append("")

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    @staticmethod
    def _camel_to_kebab(name: str) -> str:
        """Convert camelCase to kebab-case for property keys."""
        result: list[str] = []
        for ch in name:
            if ch.isupper():
                if result:
                    result.append("-")
                result.append(ch.lower())
            else:
                result.append(ch)
        return "".join(result)
