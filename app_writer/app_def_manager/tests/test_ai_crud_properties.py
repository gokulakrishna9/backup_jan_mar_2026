"""Property-based tests for AiCRUDManager.

**Property 11: CRUD Operations Preserve Definition Validity**

For any valid AI_Layer definition and any sequence of valid CRUD operations
(add_provider, remove_provider, add_ai_capability, etc.), the resulting
definition SHALL still pass AiValidator validation. CRUD operations that
would create invalid states (e.g., removing a provider referenced by an
entity capability) SHALL raise ValueError before modifying the definition.

**Validates: Requirements 17.9–17.35**
"""

import json
import os
import sys
import tempfile
from pathlib import Path

from hypothesis import given, settings, assume, note
from hypothesis import strategies as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_def_manager.scaffolder import Scaffolder
from app_def_manager.ai_crud import AiCRUDManager, AI_LAYER_FILE


# --- Strategies ---

_provider_name_st = st.from_regex(r"[a-z][a-zA-Z]{2,8}", fullmatch=True)
_entity_name_st = st.from_regex(r"[A-Z][a-zA-Z]{2,8}", fullmatch=True)
_provider_type_st = st.sampled_from(["openai", "ollama"])
_model_st = st.sampled_from(["gpt-4", "gpt-3.5-turbo", "llama2", "mistral"])
_operation_st = st.sampled_from(["search", "generate", "summarize", "classify", "chat"])
_enabled_ops_st = st.lists(_operation_st, min_size=1, max_size=3, unique=True)
_eval_type_st = st.sampled_from(["relevancy", "correctness", "safety", "custom"])
_scoring_st = st.sampled_from(["numeric", "pass_fail", "categorical"])

_entity_desc_st = st.fixed_dictionaries({
    "name": _entity_name_st,
    "fields": st.just([{"name": "title", "type": "String"}]),
})

_initial_entities_st = st.lists(
    _entity_desc_st, min_size=1, max_size=2, unique_by=lambda e: e["name"]
)


def _scaffold_app(tmp_dir: str, entities: list[dict]) -> Path:
    """Scaffold an app in a temp directory and return the app_dir."""
    os.chdir(tmp_dir)
    scaffolder = Scaffolder()
    return scaffolder.scaffold_application("test_app", entities, force=True)


def _load_ai_layer(app_dir: Path) -> dict:
    return json.loads((app_dir / AI_LAYER_FILE).read_text(encoding="utf-8"))


def _validate_ai_layer(ai_layer: dict) -> bool:
    """Validate the AI layer definition is structurally sound.

    Returns True if valid, raises on critical issues.
    Checks: schemaVersion, no duplicate names, provider refs valid,
    evaluator refs valid, RAG source refs valid.
    """
    assert ai_layer.get("schemaVersion") == "1.0"
    # Check no duplicate provider names
    provider_names = [p["name"] for p in ai_layer.get("providers", [])]
    assert len(provider_names) == len(set(provider_names)), "Duplicate provider names"
    pn_set = set(provider_names)

    # Check entity capabilities reference valid providers
    for cap in ai_layer.get("entityCapabilities", []):
        assert cap["providerName"] in pn_set, f"Invalid provider ref: {cap['providerName']}"
        for en in cap.get("evaluatorNames", []):
            eval_names = {e["name"] for e in ai_layer.get("evaluators", [])}
            assert en in eval_names, f"Invalid evaluator ref: {en}"
        for rn in cap.get("ragSourceNames", []):
            rag_names = {r["name"] for r in ai_layer.get("ragSources", [])}
            assert rn in rag_names, f"Invalid RAG source ref: {rn}"

    # Check standalone operations reference valid providers
    for op in ai_layer.get("standaloneOperations", []):
        assert op["providerName"] in pn_set, f"Invalid provider ref: {op['providerName']}"

    # Check assistants reference valid providers
    for a in ai_layer.get("assistants", []):
        assert a["providerName"] in pn_set, f"Invalid provider ref: {a['providerName']}"

    # Check evaluators reference valid providers
    for e in ai_layer.get("evaluators", []):
        assert e["providerName"] in pn_set, f"Invalid provider ref: {e['providerName']}"

    # Check RAG sources reference valid providers (semantic only)
    for r in ai_layer.get("ragSources", []):
        if r["type"] == "semantic":
            assert r.get("providerName") in pn_set, f"Invalid provider ref: {r.get('providerName')}"

    # Check orchestrator references valid provider
    orch = ai_layer.get("orchestrator")
    if orch:
        assert orch["providerName"] in pn_set
        mod = orch.get("moderation")
        if mod:
            assert mod["providerName"] in pn_set

    # Check documentProcessing requires documentIngestion
    if ai_layer.get("documentProcessing"):
        assert ai_layer.get("documentIngestion"), "documentProcessing requires documentIngestion"

    # Check mcpServers requires orchestrator
    if ai_layer.get("mcpServers"):
        assert ai_layer.get("orchestrator"), "mcpServers requires orchestrator"

    # Check token budget provider overrides
    tb = ai_layer.get("tokenBudget")
    if tb:
        for pn in (tb.get("providerOverrides") or {}):
            assert pn in pn_set, f"Invalid provider override ref: {pn}"

    # Check topic summarization provider
    cleanup = ai_layer.get("chatSessionCleanup")
    if cleanup:
        ts = cleanup.get("topicSummarization")
        if ts:
            assert ts["providerName"] in pn_set

    return True


