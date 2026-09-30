"""Property-based tests for AiValidator — Schema Structure Validation.

**Validates: Requirements 1.1–1.25, 1.28**

# Feature: ai-layer, Property 1: Schema Structure Validation
"""

import sys
from pathlib import Path

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

# Ensure swfaw/ is on sys.path so imports resolve
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generators.ai_validator import AiValidator
from utils.definition_loader import DefinitionBundle


# ---------------------------------------------------------------------------
# Helpers — minimal DefinitionBundle fixture
# ---------------------------------------------------------------------------

def _make_bundle(entity_class_names: list[str] | None = None) -> DefinitionBundle:
    """Build a minimal DefinitionBundle with given entity class names."""
    entities = []
    if entity_class_names:
        for name in entity_class_names:
            entities.append({
                "tableName": name.lower() + "s",
                "className": name,
                "fields": [
                    {"columnName": "id", "fieldName": "id", "javaType": "Long"},
                ],
            })
    return DefinitionBundle(
        app_name="test_app",
        definitions_dir=Path("/tmp/fake"),
        manifest={"version": "2.5", "format": "split", "files": {}},
        project_metadata={"projectMetadata": {"database": {"name": "test_db"}}},
        entity_layer={"entities": entities},
        entities={"entities": []},
        relationships={"relationships": []},
        repository_layer={"repositories": []},
        service_layer={"services": []},
        controller_layer={"controllers": []},
        dto_layer={"dtos": []},
    )


# ---------------------------------------------------------------------------
# Strategies — building blocks
# ---------------------------------------------------------------------------

_provider_name_st = st.from_regex(r"[a-z][a-zA-Z0-9]{1,10}", fullmatch=True)
_entity_name_st = st.from_regex(r"[A-Z][a-zA-Z]{2,10}", fullmatch=True)
_identifier_st = st.from_regex(r"[a-z][a-zA-Z0-9]{1,10}", fullmatch=True)

_provider_type_st = st.sampled_from(["openai", "ollama"])
_temperature_st = st.floats(min_value=0.0, max_value=2.0, allow_nan=False)
_rag_type_st = st.sampled_from(["semantic", "heuristic"])
_evaluator_type_st = st.sampled_from(["relevancy", "correctness", "safety", "custom"])
_scoring_mechanism_st = st.sampled_from(["numeric", "pass_fail", "categorical"])
_evaluator_failure_action_st = st.sampled_from(["none", "warn"])
_moderation_failure_action_st = st.sampled_from(["block", "warn", "log"])

_valid_audit_events = [
    "orchestrator_request", "tool_invocation", "moderation_flag",
    "security_violation", "budget_exceeded", "session_created",
    "document_ingested", "provider_error", "circuit_breaker_state_change",
]


# ---------------------------------------------------------------------------
# Strategy — valid provider
# ---------------------------------------------------------------------------

def _valid_provider_st(name_st=None):
    """Strategy for a valid provider dict."""
    if name_st is None:
        name_st = _provider_name_st
    return st.fixed_dictionaries({
        "name": name_st,
        "type": _provider_type_st,
        "model": st.just("gpt-4"),
        "apiKeyEnvVar": st.just("OPENAI_API_KEY"),
        "temperature": _temperature_st,
        "supportedRoles": st.just(["system", "user", "assistant"]),
    })


# ---------------------------------------------------------------------------
# Strategy — valid minimal AI_Layer
# ---------------------------------------------------------------------------

