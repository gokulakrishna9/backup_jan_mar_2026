# Database Definition Store Managers Guide

## Overview

The Database Managers layer provides programmatic CRUD operations for manipulating application definitions stored in the `swfaw_definition_store` MySQL database. This is the DB-backed equivalent of the JSON-based `managers/` layer — same patterns, same method signatures, different backend.

**Version:** 2.5.0  
**Location:** `emotisense-ai/swfaw/db_managers/`  
**Schema:** `emotisense-ai/swfaw/swfaw_definition_store.sql`  
**Database:** MySQL 8.0+ (`swfaw_definition_store`, 30 tables)

## Architecture

The db_managers layer consists of 14 components organized by tier:

### Foundation
1. **DbConnection** - Connection pooling & query helpers
2. **DbStoreManager** - Root app definition CRUD (`swfaw_app_definition`)

### Tier 1-2: Entities & Per-Entity Layers
3. **DbEntityManager** - Entity CRUD (`swfaw_entity`)
4. **DbRelationshipManager** - Relationship CRUD (`swfaw_relationship`)
5. **DbDtoManager** - DTO layer CRUD (`swfaw_dto_layer`)

### Tier 3: Query & Filter
6. **DbQueryManager** - Custom queries + joins + parameters
7. **DbFilterManager** - Filters + filter fields

### Tier 4: Application-Wide Layers
8. **DbSecurityManager** - Security config + OAuth2 + CORS + public endpoints
9. **DbConfigManager** - App config (server, logging, swagger, caching, email)
10. **DbExceptionManager** - Exception config + definitions + messages
11. **DbAuditManager** - Audit config + events + alerts
12. **DbAuthorizationManager** - Authorization config + entity access control
13. **DbGroupManager** - Group config + group definitions

### Generic
14. **DbLayerManager** - Generic CRUD on ANY of the 30 tables via aliases ⭐

## Prerequisites

```bash
pip install mysql-connector-python
```

Create the database:
```bash
mysql -u root -p < emotisense-ai/swfaw/swfaw_definition_store.sql
```

## Installation

No additional installation beyond the MySQL connector. Import from `db_managers`:

```python
from db_managers import (
    DbConnection, DbStoreManager, DbEntityManager,
    DbRelationshipManager, DbLayerManager, DbSecurityManager,
    DbConfigManager, DbExceptionManager, DbAuditManager,
    DbAuthorizationManager, DbGroupManager, DbQueryManager,
    DbFilterManager, DbDtoManager,
)
```

---

## 1. DbConnection

Connection pooling and query helpers for the `swfaw_definition_store` database.

### Initialization

```python
from db_managers import DbConnection

# Direct connection
db = DbConnection(
    host="localhost",
    port=3306,
    database="swfaw_definition_store",
    user="root",
    password="password",
    pool_size=5,
)

# From config file (~/.swfaw/db_config.json)
db = DbConnection.from_config()

# From custom config file
db = DbConnection.from_config("/path/to/my_config.json")
```

### Config File Format (`~/.swfaw/db_config.json`)

```json
{
    "host": "localhost",
    "port": 3306,
    "database": "swfaw_definition_store",
    "user": "root",
    "password": "password",
    "pool_size": 5
}
```

### Query Methods

#### fetch_all(sql, params=None)
Execute a SELECT and return all rows as dicts.

```python
rows = db.fetch_all("SELECT * FROM swfaw_app_definition WHERE is_active = 1")
```

#### fetch_one(sql, params=None)
Execute a SELECT and return one row as a dict.

```python
row = db.fetch_one("SELECT * FROM swfaw_app_definition WHERE id = %s", (1,))
```

#### execute(sql, params=None)
Execute an INSERT/UPDATE/DELETE and return affected row count.

```python
affected = db.execute(
    "UPDATE swfaw_app_definition SET project_name = %s WHERE id = %s",
    ("NewName", 1)
)
```

#### insert(sql, params=None)
Execute an INSERT and return the last inserted ID.

```python
new_id = db.insert(
    "INSERT INTO swfaw_app_definition (project_name, application_name, artifact_id, db_name) "
    "VALUES (%s, %s, %s, %s)",
    ("MyProject", "MyApp", "my-app", "my_db")
)
```

#### execute_many(sql, params_list)
Execute a statement for multiple parameter sets.

```python
db.execute_many(
    "INSERT INTO swfaw_entity (app_definition_id, table_name, columns_json, column_count) "
    "VALUES (%s, %s, %s, %s)",
    [(1, "users", "[]", 0), (1, "orders", "[]", 0)]
)
```

#### execute_transaction(operations)
Execute multiple statements in a single transaction.

```python
results = db.execute_transaction([
    ("INSERT INTO swfaw_entity (app_definition_id, table_name, columns_json, column_count) VALUES (%s, %s, %s, %s)", (1, "users", "[]", 0)),
    ("INSERT INTO swfaw_entity (app_definition_id, table_name, columns_json, column_count) VALUES (%s, %s, %s, %s)", (1, "orders", "[]", 0)),
])
```

#### table_exists(table_name)
Check if a table exists in the database.

```python
if db.table_exists("swfaw_app_definition"):
    print("Schema is set up")
```

#### close()
Close the connection pool.

```python
db.close()
```

---

