"""Tool command router — maps Kafka command types to workspace tool functions.

Every tool command arriving on ``commands.tools`` is dispatched here.
The handler is a thin router: it looks up the command type in TOOL_MAP
and delegates execution to ``execute_and_respond`` from tool_pipeline.py,
which owns the single try/except/publish pattern.

Subprocess-based tools (REAW, Discussion Tracker, GitHub Crawler,
App Validator, Theme Scraper, Dummy Data) use ``run_tool_subprocess``.
Direct-import tools (App Def Manager, Definition Editor, DB Manager)
call Python functions in-process.

Generation commands (generate_full, generate_incremental, generate_sql_only,
generate_react) are intercepted before TOOL_MAP lookup and routed to the
JobManager, which starts background threads and streams progress to
``events.jobs``.
"""

import json
import logging
from pathlib import Path

from workspace_web_app.engine.config import APPLICATION_DEFINITIONS_DIR, TOOL_PATHS, WORKSPACE_ROOT
from workspace_web_app.engine.handlers.tool_pipeline import execute_and_respond
from workspace_web_app.engine.utils.envelope import build_envelope
from workspace_web_app.engine.utils.response import error_response, success_response
from workspace_web_app.engine.utils.subprocess_run import run_tool_subprocess

logger = logging.getLogger(__name__)

APP_DEFS_ROOT = Path(APPLICATION_DEFINITIONS_DIR)

# ---------------------------------------------------------------------------
# Thin wrapper functions — each does ONE thing: call the workspace tool
# ---------------------------------------------------------------------------

# ── App Def Manager (direct import) ──────────────────────────────────────


def _scaffold_app(payload: dict) -> dict:
    """Scaffold a new application definition set."""
    from app_def_manager.scaffolder import Scaffolder

    scaffolder = Scaffolder()
    result = scaffolder.scaffold_application(
        app_name=payload["app"],
        entity_descriptions=payload.get("entities", []),
        db_name=payload.get("db_name", payload["app"]),
    )
    return result


def _add_entity(payload: dict) -> list[str]:
    """Add an entity to an application."""
    from app_def_manager.crud import CRUDManager

    mgr = CRUDManager(payload["app"])
    return mgr.add_entity(name=payload["name"], fields=payload.get("fields", []))


def _remove_entity(payload: dict) -> list[str]:
    """Remove an entity from an application."""
    from app_def_manager.crud import CRUDManager

    mgr = CRUDManager(payload["app"])
    return mgr.remove_entity(name=payload["name"])


def _add_field(payload: dict) -> list[str]:
    """Add a field to an entity."""
    from app_def_manager.crud import CRUDManager

    mgr = CRUDManager(payload["app"])
    return mgr.add_field(entity_name=payload["entity"], field=payload["field"])


def _remove_field(payload: dict) -> list[str]:
    """Remove a field from an entity."""
    from app_def_manager.crud import CRUDManager

    mgr = CRUDManager(payload["app"])
    return mgr.remove_field(entity_name=payload["entity"], field_name=payload["field_name"])


def _modify_field(payload: dict) -> list[str]:
    """Modify a field on an entity."""
    from app_def_manager.crud import CRUDManager

    mgr = CRUDManager(payload["app"])
    return mgr.modify_field(
        entity_name=payload["entity"],
        field_name=payload["field_name"],
        updates=payload["updates"],
    )


def _add_endpoint(payload: dict) -> list[str]:
    """Add a custom endpoint to an entity."""
    from app_def_manager.crud import CRUDManager

    mgr = CRUDManager(payload["app"])
    return mgr.add_endpoint(entity_name=payload["entity"], endpoint=payload["endpoint"])


def _remove_endpoint(payload: dict) -> list[str]:
    """Remove a custom endpoint from an entity."""
    from app_def_manager.crud import CRUDManager

    mgr = CRUDManager(payload["app"])
    return mgr.remove_endpoint(entity_name=payload["entity"], endpoint_name=payload["endpoint_name"])


def _add_query(payload: dict) -> list[str]:
    """Add a custom query to an entity."""
    from app_def_manager.crud import CRUDManager

    mgr = CRUDManager(payload["app"])
    return mgr.add_query(entity_name=payload["entity"], query=payload["query"])


def _remove_query(payload: dict) -> list[str]:
    """Remove a custom query from an entity."""
    from app_def_manager.crud import CRUDManager

    mgr = CRUDManager(payload["app"])
    return mgr.remove_query(entity_name=payload["entity"], query_name=payload["query_name"])


