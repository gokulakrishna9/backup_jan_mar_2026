"""Describer — rich, categorized summary of application definitions.

Usage (CLI):
    python app_def_manager/cli.py describe --app <app>
    python app_def_manager/cli.py describe --app <app> --entity <name>
    python app_def_manager/cli.py describe --app <app> --format markdown
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load_json(app_dir: Path, filename: str) -> dict:
    path = app_dir / filename
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _count_user_fields(fields: list[dict]) -> int:
    """Count user-defined fields (exclude PK, audit, soft-delete)."""
    auto_cols = {"created_at", "updated_at", "is_deleted"}
    count = 0
    for f in fields:
        col = f.get("columnName", f.get("name", ""))
        if f.get("isPrimaryKey") or f.get("primaryKey") or col in auto_cols:
            continue
        count += 1
    return count


def describe_app(app_name: str, fmt: str = "table") -> str:
    """Generate a rich description of all entities in an app.

    Args:
        app_name: Application name.
        fmt: Output format — "table" (default) or "markdown".

    Returns:
        Formatted string.
    """
    app_dir = Path("application_definitions") / app_name
    if not app_dir.exists():
        raise FileNotFoundError(f"Application '{app_name}' not found")

    entity_layer = _load_json(app_dir, "webflux_entity_layer.json")
    service_layer = _load_json(app_dir, "webflux_service_layer.json")
    repo_layer = _load_json(app_dir, "webflux_repository_layer.json")
    controller_layer = _load_json(app_dir, "webflux_controller_layer.json")

    # Build lookups
    svc_map = {s["entityName"]: s for s in service_layer.get("services", [])}
    repo_map = {r["entityName"]: r for r in repo_layer.get("repositories", [])}
    ctrl_map = {c["entityName"]: c for c in controller_layer.get("controllers", [])}

    entities = entity_layer.get("entities", [])
    if not entities:
        return f"  No entities found in '{app_name}'"

    rows = []
    for ent in entities:
        name = ent.get("className", "?")
        table = ent.get("tableName", "?")
        total_fields = len(ent.get("fields", []))
        user_fields = _count_user_fields(ent.get("fields", []))

        svc = svc_map.get(name, {})
        repo = repo_map.get(name, {})
        ctrl = ctrl_map.get(name, {})

        flags = []
        if svc.get("singleRecordPerUser") or repo.get("singleRecordPerUser"):
            flags.append("1-per-user")
        if svc.get("hasAuthorization"):
            flags.append("auth")
        if repo.get("enableCaching"):
            flags.append("cached")

        # Detect widget types from DTO layer
        base_path = ctrl.get("basePath", "")

        rows.append({
            "name": name,
            "table": table,
            "total_fields": total_fields,
            "user_fields": user_fields,
            "flags": flags,
            "base_path": base_path,
        })

    if fmt == "markdown":
        return _format_markdown(app_name, rows)
    return _format_table(app_name, rows)


def _format_table(app_name: str, rows: list[dict]) -> str:
    """Format as aligned ASCII table."""
    # Calculate column widths
    w_num = len(str(len(rows)))
    w_name = max(len(r["name"]) for r in rows)
    w_table = max(len(r["table"]) for r in rows)
    w_fields = 6  # "Fields"
    w_user = 4    # "User"
    w_flags = max((len(", ".join(r["flags"])) for r in rows), default=5)
    w_flags = max(w_flags, 5)
    w_path = max((len(r["base_path"]) for r in rows), default=4)
    w_path = max(w_path, 4)

    header = (
        f"  {'#':>{w_num}}  {'Entity':<{w_name}}  {'Table':<{w_table}}  "
        f"{'Fields':>{w_fields}}  {'User':>{w_user}}  {'Flags':<{w_flags}}  {'Path':<{w_path}}"
    )
    sep = "  " + "─" * (len(header) - 2)

    lines = [f"  {len(rows)} entities in '{app_name}':", "", header, sep]

    for i, r in enumerate(rows, 1):
        flags_str = ", ".join(r["flags"]) if r["flags"] else "—"
        line = (
            f"  {i:>{w_num}}  {r['name']:<{w_name}}  {r['table']:<{w_table}}  "
            f"{r['total_fields']:>{w_fields}}  {r['user_fields']:>{w_user}}  "
            f"{flags_str:<{w_flags}}  {r['base_path']:<{w_path}}"
        )
        lines.append(line)

    lines.append(sep)
    lines.append(f"  Total: {len(rows)} entities, {sum(r['user_fields'] for r in rows)} user fields")
    return "\n".join(lines)


def _format_markdown(app_name: str, rows: list[dict]) -> str:
    """Format as Markdown table."""
    lines = [
        f"## {app_name} — {len(rows)} entities",
        "",
        "| # | Entity | Table | Fields | User | Flags | Path |",
        "|---|--------|-------|--------|------|-------|------|",
    ]
    for i, r in enumerate(rows, 1):
        flags_str = ", ".join(r["flags"]) if r["flags"] else "—"
        lines.append(
            f"| {i} | {r['name']} | {r['table']} | {r['total_fields']} | "
            f"{r['user_fields']} | {flags_str} | `{r['base_path']}` |"
        )
    lines.append(f"\nTotal: {len(rows)} entities, {sum(r['user_fields'] for r in rows)} user fields")
    return "\n".join(lines)


def describe_entity(app_name: str, entity_name: str) -> str:
    """Generate a detailed description of a single entity."""
    app_dir = Path("application_definitions") / app_name
    if not app_dir.exists():
        raise FileNotFoundError(f"Application '{app_name}' not found")

    entity_layer = _load_json(app_dir, "webflux_entity_layer.json")
    service_layer = _load_json(app_dir, "webflux_service_layer.json")
    repo_layer = _load_json(app_dir, "webflux_repository_layer.json")
    controller_layer = _load_json(app_dir, "webflux_controller_layer.json")
    dto_layer = _load_json(app_dir, "webflux_dto_layer.json")

    # Find entity
    ent = None
    for e in entity_layer.get("entities", []):
        if e.get("className") == entity_name:
            ent = e
            break
    if not ent:
        raise ValueError(f"Entity '{entity_name}' not found in '{app_name}'")

    svc = next((s for s in service_layer.get("services", []) if s["entityName"] == entity_name), {})
    repo = next((r for r in repo_layer.get("repositories", []) if r["entityName"] == entity_name), {})
    ctrl = next((c for c in controller_layer.get("controllers", []) if c["entityName"] == entity_name), {})

    auto_cols = {"created_at", "updated_at", "is_deleted"}

    lines = [
        f"  Entity: {entity_name}",
        f"  Table:  {ent.get('tableName', '?')}",
        f"  Path:   {ctrl.get('basePath', '?')}",
        "",
        "  Flags:",
        f"    hasAuthorization:    {svc.get('hasAuthorization', False)}",
        f"    singleRecordPerUser: {svc.get('singleRecordPerUser', False)}",
        f"    hasSoftDelete:       {ent.get('hasSoftDelete', False)}",
        f"    hasAuditFields:      {ent.get('hasAuditFields', False)}",
        f"    enableCaching:       {repo.get('enableCaching', False)}",
        "",
        "  Fields:",
    ]

    for f in ent.get("fields", []):
        col = f.get("columnName", "?")
        field = f.get("fieldName", "?")
        jtype = f.get("javaType", "?")
        pk = " [PK]" if f.get("isPrimaryKey") else ""
        auto = " [auto]" if col in auto_cols or f.get("isPrimaryKey") else ""
        nullable = "" if f.get("isNullable", True) else " NOT NULL"
        lines.append(f"    {field:<30} {jtype:<20} {col}{pk}{auto}{nullable}")

    # Show DTO widget annotations if any
    dto_defs = [d for d in dto_layer.get("dtos", []) if d.get("entityName") == entity_name]
    widgets = []
    for dto in dto_defs:
        for df in dto.get("fields", []):
            w = df.get("fieldWidget")
            if w:
                widgets.append((df["fieldName"], w))
    if widgets:
        lines.append("")
        lines.append("  Widget Mappings:")
        for fname, widget in widgets:
            lines.append(f"    {fname:<30} → {widget}")

    # Show endpoints
    endpoints = ctrl.get("endpoints", {})
    if endpoints:
        lines.append("")
        lines.append("  Endpoints:")
        for ep_name, ep in endpoints.items():
            if isinstance(ep, dict) and ep.get("enabled"):
                auth = "🔒" if ep.get("requiresAuth") else "🔓"
                lines.append(f"    {auth} {ep.get('method', '?'):6} {ctrl.get('basePath', '')}{ep.get('path', '')}")

    return "\n".join(lines)


# ── AI Layer Description ────────────────────────────────────────────────


def describe_ai_layer(app_name: str, fmt: str = "table") -> str:
    """Generate a formatted summary of the AI layer configuration.

    Args:
        app_name: Application name.
        fmt: Output format — "table" (default) or "markdown".

    Returns:
        Formatted string.
    """
    app_dir = Path("application_definitions") / app_name
    if not app_dir.exists():
        raise FileNotFoundError(f"Application '{app_name}' not found")

    ai = _load_json(app_dir, "webflux_ai_layer.json")
    if not ai:
        return f"  No AI layer configuration found for '{app_name}'"

    sections = []

    # Schema version
    sections.append(("Schema Version", ai.get("schemaVersion", "?")))

    # Providers
    providers = ai.get("providers", [])
    if providers:
        prov_lines = []
        for p in providers:
            emb = p.get("embeddingModel", p.get("model", ""))
            res = "✓" if p.get("resilience") else "—"
            prov_lines.append(f"{p['name']} ({p['type']}, {p['model']}, emb={emb}, resilience={res})")
        sections.append(("Providers", "\n".join(prov_lines)))
    else:
        sections.append(("Providers", "None"))

    # Entity Capabilities
    caps = ai.get("entityCapabilities", [])
    if caps:
        cap_lines = []
        for c in caps:
            ops = ", ".join(c.get("enabledOperations", []))
            rag = ", ".join(c.get("ragSourceNames", [])) or "—"
            evals = ", ".join(c.get("evaluatorNames", [])) or "—"
            cap_lines.append(f"{c['entityName']} → {c['providerName']} [{ops}] RAG={rag} Eval={evals}")
        sections.append(("Entity Capabilities", "\n".join(cap_lines)))
    else:
        sections.append(("Entity Capabilities", "None"))

    # Standalone Operations
    ops = ai.get("standaloneOperations", [])
    if ops:
        op_lines = []
        for o in ops:
            actions = ", ".join(o.get("enabledActions", []))
            st_table = "✓" if o.get("stateTable") else "—"
            op_lines.append(f"{o['name']} ({o.get('type', '?')}) → {o['providerName']} [{actions}] state={st_table}")
        sections.append(("Standalone Operations", "\n".join(op_lines)))
    else:
        sections.append(("Standalone Operations", "None"))

    # Assistants
    assistants = ai.get("assistants", [])
    if assistants:
        a_lines = []
        for a in assistants:
            ttl = a.get("sessionTtlDays", "default")
            a_lines.append(f"{a['name']} → {a['providerName']} (window={a.get('memoryWindowSize', 20)}, ttl={ttl})")
        sections.append(("Assistants", "\n".join(a_lines)))
    else:
        sections.append(("Assistants", "None"))

    # RAG Sources
    rags = ai.get("ragSources", [])
    if rags:
        r_lines = []
        for r in rags:
            enabled = "✓" if r.get("enabled") else "✗"
            sec = r.get("securityMode", "public")
            r_lines.append(f"{r['name']} ({r['type']}, {enabled}, security={sec})")
        sections.append(("RAG Sources", "\n".join(r_lines)))
    else:
        sections.append(("RAG Sources", "None"))

    # Evaluators
    evals = ai.get("evaluators", [])
    if evals:
        e_lines = []
        for e in evals:
            e_lines.append(f"{e['name']} ({e['type']}, {e['scoringMechanism']}, mode={e.get('mode', 'async')})")
        sections.append(("Evaluators", "\n".join(e_lines)))
    else:
        sections.append(("Evaluators", "None"))

    # Vector Store
    vs = ai.get("vectorStore")
    sections.append(("Vector Store", f"{vs['type']} ({vs.get('host', '?')}:{vs.get('port', '?')})" if vs else "Not configured"))

    # Document Ingestion/Processing
    di = ai.get("documentIngestion")
    dp = ai.get("documentProcessing")
    sections.append(("Document Ingestion", "Enabled" if di and di.get("enabled") else "Disabled"))
    sections.append(("Document Processing", "Enabled" if dp and dp.get("enabled") else "Disabled"))

    # Orchestrator
    orch = ai.get("orchestrator")
    if orch:
        ps = orch.get("promptSecurity", {})
        sg = "✓" if ps.get("safeGuardAdvisor", {}).get("enabled") else "✗"
        cw = "✓" if ps.get("canaryWordAdvisor", {}).get("enabled") else "✗"
        mod = orch.get("moderation", {})
        mod_str = "✓" if mod.get("enabled") else "✗"
        sections.append(("Orchestrator", f"{orch['providerName']} (safeguard={sg}, canary={cw}, moderation={mod_str})"))
    else:
        sections.append(("Orchestrator", "Not configured"))

    # MCP Servers
    mcps = ai.get("mcpServers", [])
    if mcps:
        m_lines = []
        for m in mcps:
            enabled = "✓" if m.get("enabled") else "✗"
            roles = ", ".join(m.get("requiredRoles", []))
            m_lines.append(f"{m['name']} ({m['transportType']}, {enabled}, roles=[{roles}])")
        sections.append(("MCP Servers", "\n".join(m_lines)))
    else:
        sections.append(("MCP Servers", "None"))

    # Feature Flags
    flags = []
    if ai.get("observability", {}) and ai["observability"].get("enabled"):
        flags.append("observability")
    if ai.get("tokenBudget", {}) and ai["tokenBudget"].get("enabled"):
        flags.append("tokenBudget")
    if ai.get("rateLimiting"):
        flags.append("rateLimiting")
    if ai.get("auditLog", {}) and ai["auditLog"].get("enabled"):
        flags.append("auditLog")
    if ai.get("chatSessionCleanup", {}) and ai["chatSessionCleanup"].get("enabled"):
        flags.append("sessionCleanup")
    sections.append(("Feature Flags", ", ".join(flags) if flags else "None"))

    if fmt == "markdown":
        return _format_ai_markdown(app_name, sections)
    return _format_ai_table(app_name, sections)


def _format_ai_table(app_name: str, sections: list[tuple[str, str]]) -> str:
    """Format AI layer summary as aligned ASCII table."""
    w_label = max(len(s[0]) for s in sections)
    lines = [f"  AI Layer for '{app_name}':", ""]
    for label, value in sections:
        for i, vline in enumerate(value.split("\n")):
            if i == 0:
                lines.append(f"  {label:<{w_label}}  {vline}")
            else:
                lines.append(f"  {'':<{w_label}}  {vline}")
    return "\n".join(lines)


def _format_ai_markdown(app_name: str, sections: list[tuple[str, str]]) -> str:
    """Format AI layer summary as Markdown."""
    lines = [f"## AI Layer — {app_name}", ""]
    for label, value in sections:
        if "\n" in value:
            lines.append(f"### {label}")
            for vline in value.split("\n"):
                lines.append(f"- {vline}")
            lines.append("")
        else:
            lines.append(f"- **{label}**: {value}")
    return "\n".join(lines)


def describe_ai_react(app_name: str, fmt: str = "table") -> str:
    """Generate a formatted summary of the React AI configuration.

    Args:
        app_name: Application name.
        fmt: Output format — "table" (default) or "markdown".

    Returns:
        Formatted string.
    """
    app_dir = Path("application_definitions") / app_name
    if not app_dir.exists():
        raise FileNotFoundError(f"Application '{app_name}' not found")

    react = _load_json(app_dir, "react_ai_config.json")
    if not react:
        return f"  No React AI configuration found for '{app_name}'"

    sections = []

    sections.append(("Schema Version", react.get("schemaVersion", "?")))

    # Chat Panel
    cp = react.get("chatPanel", {})
    if cp.get("enabled"):
        streaming = "✓" if cp.get("streamingEnabled", True) else "✗"
        sections.append(("Chat Panel", f"Enabled ({cp.get('position', '?')}, streaming={streaming}, assistant={cp.get('defaultAssistant', '—')})"))
    else:
        sections.append(("Chat Panel", "Disabled"))

    # Entity Features
    ef = react.get("entityFeatures", [])
    if ef:
        ef_lines = []
        for f in ef:
            search = "✓" if f.get("smartSearch") else "✗"
            gen_fields = ", ".join(g.get("fieldName", "?") for g in f.get("contentGeneration", []))
            sug_fields = ", ".join(s.get("fieldName", "?") for s in f.get("suggestions", []))
            ef_lines.append(f"{f['entityName']} (search={search}, gen=[{gen_fields}], sug=[{sug_fields}])")
        sections.append(("Entity Features", "\n".join(ef_lines)))
    else:
        sections.append(("Entity Features", "None"))

    # Standalone Features
    sf = react.get("standaloneFeatures", [])
    if sf:
        sf_lines = []
        for f in sf:
            sf_lines.append(f"{f['operationName']} → {f.get('pageRoute', '?')} ({f.get('componentType', '?')})")
        sections.append(("Standalone Features", "\n".join(sf_lines)))
    else:
        sections.append(("Standalone Features", "None"))

    # Theme
    theme = react.get("theme", {})
    sections.append(("Theme", f"accent={theme.get('accentColor', '?')}, bubble={theme.get('chatBubbleStyle', '?')}, loading={theme.get('loadingAnimation', '?')}"))

    # Evaluation Display
    ed = react.get("evaluationDisplay")
    if ed and ed.get("enabled"):
        sections.append(("Evaluation Display", f"Enabled (badge={ed.get('badgeStyle', '?')})"))
    else:
        sections.append(("Evaluation Display", "Disabled"))

    # RAG Features
    rf = react.get("ragFeatures")
    if rf and rf.get("enabled"):
        sections.append(("RAG Features", f"Enabled (admin={rf.get('adminPageRoute', '?')})"))
    else:
        sections.append(("RAG Features", "Disabled"))

    if fmt == "markdown":
        return _format_ai_markdown(app_name + " React AI", sections)
    return _format_ai_table(app_name + " React AI", sections)