## 2. DbStoreManager

CRUD operations on `swfaw_app_definition` — the root table. Every other manager requires an `app_id` from this table.

### Initialization

```python
from db_managers import DbConnection, DbStoreManager

db = DbConnection.from_config()
store = DbStoreManager(db)
```

### Methods

#### create_app(...)
Create a new application definition. Returns the new `app_id`.

```python
app_id = store.create_app(
    project_name="Pet Store",
    application_name="PetStoreApp",
    artifact_id="pet-store",
    db_name="pet_store_db",
    group_id="com.example",
    project_version="1.0.0",
    port=8081,
    description="Demo pet store application",
)
print(f"Created app: id={app_id}")
```

#### get_app(app_id)
Get an application definition by ID.

```python
app = store.get_app(app_id)
print(f"Project: {app['project_name']}")
print(f"Database: {app['db_name']}")
```

#### get_app_by_artifact(group_id, artifact_id, version)
Get an app by its unique artifact coordinates.

```python
app = store.get_app_by_artifact("com.example", "pet-store", "1.0.0")
```

#### list_apps(active_only=True)
List all application definitions.

```python
apps = store.list_apps()
for app in apps:
    print(f"  [{app['id']}] {app['project_name']} - {app['db_name']}")
```

#### app_exists(app_id)
Check if an app definition exists.

```python
if store.app_exists(1):
    print("App 1 exists")
```

#### get_statistics(app_id)
Get statistics for an app definition.

```python
stats = store.get_statistics(app_id)
print(f"Entities: {stats['total_entities']}")
print(f"Relationships: {stats['total_relationships']}")
print(f"Columns: {stats['total_columns']}")
```

#### update_app(app_id, **kwargs)
Update fields on an app definition.

```python
store.update_app(app_id, port=8082, project_version="2.0.0")
```

#### refresh_statistics(app_id)
Recalculate and update the denormalized statistics counters.

```python
stats = store.refresh_statistics(app_id)
print(f"Updated stats: {stats}")
```

#### deactivate_app(app_id) / activate_app(app_id)
Soft-delete or re-activate an app definition.

```python
store.deactivate_app(app_id)   # Sets is_active = 0
store.activate_app(app_id)     # Sets is_active = 1
```

#### delete_app(app_id)
Hard-delete an app definition and all child rows (CASCADE).

```python
store.delete_app(app_id)
```

---

## 3. DbEntityManager

CRUD operations on `swfaw_entity` (replaces `entities.json`).

### Initialization

```python
from db_managers import DbConnection, DbEntityManager

db = DbConnection.from_config()
em = DbEntityManager(db, app_id=1)
```

### Methods

#### add_entity(table_name, columns=None, primary_key_column=None, sort_order=0)
Add a new entity definition.

```python
entity_id = em.add_entity("users", columns=[
    {"name": "id", "type": "BIGINT", "primaryKey": True, "nullable": False, "autoIncrement": True},
    {"name": "email", "type": "VARCHAR(255)", "nullable": False, "unique": True},
    {"name": "name", "type": "VARCHAR(255)", "nullable": False},
])
```

#### get_entity(table_name) / get_entity_by_id(entity_id)
Get an entity by table name or row ID. Auto-parses `columns_json`.

```python
entity = em.get_entity("users")
print(f"Columns: {entity['columns']}")
print(f"PK: {entity['primary_key_column']}")
```

#### list_entities() / list_entity_names()
List all entities or just their names.

```python
names = em.list_entity_names()  # ["orders", "users"]
entities = em.list_entities()    # Full row dicts with parsed columns
```

#### entity_exists(table_name)
```python
if em.entity_exists("users"):
    print("Users entity exists")
```

#### get_entity_details(table_name)
Get detailed info including relationship count.

```python
details = em.get_entity_details("users")
print(f"Columns: {details['column_count']}, Relationships: {details['relationship_count']}")
```

#### update_entity(table_name, **kwargs)
Update entity fields. Accepts `columns` as a list (auto-serialized).

```python
em.update_entity("users", columns=[...], primary_key_column="id")
```

#### remove_entity(table_name)
Remove an entity. CASCADE deletes child layer rows.

```python
em.remove_entity("old_table")
```

---

## 4. DbRelationshipManager

CRUD operations on `swfaw_relationship` (replaces `relationships.json`).

### Initialization

```python
from db_managers import DbConnection, DbRelationshipManager

db = DbConnection.from_config()
rm = DbRelationshipManager(db, app_id=1)
```

### Methods

#### add_relationship(source_table, target_table, relationship_type, foreign_key_column=None, join_table=None)

```python
# ManyToOne
rel_id = rm.add_relationship("orders", "users", "ManyToOne", foreign_key_column="user_id")

# ManyToMany
rel_id = rm.add_relationship("students", "courses", "ManyToMany", join_table="student_courses")
```

**Relationship Types:** `OneToOne`, `OneToMany`, `ManyToOne`, `ManyToMany`

#### get_relationships(table_name) / get_incoming_relationships(table_name) / get_all_relationships(table_name)

```python
outgoing = rm.get_relationships("orders")       # Where orders is source
incoming = rm.get_incoming_relationships("users") # Where users is target
all_rels = rm.get_all_relationships("users")      # Both directions
```

#### list_relationships()
List all relationships for this app.