@st.composite
def valid_ai_layer_st(draw):
    """Generate a valid minimal AI_Layer dict that passes AiValidator."""
    # Generate 1-3 providers with unique names
    num_providers = draw(st.integers(min_value=1, max_value=3))
    providers = []
    used_names = set()
    for _ in range(num_providers):
        name = draw(_provider_name_st.filter(lambda n: n not in used_names))
        used_names.add(name)
        provider = draw(_valid_provider_st(st.just(name)))
        providers.append(provider)

    provider_names = [p["name"] for p in providers]
    first_provider = provider_names[0]

    ai_layer = {
        "schemaVersion": "1.0",
        "providers": providers,
        "entityCapabilities": [],
        "standaloneOperations": [],
        "promptTemplates": [],
        "assistants": [],
        "ragSources": [],
        "evaluators": [],
    }

    # Optionally add evaluators (sync only, no retry for async)
    if draw(st.booleans()):
        ev_name = draw(_identifier_st.filter(lambda n: n not in used_names))
        used_names.add(ev_name)
        ev_type = draw(_evaluator_type_st)
        scoring = draw(_scoring_mechanism_st)
        evaluator = {
            "name": ev_name,
            "type": ev_type,
            "providerName": first_provider,
            "evaluationPrompt": "Evaluate: {{input}} -> {{output}}",
            "scoringMechanism": scoring,
            "failureAction": draw(_evaluator_failure_action_st),
            "mode": "sync",
        }
        # categorical scoring requires categories
        if scoring == "categorical":
            evaluator["categories"] = ["good", "bad"]
        ai_layer["evaluators"].append(evaluator)

    # Optionally add RAG sources
    if draw(st.booleans()):
        rs_name = draw(_identifier_st.filter(lambda n: n not in used_names))
        used_names.add(rs_name)
        rs_type = draw(_rag_type_st)
        rag_source = {
            "name": rs_name,
            "type": rs_type,
            "targets": [],
        }
        if rs_type == "semantic":
            rag_source["providerName"] = first_provider
        ai_layer["ragSources"].append(rag_source)

    # Optionally add orchestrator (required for mcpServers)
    if draw(st.booleans()):
        orch = {"providerName": first_provider}
        # Optionally add moderation
        if draw(st.booleans()):
            orch["moderation"] = {
                "providerName": first_provider,
                "failureAction": draw(_moderation_failure_action_st),
            }
        ai_layer["orchestrator"] = orch

    # Optionally add observability
    if draw(st.booleans()):
        obs = {"enabled": True}
        if draw(st.booleans()):
            obs["grafana"] = {
                "url": "http://grafana:3000",
                "apiKeyEnvVar": "GRAFANA_KEY",
            }
        # Add dashboards with non-empty panels
        if draw(st.booleans()):
            dash_name = draw(_identifier_st.filter(lambda n: n not in used_names))
            used_names.add(dash_name)
            obs["dashboards"] = [{
                "name": dash_name,
                "panels": [{"title": "Test", "metricName": "ai.requests", "type": "graph"}],
            }]
        ai_layer["observability"] = obs

    # Optionally add tokenBudget (providerOverrides must reference existing providers)
    if draw(st.booleans()):
        budget = {"enabled": True}
        if draw(st.booleans()):
            budget["providerOverrides"] = {
                first_provider: {"dailyLimit": 10000}
            }
        ai_layer["tokenBudget"] = budget

    # Optionally add chatSessionCleanup
    if draw(st.booleans()):
        cleanup = {"enabled": True}
        if draw(st.booleans()):
            cleanup["topicSummarization"] = {
                "enabled": True,
                "providerName": first_provider,
            }
        ai_layer["chatSessionCleanup"] = cleanup

    # Optionally add auditLog
    if draw(st.booleans()):
        num_events = draw(st.integers(min_value=0, max_value=3))
        events = draw(st.lists(
            st.sampled_from(_valid_audit_events),
            min_size=num_events,
            max_size=num_events,
            unique=True,
        ))
        ai_layer["auditLog"] = {"enabled": True, "loggedEvents": events}

    return ai_layer


# ---------------------------------------------------------------------------
# Mutation strategies — create invalid AI_Layer dicts
# ---------------------------------------------------------------------------

@st.composite
def ai_layer_wrong_schema_version_st(draw):
    """Valid AI_Layer but with wrong schemaVersion."""
    layer = draw(valid_ai_layer_st())
    bad_version = draw(st.text(min_size=1, max_size=10).filter(lambda v: v != "1.0"))
    layer["schemaVersion"] = bad_version
    return layer


@st.composite
def ai_layer_missing_schema_version_st(draw):
    """Valid AI_Layer but with schemaVersion removed."""
    layer = draw(valid_ai_layer_st())
    layer.pop("schemaVersion", None)
    return layer


@st.composite
def ai_layer_invalid_provider_type_st(draw):
    """AI_Layer with a provider that has an invalid type."""
    layer = draw(valid_ai_layer_st())
    assume(len(layer["providers"]) > 0)
    bad_type = draw(st.text(min_size=1, max_size=10).filter(
        lambda t: t not in ("openai", "ollama")
    ))
    layer["providers"][0]["type"] = bad_type
    return layer


@st.composite
def ai_layer_temperature_out_of_range_st(draw):
    """AI_Layer with a provider temperature outside 0.0-2.0."""
    layer = draw(valid_ai_layer_st())
    assume(len(layer["providers"]) > 0)
    bad_temp = draw(st.one_of(
        st.floats(min_value=2.01, max_value=100.0, allow_nan=False, allow_infinity=False),
        st.floats(min_value=-100.0, max_value=-0.01, allow_nan=False, allow_infinity=False),
    ))
    layer["providers"][0]["temperature"] = bad_temp
    return layer


