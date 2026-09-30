"""Unit tests for the AI AiDdlGenerator.

Verifies that the AiDdlGenerator produces correct conditional DDL SQL
for all AI-related tables based on which features are enabled.

Requirements: 4.18, 8.20, 11.10, 11.22, 15.24, 15.37, 16.1–16.8
"""

import sys
from pathlib import Path

import pytest

# Ensure swfaw package is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

import jinja2

from swfaw.generators.ai_ddl_generator import AiDdlGenerator, _SQL_TYPE_MAP


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
    return AiDdlGenerator(jinja_env)


# --- AI Layer definition fixtures ---

@pytest.fixture
def empty_layer():
    """AI layer with no features enabled."""
    return {
        "schemaVersion": "1.0",
        "providers": [],
        "entityCapabilities": [],
        "standaloneOperations": [],
        "promptTemplates": [],
        "assistants": [],
        "ragSources": [],
        "evaluators": [],
    }


@pytest.fixture
def layer_with_entity_chat():
    """AI layer with entity chat operation."""
    return {
        "entityCapabilities": [
            {"entityName": "Product", "enabledOperations": ["chat", "search"]},
        ],
        "standaloneOperations": [],
        "ragSources": [],
        "evaluators": [],
    }


@pytest.fixture
def layer_with_standalone_chat():
    """AI layer with standalone chat action."""
    return {
        "entityCapabilities": [],
        "standaloneOperations": [
            {"name": "helpdesk", "enabledActions": ["chat", "generate"]},
        ],
        "ragSources": [],
        "evaluators": [],
    }


@pytest.fixture
def layer_with_chatstream():
    """AI layer with chatStream operation."""
    return {
        "entityCapabilities": [
            {"entityName": "Order", "enabledOperations": ["chatStream"]},
        ],
        "standaloneOperations": [],
        "ragSources": [],
        "evaluators": [],
    }


@pytest.fixture
def layer_no_chat():
    """AI layer with entity ops but no chat."""
    return {
        "entityCapabilities": [
            {"entityName": "Product", "enabledOperations": ["search", "summarize"]},
        ],
        "standaloneOperations": [
            {"name": "helper", "enabledActions": ["generate", "query"]},
        ],
        "ragSources": [],
        "evaluators": [],
    }


@pytest.fixture
def layer_with_rag():
    """AI layer with an enabled RAG source."""
    return {
        "entityCapabilities": [],
        "standaloneOperations": [],
        "ragSources": [
            {"name": "product_docs", "type": "semantic", "enabled": True},
        ],
        "evaluators": [],
    }


@pytest.fixture
def layer_with_rag_disabled():
    """AI layer with RAG sources all disabled."""
    return {
        "entityCapabilities": [],
        "standaloneOperations": [],
        "ragSources": [
            {"name": "product_docs", "type": "semantic", "enabled": False},
        ],
        "evaluators": [],
    }


@pytest.fixture
def layer_with_evaluators():
    """AI layer with evaluators configured."""
    return {
        "entityCapabilities": [],
        "standaloneOperations": [],
        "ragSources": [],
        "evaluators": [
            {"name": "relevancy_check", "type": "relevancy"},
        ],
    }


@pytest.fixture
def layer_with_ingestion():
    """AI layer with document ingestion enabled."""
    return {
        "entityCapabilities": [],
        "standaloneOperations": [],
        "ragSources": [],
        "evaluators": [],
        "documentIngestion": {"enabled": True},
    }


@pytest.fixture
def layer_with_processing():
    """AI layer with document processing enabled (and ingestion)."""
    return {
        "entityCapabilities": [],
        "standaloneOperations": [],
        "ragSources": [],
        "evaluators": [],
        "documentIngestion": {"enabled": True},
        "documentProcessing": {"enabled": True},
    }


@pytest.fixture
def layer_with_token_budget():
    """AI layer with token budget enabled."""
    return {
        "entityCapabilities": [],
        "standaloneOperations": [],
        "ragSources": [],
        "evaluators": [],
        "tokenBudget": {"enabled": True},
    }