```python
rels = rm.list_relationships()
```

#### relationship_exists(source_table, target_table, relationship_type)

```python
if rm.relationship_exists("orders", "users", "ManyToOne"):
    print("Relationship exists")
```

#### update_relationship(rel_id, **kwargs) / remove_relationship(rel_id)

```python
rm.update_relationship(rel_id, relationship_type="OneToOne")
rm.remove_relationship(rel_id)
```

#### remove_relationships_for_table(table_name)
Remove all relationships involving a table.

```python
rm.remove_relationships_for_table("old_table")
```

---

## 5. DbLayerManager ⭐

Generic CRUD on ANY of the 30 `swfaw_` tables using table aliases. This is the DB equivalent of `LayerManager` — the Swiss army knife.

### Initialization

```python
from db_managers import DbConnection, DbLayerManager

db = DbConnection.from_config()
lm = DbLayerManager(db, app_id=1)
```

### Table Aliases

| Alias | Table | Type |
|-------|-------|------|
| `app_definition` | `swfaw_app_definition` | Singleton |
| `entity` | `swfaw_entity` | Multi-row |
| `relationship` | `swfaw_relationship` | Multi-row |
| `entity_layer` | `swfaw_entity_layer` | Multi-row |
| `entity_layer_field` | `swfaw_entity_layer_field` | Multi-row (child) |
| `repository_layer` | `swfaw_repository_layer` | Multi-row |
| `service_layer` | `swfaw_service_layer` | Multi-row |
| `controller_layer` | `swfaw_controller_layer` | Multi-row |
| `dto_layer` | `swfaw_dto_layer` | Multi-row |
| `query` | `swfaw_query` | Multi-row |
| `query_join` | `swfaw_query_join` | Multi-row (child) |
| `query_parameter` | `swfaw_query_parameter` | Multi-row (child) |
| `filter` | `swfaw_filter` | Multi-row |
| `filter_field` | `swfaw_filter_field` | Multi-row (child) |
| `security_config` | `swfaw_security_config` | Singleton |
| `security_oauth2` | `swfaw_security_oauth2_provider` | Multi-row (child) |
| `security_cors` | `swfaw_security_cors` | Singleton (child) |
| `security_public_endpoint` | `swfaw_security_public_endpoint` | Multi-row (child) |
| `app_config` | `swfaw_app_config` | Singleton |
| `exception_config` | `swfaw_exception_config` | Singleton |
| `exception_definition` | `swfaw_exception_definition` | Multi-row |
| `exception_message` | `swfaw_exception_message` | Multi-row |
| `audit_config` | `swfaw_audit_config` | Singleton |
| `audit_event` | `swfaw_audit_event` | Multi-row (child) |
| `audit_alert` | `swfaw_audit_alert` | Multi-row (child) |
| `authorization_config` | `swfaw_authorization_config` | Singleton |
| `entity_access_control` | `swfaw_entity_access_control` | Multi-row (child) |
| `group_config` | `swfaw_group_config` | Singleton |
| `group_definition` | `swfaw_group_definition` | Multi-row |
| `custom_query_template` | `swfaw_custom_query_template` | Multi-row |

### Core Methods

#### get(alias, predicate=None)
Get rows from a table. Returns a single dict for singleton tables, or a list for multi-row tables.

```python
# Singleton table → returns dict
security = lm.get("security_config")
print(f"JWT expiration: {security['jwt_expiration']}")

# Multi-row table → returns list
entities = lm.get("entity_layer")
for e in entities:
    print(f"  {e['table_name']} → {e['class_name']}")

# With predicate filter
user_layer = lm.get("entity_layer", {"table_name": "users"})
```

#### get_value(alias, column, predicate=None)
Get a single column value.

```python
expiration = lm.get_value("security_config", "jwt_expiration")
class_name = lm.get_value("entity_layer", "class_name", {"table_name": "users"})
```

#### set(alias, column, value, predicate=None)
Set a single column value on matching rows. Auto-serializes `_json` columns.

```python
# Update singleton
lm.set("security_config", "jwt_expiration", 7200000)

# Update with predicate
lm.set("entity_layer", "has_audit_fields", 1, {"table_name": "users"})

# JSON column (auto-serialized)
lm.set("security_cors", "allowed_origins_json", ["http://localhost:3000"])
```

#### update(alias, updates, predicate=None)
Update multiple columns on matching rows.

```python
lm.update("security_config", {
    "jwt_expiration": 7200000,
    "jwt_issuer": "acme",
    "jwt_algorithm": "HS512",
})

lm.update("service_layer", {
    "has_authorization": 1,
    "auth_check_on_delete": 0,
}, {"entity_name": "users"})
```

#### insert(alias, data)
Insert a new row. Auto-injects `app_definition_id` and auto-serializes `_json` columns.

```python
lm.insert("entity_layer", {
    "table_name": "products",
    "class_name": "Product",
    "package_name": "com.example.entity",
    "has_audit_fields": 1,
})

lm.insert("security_public_endpoint", {
    "security_config_id": 1,
    "endpoint_pattern": "/api/v1/health",
})
```

#### delete(alias, predicate=None)
Delete rows matching the predicate.

```python
lm.delete("security_public_endpoint", {"endpoint_pattern": "/api/health"})
lm.delete("entity_layer", {"table_name": "old_table"})
```

