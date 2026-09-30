# Session Summary: Application Definition Database Store Design
**Date:** 2026-03-14
**Project:** swfaw_v2 (Spring WebFlux App Writer v2)

## What Was Done

Designed and documented a complete MySQL database schema to replace the
JSON file-based application definition storage in swfaw_v2.

### Deliverables Created

1. **Design Documents** — `emotisense-ai/swfaw/docs/db_store_design/`
   - `00_OVERVIEW.md` — Master index, JSON→DB mapping, design principles
   - `01_FOUNDATION.md` — app_definition + entity tables (Tables 1-2)
   - `02_PER_ENTITY_LAYERS.md` — relationship/entity/repo/service/controller/dto (Tables 3-9)
   - `03_QUERY_FILTER_LAYERS.md` — query/join/parameter/filter/filter_field (Tables 10-14)
   - `04_SECURITY_CONFIG.md` — security/oauth2/cors/public_endpoint (Tables 15-18)
   - `05_APP_CONFIG_EXCEPTION.md` — app_config/exception tables (Tables 19-22)
   - `06_AUDIT_AUTHORIZATION.md` — audit/authorization/group/custom_query (Tables 23-30)
   - `07_MIGRATION_STRATEGY.md` — 6-phase migration plan with effort estimates

2. **SQL Schema File** — `emotisense-ai/swfaw/swfaw_definition_store.sql`
   - 797 lines, 30 CREATE TABLE statements
   - Ready to execute against MySQL 8.0+
   - Creates `swfaw_definition_store` database
   - All FKs, unique keys, indexes included

### Schema Summary

- **30 tables** across 4 tiers replacing 18 JSON files
- **42 JSON columns** used for deeply nested/variable structures
- All tables prefixed with `swfaw_` to avoid collisions
- `app_definition_id` is the universal FK linking everything
- CASCADE deletes on all foreign keys

### Table Count by Tier

| Tier | Tables | Description |
|------|--------|-------------|
| 1 - Foundation | 2 | app_definition, entity |
| 2 - Per-Entity | 7 | relationship, entity_layer, entity_layer_field, repository, service, controller, dto |
| 3 - Query/Filter | 5 | query, query_join, query_parameter, filter, filter_field |
| 4 - App-Wide | 16 | security (4), app_config (1), exception (3), audit (3), authorization (2), groups (2), custom_query (1) |

## What Was NOT Done (Next Session Work)

### Phase 2: Storage Abstraction Layer
- Create `emotisense-ai/swfaw/storage/` module
- `base.py` — Abstract `DefinitionStore` class
- `json_store.py` — Wrap existing JSON file operations
- `db_store.py` — New MySQL implementation
- `db_connection.py` — Connection management

### Phase 3: JSON → DB Import Tool
- `tools/import_json_to_db.py` — Migrate existing JSON definitions to DB

### Phase 4: Code Changes
- Update `DefinitionManager` to accept `DefinitionStore` backend
- Add `--storage` flag to CLI scripts (generate_app.py, phase1, phase2)
- Add `~/.swfaw/db_config.json` support

### Phase 5: DB → JSON Export Tool
- `tools/export_db_to_json.py` — Dump DB definitions back to JSON

### Phase 6: Testing
- Test import with existing generated app (ems_recruitment_portal)
- Verify round-trip: JSON → DB → JSON produces identical output
- Test code generation from DB-stored definitions

## Key Design Decisions to Remember

1. **Columns stored as JSON** on `swfaw_entity` (not normalized) — loaded as batch
2. **DTO field configs as JSON** — nested validation rules too complex to normalize
3. **Controller endpoints as 5 separate JSON columns** — allows per-endpoint queries
4. **Exception messages normalized** — frequently edited per-entity
5. **Group definitions unified** — system + table access in one table with discriminator
6. **Existing managers need zero changes** — they operate on in-memory dicts
7. **Only DefinitionManager.load()/save() needs the storage abstraction**

## Files Modified/Created This Session

```
emotisense-ai/swfaw/
├── swfaw_definition_store.sql              (NEW - 797 lines)
└── docs/db_store_design/
    ├── 00_OVERVIEW.md                      (NEW)
    ├── 01_FOUNDATION.md                    (NEW)
    ├── 02_PER_ENTITY_LAYERS.md             (NEW)
    ├── 03_QUERY_FILTER_LAYERS.md           (NEW)
    ├── 04_SECURITY_CONFIG.md               (NEW)
    ├── 05_APP_CONFIG_EXCEPTION.md          (NEW)
    ├── 06_AUDIT_AUTHORIZATION.md           (NEW)
    └── 07_MIGRATION_STRATEGY.md            (NEW)
```