@pytest.fixture
def layer_with_audit_log():
    """AI layer with audit log enabled."""
    return {
        "entityCapabilities": [],
        "standaloneOperations": [],
        "ragSources": [],
        "evaluators": [],
        "auditLog": {"enabled": True},
    }


@pytest.fixture
def layer_with_topics():
    """AI layer with chatSessionCleanup + topicSummarization enabled."""
    return {
        "entityCapabilities": [],
        "standaloneOperations": [],
        "ragSources": [],
        "evaluators": [],
        "chatSessionCleanup": {
            "enabled": True,
            "topicSummarization": {"enabled": True, "providerName": "gpt4"},
        },
    }


@pytest.fixture
def layer_with_cleanup_no_topics():
    """AI layer with chatSessionCleanup but no topicSummarization."""
    return {
        "entityCapabilities": [],
        "standaloneOperations": [],
        "ragSources": [],
        "evaluators": [],
        "chatSessionCleanup": {"enabled": True},
    }


@pytest.fixture
def layer_with_state_table():
    """AI layer with a standalone operation that has a stateTable."""
    return {
        "entityCapabilities": [],
        "standaloneOperations": [
            {
                "name": "code_assistant",
                "enabledActions": ["generate"],
                "stateTable": {
                    "tableName": "ai_code_assistant_state",
                    "columns": [
                        {"name": "language", "type": "VARCHAR", "length": 50, "nullable": False},
                        {"name": "snippet", "type": "TEXT", "nullable": True},
                        {"name": "score", "type": "DOUBLE", "nullable": True, "defaultValue": "0.0"},
                        {"name": "is_active", "type": "BOOLEAN", "nullable": False, "defaultValue": "1"},
                    ],
                },
            },
        ],
        "ragSources": [],
        "evaluators": [],
    }


@pytest.fixture
def layer_full():
    """AI layer with all features enabled."""
    return {
        "entityCapabilities": [
            {"entityName": "Product", "enabledOperations": ["chat", "search"]},
        ],
        "standaloneOperations": [
            {
                "name": "helpdesk",
                "enabledActions": ["chat"],
                "stateTable": {
                    "tableName": "ai_helpdesk_state",
                    "columns": [
                        {"name": "ticket_id", "type": "VARCHAR", "length": 100},
                    ],
                },
            },
        ],
        "ragSources": [
            {"name": "docs", "type": "semantic", "enabled": True},
        ],
        "evaluators": [
            {"name": "safety", "type": "safety"},
        ],
        "documentIngestion": {"enabled": True},
        "documentProcessing": {"enabled": True},
        "tokenBudget": {"enabled": True},
        "auditLog": {"enabled": True},
        "chatSessionCleanup": {
            "enabled": True,
            "topicSummarization": {"enabled": True, "providerName": "gpt4"},
        },
    }


# ===================================================================
# Test: generate() — conditional generation
# ===================================================================

class TestAiDdlGeneratorGenerate:
    """Tests for the generate() method's conditional behavior."""

    def test_no_output_when_ai_layer_is_none(self, generator):
        assert generator.generate(None) == []

    def test_no_output_when_ai_layer_is_empty_dict(self, generator):
        assert generator.generate({}) == []

    def test_no_output_when_no_features_enabled(self, generator, empty_layer):
        assert generator.generate(empty_layer) == []

    def test_no_output_when_no_chat_ops(self, generator, layer_no_chat):
        assert generator.generate(layer_no_chat) == []

    def test_generates_one_file(self, generator, layer_with_entity_chat):
        result = generator.generate(layer_with_entity_chat)
        assert len(result) == 1

    def test_default_output_path(self, generator, layer_with_entity_chat):
        result = generator.generate(layer_with_entity_chat)
        assert result[0][0] == "ai_tables.sql"

    def test_custom_output_path(self, generator, layer_with_entity_chat):
        result = generator.generate(layer_with_entity_chat, output_path="schema/ai.sql")
        assert result[0][0] == "schema/ai.sql"

    def test_content_is_nonempty(self, generator, layer_with_entity_chat):
        result = generator.generate(layer_with_entity_chat)
        assert len(result[0][1]) > 0

    def test_full_layer_generates_one_file(self, generator, layer_full):
        result = generator.generate(layer_full)
        assert len(result) == 1


