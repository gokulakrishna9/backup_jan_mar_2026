# Migration Strategy: JSON Files → Database Store

## Overview

This document outlines the plan for migrating the application definition
storage from JSON files to the MySQL database described in documents 01-06.

---

## Phase 1: Database Schema Creation

Create the `swfaw_definition_store` database and all 30 tables.

### Execution Order (respecting FK dependencies)

```
1. swfaw_app_definition          (no dependencies)
2. swfaw_entity                  (→ app_definition)
3. swfaw_relationship            (→ app_definition)
4. swfaw_entity_layer            (→ app_definition)
5. swfaw_entity_layer_field      (→ entity_layer)
6. swfaw_repository_layer        (→ app_definition)
7. swfaw_service_layer           (→ app_definition)
8. swfaw_controller_layer        (→ app_definition)
9. swfaw_dto_layer               (→ app_definition)
10. swfaw_query                  (→ app_definition)
11. swfaw_query_join             (→ query)
12. swfaw_query_parameter        (→ query)
13. swfaw_filter                 (→ app_definition)
14. swfaw_filter_field           (→ filter)
15. swfaw_security_config        (→ app_definition)
16. swfaw_security_oauth2_provider (→ security_config)
17. swfaw_security_cors          (→ security_config)
18. swfaw_security_public_endpoint (→ security_config)
19. swfaw_app_config             (→ app_definition)
20. swfaw_exception_config       (→ app_definition)
21. swfaw_exception_definition   (→ app_definition)
22. swfaw_exception_message      (→ app_definition)
23. swfaw_audit_config           (→ app_definition)
24. swfaw_audit_event            (→ audit_config)
25. swfaw_audit_alert            (→ audit_config)
26. swfaw_authorization_config   (→ app_definition)
27. swfaw_entity_access_control  (→ authorization_config)
28. swfaw_group_config           (→ app_definition)
29. swfaw_group_definition       (→ app_definition)
30. swfaw_custom_query_template  (→ app_definition)
```

---

## Phase 2: Storage Abstraction Layer

Before changing any existing code, introduce a storage abstraction that
both JSON and DB backends can implement.

### New Module: `emotisense-ai/swfaw/storage/`

```
storage/
├── __init__.py
├── base.py              # Abstract base class (DefinitionStore)
├── json_store.py        # Current JSON file implementation
├── db_store.py          # New MySQL implementation
└── db_connection.py     # Database connection management
```

### Abstract Interface

```python
class DefinitionStore(ABC):
    """Abstract storage backend for application definitions."""

    @abstractmethod
    def load(self, app_id: str) -> dict:
        """Load complete application definition."""

    @abstractmethod
    def save(self, app_id: str, definition: dict) -> None:
        """Save complete application definition."""

    @abstractmethod
    def get_layer(self, app_id: str, layer_name: str) -> dict:
        """Load a single layer by name."""

    @abstractmethod
    def set_layer(self, app_id: str, layer_name: str, data: dict) -> None:
        """Save a single layer."""

    @abstractmethod
    def list_apps(self) -> list:
        """List all application definitions."""

    @abstractmethod
    def delete_app(self, app_id: str) -> None:
        """Delete an application definition and all its layers."""
```

### Migration Path

1. Wrap current JSON file operations in `JsonStore(DefinitionStore)`
2. Implement `DbStore(DefinitionStore)` using the new schema
3. Update `DefinitionManager` to accept a `DefinitionStore` instance
4. Add `--storage` flag to CLI: `--storage json` (default) or `--storage db`

---

## Phase 3: JSON → DB Import Tool

A one-time migration script to import existing JSON definitions into the database.

### Script: `tools/import_json_to_db.py`

```python
# Usage:
python tools/import_json_to_db.py \
    --input ../generated_application/my_app/application_definitions/ \
    --db-host localhost \
    --db-name swfaw_definition_store
```

### Import Order (matches table creation order)