@st.composite
def ai_layer_missing_user_role_st(draw):
    """AI_Layer with a provider whose supportedRoles doesn't include 'user'."""
    layer = draw(valid_ai_layer_st())
    assume(len(layer["providers"]) > 0)
    layer["providers"][0]["supportedRoles"] = ["system", "assistant"]
    return layer


@st.composite
def ai_layer_async_evaluator_retry_st(draw):
    """AI_Layer with an async evaluator that has failureAction 'retry'."""
    layer = draw(valid_ai_layer_st())
    provider_name = layer["providers"][0]["name"]
    layer["evaluators"] = [{
        "name": "bad_eval",
        "type": "relevancy",
        "providerName": provider_name,
        "evaluationPrompt": "test {{input}} {{output}}",
        "scoringMechanism": "numeric",
        "failureAction": "retry",
        "mode": "async",
    }]
    return layer


@st.composite
def ai_layer_invalid_audit_event_st(draw):
    """AI_Layer with an invalid audit log event type."""
    layer = draw(valid_ai_layer_st())
    bad_event = draw(st.text(min_size=1, max_size=20).filter(
        lambda e: e not in _valid_audit_events
    ))
    layer["auditLog"] = {"enabled": True, "loggedEvents": [bad_event]}
    return layer


@st.composite
def ai_layer_grafana_missing_url_st(draw):
    """AI_Layer with observability.grafana missing url."""
    layer = draw(valid_ai_layer_st())
    layer["observability"] = {
        "enabled": True,
        "grafana": {"apiKeyEnvVar": "GRAFANA_KEY"},
    }
    return layer


@st.composite
def ai_layer_grafana_missing_api_key_st(draw):
    """AI_Layer with observability.grafana missing apiKeyEnvVar."""
    layer = draw(valid_ai_layer_st())
    layer["observability"] = {
        "enabled": True,
        "grafana": {"url": "http://grafana:3000"},
    }
    return layer


@st.composite
def ai_layer_empty_dashboard_panels_st(draw):
    """AI_Layer with observability dashboard with empty panels."""
    layer = draw(valid_ai_layer_st())
    layer["observability"] = {
        "enabled": True,
        "dashboards": [{"name": "empty_dash", "panels": []}],
    }
    return layer


@st.composite
def ai_layer_semantic_rag_no_provider_st(draw):
    """AI_Layer with a semantic RAG source missing providerName."""
    layer = draw(valid_ai_layer_st())
    layer["ragSources"] = [{
        "name": "bad_rag",
        "type": "semantic",
        "targets": [],
    }]
    return layer


@st.composite
def ai_layer_token_budget_bad_provider_st(draw):
    """AI_Layer with tokenBudget.providerOverrides referencing nonexistent provider."""
    layer = draw(valid_ai_layer_st())
    existing_names = {p["name"] for p in layer["providers"]}
    bad_name = draw(_identifier_st.filter(lambda n: n not in existing_names))
    layer["tokenBudget"] = {
        "enabled": True,
        "providerOverrides": {bad_name: {"dailyLimit": 1000}},
    }
    return layer


@st.composite
def ai_layer_invalid_moderation_action_st(draw):
    """AI_Layer with orchestrator.moderation.failureAction invalid."""
    layer = draw(valid_ai_layer_st())
    provider_name = layer["providers"][0]["name"]
    bad_action = draw(st.text(min_size=1, max_size=10).filter(
        lambda a: a not in ("block", "warn", "log")
    ))
    layer["orchestrator"] = {
        "providerName": provider_name,
        "moderation": {
            "providerName": provider_name,
            "failureAction": bad_action,
        },
    }
    return layer


@st.composite
def ai_layer_categorical_no_categories_st(draw):
    """AI_Layer with categorical evaluator missing categories."""
    layer = draw(valid_ai_layer_st())
    provider_name = layer["providers"][0]["name"]
    layer["evaluators"] = [{
        "name": "cat_eval",
        "type": "custom",
        "providerName": provider_name,
        "evaluationPrompt": "test {{input}} {{output}}",
        "scoringMechanism": "categorical",
        "failureAction": "none",
        "mode": "sync",
    }]
    return layer


@st.composite
def ai_layer_duplicate_provider_names_st(draw):
    """AI_Layer with duplicate provider names."""
    layer = draw(valid_ai_layer_st())
    assume(len(layer["providers"]) > 0)
    # Duplicate the first provider
    dup = dict(layer["providers"][0])
    layer["providers"].append(dup)
    return layer