# ===================================================================
# Test: Chat tables (Req 16.1, 16.2)
# ===================================================================

class TestChatTables:
    """Tests for ai_chat_session and ai_chat_message DDL."""

    def _get_sql(self, generator, ai_layer):
        result = generator.generate(ai_layer)
        assert len(result) == 1
        return result[0][1]

    def test_entity_chat_creates_session_table(self, generator, layer_with_entity_chat):
        sql = self._get_sql(generator, layer_with_entity_chat)
        assert "CREATE TABLE IF NOT EXISTS ai_chat_session" in sql

    def test_entity_chat_creates_message_table(self, generator, layer_with_entity_chat):
        sql = self._get_sql(generator, layer_with_entity_chat)
        assert "CREATE TABLE IF NOT EXISTS ai_chat_message" in sql

    def test_standalone_chat_creates_tables(self, generator, layer_with_standalone_chat):
        sql = self._get_sql(generator, layer_with_standalone_chat)
        assert "ai_chat_session" in sql
        assert "ai_chat_message" in sql

    def test_chatstream_creates_tables(self, generator, layer_with_chatstream):
        sql = self._get_sql(generator, layer_with_chatstream)
        assert "ai_chat_session" in sql

    def test_no_chat_skips_tables(self, generator, layer_no_chat):
        result = generator.generate(layer_no_chat)
        assert result == []

    def test_session_user_entity_index(self, generator, layer_with_entity_chat):
        sql = self._get_sql(generator, layer_with_entity_chat)
        assert "idx_chat_session_user_entity" in sql
        assert "user_id, entity_type, entity_id" in sql

    def test_session_user_standalone_index(self, generator, layer_with_entity_chat):
        sql = self._get_sql(generator, layer_with_entity_chat)
        assert "idx_chat_session_user_standalone" in sql

    def test_message_fk_to_session(self, generator, layer_with_entity_chat):
        sql = self._get_sql(generator, layer_with_entity_chat)
        assert "FOREIGN KEY (session_id) REFERENCES ai_chat_session(id)" in sql

    def test_message_session_created_index(self, generator, layer_with_entity_chat):
        sql = self._get_sql(generator, layer_with_entity_chat)
        assert "idx_chat_message_session_created" in sql


# ===================================================================
# Test: RAG document chunk table (Req 16.4, 16.5)
# ===================================================================

class TestRagTable:
    """Tests for ai_document_chunk DDL."""

    def _get_sql(self, generator, ai_layer):
        result = generator.generate(ai_layer)
        assert len(result) == 1
        return result[0][1]

    def test_enabled_rag_creates_chunk_table(self, generator, layer_with_rag):
        sql = self._get_sql(generator, layer_with_rag)
        assert "CREATE TABLE IF NOT EXISTS ai_document_chunk" in sql

    def test_disabled_rag_skips_chunk_table(self, generator, layer_with_rag_disabled):
        result = generator.generate(layer_with_rag_disabled)
        assert result == []

    def test_fulltext_index_on_chunk_text(self, generator, layer_with_rag):
        sql = self._get_sql(generator, layer_with_rag)
        assert "FULLTEXT INDEX ft_doc_chunk_text (chunk_text)" in sql

    def test_source_entity_index(self, generator, layer_with_rag):
        sql = self._get_sql(generator, layer_with_rag)
        assert "idx_doc_chunk_source_entity" in sql
        assert "source_name, entity_type, entity_id" in sql


# ===================================================================
# Test: Evaluation result table (Req 16.6, 16.7)
# ===================================================================

