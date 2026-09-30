# App Definition Manager

Workspace tool for scaffolding, editing, and tracking application definitions. Works with the Phase 3 definition-first pipeline (`swfaw/phase3_definition_first.py`) to generate SQL DDL + Java code from `application_definitions/<app_name>/`.

## Quick Start

```bash
# Scaffold a new app
py app_def_manager/cli.py scaffold --name my_app --entities '[{"name":"User","fields":[{"name":"email","type":"String"}]}]'

# Generate code from definitions
py swfaw/phase3_definition_first.py --app my_app --output generated_application/my_app
```

## CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `scaffold` | Create new app with all definition files | `--name my_app --entities '<json>' [--db-name <db>] [--base-package com.example] [--force]` |
| `add-entity` | Add entity to all 6 layer files | `--app my_app --name Product --fields '<json>'` |
| `remove-entity` | Remove entity from all 6 layer files | `--app my_app --name Product` |
| `add-field` | Add field to entity_layer + entities + dto_layer | `--app my_app --entity User --field '{"name":"age","type":"Integer"}'` |
| `remove-field` | Remove field from 3 layer files | `--app my_app --entity User --field age` |
| `modify-field` | Update field properties in 3 layer files | `--app my_app --entity User --field age --updates '{"type":"Long"}'` |
| `add-endpoint` | Add custom endpoint to controller_layer | `--app my_app --entity User --endpoint '<json>'` |
| `remove-endpoint` | Remove custom endpoint | `--app my_app --entity User --endpoint search` |
| `add-query` | Add custom query to repository_layer | `--app my_app --entity User --query '<json>'` |
| `remove-query` | Remove custom query | `--app my_app --entity User --query findByEmail` |
| `add-relationship` | Add relationship to relationships file | `--app my_app --relationship '<json>'` |
| `remove-relationship` | Remove relationship | `--app my_app --source Post --target User` |
| `status` | Show dirty/clean status per file | `--app my_app` |
| `mark-clean` | Mark file(s) as clean | `--app my_app [--file <filename>]` |
| `mark-dirty` | Mark file(s) as dirty | `--app my_app [--file <filename>]` |
| `list-apps` | List all application definitions | _(no args)_ |
| `list-entities` | List entities in an app | `--app my_app` |

## Definition Files

Each app under `application_definitions/<app_name>/` contains these files:

### Required Files (9)

| File | Purpose | Key Contents |
|------|---------|-------------|
| `webflux_manifest.json` | Index file | Version, file references, statistics |
| `webflux_project_metadata.json` | Project config | App name, database config, port, package |
| `webflux_entity_layer.json` | Entity definitions | Table/class names, fields with types, PK/nullable/columnDefinition |
| `webflux_entities.json` | Column-level view | Table names with SQL column definitions (used by DatabaseDefinition reconstruction) |
| `webflux_relationships.json` | Entity relationships | FK references between tables (ManyToOne, OneToMany, etc.) |
| `webflux_repository_layer.json` | Repository config | R2DBC repos per entity, custom queries, soft-delete, caching |
| `webflux_service_layer.json` | Service config | Business logic per entity, authorization, transactions |
| `webflux_controller_layer.json` | Controller config | REST endpoints per entity (CRUD + custom), CORS, rate limits |
| `webflux_dto_layer.json` | DTO config | Input/Output/Filter DTOs per entity with field inclusion and validation |

### Tracking File (1)

| File | Purpose |
|------|---------|
| `_generation_status.json` | Dirty/clean status per definition file, SHA-256 hashes, timestamps |

### Optional Files

| File | Purpose |
|------|---------|
| `webflux_query_layer.json` | Custom R2DBC queries |
| `webflux_filter_layer.json` | Filter configurations |
| `webflux_security_layer.json` | Security/auth config |
| `webflux_config_layer.json` | Application config overrides |
| `webflux_custom_queries_layer.json` | Advanced custom queries |
| `webflux_group_definition_layer.json` | Authorization group definitions |
| `webflux_authorization_layer.json` | Per-entity authorization rules |
| `webflux_audit_logging_layer.json` | Audit logging config |
| `webflux_exception_layer.json` | Custom exception handling |