@st.composite
def ai_layer_mcp_without_orchestrator_st(draw):
    """AI_Layer with mcpServers but no orchestrator."""
    layer = draw(valid_ai_layer_st())
    layer.pop("orchestrator", None)
    layer["mcpServers"] = [{
        "name": "test_mcp",
        "transportType": "stdio",
        "requiredRoles": [],
    }]
    return layer


@st.composite
def ai_layer_doc_processing_without_ingestion_st(draw):
    """AI_Layer with documentProcessing enabled but documentIngestion disabled."""
    layer = draw(valid_ai_layer_st())
    layer["documentIngestion"] = {"enabled": False}
    layer["documentProcessing"] = {"enabled": True, "tasks": []}
    return layer


@st.composite
def ai_layer_cleanup_bad_provider_st(draw):
    """AI_Layer with chatSessionCleanup.topicSummarization referencing bad provider."""
    layer = draw(valid_ai_layer_st())
    existing_names = {p["name"] for p in layer["providers"]}
    bad_name = draw(_identifier_st.filter(lambda n: n not in existing_names))
    layer["chatSessionCleanup"] = {
        "enabled": True,
        "topicSummarization": {
            "enabled": True,
            "providerName": bad_name,
        },
    }
    return layer



# ---------------------------------------------------------------------------
# Property 1: Valid AI_Layer dicts pass validation
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(ai_layer=valid_ai_layer_st())
def test_valid_ai_layer_passes_validation(ai_layer: dict) -> None:
    """Property 1 (positive): Schema Structure Validation — valid case

    For any randomly generated AI_Layer dictionary with all required fields
    present, correct types, valid enum values, in-range numerics, and
    schemaVersion "1.0", AiValidator.validate() SHALL accept it without
    raising ValueError.

    **Validates: Requirements 1.1–1.18, 1.28**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    # Should not raise — returns warnings list
    warnings = validator.validate(ai_layer, bundle)
    assert isinstance(warnings, list)


# ---------------------------------------------------------------------------
# Property 1: Invalid AI_Layer dicts raise ValueError
# ---------------------------------------------------------------------------


@settings(max_examples=20)
@given(ai_layer=ai_layer_wrong_schema_version_st())
def test_wrong_schema_version_raises(ai_layer: dict) -> None:
    """Property 1 (negative): Wrong schemaVersion raises ValueError.

    **Validates: Requirement 1.28**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="schemaVersion"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_missing_schema_version_st())
def test_missing_schema_version_raises(ai_layer: dict) -> None:
    """Property 1 (negative): Missing schemaVersion raises ValueError.

    **Validates: Requirement 1.28**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="schemaVersion"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_invalid_provider_type_st())
def test_invalid_provider_type_raises(ai_layer: dict) -> None:
    """Property 1 (negative): Invalid provider type raises ValueError.

    **Validates: Requirement 1.2**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="type"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_temperature_out_of_range_st())
def test_temperature_out_of_range_raises(ai_layer: dict) -> None:
    """Property 1 (negative): Temperature outside 0.0-2.0 raises ValueError.

    **Validates: Requirement 1.2**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="temperature"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_missing_user_role_st())
def test_missing_user_role_raises(ai_layer: dict) -> None:
    """Property 1 (negative): Provider supportedRoles missing 'user' raises ValueError.

    **Validates: Requirement 1.2**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="user"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_async_evaluator_retry_st())
def test_async_evaluator_retry_raises(ai_layer: dict) -> None:
    """Property 1 (negative): Async evaluator with retry failureAction raises ValueError.

    **Validates: Requirement 1.8**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="retry"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_invalid_audit_event_st())
def test_invalid_audit_event_raises(ai_layer: dict) -> None:
    """Property 1 (negative): Invalid audit log event type raises ValueError.

    **Validates: Requirement 1.18**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="loggedEvents"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_grafana_missing_url_st())
def test_grafana_missing_url_raises(ai_layer: dict) -> None:
    """Property 1 (negative): Grafana without url raises ValueError.

    **Validates: Requirement 1.14**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="url"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_grafana_missing_api_key_st())
def test_grafana_missing_api_key_raises(ai_layer: dict) -> None:
    """Property 1 (negative): Grafana without apiKeyEnvVar raises ValueError.

    **Validates: Requirement 1.14**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="apiKeyEnvVar"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_empty_dashboard_panels_st())
