"""AiCRUDManager — CRUD operations on AI layer definition files.

All methods validate cross-references, mark definition files dirty via
StatusTracker, and raise ValueError for invalid operations.

Requirements: 17.9–17.35
"""

import json
from pathlib import Path

from app_def_manager.status_tracker import StatusTracker

AI_LAYER_FILE = "webflux_ai_layer.json"
REACT_AI_FILE = "react_ai_config.json"

VALID_PROVIDER_TYPES = {"openai", "ollama"}
VALID_EVALUATOR_TYPES = {"relevancy", "correctness", "safety", "custom"}
VALID_SCORING_MECHANISMS = {"numeric", "pass_fail", "categorical"}
VALID_EVALUATOR_MODES = {"sync", "async"}
VALID_FAILURE_ACTIONS = {"none", "retry", "warn"}
VALID_RAG_TYPES = {"semantic", "heuristic"}
VALID_SECURITY_MODES = {"public", "role_restricted"}
VALID_VECTOR_STORE_TYPES = {"milvus", "qdrant", "pgvector", "in_memory"}
VALID_MCP_TRANSPORT_TYPES = {"stdio", "sse"}
VALID_ENFORCEMENT_ACTIONS = {"block", "warn", "log"}
VALID_MODERATION_FAILURE_ACTIONS = {"block", "warn", "log"}
VALID_AUDIT_EVENTS = {
    "orchestrator_request", "tool_invocation", "moderation_flag",
    "security_violation", "budget_exceeded", "session_created",
    "document_ingested", "provider_error", "circuit_breaker_state_change",
}
VALID_STANDALONE_TYPES = {"chat", "generate", "query", "workflow"}
VALID_RATE_LIMIT_CATEGORIES = {
    "entity", "standalone", "rag", "evaluations",
    "documentIngestion", "documentProcessing", "orchestrator", "observability",
}