def _add_relationship(payload: dict) -> list[str]:
    """Add a relationship between entities."""
    from app_def_manager.crud import CRUDManager

    mgr = CRUDManager(payload["app"])
    return mgr.add_relationship(relationship=payload["relationship"])


def _remove_relationship(payload: dict) -> list[str]:
    """Remove a relationship between entities."""
    from app_def_manager.crud import CRUDManager

    mgr = CRUDManager(payload["app"])
    return mgr.remove_relationship(source=payload["source"], target=payload["target"])


def _app_status(payload: dict) -> dict:
    """Get dirty/clean file status for an application."""
    from app_def_manager.status_tracker import StatusTracker

    app_dir = APP_DEFS_ROOT / payload["app"]
    tracker = StatusTracker(app_dir)
    dirty = tracker.get_dirty_files()
    clean = tracker.get_clean_files()
    return {"app": payload["app"], "dirty": dirty, "clean": clean}


def _list_apps(payload: dict) -> list[str]:
    """List all application definitions."""
    if not APP_DEFS_ROOT.exists():
        return []
    return sorted(
        d.name for d in APP_DEFS_ROOT.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )


def _list_entities(payload: dict) -> list[dict]:
    """List entities in an application."""
    import json as _json

    app_dir = APP_DEFS_ROOT / payload["app"]
    entity_layer_path = app_dir / "webflux_entity_layer.json"
    if not entity_layer_path.exists():
        raise FileNotFoundError(f"Entity layer not found for '{payload['app']}'")
    data = _json.loads(entity_layer_path.read_text(encoding="utf-8"))
    entities = data.get("entities", [])
    return [
        {
            "className": e.get("className"),
            "tableName": e.get("tableName"),
            "fieldCount": len(e.get("fields", [])),
        }
        for e in entities
    ]


def _bulk_update(payload: dict) -> dict:
    """Bulk-update entity-level flags across definition layers."""
    from app_def_manager.bulk_updater import bulk_update

    return bulk_update(
        app_name=payload["app"],
        entity_names=payload.get("entities", ["ALL"]),
        updates=payload.get("updates", {}),
    )


def _describe_app(payload: dict) -> str:
    """Get a rich description of an application."""
    from app_def_manager.describer import describe_app

    return describe_app(
        app_name=payload["app"],
        fmt=payload.get("format", "table"),
    )


# ── Definition Editor (direct import) ────────────────────────────────────


def _definition_get(payload: dict) -> object:
    """Get a definition value (optionally at a JSON path)."""
    from definition_editor.editor import DefinitionEditor

    app_dir = str(APP_DEFS_ROOT / payload["app"])
    editor = DefinitionEditor(app_dir)
    return editor.get(name=payload["file"], path=payload.get("path"))


def _definition_set(payload: dict) -> dict:
    """Set a definition value at a JSON path."""
    from definition_editor.editor import DefinitionEditor

    app_dir = str(APP_DEFS_ROOT / payload["app"])
    editor = DefinitionEditor(app_dir)
    editor.set(name=payload["file"], path=payload["path"], value=payload["value"])
    return {"file": payload["file"], "path": payload["path"], "status": "updated"}


def _definition_list(payload: dict) -> list[str]:
    """List definition files for an application."""
    from definition_editor.editor import DefinitionEditor

    app_dir = str(APP_DEFS_ROOT / payload["app"])
    editor = DefinitionEditor(app_dir)
    return editor.list_files(prefix=payload.get("prefix"))


# ── DB Manager (direct import) ───────────────────────────────────────────


def _db_create(payload: dict) -> dict:
    """Create a database."""
    from db_manager.db_manager import create_database

    create_database(name=payload["name"], **_db_conn_kwargs(payload))
    return {"name": payload["name"], "status": "created"}


def _db_drop(payload: dict) -> dict:
    """Drop a database."""
    from db_manager.db_manager import drop_database

    drop_database(name=payload["name"], **_db_conn_kwargs(payload))
    return {"name": payload["name"], "status": "dropped"}


def _db_list(payload: dict) -> list[str]:
    """List databases."""
    from db_manager.db_manager import list_databases

    return list_databases(**_db_conn_kwargs(payload))


def _db_setup(payload: dict) -> dict:
    """Run the full database setup workflow."""
    from db_manager.db_manager import setup_database

    result = setup_database(name=payload["name"], **_db_conn_kwargs(payload))
    return result


def _db_query(payload: dict) -> dict:
    """Execute a query against a database."""
    from db_manager.db_manager import query_database

    return query_database(
        name=payload["name"],
        query_json=json.dumps(payload["query"]),
        **_db_conn_kwargs(payload),
    )


