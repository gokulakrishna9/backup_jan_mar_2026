"""CLI for the App Definition Manager.

Usage:
    py app_def_manager/cli.py <command> [args]

Commands:
    scaffold --name <app> --entities <json>
    add-entity --app <app> --name <name> --fields <json>
    remove-entity --app <app> --name <name>
    add-field --app <app> --entity <name> --field <json>
    remove-field --app <app> --entity <name> --field <name>
    modify-field --app <app> --entity <name> --field <name> --updates <json>
    add-endpoint --app <app> --entity <name> --endpoint <json>
    remove-endpoint --app <app> --entity <name> --endpoint <name>
    add-query --app <app> --entity <name> --query <json>
    remove-query --app <app> --entity <name> --query <name>
    add-relationship --app <app> --relationship <json>
    remove-relationship --app <app> --source <name> --target <name>
    add-json-column --app <app> --entity <name> --column <col> --field <field>
    remove-json-column --app <app> --entity <name> --field <field>
    add-document-collection --app <app> --name <name> --table <table> [--description <desc>]
    remove-document-collection --app <app> --name <name>
    status --app <app>
    mark-clean --app <app> [--file <filename>]
    mark-dirty --app <app> [--file <filename>]
    list-apps
    list-entities --app <app>
    batch --file <json_file>
    bulk-update --app <app> --entities <names|ALL> --set <key=value> [--set ...]

Batch file format (JSON array of operations):
    [
      {"command": "add-entity", "app": "my_app", "name": "Product",
       "fields": [{"name": "title", "type": "String"}]},
      {"command": "remove-field", "app": "my_app", "entity": "Order", "field": "old_col"},
      {"command": "add-relationship", "app": "my_app",
       "relationship": {"source": "Order", "target": "Product", "type": "MANY_TO_ONE"}}
    ]
"""

import argparse
import io
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_def_manager.scaffolder import Scaffolder
from app_def_manager.crud import CRUDManager
from app_def_manager.status_tracker import StatusTracker

APP_DEFS_ROOT = Path("application_definitions")