class TestEvaluationTable:
    """Tests for ai_evaluation_result DDL."""

    def _get_sql(self, generator, ai_layer):
        result = generator.generate(ai_layer)
        assert len(result) == 1
        return result[0][1]

    def test_evaluators_create_table(self, generator, layer_with_evaluators):
        sql = self._get_sql(generator, layer_with_evaluators)
        assert "CREATE TABLE IF NOT EXISTS ai_evaluation_result" in sql

    def test_no_evaluators_skip_table(self, generator, empty_layer):
        result = generator.generate(empty_layer)
        assert result == []

    def test_user_operation_index(self, generator, layer_with_evaluators):
        sql = self._get_sql(generator, layer_with_evaluators)
        assert "idx_eval_user_operation" in sql

    def test_evaluator_created_index(self, generator, layer_with_evaluators):
        sql = self._get_sql(generator, layer_with_evaluators)
        assert "idx_eval_evaluator_created" in sql

    def test_composite_index(self, generator, layer_with_evaluators):
        sql = self._get_sql(generator, layer_with_evaluators)
        assert "idx_eval_op_evaluator_created" in sql


# ===================================================================
# Test: Document ingestion table (Req 11.10)
# ===================================================================

class TestIngestionTable:
    """Tests for ai_ingested_document DDL."""

    def _get_sql(self, generator, ai_layer):
        result = generator.generate(ai_layer)
        assert len(result) == 1
        return result[0][1]

    def test_ingestion_creates_table(self, generator, layer_with_ingestion):
        sql = self._get_sql(generator, layer_with_ingestion)
        assert "CREATE TABLE IF NOT EXISTS ai_ingested_document" in sql

    def test_user_source_index(self, generator, layer_with_ingestion):
        sql = self._get_sql(generator, layer_with_ingestion)
        assert "idx_ingested_user_source" in sql

    def test_status_index(self, generator, layer_with_ingestion):
        sql = self._get_sql(generator, layer_with_ingestion)
        assert "idx_ingested_status" in sql

    def test_rag_index(self, generator, layer_with_ingestion):
        sql = self._get_sql(generator, layer_with_ingestion)
        assert "idx_ingested_rag" in sql

    def test_longtext_extracted_text(self, generator, layer_with_ingestion):
        sql = self._get_sql(generator, layer_with_ingestion)
        assert "extracted_text LONGTEXT" in sql


# ===================================================================
# Test: Document processing table (Req 11.22)
# ===================================================================

class TestProcessingTable:
    """Tests for ai_document_task_result DDL."""

    def _get_sql(self, generator, ai_layer):
        result = generator.generate(ai_layer)
        assert len(result) == 1
        return result[0][1]

    def test_processing_creates_table(self, generator, layer_with_processing):
        sql = self._get_sql(generator, layer_with_processing)
        assert "CREATE TABLE IF NOT EXISTS ai_document_task_result" in sql

    def test_fk_to_ingested_document(self, generator, layer_with_processing):
        sql = self._get_sql(generator, layer_with_processing)
        assert "FOREIGN KEY (document_id) REFERENCES ai_ingested_document(id)" in sql

    def test_cascade_delete(self, generator, layer_with_processing):
        sql = self._get_sql(generator, layer_with_processing)
        assert "ON DELETE CASCADE" in sql

    def test_doc_name_index(self, generator, layer_with_processing):
        sql = self._get_sql(generator, layer_with_processing)
        assert "idx_task_doc_name" in sql

    def test_user_type_index(self, generator, layer_with_processing):
        sql = self._get_sql(generator, layer_with_processing)
        assert "idx_task_user_type" in sql

    def test_status_index(self, generator, layer_with_processing):
        sql = self._get_sql(generator, layer_with_processing)
        assert "idx_task_status" in sql


# ===================================================================
# Test: Token usage table (Req 15.24)
# ===================================================================

class TestTokenUsageTable:
    """Tests for ai_token_usage DDL."""

    def _get_sql(self, generator, ai_layer):
        result = generator.generate(ai_layer)
        assert len(result) == 1
        return result[0][1]

    def test_budget_creates_table(self, generator, layer_with_token_budget):
        sql = self._get_sql(generator, layer_with_token_budget)
        assert "CREATE TABLE IF NOT EXISTS ai_token_usage" in sql

    def test_user_provider_created_index(self, generator, layer_with_token_budget):
        sql = self._get_sql(generator, layer_with_token_budget)
        assert "idx_token_user_provider_created" in sql

    def test_user_created_index(self, generator, layer_with_token_budget):
        sql = self._get_sql(generator, layer_with_token_budget)
        assert "idx_token_user_created" in sql