def test_empty_dashboard_panels_raises(ai_layer: dict) -> None:
    """Property 1 (negative): Dashboard with empty panels raises ValueError.

    **Validates: Requirement 1.14**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="panels"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_semantic_rag_no_provider_st())
def test_semantic_rag_no_provider_raises(ai_layer: dict) -> None:
    """Property 1 (negative): Semantic RAG source without providerName raises ValueError.

    **Validates: Requirement 1.7**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="providerName"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_token_budget_bad_provider_st())
def test_token_budget_bad_provider_raises(ai_layer: dict) -> None:
    """Property 1 (negative): tokenBudget referencing nonexistent provider raises ValueError.

    **Validates: Requirement 1.16**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="providerOverrides"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_invalid_moderation_action_st())
def test_invalid_moderation_action_raises(ai_layer: dict) -> None:
    """Property 1 (negative): Invalid moderation failureAction raises ValueError.

    **Validates: Requirement 1.12**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="failureAction"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_categorical_no_categories_st())
def test_categorical_no_categories_raises(ai_layer: dict) -> None:
    """Property 1 (negative): Categorical evaluator without categories raises ValueError.

    **Validates: Requirement 1.8**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="categories"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_duplicate_provider_names_st())
def test_duplicate_provider_names_raises(ai_layer: dict) -> None:
    """Property 1 (negative): Duplicate provider names raises ValueError.

    **Validates: Requirement 1.2**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="[Dd]uplicate"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_mcp_without_orchestrator_st())
def test_mcp_without_orchestrator_raises(ai_layer: dict) -> None:
    """Property 1 (negative): mcpServers without orchestrator raises ValueError.

    **Validates: Requirement 1.13**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="orchestrator"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_doc_processing_without_ingestion_st())
def test_doc_processing_without_ingestion_raises(ai_layer: dict) -> None:
    """Property 1 (negative): documentProcessing without documentIngestion raises ValueError.

    **Validates: Requirement 1.10, 1.11**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="documentIngestion"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=20)