def _ensure_utf8_streams():
    """Reconfigure stdout/stderr to UTF-8 so emoji prints safely on Windows."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    else:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    else:
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def main():
    _ensure_utf8_streams()
    parser = argparse.ArgumentParser(
        description="App Definition Manager — scaffold, CRUD, and status tracking for application definitions"
    )
    sub = parser.add_subparsers(dest="command")

    # scaffold
    p_scaffold = sub.add_parser("scaffold", help="Create new application definition")
    p_scaffold.add_argument("--name", required=True, help="Application name")
    p_scaffold.add_argument("--entities", required=True,
                            help='JSON array of entity descriptions: [{"name":"User","fields":[{"name":"email","type":"String"}]}]')
    p_scaffold.add_argument("--db-name", default=None, help="Database name (defaults to snake_case of app name)")
    p_scaffold.add_argument("--base-package", default="com.example", help="Java base package (default: com.example)")
    p_scaffold.add_argument("--force", action="store_true", help="Overwrite existing directory")

    # add-entity
    p_add_entity = sub.add_parser("add-entity", help="Add entity to existing app")
    p_add_entity.add_argument("--app", required=True, help="Application name")
    p_add_entity.add_argument("--name", required=True, help="Entity class name (PascalCase)")
    p_add_entity.add_argument("--fields", required=True,
                              help='JSON array of fields: [{"name":"email","type":"String"}]')

    # remove-entity
    p_rm_entity = sub.add_parser("remove-entity", help="Remove entity from app")
    p_rm_entity.add_argument("--app", required=True, help="Application name")
    p_rm_entity.add_argument("--name", required=True, help="Entity class name")

    # add-field
    p_add_field = sub.add_parser("add-field", help="Add field to entity")
    p_add_field.add_argument("--app", required=True, help="Application name")
    p_add_field.add_argument("--entity", required=True, help="Entity class name")
    p_add_field.add_argument("--field", required=True,
                             help='JSON field descriptor: {"name":"age","type":"Integer"}')

    # remove-field
    p_rm_field = sub.add_parser("remove-field", help="Remove field from entity")
    p_rm_field.add_argument("--app", required=True, help="Application name")
    p_rm_field.add_argument("--entity", required=True, help="Entity class name")
    p_rm_field.add_argument("--field", required=True, help="Field name to remove")

    # modify-field
    p_mod_field = sub.add_parser("modify-field", help="Modify field properties")
    p_mod_field.add_argument("--app", required=True, help="Application name")
    p_mod_field.add_argument("--entity", required=True, help="Entity class name")
    p_mod_field.add_argument("--field", required=True, help="Field name to modify")
    p_mod_field.add_argument("--updates", required=True,
                             help='JSON updates: {"type":"Integer","isNullable":false}')

    # add-endpoint
    p_add_ep = sub.add_parser("add-endpoint", help="Add custom endpoint to entity controller")
    p_add_ep.add_argument("--app", required=True, help="Application name")
    p_add_ep.add_argument("--entity", required=True, help="Entity class name")
    p_add_ep.add_argument("--endpoint", required=True, help="JSON endpoint descriptor")

    # remove-endpoint
    p_rm_ep = sub.add_parser("remove-endpoint", help="Remove custom endpoint")
    p_rm_ep.add_argument("--app", required=True, help="Application name")
    p_rm_ep.add_argument("--entity", required=True, help="Entity class name")
    p_rm_ep.add_argument("--endpoint", required=True, help="Endpoint name to remove")

    # add-query
    p_add_q = sub.add_parser("add-query", help="Add custom query to entity repository")
    p_add_q.add_argument("--app", required=True, help="Application name")
    p_add_q.add_argument("--entity", required=True, help="Entity class name")
    p_add_q.add_argument("--query", required=True, help="JSON query descriptor")

    # remove-query
    p_rm_q = sub.add_parser("remove-query", help="Remove custom query")
    p_rm_q.add_argument("--app", required=True, help="Application name")
    p_rm_q.add_argument("--entity", required=True, help="Entity class name")
    p_rm_q.add_argument("--query", required=True, help="Query name to remove")

    # add-relationship
    p_add_rel = sub.add_parser("add-relationship", help="Add relationship between entities")
    p_add_rel.add_argument("--app", required=True, help="Application name")
    p_add_rel.add_argument("--relationship", required=True, help="JSON relationship descriptor")

    # remove-relationship
    p_rm_rel = sub.add_parser("remove-relationship", help="Remove relationship")
    p_rm_rel.add_argument("--app", required=True, help="Application name")
    p_rm_rel.add_argument("--source", required=True, help="Source entity name")
    p_rm_rel.add_argument("--target", required=True, help="Target entity name")

    # status
    p_status = sub.add_parser("status", help="Show dirty/clean status for app")
    p_status.add_argument("--app", required=True, help="Application name")

    # mark-clean
    p_clean = sub.add_parser("mark-clean", help="Mark file(s) as clean")
    p_clean.add_argument("--app", required=True, help="Application name")
    p_clean.add_argument("--file", default=None, help="Specific file to mark (omit for all)")

    # mark-dirty
    p_dirty = sub.add_parser("mark-dirty", help="Mark file(s) as dirty")
    p_dirty.add_argument("--app", required=True, help="Application name")
    p_dirty.add_argument("--file", default=None, help="Specific file to mark (omit for all)")

    # add-json-column
    p_add_jc = sub.add_parser("add-json-column", help="Add JSON column mapping to document storage layer")
    p_add_jc.add_argument("--app", required=True, help="Application name")
    p_add_jc.add_argument("--entity", required=True, help="Entity class name")
    p_add_jc.add_argument("--column", required=True, help="Database column name")
    p_add_jc.add_argument("--field", required=True, help="Java field name")

    # remove-json-column
    p_rm_jc = sub.add_parser("remove-json-column", help="Remove JSON column mapping from document storage layer")
    p_rm_jc.add_argument("--app", required=True, help="Application name")
    p_rm_jc.add_argument("--entity", required=True, help="Entity class name")
    p_rm_jc.add_argument("--field", required=True, help="Java field name to remove")

    # add-document-collection
    p_add_dc = sub.add_parser("add-document-collection", help="Add document collection to document storage layer")
    p_add_dc.add_argument("--app", required=True, help="Application name")
    p_add_dc.add_argument("--name", required=True, help="Collection name (PascalCase)")
    p_add_dc.add_argument("--table", required=True, help="Database table name")
    p_add_dc.add_argument("--description", default="", help="Optional description")

    # remove-document-collection
    p_rm_dc = sub.add_parser("remove-document-collection", help="Remove document collection from document storage layer")
    p_rm_dc.add_argument("--app", required=True, help="Application name")
    p_rm_dc.add_argument("--name", required=True, help="Collection name to remove")

    # list-apps
    sub.add_parser("list-apps", help="List all application definitions")

    # list-entities
    p_list_ent = sub.add_parser("list-entities", help="List entities in an app")
    p_list_ent.add_argument("--app", required=True, help="Application name")

    # describe — rich formatted entity summary
    p_describe = sub.add_parser("describe", help="Rich formatted summary of app entities")
    p_describe.add_argument("--app", required=True, help="Application name")
    p_describe.add_argument("--entity", default=None, help="Single entity to describe in detail")
    p_describe.add_argument("--format", default="table", choices=["table", "markdown"],
                            help="Output format (default: table)")
    p_describe.add_argument("--ai-layer", action="store_true", help="Show AI layer summary")
    p_describe.add_argument("--ai-react", action="store_true", help="Show React AI config summary")

    # batch — run multiple commands from a JSON file
    p_batch = sub.add_parser("batch", help="Run multiple commands from a JSON file")
    p_batch.add_argument("--file", required=True, help="Path to JSON file with array of operations")

    # bulk-update — batch-update entity-level flags across layers
    p_bulk = sub.add_parser("bulk-update", help="Bulk update entity-level flags across layers")
    p_bulk.add_argument("--app", required=True, help="Application name")
    p_bulk.add_argument("--entities", required=True, help="Comma-separated entity names or ALL")
    p_bulk.add_argument("--set", action="append", required=True, dest="sets",
                        help="key=value pair to set (can repeat)")

    # ── AI CRUD subcommands ─────────────────────────────────────────────

    # ai-add-provider
    p = sub.add_parser("ai-add-provider", help="Add AI provider")
    p.add_argument("--app", required=True)
    p.add_argument("--name", required=True, help="Provider name")
    p.add_argument("--type", required=True, choices=["openai", "ollama"])
    p.add_argument("--model", required=True)
    p.add_argument("--api-key-env-var", default="OPENAI_API_KEY")

    # ai-remove-provider
    p = sub.add_parser("ai-remove-provider", help="Remove AI provider")
    p.add_argument("--app", required=True)
    p.add_argument("--name", required=True)

    # ai-add-capability
    p = sub.add_parser("ai-add-capability", help="Add entity AI capability")
    p.add_argument("--app", required=True)
    p.add_argument("--entity", required=True, help="Entity name")
    p.add_argument("--provider", required=True, help="Provider name")
    p.add_argument("--operations", required=True, help="Comma-separated operations")

    # ai-remove-capability
    p = sub.add_parser("ai-remove-capability", help="Remove entity AI capability")
    p.add_argument("--app", required=True)
    p.add_argument("--entity", required=True)

    # ai-add-prompt-template
    p = sub.add_parser("ai-add-prompt-template", help="Add prompt template")
    p.add_argument("--app", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--operation", required=True)
    p.add_argument("--template", required=True)

    # ai-remove-prompt-template
    p = sub.add_parser("ai-remove-prompt-template", help="Remove prompt template")
    p.add_argument("--app", required=True)
    p.add_argument("--name", required=True)

    # ai-add-assistant
    p = sub.add_parser("ai-add-assistant", help="Add AI assistant")
    p.add_argument("--app", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--system-prompt", required=True)
    p.add_argument("--provider", required=True)
    p.add_argument("--entity-scope", required=True)

    # ai-remove-assistant
    p = sub.add_parser("ai-remove-assistant", help="Remove AI assistant")
    p.add_argument("--app", required=True)
    p.add_argument("--name", required=True)

    # ai-add-standalone
    p = sub.add_parser("ai-add-standalone", help="Add standalone AI operation")
    p.add_argument("--app", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--type", required=True)
    p.add_argument("--provider", required=True)
    p.add_argument("--base-path", required=True)
    p.add_argument("--system-prompt", required=True)
    p.add_argument("--actions", required=True, help="Comma-separated enabled actions")

    # ai-remove-standalone
    p = sub.add_parser("ai-remove-standalone", help="Remove standalone AI operation")
    p.add_argument("--app", required=True)
    p.add_argument("--name", required=True)

    # ai-add-rag-source
    p = sub.add_parser("ai-add-rag-source", help="Add RAG source")
    p.add_argument("--app", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--type", required=True, choices=["semantic", "heuristic"])
    p.add_argument("--provider", default=None, help="Provider name (required for semantic)")
    p.add_argument("--enabled", action="store_true")

    # ai-remove-rag-source
    p = sub.add_parser("ai-remove-rag-source", help="Remove RAG source")
    p.add_argument("--app", required=True)
    p.add_argument("--name", required=True)

    # ai-add-evaluator
    p = sub.add_parser("ai-add-evaluator", help="Add evaluator")
    p.add_argument("--app", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--type", required=True, choices=["relevancy", "correctness", "safety", "custom"])
    p.add_argument("--provider", required=True)
    p.add_argument("--prompt", required=True, help="Evaluation prompt")
    p.add_argument("--scoring", required=True, choices=["numeric", "pass_fail", "categorical"])

    # ai-remove-evaluator
    p = sub.add_parser("ai-remove-evaluator", help="Remove evaluator")
    p.add_argument("--app", required=True)
    p.add_argument("--name", required=True)

    # ai-set-orchestrator
    p = sub.add_parser("ai-set-orchestrator", help="Set orchestrator config")
    p.add_argument("--app", required=True)
    p.add_argument("--provider", required=True)

    # ai-remove-orchestrator
    p = sub.add_parser("ai-remove-orchestrator", help="Remove orchestrator")
    p.add_argument("--app", required=True)

    # ai-add-mcp-server
    p = sub.add_parser("ai-add-mcp-server", help="Add MCP server")
    p.add_argument("--app", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--transport", required=True, choices=["stdio", "sse"])
    p.add_argument("--roles", required=True, help="Comma-separated required roles")

    # ai-remove-mcp-server
    p = sub.add_parser("ai-remove-mcp-server", help="Remove MCP server")
    p.add_argument("--app", required=True)
    p.add_argument("--name", required=True)

    # ai-set-vector-store
    p = sub.add_parser("ai-set-vector-store", help="Set vector store config")
    p.add_argument("--app", required=True)
    p.add_argument("--type", default="milvus", choices=["milvus", "qdrant", "pgvector", "in_memory"])

    # ai-remove-vector-store
    p = sub.add_parser("ai-remove-vector-store", help="Remove vector store")
    p.add_argument("--app", required=True)

    # ai-set-observability
    p = sub.add_parser("ai-set-observability", help="Enable observability")
    p.add_argument("--app", required=True)

    # ai-remove-observability
    p = sub.add_parser("ai-remove-observability", help="Remove observability")
    p.add_argument("--app", required=True)

    # ai-set-token-budget
    p = sub.add_parser("ai-set-token-budget", help="Set token budget")
    p.add_argument("--app", required=True)
    p.add_argument("--daily-limit", type=int, default=None)
    p.add_argument("--monthly-limit", type=int, default=None)

    # ai-remove-token-budget
    p = sub.add_parser("ai-remove-token-budget", help="Remove token budget")
    p.add_argument("--app", required=True)

    # ai-set-rate-limiting
    p = sub.add_parser("ai-set-rate-limiting", help="Set rate limiting")
    p.add_argument("--app", required=True)
    p.add_argument("--default-rpm", type=int, default=20)

    # ai-remove-rate-limiting
    p = sub.add_parser("ai-remove-rate-limiting", help="Remove rate limiting")
    p.add_argument("--app", required=True)

    # ai-set-session-cleanup
    p = sub.add_parser("ai-set-session-cleanup", help="Set chat session cleanup")
    p.add_argument("--app", required=True)
    p.add_argument("--ttl-days", type=int, default=30)

    # ai-remove-session-cleanup
    p = sub.add_parser("ai-remove-session-cleanup", help="Remove session cleanup")
    p.add_argument("--app", required=True)

    # ai-set-audit-log
    p = sub.add_parser("ai-set-audit-log", help="Set audit log")
    p.add_argument("--app", required=True)
    p.add_argument("--retention-days", type=int, default=90)

    # ai-remove-audit-log
    p = sub.add_parser("ai-remove-audit-log", help="Remove audit log")
    p.add_argument("--app", required=True)

    # ai-set-document-ingestion
    p = sub.add_parser("ai-set-document-ingestion", help="Set document ingestion")
    p.add_argument("--app", required=True)

    # ai-remove-document-ingestion
    p = sub.add_parser("ai-remove-document-ingestion", help="Remove document ingestion")
    p.add_argument("--app", required=True)

    # ai-set-document-processing
    p = sub.add_parser("ai-set-document-processing", help="Set document processing")
    p.add_argument("--app", required=True)

    # ai-remove-document-processing
    p = sub.add_parser("ai-remove-document-processing", help="Remove document processing")
    p.add_argument("--app", required=True)

    # ai-set-moderation
    p = sub.add_parser("ai-set-moderation", help="Set moderation config")
    p.add_argument("--app", required=True)
    p.add_argument("--provider", required=True)
    p.add_argument("--categories", required=True, help="Comma-separated categories")

    # ai-remove-moderation
    p = sub.add_parser("ai-remove-moderation", help="Remove moderation")
    p.add_argument("--app", required=True)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "batch":
            _dispatch_batch(args.file)
        else:
            _dispatch(args)
    except json.JSONDecodeError as e:
        print(f"  ❌ Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except (ValueError, FileExistsError, FileNotFoundError, KeyError) as e:
        print(f"  ❌ {e}", file=sys.stderr)
        sys.exit(1)


# ── Batch key → argparse attribute mapping ──────────────────────────────────
# Maps camelCase JSON keys to the snake_case/hyphenated attribute names
# that _dispatch expects on the args namespace.
_BATCH_KEY_MAP = {
    "command": "command",
    "app": "app",
    "name": "name",
    "entities": "entities",       # JSON-serialised by batch runner
    "fields": "fields",           # JSON-serialised by batch runner
    "field": "field",             # JSON-serialised for add-field, plain str for remove-field
    "entity": "entity",
    "updates": "updates",         # JSON-serialised by batch runner
    "endpoint": "endpoint",       # JSON-serialised by batch runner
    "query": "query",             # JSON-serialised by batch runner
    "relationship": "relationship",  # JSON-serialised by batch runner
    "source": "source",
    "target": "target",
    "dbName": "db_name",
    "basePackage": "base_package",
    "force": "force",
    "file": "file",
    "column": "column",
    "table": "table",
    "description": "description",
}

# Keys whose values should be JSON-serialised when they are dicts/lists
# (because _dispatch calls json.loads on them).
_BATCH_JSON_KEYS = {"entities", "fields", "field", "updates", "endpoint", "query", "relationship"}


def _dispatch_batch(filepath: str):
    """Read a JSON file containing an array of operations and execute each."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Batch file not found: {filepath}")

    with open(path, "r", encoding="utf-8") as f:
        operations = json.load(f)

    if not isinstance(operations, list):
        raise ValueError("Batch file must contain a JSON array of operations")

    total = len(operations)
    failed = 0
    for i, op in enumerate(operations, 1):
        cmd = op.get("command")
        if not cmd:
            print(f"  ⚠️  Operation {i}/{total}: missing 'command' key — skipped")
            failed += 1
            continue

        # Build an argparse-like namespace from the operation dict
        ns = argparse.Namespace()
        ns.command = cmd

        for key, value in op.items():
            attr = _BATCH_KEY_MAP.get(key, key.replace("-", "_"))
            # JSON-serialise complex values so _dispatch can json.loads() them
            if key in _BATCH_JSON_KEYS and isinstance(value, (dict, list)):
                value = json.dumps(value)
            setattr(ns, attr, value)

        # Provide defaults for optional attributes that _dispatch may access
        if not hasattr(ns, "db_name"):
            ns.db_name = None
        if not hasattr(ns, "base_package"):
            ns.base_package = "com.example"
        if not hasattr(ns, "force"):
            ns.force = False
        if not hasattr(ns, "file"):
            ns.file = None
        if not hasattr(ns, "description"):
            ns.description = ""

        try:
            print(f"  [{i}/{total}] {cmd}", end=" ")
            _dispatch(ns)
        except Exception as e:
            print(f"  ❌ Operation {i}/{total} ({cmd}) failed: {e}", file=sys.stderr)
            failed += 1

    if failed:
        print(f"\n  ⚠️  Batch complete: {total - failed}/{total} succeeded, {failed} failed")
    else:
        print(f"\n  ✅ Batch complete: all {total} operations succeeded")


