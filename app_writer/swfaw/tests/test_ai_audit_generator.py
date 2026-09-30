"""Unit tests for the AI AuditGenerator.

Verifies that the AuditGenerator produces correct Java source files
for AiAuditService, AiAuditCleanupScheduler, AiAuditController,
AiAuditLog entity/repository, and DTOs (AiAuditEventDTO, AiAuditStatsDTO,
AiAuditPageDTO).

Requirements: 15.34–15.47
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_audit_generator import (
    AuditGenerator,
    DEFAULT_RETENTION_DAYS,
    DEFAULT_CLEANUP_CRON,
    VALID_EVENT_TYPES,
    CLEANUP_BATCH_SIZE,
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
    return AuditGenerator(jinja_env)


@pytest.fixture
def output_dirs():
    return {
        "audit": Path("com/example/app/ai/audit"),
        "controller": Path("com/example/app/ai/controller"),
        "dto": Path("com/example/app/ai/dto"),
        "entity": Path("com/example/app/ai/entity"),
        "repository": Path("com/example/app/ai/repository"),
    }


# --- Audit log fixtures ---

@pytest.fixture
def audit_disabled():
    """Audit log with enabled=false."""
    return {"enabled": False}


@pytest.fixture
def audit_none():
    """Audit log is None."""
    return None


@pytest.fixture
def audit_minimal():
    """Audit log enabled with defaults only."""
    return {"enabled": True}


@pytest.fixture
def audit_with_retention():
    """Audit log with custom retention days."""
    return {
        "enabled": True,
        "retentionDays": 30,
    }


@pytest.fixture
def audit_with_cron():
    """Audit log with custom cleanup cron."""
    return {
        "enabled": True,
        "cleanupCronExpression": "0 30 4 * * *",
    }


@pytest.fixture
def audit_with_logged_events():
    """Audit log with specific logged events."""
    return {
        "enabled": True,
        "loggedEvents": [
            "orchestrator_request",
            "tool_invocation",
            "moderation_flag",
        ],
    }


@pytest.fixture
def audit_full():
    """Full audit log configuration."""
    return {
        "enabled": True,
        "retentionDays": 60,
        "cleanupCronExpression": "0 0 4 * * *",
        "loggedEvents": [
            "orchestrator_request",
            "tool_invocation",
            "moderation_flag",
            "security_violation",
            "budget_exceeded",
        ],
    }


@pytest.fixture
def audit_all_events():
    """Audit log with empty loggedEvents (log all)."""
    return {
        "enabled": True,
        "retentionDays": 90,
        "loggedEvents": [],
    }


# =====================================================================
# Test: generate() — file count and conditional generation
# =====================================================================

class TestAuditGeneratorGenerate:
    """Tests for the generate() method output."""

    def test_no_files_when_audit_is_none(self, generator, output_dirs):
        """Req 15.43: No files when auditLog is None."""
        assert generator.generate(None, "com.example.app", output_dirs) == []

    def test_no_files_when_audit_disabled(self, generator, audit_disabled, output_dirs):
        """Req 15.43: No files when auditLog.enabled is false."""
        assert generator.generate(audit_disabled, "com.example.app", output_dirs) == []

    def test_no_files_when_empty_dict(self, generator, output_dirs):
        """Req 15.43: No files when auditLog is empty dict."""
        assert generator.generate({}, "com.example.app", output_dirs) == []

    def test_minimal_generates_8_files(self, generator, audit_minimal, output_dirs):
        """Minimal config generates service + scheduler + controller + entity + repo + 3 DTOs = 8 files."""
        results = generator.generate(audit_minimal, "com.example.app", output_dirs)
        assert len(results) == 8

    def test_full_config_generates_8_files(self, generator, audit_full, output_dirs):
        """Full config also generates exactly 8 files."""
        results = generator.generate(audit_full, "com.example.app", output_dirs)
        assert len(results) == 8

    def test_all_content_is_nonempty(self, generator, audit_full, output_dirs):
        """All generated files have non-empty content."""
        results = generator.generate(audit_full, "com.example.app", output_dirs)
        for filepath, content in results:
            assert content.strip(), f"Empty content for {filepath}"

    def test_output_dirs_used_in_paths(self, generator, audit_full, output_dirs):
        """Output directory paths are used in generated file paths."""
        results = generator.generate(audit_full, "com.example.app", output_dirs)
        paths = [fp for fp, _ in results]
        assert any("com/example/app/ai/audit" in p for p in paths)
        assert any("com/example/app/ai/controller" in p for p in paths)
        assert any("com/example/app/ai/dto" in p for p in paths)
        assert any("com/example/app/ai/entity" in p for p in paths)
        assert any("com/example/app/ai/repository" in p for p in paths)

    def test_correct_filenames(self, generator, audit_full, output_dirs):
        """Correct Java class filenames are generated."""
        results = generator.generate(audit_full, "com.example.app", output_dirs)
        filenames = [Path(fp).name for fp, _ in results]
        assert "AiAuditService.java" in filenames
        assert "AiAuditCleanupScheduler.java" in filenames
        assert "AiAuditController.java" in filenames
        assert "AiAuditLog.java" in filenames
        assert "AiAuditLogRepository.java" in filenames
        assert "AiAuditEventDTO.java" in filenames
        assert "AiAuditStatsDTO.java" in filenames
        assert "AiAuditPageDTO.java" in filenames


# =====================================================================
# Test: AiAuditService template output
# =====================================================================

class TestAiAuditService:
    """Tests for the generated AiAuditService Java class."""

    def _get_service(self, generator, audit_log, output_dirs):
        results = generator.generate(audit_log, "com.example.app", output_dirs)
        for fp, content in results:
            if "AiAuditService.java" in fp:
                return content
        pytest.fail("AiAuditService.java not found in results")

    def test_package_declaration(self, generator, audit_minimal, output_dirs):
        content = self._get_service(generator, audit_minimal, output_dirs)
        assert "package com.example.app.ai.audit;" in content

    def test_service_annotation(self, generator, audit_minimal, output_dirs):
        content = self._get_service(generator, audit_minimal, output_dirs)
        assert "@Service" in content

    def test_class_name(self, generator, audit_minimal, output_dirs):
        content = self._get_service(generator, audit_minimal, output_dirs)
        assert "class AiAuditService" in content

    def test_repository_injection(self, generator, audit_minimal, output_dirs):
        content = self._get_service(generator, audit_minimal, output_dirs)
        assert "AiAuditLogRepository" in content

    def test_log_method_exists(self, generator, audit_minimal, output_dirs):
        """Req 15.35: Provides log() method accepting event details."""
        content = self._get_service(generator, audit_minimal, output_dirs)
        assert "public void log(" in content

    def test_fire_and_forget_on_bounded_elastic(self, generator, audit_minimal, output_dirs):
        """Req 15.34: Async fire-and-forget on Schedulers.boundedElastic()."""
        content = self._get_service(generator, audit_minimal, output_dirs)
        assert "Schedulers.boundedElastic()" in content

    def test_subscribe_fire_and_forget(self, generator, audit_minimal, output_dirs):
        """Req 15.34: Fire-and-forget via subscribe()."""
        content = self._get_service(generator, audit_minimal, output_dirs)
        assert ".subscribe(" in content

    def test_truncate_summary(self, generator, audit_minimal, output_dirs):
        """Req 15.35: requestSummary and responseSummary truncated to 1000 chars."""
        content = self._get_service(generator, audit_minimal, output_dirs)
        assert "MAX_SUMMARY_LENGTH" in content
        assert "1000" in content
        assert "truncate(" in content

    def test_should_log_method(self, generator, audit_minimal, output_dirs):
        """Req 15.45: shouldLog checks event type against config."""
        content = self._get_service(generator, audit_minimal, output_dirs)
        assert "shouldLog" in content

    def test_log_all_events_when_empty(self, generator, audit_all_events, output_dirs):
        """Req 15.45: When loggedEvents is empty, log all event types."""
        content = self._get_service(generator, audit_all_events, output_dirs)
        assert "LOG_ALL_EVENTS = true" in content

    def test_specific_logged_events(self, generator, audit_with_logged_events, output_dirs):
        """Req 15.45: When loggedEvents is specified, only those are logged."""
        content = self._get_service(generator, audit_with_logged_events, output_dirs)
        assert "LOG_ALL_EVENTS = false" in content
        assert '"orchestrator_request"' in content
        assert '"tool_invocation"' in content
        assert '"moderation_flag"' in content

    def test_failure_logged_at_warn(self, generator, audit_minimal, output_dirs):
        """Req 15.44: Failures in audit logging logged at WARN level."""
        content = self._get_service(generator, audit_minimal, output_dirs)
        assert "log.warn" in content

    def test_non_blocking_mono(self, generator, audit_minimal, output_dirs):
        """Req 15.44: Non-blocking audit recording."""
        content = self._get_service(generator, audit_minimal, output_dirs)
        assert "Mono.defer" in content

    def test_logging_annotation(self, generator, audit_minimal, output_dirs):
        content = self._get_service(generator, audit_minimal, output_dirs)
        assert "@Slf4j" in content

    def test_event_type_parameter(self, generator, audit_minimal, output_dirs):
        """Req 15.35: log() accepts eventType."""
        content = self._get_service(generator, audit_minimal, output_dirs)
        assert "String eventType" in content

    def test_user_id_parameter(self, generator, audit_minimal, output_dirs):
        """Req 15.35: log() accepts userId."""
        content = self._get_service(generator, audit_minimal, output_dirs)
        assert "Long userId" in content

    def test_status_parameter(self, generator, audit_minimal, output_dirs):
        """Req 15.35: log() accepts status."""
        content = self._get_service(generator, audit_minimal, output_dirs)
        assert "String status" in content

    def test_ip_address_parameter(self, generator, audit_minimal, output_dirs):
        """Req 15.35: log() accepts ipAddress."""
        content = self._get_service(generator, audit_minimal, output_dirs)
        assert "String ipAddress" in content


# =====================================================================
# Test: AiAuditCleanupScheduler template output
# =====================================================================

class TestAiAuditCleanupScheduler:
    """Tests for the generated AiAuditCleanupScheduler Java class."""

    def _get_scheduler(self, generator, audit_log, output_dirs):
        results = generator.generate(audit_log, "com.example.app", output_dirs)
        for fp, content in results:
            if "AiAuditCleanupScheduler.java" in fp:
                return content
        pytest.fail("AiAuditCleanupScheduler.java not found in results")

    def test_package_declaration(self, generator, audit_minimal, output_dirs):
        content = self._get_scheduler(generator, audit_minimal, output_dirs)
        assert "package com.example.app.ai.audit;" in content

    def test_component_annotation(self, generator, audit_minimal, output_dirs):
        content = self._get_scheduler(generator, audit_minimal, output_dirs)
        assert "@Component" in content

    def test_class_name(self, generator, audit_minimal, output_dirs):
        content = self._get_scheduler(generator, audit_minimal, output_dirs)
        assert "class AiAuditCleanupScheduler" in content

    def test_scheduled_annotation_default_cron(self, generator, audit_minimal, output_dirs):
        """Req 15.38: Default cron is 3 AM daily."""
        content = self._get_scheduler(generator, audit_minimal, output_dirs)
        assert '@Scheduled(cron = "0 0 3 * * *")' in content

    def test_scheduled_annotation_custom_cron(self, generator, audit_with_cron, output_dirs):
        """Req 15.38: Custom cron expression used."""
        content = self._get_scheduler(generator, audit_with_cron, output_dirs)
        assert '@Scheduled(cron = "0 30 4 * * *")' in content

    def test_default_retention_days(self, generator, audit_minimal, output_dirs):
        """Req 15.38: Default retention is 90 days."""
        content = self._get_scheduler(generator, audit_minimal, output_dirs)
        assert "minusDays(90)" in content

    def test_custom_retention_days(self, generator, audit_with_retention, output_dirs):
        """Req 15.38: Custom retention days used."""
        content = self._get_scheduler(generator, audit_with_retention, output_dirs)
        assert "minusDays(30)" in content

    def test_batch_size(self, generator, audit_minimal, output_dirs):
        """Req 15.38: Deletes in batches of 5000."""
        content = self._get_scheduler(generator, audit_minimal, output_dirs)
        assert "5000" in content

    def test_repository_injection(self, generator, audit_minimal, output_dirs):
        content = self._get_scheduler(generator, audit_minimal, output_dirs)
        assert "AiAuditLogRepository" in content

    def test_logging_annotation(self, generator, audit_minimal, output_dirs):
        content = self._get_scheduler(generator, audit_minimal, output_dirs)
        assert "@Slf4j" in content

    def test_cleanup_method_name(self, generator, audit_minimal, output_dirs):
        content = self._get_scheduler(generator, audit_minimal, output_dirs)
        assert "cleanupExpiredAuditRecords" in content


# =====================================================================
# Test: AiAuditController template output
# =====================================================================

class TestAiAuditController:
    """Tests for the generated AiAuditController Java class."""

    def _get_controller(self, generator, audit_log, output_dirs):
        results = generator.generate(audit_log, "com.example.app", output_dirs)
        for fp, content in results:
            if "AiAuditController.java" in fp:
                return content
        pytest.fail("AiAuditController.java not found in results")

    def test_package_declaration(self, generator, audit_minimal, output_dirs):
        content = self._get_controller(generator, audit_minimal, output_dirs)
        assert "package com.example.app.ai.controller;" in content

    def test_rest_controller_annotation(self, generator, audit_minimal, output_dirs):
        content = self._get_controller(generator, audit_minimal, output_dirs)
        assert "@RestController" in content

    def test_request_mapping(self, generator, audit_minimal, output_dirs):
        """Req 15.39: Base path /api/ai/audit."""
        content = self._get_controller(generator, audit_minimal, output_dirs)
        assert '@RequestMapping("/api/ai/audit")' in content

    def test_class_name(self, generator, audit_minimal, output_dirs):
        content = self._get_controller(generator, audit_minimal, output_dirs)
        assert "class AiAuditController" in content

    def test_admin_role_required(self, generator, audit_minimal, output_dirs):
        """Req 15.39: All endpoints require JWT auth with admin role."""
        content = self._get_controller(generator, audit_minimal, output_dirs)
        assert "hasRole('ADMIN')" in content

    def test_paginated_listing_endpoint(self, generator, audit_minimal, output_dirs):
        """Req 15.39: GET / paginated audit log with filters."""
        content = self._get_controller(generator, audit_minimal, output_dirs)
        assert "@GetMapping" in content
        assert "getAuditLog" in content

    def test_filter_parameters(self, generator, audit_minimal, output_dirs):
        """Req 15.39: Filters: eventType, userId, providerName, status, dateFrom, dateTo."""
        content = self._get_controller(generator, audit_minimal, output_dirs)
        assert "eventType" in content
        assert "userId" in content
        assert "providerName" in content
        assert "status" in content
        assert "dateFrom" in content
        assert "dateTo" in content

    def test_pagination_parameters(self, generator, audit_minimal, output_dirs):
        """Req 15.39: Pagination with page and pageSize."""
        content = self._get_controller(generator, audit_minimal, output_dirs)
        assert "page" in content
        assert "pageSize" in content

    def test_stats_endpoint(self, generator, audit_minimal, output_dirs):
        """Req 15.39: GET /stats endpoint."""
        content = self._get_controller(generator, audit_minimal, output_dirs)
        assert '@GetMapping("/stats")' in content
        assert "getStats" in content

    def test_user_audit_trail_endpoint(self, generator, audit_minimal, output_dirs):
        """Req 15.39: GET /user/{userId} endpoint."""
        content = self._get_controller(generator, audit_minimal, output_dirs)
        assert '@GetMapping("/user/{userId}")' in content
        assert "getUserAuditTrail" in content

    def test_reactive_imports(self, generator, audit_minimal, output_dirs):
        content = self._get_controller(generator, audit_minimal, output_dirs)
        assert "import reactor.core.publisher.Flux;" in content
        assert "import reactor.core.publisher.Mono;" in content

    def test_audit_event_dto_usage(self, generator, audit_minimal, output_dirs):
        content = self._get_controller(generator, audit_minimal, output_dirs)
        assert "AiAuditEventDTO" in content

    def test_audit_page_dto_usage(self, generator, audit_minimal, output_dirs):
        content = self._get_controller(generator, audit_minimal, output_dirs)
        assert "AiAuditPageDTO" in content

    def test_audit_stats_dto_usage(self, generator, audit_minimal, output_dirs):
        content = self._get_controller(generator, audit_minimal, output_dirs)
        assert "AiAuditStatsDTO" in content


# =====================================================================
# Test: AiAuditLog entity template output
# =====================================================================

class TestAiAuditLogEntity:
    """Tests for the generated AiAuditLog entity Java class."""

    def _get_entity(self, generator, audit_log, output_dirs):
        results = generator.generate(audit_log, "com.example.app", output_dirs)
        for fp, content in results:
            if fp.endswith("AiAuditLog.java"):
                return content
        pytest.fail("AiAuditLog.java not found in results")

    def test_package_declaration(self, generator, audit_minimal, output_dirs):
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert "package com.example.app.ai.entity;" in content

    def test_table_annotation(self, generator, audit_minimal, output_dirs):
        """Req 15.41: @Table("ai_audit_log")."""
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert '@Table("ai_audit_log")' in content

    def test_class_name(self, generator, audit_minimal, output_dirs):
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert "class AiAuditLog" in content

    def test_id_field(self, generator, audit_minimal, output_dirs):
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert "@Id" in content
        assert "Long id" in content

    def test_event_type_field(self, generator, audit_minimal, output_dirs):
        """Req 15.37: event_type column."""
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert "eventType" in content

    def test_user_id_field(self, generator, audit_minimal, output_dirs):
        """Req 15.37: user_id column."""
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert "userId" in content

    def test_provider_name_field(self, generator, audit_minimal, output_dirs):
        """Req 15.37: provider_name column (nullable)."""
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert "providerName" in content

    def test_operation_name_field(self, generator, audit_minimal, output_dirs):
        """Req 15.37: operation_name column (nullable)."""
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert "operationName" in content

    def test_tool_name_field(self, generator, audit_minimal, output_dirs):
        """Req 15.37: tool_name column (nullable)."""
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert "toolName" in content

    def test_request_summary_field(self, generator, audit_minimal, output_dirs):
        """Req 15.37: request_summary column (TEXT, nullable)."""
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert "requestSummary" in content

    def test_response_summary_field(self, generator, audit_minimal, output_dirs):
        """Req 15.37: response_summary column (TEXT, nullable)."""
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert "responseSummary" in content

    def test_duration_ms_field(self, generator, audit_minimal, output_dirs):
        """Req 15.37: duration_ms column (BIGINT, nullable)."""
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert "durationMs" in content

    def test_status_field(self, generator, audit_minimal, output_dirs):
        """Req 15.37: status column."""
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert "String status" in content

    def test_details_field(self, generator, audit_minimal, output_dirs):
        """Req 15.37: details column (JSON, nullable)."""
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert "details" in content

    def test_ip_address_field(self, generator, audit_minimal, output_dirs):
        """Req 15.37: ip_address column (nullable)."""
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert "ipAddress" in content

    def test_created_at_field(self, generator, audit_minimal, output_dirs):
        """Req 15.37: created_at column."""
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert "createdAt" in content

    def test_data_annotation(self, generator, audit_minimal, output_dirs):
        content = self._get_entity(generator, audit_minimal, output_dirs)
        assert "@Data" in content


# =====================================================================
# Test: AiAuditLogRepository template output
# =====================================================================

class TestAiAuditLogRepository:
    """Tests for the generated AiAuditLogRepository Java interface."""

    def _get_repo(self, generator, audit_log, output_dirs):
        results = generator.generate(audit_log, "com.example.app", output_dirs)
        for fp, content in results:
            if "AiAuditLogRepository.java" in fp:
                return content
        pytest.fail("AiAuditLogRepository.java not found in results")

    def test_package_declaration(self, generator, audit_minimal, output_dirs):
        content = self._get_repo(generator, audit_minimal, output_dirs)
        assert "package com.example.app.ai.repository;" in content

    def test_repository_annotation(self, generator, audit_minimal, output_dirs):
        content = self._get_repo(generator, audit_minimal, output_dirs)
        assert "@Repository" in content

    def test_extends_r2dbc_repository(self, generator, audit_minimal, output_dirs):
        """Req 15.41: R2dbcRepository for reactive access."""
        content = self._get_repo(generator, audit_minimal, output_dirs)
        assert "R2dbcRepository<AiAuditLog, Long>" in content

    def test_find_by_user_id_method(self, generator, audit_minimal, output_dirs):
        """Req 15.41: Query by user."""
        content = self._get_repo(generator, audit_minimal, output_dirs)
        assert "findByUserIdOrderByCreatedAtDesc" in content

    def test_find_by_event_type_method(self, generator, audit_minimal, output_dirs):
        """Req 15.41: Query by event type."""
        content = self._get_repo(generator, audit_minimal, output_dirs)
        assert "findByEventTypeOrderByCreatedAtDesc" in content

    def test_find_by_filters_method(self, generator, audit_minimal, output_dirs):
        """Req 15.41: Filtering by event type, user, provider, status, date range."""
        content = self._get_repo(generator, audit_minimal, output_dirs)
        assert "findByFilters" in content

    def test_count_by_filters_method(self, generator, audit_minimal, output_dirs):
        """Req 15.39: Count for pagination."""
        content = self._get_repo(generator, audit_minimal, output_dirs)
        assert "countByFilters" in content

    def test_stats_by_event_type_method(self, generator, audit_minimal, output_dirs):
        """Req 15.39: Stats aggregation."""
        content = self._get_repo(generator, audit_minimal, output_dirs)
        assert "getStatsByEventType" in content

    def test_delete_by_created_at_method(self, generator, audit_minimal, output_dirs):
        """Req 15.38: Batch deletion for cleanup."""
        content = self._get_repo(generator, audit_minimal, output_dirs)
        assert "deleteByCreatedAtBeforeLimit" in content


# =====================================================================
# Test: DTO template outputs
# =====================================================================

class TestAiAuditEventDTO:
    """Tests for the generated AiAuditEventDTO Java class."""

    def _get_dto(self, generator, audit_log, output_dirs):
        results = generator.generate(audit_log, "com.example.app", output_dirs)
        for fp, content in results:
            if fp.endswith("AiAuditEventDTO.java"):
                return content
        pytest.fail("AiAuditEventDTO.java not found in results")

    def test_package_declaration(self, generator, audit_minimal, output_dirs):
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "package com.example.app.ai.dto;" in content

    def test_data_annotation(self, generator, audit_minimal, output_dirs):
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "@Data" in content

    def test_builder_annotation(self, generator, audit_minimal, output_dirs):
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "@Builder" in content

    def test_class_name(self, generator, audit_minimal, output_dirs):
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "class AiAuditEventDTO" in content

    def test_all_audit_log_fields(self, generator, audit_minimal, output_dirs):
        """Req 15.40: AiAuditEventDTO with all audit log fields."""
        content = self._get_dto(generator, audit_minimal, output_dirs)
        for field in [
            "eventType", "userId", "providerName", "operationName",
            "toolName", "requestSummary", "responseSummary", "durationMs",
            "status", "details", "ipAddress", "createdAt",
        ]:
            assert field in content, f"Missing field: {field}"


class TestAiAuditStatsDTO:
    """Tests for the generated AiAuditStatsDTO Java class."""

    def _get_dto(self, generator, audit_log, output_dirs):
        results = generator.generate(audit_log, "com.example.app", output_dirs)
        for fp, content in results:
            if "AiAuditStatsDTO.java" in fp:
                return content
        pytest.fail("AiAuditStatsDTO.java not found in results")

    def test_package_declaration(self, generator, audit_minimal, output_dirs):
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "package com.example.app.ai.dto;" in content

    def test_class_name(self, generator, audit_minimal, output_dirs):
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "class AiAuditStatsDTO" in content

    def test_event_type_field(self, generator, audit_minimal, output_dirs):
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "eventType" in content

    def test_count_field(self, generator, audit_minimal, output_dirs):
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "long count" in content

    def test_success_count_field(self, generator, audit_minimal, output_dirs):
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "successCount" in content

    def test_error_count_field(self, generator, audit_minimal, output_dirs):
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "errorCount" in content

    def test_blocked_count_field(self, generator, audit_minimal, output_dirs):
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "blockedCount" in content


class TestAiAuditPageDTO:
    """Tests for the generated AiAuditPageDTO Java class."""

    def _get_dto(self, generator, audit_log, output_dirs):
        results = generator.generate(audit_log, "com.example.app", output_dirs)
        for fp, content in results:
            if "AiAuditPageDTO.java" in fp:
                return content
        pytest.fail("AiAuditPageDTO.java not found in results")

    def test_package_declaration(self, generator, audit_minimal, output_dirs):
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "package com.example.app.ai.dto;" in content

    def test_class_name(self, generator, audit_minimal, output_dirs):
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "class AiAuditPageDTO" in content

    def test_events_field(self, generator, audit_minimal, output_dirs):
        """Req 15.40: events array."""
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "List<AiAuditEventDTO> events" in content

    def test_total_count_field(self, generator, audit_minimal, output_dirs):
        """Req 15.40: totalCount."""
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "totalCount" in content

    def test_page_field(self, generator, audit_minimal, output_dirs):
        """Req 15.40: page."""
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "int page" in content

    def test_page_size_field(self, generator, audit_minimal, output_dirs):
        """Req 15.40: pageSize."""
        content = self._get_dto(generator, audit_minimal, output_dirs)
        assert "pageSize" in content


# =====================================================================
# Test: _build_context
# =====================================================================

class TestBuildContext:
    """Tests for the _build_context method."""

    def test_defaults_when_minimal(self, generator):
        ctx = generator._build_context({"enabled": True}, "com.example.app")
        assert ctx["base_package"] == "com.example.app"
        assert ctx["retention_days"] == 90
        assert ctx["cleanup_cron"] == "0 0 3 * * *"
        assert ctx["logged_events"] == []
        assert ctx["log_all_events"] is True
        assert ctx["cleanup_batch_size"] == 5000

    def test_custom_retention(self, generator):
        audit = {"enabled": True, "retentionDays": 30}
        ctx = generator._build_context(audit, "com.test.pkg")
        assert ctx["retention_days"] == 30

    def test_custom_cron(self, generator):
        audit = {"enabled": True, "cleanupCronExpression": "0 30 4 * * *"}
        ctx = generator._build_context(audit, "com.test.pkg")
        assert ctx["cleanup_cron"] == "0 30 4 * * *"

    def test_specific_logged_events(self, generator):
        audit = {
            "enabled": True,
            "loggedEvents": ["orchestrator_request", "tool_invocation"],
        }
        ctx = generator._build_context(audit, "com.test.pkg")
        assert ctx["logged_events"] == ["orchestrator_request", "tool_invocation"]
        assert ctx["log_all_events"] is False

    def test_empty_logged_events_means_log_all(self, generator):
        audit = {"enabled": True, "loggedEvents": []}
        ctx = generator._build_context(audit, "com.test.pkg")
        assert ctx["log_all_events"] is True

    def test_null_logged_events_means_log_all(self, generator):
        audit = {"enabled": True, "loggedEvents": None}
        ctx = generator._build_context(audit, "com.test.pkg")
        assert ctx["log_all_events"] is True


# =====================================================================
# Test: Module constants
# =====================================================================

class TestModuleConstants:
    """Tests for module-level constants."""

    def test_default_retention_days(self):
        assert DEFAULT_RETENTION_DAYS == 90

    def test_default_cleanup_cron(self):
        assert DEFAULT_CLEANUP_CRON == "0 0 3 * * *"

    def test_cleanup_batch_size(self):
        assert CLEANUP_BATCH_SIZE == 5000

    def test_valid_event_types(self):
        assert VALID_EVENT_TYPES == frozenset({
            "orchestrator_request",
            "tool_invocation",
            "moderation_flag",
            "security_violation",
            "budget_exceeded",
            "session_created",
            "document_ingested",
            "provider_error",
            "circuit_breaker_state_change",
        })

    def test_valid_event_types_count(self):
        assert len(VALID_EVENT_TYPES) == 9
