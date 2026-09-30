"""Property-based tests for Conditional Code Generation (Property 8).

Uses the AiDdlGenerator as a proxy for the full AI_Generator conditional
logic — it already implements feature detection for all AI features and
conditionally generates DDL iff the corresponding feature is enabled.

**Validates: Requirements 4.23, 5.1, 5.8, 6.1, 8.7, 9.1, 9.4, 10.3,
11.5, 11.10, 11.17, 13.1, 13.4, 13.9, 13.34, 15.12, 15.29, 15.43,
16.1–16.7**

# Feature: ai-layer, Property 8: Conditional Code Generation
"""

import sys
from pathlib import Path

import pytest
from hypothesis import given, settings, assume, HealthCheck
from hypothesis import strategies as st

# Ensure swfaw/ is on sys.path so imports resolve
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import jinja2

from generators.ai_ddl_generator import AiDdlGenerator


# ---------------------------------------------------------------------------
# Jinja2 environment fixture
# ---------------------------------------------------------------------------

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
_JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(_TEMPLATES_DIR)),
    keep_trailing_newline=True,
    trim_blocks=True,
    lstrip_blocks=True,
)
_GENERATOR = AiDdlGenerator(_JINJA_ENV)


# ---------------------------------------------------------------------------
# Strategies — building blocks
# ---------------------------------------------------------------------------

_identifier_st = st.from_regex(r"[a-z][a-z0-9_]{2,12}", fullmatch=True)
_entity_name_st = st.from_regex(r"[A-Z][a-zA-Z]{2,10}", fullmatch=True)

_entity_ops = ["search", "generate", "summarize", "classify", "chat", "chatStream"]
_standalone_actions = ["chat", "chatStream", "generate", "query"]

_col_type_st = st.sampled_from(["VARCHAR", "TEXT", "INT", "BIGINT", "BOOLEAN", "DATETIME", "JSON", "DOUBLE"])


# ---------------------------------------------------------------------------
# Composite strategy — random AI_Layer with features randomly toggled
# ---------------------------------------------------------------------------