#### find(alias, predicate)
Find the first row matching a predicate.

```python
row = lm.find("entity_layer", {"table_name": "users"})
if row:
    print(f"Class: {row['class_name']}")
```

#### filter(alias, predicate)
Filter all rows matching a predicate.

```python
user_dtos = lm.filter("dto_layer", {"entity_name": "users"})
print(f"Found {len(user_dtos)} DTOs for users")
```

#### exists(alias, predicate=None)
Check if any rows exist.

```python
if lm.exists("security_config"):
    print("Security is configured")

if lm.exists("entity_layer", {"table_name": "users"}):
    print("Users entity layer exists")
```

#### count(alias, predicate=None)
Count matching rows.

```python
total = lm.count("entity_layer")
print(f"Total entity layers: {total}")
```

#### list_tables() / describe(alias)
List available aliases or get column metadata.

```python
aliases = lm.list_tables()
columns = lm.describe("security_config")
```

### JSON Search — Predicate Syntax (`$`)

DbLayerManager supports querying JSON columns directly in predicates passed to `find`, `filter`, `get`, `exists`, `count`, and `delete`. Use the `$` separator in predicate keys:

| Predicate Key | MySQL Function | Description |
|---------------|---------------|-------------|
| `col$path` | `JSON_EXTRACT(col, path) = value` | Equality check at path |
| `col$path$contains` | `JSON_CONTAINS(col, value, path)` | Contains candidate at path |
| `col$contains` | `JSON_CONTAINS(col, value)` | Contains candidate (root) |
| `col$path$exists` | `JSON_CONTAINS_PATH(col, 'one', path)` | Path exists |
| `col$path$type` | `JSON_TYPE(JSON_EXTRACT(col, path)) = value` | Type check |
| `col$path$overlaps` | `JSON_OVERLAPS(JSON_EXTRACT(col, path), value)` | Any common elements |
| `col$path$length` | `JSON_LENGTH(JSON_EXTRACT(col, path)) = value` | Length check |

```python
# Find entities where columns_json contains a column named "email"
lm.find("entity", {"columns_json$contains": {"name": "email"}})

# Filter entities where a specific path contains a value
lm.filter("entity", {"columns_json$.items$contains": {"name": "email"}})

# Check if a JSON path exists
lm.exists("entity", {"columns_json$[0].name$exists": True})

# Check JSON type at a path
lm.filter("entity", {"columns_json$$type": "ARRAY"})

# Check array length
lm.filter("entity", {"columns_json$$length": 5})

# Check overlap with a set of values
lm.filter("entity", {"columns_json$[*].type$overlaps": ["VARCHAR", "TEXT"]})
```

### JSON Search — Dedicated MySQL JSON Methods

For more complex queries, DbLayerManager provides 14 dedicated methods that map directly to MySQL JSON functions.

#### Read Methods

##### json_extract(alias, column, path, predicate=None)
`JSON_EXTRACT` — extract values at a JSON path.

```python
# Get all column names from the users entity
names = lm.json_extract("entity", "columns_json", "$[*].name",
                        {"table_name": "users"})
```

##### json_value(alias, column, path, predicate=None)
`JSON_VALUE` — extract an unquoted scalar string.

```python
emails = lm.json_value("entity", "columns_json", "$[1].name",
                       {"table_name": "users"})
```

##### json_contains(alias, column, candidate, path=None, predicate=None)
`JSON_CONTAINS` — find rows where JSON contains a candidate value.

```python
# Find entities that have a column named "email"
rows = lm.json_contains("entity", "columns_json", {"name": "email"})

# Scoped to a path
rows = lm.json_contains("entity", "columns_json", "email", path="$[*].name")
```

##### json_contains_path(alias, column, *paths, mode="one", predicate=None)
`JSON_CONTAINS_PATH` — find rows where JSON path(s) exist.

```python
# Any of these paths exist
rows = lm.json_contains_path("entity", "columns_json", "$[*].name")

# All paths must exist
rows = lm.json_contains_path("entity", "columns_json",
                             "$[*].name", "$[*].type", mode="all")
```

##### json_search(alias, column, search_str, mode="one", path=None, predicate=None)
`JSON_SEARCH` — find rows where a string value matches (supports `%` and `_` wildcards).

```python
rows = lm.json_search("entity", "columns_json", "%email%")
rows = lm.json_search("entity", "columns_json", "email", path="$[*].name")
```

##### json_keys(alias, column, path=None, predicate=None)
`JSON_KEYS` — get keys of a JSON object at a path.

```python
keys = lm.json_keys("app_config", "config_json")
```

##### json_length(alias, column, path=None, predicate=None)
`JSON_LENGTH` — get length of JSON value at a path.

```python
lengths = lm.json_length("entity", "columns_json")
```

##### json_type(alias, column, path=None, predicate=None)
`JSON_TYPE` — get the MySQL JSON type (OBJECT, ARRAY, STRING, INTEGER, etc.).

```python
types = lm.json_type("entity", "columns_json")  # → ["ARRAY"]
```

##### json_overlaps(alias, column, candidate, path=None, predicate=None)
`JSON_OVERLAPS` — find rows where JSON has any common elements with candidate.