# --- Property 11: CRUD add/remove provider preserves validity ---

@settings(max_examples=30)
@given(
    initial_entities=_initial_entities_st,
    provider_name=_provider_name_st,
    provider_type=_provider_type_st,
    model=_model_st,
)
def test_add_remove_provider_preserves_validity(
    initial_entities, provider_name, provider_type, model
):
    """Property 11: Adding then removing a provider preserves definition validity.

    **Validates: Requirements 17.9, 17.34, 17.35**
    """
    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            app_dir = _scaffold_app(tmp, initial_entities)
            crud = AiCRUDManager("test_app")

            # Add provider
            dirty = crud.add_provider(provider_name, provider_type, model)
            assert AI_LAYER_FILE in dirty

            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)
            assert any(p["name"] == provider_name for p in data["providers"])

            # Remove provider
            dirty = crud.remove_provider(provider_name)
            assert AI_LAYER_FILE in dirty

            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)
            assert not any(p["name"] == provider_name for p in data["providers"])

        finally:
            os.chdir(original_cwd)


# --- Property 11: CRUD add entity capability with valid refs ---

@settings(max_examples=30)
@given(
    initial_entities=_initial_entities_st,
    provider_name=_provider_name_st,
    provider_type=_provider_type_st,
    model=_model_st,
    entity_name=_entity_name_st,
    enabled_ops=_enabled_ops_st,
)
def test_add_remove_capability_preserves_validity(
    initial_entities, provider_name, provider_type, model,
    entity_name, enabled_ops
):
    """Property 11: Adding then removing an entity capability preserves validity.

    **Validates: Requirements 17.10, 17.34, 17.35**
    """
    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            app_dir = _scaffold_app(tmp, initial_entities)
            crud = AiCRUDManager("test_app")

            # Add provider first
            crud.add_provider(provider_name, provider_type, model)

            # Add capability
            dirty = crud.add_ai_capability(entity_name, provider_name, enabled_ops)
            assert AI_LAYER_FILE in dirty

            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)

            # Remove capability
            crud.remove_ai_capability(entity_name)
            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)

            # Now safe to remove provider
            crud.remove_provider(provider_name)
            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)

        finally:
            os.chdir(original_cwd)


# --- Property 11: Removing provider with dependents raises ValueError ---

@settings(max_examples=30)
@given(
    initial_entities=_initial_entities_st,
    provider_name=_provider_name_st,
    provider_type=_provider_type_st,
    model=_model_st,
    entity_name=_entity_name_st,
)
def test_remove_provider_with_dependents_raises(
    initial_entities, provider_name, provider_type, model, entity_name
):
    """Property 11: Removing a provider referenced by a capability raises ValueError.

    **Validates: Requirements 17.9, 17.35**
    """
    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            app_dir = _scaffold_app(tmp, initial_entities)
            crud = AiCRUDManager("test_app")

            crud.add_provider(provider_name, provider_type, model)
            crud.add_ai_capability(entity_name, provider_name, ["search"])

            import pytest
            with pytest.raises(ValueError, match="Cannot remove provider"):
                crud.remove_provider(provider_name)

            # Definition should still be valid (unchanged)
            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)

        finally:
            os.chdir(original_cwd)


# --- Property 11: Full CRUD sequence preserves validity ---

