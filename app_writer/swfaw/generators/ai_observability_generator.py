"""Observability sub-generator for the AI Layer.

Generates AiMetricsService, AiHealthIndicator, AiObservabilityConfig,
AiObservabilityController, and GrafanaDashboardProvisioningService.

Requirements: 15.1–15.16
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import jinja2

# Valid panel types for Grafana dashboards
VALID_PANEL_TYPES = {"graph", "stat", "gauge", "table"}

# Default Prometheus configuration
DEFAULT_PROMETHEUS_ENDPOINT = "/actuator/prometheus"
DEFAULT_SCRAPE_INTERVAL = "15s"

# Default Grafana configuration
DEFAULT_GRAFANA_ORG_ID = 1

# Default panel span
DEFAULT_PANEL_SPAN = 12

# Default layout
DEFAULT_LAYOUT_COLUMNS_PER_ROW = 2


class ObservabilityGenerator:
    """Generates observability Java files from the AI_Layer definition.

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
        observability: dict | None,
        base_package: str,
        output_dirs: dict[str, Path],
    ) -> list[tuple[str, str]]:
        """Generate observability Java files.

        Returns a list of ``(filepath, content)`` tuples where *filepath*
        is relative to the project source root.

        Req 15.12: When observability is absent or ``enabled`` is false,
        no observability files are generated.
        """
        if not observability or not observability.get("enabled", False):
            return []

        results: list[tuple[str, str]] = []

        observability_dir = output_dirs.get(
            "observability", Path("ai/observability")
        )
        controller_dir = output_dirs.get(
            "controller", Path("ai/controller")
        )
        config_dir = output_dirs.get("config", Path("ai/config"))

        # Build contexts
        prometheus_ctx = self._build_prometheus_context(observability)
        grafana_ctx = self._build_grafana_context(observability)

        # 1. AiMetricsService (Req 15.1, 15.2, 15.3, 15.14, 15.16)
        results.append((
            str(observability_dir / "AiMetricsService.java"),
            self._render(
                "observability/ai_metrics_service.java.j2",
                {"base_package": base_package},
            ),
        ))

        # 2. AiHealthIndicator (Req 15.4)
        results.append((
            str(observability_dir / "AiHealthIndicator.java"),
            self._render(
                "observability/ai_health_indicator.java.j2",
                {"base_package": base_package},
            ),
        ))

        # 3. AiObservabilityConfig (Req 15.13)
        config_ctx = {
            "base_package": base_package,
            **prometheus_ctx,
            **grafana_ctx,
            "has_grafana": grafana_ctx["grafana_url"] != "",
        }
        results.append((
            str(config_dir / "AiObservabilityConfig.java"),
            self._render(
                "config/observability_config.java.j2",
                config_ctx,
            ),
        ))

        # 4. AiObservabilityController (Req 15.15)
        results.append((
            str(controller_dir / "AiObservabilityController.java"),
            self._render(
                "controller/observability_controller.java.j2",
                {
                    "base_package": base_package,
                    "has_grafana": grafana_ctx["grafana_url"] != "",
                },
            ),
        ))

        # 5. GrafanaDashboardProvisioningService (Req 15.6–15.10)
        grafana = observability.get("grafana")
        dashboards = observability.get("dashboards", [])
        if grafana and dashboards:
            dashboard_ctx = self._build_dashboard_context(
                grafana, dashboards, base_package
            )
            results.append((
                str(observability_dir / "GrafanaDashboardProvisioningService.java"),
                self._render(
                    "observability/grafana_dashboard_provisioning_service.java.j2",
                    dashboard_ctx,
                ),
            ))

        return results

    # ------------------------------------------------------------------
    # Context builders
    # ------------------------------------------------------------------

    def _build_prometheus_context(self, observability: dict) -> dict:
        """Build context for Prometheus configuration."""
        prometheus = observability.get("prometheus", {})
        return {
            "prometheus_endpoint": prometheus.get(
                "endpointPath", DEFAULT_PROMETHEUS_ENDPOINT
            ),
            "scrape_interval_hint": prometheus.get(
                "scrapeIntervalHint", DEFAULT_SCRAPE_INTERVAL
            ),
        }

    def _build_grafana_context(self, observability: dict) -> dict:
        """Build context for Grafana configuration."""
        grafana = observability.get("grafana", {})
        return {
            "grafana_url": grafana.get("url", ""),
            "grafana_api_key_env_var": grafana.get("apiKeyEnvVar", ""),
            "grafana_org_id": grafana.get("orgId", DEFAULT_GRAFANA_ORG_ID),
        }

    def _build_dashboard_context(
        self,
        grafana: dict,
        dashboards: list[dict],
        base_package: str,
    ) -> dict:
        """Build Jinja2 context for the GrafanaDashboardProvisioningService."""
        processed_dashboards = []
        for dash in dashboards:
            layout = dash.get("layout", {})
            panels = []
            for panel in dash.get("panels", []):
                panels.append({
                    "title": panel.get("title", ""),
                    "metric_name": panel.get("metricName", ""),
                    "type": panel.get("type", "graph"),
                    "span": panel.get("span", DEFAULT_PANEL_SPAN),
                })
            processed_dashboards.append({
                "name": dash.get("name", ""),
                "panels": panels,
                "rows": layout.get("rows", 0),
                "columns_per_row": layout.get(
                    "columnsPerRow", DEFAULT_LAYOUT_COLUMNS_PER_ROW
                ),
            })

        return {
            "base_package": base_package,
            "grafana_url": grafana.get("url", ""),
            "grafana_api_key_env_var": grafana.get("apiKeyEnvVar", ""),
            "grafana_org_id": grafana.get("orgId", DEFAULT_GRAFANA_ORG_ID),
            "dashboards": processed_dashboards,
        }

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def _render(self, template_name: str, ctx: dict) -> str:
        """Render a Jinja2 template under the ai/ prefix."""
        template = self.jinja_env.get_template(f"ai/{template_name}")
        return template.render(**ctx)