```python
rows = lm.json_overlaps("entity", "columns_json",
                        ["VARCHAR", "TEXT"], path="$[*].type")
```

#### Write Methods

##### json_set(alias, column, path_value_pairs, predicate=None)
`JSON_SET` — set values at paths (insert or update).

```python
lm.json_set("entity", "columns_json", {"$[0].nullable": False},
            {"table_name": "users"})
```

##### json_insert(alias, column, path_value_pairs, predicate=None)
`JSON_INSERT` — insert values only at paths that don't exist yet.

```python
lm.json_insert("entity", "columns_json",
               {"$[0].comment": "Primary key"},
               {"table_name": "users"})
```

##### json_replace(alias, column, path_value_pairs, predicate=None)
`JSON_REPLACE` — replace values only at paths that already exist.

```python
lm.json_replace("entity", "columns_json",
                {"$[0].type": "BIGINT UNSIGNED"},
                {"table_name": "users"})
```

##### json_remove(alias, column, *paths, predicate=None)
`JSON_REMOVE` — remove values at paths.

```python
lm.json_remove("entity", "columns_json", "$[2]",
               predicate={"table_name": "users"})
```

##### json_array_append(alias, column, path, value, predicate=None)
`JSON_ARRAY_APPEND` — append a value to a JSON array.

```python
lm.json_array_append("entity", "columns_json", "$",
                     {"name": "status", "type": "VARCHAR(50)"},
                     {"table_name": "users"})
```

---

## 6. DbSecurityManager

CRUD on security tables: `swfaw_security_config`, `swfaw_security_oauth2_provider`, `swfaw_security_cors`, `swfaw_security_public_endpoint`.

```python
from db_managers import DbConnection, DbSecurityManager

db = DbConnection.from_config()
sm = DbSecurityManager(db, app_id=1)

# Create config
sm.create_config(jwt_expiration=86400000, jwt_algorithm="HS256")

# Update
sm.update_config(jwt_issuer="my-company", rate_limit_default_per_min=120)

# CORS
sm.set_cors(
    cors_enabled=1,
    allowed_origins_json=["http://localhost:3000"],
    allowed_methods_json=["GET", "POST", "PUT", "DELETE"],
)

# OAuth2
sm.add_oauth2_provider("google",
    client_id="xxx", client_secret="yyy",
    redirect_uri="http://localhost:8080/oauth2/callback/google",
    scopes=["openid", "profile", "email"],
)
sm.remove_oauth2_provider("google")

# Public endpoints
sm.add_public_endpoint("/api/v1/auth/**")
sm.add_public_endpoint("/api/v1/health")
endpoints = sm.list_public_endpoints()
sm.remove_public_endpoint("/api/v1/health")
```

---

## 7. DbConfigManager

CRUD on `swfaw_app_config` with convenience methods for each config section.

```python
from db_managers import DbConnection, DbConfigManager

db = DbConnection.from_config()
cm = DbConfigManager(db, app_id=1)

# Create
cm.create_config(server_port=8081, java_version="21", swagger_enabled=1)

# Update any fields
cm.update_config(spring_boot_version="3.3.0", server_http2_enabled=1)

# Convenience methods
cm.set_logging(log_level_root="INFO", log_level_application="DEBUG")
cm.set_swagger(swagger_title="My API", swagger_description="API docs")
cm.set_caching(caching_enabled=1, caching_type="redis", caching_ttl=7200)
cm.set_email(email_enabled=1, email_host="smtp.example.com", email_port=587)
cm.set_r2dbc_pool(r2dbc_pool_max_size=100, r2dbc_pool_initial_size=20)
```

---

## 8. DbExceptionManager

CRUD on exception tables: config, definitions, and per-entity messages.

```python
from db_managers import DbConnection, DbExceptionManager

db = DbConnection.from_config()
exc = DbExceptionManager(db, app_id=1)

# Config (singleton)
exc.create_config(log_level="ERROR", resp_include_stack_trace=0)
exc.update_config(handle_validation_errors=1)

# Custom exception definitions
exc.add_exception("ResourceNotFoundException", 404, "Resource not found")
exc.add_exception("DuplicateResourceException", 409, "Resource already exists")
exc.list_exceptions()
exc.remove_exception("DuplicateResourceException")

# Per-entity messages
exc.add_message("ResourceNotFoundException", "users", "User not found")
exc.add_message("ResourceNotFoundException", "orders", "Order not found")
exc.update_message("ResourceNotFoundException", "users", "User not found with given ID")
exc.list_messages("ResourceNotFoundException")
exc.remove_message("ResourceNotFoundException", "orders")
```

---

## 9. DbAuditManager

CRUD on audit tables: config, events, and alerts.

```python
from db_managers import DbConnection, DbAuditManager

db = DbConnection.from_config()
am = DbAuditManager(db, app_id=1)

# Config (singleton)
am.create_config(audit_enabled=1, storage_retention_days=365)
am.update_config(exclude_read_operations=0)

# Events
am.add_event("AUTH", "LOGIN_SUCCESS", "INFO", "User {username} logged in",
             include_user_agent=True, include_location=True)
am.add_event("DATA", "ENTITY_CREATED", "INFO", "{entityName} created by {username}",
             include_entity_data=True)
am.list_events(category="AUTH")
am.remove_event("AUTH", "LOGIN_SUCCESS")

# Alerts
am.add_alert("LOGIN_FAILED", threshold=5, time_window_minutes=15,
             action="SEND_EMAIL", recipients=["admin@example.com"])
am.list_alerts()
am.remove_alert("LOGIN_FAILED")
```