# ===================================================================
# Test: Audit log table (Req 15.37)
# ===================================================================

class TestAuditLogTable:
    """Tests for ai_audit_log DDL."""

    def _get_sql(self, generator, ai_layer):
        result = generator.generate(ai_layer)
        assert len(result) == 1
        return result[0][1]

    def test_audit_creates_table(self, generator, layer_with_audit_log):
        sql = self._get_sql(generator, layer_with_audit_log)
        assert "CREATE TABLE IF NOT EXISTS ai_audit_log" in sql

    def test_event_created_index(self, generator, layer_with_audit_log):
        sql = self._get_sql(generator, layer_with_audit_log)
        assert "idx_audit_event_created" in sql

    def test_user_created_index(self, generator, layer_with_audit_log):
        sql = self._get_sql(generator, layer_with_audit_log)
        assert "idx_audit_user_created" in sql

    def test_user_event_index(self, generator, layer_with_audit_log):
        sql = self._get_sql(generator, layer_with_audit_log)
        assert "idx_audit_user_event" in sql

    def test_created_index(self, generator, layer_with_audit_log):
        sql = self._get_sql(generator, layer_with_audit_log)
        assert "idx_audit_created" in sql

    def test_ip_address_column(self, generator, layer_with_audit_log):
        sql = self._get_sql(generator, layer_with_audit_log)
        assert "ip_address VARCHAR(45)" in sql

    def test_details_json_column(self, generator, layer_with_audit_log):
        sql = self._get_sql(generator, layer_with_audit_log)
        assert "details JSON" in sql


# ===================================================================
# Test: Topic tables (Req 4.18)
# ===================================================================

class TestTopicTables:
    """Tests for ai_topic, ai_user_topic_hit, ai_global_topic_hit DDL."""

    def _get_sql(self, generator, ai_layer):
        result = generator.generate(ai_layer)
        assert len(result) == 1
        return result[0][1]

    def test_topics_create_all_three_tables(self, generator, layer_with_topics):
        sql = self._get_sql(generator, layer_with_topics)
        assert "CREATE TABLE IF NOT EXISTS ai_topic" in sql
        assert "CREATE TABLE IF NOT EXISTS ai_user_topic_hit" in sql
        assert "CREATE TABLE IF NOT EXISTS ai_global_topic_hit" in sql

    def test_cleanup_without_topics_skips(self, generator, layer_with_cleanup_no_topics):
        result = generator.generate(layer_with_cleanup_no_topics)
        assert result == []

    def test_topic_unique_name(self, generator, layer_with_topics):
        sql = self._get_sql(generator, layer_with_topics)
        assert "uq_topic_name" in sql

    def test_user_topic_unique_index(self, generator, layer_with_topics):
        sql = self._get_sql(generator, layer_with_topics)
        assert "uq_user_topic (user_id, topic_id)" in sql

    def test_user_topic_hits_index(self, generator, layer_with_topics):
        sql = self._get_sql(generator, layer_with_topics)
        assert "idx_user_topic_hits" in sql

    def test_global_topic_unique_index(self, generator, layer_with_topics):
        sql = self._get_sql(generator, layer_with_topics)
        assert "uq_global_topic (topic_id)" in sql

    def test_global_topic_hits_index(self, generator, layer_with_topics):
        sql = self._get_sql(generator, layer_with_topics)
        assert "idx_global_topic_hits" in sql

    def test_user_topic_fk(self, generator, layer_with_topics):
        sql = self._get_sql(generator, layer_with_topics)
        assert "fk_user_topic_hit_topic" in sql

    def test_global_topic_fk(self, generator, layer_with_topics):
        sql = self._get_sql(generator, layer_with_topics)
        assert "fk_global_topic_hit_topic" in sql