@settings(max_examples=30)
@given(
    initial_entities=_initial_entities_st,
    prov1_name=_provider_name_st,
    prov2_name=_provider_name_st,
    prov_type=_provider_type_st,
    model=_model_st,
    entity_name=_entity_name_st,
    eval_name=_provider_name_st,
    eval_type=_eval_type_st,
    scoring=_scoring_st,
)
def test_full_crud_sequence_preserves_validity(
    initial_entities, prov1_name, prov2_name, prov_type, model,
    entity_name, eval_name, eval_type, scoring
):
    """Property 11: A full sequence of CRUD operations preserves definition validity.

    Sequence: add providers → add evaluator → add capability with evaluator →
    add orchestrator → add MCP server → set token budget → set audit log →
    set session cleanup → remove in reverse order.

    **Validates: Requirements 17.9–17.35**
    """
    assume(prov1_name != prov2_name)
    assume(prov1_name != eval_name)
    assume(prov2_name != eval_name)

    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            app_dir = _scaffold_app(tmp, initial_entities)
            crud = AiCRUDManager("test_app")

            # Add two providers
            crud.add_provider(prov1_name, prov_type, model)
            crud.add_provider(prov2_name, prov_type, model)
            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)

            # Add evaluator
            crud.add_evaluator(eval_name, eval_type, prov1_name,
                               "Evaluate: {{input}} {{output}}", scoring)
            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)

            # Add capability with evaluator
            crud.add_ai_capability(entity_name, prov1_name, ["search"],
                                    evaluatorNames=[eval_name])
            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)

            # Add orchestrator
            crud.set_orchestrator(prov2_name)
            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)

            # Add MCP server (requires orchestrator)
            crud.add_mcp_server("test_mcp", "stdio", ["ADMIN"])
            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)

            # Set token budget
            crud.set_token_budget(enabled=True, defaultDailyLimitPerUser=10000,
                                   providerOverrides={prov1_name: {"dailyLimit": 5000}})
            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)

            # Set audit log
            crud.set_audit_log(enabled=True, loggedEvents=["orchestrator_request", "tool_invocation"])
            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)

            # Set session cleanup
            crud.set_chat_session_cleanup(enabled=True)
            crud.set_topic_summarization(True, prov1_name, 5)
            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)

            # Set rate limiting
            crud.set_rate_limiting(30, {"entity": 50, "standalone": 40})
            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)

            # Set observability
            crud.set_observability(enabled=True)
            crud.add_observability_dashboard("test_dash",
                                              [{"title": "Requests", "metricName": "ai.requests", "type": "graph"}])
            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)

            # --- Reverse teardown ---
            crud.remove_observability_dashboard("test_dash")
            crud.remove_observability()
            crud.remove_rate_limiting()
            crud.remove_topic_summarization()
            crud.remove_chat_session_cleanup()
            crud.remove_audit_log()
            crud.remove_token_budget()
            crud.remove_mcp_server("test_mcp")
            crud.remove_orchestrator()
            crud.remove_ai_capability(entity_name)
            crud.remove_evaluator(eval_name)
            crud.remove_provider(prov2_name)
            crud.remove_provider(prov1_name)

            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)
            # Should be back to empty state
            assert len(data["providers"]) == 0
            assert len(data.get("entityCapabilities", [])) == 0
            assert len(data.get("evaluators", [])) == 0

        finally:
            os.chdir(original_cwd)


# --- Property 11: Removing evaluator with dependents raises ValueError ---

@settings(max_examples=30)
@given(
    initial_entities=_initial_entities_st,
    provider_name=_provider_name_st,
    provider_type=_provider_type_st,
    model=_model_st,
    entity_name=_entity_name_st,
    eval_name=_provider_name_st,
)
def test_remove_evaluator_with_dependents_raises(
    initial_entities, provider_name, provider_type, model,
    entity_name, eval_name
):
    """Property 11: Removing an evaluator referenced by a capability raises ValueError.

    **Validates: Requirements 17.15, 17.35**
    """
    assume(provider_name != eval_name)

    with tempfile.TemporaryDirectory() as tmp:
        original_cwd = os.getcwd()
        try:
            app_dir = _scaffold_app(tmp, initial_entities)
            crud = AiCRUDManager("test_app")

            crud.add_provider(provider_name, provider_type, model)
            crud.add_evaluator(eval_name, "relevancy", provider_name,
                               "Evaluate: {{input}} {{output}}", "numeric")
            crud.add_ai_capability(entity_name, provider_name, ["search"],
                                    evaluatorNames=[eval_name])

            import pytest
            with pytest.raises(ValueError, match="Cannot remove evaluator"):
                crud.remove_evaluator(eval_name)

            data = _load_ai_layer(app_dir)
            _validate_ai_layer(data)

        finally:
            os.chdir(original_cwd)
