"""Unit tests for the AI ObservabilityGenerator.

Verifies that the ObservabilityGenerator produces correct Java source files
for AiMetricsService, AiHealthIndicator, AiObservabilityConfig,
AiObservabilityController, and GrafanaDashboardProvisioningService.

Requirements: 15.1–15.16
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_observability_generator import (
    ObservabilityGenerator,
    VALID_PANEL_TYPES,
    DEFAULT_PROMETHEUS_ENDPOINT,
    DEFAULT_SCRAPE_INTERVAL,
    DEFAULT_GRAFANA_ORG_ID,
    DEFAULT_PANEL_SPAN,
    DEFAULT_LAYOUT_COLUMNS_PER_ROW,
)


@pytest.fixture
def jinja_env():
    """Create a Jinja2 environment pointing at the swfaw/templates directory."""
    templates_dir = Path(__file__).resolve().parent.parent / "templates"
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(templates_dir)),
        keep_trailing_newline=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )


@pytest.fixture
def generator(jinja_env):
    return ObservabilityGenerator(jinja_env)


@pytest.fixture
def output_dirs():
    return {
        "observability": Path("com/example/app/ai/observability"),
        "controller": Path("com/example/app/ai/controller"),
        "config": Path("com/example/app/ai/config"),
    }


# --- Observability fixtures ---

@pytest.fixture
def obs_disabled():
    """Observability with enabled=false."""
    return {"enabled": False}


@pytest.fixture
def obs_none():
    """Observability is None."""
    return None


@pytest.fixture
def obs_minimal():
    """Observability enabled with no prometheus/grafana/dashboards."""
    return {"enabled": True}


@pytest.fixture
def obs_with_prometheus():
    """Observability enabled with prometheus config."""
    return {
        "enabled": True,
        "prometheus": {
            "endpointPath": "/metrics/prometheus",
            "scrapeIntervalHint": "30s",
        },
    }


@pytest.fixture
def obs_with_grafana_no_dashboards():
    """Observability enabled with grafana but no dashboards."""
    return {
        "enabled": True,
        "grafana": {
            "url": "http://grafana:3000",
            "apiKeyEnvVar": "GRAFANA_API_KEY",
            "orgId": 2,
        },
        "dashboards": [],
    }


@pytest.fixture
def obs_with_grafana_and_dashboards():
    """Observability enabled with grafana and dashboards."""
    return {
        "enabled": True,
        "grafana": {
            "url": "http://grafana:3000",
            "apiKeyEnvVar": "GRAFANA_API_KEY",
            "orgId": 3,
        },
        "dashboards": [
            {
                "name": "AI Operations",
                "panels": [
                    {
                        "title": "Request Count",
                        "metricName": "ai.operations.count",
                        "type": "graph",
                        "span": 12,
                    },
                    {
                        "title": "Error Rate",
                        "metricName": "ai.operations.errors",
                        "type": "stat",
                        "span": 6,
                    },
                ],
                "layout": {"rows": 2, "columnsPerRow": 2},
            },
        ],
    }


@pytest.fixture
def obs_full():
    """Full observability config with prometheus, grafana, and dashboards."""
    return {
        "enabled": True,
        "prometheus": {
            "endpointPath": "/actuator/prometheus",
            "scrapeIntervalHint": "15s",
        },
        "grafana": {
            "url": "http://grafana:3000",
            "apiKeyEnvVar": "GRAFANA_KEY",
            "orgId": 1,
        },
        "dashboards": [
            {
                "name": "AI Overview",
                "panels": [
                    {
                        "title": "Latency P99",
                        "metricName": "ai.operations.latency",
                        "type": "gauge",
                        "span": 8,
                    },
                ],
                "layout": {"columnsPerRow": 3},
            },
            {
                "name": "Token Usage",
                "panels": [
                    {
                        "title": "Prompt Tokens",
                        "metricName": "ai.tokens.prompt",
                        "type": "table",
                        "span": 24,
                    },
                ],
            },
        ],
    }


# =====================================================================
# Test: generate() conditional generation
# =====================================================================


class TestObservabilityGeneratorGenerate:
    """Tests for the generate() method's conditional file generation."""

    def test_no_files_when_observability_is_none(self, generator, output_dirs):
        """Req 15.12: No files when observability is None."""
        assert generator.generate(None, "com.example.app", output_dirs) == []

    def test_no_files_when_observability_disabled(self, generator, obs_disabled, output_dirs):
        """Req 15.12: No files when enabled=false."""
        assert generator.generate(obs_disabled, "com.example.app", output_dirs) == []

    def test_no_files_when_empty_dict(self, generator, output_dirs):
        """Req 15.12: No files when observability is empty dict (enabled defaults false)."""
        assert generator.generate({}, "com.example.app", output_dirs) == []

    def test_minimal_generates_4_files(self, generator, obs_minimal, output_dirs):
        """Minimal enabled config generates 4 core files (no Grafana service)."""
        results = generator.generate(obs_minimal, "com.example.app", output_dirs)
        assert len(results) == 4

    def test_with_prometheus_generates_4_files(self, generator, obs_with_prometheus, output_dirs):
        """Prometheus config without grafana/dashboards still generates 4 core files."""
        results = generator.generate(obs_with_prometheus, "com.example.app", output_dirs)
        assert len(results) == 4

    def test_grafana_no_dashboards_generates_4_files(
        self, generator, obs_with_grafana_no_dashboards, output_dirs
    ):
        """Grafana without dashboards generates 4 core files (no provisioning service)."""
        results = generator.generate(obs_with_grafana_no_dashboards, "com.example.app", output_dirs)
        assert len(results) == 4

    def test_grafana_with_dashboards_generates_5_files(
        self, generator, obs_with_grafana_and_dashboards, output_dirs
    ):
        """Grafana with dashboards generates 5 files (includes provisioning service)."""
        results = generator.generate(obs_with_grafana_and_dashboards, "com.example.app", output_dirs)
        assert len(results) == 5

    def test_full_config_generates_5_files(self, generator, obs_full, output_dirs):
        """Full config generates 5 files."""
        results = generator.generate(obs_full, "com.example.app", output_dirs)
        assert len(results) == 5

    def test_all_content_is_nonempty(self, generator, obs_full, output_dirs):
        """All generated content strings are non-empty."""
        results = generator.generate(obs_full, "com.example.app", output_dirs)
        for filepath, content in results:
            assert content.strip(), f"Empty content for {filepath}"

    def test_output_dirs_used_in_paths(self, generator, obs_full, output_dirs):
        """Output directory paths are used in generated file paths."""
        results = generator.generate(obs_full, "com.example.app", output_dirs)
        paths = [fp for fp, _ in results]
        assert any("com/example/app/ai/observability" in p for p in paths)
        assert any("com/example/app/ai/controller" in p for p in paths)
        assert any("com/example/app/ai/config" in p for p in paths)

    def test_correct_filenames(self, generator, obs_full, output_dirs):
        """Correct Java filenames are generated."""
        results = generator.generate(obs_full, "com.example.app", output_dirs)
        filenames = [Path(fp).name for fp, _ in results]
        assert "AiMetricsService.java" in filenames
        assert "AiHealthIndicator.java" in filenames
        assert "AiObservabilityConfig.java" in filenames
        assert "AiObservabilityController.java" in filenames
        assert "GrafanaDashboardProvisioningService.java" in filenames