---

## 10. DbAuthorizationManager

CRUD on authorization tables: config and entity access control.

```python
from db_managers import DbConnection, DbAuthorizationManager

db = DbConnection.from_config()
authz = DbAuthorizationManager(db, app_id=1)

# Config (singleton)
authz.create_config(
    authz_enabled=1,
    access_control_model="document-based",
    access_controls_json=["OWNER", "GROUP", "PUBLIC"],
    document_group_types_json=["VIEWER", "EDITOR", "ADMIN"],
)
authz.update_config(super_user_enabled=1, super_user_bypass_all=1)

# Entity access control
authz.add_entity_access("users", "users",
    enable_access_control=1, check_on_create=1, check_on_read=1)
authz.update_entity_access("users", check_on_delete=0)
authz.list_entity_access()
authz.get_entity_access("users")
authz.remove_entity_access("users")
```

---

## 11. DbGroupManager

CRUD on group tables: config and group definitions.

```python
from db_managers import DbConnection, DbGroupManager

db = DbConnection.from_config()
gm = DbGroupManager(db, app_id=1)

# Config (singleton)
gm.create_config(allow_runtime_creation=0, admin_group_name="Administrators")
gm.update_config(admin_can_grant_membership=1)

# System groups
gm.add_group("Administrators", "SYSTEM", is_super_group=1, description="Full access")
gm.add_group("Users", "SYSTEM", is_default_group=1, auto_assign_new_users=1)

# Table access groups
gm.add_group("orders_viewers", "TABLE_ACCESS",
    table_name="orders", entity_name="Order",
    group_type="VIEWER", access_level="READ",
    allow_read=1, allow_create=0, allow_update=0, allow_delete=0)

# Query
gm.list_system_groups()
gm.list_table_access_groups(table_name="orders")
gm.get_group("Administrators")
gm.update_group("Users", description="Default user group")
gm.remove_group("old_group")
```

---

## 12. DbQueryManager

CRUD on query tables: queries, joins, and parameters.

```python
from db_managers import DbConnection, DbQueryManager

db = DbConnection.from_config()
qm = DbQueryManager(db, app_id=1)

# Add a query
query_id = qm.add_query(
    entity_name="orders",
    query_name="findByUserAndStatus",
    return_type="OrderDto",
    select_fields=["o.id", "o.total", "o.status", "u.name AS user_name"],
    from_clause="orders o",
    description="Find orders by user and status",
    pagination=True,
)

# Add joins
qm.add_join(query_id, "LEFT JOIN", "users u", "o.user_id = u.id")

# Add parameters
qm.add_parameter(query_id, "userId", "Long", is_required=True)
qm.add_parameter(query_id, "status", "String", is_required=False, default_value="ACTIVE")

# Get full query with joins + params
full = qm.get_full_query("orders", "findByUserAndStatus")
print(f"Query: {full['query_name']}")
print(f"Joins: {len(full['joins'])}")
print(f"Params: {len(full['parameters'])}")

# List / remove
qm.list_queries(entity_name="orders")
qm.remove_query("orders", "findByUserAndStatus")
```

---

## 13. DbFilterManager

CRUD on filter tables: filters and filter fields.

```python
from db_managers import DbConnection, DbFilterManager

db = DbConnection.from_config()
fm = DbFilterManager(db, app_id=1)

# Add a filter for an entity
filter_id = fm.add_filter("users")

# Add filter fields
fm.add_field(filter_id, "email", "String", operators=["eq", "contains", "startsWith"])
fm.add_field(filter_id, "created_at", "LocalDateTime", operators=["gte", "lte", "between"])
fm.add_field(filter_id, "status", "String", operators=["eq", "in"])

# Get full filter with fields
full = fm.get_full_filter("users")
print(f"Filter fields: {len(full['fields'])}")

# Update / remove fields
fm.update_field(field_id, operators=["eq", "neq", "in"])
fm.remove_field(field_id)

# List / remove filters
fm.list_filters()
fm.list_fields("users")
fm.remove_filter("users")
```

---

## 14. DbDtoManager

CRUD on `swfaw_dto_layer`. Each entity typically has 3 DTOs: Input, Output, Filter.

```python
from db_managers import DbConnection, DbDtoManager

db = DbConnection.from_config()
dm = DbDtoManager(db, app_id=1)

# Add DTOs
dm.add_dto("users", "Input", "UserInputDto", field_configs=[
    {"fieldName": "email", "javaType": "String", "validation": {"required": True, "email": True}},
    {"fieldName": "name", "javaType": "String", "validation": {"required": True, "maxLength": 255}},
])

dm.add_dto("users", "Output", "UserOutputDto", field_configs=[
    {"fieldName": "id", "javaType": "Long"},
    {"fieldName": "email", "javaType": "String"},
    {"fieldName": "name", "javaType": "String"},
], exclude_sensitive_fields=["password"])

dm.add_dto("users", "Filter", "UserFilterDto", field_configs=[
    {"fieldName": "email", "javaType": "String"},
    {"fieldName": "status", "javaType": "String"},
])

# Query
dtos = dm.list_dtos("users")           # All DTOs for users
input_dto = dm.get_dto("users", "Input") # Specific DTO

# Update
dm.update_dto("users", "Input", field_configs=[...])

# Remove
dm.remove_dto("users", "Filter")
dm.remove_all_dtos("users")  # Remove all 3
```