@st.composite
def random_ai_layer_st(draw):
    """Generate an AI_Layer dict with each feature independently toggled."""
    used_names: set[str] = set()

    def fresh_name():
        n = draw(_identifier_st.filter(lambda x: x not in used_names))
        used_names.add(n)
        return n

    layer: dict = {
        "entityCapabilities": [],
        "standaloneOperations": [],
        "ragSources": [],
        "evaluators": [],
    }

    # --- Chat: entity capabilities with chat/chatStream ops ---
    has_entity_chat = draw(st.booleans())
    if has_entity_chat:
        ops = draw(st.lists(
            st.sampled_from(_entity_ops),
            min_size=1, max_size=4, unique=True,
        ).filter(lambda ops: "chat" in ops or "chatStream" in ops))
        layer["entityCapabilities"].append({
            "entityName": draw(_entity_name_st),
            "enabledOperations": ops,
        })

    # --- Chat: standalone operations with chat/chatStream actions ---
    has_standalone_chat = draw(st.booleans())
    if has_standalone_chat:
        actions = draw(st.lists(
            st.sampled_from(_standalone_actions),
            min_size=1, max_size=3, unique=True,
        ).filter(lambda a: "chat" in a or "chatStream" in a))
        layer["standaloneOperations"].append({
            "name": fresh_name(),
            "enabledActions": actions,
        })

    # --- Non-chat entity ops (no chat/chatStream) ---
    has_entity_no_chat = draw(st.booleans())
    if has_entity_no_chat:
        non_chat_ops = draw(st.lists(
            st.sampled_from(["search", "generate", "summarize", "classify"]),
            min_size=1, max_size=3, unique=True,
        ))
        layer["entityCapabilities"].append({
            "entityName": draw(_entity_name_st),
            "enabledOperations": non_chat_ops,
        })

    # --- Non-chat standalone ops ---
    has_standalone_no_chat = draw(st.booleans())
    if has_standalone_no_chat:
        non_chat_actions = draw(st.lists(
            st.sampled_from(["generate", "query"]),
            min_size=1, max_size=2, unique=True,
        ))
        layer["standaloneOperations"].append({
            "name": fresh_name(),
            "enabledActions": non_chat_actions,
        })

    # --- RAG sources ---
    has_rag = draw(st.booleans())
    if has_rag:
        enabled = draw(st.booleans())
        layer["ragSources"].append({
            "name": fresh_name(),
            "type": "semantic",
            "enabled": enabled,
        })

    # --- Evaluators ---
    has_evaluators = draw(st.booleans())
    if has_evaluators:
        layer["evaluators"].append({
            "name": fresh_name(),
            "type": "relevancy",
        })

    # --- Document ingestion ---
    has_ingestion = draw(st.booleans())
    if has_ingestion:
        layer["documentIngestion"] = {"enabled": draw(st.booleans())}

    # --- Document processing ---
    has_processing = draw(st.booleans())
    if has_processing:
        layer["documentProcessing"] = {"enabled": draw(st.booleans())}

    # --- Token budget ---
    has_budget = draw(st.booleans())
    if has_budget:
        layer["tokenBudget"] = {"enabled": draw(st.booleans())}

    # --- Audit log ---
    has_audit = draw(st.booleans())
    if has_audit:
        layer["auditLog"] = {"enabled": draw(st.booleans())}

    # --- Chat session cleanup + topic summarization ---
    has_cleanup = draw(st.booleans())
    if has_cleanup:
        cleanup_enabled = draw(st.booleans())
        cleanup: dict = {"enabled": cleanup_enabled}
        if draw(st.booleans()):
            cleanup["topicSummarization"] = {
                "enabled": draw(st.booleans()),
                "providerName": "gpt4",
            }
        layer["chatSessionCleanup"] = cleanup

    # --- Standalone state tables ---
    has_state_table = draw(st.booleans())
    if has_state_table:
        table_name = "ai_" + fresh_name() + "_state"
        num_cols = draw(st.integers(min_value=1, max_value=3))
        columns = []
        col_names_used: set[str] = set()
        for _ in range(num_cols):
            col_name = draw(_identifier_st.filter(lambda x: x not in col_names_used))
            col_names_used.add(col_name)
            col_type = draw(_col_type_st)
            col: dict = {"name": col_name, "type": col_type}
            if col_type == "VARCHAR":
                col["length"] = draw(st.integers(min_value=10, max_value=500))
            columns.append(col)

        layer["standaloneOperations"].append({
            "name": fresh_name(),
            "enabledActions": ["generate"],
            "stateTable": {
                "tableName": table_name,
                "columns": columns,
            },
        })

    return layer


# ---------------------------------------------------------------------------
# Helper — run generator and get SQL (or empty string)
# ---------------------------------------------------------------------------

def _generate_sql(ai_layer: dict) -> str:
    """Run the DDL generator and return the SQL content, or '' if nothing generated."""
    result = _GENERATOR.generate(ai_layer)
    if not result:
        return ""
    assert len(result) == 1
    return result[0][1]


# ---------------------------------------------------------------------------
# Helper — feature detection mirrors (same logic as AiDdlGenerator)
# ---------------------------------------------------------------------------

def _expect_chat(layer: dict) -> bool:
    return AiDdlGenerator._has_chat_operations(layer)

def _expect_rag(layer: dict) -> bool:
    return AiDdlGenerator._has_enabled_rag_sources(layer)

def _expect_evaluators(layer: dict) -> bool:
    return AiDdlGenerator._has_evaluators(layer)

def _expect_ingestion(layer: dict) -> bool:
    return AiDdlGenerator._has_document_ingestion(layer)

def _expect_processing(layer: dict) -> bool:
    return AiDdlGenerator._has_document_processing(layer)

def _expect_budget(layer: dict) -> bool:
    return AiDdlGenerator._has_token_budget(layer)

def _expect_audit(layer: dict) -> bool:
    return AiDdlGenerator._has_audit_log(layer)

def _expect_topics(layer: dict) -> bool:
    return AiDdlGenerator._has_topic_tables(layer)