@given(ai_layer=ai_layer_cleanup_bad_provider_st())
def test_cleanup_bad_provider_raises(ai_layer: dict) -> None:
    """Property 1 (negative): chatSessionCleanup referencing bad provider raises ValueError.

    **Validates: Requirement 1.17**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="providerName"):
        validator.validate(ai_layer, bundle)


# ===========================================================================
# Property 2: Invalid JSON Rejection
# ===========================================================================
# **Validates: Requirements 1.26, 1.27**
#
# For any byte string that is not valid JSON, the Definition_Loader SHALL
# raise a ValueError with a descriptive error message when attempting to
# load it as webflux_ai_layer.json or react_ai_config.json.
# ===========================================================================

import json as _json
import tempfile

from utils.definition_loader import _load_json_file


def _is_valid_json(data: bytes) -> bool:
    """Return True if *data* can be decoded as valid JSON."""
    try:
        _json.loads(data)
        return True
    except Exception:
        return False


@settings(max_examples=30)
@given(raw=st.binary(min_size=0, max_size=512))
def test_invalid_json_bytes_rejected(raw: bytes) -> None:
    """Property 2: Invalid JSON Rejection — arbitrary byte strings.

    For any byte string that is NOT valid JSON, _load_json_file SHALL raise
    a ValueError with a descriptive error message containing the file path.

    **Validates: Requirements 1.26, 1.27**
    """
    assume(not _is_valid_json(raw))

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        tmp.write(raw)
        tmp_path = Path(tmp.name)

    try:
        with pytest.raises(ValueError, match="Invalid JSON in definition file"):
            _load_json_file(tmp_path)
    finally:
        tmp_path.unlink(missing_ok=True)


@settings(max_examples=30)
@given(raw=st.text(
    alphabet=st.characters(blacklist_categories=("Cs",)),
    min_size=1,
    max_size=256,
).filter(lambda t: not _is_valid_json(t.encode("utf-8"))))
def test_invalid_json_text_rejected(raw: str) -> None:
    """Property 2: Invalid JSON Rejection — arbitrary text strings.

    For any text string that is NOT valid JSON, _load_json_file SHALL raise
    a ValueError with a descriptive error message.

    **Validates: Requirements 1.26, 1.27**
    """
    with tempfile.NamedTemporaryFile(
        suffix=".json", mode="w", encoding="utf-8", delete=False
    ) as tmp:
        tmp.write(raw)
        tmp_path = Path(tmp.name)

    try:
        with pytest.raises(ValueError, match="Invalid JSON in definition file"):
            _load_json_file(tmp_path)
    finally:
        tmp_path.unlink(missing_ok=True)


# ===========================================================================
# Property 3: Cross-Reference Validation
# ===========================================================================
# **Validates: Requirements 1.29, 1.31, 11.27**
#
# For any AI_Layer definition containing a reference (provider name, entity
# name, assistant name, RAG source name, evaluator name, or MCP server name)
# that does not exist in the corresponding array, the AiValidator SHALL raise
# a ValueError identifying the broken reference.
# ===========================================================================


# ---------------------------------------------------------------------------
# Mutation strategies — break cross-references
# ---------------------------------------------------------------------------

@st.composite
def ai_layer_entity_cap_bad_provider_st(draw):
    """AI_Layer with entityCapabilities referencing nonexistent provider."""
    layer = draw(valid_ai_layer_st())
    existing_providers = {p["name"] for p in layer["providers"]}
    bad_provider = draw(_identifier_st.filter(lambda n: n not in existing_providers))
    # Need a real entity in the bundle for this test
    layer["entityCapabilities"] = [{
        "entityName": "TestEntity",
        "providerName": bad_provider,
        "enabledOperations": ["search"],
        "searchableFields": ["name"],
    }]
    return layer


@st.composite
def ai_layer_entity_cap_bad_entity_st(draw):
    """AI_Layer with entityCapabilities referencing nonexistent entity."""
    layer = draw(valid_ai_layer_st())
    first_provider = layer["providers"][0]["name"]
    bad_entity = draw(_entity_name_st)
    layer["entityCapabilities"] = [{
        "entityName": bad_entity,
        "providerName": first_provider,
        "enabledOperations": ["search"],
        "searchableFields": ["name"],
    }]
    return layer


@st.composite
def ai_layer_standalone_bad_provider_st(draw):
    """AI_Layer with standaloneOperations referencing nonexistent provider."""
    layer = draw(valid_ai_layer_st())
    existing_providers = {p["name"] for p in layer["providers"]}
    bad_provider = draw(_identifier_st.filter(lambda n: n not in existing_providers))
    layer["standaloneOperations"] = [{
        "name": "badOp",
        "type": "chat",
        "providerName": bad_provider,
        "basePath": "bad-op",
        "systemPrompt": "You are a helper.",
        "enabledActions": ["chat"],
    }]
    return layer


@st.composite
def ai_layer_standalone_bad_assistant_st(draw):
    """AI_Layer with standaloneOperations referencing nonexistent assistant."""
    layer = draw(valid_ai_layer_st())
    first_provider = layer["providers"][0]["name"]
    existing_assistants = {a["name"] for a in layer.get("assistants", [])}
    bad_assistant = draw(_identifier_st.filter(lambda n: n not in existing_assistants))
    layer["standaloneOperations"] = [{
        "name": "badOp",
        "type": "chat",
        "providerName": first_provider,
        "basePath": "bad-op",
        "systemPrompt": "You are a helper.",
        "enabledActions": ["chat"],
        "assistantName": bad_assistant,
    }]
    return layer


@st.composite
def ai_layer_evaluator_bad_provider_st(draw):
    """AI_Layer with evaluators referencing nonexistent provider."""
    layer = draw(valid_ai_layer_st())
    existing_providers = {p["name"] for p in layer["providers"]}
    bad_provider = draw(_identifier_st.filter(lambda n: n not in existing_providers))
    layer["evaluators"] = [{
        "name": "badEval",
        "type": "relevancy",
        "providerName": bad_provider,
        "evaluationPrompt": "test {{input}} {{output}}",
        "scoringMechanism": "numeric",
        "failureAction": "none",
        "mode": "sync",
    }]
    return layer


@st.composite
def ai_layer_entity_cap_bad_rag_source_st(draw):
    """AI_Layer with entityCapabilities.ragSourceNames referencing nonexistent RAG source."""
    layer = draw(valid_ai_layer_st())
    first_provider = layer["providers"][0]["name"]
    existing_rag = {r["name"] for r in layer.get("ragSources", [])}
    bad_rag = draw(_identifier_st.filter(lambda n: n not in existing_rag))
    # Use a real entity name that will be in the bundle
    layer["entityCapabilities"] = [{
        "entityName": "TestEntity",
        "providerName": first_provider,
        "enabledOperations": ["search"],
        "searchableFields": ["name"],
        "ragSourceNames": [bad_rag],
    }]
    return layer


@st.composite
def ai_layer_entity_cap_bad_evaluator_st(draw):
    """AI_Layer with entityCapabilities.evaluatorNames referencing nonexistent evaluator."""
    layer = draw(valid_ai_layer_st())
    first_provider = layer["providers"][0]["name"]
    existing_evals = {e["name"] for e in layer.get("evaluators", [])}
    bad_eval = draw(_identifier_st.filter(lambda n: n not in existing_evals))
    layer["entityCapabilities"] = [{
        "entityName": "TestEntity",
        "providerName": first_provider,
        "enabledOperations": ["search"],
        "searchableFields": ["name"],
        "evaluatorNames": [bad_eval],
    }]
    return layer


@st.composite
def ai_layer_orchestrator_bad_provider_st(draw):
    """AI_Layer with orchestrator referencing nonexistent provider."""
    layer = draw(valid_ai_layer_st())
    existing_providers = {p["name"] for p in layer["providers"]}
    bad_provider = draw(_identifier_st.filter(lambda n: n not in existing_providers))
    layer["orchestrator"] = {"providerName": bad_provider}
    return layer


@st.composite
def ai_layer_orchestrator_moderation_bad_provider_st(draw):
    """AI_Layer with orchestrator.moderation referencing nonexistent provider."""
    layer = draw(valid_ai_layer_st())
    first_provider = layer["providers"][0]["name"]
    existing_providers = {p["name"] for p in layer["providers"]}
    bad_provider = draw(_identifier_st.filter(lambda n: n not in existing_providers))
    layer["orchestrator"] = {
        "providerName": first_provider,
        "moderation": {
            "providerName": bad_provider,
            "failureAction": "block",
        },
    }
    return layer


@st.composite
def ai_layer_doc_ingestion_bad_rag_source_st(draw):
    """AI_Layer with documentIngestion.targetRagSourceName referencing nonexistent RAG source."""
    layer = draw(valid_ai_layer_st())
    existing_rag = {r["name"] for r in layer.get("ragSources", [])}
    bad_rag = draw(_identifier_st.filter(lambda n: n not in existing_rag))
    layer["documentIngestion"] = {
        "enabled": True,
        "targetRagSourceName": bad_rag,
    }
    return layer


@st.composite
def ai_layer_assistant_bad_provider_st(draw):
    """AI_Layer with assistants referencing nonexistent provider."""
    layer = draw(valid_ai_layer_st())
    existing_providers = {p["name"] for p in layer["providers"]}
    bad_provider = draw(_identifier_st.filter(lambda n: n not in existing_providers))
    layer["assistants"] = [{
        "name": "badAssistant",
        "systemPrompt": "You are a helper.",
        "providerName": bad_provider,
        "entityScope": [],
        "memoryWindowSize": 20,
    }]
    return layer


@st.composite
def ai_layer_standalone_bad_rag_source_st(draw):
    """AI_Layer with standaloneOperations.ragSourceNames referencing nonexistent RAG source."""
    layer = draw(valid_ai_layer_st())
    first_provider = layer["providers"][0]["name"]
    existing_rag = {r["name"] for r in layer.get("ragSources", [])}
    bad_rag = draw(_identifier_st.filter(lambda n: n not in existing_rag))
    layer["standaloneOperations"] = [{
        "name": "badOp",
        "type": "chat",
        "providerName": first_provider,
        "basePath": "bad-op",
        "systemPrompt": "You are a helper.",
        "enabledActions": ["chat"],
        "ragSourceNames": [bad_rag],
    }]
    return layer


@st.composite
def ai_layer_standalone_bad_evaluator_st(draw):
    """AI_Layer with standaloneOperations.evaluatorNames referencing nonexistent evaluator."""
    layer = draw(valid_ai_layer_st())
    first_provider = layer["providers"][0]["name"]
    existing_evals = {e["name"] for e in layer.get("evaluators", [])}
    bad_eval = draw(_identifier_st.filter(lambda n: n not in existing_evals))
    layer["standaloneOperations"] = [{
        "name": "badOp",
        "type": "chat",
        "providerName": first_provider,
        "basePath": "bad-op",
        "systemPrompt": "You are a helper.",
        "enabledActions": ["chat"],
        "evaluatorNames": [bad_eval],
    }]
    return layer


# ---------------------------------------------------------------------------
# Property 3: Cross-reference tests
# ---------------------------------------------------------------------------


@settings(max_examples=15)
@given(ai_layer=ai_layer_entity_cap_bad_provider_st())
def test_xref_entity_cap_bad_provider(ai_layer: dict) -> None:
    """Property 3: entityCapabilities referencing nonexistent provider raises ValueError.

    **Validates: Requirements 1.29, 1.31**
    """
    bundle = _make_bundle(["TestEntity"])
    validator = AiValidator()
    with pytest.raises(ValueError, match="not found in providers"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=15)
@given(ai_layer=ai_layer_entity_cap_bad_entity_st())
def test_xref_entity_cap_bad_entity(ai_layer: dict) -> None:
    """Property 3: entityCapabilities referencing nonexistent entity raises ValueError.

    **Validates: Requirements 1.29, 1.31**
    """
    # Empty bundle — no entities defined
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="not found in entity_layer"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=15)
@given(ai_layer=ai_layer_standalone_bad_provider_st())
def test_xref_standalone_bad_provider(ai_layer: dict) -> None:
    """Property 3: standaloneOperations referencing nonexistent provider raises ValueError.

    **Validates: Requirements 1.29, 1.31**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="not found in providers"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=15)