---

## Complete Usage Example

```python
from db_managers import (
    DbConnection, DbStoreManager, DbEntityManager,
    DbRelationshipManager, DbLayerManager, DbSecurityManager,
    DbConfigManager, DbExceptionManager, DbQueryManager,
    DbFilterManager, DbDtoManager,
)

# 1. Connect
db = DbConnection.from_config()

# 2. Create app definition
store = DbStoreManager(db)
app_id = store.create_app(
    project_name="Pet Store",
    application_name="PetStoreApp",
    artifact_id="pet-store",
    db_name="pet_store_db",
)

# 3. Add entities
em = DbEntityManager(db, app_id)
em.add_entity("pets", columns=[
    {"name": "id", "type": "BIGINT", "primaryKey": True, "nullable": False},
    {"name": "name", "type": "VARCHAR(255)", "nullable": False},
    {"name": "owner_id", "type": "BIGINT", "nullable": True},
])
em.add_entity("owners", columns=[
    {"name": "id", "type": "BIGINT", "primaryKey": True, "nullable": False},
    {"name": "email", "type": "VARCHAR(255)", "nullable": False},
])

# 4. Add relationships
rm = DbRelationshipManager(db, app_id)
rm.add_relationship("pets", "owners", "ManyToOne", foreign_key_column="owner_id")

# 5. Configure layers via generic manager
lm = DbLayerManager(db, app_id)
lm.insert("entity_layer", {"table_name": "pets", "class_name": "Pet"})
lm.insert("entity_layer", {"table_name": "owners", "class_name": "Owner"})

# 6. Security
sm = DbSecurityManager(db, app_id)
sm.create_config(jwt_expiration=86400000)
sm.add_public_endpoint("/api/v1/auth/**")

# 7. App config
cm = DbConfigManager(db, app_id)
cm.create_config(server_port=8081, swagger_enabled=1, swagger_title="Pet Store API")

# 8. Exceptions
exc = DbExceptionManager(db, app_id)
exc.create_config()
exc.add_exception("PetNotFoundException", 404, "Pet not found")

# 9. Custom query
qm = DbQueryManager(db, app_id)
q_id = qm.add_query("pets", "findBySpecies", "PetDto",
    select_fields=["p.*"], from_clause="pets p")
qm.add_parameter(q_id, "species", "String")

# 10. Refresh stats
store.refresh_statistics(app_id)
print(f"Done! App ID: {app_id}")
```

---

## JSON ↔ DB Manager Comparison

| JSON Manager | DB Manager | Notes |
|-------------|-----------|-------|
| `DefinitionManager` | `DbStoreManager` | Root definition CRUD |
| `EntityManager` | `DbEntityManager` | Entity/table CRUD |
| `FieldManager` | (use `DbEntityManager.update_entity`) | Fields stored as JSON in entity |
| `RelationshipManager` | `DbRelationshipManager` | Relationship CRUD |
| `LayerManager` | `DbLayerManager` | Generic CRUD (files → tables) |
| `QueryManager` | `DbQueryManager` | Custom query CRUD |
| `FilterManager` | `DbFilterManager` | Filter CRUD |
| — | `DbSecurityManager` | New: dedicated security CRUD |
| — | `DbConfigManager` | New: dedicated app config CRUD |
| — | `DbExceptionManager` | New: dedicated exception CRUD |
| — | `DbAuditManager` | New: dedicated audit CRUD |
| — | `DbAuthorizationManager` | New: dedicated authz CRUD |
| — | `DbGroupManager` | New: dedicated group CRUD |
| — | `DbDtoManager` | New: dedicated DTO CRUD |

### Key Differences

1. **No load/save cycle** — DB managers write immediately (no `def_manager.save()` needed)
2. **app_id scoping** — Every manager takes `app_id` to scope operations to one app definition
3. **Auto JSON handling** — Columns ending in `_json` are auto-serialized/deserialized
4. **Connection pooling** — `DbConnection` manages a MySQL connection pool
5. **Config file** — Connection details in `~/.swfaw/db_config.json`

---

## Best Practices

1. **Use `DbConnection.from_config()`** for consistent connection management
2. **Create the app definition first** — all other managers need the `app_id`
3. **Use specialized managers** for domain-specific operations (security, audit, etc.)
4. **Use `DbLayerManager`** for quick ad-hoc operations on any table
5. **Call `refresh_statistics()`** after bulk entity/relationship changes
6. **Use `execute_transaction()`** for multi-table atomic operations
7. **Use JSON predicate syntax (`$`)** for quick JSON column queries in find/filter
8. **Use dedicated JSON methods** for complex JSON operations (multi-path, wildcards, writes)

---

## 15. Storage Abstraction Layer

**Location:** `emotisense-ai/swfaw/storage/`  
**Purpose:** Pluggable storage backends for the two-phase code generation pipeline

