# App Definition Manager → Definition Files → Generated Code: One-to-One Mapping

> This document maps every App Def Manager CLI command to the JSON definition properties it creates/modifies,
> and then maps those properties to the generated code produced by swfaw (Java WebFlux) and REAW (React).

---

## Table of Contents

1. [Definition File Overview](#1-definition-file-overview)
2. [scaffold Command](#2-scaffold-command)
3. [Entity Operations](#3-entity-operations)
4. [Field Operations](#4-field-operations)
5. [Endpoint Operations](#5-endpoint-operations)
6. [Query Operations](#6-query-operations)
7. [Relationship Operations](#7-relationship-operations)
8. [Document Storage Operations](#8-document-storage-operations)
9. [bulk-update Command](#9-bulk-update-command)
10. [Status Tracking](#10-status-tracking)
11. [AI Layer Operations](#11-ai-layer-operations)
12. [Property-Level Mapping: WebFlux Definitions → swfaw Generated Java](#12-property-level-mapping-webflux-definitions--swfaw-generated-java)
13. [Property-Level Mapping: React Definitions → REAW Generated React](#13-property-level-mapping-react-definitions--reaw-generated-react)
14. [Java Type → SQL Type Mapping](#14-java-type--sql-type-mapping)
15. [Generation Flow Diagram](#15-generation-flow-diagram)

---

## 1. Definition File Overview

### WebFlux (Backend) Definition Files

| File | Layer Alias | Purpose |
|------|-------------|---------|
| `webflux_manifest.json` | `manifest` | Index of all definition files, version, statistics |
| `webflux_project_metadata.json` | `project_metadata` | Project name, package, database config, port |
| `webflux_entities.json` | `entities` | Raw table/column definitions (SQL-level view) |
| `webflux_entity_layer.json` | `entity` | JPA/R2DBC entity configuration (Java-level view) |
| `webflux_repository_layer.json` | `repository` | Repository interfaces, custom queries, caching |
| `webflux_service_layer.json` | `service` | Service classes, authorization, transactions |
| `webflux_controller_layer.json` | `controller` | REST endpoints, CORS, rate limiting, roles |
| `webflux_dto_layer.json` | `dto` | Input/Output/Filter DTOs per entity |
| `webflux_relationships.json` | `relationships` | Entity relationships (FK, join definitions) |
| `webflux_document_storage_layer.json` | — | File storage, JSON columns, document collections |
| `webflux_ai_layer.json` | — | AI providers, capabilities, RAG, evaluators, etc. |

### React (Frontend) Definition Files

| File | Concern | Purpose |
|------|---------|---------|
| `react_manifest.json` | manifest | Index of all React definition files |
| `react_routes.json` | routing | URL paths, page components, nav labels, auth |
| `react_page_definitions.json` | page_definitions | Page layouts (CSS Grid), component placements |
| `react_component_mappings.json` | component_mappings | Field → React component mapping per entity |
| `react_form_groupings.json` | form_groupings | Tabbed form groupings across related entities |
| `react_layout.json` | layout | App shell layout (header, footer, sidebar, nav groups) |
| `react_auth_config.json` | authentication | JWT/OAuth2 config, protected routes, login endpoints |
| `react_api_services.json` | api_services | API endpoint definitions per entity |
| `react_redux_store.json` | redux_store | Redux slices, thunks, pagination per entity |
| `react_theme.json` | theme | Colors, typography, spacing, shadows, animations |
| `react_env.json` | env_config | Environment variables (VITE_API_BASE_URL, etc.) |
| `react_ai_config.json` | — | Chat panel, entity AI features, standalone AI features |

---

## 2. scaffold Command

```
py app_def_manager/cli.py scaffold --name <app> --entities <json> [--db-name <name>] [--base-package <pkg>] [--force]
```

### Arguments → Definition Properties

| Argument | Definition File | Property Path | Default |
|----------|----------------|---------------|---------|
| `--name` | `webflux_project_metadata.json` | `projectMetadata.name` (kebab-case), `projectMetadata.applicationName` (Title Case) | — |
| `--name` | `webflux_project_metadata.json` | `projectMetadata.artifactId` (kebab-case) | — |
| `--db-name` | `webflux_project_metadata.json` | `projectMetadata.database.name` | snake_case of `--name` |
| `--base-package` | `webflux_project_metadata.json` | `projectMetadata.groupId` | `com.example` |
| `--entities` | All 6 layer files | Creates entries in entity, entities, repository, service, controller, dto layers | — |

### Files Created by scaffold

All 12 definition files are created:
- `webflux_manifest.json` — version `2.5`, format `split`, file index, statistics
- `webflux_project_metadata.json` — project name, database config (mysql, localhost:3306, root/password), port 8081
- `webflux_entity_layer.json` — entity definitions with auto-generated PK + audit fields
- `webflux_entities.json` — column-level view of same entities
- `webflux_repository_layer.json` — one repository per entity, all flags false
- `webflux_service_layer.json` — one service per entity, first entity is `isRootEntity: true`
- `webflux_controller_layer.json` — one controller per entity with 5 CRUD endpoints
- `webflux_dto_layer.json` — 3 DTOs per entity (Input, Output, Filter)
- `webflux_relationships.json` — empty relationships array
- `webflux_document_storage_layer.json` — empty (fileStorage disabled)
- `webflux_ai_layer.json` — empty AI layer skeleton
- `react_ai_config.json` — all AI features disabled
- `_generation_status.json` — all files marked dirty

### Auto-Generated Fields Per Entity

For each entity, the scaffolder automatically adds:
1. **Primary key**: `{table_name}_id` (Long, BIGINT UNSIGNED, not nullable)
2. **Audit fields**: `created_at` (TIMESTAMP), `updated_at` (TIMESTAMP)

---

## 3. Entity Operations

### add-entity

```
py app_def_manager/cli.py add-entity --app <app> --name <EntityName> --fields '[{"name":"email","type":"String"}]'
```

**Touches 6 files** (marks all dirty):

| File | Array Path | Entry Created |
|------|-----------|---------------|
| `webflux_entity_layer.json` | `entities[]` | `{tableName, className, packageName, fields[], hasAuditFields: true, hasSoftDelete: false}` |
| `webflux_entities.json` | `entities[]` | `{name: table_name, columns[]}` |
| `webflux_repository_layer.json` | `repositories[]` | `{entityName, className, packageName, idType: "Long", hasCustomQueries: false, customQueries: [], hasSoftDelete: false, hasAuthorization: false, singleRecordPerUser: false, enableCaching: false, cacheNames: []}` |
| `webflux_service_layer.json` | `services[]` | `{entityName, className, packageName, repositoryName, isRootEntity: false, hasAuthorization: false, singleRecordPerUser: false, authorizationConfig: {...}, transactionManagement: {...}, customMethods: [], validationRules: {...}}` |
| `webflux_controller_layer.json` | `controllers[]` | `{entityName, className, packageName, serviceName, basePath, isRootEntity: false, singleRecordPerUser: false, endpoints: {create, getById, getAll, update, delete}, customEndpoints: [], corsConfig: {...}}` |
| `webflux_dto_layer.json` | `dtos[]` | 3 entries: Input DTO (user fields), Output DTO (id + user + audit), Filter DTO (user fields) |

### remove-entity

```
py app_def_manager/cli.py remove-entity --app <app> --name <EntityName>
```

Removes the entity from all 6 layer files by filtering on `className`/`entityName`/`name`.

---

## 4. Field Operations

### add-field

```
py app_def_manager/cli.py add-field --app <app> --entity <EntityName> --field '{"name":"age","type":"Integer"}'
```

**Touches 3 files** (`webflux_entity_layer.json`, `webflux_entities.json`, `webflux_dto_layer.json`):

| File | What Happens |
|------|-------------|
| `webflux_entity_layer.json` | Inserts field before audit fields: `{columnName, fieldName, javaType, isPrimaryKey: false, isNullable: true, columnDefinition}` |
| `webflux_entities.json` | Inserts column before audit columns: `{name, type, primaryKey: false, nullable: true, foreignKey: null, unique: false, defaultValue: null}` |
| `webflux_dto_layer.json` | Adds `{fieldName, javaType, includeInDTO: true}` to Input, Output (before audit), and Filter DTOs |

**Optional field properties:**
- `fieldWidget` — valid values: `text`, `richText`, `codeEditor`, `markdown`, `json`
- `language` — only when `fieldWidget: "codeEditor"` (e.g. `"java"`, `"python"`)

### remove-field

```
py app_def_manager/cli.py remove-field --app <app> --entity <EntityName> --field <field_name>
```

Removes from same 3 files by matching `columnName` (entity_layer, entities) and `fieldName` (dto_layer).

### modify-field

```
py app_def_manager/cli.py modify-field --app <app> --entity <EntityName> --field <field_name> --updates '{"type":"Integer","isNullable":false}'
```

**Supported update keys:**
- `type` → updates `javaType` + `columnDefinition` in entity_layer, `type` in entities, `javaType` in dto_layer
- `isNullable` → updates `isNullable` in entity_layer, `nullable` in entities
- `fieldWidget` → updates `fieldWidget` in dto_layer (valid: text, richText, codeEditor, markdown, json)
- `language` → updates `language` in dto_layer (only with codeEditor widget)

---

## 5. Endpoint Operations

### add-endpoint

```
py app_def_manager/cli.py add-endpoint --app <app> --entity <EntityName> --endpoint '<json>'
```

**Touches 1 file**: `webflux_controller_layer.json`
- Appends to `controllers[].customEndpoints[]`

### remove-endpoint

```
py app_def_manager/cli.py remove-endpoint --app <app> --entity <EntityName> --endpoint <endpoint_name>
```

Removes from `customEndpoints[]` by matching `name`.

---

## 6. Query Operations

### add-query

```
py app_def_manager/cli.py add-query --app <app> --entity <EntityName> --query '<json>'
```

**Touches 1 file**: `webflux_repository_layer.json`
- Appends to `repositories[].customQueries[]`
- Sets `hasCustomQueries: true`

### remove-query

```
py app_def_manager/cli.py remove-query --app <app> --entity <EntityName> --query <query_name>
```

Removes from `customQueries[]` by matching `name`. Sets `hasCustomQueries: false` if array is empty.

---

## 7. Relationship Operations

### add-relationship

```
py app_def_manager/cli.py add-relationship --app <app> --relationship '{"sourceEntity":"Order","targetEntity":"Product","type":"MANY_TO_ONE"}'
```

**Touches 1 file**: `webflux_relationships.json`
- Appends to `relationships[]`

### remove-relationship

```
py app_def_manager/cli.py remove-relationship --app <app> --source <SourceEntity> --target <TargetEntity>
```

Removes by matching `sourceEntity` + `targetEntity`.

---

## 8. Document Storage Operations

All touch `webflux_document_storage_layer.json` only.

### add-json-column

```
py app_def_manager/cli.py add-json-column --app <app> --entity <EntityName> --column <db_col> --field <java_field>
```

Appends `{entityName, columnName, fieldName}` to `jsonColumns[]`.

### remove-json-column

```
py app_def_manager/cli.py remove-json-column --app <app> --entity <EntityName> --field <java_field>
```

### add-document-collection

```
py app_def_manager/cli.py add-document-collection --app <app> --name <CollectionName> --table <table_name> [--description <desc>]
```

Appends `{name, tableName, description}` to `documentCollections[]`.

### remove-document-collection

```
py app_def_manager/cli.py remove-document-collection --app <app> --name <CollectionName>
```

---

## 9. bulk-update Command

```
py app_def_manager/cli.py bulk-update --app <app> --entities <names|ALL> --set <key=value> [--set ...]
```

**Updates 3 layer files** (service, repository, controller):

| Key | Type | Layers Updated | Effect |
|-----|------|----------------|--------|
| `hasAuthorization` | bool | service, repository, controller | Enables ownership-based record access control |
| `singleRecordPerUser` | bool | service, repository, controller | Restricts to one record per authenticated user |
| `enableCaching` | bool | service, repository, controller | Enables response caching |
| `isRootEntity` | bool | service, repository, controller | Marks as root entity in hierarchy |
| Any other entity-level key | any | service, repository, controller | Set directly on entity entry |
| `requiresAuth` | bool | controller (endpoint-level) | Sets `requiresAuth` on all 5 CRUD endpoints |
| `roles` | string | controller (endpoint-level) | Sets `roles: ["<value>"]` on all 5 CRUD endpoints |

---

## 10. Status Tracking

```
py app_def_manager/cli.py status --app <app>
py app_def_manager/cli.py mark-clean --app <app> [--file <filename>]
py app_def_manager/cli.py mark-dirty --app <app> [--file <filename>]
```

Manages `_generation_status.json` — tracks which definition files have changed since last code generation.
Phase 3 (`phase3_definition_first.py`) uses this for incremental generation: only dirty files trigger regeneration.

---

## 11. AI Layer Operations

All AI commands modify `webflux_ai_layer.json` and/or `react_ai_config.json`.

### Provider Management

| Command | Properties Created in `webflux_ai_layer.json` |
|---------|-----------------------------------------------|
| `ai-add-provider --name X --type openai --model gpt-4 --api-key-env-var KEY` | `providers[]: {name, type, model, apiKeyEnvVar, supportedRoles?, roleFallbacks?, chatOptions?, supportedParameters?, parameterFallbacks?, resilience?}` |
| `ai-remove-provider --name X` | Removes from `providers[]` |

### Entity Capabilities

| Command | Properties |
|---------|-----------|
| `ai-add-capability --entity X --provider Y --operations "summarize,generate"` | `entityCapabilities[]: {entityName, providerName, operations[], ragSources?, evaluators?, rolePromptSequence?, chatOptions?, responseType?}` |
| `ai-remove-capability --entity X` | Removes from `entityCapabilities[]` |

### Prompt Templates

| Command | Properties |
|---------|-----------|
| `ai-add-prompt-template --name X --operation Y --template "..."` | `promptTemplates[]: {name, operation, template}` |
| `ai-remove-prompt-template --name X` | Removes from `promptTemplates[]` |

### Assistants

| Command | Properties |
|---------|-----------|
| `ai-add-assistant --name X --system-prompt "..." --provider Y --entity-scope "E1,E2"` | `assistants[]: {name, systemPrompt, providerName, entityScope[], rolePromptSequence?, chatOptions?, responseType?}` |
| `ai-remove-assistant --name X` | Removes from `assistants[]` |

### Standalone Operations

| Command | Properties |
|---------|-----------|
| `ai-add-standalone --name X --type chat --provider Y --base-path /api/ai/X --system-prompt "..." --actions "send,clear"` | `standaloneOperations[]: {name, type, providerName, basePath, systemPrompt, enabledActions[], ragSources?, evaluators?, rolePromptSequence?, chatOptions?, responseType?}` |
| `ai-remove-standalone --name X` | Removes from `standaloneOperations[]` |

### RAG Sources

| Command | Properties |
|---------|-----------|
| `ai-add-rag-source --name X --type semantic --provider Y --enabled` | `ragSources[]: {name, type, providerName?, enabled}` |
| `ai-remove-rag-source --name X` | Removes from `ragSources[]` |

### Evaluators

| Command | Properties |
|---------|-----------|
| `ai-add-evaluator --name X --type relevancy --provider Y --prompt "..." --scoring numeric` | `evaluators[]: {name, type, providerName, prompt, scoring}` |
| `ai-remove-evaluator --name X` | Removes from `evaluators[]` |

### Infrastructure Config (singleton objects)

| Command | Property Path | Properties |
|---------|--------------|-----------|
| `ai-set-orchestrator --provider X` | `orchestrator` | `{providerName, ...kwargs}` |
| `ai-set-vector-store --type milvus` | `vectorStore` | `{type, ...kwargs}` |
| `ai-set-observability` | `observability` | `{enabled: true, dashboards?, ...kwargs}` |
| `ai-set-rate-limiting --default-rpm 20` | `rateLimiting` | `{defaultRpm, ...kwargs}` |
| `ai-set-token-budget --daily-limit N --monthly-limit M` | `tokenBudget` | `{enabled, dailyLimit?, monthlyLimit?, providerOverrides?, ...kwargs}` |
| `ai-set-session-cleanup --ttl-days 30` | `chatSessionCleanup` | `{enabled, ttlDays, ...kwargs}` |
| `ai-set-audit-log --retention-days 90` | `auditLog` | `{enabled, retentionDays, ...kwargs}` |
| `ai-set-document-ingestion` | `documentIngestion` | `{enabled, sources?, ...kwargs}` |
| `ai-set-document-processing` | `documentProcessing` | `{enabled, tasks?, ...kwargs}` |
| `ai-set-moderation --provider X --categories "hate,violence"` | `moderation` (under promptSecurity) | `{enabled, providerName, categories[]}` |
| `ai-add-mcp-server --name X --transport stdio --roles "ADMIN"` | `mcpServers[]` | `{name, transportType, requiredRoles[], enabled: true}` |

### React AI Config (`react_ai_config.json`)

| Property | Purpose |
|----------|---------|
| `chatPanel.enabled` | Show/hide AI chat panel |
| `chatPanel.position` | `"sidebar"` or `"bottom"` |
| `chatPanel.defaultAssistant` | Default assistant name |
| `chatPanel.showOnPages[]` | Routes where chat appears |
| `chatPanel.streamingEnabled` | Enable streaming responses |
| `entityFeatures[]` | Per-entity AI buttons/features |
| `standaloneFeatures[]` | Standalone AI pages |
| `theme` | AI UI styling (accentColor, chatBubbleStyle, loadingAnimation) |
| `evaluationDisplay` | How to show evaluation results |
| `ragFeatures` | RAG-specific UI config |

---

## 12. Property-Level Mapping: WebFlux Definitions → swfaw Generated Java

### webflux_entity_layer.json → Entity Classes

| Definition Property | Generated Java Code | Template |
|--------------------|--------------------|---------| 
| `tableName` | `@Table(name = "tableName")` | `entity_templates.py` |
| `className` | `public class ClassName { ... }` | `entity_templates.py` |
| `packageName` | `package com.example.entity;` | `entity_templates.py` |
| `fields[].columnName` | `@Column("column_name")` | `entity_templates.py` |
| `fields[].fieldName` | `private Type fieldName;` | `entity_templates.py` |
| `fields[].javaType` | Java type declaration | `entity_templates.py` |
| `fields[].isPrimaryKey` | `@Id` annotation | `entity_templates.py` |
| `hasAuditFields` | `createdAt`, `updatedAt` fields with `@Column` | `entity_templates.py` |
| `hasSoftDelete` | `deletedAt` field with `@Column("deleted_at")` | `entity_templates.py` |
| `isRootEntity` | Javadoc comment "Root entity with authorization support" | `entity_templates.py` |
| `parentEntity` | Javadoc comment "Sub-entity of X" | `entity_templates.py` |

### webflux_repository_layer.json → Repository Interfaces

| Definition Property | Generated Java Code | Template |
|--------------------|--------------------|---------| 
| `className` | `public interface ClassName extends R2dbcRepository<Entity, IdType>` | `repository_templates.py` |
| `packageName` | `package com.example.repository;` | `repository_templates.py` |
| `entityName` | Generic type parameter in `R2dbcRepository<EntityName, ...>` | `repository_templates.py` |
| `idType` | Generic type parameter `R2dbcRepository<..., Long>` | `repository_templates.py` |
| `hasSoftDelete` | `findByIdAndDeletedAtIsNull()`, `findAllByDeletedAtIsNull()` methods | `repository_templates.py` |
| `hasAuthorization` | `findAllPagedAuthorized()`, `countAuthorized()`, `findAllPagedOwnedOrShared()`, `countOwnedOrShared()` methods | `repository_templates.py` |
| `singleRecordPerUser` | `findByOwnerUserId()` method | `repository_templates.py` |
| `customQueries[]` | Custom `@Query` annotated methods | `custom_query_templates.py` |
| `enableCaching` | `@Cacheable` annotations on read methods | `repository_templates.py` |

### webflux_service_layer.json → Service Classes

| Definition Property | Generated Java Code | Template |
|--------------------|--------------------|---------| 
| `className` | `public class ClassName { ... }` | `service_templates.py` |
| `packageName` | `package com.example.service;` | `service_templates.py` |
| `repositoryName` | `private final RepositoryName repository;` | `service_templates.py` |
| `hasAuthorization` | Injects `RecordOwnerRepository`, `QueryGroupRecordRepository`, `QueryGroupMemberRepository`, `AuthUserRepository`, `JwtService`; wraps CRUD in `SecurityContextHolder.getCurrentUser()` | `service_templates.py` |
| `singleRecordPerUser` | Create method checks `repository.findByOwnerUserId()` and rejects duplicates with `IllegalStateException` | `service_templates.py` |
| `authorizationConfig.checkOnCreate/Read/Update/Delete` | Conditional authorization checks per operation | `service_templates.py` |
| `authorizationConfig.allowPublicRead` | Skips auth check on read operations | `service_templates.py` |
| `authorizationConfig.requireOwnership` | Enforces record ownership validation | `service_templates.py` |
| `transactionManagement.enabled` | `@Transactional` annotation | `service_templates.py` |
| `transactionManagement.propagation` | `@Transactional(propagation = Propagation.REQUIRED)` | `service_templates.py` |
| `transactionManagement.isolation` | `@Transactional(isolation = Isolation.DEFAULT)` | `service_templates.py` |
| `transactionManagement.timeout` | `@Transactional(timeout = 30)` | `service_templates.py` |
| `customMethods[]` | Additional service methods | `service_templates.py` |
| `isRootEntity` | First entity flag (affects generation order) | `service_templates.py` |

### webflux_controller_layer.json → Controller Classes

| Definition Property | Generated Java Code | Template |
|--------------------|--------------------|---------| 
| `className` | `public class ClassName { ... }` | `controller_templates.py` |
| `packageName` | `package com.example.controller;` | `controller_templates.py` |
| `serviceName` | `private final ServiceName service;` | `controller_templates.py` |
| `basePath` | `@RequestMapping("/api/entities")` | `controller_templates.py` |
| `endpoints.create.enabled` | Generates `@PostMapping` create method | `controller_templates.py` |
| `endpoints.create.path` | `@PostMapping("path")` | `controller_templates.py` |
| `endpoints.create.method` | HTTP method annotation | `controller_templates.py` |
| `endpoints.create.requiresAuth` | `@TableAccess(operation = "CREATE")` + Swagger 401/403 responses | `controller_templates.py` |
| `endpoints.create.roles[]` | Role-based access annotations | `controller_templates.py` |
| `endpoints.create.rateLimitPerMinute` | Rate limiting configuration | `controller_templates.py` |
| `endpoints.getById.enabled` | Generates `@GetMapping("/{id}")` findById method | `controller_templates.py` |
| `endpoints.getAll.enabled` | Generates paginated `@GetMapping` findAll method | `controller_templates.py` |
| `endpoints.getAll.defaultPageSize` | Default page size parameter | `controller_templates.py` |
| `endpoints.getAll.supportsPagination` | Pagination query params (page, size) | `controller_templates.py` |
| `endpoints.getAll.supportsFiltering` | Filter query params | `controller_templates.py` |
| `endpoints.getAll.supportsSorting` | Sort query params (sortBy, sortDir) | `controller_templates.py` |
| `endpoints.update.enabled` | Generates `@PutMapping("/{id}")` update method | `controller_templates.py` |
| `endpoints.delete.enabled` | Generates `@DeleteMapping("/{id}")` delete method | `controller_templates.py` |
| `customEndpoints[]` | Additional endpoint methods | `controller_templates.py` |
| `corsConfig.enabled` | `@CrossOrigin(...)` annotation on class | `controller_templates.py` |
| `corsConfig.allowedOrigins[]` | `origins = {"*"}` | `controller_templates.py` |
| `corsConfig.allowedMethods[]` | `methods = {RequestMethod.GET, ...}` | `controller_templates.py` |
| `corsConfig.allowedHeaders[]` | `allowedHeaders = {"*"}` | `controller_templates.py` |
| `corsConfig.maxAge` | `maxAge = value` | `controller_templates.py` |
| `singleRecordPerUser` | Affects endpoint behavior (single-record semantics) | `controller_templates.py` |

### webflux_dto_layer.json → DTO Classes

| Definition Property | Generated Java Code | Template |
|--------------------|--------------------|---------| 
| `dtoType: "Input"` | `public class EntityInputDTO { ... }` with validation annotations | `dto_templates.py` |
| `dtoType: "Output"` | `public class EntityOutputDTO { ... }` with all fields | `dto_templates.py` |
| `dtoType: "Filter"` | `public class EntityFilterDTO { ... }` with date range filters | `dto_templates.py` |
| `className` | Class name | `dto_templates.py` |
| `packageName` | Package declaration | `dto_templates.py` |
| `fields[].fieldName` | `private Type fieldName;` | `dto_templates.py` |
| `fields[].javaType` | Java type declaration | `dto_templates.py` |
| `fields[].includeInDTO` | Whether field is included (if false, skipped) | `dto_templates.py` |
| `fields[].fieldWidget` | Comment/metadata (used by REAW for component selection) | — |
| `fields[].validation.required` | `@NotNull(message = "...")` | `dto_templates.py` |
| `fields[].validation.email` | `@Email(message = "...")` | `dto_templates.py` |
| `fields[].validation.minLength` | `@Size(min = N, ...)` | `dto_templates.py` |
| `fields[].validation.maxLength` | `@Size(max = N, ...)` | `dto_templates.py` |
| `fields[].validation.pattern` | `@Pattern(regexp = "...", ...)` | `dto_templates.py` |
| `fields[].validation.min` | `@Min(value = N, ...)` | `dto_templates.py` |
| `fields[].validation.max` | `@Max(value = N, ...)` | `dto_templates.py` |
| `hasPublicFlag` (entity-level) | `private Boolean isPublic;` in Input DTO | `dto_templates.py` |
| `excludeSensitiveFields[]` | Fields excluded from Output DTO | `dto_templates.py` |

### webflux_project_metadata.json → Build/Config Files

| Definition Property | Generated Output | Template |
|--------------------|-----------------|---------|
| `projectMetadata.name` | `pom.xml` artifact name, `application.yml` app name | `pom_templates.py`, `config_templates.py` |
| `projectMetadata.groupId` | `pom.xml` groupId, base package for all Java files | `pom_templates.py` |
| `projectMetadata.artifactId` | `pom.xml` artifactId | `pom_templates.py` |
| `projectMetadata.version` | `pom.xml` version | `pom_templates.py` |
| `projectMetadata.port` | `application.yml` server.port | `config_templates.py` |
| `projectMetadata.database.type` | R2DBC driver selection | `config_templates.py` |
| `projectMetadata.database.host` | `application.yml` r2dbc.url host | `config_templates.py` |
| `projectMetadata.database.port` | `application.yml` r2dbc.url port | `config_templates.py` |
| `projectMetadata.database.name` | `application.yml` r2dbc.url database name | `config_templates.py` |
| `projectMetadata.database.username` | `application.yml` r2dbc.username | `config_templates.py` |
| `projectMetadata.database.password` | `application.yml` r2dbc.password | `config_templates.py` |
| `projectMetadata.sqlFileName` | Output SQL file name in `schema.sql` | DDL generator |

### webflux_entities.json → SQL DDL (schema.sql)

| Definition Property | Generated SQL |
|--------------------|--------------|
| `entities[].name` | `CREATE TABLE table_name (...)` |
| `entities[].columns[].name` | Column name in DDL |
| `entities[].columns[].type` | Column type (VARCHAR(255), BIGINT UNSIGNED, etc.) |
| `entities[].columns[].primaryKey` | `PRIMARY KEY (col)` + `AUTO_INCREMENT` |
| `entities[].columns[].nullable` | `NOT NULL` constraint |
| `entities[].columns[].foreignKey` | `FOREIGN KEY (col) REFERENCES table(col)` |
| `entities[].columns[].unique` | `UNIQUE` constraint |
| `entities[].columns[].defaultValue` | `DEFAULT value` |

### webflux_document_storage_layer.json → Document Storage Code

| Definition Property | Generated Java Code | Template |
|--------------------|--------------------|---------| 
| `fileStorage.enabled` | File upload/download controller + service | `file_storage_templates.py` |
| `jsonColumns[].entityName` | JSON serialization in entity | `json_column_templates.py` |
| `jsonColumns[].columnName` | `@Column("col")` with JSON converter | `json_column_templates.py` |
| `jsonColumns[].fieldName` | Java field with `@JsonProperty` | `json_column_templates.py` |
| `documentCollections[].name` | Document collection entity + repository | `document_collection_templates.py` |
| `documentCollections[].tableName` | `@Table("table")` on collection entity | `document_collection_templates.py` |

---

## 13. Property-Level Mapping: React Definitions → REAW Generated React

### react_routes.json → App.jsx Routes + Navigation

| Definition Property | Generated React Code | Generator |
|--------------------|---------------------|-----------|
| `[].path` | `<Route path="/path" element={<Component />} />` in App.jsx | `scaffold_generator.py` |
| `[].pageComponent` | Component import + route element | `scaffold_generator.py` |
| `[].pageType` | Determines page generator: `entity`, `filter`, `query` | `entity_page_generator.py` / `filter_page_generator.py` / `query_page_generator.py` |
| `[].pageFolder` | Output directory: `src/pages/{pageFolder}/` | All page generators |
| `[].entityName` | Links route to entity's Redux slice + API service | `scaffold_generator.py` |
| `[].navLabel` | Sidebar navigation link text | `grid_layout_generator.py` |
| `[].navGroup` | Sidebar navigation group heading | `grid_layout_generator.py` |
| `[].requiresAuth` | Wraps route in `<ProtectedRoute>` | `scaffold_generator.py` |

### react_page_definitions.json → Page Components

| Definition Property | Generated React Code | Generator |
|--------------------|---------------------|-----------|
| `[].pageId` | Component name: `function PageId() { ... }` | `entity_page_generator.py` |
| `[].pageType` | Selects generator (entity/filter/query) | — |
| `[].entityName` | Connects to entity's form/table components | `entity_page_generator.py` |
| `[].gridTemplate.gridTemplateRows` | CSS Grid: `gridTemplateRows: "1fr"` | `entity_page_generator.py` |
| `[].gridTemplate.gridTemplateColumns` | CSS Grid: `gridTemplateColumns: "1fr"` | `entity_page_generator.py` |
| `[].gridTemplate.gridTemplateAreas[]` | CSS Grid: `gridTemplateAreas: '"content"'` | `entity_page_generator.py` |
| `[].componentPlacements[].componentType` | Which component to render: `"groupedForm"` → GroupedForm, `"form"` → EntityForm, `"dataTable"` → DataTable | `entity_page_generator.py` |
| `[].componentPlacements[].entityName` | Entity-specific component import | `entity_page_generator.py` |
| `[].componentPlacements[].gridArea` | `style={{ gridArea: "content" }}` | `entity_page_generator.py` |
| `[].componentPlacements[].formLayout.columnsLg` | Responsive form columns (large screens) | `entity_page_generator.py` |
| `[].componentPlacements[].formLayout.columnsMd` | Responsive form columns (medium screens) | `entity_page_generator.py` |
| `[].componentPlacements[].formLayout.columnsSm` | Responsive form columns (small screens) | `entity_page_generator.py` |

### react_component_mappings.json → Entity Forms + DataTables

| Definition Property | Generated React Code | Generator |
|--------------------|---------------------|-----------|
| `[].entityName` | Component directory: `src/components/entities/{entityName}/` | `entity_component_generator.py` |
| `[].fields[].fieldName` | Form field `name` prop, DataTable column accessor | `entity_component_generator.py` |
| `[].fields[].fieldLabel` | `<label>` text, DataTable column header | `entity_component_generator.py` |
| `[].fields[].componentType` | React component rendered (see table below) | `entity_component_generator.py` |
| `[].fields[].javaType` | Determines input validation/formatting | `entity_component_generator.py` |
| `[].fields[].columnDefinition` | Informs max length / input constraints | `entity_component_generator.py` |
| `[].fields[].props` | Spread as component props (e.g. `mode: "datetime"` for Calendar) | `entity_component_generator.py` |
| `[].fields[].includeInDTO` | Whether field appears in form/table | `entity_component_generator.py` |
| `[].excludeSensitiveFields[]` | Fields hidden from DataTable display | `entity_component_generator.py` |
| `[].singleRecordPerUser` | Hides DataTable, shows form-only view | `entity_component_generator.py` |

#### componentType → React Component Mapping

| componentType | React Component | Import |
|--------------|----------------|--------|
| `InputText` | `<InputText />` | PrimeReact |
| `InputNumber` | `<InputNumber />` | PrimeReact |
| `InputTextarea` | `<InputTextarea />` | PrimeReact |
| `Checkbox` | `<Checkbox />` | PrimeReact |
| `Calendar` | `<Calendar />` | PrimeReact |
| `Dropdown` | `<Dropdown />` | PrimeReact |
| `QuillEditor` | `<QuillEditor />` | Custom wrapper (rich text) |
| `MonacoEditor` | `<MonacoEditor />` | Custom wrapper (code editor) |
| `MarkdownEditor` | `<MarkdownEditor />` | Custom wrapper (markdown) |
| `FileUpload` | `<FileUpload />` | PrimeReact |

### react_form_groupings.json → Grouped/Tabbed Forms

| Definition Property | Generated React Code | Generator |
|--------------------|---------------------|-----------|
| `[].groupName` | Component name: `{GroupName}Form.jsx` | `grouped_form_generator.py` |
| `[].parentEntity` | Primary entity whose page hosts the grouped form | `grouped_form_generator.py` |
| `[].tabs[].entityName` | Tab content renders that entity's form | `grouped_form_generator.py` |
| `[].tabs[].tabLabel` | Tab header text | `grouped_form_generator.py` |
| `[].tabs[].tabOrder` | Tab display order | `grouped_form_generator.py` |

### react_layout.json → App Shell (Grid Layout)

| Definition Property | Generated React Code | Generator |
|--------------------|---------------------|-----------|
| `applicationName` | App title in header, `<title>` tag | `grid_layout_generator.py` |
| `apiPort` | Used in API base URL construction | `grid_layout_generator.py` |
| `header.visible` | Renders `<Header />` component | `grid_layout_generator.py` |
| `header.collapsible` | Adds collapse toggle button | `grid_layout_generator.py` |
| `footer.visible` | Renders `<Footer />` component | `grid_layout_generator.py` |
| `leftNav.visible` | Renders `<Sidebar />` component | `grid_layout_generator.py` |
| `leftNav.collapsible` | Adds sidebar collapse toggle | `grid_layout_generator.py` |
| `leftNav.defaultCollapsed` | Initial collapsed state | `grid_layout_generator.py` |
| `navGroups[].groupName` | Sidebar section heading | `grid_layout_generator.py` |
| `navGroups[].entities[].label` | Navigation link text | `grid_layout_generator.py` |
| `navGroups[].entities[].path` | Navigation link `href` / `to` | `grid_layout_generator.py` |

### react_auth_config.json → Auth Components

| Definition Property | Generated React Code | Generator |
|--------------------|---------------------|-----------|
| `jwtEnabled` | JWT token handling in API interceptor | `auth_generator.py` |
| `oauth2Enabled` | OAuth2 login buttons | `auth_generator.py` |
| `oauth2Providers[]` | Provider-specific login buttons (Google, GitHub, etc.) | `auth_generator.py` |
| `refreshTokenEnabled` | Token refresh logic in API interceptor | `auth_generator.py` |
| `protectedRoutes[]` | Routes wrapped in `<ProtectedRoute>` | `auth_generator.py` |
| `permissionsEndpoint` | API call to fetch user permissions | `permission_generator.py` |
| `loginEndpoint` | Login form submission URL | `auth_generator.py` |
| `registerEndpoint` | Registration form submission URL | `auth_generator.py` |
| `registerEnabled` | Shows/hides registration form | `auth_generator.py` |

### react_api_services.json → API Service Files

| Definition Property | Generated React Code | Generator |
|--------------------|---------------------|-----------|
| `[].entityName` | Service file: `src/services/{entityName}Service.js` | `api_service_generator.py` |
| `[].basePath` | `axios.get(BASE_URL + "/api/entities")` | `api_service_generator.py` |
| `[].endpoints.create.enabled` | `export const createEntity = (data) => axios.post(...)` | `api_service_generator.py` |
| `[].endpoints.getById.enabled` | `export const getEntityById = (id) => axios.get(...)` | `api_service_generator.py` |
| `[].endpoints.getAll.enabled` | `export const getAllEntities = (params) => axios.get(...)` | `api_service_generator.py` |
| `[].endpoints.getAll.supportsPagination` | Adds `page` and `size` query params | `api_service_generator.py` |
| `[].endpoints.getAll.supportsFiltering` | Adds filter params to request | `api_service_generator.py` |
| `[].endpoints.getAll.supportsSorting` | Adds `sortBy` and `sortDir` params | `api_service_generator.py` |
| `[].endpoints.update.enabled` | `export const updateEntity = (id, data) => axios.put(...)` | `api_service_generator.py` |
| `[].endpoints.delete.enabled` | `export const deleteEntity = (id) => axios.delete(...)` | `api_service_generator.py` |

### react_redux_store.json → Redux Store + Slices

| Definition Property | Generated React Code | Generator |
|--------------------|---------------------|-----------|
| `[].entityName` | Slice file: `src/store/{entityName}Slice.js` | `redux_generator.py` |
| `[].pkField` | ID field used in `createEntityAdapter` | `redux_generator.py` |
| `[].thunks.fetchAll` | `createAsyncThunk("entity/fetchAll", ...)` | `redux_generator.py` |
| `[].thunks.fetchById` | `createAsyncThunk("entity/fetchById", ...)` | `redux_generator.py` |
| `[].thunks.create` | `createAsyncThunk("entity/create", ...)` | `redux_generator.py` |
| `[].thunks.update` | `createAsyncThunk("entity/update", ...)` | `redux_generator.py` |
| `[].thunks.delete` | `createAsyncThunk("entity/delete", ...)` | `redux_generator.py` |
| `[].stateShape.listState` | `items: [], loading: false, error: null` | `redux_generator.py` |
| `[].stateShape.singleItemState` | `currentItem: null, itemLoading: false` | `redux_generator.py` |
| `[].stateShape.mutationState` | `saving: false, deleting: false, mutationError: null` | `redux_generator.py` |
| `[].pagination.currentPage` | `pagination.currentPage` in initial state | `redux_generator.py` |
| `[].pagination.pageSize` | `pagination.pageSize` in initial state | `redux_generator.py` |
| `[].pagination.totalCount` | `pagination.totalCount` in initial state | `redux_generator.py` |

### react_theme.json → Theme/CSS Variables

| Definition Property | Generated React Code | Generator |
|--------------------|---------------------|-----------|
| `colorPalette.*` | CSS custom properties: `--color-background-primary: #f9fafb` | `theme_generator.py` |
| `typography.fontFamily` | `--font-family: 'Inter var', sans-serif` | `theme_generator.py` |
| `typography.fontSize` | `--font-size: 14px` | `theme_generator.py` |
| `typography.headingFontFamily` | `--heading-font-family: ...` | `theme_generator.py` |
| `typography.headingFontWeight` | `--heading-font-weight: 600` | `theme_generator.py` |
| `spacing.*` | `--spacing-small: 4px`, `--spacing-medium: 8px`, etc. | `theme_generator.py` |
| `borders.radius` | `--border-radius: 6px` | `theme_generator.py` |
| `borders.width` | `--border-width: 1px` | `theme_generator.py` |
| `shadows.*` | `--shadow-small: ...`, `--shadow-medium: ...` | `theme_generator.py` |
| `components.button.*` | Button-specific CSS overrides | `theme_generator.py` |
| `components.sidebar.*` | Sidebar background/text color | `theme_generator.py` |
| `animationsEnabled` | Enables/disables CSS transitions | `theme_generator.py` |
| `animationStyle.transitionDuration` | `--transition-duration: 200ms` | `theme_generator.py` |

### react_env.json → .env File

| Definition Property | Generated Output | Generator |
|--------------------|-----------------|-----------|
| `variables[].key` | `VITE_API_BASE_URL=http://localhost:8081` | `scaffold_generator.py` |
| `variables[].value` | Environment variable value | `scaffold_generator.py` |
| `variables[].comment` | Comment above the variable | `scaffold_generator.py` |

---

## 14. Java Type → SQL Type Mapping

Used by scaffolder and field operations to infer `columnDefinition` from `javaType`:

| Java Type | SQL Column Definition |
|-----------|---------------------|
| `Long` | `BIGINT UNSIGNED` |
| `Integer` | `INT` |
| `Short` | `SMALLINT` |
| `Byte` | `TINYINT` |
| `String` | `VARCHAR(255)` |
| `Boolean` | `BOOLEAN` |
| `LocalDate` | `DATE` |
| `LocalDateTime` | `TIMESTAMP` |
| `LocalTime` | `TIME` |
| `BigDecimal` | `DECIMAL(19,4)` |
| `Float` | `FLOAT` |
| `Double` | `DOUBLE` |
| `byte[]` | `BLOB` |
| `UUID` | `VARCHAR(36)` |

---

## 15. Generation Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                     App Def Manager (CLI)                            │
│  scaffold / add-entity / add-field / bulk-update / ai-add-* / ...   │
└──────────────────────────────────┬──────────────────────────────────┘
                                   │ writes
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              application_definitions/<app>/                          │
│                                                                     │
│  webflux_manifest.json          react_manifest.json                 │
│  webflux_project_metadata.json  react_routes.json                   │
│  webflux_entities.json          react_page_definitions.json         │
│  webflux_entity_layer.json      react_component_mappings.json       │
│  webflux_repository_layer.json  react_form_groupings.json           │
│  webflux_service_layer.json     react_layout.json                   │
│  webflux_controller_layer.json  react_auth_config.json              │
│  webflux_dto_layer.json         react_api_services.json             │
│  webflux_relationships.json     react_redux_store.json              │
│  webflux_document_storage.json  react_theme.json                    │
│  webflux_ai_layer.json          react_env.json                      │
│  _generation_status.json        react_ai_config.json                │
└───────────┬─────────────────────────────────────┬───────────────────┘
            │                                     │
            │ swfaw reads                         │ REAW reads
            ▼                                     ▼
┌───────────────────────────┐     ┌───────────────────────────────────┐
│  swfaw (Phase 2/3)        │     │  REAW                             │
│                           │     │                                   │
│  Templates:               │     │  Phase 1: Generates react_*.json  │
│  • entity_templates.py    │     │    from webflux definitions       │
│  • repository_templates   │     │                                   │
│  • service_templates.py   │     │  Phase 2: Generates React code    │
│  • controller_templates   │     │    from react_*.json definitions  │
│  • dto_templates.py       │     │                                   │
│  • config_templates.py    │     │  Generators:                      │
│  • pom_templates.py       │     │  • scaffold_generator.py          │
│  • security_templates.py  │     │  • entity_component_generator.py  │
│  • auth_*_templates.py    │     │  • entity_page_generator.py       │
│  • sql_builder.py (DDL)   │     │  • grouped_form_generator.py      │
│  • ai/ templates          │     │  • redux_generator.py             │
│                           │     │  • api_service_generator.py       │
└───────────┬───────────────┘     │  • auth_generator.py              │
            │                     │  • theme_generator.py             │
            │ generates           │  • grid_layout_generator.py       │
            ▼                     │  • filter/query generators        │
┌───────────────────────────┐     │  • ai_react_generator.py         │
│ generated_application/    │     └───────────────┬───────────────────┘
│   <app>/webflux_app/      │                     │ generates
│                           │                     ▼
│  src/main/java/           │     ┌───────────────────────────────────┐
│    com.example/           │     │ generated_application/            │
│      entity/              │     │   <app>/react_app/                │
│        Entity.java        │     │                                   │
│      repository/          │     │  src/                             │
│        EntityRepo.java    │     │    components/entities/            │
│      service/             │     │      {entity}/Form.jsx            │
│        EntityService.java │     │      {entity}/DataTable.jsx       │
│      controller/          │     │    pages/{folder}/Page.jsx        │
│        EntityCtrl.java    │     │    services/{entity}Service.js    │
│      dto/                 │     │    store/{entity}Slice.js         │
│        InputDTO.java      │     │    store/store.js                 │
│        OutputDTO.java     │     │    App.jsx (routes)               │
│        FilterDTO.java     │     │    main.jsx                       │
│      config/              │     │  package.json                     │
│      security/            │     │  vite.config.js                   │
│      exception/           │     │  .env                             │
│  schema.sql               │     │  index.html                       │
│  pom.xml                  │     └───────────────────────────────────┘
│  application.yml          │
└───────────────────────────┘
```

---

## Summary: Command → Files Touched

| Command | Files Modified (marked dirty) |
|---------|------------------------------|
| `scaffold` | All 12 definition files (creates new) |
| `add-entity` | entity_layer, entities, repository_layer, service_layer, controller_layer, dto_layer |
| `remove-entity` | entity_layer, entities, repository_layer, service_layer, controller_layer, dto_layer |
| `add-field` | entity_layer, entities, dto_layer |
| `remove-field` | entity_layer, entities, dto_layer |
| `modify-field` | entity_layer, entities, dto_layer |
| `add-endpoint` | controller_layer |
| `remove-endpoint` | controller_layer |
| `add-query` | repository_layer |
| `remove-query` | repository_layer |
| `add-relationship` | relationships |
| `remove-relationship` | relationships |
| `add-json-column` | document_storage_layer |
| `remove-json-column` | document_storage_layer |
| `add-document-collection` | document_storage_layer |
| `remove-document-collection` | document_storage_layer |
| `bulk-update` | service_layer, repository_layer, controller_layer |
| `ai-*` commands | webflux_ai_layer.json and/or react_ai_config.json |