@given(ai_layer=ai_layer_standalone_bad_assistant_st())
def test_xref_standalone_bad_assistant(ai_layer: dict) -> None:
    """Property 3: standaloneOperations referencing nonexistent assistant raises ValueError.

    **Validates: Requirements 1.29, 1.31**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="not found in assistants"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=15)
@given(ai_layer=ai_layer_evaluator_bad_provider_st())
def test_xref_evaluator_bad_provider(ai_layer: dict) -> None:
    """Property 3: evaluators referencing nonexistent provider raises ValueError.

    **Validates: Requirements 1.29, 1.31**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="not found in providers"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=15)
@given(ai_layer=ai_layer_entity_cap_bad_rag_source_st())
def test_xref_entity_cap_bad_rag_source(ai_layer: dict) -> None:
    """Property 3: entityCapabilities.ragSourceNames referencing nonexistent RAG source raises ValueError.

    **Validates: Requirements 1.29, 1.31**
    """
    bundle = _make_bundle(["TestEntity"])
    validator = AiValidator()
    with pytest.raises(ValueError, match="not found in ragSources"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=15)
@given(ai_layer=ai_layer_entity_cap_bad_evaluator_st())
def test_xref_entity_cap_bad_evaluator(ai_layer: dict) -> None:
    """Property 3: entityCapabilities.evaluatorNames referencing nonexistent evaluator raises ValueError.

    **Validates: Requirements 1.29, 1.31**
    """
    bundle = _make_bundle(["TestEntity"])
    validator = AiValidator()
    with pytest.raises(ValueError, match="not found in evaluators"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=15)