def _db_conn_kwargs(payload: dict) -> dict:
    """Extract optional DB connection kwargs from payload."""
    kwargs = {}
    for key in ("host", "port", "user", "password"):
        if key in payload:
            kwargs[key] = payload[key]
    return kwargs


# ── Subprocess-based tools ───────────────────────────────────────────────
# These tools are invoked via CLI subprocess because of module name
# conflicts (REAW) or because they are standalone CLI tools.


async def _validate_backend(payload: dict) -> dict:
    """Run backend validation via subprocess."""
    cmd = f"python {TOOL_PATHS['app_validator']} backend --definitions {APP_DEFS_ROOT / payload['app']}"
    return await run_tool_subprocess(cmd)


async def _validate_frontend(payload: dict) -> dict:
    """Run frontend validation via subprocess."""
    cmd = f"python {TOOL_PATHS['app_validator']} frontend --definitions {APP_DEFS_ROOT / payload['app']}"
    return await run_tool_subprocess(cmd)


async def _validate_api_coverage(payload: dict) -> dict:
    """Run API coverage validation via subprocess."""
    cmd = f"python {TOOL_PATHS['app_validator']} api-coverage --definitions {APP_DEFS_ROOT / payload['app']}"
    if "backend_url" in payload:
        cmd += f" --backend-url {payload['backend_url']}"
    return await run_tool_subprocess(cmd)


async def _theme_scrape(payload: dict) -> dict:
    """Scrape a theme via subprocess."""
    cmd = f"python {TOOL_PATHS['theme_scraper']} --url {payload['url']}"
    if "output" in payload:
        cmd += f" --output {payload['output']}"
    return await run_tool_subprocess(cmd)


async def _dummy_data(payload: dict) -> dict:
    """Generate dummy data via subprocess."""
    cmd = f"python {TOOL_PATHS['dummy_data']}"
    if "app" in payload:
        cmd += f" --input generated_application/{payload['app']}/schema.sql"
        cmd += f" --app-dir generated_application/{payload['app']}/webflux_app"
    if "leaf_records" in payload:
        cmd += f" --leaf-records {payload['leaf_records']}"
    return await run_tool_subprocess(cmd)


# ── Discussion Tracker (subprocess) ──────────────────────────────────────


async def _discussion_log(payload: dict) -> dict:
    """Log a discussion entry via subprocess."""
    cmd = f"python {TOOL_PATHS['discussion_tracker']} log"
    if "message" in payload:
        cmd += f" --message {json.dumps(payload['message'])}"
    return await run_tool_subprocess(cmd)


async def _discussion_task(payload: dict) -> dict:
    """Create a discussion task via subprocess."""
    cmd = f"python {TOOL_PATHS['discussion_tracker']} task"
    if "title" in payload:
        cmd += f" --title {json.dumps(payload['title'])}"
    if "description" in payload:
        cmd += f" --description {json.dumps(payload['description'])}"
    return await run_tool_subprocess(cmd)


async def _discussion_decision(payload: dict) -> dict:
    """Record a discussion decision via subprocess."""
    cmd = f"python {TOOL_PATHS['discussion_tracker']} decision"
    if "title" in payload:
        cmd += f" --title {json.dumps(payload['title'])}"
    if "rationale" in payload:
        cmd += f" --rationale {json.dumps(payload['rationale'])}"
    return await run_tool_subprocess(cmd)


async def _discussion_complete(payload: dict) -> dict:
    """Mark a discussion task as complete via subprocess."""
    cmd = f"python {TOOL_PATHS['discussion_tracker']} complete --id {payload['id']}"
    return await run_tool_subprocess(cmd)


async def _discussion_start(payload: dict) -> dict:
    """Mark a discussion task as in-progress via subprocess."""
    cmd = f"python {TOOL_PATHS['discussion_tracker']} start --id {payload['id']}"
    if "notes" in payload:
        cmd += f" --notes {json.dumps(payload['notes'])}"
    return await run_tool_subprocess(cmd)


async def _discussion_list(payload: dict) -> dict:
    """List discussions via subprocess."""
    cmd = f"python {TOOL_PATHS['discussion_tracker']} list"
    if "type" in payload:
        cmd += f" --type {payload['type']}"
    return await run_tool_subprocess(cmd)


async def _discussion_search(payload: dict) -> dict:
    """Search discussions via subprocess."""
    cmd = f"python {TOOL_PATHS['discussion_tracker']} search --query {json.dumps(payload['query'])}"
    return await run_tool_subprocess(cmd)


async def _discussion_summary(payload: dict) -> dict:
    """Get discussion summary via subprocess."""
    cmd = f"python {TOOL_PATHS['discussion_tracker']} summary"
    return await run_tool_subprocess(cmd)