# ===================================================================
# Test: Standalone state tables (Req 16.3)
# ===================================================================

class TestStateTable:
    """Tests for standalone operation state table DDL."""

    def _get_sql(self, generator, ai_layer):
        result = generator.generate(ai_layer)
        assert len(result) == 1
        return result[0][1]

    def test_state_table_created(self, generator, layer_with_state_table):
        sql = self._get_sql(generator, layer_with_state_table)
        assert "CREATE TABLE IF NOT EXISTS ai_code_assistant_state" in sql

    def test_auto_id_column(self, generator, layer_with_state_table):
        sql = self._get_sql(generator, layer_with_state_table)
        assert "id BIGINT AUTO_INCREMENT PRIMARY KEY" in sql

    def test_auto_user_id_column(self, generator, layer_with_state_table):
        sql = self._get_sql(generator, layer_with_state_table)
        assert "user_id BIGINT NOT NULL" in sql

    def test_auto_timestamps(self, generator, layer_with_state_table):
        sql = self._get_sql(generator, layer_with_state_table)
        assert "created_at DATETIME" in sql
        assert "updated_at DATETIME" in sql

    def test_user_index(self, generator, layer_with_state_table):
        sql = self._get_sql(generator, layer_with_state_table)
        assert "idx_ai_code_assistant_state_user" in sql

    def test_varchar_with_length(self, generator, layer_with_state_table):
        sql = self._get_sql(generator, layer_with_state_table)
        assert "language VARCHAR(50)" in sql

    def test_not_null_column(self, generator, layer_with_state_table):
        sql = self._get_sql(generator, layer_with_state_table)
        assert "language VARCHAR(50) NOT NULL" in sql

    def test_nullable_column(self, generator, layer_with_state_table):
        sql = self._get_sql(generator, layer_with_state_table)
        # snippet is TEXT and nullable — should NOT have NOT NULL
        assert "snippet TEXT," in sql

    def test_default_value(self, generator, layer_with_state_table):
        sql = self._get_sql(generator, layer_with_state_table)
        assert "score DOUBLE DEFAULT 0.0" in sql

    def test_boolean_maps_to_tinyint(self, generator, layer_with_state_table):
        sql = self._get_sql(generator, layer_with_state_table)
        assert "is_active TINYINT(1) NOT NULL DEFAULT 1" in sql


# ===================================================================
# Test: Full layer — all tables present
# ===================================================================

class TestFullLayer:
    """Tests that a full AI layer generates all expected tables."""

    def _get_sql(self, generator, ai_layer):
        result = generator.generate(ai_layer)
        assert len(result) == 1
        return result[0][1]

    def test_all_tables_present(self, generator, layer_full):
        sql = self._get_sql(generator, layer_full)
        assert "ai_chat_session" in sql
        assert "ai_chat_message" in sql
        assert "ai_document_chunk" in sql
        assert "ai_evaluation_result" in sql
        assert "ai_ingested_document" in sql
        assert "ai_document_task_result" in sql
        assert "ai_token_usage" in sql
        assert "ai_audit_log" in sql
        assert "ai_topic" in sql
        assert "ai_user_topic_hit" in sql
        assert "ai_global_topic_hit" in sql
        assert "ai_helpdesk_state" in sql


# ===================================================================
# Test: Feature detection helpers
# ===================================================================