1. Read `manifest.json` + `project_metadata.json` → INSERT `swfaw_app_definition`
2. Read `entities.json` → INSERT `swfaw_entity` (one row per table)
3. Read `relationships.json` → INSERT `swfaw_relationship`
4. Read `entity_layer.json` → INSERT `swfaw_entity_layer` + `swfaw_entity_layer_field`
5. Read `repository_layer.json` → INSERT `swfaw_repository_layer`
6. Read `service_layer.json` → INSERT `swfaw_service_layer`
7. Read `controller_layer.json` → INSERT `swfaw_controller_layer`
8. Read `dto_layer.json` → INSERT `swfaw_dto_layer`
9. Read `query_layer.json` → INSERT `swfaw_query` + `swfaw_query_join` + `swfaw_query_parameter`
10. Read `filter_layer.json` → INSERT `swfaw_filter` + `swfaw_filter_field`
11. Read `security_layer.json` → INSERT security tables (4 tables)
12. Read `config_layer.json` → INSERT `swfaw_app_config`
13. Read `exception_layer.json` → INSERT exception tables (3 tables)
14. Read `audit_logging_layer.json` → INSERT audit tables (3 tables)
15. Read `authorization_layer.json` → INSERT authorization tables (2 tables)
16. Read `group_definition_layer.json` → INSERT group tables (2 tables)
17. Read `custom_queries_layer.json` → INSERT `swfaw_custom_query_template`
18. Update statistics on `swfaw_app_definition`

---

## Phase 4: Code Changes Required

### Files That Need Modification

| Component | File(s) | Change |
|-----------|---------|--------|
| DefinitionManager | `managers/definition_manager.py` | Accept `DefinitionStore` backend; delegate load/save |
| EntityManager | `managers/entity_manager.py` | No change (operates on in-memory dicts) |
| FieldManager | `managers/field_manager.py` | No change (operates on in-memory dicts) |
| RelationshipManager | `managers/relationship_manager.py` | No change (operates on in-memory dicts) |
| LayerManager | `managers/layer_manager.py` | No change (operates on in-memory dicts) |
| Phase 1 | `phase1_generate_definition.py` | Add `--storage` flag, use store backend |
| Phase 2 | `phase2_generate_code.py` | Add `--storage` flag, load from store |
| Unified | `generate_app.py` | Pass `--storage` through to both phases |

### Key Insight: Minimal Code Changes

The managers layer already operates on in-memory Python dicts. The only
code that touches the filesystem is `DefinitionManager.load()` and
`DefinitionManager.save()`. By introducing the storage abstraction at
that boundary, all existing manager logic works unchanged.

The flow becomes:

```
JSON Store:  SQL → Parser → Transformer → JSON files → load() → in-memory dicts
DB Store:    SQL → Parser → Transformer → DB tables  → load() → in-memory dicts
                                                                      ↓
                                                              (same from here)
                                                                      ↓
                                                              Generators → Code
```

---

## Phase 5: DB → JSON Export Tool

For backward compatibility, provide an export tool that dumps a DB-stored
definition back to JSON files.

### Script: `tools/export_db_to_json.py`

```python
# Usage:
python tools/export_db_to_json.py \
    --app-id 1 \
    --output ../generated_application/my_app/application_definitions/ \
    --db-host localhost \
    --db-name swfaw_definition_store
```

This ensures:
- Existing JSON-based workflows continue to work
- Definitions can be version-controlled as JSON even when stored in DB
- Teams can review definitions in a human-readable format

---

## Phase 6: CLI Integration

### Updated CLI Flags

```bash
# Phase 1 with DB storage
python phase1_generate_definition.py \
    --input ../mysql_database_design/schema.sql \
    --storage db \
    --db-host localhost \
    --db-name swfaw_definition_store

# Phase 2 from DB storage
python phase2_generate_code.py \
    --app-id 1 \
    --storage db \
    --db-host localhost \
    --db-name swfaw_definition_store \
    --output ../generated_application/my_app

# Unified with DB storage
python generate_app.py \
    --input ../mysql_database_design/schema.sql \
    --storage db \
    --db-host localhost \
    --db-name swfaw_definition_store
```

### DB Connection Config

Support a config file at `~/.swfaw/db_config.json` to avoid repeating
connection params:

```json
{
    "host": "localhost",
    "port": 3306,
    "database": "swfaw_definition_store",
    "username": "root",
    "password": "password"
}
```

Then CLI simplifies to:

```bash
python generate_app.py --input schema.sql --storage db
```

---

## Implementation Priority

| Priority | Task | Effort | Dependencies |
|----------|------|--------|-------------|
| 1 | Create database schema (all 30 tables) | Medium | None |
| 2 | Build storage abstraction (`storage/base.py`) | Small | None |
| 3 | Wrap existing JSON ops in `JsonStore` | Small | #2 |
| 4 | Implement `DbStore` | Large | #1, #2 |
| 5 | Update `DefinitionManager` to use store | Small | #2, #3 |
| 6 | Build JSON → DB import tool | Medium | #1, #4 |
| 7 | Build DB → JSON export tool | Medium | #4 |
| 8 | Add CLI flags | Small | #5 |
| 9 | Test with existing generated app | Medium | #6 |
| 10 | Documentation updates | Small | All |

### Estimated Total Effort

- Schema creation: ~2 hours (SQL file generation)
- Storage abstraction + JsonStore: ~2 hours
- DbStore implementation: ~6-8 hours (30 tables, read/write for each)
- Import/Export tools: ~3 hours
- CLI + testing: ~3 hours
- Total: ~16-18 hours of development

---

## Rollback Plan

Since the storage abstraction supports both backends:
- Default remains `--storage json` (no breaking changes)
- DB storage is opt-in via `--storage db`
- Export tool can always dump DB back to JSON
- If DB store has issues, switch back to JSON with zero data loss

---

## Complete Table Summary

| # | Table Name | Replaces | Rows per App (100 entities) |
|---|-----------|----------|---------------------------|
| 1 | `swfaw_app_definition` | manifest + project_metadata | 1 |
| 2 | `swfaw_entity` | entities.json | 100 |
| 3 | `swfaw_relationship` | relationships.json | 0-200 |
| 4 | `swfaw_entity_layer` | entity_layer.json (headers) | 100 |
| 5 | `swfaw_entity_layer_field` | entity_layer.json (fields) | ~700 |
| 6 | `swfaw_repository_layer` | repository_layer.json | 100 |
| 7 | `swfaw_service_layer` | service_layer.json | 100 |
| 8 | `swfaw_controller_layer` | controller_layer.json | 100 |
| 9 | `swfaw_dto_layer` | dto_layer.json | 300 (3 per entity) |
| 10 | `swfaw_query` | query_layer.json | 100-500 |
| 11 | `swfaw_query_join` | query joins | 0-200 |
| 12 | `swfaw_query_parameter` | query parameters | 0-500 |
| 13 | `swfaw_filter` | filter_layer.json (headers) | 100 |
| 14 | `swfaw_filter_field` | filter_layer.json (fields) | ~700 |
| 15 | `swfaw_security_config` | security_layer.json (core) | 1 |
| 16 | `swfaw_security_oauth2_provider` | OAuth2 providers | 0-5 |
| 17 | `swfaw_security_cors` | CORS config | 1 |
| 18 | `swfaw_security_public_endpoint` | public endpoints | 5-20 |
| 19 | `swfaw_app_config` | config_layer.json | 1 |
| 20 | `swfaw_exception_config` | exception global settings | 1 |
| 21 | `swfaw_exception_definition` | custom exceptions | 6 |
| 22 | `swfaw_exception_message` | per-entity messages | ~100-600 |
| 23 | `swfaw_audit_config` | audit settings | 1 |
| 24 | `swfaw_audit_event` | audit event definitions | 10-20 |
| 25 | `swfaw_audit_alert` | audit alerts | 2-10 |
| 26 | `swfaw_authorization_config` | authorization settings | 1 |
| 27 | `swfaw_entity_access_control` | per-entity authz | 100 |
| 28 | `swfaw_group_config` | group management settings | 1 |
| 29 | `swfaw_group_definition` | system + table groups | 200+ |
| 30 | `swfaw_custom_query_template` | authz query templates | 0-100 |

**Total rows for a 100-entity app: ~3,500-4,500 rows across 30 tables**
