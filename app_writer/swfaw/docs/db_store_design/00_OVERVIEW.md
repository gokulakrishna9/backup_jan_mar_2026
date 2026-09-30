# Application Definition Database Store Design

## Overview

This document series describes the database schema design for migrating swfaw_v2's
application definition layer from JSON files to a relational database (MySQL).

## Current State (JSON Files)

The application definition is currently stored as 18 JSON files in the
`application_definitions/` folder of each generated application:

| # | File | Type | Description |
|---|------|------|-------------|
| 1 | `manifest.json` | App-wide | Version, format, file index, statistics |
| 2 | `project_metadata.json` | App-wide | Project name, groupId, database config |
| 3 | `entities.json` | App-wide | All table definitions with columns |
| 4 | `relationships.json` | App-wide | All table relationships |
| 5 | `entity_layer.json` | Per-entity | R2DBC entity class config (fields, flags) |
| 6 | `repository_layer.json` | Per-entity | Repository config (caching, soft delete) |
| 7 | `service_layer.json` | Per-entity | Service config (auth, transactions) |
| 8 | `controller_layer.json` | Per-entity | REST endpoints, CORS, rate limiting |
| 9 | `dto_layer.json` | Per-entity | Input/Output/Filter DTOs with validation |
| 10 | `query_layer.json` | Per-entity | Custom R2DBC queries with joins |
| 11 | `filter_layer.json` | Per-entity | Filter fields and operators |
| 12 | `security_layer.json` | App-wide | JWT, OAuth2, CORS, CSRF, rate limiting |
| 13 | `config_layer.json` | App-wide | Server, logging, features (swagger, etc.) |
| 14 | `exception_layer.json` | App-wide | Custom exceptions, error format |
| 15 | `audit_logging_layer.json` | App-wide | Audit events, storage, alerting |
| 16 | `authorization_layer.json` | App-wide | Access controls, entity permissions |
| 17 | `group_definition_layer.json` | App-wide | System groups, table access groups |
| 18 | `custom_queries_layer.json` | App-wide | Authorization custom query templates |

## Target State (Database Tables)

The 18 JSON files map to **30 database tables** organized into 4 tiers:

### Tier 1: Foundation (2 tables)
- `swfaw_app_definition` — Root table (manifest + project metadata)
- `swfaw_entity` — Table/entity definitions with columns stored as JSON

### Tier 2: Per-Entity Layers (7 tables)
- `swfaw_relationship` — Table relationships
- `swfaw_entity_layer` — R2DBC entity generation config
- `swfaw_entity_layer_field` — Entity field definitions
- `swfaw_repository_layer` — Repository generation config
- `swfaw_service_layer` — Service generation config
- `swfaw_controller_layer` — Controller/endpoint generation config
- `swfaw_dto_layer` — DTO generation config (with field configs as JSON)

### Tier 3: Query & Filter Layers (5 tables)
- `swfaw_query` — Custom R2DBC query definitions
- `swfaw_query_join` — Query join clauses
- `swfaw_query_parameter` — Query parameters
- `swfaw_filter` — Filter definitions per entity
- `swfaw_filter_field` — Filter field + operator definitions

### Tier 4: Application-Wide Layers (16 tables)
- `swfaw_security_config` — JWT, password policy, session, CSRF, rate limiting
- `swfaw_security_oauth2_provider` — OAuth2 provider configs
- `swfaw_security_cors` — CORS configuration
- `swfaw_security_public_endpoint` — Public endpoint whitelist
- `swfaw_app_config` — Server, logging, features config
- `swfaw_exception_config` — Global exception handling settings
- `swfaw_exception_definition` — Custom exception classes
- `swfaw_exception_message` — Per-entity exception messages
- `swfaw_audit_config` — Audit logging configuration
- `swfaw_audit_event` — Audit event definitions
- `swfaw_audit_alert` — Audit alerting rules
- `swfaw_authorization_config` — Access control model + super user settings
- `swfaw_entity_access_control` — Per-entity authorization flags
- `swfaw_group_config` — Group management + owner enrollment settings
- `swfaw_group_definition` — System groups + table access groups
- `swfaw_custom_query_template` — Authorization custom query templates

## Design Principles

1. **Every table prefixed with `swfaw_`** to avoid collisions with generated app tables
2. **`app_definition_id` is the universal FK** — every table links back to the root
3. **JSON columns for deeply nested/variable structures** — avoids over-normalization
4. **Flat columns for frequently queried/filtered fields** — keeps queries simple
5. **Soft delete via `is_active`** on the root table only
6. **Audit columns** (`date_created`, `date_modified`) on all tables
7. **No auto-increment on child tables** where natural keys exist

## Document Index

| File | Content |
|------|---------|
| `00_OVERVIEW.md` | This file — overview and table index |
| `01_FOUNDATION.md` | Tier 1: app_definition + entity tables |
| `02_PER_ENTITY_LAYERS.md` | Tier 2: entity/repo/service/controller/dto layers |
| `03_QUERY_FILTER_LAYERS.md` | Tier 3: query + filter layer tables |
| `04_SECURITY_CONFIG.md` | Tier 4a: security + CORS + OAuth2 tables |
| `05_APP_CONFIG_EXCEPTION.md` | Tier 4b: app config + exception tables |
| `06_AUDIT_AUTHORIZATION.md` | Tier 4c: audit + authorization + group tables |
| `07_MIGRATION_STRATEGY.md` | Migration plan: JSON → DB, code changes needed |