# =====================================================================
# Test: AiMetricsService template output
# =====================================================================


class TestAiMetricsService:
    """Tests for the AiMetricsService generated Java class."""

    def _get_service(self, generator, observability, output_dirs):
        results = generator.generate(observability, "com.example.app", output_dirs)
        for fp, content in results:
            if "AiMetricsService.java" in fp:
                return content
        pytest.fail("AiMetricsService.java not found in results")

    def test_package_declaration(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "package com.example.app.ai.observability;" in content

    def test_service_annotation(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "@Service" in content

    def test_class_name(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "public class AiMetricsService" in content

    def test_meter_registry_injection(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "MeterRegistry" in content

    def test_record_operation_count_method(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "recordOperationCount" in content

    def test_operation_count_metric_name(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "ai.operations.count" in content

    def test_start_timer_method(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "startTimer" in content

    def test_record_operation_latency_method(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "recordOperationLatency" in content

    def test_latency_percentiles(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "publishPercentiles" in content

    def test_record_prompt_tokens_method(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "recordPromptTokens" in content

    def test_record_completion_tokens_method(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "recordCompletionTokens" in content

    def test_record_error_method(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "recordError" in content

    def test_active_session_gauge(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "ai.sessions.active" in content

    def test_rag_retrieval_latency(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "ai.rag.retrieval.latency" in content

    def test_evaluator_pass_rate(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "ai.evaluator.pass_rate" in content

    def test_document_ingestion_throughput(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "ai.documents.ingestion.throughput" in content

    def test_document_processing_throughput(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "ai.documents.processing.throughput" in content

    def test_moderation_flags(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "ai.moderation.flags" in content

    def test_mcp_invocations(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "ai.mcp.invocations" in content

    def test_timer_sample_import(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "import io.micrometer.core.instrument.Timer;" in content

    def test_counter_import(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "import io.micrometer.core.instrument.Counter;" in content

    def test_gauge_import(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "import io.micrometer.core.instrument.Gauge;" in content

    def test_logging(self, generator, obs_minimal, output_dirs):
        content = self._get_service(generator, obs_minimal, output_dirs)
        assert "@Slf4j" in content


# =====================================================================
# Test: AiHealthIndicator template output
# =====================================================================


class TestAiHealthIndicator:
    """Tests for the AiHealthIndicator generated Java class."""

    def _get_indicator(self, generator, observability, output_dirs):
        results = generator.generate(observability, "com.example.app", output_dirs)
        for fp, content in results:
            if "AiHealthIndicator.java" in fp:
                return content
        pytest.fail("AiHealthIndicator.java not found in results")

    def test_package_declaration(self, generator, obs_minimal, output_dirs):
        content = self._get_indicator(generator, obs_minimal, output_dirs)
        assert "package com.example.app.ai.observability;" in content

    def test_component_annotation(self, generator, obs_minimal, output_dirs):
        content = self._get_indicator(generator, obs_minimal, output_dirs)
        assert "@Component" in content

    def test_class_name(self, generator, obs_minimal, output_dirs):
        content = self._get_indicator(generator, obs_minimal, output_dirs)
        assert "public class AiHealthIndicator" in content

    def test_implements_reactive_health_indicator(self, generator, obs_minimal, output_dirs):
        content = self._get_indicator(generator, obs_minimal, output_dirs)
        assert "implements ReactiveHealthIndicator" in content

    def test_health_method(self, generator, obs_minimal, output_dirs):
        content = self._get_indicator(generator, obs_minimal, output_dirs)
        assert "public Mono<Health> health()" in content

    def test_health_up(self, generator, obs_minimal, output_dirs):
        content = self._get_indicator(generator, obs_minimal, output_dirs)
        assert "Health.up()" in content

    def test_health_down_on_error(self, generator, obs_minimal, output_dirs):
        content = self._get_indicator(generator, obs_minimal, output_dirs)
        assert "Health.down()" in content

    def test_reactive_imports(self, generator, obs_minimal, output_dirs):
        content = self._get_indicator(generator, obs_minimal, output_dirs)
        assert "import reactor.core.publisher.Mono;" in content

    def test_actuator_import(self, generator, obs_minimal, output_dirs):
        content = self._get_indicator(generator, obs_minimal, output_dirs)
        assert "import org.springframework.boot.actuate.health.ReactiveHealthIndicator;" in content


# =====================================================================
# Test: AiObservabilityConfig template output
# =====================================================================


class TestAiObservabilityConfig:
    """Tests for the AiObservabilityConfig generated Java class."""

    def _get_config(self, generator, observability, output_dirs):
        results = generator.generate(observability, "com.example.app", output_dirs)
        for fp, content in results:
            if "AiObservabilityConfig.java" in fp:
                return content
        pytest.fail("AiObservabilityConfig.java not found in results")

    def test_package_declaration(self, generator, obs_minimal, output_dirs):
        content = self._get_config(generator, obs_minimal, output_dirs)
        assert "package com.example.app.ai.config;" in content

    def test_configuration_annotation(self, generator, obs_minimal, output_dirs):
        content = self._get_config(generator, obs_minimal, output_dirs)
        assert "@Configuration" in content

    def test_conditional_on_property(self, generator, obs_minimal, output_dirs):
        content = self._get_config(generator, obs_minimal, output_dirs)
        assert '@ConditionalOnProperty(name = "ai.observability.enabled", havingValue = "true")' in content

    def test_class_name(self, generator, obs_minimal, output_dirs):
        content = self._get_config(generator, obs_minimal, output_dirs)
        assert "public class AiObservabilityConfig" in content

    def test_metrics_service_bean(self, generator, obs_minimal, output_dirs):
        content = self._get_config(generator, obs_minimal, output_dirs)
        assert "aiMetricsService" in content

    def test_health_indicator_bean(self, generator, obs_minimal, output_dirs):
        content = self._get_config(generator, obs_minimal, output_dirs)
        assert "aiHealthIndicator" in content

    def test_no_grafana_bean_without_grafana(self, generator, obs_minimal, output_dirs):
        content = self._get_config(generator, obs_minimal, output_dirs)
        assert "grafanaDashboardProvisioningService" not in content

    def test_grafana_bean_with_grafana(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_config(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "GrafanaDashboardProvisioningService" in content
        assert "grafanaDashboardProvisioningService" in content


# =====================================================================
# Test: AiObservabilityController template output
# =====================================================================


class TestAiObservabilityController:
    """Tests for the AiObservabilityController generated Java class."""

    def _get_controller(self, generator, observability, output_dirs):
        results = generator.generate(observability, "com.example.app", output_dirs)
        for fp, content in results:
            if "AiObservabilityController.java" in fp:
                return content
        pytest.fail("AiObservabilityController.java not found in results")

    def test_package_declaration(self, generator, obs_minimal, output_dirs):
        content = self._get_controller(generator, obs_minimal, output_dirs)
        assert "package com.example.app.ai.controller;" in content

    def test_rest_controller_annotation(self, generator, obs_minimal, output_dirs):
        content = self._get_controller(generator, obs_minimal, output_dirs)
        assert "@RestController" in content

    def test_request_mapping(self, generator, obs_minimal, output_dirs):
        content = self._get_controller(generator, obs_minimal, output_dirs)
        assert '@RequestMapping("/api/ai/observability")' in content

    def test_class_name(self, generator, obs_minimal, output_dirs):
        content = self._get_controller(generator, obs_minimal, output_dirs)
        assert "public class AiObservabilityController" in content

    def test_metrics_summary_endpoint(self, generator, obs_minimal, output_dirs):
        content = self._get_controller(generator, obs_minimal, output_dirs)
        assert '@GetMapping("/metrics/summary")' in content

    def test_health_endpoint(self, generator, obs_minimal, output_dirs):
        content = self._get_controller(generator, obs_minimal, output_dirs)
        assert '@GetMapping("/health")' in content

    def test_admin_role_required(self, generator, obs_minimal, output_dirs):
        content = self._get_controller(generator, obs_minimal, output_dirs)
        assert "@PreAuthorize" in content
        assert "ADMIN" in content

    def test_no_provision_endpoint_without_grafana(self, generator, obs_minimal, output_dirs):
        content = self._get_controller(generator, obs_minimal, output_dirs)
        assert '@PostMapping("/dashboards/provision")' not in content

    def test_provision_endpoint_with_grafana(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_controller(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert '@PostMapping("/dashboards/provision")' in content

    def test_reactive_imports(self, generator, obs_minimal, output_dirs):
        content = self._get_controller(generator, obs_minimal, output_dirs)
        assert "import reactor.core.publisher.Mono;" in content


# =====================================================================
# Test: GrafanaDashboardProvisioningService template output
# =====================================================================


class TestGrafanaDashboardProvisioningService:
    """Tests for the GrafanaDashboardProvisioningService generated Java class."""

    def _get_service(self, generator, observability, output_dirs):
        results = generator.generate(observability, "com.example.app", output_dirs)
        for fp, content in results:
            if "GrafanaDashboardProvisioningService.java" in fp:
                return content
        pytest.fail("GrafanaDashboardProvisioningService.java not found in results")

    def test_package_declaration(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "package com.example.app.ai.observability;" in content

    def test_service_annotation(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "@Service" in content

    def test_class_name(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "public class GrafanaDashboardProvisioningService" in content

    def test_grafana_url(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "http://grafana:3000" in content

    def test_api_key_env_var(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "GRAFANA_API_KEY" in content

    def test_org_id(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "ORG_ID = 3" in content

    def test_application_ready_event_listener(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "@EventListener(ApplicationReadyEvent.class)" in content

    def test_provision_all_dashboards_method(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "provisionAllDashboards" in content

    def test_overwrite_true(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert 'overwrite' in content

    def test_dashboard_name_in_payload(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "AI Operations" in content

    def test_panel_metric_names(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "ai.operations.count" in content
        assert "ai.operations.errors" in content

    def test_panel_titles(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "Request Count" in content
        assert "Error Rate" in content

    def test_webclient_usage(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "WebClient" in content

    def test_api_dashboards_db_endpoint(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "/api/dashboards/db" in content

    def test_error_handling_continues(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "onErrorResume" in content

    def test_reactive_imports(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "import reactor.core.publisher.Mono;" in content
        assert "import reactor.core.publisher.Flux;" in content

    def test_map_panel_type_method(self, generator, obs_with_grafana_and_dashboards, output_dirs):
        content = self._get_service(generator, obs_with_grafana_and_dashboards, output_dirs)
        assert "mapPanelType" in content

    def test_multiple_dashboards(self, generator, obs_full, output_dirs):
        """Full config with 2 dashboards generates both dashboard names."""
        content = self._get_service(generator, obs_full, output_dirs)
        assert "AI Overview" in content
        assert "Token Usage" in content


# =====================================================================
# Test: Context builders
# =====================================================================


class TestBuildPrometheusContext:
    """Tests for _build_prometheus_context."""

    def test_defaults(self, generator):
        ctx = generator._build_prometheus_context({"enabled": True})
        assert ctx["prometheus_endpoint"] == DEFAULT_PROMETHEUS_ENDPOINT
        assert ctx["scrape_interval_hint"] == DEFAULT_SCRAPE_INTERVAL

    def test_custom_values(self, generator):
        obs = {
            "enabled": True,
            "prometheus": {
                "endpointPath": "/custom/metrics",
                "scrapeIntervalHint": "60s",
            },
        }
        ctx = generator._build_prometheus_context(obs)
        assert ctx["prometheus_endpoint"] == "/custom/metrics"
        assert ctx["scrape_interval_hint"] == "60s"


class TestBuildGrafanaContext:
    """Tests for _build_grafana_context."""

    def test_defaults_when_no_grafana(self, generator):
        ctx = generator._build_grafana_context({"enabled": True})
        assert ctx["grafana_url"] == ""
        assert ctx["grafana_api_key_env_var"] == ""
        assert ctx["grafana_org_id"] == DEFAULT_GRAFANA_ORG_ID

    def test_custom_values(self, generator):
        obs = {
            "enabled": True,
            "grafana": {
                "url": "http://grafana:3000",
                "apiKeyEnvVar": "MY_KEY",
                "orgId": 5,
            },
        }
        ctx = generator._build_grafana_context(obs)
        assert ctx["grafana_url"] == "http://grafana:3000"
        assert ctx["grafana_api_key_env_var"] == "MY_KEY"
        assert ctx["grafana_org_id"] == 5


class TestBuildDashboardContext:
    """Tests for _build_dashboard_context."""

    def test_dashboard_name(self, generator):
        grafana = {"url": "http://g:3000", "apiKeyEnvVar": "K", "orgId": 1}
        dashboards = [{"name": "Test", "panels": [], "layout": {}}]
        ctx = generator._build_dashboard_context(grafana, dashboards, "com.example")
        assert ctx["dashboards"][0]["name"] == "Test"

    def test_panel_processing(self, generator):
        grafana = {"url": "http://g:3000", "apiKeyEnvVar": "K", "orgId": 1}
        dashboards = [{
            "name": "D1",
            "panels": [
                {"title": "P1", "metricName": "m1", "type": "graph", "span": 12},
            ],
            "layout": {"columnsPerRow": 3},
        }]
        ctx = generator._build_dashboard_context(grafana, dashboards, "com.example")
        panel = ctx["dashboards"][0]["panels"][0]
        assert panel["title"] == "P1"
        assert panel["metric_name"] == "m1"
        assert panel["type"] == "graph"
        assert panel["span"] == 12

    def test_default_panel_span(self, generator):
        grafana = {"url": "http://g:3000", "apiKeyEnvVar": "K", "orgId": 1}
        dashboards = [{"name": "D1", "panels": [{"title": "P1", "metricName": "m1"}]}]
        ctx = generator._build_dashboard_context(grafana, dashboards, "com.example")
        assert ctx["dashboards"][0]["panels"][0]["span"] == DEFAULT_PANEL_SPAN

    def test_default_columns_per_row(self, generator):
        grafana = {"url": "http://g:3000", "apiKeyEnvVar": "K", "orgId": 1}
        dashboards = [{"name": "D1", "panels": []}]
        ctx = generator._build_dashboard_context(grafana, dashboards, "com.example")
        assert ctx["dashboards"][0]["columns_per_row"] == DEFAULT_LAYOUT_COLUMNS_PER_ROW

    def test_grafana_context_fields(self, generator):
        grafana = {"url": "http://g:3000", "apiKeyEnvVar": "K", "orgId": 7}
        ctx = generator._build_dashboard_context(grafana, [], "com.example")
        assert ctx["grafana_url"] == "http://g:3000"
        assert ctx["grafana_api_key_env_var"] == "K"
        assert ctx["grafana_org_id"] == 7
        assert ctx["base_package"] == "com.example"


# =====================================================================
# Test: Module constants
# =====================================================================


class TestModuleConstants:
    """Tests for module-level constants."""

    def test_valid_panel_types(self):
        assert VALID_PANEL_TYPES == {"graph", "stat", "gauge", "table"}

    def test_default_prometheus_endpoint(self):
        assert DEFAULT_PROMETHEUS_ENDPOINT == "/actuator/prometheus"

    def test_default_scrape_interval(self):
        assert DEFAULT_SCRAPE_INTERVAL == "15s"

    def test_default_grafana_org_id(self):
        assert DEFAULT_GRAFANA_ORG_ID == 1

    def test_default_panel_span(self):
        assert DEFAULT_PANEL_SPAN == 12

    def test_default_layout_columns_per_row(self):
        assert DEFAULT_LAYOUT_COLUMNS_PER_ROW == 2