# ── GitHub Crawler (subprocess) ──────────────────────────────────────────


async def _github_list_repos(payload: dict) -> dict:
    """List GitHub repos for a user via subprocess."""
    cmd = f"python -m github_crawler.cli list-repos --user {payload['user']} --json"
    return await run_tool_subprocess(cmd)


async def _github_repo_info(payload: dict) -> dict:
    """Get GitHub repo info via subprocess."""
    cmd = f"python -m github_crawler.cli repo-info --owner {payload['owner']} --repo {payload['repo']} --json"
    return await run_tool_subprocess(cmd)


async def _github_tree(payload: dict) -> dict:
    """Browse a GitHub repo file tree via subprocess."""
    cmd = f"python -m github_crawler.cli tree --owner {payload['owner']} --repo {payload['repo']} --json"
    if "branch" in payload:
        cmd += f" --branch {payload['branch']}"
    return await run_tool_subprocess(cmd)


async def _github_read_file(payload: dict) -> dict:
    """Read a file from a GitHub repo via subprocess."""
    cmd = f"python -m github_crawler.cli read-file --owner {payload['owner']} --repo {payload['repo']} --path {payload['path']} --json"
    return await run_tool_subprocess(cmd)


async def _github_summarize(payload: dict) -> dict:
    """Generate a summary of a GitHub user's repos via subprocess."""
    cmd = f"python -m github_crawler.cli summarize --user {payload['user']} --json"
    return await run_tool_subprocess(cmd)


# ── AI Config (LLMProviderManager) ───────────────────────────────────────


async def _ai_config_get(payload: dict) -> dict:
    """Get AI configuration: model registry, active model, params, provider status."""
    from workspace_web_app.engine.services.llm_provider_manager import LLMProviderManager

    mgr = LLMProviderManager()
    return {
        "active_model": mgr.get_active_model(),
        "model_params": mgr.get_model_params(),
        "model_registry": mgr.get_model_registry(),
    }


async def _ai_config_update(payload: dict) -> dict:
    """Update AI configuration: active model, params, custom endpoints."""
    from workspace_web_app.engine.services.llm_provider_manager import LLMProviderManager

    mgr = LLMProviderManager()

    if "active_model" in payload:
        mgr.set_active_model(payload["active_model"])

    if "model_params" in payload:
        mgr.update_model_params(payload["model_params"])

    if "custom_endpoint" in payload:
        ep = payload["custom_endpoint"]
        if ep.get("action") == "remove":
            mgr.remove_custom_endpoint(ep["name"])
        else:
            mgr.add_custom_endpoint(
                name=ep["name"],
                base_url=ep.get("base_url", ""),
                api_key=ep.get("api_key", ""),
                models=ep.get("models", []),
            )

    if payload.get("save", False):
        mgr.save_config()

    return {
        "active_model": mgr.get_active_model(),
        "model_params": mgr.get_model_params(),
        "status": "updated",
    }


async def _ai_health_check(payload: dict) -> dict:
    """Run a health check against a specific LLM provider."""
    from workspace_web_app.engine.services.llm_provider_manager import LLMProviderManager

    mgr = LLMProviderManager()
    provider = payload.get("provider", "")
    if not provider:
        raise ValueError("Missing required field: provider")
    return await mgr.health_check(provider)


# ── Generation type mapping (handled by JobManager via ToolHandler) ───────

_GENERATION_TYPE_MAP: dict[str, str] = {
    "generate_full": "full",
    "generate_incremental": "incremental",
    "generate_sql_only": "sql_only",
    "generate_react": "react",
}


# ---------------------------------------------------------------------------
# TOOL_MAP — single lookup table for all command types
# ---------------------------------------------------------------------------