class TestFeatureDetection:
    """Tests for the static feature detection methods."""

    def test_has_chat_entity(self):
        layer = {"entityCapabilities": [{"enabledOperations": ["chat"]}], "standaloneOperations": []}
        assert AiDdlGenerator._has_chat_operations(layer) is True

    def test_has_chat_standalone(self):
        layer = {"entityCapabilities": [], "standaloneOperations": [{"enabledActions": ["chat"]}]}
        assert AiDdlGenerator._has_chat_operations(layer) is True

    def test_has_chatstream(self):
        layer = {"entityCapabilities": [{"enabledOperations": ["chatStream"]}], "standaloneOperations": []}
        assert AiDdlGenerator._has_chat_operations(layer) is True

    def test_no_chat(self):
        layer = {"entityCapabilities": [{"enabledOperations": ["search"]}], "standaloneOperations": []}
        assert AiDdlGenerator._has_chat_operations(layer) is False

    def test_has_enabled_rag(self):
        layer = {"ragSources": [{"enabled": True}]}
        assert AiDdlGenerator._has_enabled_rag_sources(layer) is True

    def test_no_enabled_rag(self):
        layer = {"ragSources": [{"enabled": False}]}
        assert AiDdlGenerator._has_enabled_rag_sources(layer) is False

    def test_empty_rag(self):
        layer = {"ragSources": []}
        assert AiDdlGenerator._has_enabled_rag_sources(layer) is False

    def test_has_evaluators(self):
        layer = {"evaluators": [{"name": "x"}]}
        assert AiDdlGenerator._has_evaluators(layer) is True

    def test_no_evaluators(self):
        layer = {"evaluators": []}
        assert AiDdlGenerator._has_evaluators(layer) is False

    def test_has_ingestion(self):
        layer = {"documentIngestion": {"enabled": True}}
        assert AiDdlGenerator._has_document_ingestion(layer) is True

    def test_no_ingestion(self):
        layer = {"documentIngestion": {"enabled": False}}
        assert AiDdlGenerator._has_document_ingestion(layer) is False

    def test_has_processing(self):
        layer = {"documentProcessing": {"enabled": True}}
        assert AiDdlGenerator._has_document_processing(layer) is True

    def test_has_budget(self):
        layer = {"tokenBudget": {"enabled": True}}
        assert AiDdlGenerator._has_token_budget(layer) is True

    def test_has_audit(self):
        layer = {"auditLog": {"enabled": True}}
        assert AiDdlGenerator._has_audit_log(layer) is True

    def test_has_topics(self):
        layer = {"chatSessionCleanup": {"enabled": True, "topicSummarization": {"enabled": True}}}
        assert AiDdlGenerator._has_topic_tables(layer) is True

    def test_no_topics_when_cleanup_disabled(self):
        layer = {"chatSessionCleanup": {"enabled": False, "topicSummarization": {"enabled": True}}}
        assert AiDdlGenerator._has_topic_tables(layer) is False

    def test_no_topics_when_summarization_disabled(self):
        layer = {"chatSessionCleanup": {"enabled": True, "topicSummarization": {"enabled": False}}}
        assert AiDdlGenerator._has_topic_tables(layer) is False


# ===================================================================
# Test: _build_context
# ===================================================================

class TestBuildContext:
    """Tests for the _build_context method."""

    def test_empty_layer_has_no_tables(self, generator, empty_layer):
        ctx = generator._build_context(empty_layer)
        assert ctx["has_any_table"] is False

    def test_full_layer_has_all_flags(self, generator, layer_full):
        ctx = generator._build_context(layer_full)
        assert ctx["has_any_table"] is True
        assert ctx["has_chat"] is True
        assert ctx["has_rag"] is True
        assert ctx["has_evaluators"] is True
        assert ctx["has_ingestion"] is True
        assert ctx["has_processing"] is True
        assert ctx["has_token_budget"] is True
        assert ctx["has_audit_log"] is True
        assert ctx["has_topics"] is True
        assert len(ctx["state_tables"]) == 1


# ===================================================================
# Test: SQL type mapping
# ===================================================================

class TestSqlTypeMap:
    """Tests for the _SQL_TYPE_MAP constant."""

    def test_varchar_mapping(self):
        assert _SQL_TYPE_MAP["VARCHAR"] == "VARCHAR"

    def test_boolean_mapping(self):
        assert _SQL_TYPE_MAP["BOOLEAN"] == "TINYINT(1)"

    def test_json_mapping(self):
        assert _SQL_TYPE_MAP["JSON"] == "JSON"

    def test_all_types_present(self):
        expected = {"VARCHAR", "TEXT", "INT", "BIGINT", "BOOLEAN", "DATETIME", "JSON", "DOUBLE"}
        assert set(_SQL_TYPE_MAP.keys()) == expected