def _expect_state_tables(layer: dict) -> list[dict]:
    return AiDdlGenerator._get_state_tables(layer)


# ===========================================================================
# Property 8: Conditional Code Generation
# ===========================================================================


@settings(max_examples=30, deadline=None)
@given(layer=random_ai_layer_st())
def test_chat_tables_iff_chat_operations(layer: dict) -> None:
    """Property 8: Chat tables generated iff chat/chatStream operations exist.

    **Validates: Requirements 4.23, 16.1, 16.2**
    """
    sql = _generate_sql(layer)
    expect = _expect_chat(layer)

    if expect:
        assert "ai_chat_session" in sql, "Chat ops enabled but ai_chat_session missing"
        assert "ai_chat_message" in sql, "Chat ops enabled but ai_chat_message missing"
    else:
        assert "ai_chat_session" not in sql, "No chat ops but ai_chat_session present"
        assert "ai_chat_message" not in sql, "No chat ops but ai_chat_message present"


@settings(max_examples=30, deadline=None)
@given(layer=random_ai_layer_st())
def test_rag_table_iff_rag_enabled(layer: dict) -> None:
    """Property 8: RAG document chunk table generated iff any RAG source enabled.

    **Validates: Requirements 8.7, 9.1, 9.4, 16.4, 16.5**
    """
    sql = _generate_sql(layer)
    expect = _expect_rag(layer)

    if expect:
        assert "ai_document_chunk" in sql, "RAG enabled but ai_document_chunk missing"
    else:
        assert "ai_document_chunk" not in sql, "RAG disabled but ai_document_chunk present"


@settings(max_examples=30, deadline=None)
@given(layer=random_ai_layer_st())
def test_evaluation_table_iff_evaluators_configured(layer: dict) -> None:
    """Property 8: Evaluation result table generated iff evaluators configured.

    **Validates: Requirements 10.3, 16.6, 16.7**
    """
    sql = _generate_sql(layer)
    expect = _expect_evaluators(layer)

    if expect:
        assert "ai_evaluation_result" in sql, "Evaluators configured but table missing"
    else:
        assert "ai_evaluation_result" not in sql, "No evaluators but table present"


@settings(max_examples=30, deadline=None)
@given(layer=random_ai_layer_st())
def test_ingestion_table_iff_ingestion_enabled(layer: dict) -> None:
    """Property 8: Ingested document table generated iff documentIngestion enabled.

    **Validates: Requirements 11.5, 11.10**
    """
    sql = _generate_sql(layer)
    expect = _expect_ingestion(layer)
    # Use CREATE TABLE marker to avoid false positives from FK references
    create_marker = "CREATE TABLE IF NOT EXISTS ai_ingested_document"

    if expect:
        assert create_marker in sql, "Ingestion enabled but table missing"
    else:
        assert create_marker not in sql, "Ingestion disabled but table present"


@settings(max_examples=30, deadline=None)
@given(layer=random_ai_layer_st())
def test_processing_table_iff_processing_enabled(layer: dict) -> None:
    """Property 8: Document task result table generated iff documentProcessing enabled.

    **Validates: Requirements 11.17**
    """
    sql = _generate_sql(layer)
    expect = _expect_processing(layer)

    if expect:
        assert "ai_document_task_result" in sql, "Processing enabled but table missing"
    else:
        assert "ai_document_task_result" not in sql, "Processing disabled but table present"


@settings(max_examples=30, deadline=None)
@given(layer=random_ai_layer_st())
def test_token_usage_table_iff_budget_enabled(layer: dict) -> None:
    """Property 8: Token usage table generated iff tokenBudget enabled.

    **Validates: Requirements 15.29**
    """
    sql = _generate_sql(layer)
    expect = _expect_budget(layer)

    if expect:
        assert "ai_token_usage" in sql, "Budget enabled but table missing"
    else:
        assert "ai_token_usage" not in sql, "Budget disabled but table present"