TOOL_MAP: dict[str, callable] = {
    # App Def Manager
    "scaffold_app": _scaffold_app,
    "add_entity": _add_entity,
    "remove_entity": _remove_entity,
    "add_field": _add_field,
    "remove_field": _remove_field,
    "modify_field": _modify_field,
    "add_endpoint": _add_endpoint,
    "remove_endpoint": _remove_endpoint,
    "add_query": _add_query,
    "remove_query": _remove_query,
    "add_relationship": _add_relationship,
    "remove_relationship": _remove_relationship,
    "app_status": _app_status,
    "list_apps": _list_apps,
    "list_entities": _list_entities,
    "bulk_update": _bulk_update,
    "describe_app": _describe_app,
    # Definition Editor
    "definition_get": _definition_get,
    "definition_set": _definition_set,
    "definition_list": _definition_list,
    # DB Manager
    "db_create": _db_create,
    "db_drop": _db_drop,
    "db_list": _db_list,
    "db_setup": _db_setup,
    "db_query": _db_query,
    # App Validator (subprocess)
    "validate_backend": _validate_backend,
    "validate_frontend": _validate_frontend,
    "validate_api_coverage": _validate_api_coverage,
    # Theme Scraper (subprocess)
    "theme_scrape": _theme_scrape,
    # Dummy Data (subprocess)
    "dummy_data": _dummy_data,
    # Discussion Tracker (subprocess)
    "discussion_log": _discussion_log,
    "discussion_task": _discussion_task,
    "discussion_decision": _discussion_decision,
    "discussion_complete": _discussion_complete,
    "discussion_start": _discussion_start,
    "discussion_list": _discussion_list,
    "discussion_search": _discussion_search,
    "discussion_summary": _discussion_summary,
    # GitHub Crawler (subprocess)
    "github_list_repos": _github_list_repos,
    "github_repo_info": _github_repo_info,
    "github_tree": _github_tree,
    "github_read_file": _github_read_file,
    "github_summarize": _github_summarize,
    # AI Config (LLMProviderManager)
    "ai_config_get": _ai_config_get,
    "ai_config_update": _ai_config_update,
    "ai_health_check": _ai_health_check,
    # Generation commands are handled by JobManager via _handle_generation
    # (not in TOOL_MAP — intercepted before lookup)
}

RESULTS_TOOLS_TOPIC = "results.tools"


# ---------------------------------------------------------------------------
# ToolHandler — the thin router
# ---------------------------------------------------------------------------


class ToolHandler:
    """Routes ``commands.tools`` messages to workspace tool functions.

    Usage::

        handler = ToolHandler(producer, job_manager)
        await handler.handle(message)
    """

    def __init__(self, producer, job_manager=None):
        self.producer = producer
        self.job_manager = job_manager

    async def handle(self, message: dict) -> None:
        """Dispatch a tool command message.

        1. If it's a generation command and a JobManager is available,
           delegate to ``_handle_generation``.
        2. Otherwise look up the command type in TOOL_MAP.
        3. Call ``execute_and_respond`` with the mapped function.
        4. For unknown types, publish an error response.
        """
        cmd_type = message.get("type", "")
        correlation_id = message.get("correlationId", "")
        session_id = message.get("sessionId", "")
        app_name = message.get("appName", "")
        payload = message.get("payload", {})

        # Generation commands are handled by JobManager when available
        if cmd_type in _GENERATION_TYPE_MAP and self.job_manager is not None:
            await self._handle_generation(
                cmd_type, payload, correlation_id, session_id, app_name,
            )
            return

        tool_fn = TOOL_MAP.get(cmd_type)

        if tool_fn is None:
            logger.warning("Unknown tool command type: %s (cid=%s)", cmd_type, correlation_id)
            envelope = build_envelope(
                type=cmd_type,
                payload=error_response(f"Unknown command type: {cmd_type}"),
                correlation_id=correlation_id,
                session_id=session_id,
                app_name=app_name,
            )
            await self.producer.send_and_wait(
                RESULTS_TOOLS_TOPIC,
                json.dumps(envelope).encode("utf-8"),
            )
            return

        await execute_and_respond(
            tool_fn=tool_fn,
            payload=payload,
            producer=self.producer,
            correlation_id=correlation_id,
            cmd_type=cmd_type,
            session_id=session_id,
            app_name=app_name,
        )

    async def _handle_generation(
        self,
        cmd_type: str,
        payload: dict,
        correlation_id: str,
        session_id: str,
        app_name: str,
    ) -> None:
        """Start a generation job via JobManager and publish the job_id."""
        gen_type = _GENERATION_TYPE_MAP[cmd_type]
        app = payload.get("app", app_name)

        try:
            job_id = self.job_manager.start_job(
                app=app,
                gen_type=gen_type,
                producer=self.producer,
                correlation_id=correlation_id,
                session_id=session_id,
            )
            result_payload = success_response({"job_id": job_id})
        except (ValueError, Exception) as exc:
            logger.error("Generation %s failed (cid=%s): %s", cmd_type, correlation_id, exc)
            result_payload = error_response(str(exc))

        envelope = build_envelope(
            type=cmd_type,
            payload=result_payload,
            correlation_id=correlation_id,
            session_id=session_id,
            app_name=app_name,
        )
        await self.producer.send_and_wait(
            RESULTS_TOOLS_TOPIC,
            json.dumps(envelope).encode("utf-8"),
        )
