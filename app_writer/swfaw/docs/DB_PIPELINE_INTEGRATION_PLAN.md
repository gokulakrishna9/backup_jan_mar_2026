# DB Pipeline Integration Plan

## Goal

Wire the `db_managers/` MySQL backend into the swfaw_v2 code generation pipeline
alongside the existing JSON file backend. Both backends must be interchangeable.
The JSON workflow remains the default — DB is opt-in via `--storage db`.

---

## Current Pipeline (JSON Only)

```
SQL/JSON Input
    │
    ▼
Phase 1: SQLParser → DatabaseDefinition (Pydantic model)
    │
    ▼
split_definition() → application_definitions/*.json (15+ files)
    │
    ▼
Phase 2: load_split_definition() → DatabaseDefinition (reconstructed)
    │
    ▼
main.generate_application() → load_layer_definitions_if_exist()
    │                              │
    ├── layer defs found ──────────┤
    │   generate_from_layer_definitions()
    │
    ├── no layer defs ─────────────┤
    │   generate_from_transformers()
    │
    ▼
Generators (26) → 850+ Java files
```

### Key Data Flow Points

| Step | Function | Input | Output |
|------|----------|-------|--------|
| Parse | `load_or_parse_definition()` | .sql or .json file | `DatabaseDefinition` |
| Save (P1) | `split_definition()` | `DatabaseDefinition` | 15+ JSON files |
| Load (P2) | `load_split_definition()` | JSON files | `DatabaseDefinition` |
| Layer load | `load_layer_definitions_if_exist()` | JSON files | `Dict[str, Any]` or None |
| Generate | `generate_application()` | `DatabaseDefinition` + optional layer defs | Java files |

### What the Generators Actually Consume

The generators don't read JSON files directly. They consume:
1. `DatabaseDefinition` — the Pydantic model (tables, columns, relationships, project metadata)
2. `layer_definitions` — a dict of layer JSON data (entity_layer, repository_layer, etc.)

This means the storage backend only needs to produce these two objects.

---

## Target Pipeline (JSON + DB)

```
SQL/JSON Input
    │
    ▼
Phase 1: SQLParser → DatabaseDefinition
    │
    ├── --storage json (default) ──→ split_definition() → JSON files
    ├── --storage db ──────────────→ db_store.save() → MySQL tables
    └── --storage both ────────────→ JSON files + MySQL tables
    │
    ▼
Phase 2:
    │
    ├── --storage json (default) ──→ load_split_definition() → DatabaseDefinition
    └── --storage db ──────────────→ db_store.load() → DatabaseDefinition
    │
    ▼
main.generate_application() → unchanged (receives same objects)
```

---

## Implementation Stages

### Stage 1: Storage Abstraction Layer

**New module:** `emotisense-ai/swfaw/storage/`

Create an abstract interface that both JSON and DB backends implement.
The interface produces the exact same objects the generators already consume.

```
storage/
├── __init__.py
├── base.py            # Abstract DefinitionStore interface
├── json_store.py      # Wraps existing JSON file operations
└── db_store.py        # Implements interface using db_managers
```

#### `base.py` — Abstract Interface

```python
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from models.database_definition import DatabaseDefinition


class DefinitionStore(ABC):
    """Abstract storage backend for application definitions."""

    @abstractmethod
    def save(self, db_def: DatabaseDefinition, output_dir: str) -> str:
        """Save a complete application definition.
        Returns: identifier (file path for JSON, app_id for DB).
        """

    @abstractmethod
    def load(self, identifier: str) -> DatabaseDefinition:
        """Load a DatabaseDefinition from storage.
        identifier: output_dir for JSON, app_id for DB.
        """

    @abstractmethod
    def load_layer_definitions(self, identifier: str) -> Optional[Dict[str, Any]]:
        """Load layer definition data (entity_layer, repository_layer, etc.).
        Returns: dict of layer data or None if not available.
        """

    @abstractmethod
    def list_apps(self) -> List[Dict[str, Any]]:
        """List available application definitions."""

    @abstractmethod
    def delete(self, identifier: str) -> bool:
        """Delete an application definition."""
```

#### `json_store.py` — Wraps Existing Code

Delegates to the existing functions — no logic duplication:

```python
from .base import DefinitionStore
from utils.definition_splitter import split_definition, load_split_definition, load_layer_definitions_if_exist


class JsonStore(DefinitionStore):

    def save(self, db_def, output_dir):
        file_paths = split_definition(db_def, output_dir)
        return file_paths['manifest']

    def load(self, identifier):
        # identifier = output_dir
        return load_split_definition(identifier)

    def load_layer_definitions(self, identifier):
        return load_layer_definitions_if_exist(identifier)

    def list_apps(self):
        # Scan ../generated_application/ for manifest.json files
        ...

    def delete(self, identifier):
        # Remove output_dir
        ...
```

#### `db_store.py` — Uses db_managers

This is the core new work. It must:

1. **save()**: Convert `DatabaseDefinition` → insert into all 30 tables
2. **load()**: Read from tables → reconstruct `DatabaseDefinition`
3. **load_layer_definitions()**: Read layer tables → produce same dict structure as JSON

```python
from .base import DefinitionStore
from db_managers import (
    DbConnection, DbStoreManager, DbEntityManager,
    DbRelationshipManager, DbLayerManager,
    DbSecurityManager, DbConfigManager, DbExceptionManager,
    DbAuditManager, DbAuthorizationManager, DbGroupManager,
    DbQueryManager, DbFilterManager, DbDtoManager,
)


class DbStore(DefinitionStore):

    def __init__(self, db: DbConnection):
        self.db = db

    def save(self, db_def, output_dir):
        # 1. Create app definition row
        # 2. Insert entities (with columns_json)
        # 3. Insert relationships
        # 4. Generate and insert layer definitions
        # 5. Insert config layers (security, audit, etc.)
        # Returns: str(app_id)
        ...

    def load(self, identifier):
        # identifier = str(app_id)
        # 1. Load app definition → project metadata
        # 2. Load entities → tables with columns
        # 3. Load relationships → attach to tables
        # 4. Reconstruct DatabaseDefinition
        ...

    def load_layer_definitions(self, identifier):
        # 1. Load entity_layer rows → entity_layer dict
        # 2. Load repository_layer rows → repository_layer dict
        # 3. Load service_layer, controller_layer, dto_layer
        # 4. Return same dict structure as load_layer_definitions_if_exist()
        ...
```

##### save() — Detailed Mapping

The save operation must map `DatabaseDefinition` fields to the 30 DB tables.
This follows the same order as the JSON `split_definition()` function:

| DatabaseDefinition Field | DB Table(s) | Method |
|--------------------------|-------------|--------|
| `projectMetadata.*` | `swfaw_app_definition` | `DbStoreManager.create_app()` |
| `tables[].name, columns` | `swfaw_entity` | `DbEntityManager.add_entity()` |
| `tables[].relationships` | `swfaw_relationship` | `DbRelationshipManager.add_relationship()` |
| Layer definitions (generated) | `swfaw_entity_layer`, `swfaw_entity_layer_field`, `swfaw_repository_layer`, `swfaw_service_layer`, `swfaw_controller_layer`, `swfaw_dto_layer` | `DbLayerManager.insert()` |
| Query layer (generated) | `swfaw_query`, `swfaw_query_join`, `swfaw_query_parameter` | `DbQueryManager` |
| Filter layer (generated) | `swfaw_filter`, `swfaw_filter_field` | `DbFilterManager` |
| Security config (generated) | `swfaw_security_config`, `swfaw_security_*` | `DbSecurityManager` |
| App config (generated) | `swfaw_app_config` | `DbConfigManager` |
| Exception config (generated) | `swfaw_exception_config`, `swfaw_exception_*` | `DbExceptionManager` |
| Audit config (generated) | `swfaw_audit_config`, `swfaw_audit_*` | `DbAuditManager` |
| Authorization config (generated) | `swfaw_authorization_config`, `swfaw_entity_access_control` | `DbAuthorizationManager` |
| Group config (generated) | `swfaw_group_config`, `swfaw_group_definition` | `DbGroupManager` |

Note: The "generated" layer definitions come from `layer_definition_generator.py`.
During save, we call the same generator, then store the results in DB tables
instead of JSON files.

##### load() — Detailed Mapping

The load operation reconstructs `DatabaseDefinition` from DB tables:

```python
def load(self, identifier):
    app_id = int(identifier)
    store = DbStoreManager(self.db)
    app = store.get_app(app_id)

    # Reconstruct ProjectMetadata
    project_metadata = {
        "name": app["project_name"],
        "applicationName": app["application_name"],
        "groupId": app["group_id"],
        "artifactId": app["artifact_id"],
        "version": app["project_version"],
        "port": app["port"],
        "sqlFileName": app["sql_file_name"],
        "database": {
            "type": app["db_type"],
            "host": app["db_host"],
            "port": app["db_port"],
            "name": app["db_name"],
            "url": app["db_url"],
            "username": app["db_username"],
            "password": app["db_password"],
        }
    }

    # Reconstruct tables
    em = DbEntityManager(self.db, app_id)
    rm = DbRelationshipManager(self.db, app_id)
    entities = em.list_entities()
    all_rels = rm.list_relationships()

    tables = []
    for entity in entities:
        # columns are already parsed from columns_json
        entity_rels = [r for r in all_rels if r["source_table"] == entity["table_name"]]
        tables.append({
            "name": entity["table_name"],
            "columns": entity["columns"],
            "relationships": [{
                "type": r["relationship_type"],
                "targetTable": r["target_table"],
                "foreignKey": r["foreign_key_column"],
                "joinTable": r["join_table"],
            } for r in entity_rels]
        })

    return DatabaseDefinition(**{
        "projectMetadata": project_metadata,
        "tables": tables,
    })
```

##### load_layer_definitions() — Detailed Mapping

Must produce the exact same dict structure that `load_layer_definitions_if_exist()`
returns from JSON files. The generators expect this format:

```python
{
    "entity_layer": { ... },       # from swfaw_entity_layer + swfaw_entity_layer_field
    "repository_layer": { ... },   # from swfaw_repository_layer
    "service_layer": { ... },      # from swfaw_service_layer
    "controller_layer": { ... },   # from swfaw_controller_layer
    "dto_layer": { ... },          # from swfaw_dto_layer
}
```

Each layer dict must match the JSON file format exactly. This requires reading
the DB rows and reshaping them into the same nested structure the JSON files use.

---

### Stage 2: Wire Phase 1 to Storage Abstraction

**Modified file:** `phase1_generate_definition.py`

Add `--storage` argument:

```python
parser.add_argument(
    '--storage', '-s',
    choices=['json', 'db', 'both'],
    default='json',
    help='Storage backend: json (default), db (MySQL), both'
)
parser.add_argument(
    '--db-config',
    default=None,
    help='Path to DB config file (default: ~/.swfaw/db_config.json)'
)
```

In `save_application_definition()`, use the storage abstraction:

```python
from storage import JsonStore, DbStore

if args.storage in ('json', 'both'):
    json_store = JsonStore()
    json_store.save(db_def, output_dir)

if args.storage in ('db', 'both'):
    db = DbConnection.from_config(args.db_config)
    db_store = DbStore(db)
    app_id = db_store.save(db_def, output_dir)
    print(f">> Saved to database with app_id: {app_id}")
```

**No changes to:** parsers, transformers, models, or layer_definition_generator.

---

### Stage 3: Wire Phase 2 to Storage Abstraction

**Modified file:** `phase2_generate_code.py`

Add `--storage` and `--app-id` arguments:

```python
parser.add_argument(
    '--storage', '-s',
    choices=['json', 'db'],
    default='json',
    help='Storage backend to load from: json (default), db (MySQL)'
)
parser.add_argument(
    '--app-id',
    type=int,
    default=None,
    help='App definition ID (required when --storage db)'
)
```

In `load_application_definition()`:

```python
if args.storage == 'db':
    db = DbConnection.from_config(args.db_config)
    db_store = DbStore(db)
    db_def = db_store.load(str(args.app_id))
    layer_definitions = db_store.load_layer_definitions(str(args.app_id))
else:
    db_def = load_split_definition(args.output)
    layer_definitions = load_layer_definitions_if_exist(args.output)
```

**No changes to:** main.py, generators, or templates.

---

### Stage 4: Wire generate_app.py (Unified Workflow)

**Modified file:** `generate_app.py`