def _dispatch(args):
    """Route command to the appropriate handler."""
    cmd = args.command

    if cmd == "scaffold":
        entities = json.loads(args.entities)
        scaffolder = Scaffolder()
        path = scaffolder.scaffold_application(
            app_name=args.name,
            entity_descriptions=entities,
            db_name=args.db_name,
            base_package=args.base_package,
            force=args.force,
        )
        entity_count = len(entities)
        print(f"  ✅ Scaffolded '{args.name}' with {entity_count} entit{'y' if entity_count == 1 else 'ies'} at {path}")

    elif cmd == "add-entity":
        fields = json.loads(args.fields)
        crud = CRUDManager(args.app)
        dirty = crud.add_entity(args.name, fields)
        print(f"  ✅ Entity '{args.name}' added to {args.app} ({len(dirty)} files marked dirty)")

    elif cmd == "remove-entity":
        crud = CRUDManager(args.app)
        dirty = crud.remove_entity(args.name)
        print(f"  ✅ Entity '{args.name}' removed from {args.app} ({len(dirty)} files marked dirty)")

    elif cmd == "add-field":
        field = json.loads(args.field)
        crud = CRUDManager(args.app)
        dirty = crud.add_field(args.entity, field)
        print(f"  ✅ Field added to '{args.entity}' in {args.app} ({len(dirty)} files marked dirty)")

    elif cmd == "remove-field":
        crud = CRUDManager(args.app)
        dirty = crud.remove_field(args.entity, args.field)
        print(f"  ✅ Field '{args.field}' removed from '{args.entity}' in {args.app} ({len(dirty)} files marked dirty)")

    elif cmd == "modify-field":
        updates = json.loads(args.updates)
        crud = CRUDManager(args.app)
        dirty = crud.modify_field(args.entity, args.field, updates)
        print(f"  ✅ Field '{args.field}' modified in '{args.entity}' in {args.app} ({len(dirty)} files marked dirty)")

    elif cmd == "add-endpoint":
        endpoint = json.loads(args.endpoint)
        crud = CRUDManager(args.app)
        dirty = crud.add_endpoint(args.entity, endpoint)
        print(f"  ✅ Endpoint added to '{args.entity}' in {args.app} ({len(dirty)} files marked dirty)")

    elif cmd == "remove-endpoint":
        crud = CRUDManager(args.app)
        dirty = crud.remove_endpoint(args.entity, args.endpoint)
        print(f"  ✅ Endpoint '{args.endpoint}' removed from '{args.entity}' in {args.app} ({len(dirty)} files marked dirty)")

    elif cmd == "add-query":
        query = json.loads(args.query)
        crud = CRUDManager(args.app)
        dirty = crud.add_query(args.entity, query)
        print(f"  ✅ Query added to '{args.entity}' in {args.app} ({len(dirty)} files marked dirty)")

    elif cmd == "remove-query":
        crud = CRUDManager(args.app)
        dirty = crud.remove_query(args.entity, args.query)
        print(f"  ✅ Query '{args.query}' removed from '{args.entity}' in {args.app} ({len(dirty)} files marked dirty)")

    elif cmd == "add-relationship":
        relationship = json.loads(args.relationship)
        crud = CRUDManager(args.app)
        dirty = crud.add_relationship(relationship)
        print(f"  ✅ Relationship added to {args.app} ({len(dirty)} files marked dirty)")

    elif cmd == "remove-relationship":
        crud = CRUDManager(args.app)
        dirty = crud.remove_relationship(args.source, args.target)
        print(f"  ✅ Relationship {args.source} → {args.target} removed from {args.app} ({len(dirty)} files marked dirty)")

    elif cmd == "add-json-column":
        crud = CRUDManager(args.app)
        dirty = crud.add_json_column(args.entity, args.column, args.field)
        print(f"  ✅ JSON column '{args.field}' added to '{args.entity}' in {args.app} ({len(dirty)} files marked dirty)")

    elif cmd == "remove-json-column":
        crud = CRUDManager(args.app)
        dirty = crud.remove_json_column(args.entity, args.field)
        print(f"  ✅ JSON column '{args.field}' removed from '{args.entity}' in {args.app} ({len(dirty)} files marked dirty)")

    elif cmd == "add-document-collection":
        crud = CRUDManager(args.app)
        dirty = crud.add_document_collection(args.name, args.table, args.description)
        print(f"  ✅ Document collection '{args.name}' added to {args.app} ({len(dirty)} files marked dirty)")

    elif cmd == "remove-document-collection":
        crud = CRUDManager(args.app)
        dirty = crud.remove_document_collection(args.name)
        print(f"  ✅ Document collection '{args.name}' removed from {args.app} ({len(dirty)} files marked dirty)")

    elif cmd == "status":
        app_dir = APP_DEFS_ROOT / args.app
        if not app_dir.exists():
            raise FileNotFoundError(f"Application '{args.app}' not found at {app_dir}")
        tracker = StatusTracker(app_dir)
        status = tracker.load()
        if not status or "files" not in status:
            print(f"  No status file found for '{args.app}' — all files treated as dirty")
            return
        files = status["files"]
        dirty_count = sum(1 for info in files.values() if info.get("status") == "dirty")
        clean_count = sum(1 for info in files.values() if info.get("status") == "clean")
        print(f"  Status for '{args.app}': {dirty_count} dirty, {clean_count} clean")
        for fname, info in sorted(files.items()):
            st = info.get("status", "unknown")
            marker = "🔴" if st == "dirty" else "🟢" if st == "clean" else "⚪"
            print(f"    {marker} {fname}: {st}")

    elif cmd == "mark-clean":
        app_dir = APP_DEFS_ROOT / args.app
        if not app_dir.exists():
            raise FileNotFoundError(f"Application '{args.app}' not found at {app_dir}")
        tracker = StatusTracker(app_dir)
        if args.file:
            tracker.mark_clean([args.file])
            print(f"  ✅ Marked '{args.file}' as clean in {args.app}")
        else:
            tracker.mark_all_clean()
            print(f"  ✅ Marked all files as clean in {args.app}")

    elif cmd == "mark-dirty":
        app_dir = APP_DEFS_ROOT / args.app
        if not app_dir.exists():
            raise FileNotFoundError(f"Application '{args.app}' not found at {app_dir}")
        tracker = StatusTracker(app_dir)
        if args.file:
            tracker.mark_dirty([args.file])
            print(f"  ✅ Marked '{args.file}' as dirty in {args.app}")
        else:
            tracker.mark_all_dirty()
            print(f"  ✅ Marked all files as dirty in {args.app}")

    elif cmd == "list-apps":
        if not APP_DEFS_ROOT.exists():
            print("  No application_definitions/ directory found")
            return
        apps = sorted(
            d.name for d in APP_DEFS_ROOT.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        )
        if not apps:
            print("  No applications found")
        else:
            print(f"  {len(apps)} application(s):")
            for app in apps:
                print(f"    • {app}")

    elif cmd == "list-entities":
        app_dir = APP_DEFS_ROOT / args.app
        entity_layer_path = app_dir / "webflux_entity_layer.json"
        if not entity_layer_path.exists():
            raise FileNotFoundError(
                f"Entity layer not found at {entity_layer_path}"
            )
        with open(entity_layer_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        entities = data.get("entities", [])
        if not entities:
            print(f"  No entities found in '{args.app}'")
        else:
            print(f"  {len(entities)} entit{'y' if len(entities) == 1 else 'ies'} in '{args.app}':")
            for ent in entities:
                name = ent.get("className", "?")
                table = ent.get("tableName", "?")
                field_count = len(ent.get("fields", []))
                print(f"    • {name} (table: {table}, {field_count} fields)")

    elif cmd == "bulk-update":
        from app_def_manager.bulk_updater import bulk_update, _parse_value
        entities = ["ALL"] if args.entities.upper() == "ALL" else [e.strip() for e in args.entities.split(",")]
        updates = {}
        for kv in args.sets:
            if "=" not in kv:
                raise ValueError(f"Invalid --set format: '{kv}' (expected key=value)")
            key, val = kv.split("=", 1)
            updates[key] = _parse_value(val)
        results = bulk_update(args.app, entities, updates)
        for layer, count in results.items():
            print(f"  ✅ {layer}: updated {count} entries")

    elif cmd == "describe":
        from app_def_manager.describer import describe_app, describe_entity, describe_ai_layer, describe_ai_react
        if getattr(args, "ai_layer", False):
            print(describe_ai_layer(args.app, fmt=args.format))
        elif getattr(args, "ai_react", False):
            print(describe_ai_react(args.app, fmt=args.format))
        elif args.entity:
            print(describe_entity(args.app, args.entity))
        else:
            print(describe_app(args.app, fmt=args.format))

    # ── AI CRUD dispatch ────────────────────────────────────────────────

    elif cmd.startswith("ai-"):
        from app_def_manager.ai_crud import AiCRUDManager
        ai = AiCRUDManager(args.app)

        if cmd == "ai-add-provider":
            dirty = ai.add_provider(args.name, args.type, args.model,
                                     api_key_env_var=args.api_key_env_var)
            print(f"  ✅ AI provider '{args.name}' added ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-provider":
            dirty = ai.remove_provider(args.name)
            print(f"  ✅ AI provider '{args.name}' removed ({len(dirty)} files dirty)")

        elif cmd == "ai-add-capability":
            ops = [o.strip() for o in args.operations.split(",")]
            dirty = ai.add_ai_capability(args.entity, args.provider, ops)
            print(f"  ✅ AI capability added to '{args.entity}' ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-capability":
            dirty = ai.remove_ai_capability(args.entity)
            print(f"  ✅ AI capability removed from '{args.entity}' ({len(dirty)} files dirty)")

        elif cmd == "ai-add-prompt-template":
            dirty = ai.add_prompt_template(args.name, args.operation, args.template)
            print(f"  ✅ Prompt template '{args.name}' added ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-prompt-template":
            dirty = ai.remove_prompt_template(args.name)
            print(f"  ✅ Prompt template '{args.name}' removed ({len(dirty)} files dirty)")

        elif cmd == "ai-add-assistant":
            dirty = ai.add_assistant(args.name, args.system_prompt,
                                      args.provider, args.entity_scope)
            print(f"  ✅ AI assistant '{args.name}' added ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-assistant":
            dirty = ai.remove_assistant(args.name)
            print(f"  ✅ AI assistant '{args.name}' removed ({len(dirty)} files dirty)")

        elif cmd == "ai-add-standalone":
            actions = [a.strip() for a in args.actions.split(",")]
            dirty = ai.add_standalone_operation(
                args.name, args.type, args.provider,
                args.base_path, args.system_prompt, actions)
            print(f"  ✅ Standalone operation '{args.name}' added ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-standalone":
            dirty = ai.remove_standalone_operation(args.name)
            print(f"  ✅ Standalone operation '{args.name}' removed ({len(dirty)} files dirty)")

        elif cmd == "ai-add-rag-source":
            kwargs = {"enabled": args.enabled}
            if args.provider:
                kwargs["providerName"] = args.provider
            dirty = ai.add_rag_source(args.name, args.type, **kwargs)
            print(f"  ✅ RAG source '{args.name}' added ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-rag-source":
            dirty = ai.remove_rag_source(args.name)
            print(f"  ✅ RAG source '{args.name}' removed ({len(dirty)} files dirty)")

        elif cmd == "ai-add-evaluator":
            dirty = ai.add_evaluator(args.name, args.type, args.provider,
                                      args.prompt, args.scoring)
            print(f"  ✅ Evaluator '{args.name}' added ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-evaluator":
            dirty = ai.remove_evaluator(args.name)
            print(f"  ✅ Evaluator '{args.name}' removed ({len(dirty)} files dirty)")

        elif cmd == "ai-set-orchestrator":
            dirty = ai.set_orchestrator(args.provider)
            print(f"  ✅ Orchestrator set ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-orchestrator":
            dirty = ai.remove_orchestrator()
            print(f"  ✅ Orchestrator removed ({len(dirty)} files dirty)")

        elif cmd == "ai-add-mcp-server":
            roles = [r.strip() for r in args.roles.split(",")]
            dirty = ai.add_mcp_server(args.name, args.transport, roles)
            print(f"  ✅ MCP server '{args.name}' added ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-mcp-server":
            dirty = ai.remove_mcp_server(args.name)
            print(f"  ✅ MCP server '{args.name}' removed ({len(dirty)} files dirty)")

        elif cmd == "ai-set-vector-store":
            dirty = ai.set_vector_store(type=args.type)
            print(f"  ✅ Vector store set ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-vector-store":
            dirty = ai.remove_vector_store()
            print(f"  ✅ Vector store removed ({len(dirty)} files dirty)")

        elif cmd == "ai-set-observability":
            dirty = ai.set_observability(enabled=True)
            print(f"  ✅ Observability enabled ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-observability":
            dirty = ai.remove_observability()
            print(f"  ✅ Observability removed ({len(dirty)} files dirty)")

        elif cmd == "ai-set-token-budget":
            kwargs = {}
            if args.daily_limit is not None:
                kwargs["defaultDailyLimitPerUser"] = args.daily_limit
            if args.monthly_limit is not None:
                kwargs["defaultMonthlyLimitPerUser"] = args.monthly_limit
            dirty = ai.set_token_budget(enabled=True, **kwargs)
            print(f"  ✅ Token budget set ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-token-budget":
            dirty = ai.remove_token_budget()
            print(f"  ✅ Token budget removed ({len(dirty)} files dirty)")

        elif cmd == "ai-set-rate-limiting":
            dirty = ai.set_rate_limiting(default_rpm=args.default_rpm)
            print(f"  ✅ Rate limiting set ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-rate-limiting":
            dirty = ai.remove_rate_limiting()
            print(f"  ✅ Rate limiting removed ({len(dirty)} files dirty)")

        elif cmd == "ai-set-session-cleanup":
            dirty = ai.set_chat_session_cleanup(enabled=True, defaultTtlDays=args.ttl_days)
            print(f"  ✅ Session cleanup set ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-session-cleanup":
            dirty = ai.remove_chat_session_cleanup()
            print(f"  ✅ Session cleanup removed ({len(dirty)} files dirty)")

        elif cmd == "ai-set-audit-log":
            dirty = ai.set_audit_log(enabled=True, retentionDays=args.retention_days)
            print(f"  ✅ Audit log set ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-audit-log":
            dirty = ai.remove_audit_log()
            print(f"  ✅ Audit log removed ({len(dirty)} files dirty)")

        elif cmd == "ai-set-document-ingestion":
            dirty = ai.set_document_ingestion()
            print(f"  ✅ Document ingestion set ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-document-ingestion":
            dirty = ai.remove_document_ingestion()
            print(f"  ✅ Document ingestion removed ({len(dirty)} files dirty)")

        elif cmd == "ai-set-document-processing":
            dirty = ai.set_document_processing()
            print(f"  ✅ Document processing set ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-document-processing":
            dirty = ai.remove_document_processing()
            print(f"  ✅ Document processing removed ({len(dirty)} files dirty)")

        elif cmd == "ai-set-moderation":
            cats = [c.strip() for c in args.categories.split(",")]
            dirty = ai.set_moderation(True, args.provider, cats)
            print(f"  ✅ Moderation set ({len(dirty)} files dirty)")

        elif cmd == "ai-remove-moderation":
            dirty = ai.remove_moderation()
            print(f"  ✅ Moderation removed ({len(dirty)} files dirty)")

        else:
            print(f"  ❌ Unknown AI command: {cmd}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
