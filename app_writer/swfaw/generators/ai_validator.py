"""Validates AI_Layer definition: schema, cross-references, constraints.

Checks the webflux_ai_layer.json definition for structural correctness,
cross-reference integrity, and constraint satisfaction before code generation.
Raises ValueError for errors; returns a list of warnings for non-fatal issues.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from swfaw.utils.definition_loader import DefinitionBundle

# Valid event types for auditLog.loggedEvents (Req 1.18)
VALID_AUDIT_EVENT_TYPES = frozenset({
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

# Valid moderation failure actions (Req 1.12)
VALID_MODERATION_FAILURE_ACTIONS = frozenset({"block", "warn", "log"})

# Valid provider types (Req 1.2)
VALID_PROVIDER_TYPES = frozenset({"openai", "ollama"})

# Valid evaluator modes and failure actions (Req 1.8)
VALID_EVALUATOR_TYPES = frozenset({"relevancy", "correctness", "safety", "custom"})
VALID_SCORING_MECHANISMS = frozenset({"numeric", "pass_fail", "categorical"})
VALID_EVALUATOR_FAILURE_ACTIONS = frozenset({"none", "retry", "warn"})

# Valid RAG source types (Req 1.7)
VALID_RAG_TYPES = frozenset({"semantic", "heuristic"})

# Valid role fallback strategies (Req 1.2)
VALID_ROLE_FALLBACKS = frozenset({"prepend_to_user", "skip", "merge_to_system", "error"})

# Valid parameter fallback strategies (Req 1.2)
VALID_PARAMETER_FALLBACKS = frozenset({"skip", "error"})

# Valid stateTable column types (Req 1.4)
VALID_COLUMN_TYPES = frozenset({
    "VARCHAR", "INT", "BIGINT", "TEXT", "BOOLEAN", "DATETIME", "JSON", "DOUBLE",
})


class AiValidator:
    """Validates AI_Layer definition: schema, cross-references, constraints."""

    def validate(self, ai_layer: dict, bundle: "DefinitionBundle") -> list[str]:
        """Validate the full AI_Layer definition.

        Returns a list of warning strings. Raises ``ValueError`` for errors.
        """
        warnings: list[str] = []

        self._validate_schema_version(ai_layer)

        providers = ai_layer.get("providers", [])
        self._validate_providers(providers)

        # Build helper lookups
        provider_names = {p["name"] for p in providers}
        assistant_list = ai_layer.get("assistants", [])
        assistant_names = {a["name"] for a in assistant_list}

        # Entity names from the entity_layer in the bundle
        entity_names = set()
        if bundle.entity_layer:
            for ent in bundle.entity_layer.get("entities", []):
                entity_names.add(ent.get("className", ""))

        entity_caps = ai_layer.get("entityCapabilities", [])
        self._validate_entity_capabilities(entity_caps, entity_names, providers)

        standalone_ops = ai_layer.get("standaloneOperations", [])
        self._validate_standalone_operations(standalone_ops, providers, assistant_list)

        evaluators = ai_layer.get("evaluators", [])
        self._validate_evaluators(evaluators, providers)

        rag_sources = ai_layer.get("ragSources", [])
        self._validate_rag_sources(rag_sources, providers)

        orchestrator = ai_layer.get("orchestrator")
        mcp_servers = ai_layer.get("mcpServers", [])
        if orchestrator:
            self._validate_orchestrator(orchestrator, providers, mcp_servers)

        doc_ingestion = ai_layer.get("documentIngestion") or {}
        doc_processing = ai_layer.get("documentProcessing") or {}
        self._validate_document_config(doc_ingestion, doc_processing, rag_sources)

        observability = ai_layer.get("observability")
        if observability:
            self._validate_observability(observability)

        token_budget = ai_layer.get("tokenBudget")
        if token_budget:
            self._validate_token_budget(token_budget, providers)

        cleanup = ai_layer.get("chatSessionCleanup")
        if cleanup:
            self._validate_chat_session_cleanup(cleanup, providers)

        audit_log = ai_layer.get("auditLog")
        if audit_log:
            self._validate_audit_log(audit_log)

        # Cross-reference validation (covers all sections)
        self._validate_cross_references(ai_layer, bundle)

        # Constraint: mcpServers without orchestrator (Req 1.29)
        if mcp_servers and not orchestrator:
            raise ValueError(
                "mcpServers requires orchestrator to be configured"
            )

        # Constraint: duplicate names across named arrays (Req 1.29)
        self._check_duplicate_names(ai_layer)

        # Constraint: stateTable naming conflicts (Req 1.29)
        self._check_state_table_conflicts(standalone_ops)

        # Warnings (Req 1.30)
        warnings.extend(self._collect_warnings(ai_layer, providers))

        return warnings

    # ------------------------------------------------------------------
    # Schema version
    # ------------------------------------------------------------------

    def _validate_schema_version(self, ai_layer: dict) -> None:
        """Req 1.28: schemaVersion must be '1.0'."""
        version = ai_layer.get("schemaVersion")
        if version != "1.0":
            raise ValueError(
                f"Unsupported schemaVersion '{version}'. Expected '1.0'. "
                "Migration hint: ensure your definition file uses schemaVersion \"1.0\"."
            )

    # ------------------------------------------------------------------
    # Providers
    # ------------------------------------------------------------------

    def _validate_providers(self, providers: list[dict]) -> None:
        """Req 1.2, 1.29: provider structure and constraints."""
        seen_names: set[str] = set()
        for p in providers:
            name = p.get("name", "")
            if not name:
                raise ValueError("Provider entry missing required 'name' field")

            if name in seen_names:
                raise ValueError(
                    f"Duplicate provider name '{name}' in providers"
                )
            seen_names.add(name)

            ptype = p.get("type", "")
            if ptype not in VALID_PROVIDER_TYPES:
                raise ValueError(
                    f"Provider '{name}' has invalid type '{ptype}'. "
                    f"Must be one of: {sorted(VALID_PROVIDER_TYPES)}"
                )

            temp = p.get("temperature", 0.7)
            if not isinstance(temp, (int, float)) or temp < 0.0 or temp > 2.0:
                raise ValueError(
                    f"Provider '{name}' temperature must be 0.0–2.0, got {temp}"
                )

            supported_roles = p.get("supportedRoles", ["system", "user", "assistant"])
            if "user" not in supported_roles:
                raise ValueError(
                    f"Provider '{name}' supportedRoles must include 'user'"
                )

    # ------------------------------------------------------------------
    # Entity capabilities
    # ------------------------------------------------------------------

    def _validate_entity_capabilities(
        self, caps: list, entities: set, providers: list
    ) -> None:
        """Req 1.3, 1.29: entityCapabilities references."""
        provider_names = {p["name"] for p in providers}
        for cap in caps:
            ename = cap.get("entityName", "")
            if ename not in entities:
                raise ValueError(
                    f"Entity '{ename}' in entityCapabilities not found in entity_layer"
                )
            pname = cap.get("providerName", "")
            if pname not in provider_names:
                raise ValueError(
                    f"Provider '{pname}' referenced by entityCapabilities "
                    f"(entity '{ename}') not found in providers array"
                )

    # ------------------------------------------------------------------
    # Standalone operations
    # ------------------------------------------------------------------

    def _validate_standalone_operations(
        self, ops: list, providers: list, assistants: list
    ) -> None:
        """Req 1.4, 1.29: standaloneOperations references."""
        provider_names = {p["name"] for p in providers}
        assistant_names = {a["name"] for a in assistants}
        for op in ops:
            pname = op.get("providerName", "")
            if pname not in provider_names:
                raise ValueError(
                    f"Provider '{pname}' referenced by standaloneOperations "
                    f"(operation '{op.get('name', '')}') not found in providers array"
                )
            aname = op.get("assistantName")
            if aname and aname not in assistant_names:
                raise ValueError(
                    f"Assistant '{aname}' referenced by standaloneOperations "
                    f"(operation '{op.get('name', '')}') not found in assistants array"
                )

    # ------------------------------------------------------------------
    # Cross-reference validation
    # ------------------------------------------------------------------

    def _validate_cross_references(
        self, ai_layer: dict, bundle: "DefinitionBundle"
    ) -> None:
        """Req 1.29: validate all cross-references across sections."""
        provider_names = {p["name"] for p in ai_layer.get("providers", [])}
        rag_source_names = {r["name"] for r in ai_layer.get("ragSources", [])}
        evaluator_names = {e["name"] for e in ai_layer.get("evaluators", [])}
        assistant_names = {a["name"] for a in ai_layer.get("assistants", [])}

        # Entity names from bundle
        entity_names = set()
        if bundle.entity_layer:
            for ent in bundle.entity_layer.get("entities", []):
                entity_names.add(ent.get("className", ""))

        # --- Provider references in assistants ---
        for a in ai_layer.get("assistants", []):
            pname = a.get("providerName", "")
            if pname not in provider_names:
                raise ValueError(
                    f"Provider '{pname}' referenced by assistant "
                    f"'{a.get('name', '')}' not found in providers array"
                )

        # --- RAG source name references ---
        for cap in ai_layer.get("entityCapabilities", []):
            for rsn in cap.get("ragSourceNames", []):
                if rsn not in rag_source_names:
                    raise ValueError(
                        f"RAG source '{rsn}' referenced by entityCapabilities "
                        f"(entity '{cap.get('entityName', '')}') not found in ragSources"
                    )

        for op in ai_layer.get("standaloneOperations", []):
            for rsn in op.get("ragSourceNames", []):
                if rsn not in rag_source_names:
                    raise ValueError(
                        f"RAG source '{rsn}' referenced by standaloneOperations "
                        f"(operation '{op.get('name', '')}') not found in ragSources"
                    )

        # --- Evaluator name references ---
        for cap in ai_layer.get("entityCapabilities", []):
            for en in cap.get("evaluatorNames", []):
                if en not in evaluator_names:
                    raise ValueError(
                        f"Evaluator '{en}' referenced by entityCapabilities "
                        f"(entity '{cap.get('entityName', '')}') not found in evaluators"
                    )

        for op in ai_layer.get("standaloneOperations", []):
            for en in op.get("evaluatorNames", []):
                if en not in evaluator_names:
                    raise ValueError(
                        f"Evaluator '{en}' referenced by standaloneOperations "
                        f"(operation '{op.get('name', '')}') not found in evaluators"
                    )

        # --- Prompt template entity references ---
        for pt in ai_layer.get("promptTemplates", []):
            pt_entity = pt.get("entityName")
            if pt_entity and pt_entity not in entity_names:
                raise ValueError(
                    f"Entity '{pt_entity}' in promptTemplates "
                    f"(template '{pt.get('name', '')}') not found in entity_layer"
                )

        # --- RAG source target entity references ---
        for rs in ai_layer.get("ragSources", []):
            for target in rs.get("targets", []):
                if isinstance(target, str) and target not in entity_names:
                    raise ValueError(
                        f"Entity '{target}' in ragSources "
                        f"(source '{rs.get('name', '')}') targets not found in entity_layer"
                    )

        # --- documentIngestion.targetRagSourceName ---
        doc_ingestion = ai_layer.get("documentIngestion") or {}
        target_rag = doc_ingestion.get("targetRagSourceName")
        if target_rag and target_rag not in rag_source_names:
            raise ValueError(
                f"documentIngestion.targetRagSourceName '{target_rag}' "
                "not found in ragSources"
            )

    # ------------------------------------------------------------------
    # Evaluators
    # ------------------------------------------------------------------

    def _validate_evaluators(self, evaluators: list, providers: list) -> None:
        """Req 1.8, 1.29: evaluator structure and constraints."""
        provider_names = {p["name"] for p in providers}
        seen_names: set[str] = set()
        for ev in evaluators:
            name = ev.get("name", "")
            if name in seen_names:
                raise ValueError(
                    f"Duplicate evaluator name '{name}' in evaluators"
                )
            seen_names.add(name)

            pname = ev.get("providerName", "")
            if pname not in provider_names:
                raise ValueError(
                    f"Provider '{pname}' referenced by evaluator "
                    f"'{name}' not found in providers array"
                )

            # Async evaluator with retry is invalid (Req 1.29)
            mode = ev.get("mode", "async")
            failure_action = ev.get("failureAction", "none")
            if mode == "async" and failure_action == "retry":
                raise ValueError(
                    f"Evaluator '{name}' has mode 'async' but failureAction "
                    "'retry' (retry requires sync)"
                )

            # Categorical evaluators/classification without categories
            ev_type = ev.get("type", "")
            scoring = ev.get("scoringMechanism", "")
            if scoring == "categorical" and not ev.get("categories"):
                raise ValueError(
                    f"Evaluator '{name}' uses categorical scoring but "
                    "has no 'categories' defined"
                )

    # ------------------------------------------------------------------
    # RAG sources
    # ------------------------------------------------------------------

    def _validate_rag_sources(self, sources: list, providers: list) -> None:
        """Req 1.7, 1.29: RAG source structure and constraints."""
        provider_names = {p["name"] for p in providers}
        seen_names: set[str] = set()
        for rs in sources:
            name = rs.get("name", "")
            if name in seen_names:
                raise ValueError(
                    f"Duplicate ragSource name '{name}' in ragSources"
                )
            seen_names.add(name)

            rs_type = rs.get("type", "")
            if rs_type not in VALID_RAG_TYPES:
                raise ValueError(
                    f"RAG source '{name}' has invalid type '{rs_type}'. "
                    f"Must be one of: {sorted(VALID_RAG_TYPES)}"
                )

            # Semantic RAG requires providerName (Req 1.29)
            if rs_type == "semantic":
                pname = rs.get("providerName")
                if not pname:
                    raise ValueError(
                        f"Semantic RAG source '{name}' requires 'providerName'"
                    )
                if pname not in provider_names:
                    raise ValueError(
                        f"Provider '{pname}' referenced by ragSource "
                        f"'{name}' not found in providers array"
                    )

    # ------------------------------------------------------------------
    # Orchestrator
    # ------------------------------------------------------------------

    def _validate_orchestrator(
        self, orch: dict, providers: list, mcp: list
    ) -> None:
        """Req 1.12, 1.29: orchestrator structure and constraints."""
        provider_names = {p["name"] for p in providers}

        pname = orch.get("providerName", "")
        if pname not in provider_names:
            raise ValueError(
                f"Provider '{pname}' referenced by orchestrator "
                "not found in providers array"
            )

        moderation = orch.get("moderation")
        if moderation:
            mod_provider = moderation.get("providerName", "")
            if mod_provider not in provider_names:
                raise ValueError(
                    f"Provider '{mod_provider}' referenced by "
                    "orchestrator.moderation not found in providers array"
                )
            failure_action = moderation.get("failureAction", "block")
            if failure_action not in VALID_MODERATION_FAILURE_ACTIONS:
                raise ValueError(
                    f"orchestrator.moderation.failureAction '{failure_action}' "
                    f"is invalid. Must be one of: {sorted(VALID_MODERATION_FAILURE_ACTIONS)}"
                )

    # ------------------------------------------------------------------
    # Document config
    # ------------------------------------------------------------------

    def _validate_document_config(
        self, ingestion: dict, processing: dict, rag: list
    ) -> None:
        """Req 1.29: documentProcessing requires documentIngestion."""
        proc_enabled = processing.get("enabled", False)
        ing_enabled = ingestion.get("enabled", False)

        if proc_enabled and not ing_enabled:
            raise ValueError(
                "documentProcessing requires documentIngestion to be enabled"
            )

        # Duplicate task names in documentProcessing
        tasks = processing.get("tasks", [])
        seen_task_names: set[str] = set()
        for task in tasks:
            tname = task.get("name", "")
            if tname in seen_task_names:
                raise ValueError(
                    f"Duplicate task name '{tname}' in documentProcessing.tasks"
                )
            seen_task_names.add(tname)

            # Classification tasks without categories
            if task.get("taskType") == "classification" and not task.get("categories"):
                raise ValueError(
                    f"Document processing task '{tname}' is classification type "
                    "but has no 'categories' defined"
                )

    # ------------------------------------------------------------------
    # Observability
    # ------------------------------------------------------------------

    def _validate_observability(self, obs: dict) -> None:
        """Req 1.29: observability constraints."""
        grafana = obs.get("grafana")
        if grafana:
            if not grafana.get("url"):
                raise ValueError(
                    "observability.grafana requires 'url' to be configured"
                )
            if not grafana.get("apiKeyEnvVar"):
                raise ValueError(
                    "observability.grafana requires 'apiKeyEnvVar' to be configured"
                )

        dashboards = obs.get("dashboards", [])
        seen_names: set[str] = set()
        for db in dashboards:
            dname = db.get("name", "")
            if dname in seen_names:
                raise ValueError(
                    f"Duplicate dashboard name '{dname}' in observability.dashboards"
                )
            seen_names.add(dname)

            panels = db.get("panels", [])
            if not panels:
                raise ValueError(
                    f"Dashboard '{dname}' in observability.dashboards "
                    "has empty panels array"
                )

    # ------------------------------------------------------------------
    # Token budget
    # ------------------------------------------------------------------

    def _validate_token_budget(self, budget: dict, providers: list) -> None:
        """Req 1.29: tokenBudget.providerOverrides must reference existing providers."""
        provider_names = {p["name"] for p in providers}
        overrides = budget.get("providerOverrides") or {}
        for pname in overrides:
            if pname not in provider_names:
                raise ValueError(
                    f"tokenBudget.providerOverrides references provider "
                    f"'{pname}' not found in providers array"
                )

    # ------------------------------------------------------------------
    # Chat session cleanup
    # ------------------------------------------------------------------

    def _validate_chat_session_cleanup(
        self, cleanup: dict, providers: list
    ) -> None:
        """Req 1.29: topicSummarization.providerName must exist."""
        provider_names = {p["name"] for p in providers}
        topic_sum = cleanup.get("topicSummarization")
        if topic_sum and topic_sum.get("enabled", False):
            pname = topic_sum.get("providerName", "")
            if pname not in provider_names:
                raise ValueError(
                    f"chatSessionCleanup.topicSummarization.providerName "
                    f"'{pname}' not found in providers array"
                )

    # ------------------------------------------------------------------
    # Audit log
    # ------------------------------------------------------------------

    def _validate_audit_log(self, audit: dict) -> None:
        """Req 1.29: loggedEvents must contain valid event types."""
        logged_events = audit.get("loggedEvents", [])
        for event in logged_events:
            if event not in VALID_AUDIT_EVENT_TYPES:
                raise ValueError(
                    f"auditLog.loggedEvents contains invalid event type "
                    f"'{event}'. Valid types: {sorted(VALID_AUDIT_EVENT_TYPES)}"
                )

    # ------------------------------------------------------------------
    # Duplicate name checks
    # ------------------------------------------------------------------

    def _check_duplicate_names(self, ai_layer: dict) -> None:
        """Req 1.29: check for duplicate names across named arrays."""
        # Providers already checked in _validate_providers
        # Evaluators already checked in _validate_evaluators
        # RAG sources already checked in _validate_rag_sources
        # Document processing tasks already checked in _validate_document_config
        # Dashboards already checked in _validate_observability
        pass

    # ------------------------------------------------------------------
    # State table conflicts
    # ------------------------------------------------------------------

    def _check_state_table_conflicts(self, ops: list) -> None:
        """Req 1.29: stateTable naming conflicts across standalone operations."""
        seen_tables: set[str] = set()
        for op in ops:
            st = op.get("stateTable")
            if st:
                tname = st.get("tableName", "")
                if tname in seen_tables:
                    raise ValueError(
                        f"stateTable naming conflict: table '{tname}' is used "
                        "by multiple standalone operations"
                    )
                seen_tables.add(tname)

    # ------------------------------------------------------------------
    # Warnings (non-fatal)
    # ------------------------------------------------------------------

    def _collect_warnings(
        self, ai_layer: dict, providers: list
    ) -> list[str]:
        """Req 1.30: collect non-fatal warnings."""
        warnings: list[str] = []
        provider_map = {p["name"]: p for p in providers}

        # Check all sections that reference providers for chatOptions/role warnings
        sections_with_provider = []

        # entityCapabilities
        for cap in ai_layer.get("entityCapabilities", []):
            pname = cap.get("providerName", "")
            provider = provider_map.get(pname)
            if provider:
                sections_with_provider.append(
                    (f"entityCapabilities[{cap.get('entityName', '')}]", cap, provider)
                )

        # standaloneOperations
        for op in ai_layer.get("standaloneOperations", []):
            pname = op.get("providerName", "")
            provider = provider_map.get(pname)
            if provider:
                sections_with_provider.append(
                    (f"standaloneOperations[{op.get('name', '')}]", op, provider)
                )

        # assistants
        for a in ai_layer.get("assistants", []):
            pname = a.get("providerName", "")
            provider = provider_map.get(pname)
            if provider:
                sections_with_provider.append(
                    (f"assistants[{a.get('name', '')}]", a, provider)
                )

        for section_label, section, provider in sections_with_provider:
            # Warning: systemPrompt overridden by rolePromptSequence (Req 1.30)
            if section.get("systemPrompt") and section.get("rolePromptSequence"):
                warnings.append(
                    f"{section_label}: systemPrompt is overridden by rolePromptSequence"
                )

            # Warning: chatOptions parameters not in supportedParameters (Req 1.30)
            chat_options = section.get("chatOptions") or {}
            supported_params = set(
                provider.get("supportedParameters", [])
            )
            param_fallbacks = provider.get("parameterFallbacks") or {}
            if supported_params and chat_options:
                for param in chat_options:
                    if param not in supported_params and param not in param_fallbacks:
                        warnings.append(
                            f"{section_label}: chatOptions parameter '{param}' "
                            f"not in provider '{provider['name']}' supportedParameters "
                            "and has no fallback configured"
                        )

            # Warning: rolePromptSequence roles not in supportedRoles (Req 1.30)
            rps = section.get("rolePromptSequence") or []
            supported_roles = set(
                provider.get("supportedRoles", ["system", "user", "assistant"])
            )
            role_fallbacks = provider.get("roleFallbacks") or {}
            for entry in rps:
                role = entry.get("role", "")
                if role not in supported_roles and role not in role_fallbacks:
                    warnings.append(
                        f"{section_label}: rolePromptSequence role '{role}' "
                        f"not in provider '{provider['name']}' supportedRoles "
                        "and has no fallback configured"
                    )

        # Warning: roleFallbacks for already-supported roles (Req 1.30)
        for p in providers:
            supported_roles = set(
                p.get("supportedRoles", ["system", "user", "assistant"])
            )
            role_fallbacks = p.get("roleFallbacks") or {}
            for role in role_fallbacks:
                if role in supported_roles:
                    warnings.append(
                        f"Provider '{p['name']}': roleFallbacks defines fallback "
                        f"for already-supported role '{role}'"
                    )

            # Warning: parameterFallbacks for already-supported parameters (Req 1.30)
            supported_params = set(p.get("supportedParameters", []))
            param_fallbacks = p.get("parameterFallbacks") or {}
            for param in param_fallbacks:
                if param in supported_params:
                    warnings.append(
                        f"Provider '{p['name']}': parameterFallbacks defines fallback "
                        f"for already-supported parameter '{param}'"
                    )

        return warnings