def _load_ai_layer(app_dir: Path) -> dict:
    """Load webflux_ai_layer.json from app directory."""
    path = app_dir / AI_LAYER_FILE
    if not path.exists():
        raise FileNotFoundError(f"AI layer file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _save_ai_layer(app_dir: Path, data: dict) -> None:
    """Save webflux_ai_layer.json to app directory."""
    path = app_dir / AI_LAYER_FILE
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _load_react_ai(app_dir: Path) -> dict:
    """Load react_ai_config.json from app directory."""
    path = app_dir / REACT_AI_FILE
    if not path.exists():
        raise FileNotFoundError(f"React AI config file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _save_react_ai(app_dir: Path, data: dict) -> None:
    """Save react_ai_config.json to app directory."""
    path = app_dir / REACT_AI_FILE
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


class AiCRUDManager:
    """CRUD operations on AI layer definition files with cross-reference validation."""

    def __init__(self, app_name: str):
        self.app_dir = Path("application_definitions") / app_name
        if not self.app_dir.exists():
            raise FileNotFoundError(f"Application '{app_name}' not found")
        self.status = StatusTracker(self.app_dir)

    def _load(self) -> dict:
        return _load_ai_layer(self.app_dir)

    def _save(self, data: dict) -> None:
        _save_ai_layer(self.app_dir, data)
        self.status.mark_dirty([AI_LAYER_FILE])

    def _provider_names(self, data: dict) -> set[str]:
        return {p["name"] for p in data.get("providers", [])}

    def _find_provider_dependents(self, data: dict, provider_name: str) -> list[str]:
        """Find all sections referencing a provider name."""
        deps = []
        for cap in data.get("entityCapabilities", []):
            if cap.get("providerName") == provider_name:
                deps.append(f"entityCapability '{cap['entityName']}'")
        for op in data.get("standaloneOperations", []):
            if op.get("providerName") == provider_name:
                deps.append(f"standaloneOperation '{op['name']}'")
        for a in data.get("assistants", []):
            if a.get("providerName") == provider_name:
                deps.append(f"assistant '{a['name']}'")
        for r in data.get("ragSources", []):
            if r.get("providerName") == provider_name:
                deps.append(f"ragSource '{r['name']}'")
        for e in data.get("evaluators", []):
            if e.get("providerName") == provider_name:
                deps.append(f"evaluator '{e['name']}'")
        orch = data.get("orchestrator")
        if orch and orch.get("providerName") == provider_name:
            deps.append("orchestrator")
        if orch:
            mod = orch.get("moderation")
            if mod and mod.get("providerName") == provider_name:
                deps.append("orchestrator.moderation")
        dp = data.get("documentProcessing")
        if dp:
            if dp.get("defaultProviderName") == provider_name:
                deps.append("documentProcessing.defaultProviderName")
            for t in dp.get("tasks", []):
                if t.get("providerName") == provider_name:
                    deps.append(f"documentProcessing.task '{t['name']}'")
        tb = data.get("tokenBudget")
        if tb and provider_name in (tb.get("providerOverrides") or {}):
            deps.append("tokenBudget.providerOverrides")
        cleanup = data.get("chatSessionCleanup")
        if cleanup:
            ts = cleanup.get("topicSummarization")
            if ts and ts.get("providerName") == provider_name:
                deps.append("chatSessionCleanup.topicSummarization")
        return deps

    # ── Provider CRUD (Req 17.9) ────────────────────────────────────────

    def add_provider(self, name: str, type: str, model: str,
                     api_key_env_var: str = "OPENAI_API_KEY",
                     **kwargs) -> list[str]:
        """Add a provider to the AI layer definition."""
        if type not in VALID_PROVIDER_TYPES:
            raise ValueError(f"Invalid provider type '{type}'. Must be one of {VALID_PROVIDER_TYPES}")
        data = self._load()
        if name in self._provider_names(data):
            raise ValueError(f"Provider '{name}' already exists")
        provider = {
            "name": name,
            "type": type,
            "model": model,
            "apiKeyEnvVar": api_key_env_var,
            "temperature": kwargs.get("temperature", 0.7),
            "maxTokens": kwargs.get("max_tokens", 2048),
        }
        for key in ("embeddingModel", "baseUrl", "chatOptions", "supportedParameters",
                     "parameterFallbacks", "supportedRoles", "roleFallbacks", "resilience"):
            if key in kwargs:
                provider[key] = kwargs[key]
        data["providers"].append(provider)
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_provider(self, name: str) -> list[str]:
        """Remove a provider. Raises ValueError if dependencies exist."""
        data = self._load()
        deps = self._find_provider_dependents(data, name)
        if deps:
            raise ValueError(f"Cannot remove provider '{name}': referenced by {', '.join(deps)}")
        original_len = len(data["providers"])
        data["providers"] = [p for p in data["providers"] if p["name"] != name]
        if len(data["providers"]) == original_len:
            raise ValueError(f"Provider '{name}' not found")
        self._save(data)
        return [AI_LAYER_FILE]

    def modify_provider(self, name: str, **updates) -> list[str]:
        """Modify provider properties."""
        data = self._load()
        provider = next((p for p in data["providers"] if p["name"] == name), None)
        if not provider:
            raise ValueError(f"Provider '{name}' not found")
        if "type" in updates and updates["type"] not in VALID_PROVIDER_TYPES:
            raise ValueError(f"Invalid provider type '{updates['type']}'")
        for key, val in updates.items():
            provider[key] = val
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Entity Capability CRUD (Req 17.10) ──────────────────────────────

    def add_ai_capability(self, entity_name: str, provider_name: str,
                          enabled_operations: list[str], **kwargs) -> list[str]:
        """Add an entity AI capability."""
        data = self._load()
        if provider_name not in self._provider_names(data):
            raise ValueError(f"Provider '{provider_name}' not found")
        existing = {c["entityName"] for c in data.get("entityCapabilities", [])}
        if entity_name in existing:
            raise ValueError(f"Entity capability for '{entity_name}' already exists")
        cap = {
            "entityName": entity_name,
            "providerName": provider_name,
            "enabledOperations": enabled_operations,
        }
        for key in ("searchableFields", "evaluatorNames", "chatOptions",
                     "rolePromptSequence", "responseType", "ragSourceNames"):
            if key in kwargs:
                cap[key] = kwargs[key]
        # Validate evaluator refs
        if "evaluatorNames" in cap:
            eval_names = {e["name"] for e in data.get("evaluators", [])}
            for en in cap["evaluatorNames"]:
                if en not in eval_names:
                    raise ValueError(f"Evaluator '{en}' not found")
        # Validate RAG source refs
        if "ragSourceNames" in cap:
            rag_names = {r["name"] for r in data.get("ragSources", [])}
            for rn in cap["ragSourceNames"]:
                if rn not in rag_names:
                    raise ValueError(f"RAG source '{rn}' not found")
        data.setdefault("entityCapabilities", []).append(cap)
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_ai_capability(self, entity_name: str) -> list[str]:
        """Remove an entity AI capability."""
        data = self._load()
        original_len = len(data.get("entityCapabilities", []))
        data["entityCapabilities"] = [
            c for c in data.get("entityCapabilities", [])
            if c["entityName"] != entity_name
        ]
        if len(data["entityCapabilities"]) == original_len:
            raise ValueError(f"Entity capability for '{entity_name}' not found")
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Prompt Template CRUD (Req 17.11) ────────────────────────────────

    def add_prompt_template(self, name: str, operation: str, template: str,
                            **kwargs) -> list[str]:
        """Add a prompt template."""
        data = self._load()
        existing = {t["name"] for t in data.get("promptTemplates", [])}
        if name in existing:
            raise ValueError(f"Prompt template '{name}' already exists")
        entry = {"name": name, "operation": operation, "template": template}
        for key in ("entityName", "targetRole"):
            if key in kwargs:
                entry[key] = kwargs[key]
        data.setdefault("promptTemplates", []).append(entry)
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_prompt_template(self, name: str) -> list[str]:
        """Remove a prompt template."""
        data = self._load()
        original_len = len(data.get("promptTemplates", []))
        data["promptTemplates"] = [
            t for t in data.get("promptTemplates", []) if t["name"] != name
        ]
        if len(data["promptTemplates"]) == original_len:
            raise ValueError(f"Prompt template '{name}' not found")
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Assistant CRUD (Req 17.12) ──────────────────────────────────────

    def add_assistant(self, name: str, system_prompt: str, provider_name: str,
                      entity_scope: str, **kwargs) -> list[str]:
        """Add an assistant."""
        data = self._load()
        if provider_name not in self._provider_names(data):
            raise ValueError(f"Provider '{provider_name}' not found")
        existing = {a["name"] for a in data.get("assistants", [])}
        if name in existing:
            raise ValueError(f"Assistant '{name}' already exists")
        assistant = {
            "name": name,
            "systemPrompt": system_prompt,
            "providerName": provider_name,
            "entityScope": entity_scope,
            "memoryWindowSize": kwargs.get("memoryWindowSize", 20),
        }
        for key in ("rolePromptSequence", "sessionTtlDays", "chatOptions"):
            if key in kwargs:
                assistant[key] = kwargs[key]
        data.setdefault("assistants", []).append(assistant)
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_assistant(self, name: str) -> list[str]:
        """Remove an assistant. Checks for dependent standalone operations."""
        data = self._load()
        deps = [
            f"standaloneOperation '{op['name']}'"
            for op in data.get("standaloneOperations", [])
            if op.get("assistantName") == name
        ]
        if deps:
            raise ValueError(f"Cannot remove assistant '{name}': referenced by {', '.join(deps)}")
        original_len = len(data.get("assistants", []))
        data["assistants"] = [a for a in data.get("assistants", []) if a["name"] != name]
        if len(data["assistants"]) == original_len:
            raise ValueError(f"Assistant '{name}' not found")
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Standalone Operation CRUD (Req 17.13) ───────────────────────────

    def add_standalone_operation(self, name: str, type: str, provider_name: str,
                                 base_path: str, system_prompt: str,
                                 enabled_actions: list[str], **kwargs) -> list[str]:
        """Add a standalone operation."""
        data = self._load()
        if provider_name not in self._provider_names(data):
            raise ValueError(f"Provider '{provider_name}' not found")
        existing = {op["name"] for op in data.get("standaloneOperations", [])}
        if name in existing:
            raise ValueError(f"Standalone operation '{name}' already exists")
        if "assistantName" in kwargs:
            assistant_names = {a["name"] for a in data.get("assistants", [])}
            if kwargs["assistantName"] not in assistant_names:
                raise ValueError(f"Assistant '{kwargs['assistantName']}' not found")
        op = {
            "name": name,
            "type": type,
            "providerName": provider_name,
            "basePath": base_path,
            "systemPrompt": system_prompt,
            "enabledActions": enabled_actions,
        }
        for key in ("rolePromptSequence", "assistantName", "chatOptions",
                     "stateTable", "evaluatorNames", "responseType", "ragSourceNames"):
            if key in kwargs:
                op[key] = kwargs[key]
        data.setdefault("standaloneOperations", []).append(op)
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_standalone_operation(self, name: str) -> list[str]:
        """Remove a standalone operation."""
        data = self._load()
        original_len = len(data.get("standaloneOperations", []))
        data["standaloneOperations"] = [
            op for op in data.get("standaloneOperations", []) if op["name"] != name
        ]
        if len(data["standaloneOperations"]) == original_len:
            raise ValueError(f"Standalone operation '{name}' not found")
        self._save(data)
        return [AI_LAYER_FILE]

    def add_standalone_feature(self, operation_name: str, page_route: str,
                                page_title: str, component_type: str = "chat",
                                show_in_nav: bool = True) -> list[str]:
        """Add a standalone feature to react_ai_config.json."""
        react = _load_react_ai(self.app_dir)
        existing = {f["operationName"] for f in react.get("standaloneFeatures", [])}
        if operation_name in existing:
            raise ValueError(f"Standalone feature '{operation_name}' already exists")
        feature = {
            "operationName": operation_name,
            "pageRoute": page_route,
            "pageTitle": page_title,
            "componentType": component_type,
            "showInNav": show_in_nav,
        }
        react.setdefault("standaloneFeatures", []).append(feature)
        _save_react_ai(self.app_dir, react)
        self.status.mark_dirty([REACT_AI_FILE])
        return [REACT_AI_FILE]

    def remove_standalone_feature(self, operation_name: str) -> list[str]:
        """Remove a standalone feature from react_ai_config.json."""
        react = _load_react_ai(self.app_dir)
        original_len = len(react.get("standaloneFeatures", []))
        react["standaloneFeatures"] = [
            f for f in react.get("standaloneFeatures", [])
            if f["operationName"] != operation_name
        ]
        if len(react["standaloneFeatures"]) == original_len:
            raise ValueError(f"Standalone feature '{operation_name}' not found")
        _save_react_ai(self.app_dir, react)
        self.status.mark_dirty([REACT_AI_FILE])
        return [REACT_AI_FILE]

    # ── RAG Source CRUD (Req 17.14) ─────────────────────────────────────

    def add_rag_source(self, name: str, type: str, **kwargs) -> list[str]:
        """Add a RAG source."""
        data = self._load()
        if type not in VALID_RAG_TYPES:
            raise ValueError(f"Invalid RAG type '{type}'. Must be one of {VALID_RAG_TYPES}")
        if type == "semantic":
            pn = kwargs.get("providerName")
            if not pn:
                raise ValueError("Semantic RAG source requires 'providerName'")
            if pn not in self._provider_names(data):
                raise ValueError(f"Provider '{pn}' not found")
        existing = {r["name"] for r in data.get("ragSources", [])}
        if name in existing:
            raise ValueError(f"RAG source '{name}' already exists")
        source = {"name": name, "type": type, "enabled": kwargs.get("enabled", False)}
        for key in ("providerName", "targets", "securityMode", "chunkSize",
                     "chunkOverlap", "topK", "similarityThreshold", "rules", "maxResults"):
            if key in kwargs:
                source[key] = kwargs[key]
        data.setdefault("ragSources", []).append(source)
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_rag_source(self, name: str) -> list[str]:
        """Remove a RAG source. Checks for dependent references."""
        data = self._load()
        deps = []
        for cap in data.get("entityCapabilities", []):
            if name in (cap.get("ragSourceNames") or []):
                deps.append(f"entityCapability '{cap['entityName']}'")
        for op in data.get("standaloneOperations", []):
            if name in (op.get("ragSourceNames") or []):
                deps.append(f"standaloneOperation '{op['name']}'")
        di = data.get("documentIngestion")
        if di and di.get("targetRagSourceName") == name:
            deps.append("documentIngestion.targetRagSourceName")
        if deps:
            raise ValueError(f"Cannot remove RAG source '{name}': referenced by {', '.join(deps)}")
        original_len = len(data.get("ragSources", []))
        data["ragSources"] = [r for r in data.get("ragSources", []) if r["name"] != name]
        if len(data["ragSources"]) == original_len:
            raise ValueError(f"RAG source '{name}' not found")
        self._save(data)
        return [AI_LAYER_FILE]

    def modify_rag_source(self, name: str, **updates) -> list[str]:
        """Modify RAG source properties."""
        data = self._load()
        source = next((r for r in data.get("ragSources", []) if r["name"] == name), None)
        if not source:
            raise ValueError(f"RAG source '{name}' not found")
        for key, val in updates.items():
            source[key] = val
        self._save(data)
        return [AI_LAYER_FILE]

    def enable_rag_source(self, name: str) -> list[str]:
        return self.modify_rag_source(name, enabled=True)

    def disable_rag_source(self, name: str) -> list[str]:
        return self.modify_rag_source(name, enabled=False)

    def add_rag_to_capability(self, entity_name: str, rag_source_name: str) -> list[str]:
        """Add a RAG source reference to an entity capability."""
        data = self._load()
        rag_names = {r["name"] for r in data.get("ragSources", [])}
        if rag_source_name not in rag_names:
            raise ValueError(f"RAG source '{rag_source_name}' not found")
        cap = next((c for c in data.get("entityCapabilities", [])
                     if c["entityName"] == entity_name), None)
        if not cap:
            raise ValueError(f"Entity capability for '{entity_name}' not found")
        cap.setdefault("ragSourceNames", [])
        if rag_source_name in cap["ragSourceNames"]:
            raise ValueError(f"RAG source '{rag_source_name}' already on capability '{entity_name}'")
        cap["ragSourceNames"].append(rag_source_name)
        self._save(data)
        return [AI_LAYER_FILE]

    def add_rag_to_standalone(self, operation_name: str, rag_source_name: str) -> list[str]:
        """Add a RAG source reference to a standalone operation."""
        data = self._load()
        rag_names = {r["name"] for r in data.get("ragSources", [])}
        if rag_source_name not in rag_names:
            raise ValueError(f"RAG source '{rag_source_name}' not found")
        op = next((o for o in data.get("standaloneOperations", [])
                    if o["name"] == operation_name), None)
        if not op:
            raise ValueError(f"Standalone operation '{operation_name}' not found")
        op.setdefault("ragSourceNames", [])
        if rag_source_name in op["ragSourceNames"]:
            raise ValueError(f"RAG source '{rag_source_name}' already on operation '{operation_name}'")
        op["ragSourceNames"].append(rag_source_name)
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Evaluator CRUD (Req 17.15) ──────────────────────────────────────

    def add_evaluator(self, name: str, type: str, provider_name: str,
                      evaluation_prompt: str, scoring_mechanism: str,
                      **kwargs) -> list[str]:
        """Add an evaluator."""
        data = self._load()
        if type not in VALID_EVALUATOR_TYPES:
            raise ValueError(f"Invalid evaluator type '{type}'")
        if scoring_mechanism not in VALID_SCORING_MECHANISMS:
            raise ValueError(f"Invalid scoring mechanism '{scoring_mechanism}'")
        if provider_name not in self._provider_names(data):
            raise ValueError(f"Provider '{provider_name}' not found")
        existing = {e["name"] for e in data.get("evaluators", [])}
        if name in existing:
            raise ValueError(f"Evaluator '{name}' already exists")
        mode = kwargs.get("mode", "async")
        failure_action = kwargs.get("failureAction", "none")
        if mode == "async" and failure_action == "retry":
            raise ValueError("Evaluator with mode 'async' cannot have failureAction 'retry'")
        evaluator = {
            "name": name,
            "type": type,
            "providerName": provider_name,
            "evaluationPrompt": evaluation_prompt,
            "scoringMechanism": scoring_mechanism,
            "mode": mode,
            "failureAction": failure_action,
        }
        for key in ("threshold", "categories", "maxRetries"):
            if key in kwargs:
                evaluator[key] = kwargs[key]
        data.setdefault("evaluators", []).append(evaluator)
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_evaluator(self, name: str) -> list[str]:
        """Remove an evaluator. Checks for dependent references."""
        data = self._load()
        deps = []
        for cap in data.get("entityCapabilities", []):
            if name in (cap.get("evaluatorNames") or []):
                deps.append(f"entityCapability '{cap['entityName']}'")
        for op in data.get("standaloneOperations", []):
            if name in (op.get("evaluatorNames") or []):
                deps.append(f"standaloneOperation '{op['name']}'")
        if deps:
            raise ValueError(f"Cannot remove evaluator '{name}': referenced by {', '.join(deps)}")
        original_len = len(data.get("evaluators", []))
        data["evaluators"] = [e for e in data.get("evaluators", []) if e["name"] != name]
        if len(data["evaluators"]) == original_len:
            raise ValueError(f"Evaluator '{name}' not found")
        self._save(data)
        return [AI_LAYER_FILE]

    def modify_evaluator(self, name: str, **updates) -> list[str]:
        """Modify evaluator properties."""
        data = self._load()
        evaluator = next((e for e in data.get("evaluators", []) if e["name"] == name), None)
        if not evaluator:
            raise ValueError(f"Evaluator '{name}' not found")
        for key, val in updates.items():
            evaluator[key] = val
        self._save(data)
        return [AI_LAYER_FILE]

    def add_evaluator_to_capability(self, entity_name: str, evaluator_name: str) -> list[str]:
        """Add an evaluator reference to an entity capability."""
        data = self._load()
        eval_names = {e["name"] for e in data.get("evaluators", [])}
        if evaluator_name not in eval_names:
            raise ValueError(f"Evaluator '{evaluator_name}' not found")
        cap = next((c for c in data.get("entityCapabilities", [])
                     if c["entityName"] == entity_name), None)
        if not cap:
            raise ValueError(f"Entity capability for '{entity_name}' not found")
        cap.setdefault("evaluatorNames", [])
        if evaluator_name in cap["evaluatorNames"]:
            raise ValueError(f"Evaluator '{evaluator_name}' already on capability '{entity_name}'")
        cap["evaluatorNames"].append(evaluator_name)
        self._save(data)
        return [AI_LAYER_FILE]

    def add_evaluator_to_standalone(self, operation_name: str, evaluator_name: str) -> list[str]:
        """Add an evaluator reference to a standalone operation."""
        data = self._load()
        eval_names = {e["name"] for e in data.get("evaluators", [])}
        if evaluator_name not in eval_names:
            raise ValueError(f"Evaluator '{evaluator_name}' not found")
        op = next((o for o in data.get("standaloneOperations", [])
                    if o["name"] == operation_name), None)
        if not op:
            raise ValueError(f"Standalone operation '{operation_name}' not found")
        op.setdefault("evaluatorNames", [])
        if evaluator_name in op["evaluatorNames"]:
            raise ValueError(f"Evaluator '{evaluator_name}' already on operation '{operation_name}'")
        op["evaluatorNames"].append(evaluator_name)
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Role Prompt Sequence (Req 17.16) ────────────────────────────────

    def set_role_prompt_sequence(self, target_type: str, target_name: str,
                                 sequence: list[dict]) -> list[str]:
        """Set rolePromptSequence on an assistant, standalone op, or entity capability."""
        data = self._load()
        target = self._find_target(data, target_type, target_name)
        target["rolePromptSequence"] = sequence
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_role_prompt_sequence(self, target_type: str, target_name: str) -> list[str]:
        """Remove rolePromptSequence from a target."""
        data = self._load()
        target = self._find_target(data, target_type, target_name)
        target.pop("rolePromptSequence", None)
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Provider Role/Parameter Methods (Req 17.17) ─────────────────────

    def set_provider_supported_roles(self, provider_name: str, roles: list[str]) -> list[str]:
        data = self._load()
        p = self._find_provider(data, provider_name)
        p["supportedRoles"] = roles
        self._save(data)
        return [AI_LAYER_FILE]

    def set_provider_role_fallbacks(self, provider_name: str, fallbacks: dict) -> list[str]:
        data = self._load()
        p = self._find_provider(data, provider_name)
        p["roleFallbacks"] = fallbacks
        self._save(data)
        return [AI_LAYER_FILE]

    def set_provider_chat_options(self, provider_name: str, options: dict) -> list[str]:
        data = self._load()
        p = self._find_provider(data, provider_name)
        p["chatOptions"] = options
        self._save(data)
        return [AI_LAYER_FILE]

    def set_provider_supported_parameters(self, provider_name: str, params: list[str]) -> list[str]:
        data = self._load()
        p = self._find_provider(data, provider_name)
        p["supportedParameters"] = params
        self._save(data)
        return [AI_LAYER_FILE]

    def set_provider_parameter_fallbacks(self, provider_name: str, fallbacks: dict) -> list[str]:
        data = self._load()
        p = self._find_provider(data, provider_name)
        p["parameterFallbacks"] = fallbacks
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Chat Options (Req 17.18) ────────────────────────────────────────

    def set_chat_options(self, target_type: str, target_name: str,
                         options: dict) -> list[str]:
        data = self._load()
        target = self._find_target(data, target_type, target_name)
        target["chatOptions"] = options
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_chat_options(self, target_type: str, target_name: str) -> list[str]:
        data = self._load()
        target = self._find_target(data, target_type, target_name)
        target.pop("chatOptions", None)
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Response Type (Req 17.19) ───────────────────────────────────────

    def set_response_type(self, target_type: str, target_name: str,
                          response_type: dict) -> list[str]:
        data = self._load()
        target = self._find_target(data, target_type, target_name)
        target["responseType"] = response_type
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_response_type(self, target_type: str, target_name: str) -> list[str]:
        data = self._load()
        target = self._find_target(data, target_type, target_name)
        target.pop("responseType", None)
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Document Ingestion (Req 17.20) ──────────────────────────────────

    def set_document_ingestion(self, **kwargs) -> list[str]:
        data = self._load()
        if "targetRagSourceName" in kwargs:
            rag_names = {r["name"] for r in data.get("ragSources", [])}
            if kwargs["targetRagSourceName"] not in rag_names:
                raise ValueError(f"RAG source '{kwargs['targetRagSourceName']}' not found")
        ingestion = {
            "enabled": kwargs.get("enabled", True),
            "allowedMimeTypes": kwargs.get("allowedMimeTypes", ["application/pdf", "text/plain"]),
            "maxFileSizeBytes": kwargs.get("maxFileSizeBytes", 10485760),
            "metadataFields": kwargs.get("metadataFields", []),
            "autoIndexOnUpload": kwargs.get("autoIndexOnUpload", True),
            "sources": kwargs.get("sources", []),
        }
        for key in ("maxTotalStorageBytes", "targetRagSourceName"):
            if key in kwargs:
                ingestion[key] = kwargs[key]
        data["documentIngestion"] = ingestion
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_document_ingestion(self) -> list[str]:
        data = self._load()
        # Check if documentProcessing depends on it
        if data.get("documentProcessing"):
            raise ValueError("Cannot remove documentIngestion: documentProcessing depends on it")
        data["documentIngestion"] = None
        self._save(data)
        return [AI_LAYER_FILE]

    def add_document_source(self, source: dict) -> list[str]:
        data = self._load()
        if not data.get("documentIngestion"):
            raise ValueError("documentIngestion must be configured first")
        data["documentIngestion"].setdefault("sources", []).append(source)
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_document_source(self, source_type: str, **match_kwargs) -> list[str]:
        data = self._load()
        if not data.get("documentIngestion"):
            raise ValueError("documentIngestion not configured")
        sources = data["documentIngestion"].get("sources", [])
        data["documentIngestion"]["sources"] = [
            s for s in sources if s.get("type") != source_type
        ]
        self._save(data)
        return [AI_LAYER_FILE]

    def modify_document_source(self, index: int, **updates) -> list[str]:
        data = self._load()
        if not data.get("documentIngestion"):
            raise ValueError("documentIngestion not configured")
        sources = data["documentIngestion"].get("sources", [])
        if index < 0 or index >= len(sources):
            raise ValueError(f"Source index {index} out of range")
        for key, val in updates.items():
            sources[index][key] = val
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Document Processing (Req 17.21) ─────────────────────────────────

    def set_document_processing(self, **kwargs) -> list[str]:
        data = self._load()
        if not data.get("documentIngestion"):
            raise ValueError("documentProcessing requires documentIngestion to be configured")
        processing = {
            "enabled": kwargs.get("enabled", True),
            "tasks": kwargs.get("tasks", []),
        }
        if "defaultProviderName" in kwargs:
            if kwargs["defaultProviderName"] not in self._provider_names(data):
                raise ValueError(f"Provider '{kwargs['defaultProviderName']}' not found")
            processing["defaultProviderName"] = kwargs["defaultProviderName"]
        data["documentProcessing"] = processing
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_document_processing(self) -> list[str]:
        data = self._load()
        data["documentProcessing"] = None
        self._save(data)
        return [AI_LAYER_FILE]

    def add_document_task(self, name: str, task_type: str, provider_name: str,
                          prompt_template: str, **kwargs) -> list[str]:
        data = self._load()
        if not data.get("documentProcessing"):
            raise ValueError("documentProcessing must be configured first")
        if provider_name not in self._provider_names(data):
            raise ValueError(f"Provider '{provider_name}' not found")
        existing = {t["name"] for t in data["documentProcessing"].get("tasks", [])}
        if name in existing:
            raise ValueError(f"Document task '{name}' already exists")
        task = {
            "name": name,
            "taskType": task_type,
            "providerName": provider_name,
            "promptTemplate": prompt_template,
        }
        for key in ("eligibleProviders", "chatOptions", "responseFormat",
                     "targetScope", "targetLanguage", "categories",
                     "requiresSecondDocument"):
            if key in kwargs:
                task[key] = kwargs[key]
        data["documentProcessing"].setdefault("tasks", []).append(task)
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_document_task(self, name: str) -> list[str]:
        data = self._load()
        if not data.get("documentProcessing"):
            raise ValueError("documentProcessing not configured")
        original_len = len(data["documentProcessing"].get("tasks", []))
        data["documentProcessing"]["tasks"] = [
            t for t in data["documentProcessing"].get("tasks", []) if t["name"] != name
        ]
        if len(data["documentProcessing"]["tasks"]) == original_len:
            raise ValueError(f"Document task '{name}' not found")
        self._save(data)
        return [AI_LAYER_FILE]

    def modify_document_task(self, name: str, **updates) -> list[str]:
        data = self._load()
        if not data.get("documentProcessing"):
            raise ValueError("documentProcessing not configured")
        task = next((t for t in data["documentProcessing"].get("tasks", [])
                      if t["name"] == name), None)
        if not task:
            raise ValueError(f"Document task '{name}' not found")
        for key, val in updates.items():
            task[key] = val
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Vector Store (Req 17.22) ────────────────────────────────────────

    def set_vector_store(self, **kwargs) -> list[str]:
        data = self._load()
        vs = {
            "type": kwargs.get("type", "milvus"),
            "host": kwargs.get("host", "localhost"),
            "port": kwargs.get("port", 19530),
            "collectionPrefix": kwargs.get("collectionPrefix", "ai_"),
            "maxConnections": kwargs.get("maxConnections", 10),
            "connectTimeoutMs": kwargs.get("connectTimeoutMs", 5000),
            "idleTimeoutMs": kwargs.get("idleTimeoutMs", 60000),
        }
        for key in ("apiKey", "database"):
            if key in kwargs:
                vs[key] = kwargs[key]
        if vs["type"] not in VALID_VECTOR_STORE_TYPES:
            raise ValueError(f"Invalid vector store type '{vs['type']}'")
        data["vectorStore"] = vs
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_vector_store(self) -> list[str]:
        data = self._load()
        data["vectorStore"] = None
        self._save(data)
        return [AI_LAYER_FILE]

    def modify_vector_store(self, **updates) -> list[str]:
        data = self._load()
        if not data.get("vectorStore"):
            raise ValueError("vectorStore not configured")
        for key, val in updates.items():
            data["vectorStore"][key] = val
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Orchestrator (Req 17.23) ────────────────────────────────────────

    def set_orchestrator(self, provider_name: str, **kwargs) -> list[str]:
        data = self._load()
        if provider_name not in self._provider_names(data):
            raise ValueError(f"Provider '{provider_name}' not found")
        orch = {"providerName": provider_name}
        for key in ("systemPrompt", "chatOptions", "accessDeniedMessage",
                     "promptSecurity", "moderation"):
            if key in kwargs:
                orch[key] = kwargs[key]
        data["orchestrator"] = orch
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_orchestrator(self) -> list[str]:
        data = self._load()
        # Check MCP servers
        if data.get("mcpServers"):
            raise ValueError("Cannot remove orchestrator: mcpServers depend on it")
        data["orchestrator"] = None
        self._save(data)
        return [AI_LAYER_FILE]

    def modify_orchestrator(self, **updates) -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator not configured")
        for key, val in updates.items():
            data["orchestrator"][key] = val
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Prompt Security (Req 17.24) ─────────────────────────────────────

    def set_prompt_security(self, security: dict) -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator must be configured first")
        data["orchestrator"]["promptSecurity"] = security
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_prompt_security(self) -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator not configured")
        data["orchestrator"].pop("promptSecurity", None)
        self._save(data)
        return [AI_LAYER_FILE]

    def set_safeguard_advisor(self, enabled: bool, sensitive_words: list[str]) -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator must be configured first")
        ps = data["orchestrator"].setdefault("promptSecurity", {})
        ps["safeGuardAdvisor"] = {"enabled": enabled, "sensitiveWords": sensitive_words}
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_safeguard_advisor(self) -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator not configured")
        ps = data["orchestrator"].get("promptSecurity", {})
        ps.pop("safeGuardAdvisor", None)
        self._save(data)
        return [AI_LAYER_FILE]

    def set_canary_word_advisor(self, enabled: bool, canary_tokens: list[str]) -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator must be configured first")
        ps = data["orchestrator"].setdefault("promptSecurity", {})
        ps["canaryWordAdvisor"] = {"enabled": enabled, "canaryTokens": canary_tokens}
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_canary_word_advisor(self) -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator not configured")
        ps = data["orchestrator"].get("promptSecurity", {})
        ps.pop("canaryWordAdvisor", None)
        self._save(data)
        return [AI_LAYER_FILE]

    def set_input_sanitization(self, enabled: bool, rules: list[dict]) -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator must be configured first")
        ps = data["orchestrator"].setdefault("promptSecurity", {})
        ps["inputSanitization"] = {"enabled": enabled, "rules": rules}
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_input_sanitization(self) -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator not configured")
        ps = data["orchestrator"].get("promptSecurity", {})
        ps.pop("inputSanitization", None)
        self._save(data)
        return [AI_LAYER_FILE]

    def set_output_filtering(self, enabled: bool, rules: list[dict]) -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator must be configured first")
        ps = data["orchestrator"].setdefault("promptSecurity", {})
        ps["outputFiltering"] = {"enabled": enabled, "rules": rules}
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_output_filtering(self) -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator not configured")
        ps = data["orchestrator"].get("promptSecurity", {})
        ps.pop("outputFiltering", None)
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Moderation (Req 17.25) ──────────────────────────────────────────

    def set_moderation(self, enabled: bool, provider_name: str,
                       categories: list[str], pre_moderation: bool = True,
                       post_moderation: bool = True,
                       failure_action: str = "block") -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator must be configured first")
        if provider_name not in self._provider_names(data):
            raise ValueError(f"Provider '{provider_name}' not found")
        if failure_action not in VALID_MODERATION_FAILURE_ACTIONS:
            raise ValueError(f"Invalid failureAction '{failure_action}'")
        data["orchestrator"]["moderation"] = {
            "enabled": enabled,
            "providerName": provider_name,
            "categories": categories,
            "preModeration": pre_moderation,
            "postModeration": post_moderation,
            "failureAction": failure_action,
        }
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_moderation(self) -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator not configured")
        data["orchestrator"].pop("moderation", None)
        self._save(data)
        return [AI_LAYER_FILE]

    def modify_moderation(self, **updates) -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator not configured")
        mod = data["orchestrator"].get("moderation")
        if not mod:
            raise ValueError("moderation not configured")
        if "providerName" in updates:
            if updates["providerName"] not in self._provider_names(data):
                raise ValueError(f"Provider '{updates['providerName']}' not found")
        if "failureAction" in updates:
            if updates["failureAction"] not in VALID_MODERATION_FAILURE_ACTIONS:
                raise ValueError(f"Invalid failureAction '{updates['failureAction']}'")
        for key, val in updates.items():
            mod[key] = val
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Access Denied Message (Req 17.26) ───────────────────────────────

    def set_access_denied_message(self, message: str) -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator must be configured first")
        data["orchestrator"]["accessDeniedMessage"] = message
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_access_denied_message(self) -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator not configured")
        data["orchestrator"].pop("accessDeniedMessage", None)
        self._save(data)
        return [AI_LAYER_FILE]

    # ── MCP Server CRUD (Req 17.27) ────────────────────────────────────

    def add_mcp_server(self, name: str, transport_type: str,
                       required_roles: list[str], **kwargs) -> list[str]:
        data = self._load()
        if not data.get("orchestrator"):
            raise ValueError("orchestrator must be configured (mcpServers require orchestrator)")
        if transport_type not in VALID_MCP_TRANSPORT_TYPES:
            raise ValueError(f"Invalid transport type '{transport_type}'")
        existing = {m["name"] for m in data.get("mcpServers", [])}
        if name in existing:
            raise ValueError(f"MCP server '{name}' already exists")
        server = {
            "name": name,
            "transportType": transport_type,
            "requiredRoles": required_roles,
            "enabled": kwargs.get("enabled", False),
        }
        for key in ("envVars", "auth", "exposedTools", "command", "args",
                     "url", "sseEndpoint"):
            if key in kwargs:
                server[key] = kwargs[key]
        data.setdefault("mcpServers", []).append(server)
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_mcp_server(self, name: str) -> list[str]:
        data = self._load()
        original_len = len(data.get("mcpServers", []))
        data["mcpServers"] = [m for m in data.get("mcpServers", []) if m["name"] != name]
        if len(data["mcpServers"]) == original_len:
            raise ValueError(f"MCP server '{name}' not found")
        self._save(data)
        return [AI_LAYER_FILE]

    def modify_mcp_server(self, name: str, **updates) -> list[str]:
        data = self._load()
        server = next((m for m in data.get("mcpServers", []) if m["name"] == name), None)
        if not server:
            raise ValueError(f"MCP server '{name}' not found")
        for key, val in updates.items():
            server[key] = val
        self._save(data)
        return [AI_LAYER_FILE]

    def enable_mcp_server(self, name: str) -> list[str]:
        return self.modify_mcp_server(name, enabled=True)

    def disable_mcp_server(self, name: str) -> list[str]:
        return self.modify_mcp_server(name, enabled=False)

    # ── Observability (Req 17.28) ───────────────────────────────────────

    def set_observability(self, enabled: bool = True, **kwargs) -> list[str]:
        data = self._load()
        obs = {"enabled": enabled, "dashboards": []}
        if "prometheus" in kwargs:
            obs["prometheus"] = kwargs["prometheus"]
        if "grafana" in kwargs:
            g = kwargs["grafana"]
            if not g.get("url") or not g.get("apiKeyEnvVar"):
                raise ValueError("grafana requires 'url' and 'apiKeyEnvVar'")
            obs["grafana"] = g
        data["observability"] = obs
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_observability(self) -> list[str]:
        data = self._load()
        data["observability"] = None
        self._save(data)
        return [AI_LAYER_FILE]

    def modify_observability(self, **updates) -> list[str]:
        data = self._load()
        if not data.get("observability"):
            raise ValueError("observability not configured")
        if "grafana" in updates:
            g = updates["grafana"]
            if g and (not g.get("url") or not g.get("apiKeyEnvVar")):
                raise ValueError("grafana requires 'url' and 'apiKeyEnvVar'")
        for key, val in updates.items():
            data["observability"][key] = val
        self._save(data)
        return [AI_LAYER_FILE]

    def add_observability_dashboard(self, name: str, panels: list[dict],
                                     layout: dict | None = None) -> list[str]:
        data = self._load()
        if not data.get("observability"):
            raise ValueError("observability must be configured first")
        if not panels:
            raise ValueError("Dashboard panels cannot be empty")
        existing = {d["name"] for d in data["observability"].get("dashboards", [])}
        if name in existing:
            raise ValueError(f"Dashboard '{name}' already exists")
        dashboard = {"name": name, "panels": panels}
        if layout:
            dashboard["layout"] = layout
        data["observability"].setdefault("dashboards", []).append(dashboard)
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_observability_dashboard(self, name: str) -> list[str]:
        data = self._load()
        if not data.get("observability"):
            raise ValueError("observability not configured")
        original_len = len(data["observability"].get("dashboards", []))
        data["observability"]["dashboards"] = [
            d for d in data["observability"].get("dashboards", []) if d["name"] != name
        ]
        if len(data["observability"]["dashboards"]) == original_len:
            raise ValueError(f"Dashboard '{name}' not found")
        self._save(data)
        return [AI_LAYER_FILE]

    def modify_observability_dashboard(self, name: str, **updates) -> list[str]:
        data = self._load()
        if not data.get("observability"):
            raise ValueError("observability not configured")
        dashboard = next((d for d in data["observability"].get("dashboards", [])
                           if d["name"] == name), None)
        if not dashboard:
            raise ValueError(f"Dashboard '{name}' not found")
        for key, val in updates.items():
            dashboard[key] = val
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Rate Limiting (Req 17.29) ───────────────────────────────────────

    def set_rate_limiting(self, default_rpm: int = 20,
                          overrides: dict | None = None) -> list[str]:
        data = self._load()
        rl = {"defaultRpm": default_rpm}
        if overrides:
            for cat in overrides:
                if cat not in VALID_RATE_LIMIT_CATEGORIES:
                    raise ValueError(f"Invalid rate limit category '{cat}'")
            rl["overrides"] = overrides
        data["rateLimiting"] = rl
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_rate_limiting(self) -> list[str]:
        data = self._load()
        data["rateLimiting"] = None
        self._save(data)
        return [AI_LAYER_FILE]

    def modify_rate_limiting(self, **updates) -> list[str]:
        data = self._load()
        if not data.get("rateLimiting"):
            raise ValueError("rateLimiting not configured")
        for key, val in updates.items():
            data["rateLimiting"][key] = val
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Provider Resilience (Req 17.30) ─────────────────────────────────

    def set_provider_resilience(self, provider_name: str,
                                 retry: dict | None = None,
                                 circuit_breaker: dict | None = None) -> list[str]:
        data = self._load()
        p = self._find_provider(data, provider_name)
        resilience = {}
        if retry:
            resilience["retry"] = retry
        if circuit_breaker:
            resilience["circuitBreaker"] = circuit_breaker
        p["resilience"] = resilience
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_provider_resilience(self, provider_name: str) -> list[str]:
        data = self._load()
        p = self._find_provider(data, provider_name)
        p.pop("resilience", None)
        self._save(data)
        return [AI_LAYER_FILE]

    def modify_provider_resilience(self, provider_name: str, **updates) -> list[str]:
        data = self._load()
        p = self._find_provider(data, provider_name)
        if "resilience" not in p:
            raise ValueError(f"Provider '{provider_name}' has no resilience config")
        for key, val in updates.items():
            p["resilience"][key] = val
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Token Budget (Req 17.31) ────────────────────────────────────────

    def set_token_budget(self, enabled: bool = True, **kwargs) -> list[str]:
        data = self._load()
        budget = {"enabled": enabled}
        for key in ("defaultDailyLimitPerUser", "defaultMonthlyLimitPerUser",
                     "warningThresholdPercent", "enforcementAction"):
            if key in kwargs:
                budget[key] = kwargs[key]
        if "enforcementAction" in budget:
            if budget["enforcementAction"] not in VALID_ENFORCEMENT_ACTIONS:
                raise ValueError(f"Invalid enforcementAction '{budget['enforcementAction']}'")
        if "providerOverrides" in kwargs:
            for pn in kwargs["providerOverrides"]:
                if pn not in self._provider_names(data):
                    raise ValueError(f"Provider '{pn}' not found in providerOverrides")
            budget["providerOverrides"] = kwargs["providerOverrides"]
        data["tokenBudget"] = budget
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_token_budget(self) -> list[str]:
        data = self._load()
        data["tokenBudget"] = None
        self._save(data)
        return [AI_LAYER_FILE]

    def modify_token_budget(self, **updates) -> list[str]:
        data = self._load()
        if not data.get("tokenBudget"):
            raise ValueError("tokenBudget not configured")
        for key, val in updates.items():
            data["tokenBudget"][key] = val
        self._save(data)
        return [AI_LAYER_FILE]

    def set_token_budget_provider_override(self, provider_name: str,
                                            daily_limit: int | None = None,
                                            monthly_limit: int | None = None) -> list[str]:
        data = self._load()
        if not data.get("tokenBudget"):
            raise ValueError("tokenBudget must be configured first")
        if provider_name not in self._provider_names(data):
            raise ValueError(f"Provider '{provider_name}' not found")
        overrides = data["tokenBudget"].setdefault("providerOverrides", {})
        override = {}
        if daily_limit is not None:
            override["dailyLimit"] = daily_limit
        if monthly_limit is not None:
            override["monthlyLimit"] = monthly_limit
        overrides[provider_name] = override
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_token_budget_provider_override(self, provider_name: str) -> list[str]:
        data = self._load()
        if not data.get("tokenBudget"):
            raise ValueError("tokenBudget not configured")
        overrides = data["tokenBudget"].get("providerOverrides", {})
        if provider_name not in overrides:
            raise ValueError(f"No override for provider '{provider_name}'")
        del overrides[provider_name]
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Chat Session Cleanup (Req 17.32) ────────────────────────────────

    def set_chat_session_cleanup(self, enabled: bool = True, **kwargs) -> list[str]:
        data = self._load()
        cleanup = {
            "enabled": enabled,
            "defaultTtlDays": kwargs.get("defaultTtlDays", 30),
            "cleanupCronExpression": kwargs.get("cleanupCronExpression", "0 0 2 * * *"),
            "batchSize": kwargs.get("batchSize", 1000),
        }
        data["chatSessionCleanup"] = cleanup
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_chat_session_cleanup(self) -> list[str]:
        data = self._load()
        data["chatSessionCleanup"] = None
        self._save(data)
        return [AI_LAYER_FILE]

    def modify_chat_session_cleanup(self, **updates) -> list[str]:
        data = self._load()
        if not data.get("chatSessionCleanup"):
            raise ValueError("chatSessionCleanup not configured")
        for key, val in updates.items():
            data["chatSessionCleanup"][key] = val
        self._save(data)
        return [AI_LAYER_FILE]

    def set_topic_summarization(self, enabled: bool, provider_name: str,
                                 max_topics_per_session: int = 5) -> list[str]:
        data = self._load()
        if not data.get("chatSessionCleanup"):
            raise ValueError("chatSessionCleanup must be configured first")
        if provider_name not in self._provider_names(data):
            raise ValueError(f"Provider '{provider_name}' not found")
        data["chatSessionCleanup"]["topicSummarization"] = {
            "enabled": enabled,
            "providerName": provider_name,
            "maxTopicsPerSession": max_topics_per_session,
        }
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_topic_summarization(self) -> list[str]:
        data = self._load()
        if not data.get("chatSessionCleanup"):
            raise ValueError("chatSessionCleanup not configured")
        data["chatSessionCleanup"].pop("topicSummarization", None)
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Audit Log (Req 17.33) ──────────────────────────────────────────

    def set_audit_log(self, enabled: bool = True, **kwargs) -> list[str]:
        data = self._load()
        audit = {
            "enabled": enabled,
            "retentionDays": kwargs.get("retentionDays", 90),
            "cleanupCronExpression": kwargs.get("cleanupCronExpression", "0 0 3 * * *"),
        }
        if "loggedEvents" in kwargs:
            for evt in kwargs["loggedEvents"]:
                if evt not in VALID_AUDIT_EVENTS:
                    raise ValueError(f"Invalid audit event type '{evt}'")
            audit["loggedEvents"] = kwargs["loggedEvents"]
        data["auditLog"] = audit
        self._save(data)
        return [AI_LAYER_FILE]

    def remove_audit_log(self) -> list[str]:
        data = self._load()
        data["auditLog"] = None
        self._save(data)
        return [AI_LAYER_FILE]

    def modify_audit_log(self, **updates) -> list[str]:
        data = self._load()
        if not data.get("auditLog"):
            raise ValueError("auditLog not configured")
        if "loggedEvents" in updates:
            for evt in updates["loggedEvents"]:
                if evt not in VALID_AUDIT_EVENTS:
                    raise ValueError(f"Invalid audit event type '{evt}'")
        for key, val in updates.items():
            data["auditLog"][key] = val
        self._save(data)
        return [AI_LAYER_FILE]

    # ── Private helpers ─────────────────────────────────────────────────

    def _find_provider(self, data: dict, name: str) -> dict:
        """Find a provider by name, raising ValueError if not found."""
        provider = next((p for p in data.get("providers", []) if p["name"] == name), None)
        if not provider:
            raise ValueError(f"Provider '{name}' not found")
        return provider

    def _find_target(self, data: dict, target_type: str, target_name: str) -> dict:
        """Find a target (assistant, standalone, or entity capability) by type and name."""
        if target_type == "assistant":
            target = next((a for a in data.get("assistants", [])
                            if a["name"] == target_name), None)
            if not target:
                raise ValueError(f"Assistant '{target_name}' not found")
        elif target_type == "standalone":
            target = next((o for o in data.get("standaloneOperations", [])
                            if o["name"] == target_name), None)
            if not target:
                raise ValueError(f"Standalone operation '{target_name}' not found")
        elif target_type == "entity":
            target = next((c for c in data.get("entityCapabilities", [])
                            if c["entityName"] == target_name), None)
            if not target:
                raise ValueError(f"Entity capability for '{target_name}' not found")
        else:
            raise ValueError(f"Invalid target_type '{target_type}'. Must be 'assistant', 'standalone', or 'entity'")
        return target