@settings(max_examples=30, deadline=None)
@given(layer=random_ai_layer_st())
def test_audit_table_iff_audit_enabled(layer: dict) -> None:
    """Property 8: Audit log table generated iff auditLog enabled.

    **Validates: Requirements 15.43**
    """
    sql = _generate_sql(layer)
    expect = _expect_audit(layer)

    if expect:
        assert "ai_audit_log" in sql, "Audit enabled but table missing"
    else:
        assert "ai_audit_log" not in sql, "Audit disabled but table present"


@settings(max_examples=30, deadline=None)
@given(layer=random_ai_layer_st())
def test_topic_tables_iff_cleanup_with_summarization(layer: dict) -> None:
    """Property 8: Topic tables generated iff chatSessionCleanup + topicSummarization enabled.

    **Validates: Requirements 4.23**
    """
    sql = _generate_sql(layer)
    expect = _expect_topics(layer)

    if expect:
        assert "ai_topic" in sql, "Topics enabled but ai_topic missing"
        assert "ai_user_topic_hit" in sql, "Topics enabled but ai_user_topic_hit missing"
        assert "ai_global_topic_hit" in sql, "Topics enabled but ai_global_topic_hit missing"
    else:
        assert "ai_user_topic_hit" not in sql, "Topics disabled but ai_user_topic_hit present"
        assert "ai_global_topic_hit" not in sql, "Topics disabled but ai_global_topic_hit present"


@settings(max_examples=30, deadline=None)
@given(layer=random_ai_layer_st())
def test_state_tables_iff_standalone_has_state_table(layer: dict) -> None:
    """Property 8: Standalone state tables generated iff stateTable configured.

    **Validates: Requirements 5.1, 5.8, 6.1, 16.3**
    """
    sql = _generate_sql(layer)
    expected_tables = _expect_state_tables(layer)

    for st_def in expected_tables:
        table_name = st_def["table_name"]
        assert table_name in sql, f"State table '{table_name}' expected but missing"

    # If no state tables expected, verify none of the ai_*_state patterns appear
    if not expected_tables:
        # No standalone state tables should be in the output
        # (other tables like ai_chat_session are not state tables)
        for op in layer.get("standaloneOperations", []):
            st = op.get("stateTable")
            if st:
                # This shouldn't happen if expected_tables is empty
                assert False, "Inconsistency: stateTable found but _get_state_tables returned empty"


@settings(max_examples=30, deadline=None, suppress_health_check=[HealthCheck.filter_too_much])
@given(layer=random_ai_layer_st())
def test_no_output_when_all_features_disabled(layer: dict) -> None:
    """Property 8: When no feature is enabled, zero DDL is generated.

    **Validates: Requirements 13.1, 13.4, 13.9, 13.34, 15.12**
    """
    # Only test layers where nothing is enabled
    any_enabled = (
        _expect_chat(layer)
        or _expect_rag(layer)
        or _expect_evaluators(layer)
        or _expect_ingestion(layer)
        or _expect_processing(layer)
        or _expect_budget(layer)
        or _expect_audit(layer)
        or _expect_topics(layer)
        or len(_expect_state_tables(layer)) > 0
    )
    assume(not any_enabled)

    result = _GENERATOR.generate(layer)
    assert result == [], "No features enabled but DDL was generated"


@settings(max_examples=30, deadline=None)
@given(layer=random_ai_layer_st())
def test_at_least_one_feature_produces_output(layer: dict) -> None:
    """Property 8: When at least one feature is enabled, DDL is generated.

    **Validates: Requirements 16.1–16.7**
    """
    any_enabled = (
        _expect_chat(layer)
        or _expect_rag(layer)
        or _expect_evaluators(layer)
        or _expect_ingestion(layer)
        or _expect_processing(layer)
        or _expect_budget(layer)
        or _expect_audit(layer)
        or _expect_topics(layer)
        or len(_expect_state_tables(layer)) > 0
    )
    assume(any_enabled)

    result = _GENERATOR.generate(layer)
    assert len(result) == 1, "Feature enabled but no DDL file generated"
    assert len(result[0][1]) > 0, "Feature enabled but DDL content is empty"