@given(ai_layer=ai_layer_orchestrator_bad_provider_st())
def test_xref_orchestrator_bad_provider(ai_layer: dict) -> None:
    """Property 3: orchestrator referencing nonexistent provider raises ValueError.

    **Validates: Requirements 1.29, 1.31**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="not found in providers"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=15)
@given(ai_layer=ai_layer_orchestrator_moderation_bad_provider_st())
def test_xref_orchestrator_moderation_bad_provider(ai_layer: dict) -> None:
    """Property 3: orchestrator.moderation referencing nonexistent provider raises ValueError.

    **Validates: Requirements 1.29, 1.31**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="not found in providers"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=15)
@given(ai_layer=ai_layer_doc_ingestion_bad_rag_source_st())
def test_xref_doc_ingestion_bad_rag_source(ai_layer: dict) -> None:
    """Property 3: documentIngestion.targetRagSourceName referencing nonexistent RAG source raises ValueError.

    **Validates: Requirements 1.29, 11.27**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="not found in ragSources"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=15)
@given(ai_layer=ai_layer_assistant_bad_provider_st())
def test_xref_assistant_bad_provider(ai_layer: dict) -> None:
    """Property 3: assistants referencing nonexistent provider raises ValueError.

    **Validates: Requirements 1.29, 1.31**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="not found in providers"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=15)
@given(ai_layer=ai_layer_standalone_bad_rag_source_st())
def test_xref_standalone_bad_rag_source(ai_layer: dict) -> None:
    """Property 3: standaloneOperations.ragSourceNames referencing nonexistent RAG source raises ValueError.

    **Validates: Requirements 1.29, 1.31**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="not found in ragSources"):
        validator.validate(ai_layer, bundle)


@settings(max_examples=15)
@given(ai_layer=ai_layer_standalone_bad_evaluator_st())
def test_xref_standalone_bad_evaluator(ai_layer: dict) -> None:
    """Property 3: standaloneOperations.evaluatorNames referencing nonexistent evaluator raises ValueError.

    **Validates: Requirements 1.29, 1.31**
    """
    bundle = _make_bundle()
    validator = AiValidator()
    with pytest.raises(ValueError, match="not found in evaluators"):
        validator.validate(ai_layer, bundle)
