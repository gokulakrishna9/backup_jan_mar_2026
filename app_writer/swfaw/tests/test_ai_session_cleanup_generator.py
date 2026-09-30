"""Unit tests for the AI SessionCleanupGenerator.

Verifies that the SessionCleanupGenerator produces correct Java source files
for ChatSessionCleanupScheduler, TopicSummarizationService,
TopicAnalyticsController, topic entities (AiTopic, AiUserTopicHit,
AiGlobalTopicHit), repositories, and DTOs.

Requirements: 4.10–4.25
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_session_cleanup_generator import (
    SessionCleanupGenerator,
    DEFAULT_TTL_DAYS,
    DEFAULT_CLEANUP_CRON,
    DEFAULT_BATCH_SIZE,
    DEFAULT_MAX_TOPICS_PER_SESSION,
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
    return SessionCleanupGenerator(jinja_env)


@pytest.fixture
def output_dirs():
    return {
        "scheduler": Path("com/example/app/ai/scheduler"),
        "service": Path("com/example/app/ai/service"),
        "controller": Path("com/example/app/ai/controller"),
        "dto": Path("com/example/app/ai/dto"),
        "entity": Path("com/example/app/ai/entity"),
        "repository": Path("com/example/app/ai/repository"),
    }


# --- Cleanup config fixtures ---

@pytest.fixture
def cleanup_disabled():
    """Cleanup with enabled=false."""
    return {"enabled": False}


@pytest.fixture
def cleanup_none():
    """Cleanup is None."""
    return None


@pytest.fixture
def cleanup_minimal():
    """Cleanup enabled with defaults only (no topic summarization)."""
    return {"enabled": True}


@pytest.fixture
def cleanup_with_ttl():
    """Cleanup with custom TTL days."""
    return {
        "enabled": True,
        "defaultTtlDays": 14,
    }


@pytest.fixture
def cleanup_with_cron():
    """Cleanup with custom cron expression."""
    return {
        "enabled": True,
        "cleanupCronExpression": "0 30 3 * * *",
    }


@pytest.fixture
def cleanup_with_batch_size():
    """Cleanup with custom batch size."""
    return {
        "enabled": True,
        "batchSize": 500,
    }


@pytest.fixture
def cleanup_with_topics():
    """Cleanup with topic summarization enabled."""
    return {
        "enabled": True,
        "topicSummarization": {
            "enabled": True,
            "providerName": "gpt4",
            "maxTopicsPerSession": 3,
        },
    }


@pytest.fixture
def cleanup_full():
    """Full cleanup configuration with topic summarization."""
    return {
        "enabled": True,
        "defaultTtlDays": 7,
        "cleanupCronExpression": "0 0 1 * * *",
        "batchSize": 2000,
        "topicSummarization": {
            "enabled": True,
            "providerName": "gpt4",
            "maxTopicsPerSession": 10,
        },
    }


@pytest.fixture
def cleanup_topics_disabled():
    """Cleanup enabled but topic summarization explicitly disabled."""
    return {
        "enabled": True,
        "topicSummarization": {
            "enabled": False,
        },
    }


BASE_PACKAGE = "com.example.app"


# =====================================================================
# Test: generate() — file count and conditional generation
# =====================================================================

class TestSessionCleanupGeneratorGenerate:
    """Req 4.23: No files when cleanup absent/disabled."""

    def test_no_files_when_cleanup_is_none(self, generator, output_dirs):
        result = generator.generate(None, BASE_PACKAGE, output_dirs)
        assert result == []

    def test_no_files_when_cleanup_disabled(self, generator, cleanup_disabled, output_dirs):
        result = generator.generate(cleanup_disabled, BASE_PACKAGE, output_dirs)
        assert result == []

    def test_no_files_when_empty_dict(self, generator, output_dirs):
        result = generator.generate({}, BASE_PACKAGE, output_dirs)
        assert result == []

    def test_minimal_generates_1_file(self, generator, cleanup_minimal, output_dirs):
        """Without topic summarization, only the scheduler is generated."""
        result = generator.generate(cleanup_minimal, BASE_PACKAGE, output_dirs)
        assert len(result) == 1

    def test_topics_disabled_generates_1_file(self, generator, cleanup_topics_disabled, output_dirs):
        result = generator.generate(cleanup_topics_disabled, BASE_PACKAGE, output_dirs)
        assert len(result) == 1

    def test_with_topics_generates_13_files(self, generator, cleanup_with_topics, output_dirs):
        """With topic summarization: scheduler + service + controller + 3 entities + 3 repos + 4 DTOs = 13."""
        result = generator.generate(cleanup_with_topics, BASE_PACKAGE, output_dirs)
        assert len(result) == 13

    def test_full_config_generates_13_files(self, generator, cleanup_full, output_dirs):
        result = generator.generate(cleanup_full, BASE_PACKAGE, output_dirs)
        assert len(result) == 13

    def test_all_content_is_nonempty(self, generator, cleanup_full, output_dirs):
        result = generator.generate(cleanup_full, BASE_PACKAGE, output_dirs)
        for filepath, content in result:
            assert content.strip(), f"Empty content for {filepath}"

    def test_output_dirs_used_in_paths(self, generator, cleanup_full, output_dirs):
        result = generator.generate(cleanup_full, BASE_PACKAGE, output_dirs)
        paths = [fp for fp, _ in result]
        assert any("com/example/app/ai/scheduler" in p for p in paths)
        assert any("com/example/app/ai/service" in p for p in paths)
        assert any("com/example/app/ai/controller" in p for p in paths)
        assert any("com/example/app/ai/entity" in p for p in paths)
        assert any("com/example/app/ai/repository" in p for p in paths)
        assert any("com/example/app/ai/dto" in p for p in paths)

    def test_correct_filenames(self, generator, cleanup_full, output_dirs):
        result = generator.generate(cleanup_full, BASE_PACKAGE, output_dirs)
        filenames = [Path(fp).name for fp, _ in result]
        assert "ChatSessionCleanupScheduler.java" in filenames
        assert "TopicSummarizationService.java" in filenames
        assert "TopicAnalyticsController.java" in filenames
        assert "AiTopic.java" in filenames
        assert "AiUserTopicHit.java" in filenames
        assert "AiGlobalTopicHit.java" in filenames
        assert "AiTopicRepository.java" in filenames
        assert "AiUserTopicHitRepository.java" in filenames
        assert "AiGlobalTopicHitRepository.java" in filenames
        assert "TopicDTO.java" in filenames
        assert "UserTopicHitDTO.java" in filenames
        assert "GlobalTopicHitDTO.java" in filenames
        assert "TopicAnalyticsResponseDTO.java" in filenames


# =====================================================================
# Test: ChatSessionCleanupScheduler template
# =====================================================================

class TestChatSessionCleanupScheduler:
    """Req 4.10–4.14, 4.19, 4.25"""

    def _get_scheduler(self, generator, cleanup, output_dirs):
        result = generator.generate(cleanup, BASE_PACKAGE, output_dirs)
        for fp, content in result:
            if "ChatSessionCleanupScheduler.java" in fp:
                return content
        pytest.fail("ChatSessionCleanupScheduler.java not found")

    def test_package_declaration(self, generator, cleanup_minimal, output_dirs):
        content = self._get_scheduler(generator, cleanup_minimal, output_dirs)
        assert "package com.example.app.ai.scheduler;" in content

    def test_component_annotation(self, generator, cleanup_minimal, output_dirs):
        content = self._get_scheduler(generator, cleanup_minimal, output_dirs)
        assert "@Component" in content

    def test_class_name(self, generator, cleanup_minimal, output_dirs):
        content = self._get_scheduler(generator, cleanup_minimal, output_dirs)
        assert "class ChatSessionCleanupScheduler" in content

    def test_scheduled_annotation_default_cron(self, generator, cleanup_minimal, output_dirs):
        content = self._get_scheduler(generator, cleanup_minimal, output_dirs)
        assert '@Scheduled(cron = "0 0 2 * * *")' in content

    def test_scheduled_annotation_custom_cron(self, generator, cleanup_with_cron, output_dirs):
        content = self._get_scheduler(generator, cleanup_with_cron, output_dirs)
        assert '@Scheduled(cron = "0 30 3 * * *")' in content

    def test_default_ttl_days(self, generator, cleanup_minimal, output_dirs):
        content = self._get_scheduler(generator, cleanup_minimal, output_dirs)
        assert "DEFAULT_TTL_DAYS = 30" in content

    def test_custom_ttl_days(self, generator, cleanup_with_ttl, output_dirs):
        content = self._get_scheduler(generator, cleanup_with_ttl, output_dirs)
        assert "DEFAULT_TTL_DAYS = 14" in content

    def test_default_batch_size(self, generator, cleanup_minimal, output_dirs):
        content = self._get_scheduler(generator, cleanup_minimal, output_dirs)
        assert "BATCH_SIZE = 1000" in content

    def test_custom_batch_size(self, generator, cleanup_with_batch_size, output_dirs):
        content = self._get_scheduler(generator, cleanup_with_batch_size, output_dirs)
        assert "BATCH_SIZE = 500" in content

    def test_session_repository_injection(self, generator, cleanup_minimal, output_dirs):
        content = self._get_scheduler(generator, cleanup_minimal, output_dirs)
        assert "AiChatSessionRepository" in content

    def test_message_repository_injection(self, generator, cleanup_minimal, output_dirs):
        content = self._get_scheduler(generator, cleanup_minimal, output_dirs)
        assert "AiChatMessageRepository" in content

    def test_logging_annotation(self, generator, cleanup_minimal, output_dirs):
        content = self._get_scheduler(generator, cleanup_minimal, output_dirs)
        assert "@Slf4j" in content

    def test_cleanup_method_name(self, generator, cleanup_minimal, output_dirs):
        content = self._get_scheduler(generator, cleanup_minimal, output_dirs)
        assert "cleanupExpiredSessions" in content

    def test_no_topic_service_when_disabled(self, generator, cleanup_minimal, output_dirs):
        content = self._get_scheduler(generator, cleanup_minimal, output_dirs)
        assert "TopicSummarizationService" not in content

    def test_topic_service_when_enabled(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_scheduler(generator, cleanup_with_topics, output_dirs)
        assert "TopicSummarizationService" in content
        assert "topicSummarizationService" in content

    def test_delete_messages_before_session(self, generator, cleanup_minimal, output_dirs):
        content = self._get_scheduler(generator, cleanup_minimal, output_dirs)
        msg_idx = content.index("deleteBySessionId")
        sess_idx = content.index("deleteById")
        assert msg_idx < sess_idx, "Messages should be deleted before session"

    def test_info_logging_on_completion(self, generator, cleanup_minimal, output_dirs):
        content = self._get_scheduler(generator, cleanup_minimal, output_dirs)
        assert "cleanup completed" in content.lower()


# =====================================================================
# Test: TopicSummarizationService template
# =====================================================================

class TestTopicSummarizationService:
    """Req 4.15–4.17, 4.19"""

    def _get_service(self, generator, cleanup, output_dirs):
        result = generator.generate(cleanup, BASE_PACKAGE, output_dirs)
        for fp, content in result:
            if "TopicSummarizationService.java" in fp:
                return content
        pytest.fail("TopicSummarizationService.java not found")

    def test_package_declaration(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_service(generator, cleanup_with_topics, output_dirs)
        assert "package com.example.app.ai.service;" in content

    def test_service_annotation(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_service(generator, cleanup_with_topics, output_dirs)
        assert "@Service" in content

    def test_class_name(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_service(generator, cleanup_with_topics, output_dirs)
        assert "class TopicSummarizationService" in content

    def test_qualifier_annotation(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_service(generator, cleanup_with_topics, output_dirs)
        assert '@Qualifier("gpt4")' in content

    def test_chat_client_injection(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_service(generator, cleanup_with_topics, output_dirs)
        assert "ChatClient chatClient" in content

    def test_max_topics_constant(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_service(generator, cleanup_with_topics, output_dirs)
        assert "MAX_TOPICS = 3" in content

    def test_full_max_topics(self, generator, cleanup_full, output_dirs):
        content = self._get_service(generator, cleanup_full, output_dirs)
        assert "MAX_TOPICS = 10" in content

    def test_summarize_session_method(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_service(generator, cleanup_with_topics, output_dirs)
        assert "summarizeSession" in content

    def test_topic_repository_injection(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_service(generator, cleanup_with_topics, output_dirs)
        assert "AiTopicRepository" in content

    def test_user_topic_hit_repository(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_service(generator, cleanup_with_topics, output_dirs)
        assert "AiUserTopicHitRepository" in content

    def test_global_topic_hit_repository(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_service(generator, cleanup_with_topics, output_dirs)
        assert "AiGlobalTopicHitRepository" in content

    def test_json_parsing(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_service(generator, cleanup_with_topics, output_dirs)
        assert "ObjectMapper" in content

    def test_logging_annotation(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_service(generator, cleanup_with_topics, output_dirs)
        assert "@Slf4j" in content

    def test_topic_extraction_prompt(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_service(generator, cleanup_with_topics, output_dirs)
        assert "TOPIC_EXTRACTION_PROMPT" in content
        assert "JSON array" in content

    def test_not_generated_when_topics_disabled(self, generator, cleanup_minimal, output_dirs):
        result = generator.generate(cleanup_minimal, BASE_PACKAGE, output_dirs)
        filenames = [Path(fp).name for fp, _ in result]
        assert "TopicSummarizationService.java" not in filenames


# =====================================================================
# Test: TopicAnalyticsController template
# =====================================================================

class TestTopicAnalyticsController:
    """Req 4.20"""

    def _get_controller(self, generator, cleanup, output_dirs):
        result = generator.generate(cleanup, BASE_PACKAGE, output_dirs)
        for fp, content in result:
            if "TopicAnalyticsController.java" in fp:
                return content
        pytest.fail("TopicAnalyticsController.java not found")

    def test_package_declaration(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_controller(generator, cleanup_with_topics, output_dirs)
        assert "package com.example.app.ai.controller;" in content

    def test_rest_controller_annotation(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_controller(generator, cleanup_with_topics, output_dirs)
        assert "@RestController" in content

    def test_request_mapping(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_controller(generator, cleanup_with_topics, output_dirs)
        assert '@RequestMapping("/api/ai/topics")' in content

    def test_class_name(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_controller(generator, cleanup_with_topics, output_dirs)
        assert "class TopicAnalyticsController" in content

    def test_user_endpoint(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_controller(generator, cleanup_with_topics, output_dirs)
        assert '@GetMapping("/user")' in content

    def test_global_endpoint(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_controller(generator, cleanup_with_topics, output_dirs)
        assert '@GetMapping("/global")' in content

    def test_admin_user_endpoint(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_controller(generator, cleanup_with_topics, output_dirs)
        assert '@GetMapping("/admin/user/{userId}")' in content

    def test_admin_role_on_admin_endpoint(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_controller(generator, cleanup_with_topics, output_dirs)
        assert "@PreAuthorize" in content
        assert "hasRole('ADMIN')" in content

    def test_jwt_auth_principal(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_controller(generator, cleanup_with_topics, output_dirs)
        assert "@AuthenticationPrincipal Jwt jwt" in content

    def test_pagination_parameters(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_controller(generator, cleanup_with_topics, output_dirs)
        assert "int page" in content
        assert "int pageSize" in content

    def test_reactive_return_types(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_controller(generator, cleanup_with_topics, output_dirs)
        assert "Mono<TopicAnalyticsResponseDTO>" in content

    def test_topic_dto_usage(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_controller(generator, cleanup_with_topics, output_dirs)
        assert "TopicDTO" in content

    def test_user_topic_hit_dto_usage(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_controller(generator, cleanup_with_topics, output_dirs)
        assert "UserTopicHitDTO" in content

    def test_global_topic_hit_dto_usage(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_controller(generator, cleanup_with_topics, output_dirs)
        assert "GlobalTopicHitDTO" in content

    def test_not_generated_when_topics_disabled(self, generator, cleanup_minimal, output_dirs):
        result = generator.generate(cleanup_minimal, BASE_PACKAGE, output_dirs)
        filenames = [Path(fp).name for fp, _ in result]
        assert "TopicAnalyticsController.java" not in filenames


# =====================================================================
# Test: AiTopic entity template
# =====================================================================

class TestAiTopicEntity:
    """Req 4.18"""

    def _get_entity(self, generator, cleanup, output_dirs):
        result = generator.generate(cleanup, BASE_PACKAGE, output_dirs)
        for fp, content in result:
            if Path(fp).name == "AiTopic.java":
                return content
        pytest.fail("AiTopic.java not found")

    def test_package_declaration(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "package com.example.app.ai.entity;" in content

    def test_table_annotation(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert '@Table("ai_topic")' in content

    def test_class_name(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "class AiTopic" in content

    def test_id_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "@Id" in content
        assert "private Long id;" in content

    def test_name_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "private String name;" in content

    def test_created_at_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "private LocalDateTime createdAt;" in content

    def test_data_annotation(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "@Data" in content


# =====================================================================
# Test: AiUserTopicHit entity template
# =====================================================================

class TestAiUserTopicHitEntity:
    """Req 4.18"""

    def _get_entity(self, generator, cleanup, output_dirs):
        result = generator.generate(cleanup, BASE_PACKAGE, output_dirs)
        for fp, content in result:
            if Path(fp).name == "AiUserTopicHit.java":
                return content
        pytest.fail("AiUserTopicHit.java not found")

    def test_package_declaration(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "package com.example.app.ai.entity;" in content

    def test_table_annotation(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert '@Table("ai_user_topic_hit")' in content

    def test_class_name(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "class AiUserTopicHit" in content

    def test_user_id_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "private Long userId;" in content

    def test_topic_id_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "private Long topicId;" in content

    def test_hit_count_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "private Integer hitCount;" in content

    def test_first_seen_at_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "private LocalDateTime firstSeenAt;" in content

    def test_last_seen_at_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "private LocalDateTime lastSeenAt;" in content


# =====================================================================
# Test: AiGlobalTopicHit entity template
# =====================================================================

class TestAiGlobalTopicHitEntity:
    """Req 4.18"""

    def _get_entity(self, generator, cleanup, output_dirs):
        result = generator.generate(cleanup, BASE_PACKAGE, output_dirs)
        for fp, content in result:
            if Path(fp).name == "AiGlobalTopicHit.java":
                return content
        pytest.fail("AiGlobalTopicHit.java not found")

    def test_package_declaration(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "package com.example.app.ai.entity;" in content

    def test_table_annotation(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert '@Table("ai_global_topic_hit")' in content

    def test_class_name(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "class AiGlobalTopicHit" in content

    def test_topic_id_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "private Long topicId;" in content

    def test_hit_count_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "private Integer hitCount;" in content

    def test_first_seen_at_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "private LocalDateTime firstSeenAt;" in content

    def test_last_seen_at_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_entity(generator, cleanup_with_topics, output_dirs)
        assert "private LocalDateTime lastSeenAt;" in content


# =====================================================================
# Test: Repository templates
# =====================================================================

class TestAiTopicRepository:
    """Req 4.17"""

    def _get_repo(self, generator, cleanup, output_dirs):
        result = generator.generate(cleanup, BASE_PACKAGE, output_dirs)
        for fp, content in result:
            if Path(fp).name == "AiTopicRepository.java":
                return content
        pytest.fail("AiTopicRepository.java not found")

    def test_package_declaration(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_repo(generator, cleanup_with_topics, output_dirs)
        assert "package com.example.app.ai.repository;" in content

    def test_repository_annotation(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_repo(generator, cleanup_with_topics, output_dirs)
        assert "@Repository" in content

    def test_extends_r2dbc_repository(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_repo(generator, cleanup_with_topics, output_dirs)
        assert "extends R2dbcRepository<AiTopic, Long>" in content

    def test_find_by_name_method(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_repo(generator, cleanup_with_topics, output_dirs)
        assert "findByName(String name)" in content


class TestAiUserTopicHitRepository:
    """Req 4.17, 4.20"""

    def _get_repo(self, generator, cleanup, output_dirs):
        result = generator.generate(cleanup, BASE_PACKAGE, output_dirs)
        for fp, content in result:
            if Path(fp).name == "AiUserTopicHitRepository.java":
                return content
        pytest.fail("AiUserTopicHitRepository.java not found")

    def test_package_declaration(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_repo(generator, cleanup_with_topics, output_dirs)
        assert "package com.example.app.ai.repository;" in content

    def test_repository_annotation(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_repo(generator, cleanup_with_topics, output_dirs)
        assert "@Repository" in content

    def test_extends_r2dbc_repository(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_repo(generator, cleanup_with_topics, output_dirs)
        assert "extends R2dbcRepository<AiUserTopicHit, Long>" in content

    def test_find_by_user_and_topic(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_repo(generator, cleanup_with_topics, output_dirs)
        assert "findByUserIdAndTopicId" in content

    def test_find_by_user_ordered_by_hit_count(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_repo(generator, cleanup_with_topics, output_dirs)
        assert "findByUserIdOrderByHitCountDesc" in content
        assert "ORDER BY hit_count DESC" in content

    def test_count_by_user_id(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_repo(generator, cleanup_with_topics, output_dirs)
        assert "countByUserId" in content


class TestAiGlobalTopicHitRepository:
    """Req 4.17, 4.20"""

    def _get_repo(self, generator, cleanup, output_dirs):
        result = generator.generate(cleanup, BASE_PACKAGE, output_dirs)
        for fp, content in result:
            if Path(fp).name == "AiGlobalTopicHitRepository.java":
                return content
        pytest.fail("AiGlobalTopicHitRepository.java not found")

    def test_package_declaration(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_repo(generator, cleanup_with_topics, output_dirs)
        assert "package com.example.app.ai.repository;" in content

    def test_repository_annotation(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_repo(generator, cleanup_with_topics, output_dirs)
        assert "@Repository" in content

    def test_extends_r2dbc_repository(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_repo(generator, cleanup_with_topics, output_dirs)
        assert "extends R2dbcRepository<AiGlobalTopicHit, Long>" in content

    def test_find_by_topic_id(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_repo(generator, cleanup_with_topics, output_dirs)
        assert "findByTopicId" in content

    def test_find_all_ordered_by_hit_count(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_repo(generator, cleanup_with_topics, output_dirs)
        assert "findAllOrderByHitCountDesc" in content
        assert "ORDER BY hit_count DESC" in content


# =====================================================================
# Test: DTO templates
# =====================================================================

class TestTopicDTO:
    """Req 4.21"""

    def _get_dto(self, generator, cleanup, output_dirs):
        result = generator.generate(cleanup, BASE_PACKAGE, output_dirs)
        for fp, content in result:
            if Path(fp).name == "TopicDTO.java":
                return content
        pytest.fail("TopicDTO.java not found")

    def test_package_declaration(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "package com.example.app.ai.dto;" in content

    def test_builder_annotation(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "@Builder" in content

    def test_class_name(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "class TopicDTO" in content

    def test_id_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "private Long id;" in content

    def test_name_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "private String name;" in content

    def test_created_at_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "private LocalDateTime createdAt;" in content


class TestUserTopicHitDTO:
    """Req 4.21"""

    def _get_dto(self, generator, cleanup, output_dirs):
        result = generator.generate(cleanup, BASE_PACKAGE, output_dirs)
        for fp, content in result:
            if Path(fp).name == "UserTopicHitDTO.java":
                return content
        pytest.fail("UserTopicHitDTO.java not found")

    def test_package_declaration(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "package com.example.app.ai.dto;" in content

    def test_builder_annotation(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "@Builder" in content

    def test_class_name(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "class UserTopicHitDTO" in content

    def test_topic_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "private TopicDTO topic;" in content

    def test_hit_count_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "private Integer hitCount;" in content

    def test_first_seen_at_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "private LocalDateTime firstSeenAt;" in content

    def test_last_seen_at_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "private LocalDateTime lastSeenAt;" in content


class TestGlobalTopicHitDTO:
    """Req 4.21"""

    def _get_dto(self, generator, cleanup, output_dirs):
        result = generator.generate(cleanup, BASE_PACKAGE, output_dirs)
        for fp, content in result:
            if Path(fp).name == "GlobalTopicHitDTO.java":
                return content
        pytest.fail("GlobalTopicHitDTO.java not found")

    def test_package_declaration(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "package com.example.app.ai.dto;" in content

    def test_builder_annotation(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "@Builder" in content

    def test_class_name(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "class GlobalTopicHitDTO" in content

    def test_topic_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "private TopicDTO topic;" in content

    def test_hit_count_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "private Integer hitCount;" in content


class TestTopicAnalyticsResponseDTO:
    """Req 4.21"""

    def _get_dto(self, generator, cleanup, output_dirs):
        result = generator.generate(cleanup, BASE_PACKAGE, output_dirs)
        for fp, content in result:
            if Path(fp).name == "TopicAnalyticsResponseDTO.java":
                return content
        pytest.fail("TopicAnalyticsResponseDTO.java not found")

    def test_package_declaration(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "package com.example.app.ai.dto;" in content

    def test_builder_annotation(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "@Builder" in content

    def test_class_name(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "class TopicAnalyticsResponseDTO" in content

    def test_topics_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "topics" in content

    def test_total_topics_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "totalTopics" in content

    def test_page_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "private Integer page;" in content

    def test_page_size_field(self, generator, cleanup_with_topics, output_dirs):
        content = self._get_dto(generator, cleanup_with_topics, output_dirs)
        assert "private Integer pageSize;" in content


# =====================================================================
# Test: _build_context
# =====================================================================

class TestBuildContext:
    """Test the context builder method."""

    def test_defaults_when_minimal(self, generator):
        ctx = generator._build_context({"enabled": True}, BASE_PACKAGE)
        assert ctx["base_package"] == BASE_PACKAGE
        assert ctx["default_ttl_days"] == DEFAULT_TTL_DAYS
        assert ctx["cleanup_cron"] == DEFAULT_CLEANUP_CRON
        assert ctx["batch_size"] == DEFAULT_BATCH_SIZE
        assert ctx["topic_summarization_enabled"] is False
        assert ctx["topic_provider_name"] == ""
        assert ctx["max_topics_per_session"] == DEFAULT_MAX_TOPICS_PER_SESSION

    def test_custom_ttl(self, generator):
        ctx = generator._build_context({"enabled": True, "defaultTtlDays": 7}, BASE_PACKAGE)
        assert ctx["default_ttl_days"] == 7

    def test_custom_cron(self, generator):
        ctx = generator._build_context(
            {"enabled": True, "cleanupCronExpression": "0 0 4 * * *"}, BASE_PACKAGE
        )
        assert ctx["cleanup_cron"] == "0 0 4 * * *"

    def test_custom_batch_size(self, generator):
        ctx = generator._build_context({"enabled": True, "batchSize": 500}, BASE_PACKAGE)
        assert ctx["batch_size"] == 500

    def test_topic_summarization_enabled(self, generator):
        ctx = generator._build_context({
            "enabled": True,
            "topicSummarization": {
                "enabled": True,
                "providerName": "gpt4",
                "maxTopicsPerSession": 8,
            },
        }, BASE_PACKAGE)
        assert ctx["topic_summarization_enabled"] is True
        assert ctx["topic_provider_name"] == "gpt4"
        assert ctx["max_topics_per_session"] == 8

    def test_topic_summarization_disabled(self, generator):
        ctx = generator._build_context({
            "enabled": True,
            "topicSummarization": {"enabled": False},
        }, BASE_PACKAGE)
        assert ctx["topic_summarization_enabled"] is False

    def test_topic_summarization_none(self, generator):
        ctx = generator._build_context({
            "enabled": True,
            "topicSummarization": None,
        }, BASE_PACKAGE)
        assert ctx["topic_summarization_enabled"] is False


# =====================================================================
# Test: Module constants
# =====================================================================

class TestModuleConstants:
    """Verify module-level constants match spec defaults."""

    def test_default_ttl_days(self):
        assert DEFAULT_TTL_DAYS == 30

    def test_default_cleanup_cron(self):
        assert DEFAULT_CLEANUP_CRON == "0 0 2 * * *"

    def test_default_batch_size(self):
        assert DEFAULT_BATCH_SIZE == 1000

    def test_default_max_topics_per_session(self):
        assert DEFAULT_MAX_TOPICS_PER_SESSION == 5