The storage layer sits between the CLI scripts (Phase 1 / Phase 2 / generate_app.py) and the generators. It provides a unified interface so the pipeline can read/write application definitions from either JSON files or the MySQL database — or both.

### Architecture

```
SQL Schema → Phase 1 → DefinitionStore.save() → JSON files and/or DB rows
                                                        ↓
             Phase 2 ← DefinitionStore.load() ← JSON files or DB rows → Generators
```

### DefinitionStore (Abstract Interface)

```python
from storage import DefinitionStore

class DefinitionStore(ABC):
    def save(self, db_def, output_dir) -> str: ...
    def load(self, identifier) -> DatabaseDefinition: ...
    def load_layer_definitions(self, identifier) -> Optional[Dict]: ...
    def list_apps(self) -> List[Dict]: ...
    def delete(self, identifier) -> bool: ...
```

### JsonStore

Wraps existing `split_definition` utilities. Zero-config, default backend.

```python
from storage import JsonStore

store = JsonStore()
manifest = store.save(db_def, output_dir)       # → application_definitions/*.json
db_def = store.load(output_dir)                  # ← reads from application_definitions/
layers = store.load_layer_definitions(output_dir)
```

### DbStore

Uses all 14 db_managers for full DB-backed storage.

```python
from storage import DbStore
from db_managers import DbConnection

db = DbConnection.from_config()
store = DbStore(db)
app_id = store.save(db_def, output_dir)          # → inserts into 30 swfaw_ tables
db_def = store.load(app_id)                      # ← reads from DB
layers = store.load_layer_definitions(app_id)
```

### CLI Flags

All three entry points (`generate_app.py`, `phase1_generate_definition.py`, `phase2_generate_code.py`) accept:

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--storage` | `json`, `db`, `both` | `json` | Storage backend to use |
| `--app-id` | integer | — | Required when `--storage db` in Phase 2 |
| `--db-config` | file path | `~/.swfaw/db_config.json` | DB connection config |

```bash
# JSON only (default — same as before)
python generate_app.py --input schema.sql

# Both JSON and DB
python generate_app.py --input schema.sql --storage both

# DB only
python generate_app.py --input schema.sql --storage db

# Phase 2 from DB
python phase2_generate_code.py --output ../generated_application/my_app --storage db --app-id 1
```

### DefinitionManager Integration

The existing `DefinitionManager` in `managers/` accepts an optional `store` parameter:

```python
from managers import DefinitionManager
from storage import DbStore
from db_managers import DbConnection

db = DbConnection.from_config()
store = DbStore(db)

dm = DefinitionManager("../generated_application/my_app", store=store)
dm.load()   # delegates to store.load()
dm.save()   # delegates to store.save()
```

---

## 16. Import/Export Tools

**Location:** `emotisense-ai/swfaw/tools/`

### import_json_to_db.py

Import an existing JSON application definition into the MySQL database.

```bash
cd emotisense-ai/swfaw

# Default DB config
python tools/import_json_to_db.py --input ../generated_application/my_app

# Custom DB config
python tools/import_json_to_db.py --input ../generated_application/my_app --db-config /path/to/config.json
```

### export_db_to_json.py

Export a database-stored application definition back to JSON files.

```bash
cd emotisense-ai/swfaw

# Export app_id 1 to a new directory
python tools/export_db_to_json.py --app-id 1 --output ../generated_application/my_app_export

# Custom DB config
python tools/export_db_to_json.py --app-id 1 --output ../generated_application/my_app_export --db-config /path/to/config.json
```

---

## Files Reference

| File | Description |
|------|-------------|
| `db_managers/__init__.py` | Package exports |
| `db_managers/db_connection.py` | Connection pooling & query helpers |
| `db_managers/db_store_manager.py` | App definition CRUD |
| `db_managers/db_entity_manager.py` | Entity CRUD |
| `db_managers/db_relationship_manager.py` | Relationship CRUD |
| `db_managers/db_layer_manager.py` | Generic table CRUD + MySQL JSON functions |
| `db_managers/db_security_manager.py` | Security config CRUD |
| `db_managers/db_config_manager.py` | App config CRUD |
| `db_managers/db_exception_manager.py` | Exception config CRUD |
| `db_managers/db_audit_manager.py` | Audit config CRUD |
| `db_managers/db_authorization_manager.py` | Authorization CRUD |
| `db_managers/db_group_manager.py` | Group config CRUD |
| `db_managers/db_query_manager.py` | Custom query CRUD |
| `db_managers/db_filter_manager.py` | Filter CRUD |
| `db_managers/db_dto_manager.py` | DTO layer CRUD |
| `storage/__init__.py` | Storage package exports |
| `storage/base.py` | Abstract DefinitionStore interface |
| `storage/json_store.py` | JSON file storage backend |
| `storage/db_store.py` | MySQL database storage backend |
| `tools/import_json_to_db.py` | Import JSON definition into DB |
| `tools/export_db_to_json.py` | Export DB definition to JSON |
| `examples/db_managers_example.py` | End-to-end usage example |
| `swfaw_definition_store.sql` | Database schema (30 tables) |
| `docs/db_store_design/` | Schema design documentation (7 docs) |
| `docs/DB_PIPELINE_INTEGRATION_PLAN.md` | DB pipeline integration plan |