Pass `--storage` through to both phases. When `--storage db`:
- Phase 1 saves to DB, captures `app_id`
- Phase 2 loads from DB using that `app_id`

```python
parser.add_argument('--storage', '-s', choices=['json', 'db', 'both'], default='json')
parser.add_argument('--db-config', default=None)
```

---

### Stage 5: Update DefinitionManager (managers/)

**Modified file:** `managers/definition_manager.py`

Add optional `store` parameter:

```python
class DefinitionManager:
    def __init__(self, output_dir: str, store: Optional[DefinitionStore] = None):
        self.store = store or JsonStore()
        ...

    def load(self):
        self.db_def = self.store.load(str(self.output_dir))
        return self.db_def

    def save(self):
        return self.store.save(self.db_def, str(self.output_dir))
```

All downstream managers (EntityManager, FieldManager, LayerManager) remain unchanged —
they operate on the in-memory `DatabaseDefinition` object.

---

### Stage 6: JSON → DB Import Tool

**New file:** `tools/import_json_to_db.py`

Reads an existing `application_definitions/` folder and imports into the database.

```bash
python tools/import_json_to_db.py --input ../generated_application/my_app --db-config ~/.swfaw/db_config.json
```

Implementation:
1. `load_split_definition()` → `DatabaseDefinition`
2. `load_layer_definitions_if_exist()` → layer dicts
3. `DbStore.save()` → insert everything into DB

---

### Stage 7: DB → JSON Export Tool

**New file:** `tools/export_db_to_json.py`

Dumps a DB-stored definition back to JSON files.

```bash
python tools/export_db_to_json.py --app-id 1 --output ../generated_application/my_app_export
```

Implementation:
1. `DbStore.load()` → `DatabaseDefinition`
2. `split_definition()` → JSON files

---

### Stage 8: Testing & Validation

1. Round-trip test: JSON → DB → JSON produces identical output
2. Code generation from DB matches code generation from JSON
3. Import existing generated app into DB, regenerate, diff output
4. Test `--storage both` writes to both backends consistently
5. Test graceful fallback when MySQL is unavailable

---

## Files Created / Modified Summary

### New Files

| File | Purpose |
|------|---------|
| `storage/__init__.py` | Package exports |
| `storage/base.py` | Abstract `DefinitionStore` interface |
| `storage/json_store.py` | JSON backend (wraps existing functions) |
| `storage/db_store.py` | DB backend (uses db_managers) |
| `tools/import_json_to_db.py` | JSON → DB import tool |
| `tools/export_db_to_json.py` | DB → JSON export tool |

### Modified Files

| File | Change |
|------|--------|
| `phase1_generate_definition.py` | Add `--storage`, `--db-config` args |
| `phase2_generate_code.py` | Add `--storage`, `--app-id`, `--db-config` args |
| `generate_app.py` | Pass `--storage` through to both phases |
| `managers/definition_manager.py` | Accept optional `DefinitionStore` backend |

### Unchanged Files

Everything else: parsers, transformers, generators, templates, models, utils,
db_managers, main.py. The storage abstraction sits between the phases and the
generators — it doesn't touch the generation logic.

---

## Key Design Principles

1. **No breaking changes** — JSON remains the default, DB is opt-in
2. **Same objects** — Both backends produce `DatabaseDefinition` + layer dicts
3. **Generators are unaware** — They don't know or care about the storage backend
4. **DRY** — `json_store.py` delegates to existing functions, no duplication
5. **Incremental** — Each stage is independently testable and deployable
6. **Reversible** — DB → JSON export ensures you can always go back

---

## Execution Order

Stages should be implemented in order (1 → 8). Each stage is discussed before coding.

| Stage | Depends On | Estimated Scope |
|-------|-----------|-----------------|
| 1. Storage abstraction | — | 4 new files |
| 2. Phase 1 wiring | Stage 1 | 1 modified file |
| 3. Phase 2 wiring | Stage 1 | 1 modified file |
| 4. generate_app.py | Stages 2, 3 | 1 modified file |
| 5. DefinitionManager | Stage 1 | 1 modified file |
| 6. Import tool | Stage 1 | 1 new file |
| 7. Export tool | Stage 1 | 1 new file |
| 8. Testing | All stages | Test scripts |