## Entity Layer Fields

Each entity in `webflux_entity_layer.json` has:

| Property | Type | Description |
|----------|------|-------------|
| `tableName` | string | SQL table name (snake_case, e.g. `user_profile`) |
| `className` | string | Java class name (PascalCase, e.g. `UserProfile`) |
| `packageName` | string | Java package (e.g. `com.example.entity`) |
| `fields` | array | Field definitions (see below) |
| `hasAuditFields` | bool | Whether `created_at`/`updated_at` are present |
| `hasSoftDelete` | bool | Whether `is_deleted` field is present |

### Field Properties

| Property | Type | Description |
|----------|------|-------------|
| `columnName` | string | SQL column name (snake_case) |
| `fieldName` | string | Java field name (camelCase) |
| `javaType` | string | Java type (`Long`, `String`, `LocalDate`, `Boolean`, etc.) |
| `isPrimaryKey` | bool | Whether this field is the primary key |
| `isNullable` | bool | Whether the column allows NULL |
| `columnDefinition` | string | Verbatim SQL type (e.g. `BIGINT UNSIGNED`, `VARCHAR(255)`) — used by DDLGenerator |

### Auto-Generated Fields

When scaffolding or adding an entity, these fields are added automatically:

| Field | columnName | javaType | Notes |
|-------|-----------|----------|-------|
| Primary key | `{table_name}_id` | Long | isPrimaryKey=true, BIGINT UNSIGNED |
| Created timestamp | `created_at` | LocalDateTime | isNullable=false, TIMESTAMP |
| Updated timestamp | `updated_at` | LocalDateTime | isNullable=false, TIMESTAMP |
| Soft delete flag | `is_deleted` | Boolean | isNullable=false, BOOLEAN |

## Java Type → SQL Type Mapping

When `columnDefinition` is empty, DDLGenerator falls back to this mapping:

| Java Type | SQL Type |
|-----------|----------|
| Long | BIGINT UNSIGNED |
| Integer | INT |
| Short | SMALLINT |
| Byte | TINYINT |
| String | VARCHAR(255) |
| Boolean | BOOLEAN |
| LocalDate | DATE |
| LocalDateTime | TIMESTAMP |
| LocalTime | TIME |
| BigDecimal | DECIMAL(19,4) |
| Float | FLOAT |
| Double | DOUBLE |
| byte[] | BLOB |
| UUID | VARCHAR(36) |

Unknown types default to `VARCHAR(255)` with a warning.

## Components

| Component | File | Purpose |
|-----------|------|---------|
| StatusTracker | `status_tracker.py` | Dirty/clean tracking per file via `_generation_status.json` |
| Scaffolder | `scaffolder.py` | Creates all 9+1 definition files from entity descriptions |
| CRUDManager | `crud.py` | Granular add/remove/modify on entities, fields, endpoints, queries, relationships |
| CLI | `cli.py` | Argparse CLI routing to Scaffolder/CRUDManager/StatusTracker |

## Dirty/Clean Tracking

- Every mutation (scaffold, add-entity, add-field, etc.) marks affected files as **dirty**
- `_generation_status.json` stores per-file: status, last_modified, last_generated, content_hash (SHA-256)
- Phase 3 reads dirty files → DependencyMapper resolves which generated files need regeneration → IncrementalGenerator regenerates only those → marks clean
- External edits detected: if a clean file's hash doesn't match stored hash, auto-marked dirty with a warning

## Dependency Map

Which definition files affect which generated outputs:

| Definition File | Triggers Regeneration Of |
|----------------|--------------------------|
| entity_layer | Entity, all DTOs, Repository, Service, Controller, SQL |
| entities | Entity, SQL |
| relationships | Entity, Repository, SQL |
| repository_layer | Repository |
| service_layer | Service |
| controller_layer | Controller |
| dto_layer | Input/Output/Filter DTOs |
| project_metadata | Config, POM, SQL |
