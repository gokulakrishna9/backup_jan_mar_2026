# App Definition Manager — Complete Reference

---

## 1. Overview

The App Definition Manager (`app_def_manager/`) is the workspace tool for scaffolding, editing, and tracking application definition JSON files. It is the primary interface for creating and modifying the `application_definitions/<app_name>/` directory, which serves as the single source of truth for code generation.

### Role in the Pipeline

The App Definition Manager sits at the front of the **Phase 3 definition-first pipeline**:

```
App Def Manager → application_definitions/<app>/*.json → Phase 3 Pipeline → Generated Code
```

1. **Scaffolder** creates all 12 definition files from entity descriptions
2. **CRUDManager** performs granular add/remove/modify operations across layers with cross-layer consistency
3. **AiCRUDManager** manages AI layer and React AI config definitions
4. **StatusTracker** tracks dirty/clean state per file via `_generation_status.json`
5. **Phase 3 Pipeline** reads dirty files → DependencyMapper resolves affected outputs → IncrementalGenerator regenerates only those → marks clean

### Architecture

```
┌─────────────┐     ┌─────────────┐     ┌───────────────┐     ┌──────────────────┐
│  Scaffolder  │────▶│ CRUDManager │────▶│ StatusTracker  │────▶│ Phase 3 Pipeline │
│ (scaffolder  │     │  (crud.py)  │     │(status_tracker │     │ (DependencyMapper│
│   .py)       │     │ (ai_crud.py)│     │   .py)         │     │  + Generator)    │
└─────────────┘     └─────────────┘     └───────────────┘     └──────────────────┘
       │                    │                    │
       ▼                    ▼                    ▼
  Creates all 12      Mutates individual    Tracks dirty/clean
  definition files    layers with cross-    per file with SHA-256
  + status file       reference validation  hash-based edit detection
```

### Supporting Components

| Component | File | Purpose |
|-----------|------|---------|
| Scaffolder | `scaffolder.py` | Creates all 12 definition files from entity descriptions |
| CRUDManager | `crud.py` | Entity/field/endpoint/query/relationship/document CRUD across layers |
| AiCRUDManager | `ai_crud.py` | AI layer + React AI config CRUD with cross-reference validation |
| StatusTracker | `status_tracker.py` | Dirty/clean tracking per file via `_generation_status.json` |
| BulkUpdater | `bulk_updater.py` | Batch-update entity-level flags across service/repo/controller layers |
| Describer | `describer.py` | Rich formatted summaries of entities and AI layer config |
| CLI | `cli.py` | Argparse CLI routing to all components |

---

## 2. Definition File Schemas (All 12 Files)

Each application under `application_definitions/<app_name>/` contains these 12 definition files plus one tracking file.

---

### 2.1 webflux_manifest.json

**Purpose:** Index file that lists all definition files, their logical names, and aggregate statistics.

```json
{
  "version": "2.5",
  "format": "split",
  "description": "Application definition split into multiple files by layer",
  "files": {
    "project_metadata": "webflux_project_metadata.json",
    "entities": "webflux_entities.json",
    "relationships": "webflux_relationships.json",
    "entity_layer": "webflux_entity_layer.json",
    "repository_layer": "webflux_repository_layer.json",
    "service_layer": "webflux_service_layer.json",
    "controller_layer": "webflux_controller_layer.json",
    "dto_layer": "webflux_dto_layer.json",
    "document_storage_layer": "webflux_document_storage_layer.json",
    "ai_layer": "webflux_ai_layer.json"
  },
  "statistics": {
    "total_entities": 7,
    "total_relationships": 0,
    "total_columns": 66
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Manifest schema version. Current: `"2.5"` |
| `format` | string | Always `"split"` — definitions are split across multiple files |
| `description` | string | Human-readable description |
| `files` | object | Map of logical layer name → filename |
| `statistics.total_entities` | int | Count of entities at scaffold time |
| `statistics.total_relationships` | int | Count of relationships at scaffold time |
| `statistics.total_columns` | int | Total columns across all entities (user fields + 3 auto per entity) |

**Cross-references:** All filenames listed in `files` must exist in the app directory.

---

### 2.2 webflux_project_metadata.json

**Purpose:** Project-level configuration — app name, database connection, Java package, port.

```json
{
  "projectMetadata": {
    "name": "job-portal",
    "applicationName": "Job Portal",
    "groupId": "com.jobportal",
    "artifactId": "job-portal",
    "version": "1.0.0",
    "port": 8081,
    "sqlFileName": "job_portal.sql",
    "dateCreated": "2026-04-01",
    "database": {
      "type": "mysql",
      "host": "localhost",
      "port": 3306,
      "name": "job_portal",
      "url": null,
      "username": "root",
      "password": "password"
    }
  }
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | kebab-case of app_name | Maven project name |
| `applicationName` | string | Title-cased app_name | Human-readable application name |
| `groupId` | string | `"com.example"` | Java base package / Maven groupId |
| `artifactId` | string | same as `name` | Maven artifactId |
| `version` | string | `"1.0.0"` | Project version |
| `port` | int | `8081` | WebFlux server port |
| `sqlFileName` | string | `"{db_name}.sql"` | Generated SQL DDL filename |
| `dateCreated` | string | ISO date of scaffold | Creation date |
| `database.type` | string | `"mysql"` | Database type |
| `database.host` | string | `"localhost"` | Database host |
| `database.port` | int | `3306` | Database port |
| `database.name` | string | snake_case of app_name | Database name |
| `database.url` | string\|null | `null` | Full JDBC URL override (if set, overrides host/port/name) |
| `database.username` | string | `"root"` | Database username |
| `database.password` | string | `"password"` | Database password |

**Generated code behavior:** `groupId` determines the base Java package for all generated classes. `port` sets the `server.port` in `application.yml`. `database.*` generates the R2DBC connection configuration.

---

### 2.3 webflux_entity_layer.json

**Purpose:** Entity definitions — the core file that defines all database tables, their Java class mappings, and field-level properties. This is the most important definition file.

```json
{
  "layerType": "entity",
  "description": "Entity layer configuration - controls JPA entity generation with R2DBC support",
  "entities": [
    {
      "tableName": "job_posting",
      "className": "JobPosting",
      "packageName": "com.jobportal.entity",
      "fields": [
        {
          "columnName": "job_posting_id",
          "fieldName": "jobPostingId",
          "javaType": "Long",
          "isPrimaryKey": true,
          "isNullable": false,
          "columnDefinition": "BIGINT UNSIGNED"
        },
        {
          "columnName": "title",
          "fieldName": "title",
          "javaType": "String",
          "isPrimaryKey": false,
          "isNullable": true,
          "columnDefinition": "VARCHAR(255)"
        },
        {
          "columnName": "salary_min",
          "fieldName": "salarymin",
          "javaType": "BigDecimal",
          "isPrimaryKey": false,
          "isNullable": true,
          "columnDefinition": "DECIMAL(19,4)"
        },
        {
          "columnName": "is_active",
          "fieldName": "isactive",
          "javaType": "Boolean",
          "isPrimaryKey": false,
          "isNullable": true,
          "columnDefinition": "BOOLEAN"
        },
        {
          "columnName": "created_at",
          "fieldName": "createdAt",
          "javaType": "LocalDateTime",
          "isPrimaryKey": false,
          "isNullable": false,
          "columnDefinition": "TIMESTAMP"
        },
        {
          "columnName": "updated_at",
          "fieldName": "updatedAt",
          "javaType": "LocalDateTime",
          "isPrimaryKey": false,
          "isNullable": false,
          "columnDefinition": "TIMESTAMP"
        }
      ],
      "hasAuditFields": true,
      "hasSoftDelete": false,
      "isRootEntity": false,
      "hasPublicFlag": false,
      "parentEntity": null
    }
  ]
}
```

#### Entity-Level Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `tableName` | string | snake_case of className | SQL table name |
| `className` | string | required | PascalCase Java class name |
| `packageName` | string | `"{groupId}.entity"` | Java package for the entity class |
| `fields` | array | required | Array of field definitions (see below) |
| `hasAuditFields` | bool | `true` | Whether `created_at`/`updated_at` fields are present |
| `hasSoftDelete` | bool | `false` | Whether `is_deleted` field is present |
| `isRootEntity` | bool | `false` (first entity = `true`) | Marks the primary/root entity of the application |
| `hasPublicFlag` | bool | `false` | Whether entity has a public visibility flag |
| `parentEntity` | string\|null | `null` | Parent entity name for hierarchical relationships |

#### Field Properties (Complete Reference)

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `columnName` | string | yes | SQL column name (snake_case). Used in DDL generation and R2DBC `@Column` annotation |
| `fieldName` | string | yes | Java field name (camelCase). Used in entity class, DTOs, and service methods |
| `javaType` | string | yes | Java type. See type mapping table below |
| `isPrimaryKey` | bool | yes | If `true`, generates `@Id` annotation and auto-increment DDL |
| `isNullable` | bool | yes | If `false`, generates `NOT NULL` in DDL and validation annotations |
| `columnDefinition` | string | yes | Verbatim SQL type used by DDLGenerator (e.g. `"BIGINT UNSIGNED"`, `"VARCHAR(255)"`) |

**Cross-references:**
- `className` is referenced by: repository_layer (`entityName`), service_layer (`entityName`), controller_layer (`entityName`), dto_layer (`entityName`), relationships (`sourceEntity`/`targetEntity`)
- `tableName` is referenced by: entities.json (`name`), relationships (FK column generation)

---

### 2.4 webflux_entities.json

**Purpose:** Column-level view of entities — used by DatabaseDefinition reconstruction and SQL DDL generation. This is a parallel representation of entity_layer focused on SQL column metadata.

```json
{
  "entities": [
    {
      "name": "student_profile",
      "columns": [
        {
          "name": "student_profile_id",
          "type": "BIGINT UNSIGNED",
          "primaryKey": true,
          "nullable": false,
          "foreignKey": null,
          "unique": false,
          "defaultValue": null
        },
        {
          "name": "resume_url",
          "type": "VARCHAR(255)",
          "primaryKey": false,
          "nullable": true,
          "foreignKey": null,
          "unique": false,
          "defaultValue": null
        },
        {
          "name": "created_at",
          "type": "TIMESTAMP",
          "primaryKey": false,
          "nullable": false,
          "foreignKey": null,
          "unique": false,
          "defaultValue": null
        }
      ]
    }
  ]
}
```

#### Entity Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | SQL table name (snake_case) — must match `tableName` in entity_layer |

#### Column Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | SQL column name (snake_case) |
| `type` | string | SQL data type (e.g. `"BIGINT UNSIGNED"`, `"VARCHAR(255)"`, `"TIMESTAMP"`) |
| `primaryKey` | bool | Whether this column is the primary key |
| `nullable` | bool | Whether the column allows NULL |
| `foreignKey` | string\|null | Foreign key reference (e.g. `"user_profile.user_profile_id"`) or `null` |
| `unique` | bool | Whether the column has a UNIQUE constraint |
| `defaultValue` | any\|null | Default value for the column, or `null` |

**Cross-references:** `name` (entity) must match `tableName` in entity_layer. Column `name` values must match `columnName` values in entity_layer fields.

---

### 2.5 webflux_relationships.json

**Purpose:** Defines relationships (foreign keys) between entities.

```json
{
  "relationships": [
    {
      "sourceEntity": "JobApplication",
      "targetEntity": "JobPosting",
      "type": "ManyToOne",
      "sourceColumn": "job_posting_id",
      "targetColumn": "job_posting_id",
      "cascadeType": "ALL",
      "fetchType": "LAZY"
    }
  ]
}
```

#### Relationship Properties

| Property | Type | Valid Values | Description |
|----------|------|-------------|-------------|
| `sourceEntity` | string | — | PascalCase entity that holds the FK |
| `targetEntity` | string | — | PascalCase entity being referenced |
| `type` | string | `"ManyToOne"`, `"OneToMany"`, `"ManyToMany"` | Relationship cardinality |
| `sourceColumn` | string | — | FK column name in source table |
| `targetColumn` | string | — | PK column name in target table |
| `cascadeType` | string | `"ALL"`, `"PERSIST"`, `"MERGE"`, `"REMOVE"`, `"NONE"` | JPA cascade behavior |
| `fetchType` | string | `"LAZY"`, `"EAGER"` | JPA fetch strategy |

**Generated code behavior:**
- `ManyToOne`: Adds FK column to source entity, generates `findBy{Target}Id` in repository
- `OneToMany`: Generates collection field in target entity, join method in repository
- `ManyToMany`: Generates join table DDL, collection fields in both entities

**Cross-references:** `sourceEntity` and `targetEntity` must exist in entity_layer `className` values.

---

### 2.6 webflux_repository_layer.json

**Purpose:** Repository layer configuration — controls R2DBC repository generation per entity, including custom queries, caching, soft-delete, and authorization flags.

```json
{
  "layerType": "repository",
  "description": "Repository layer configuration - controls R2DBC repository generation",
  "repositories": [
    {
      "entityName": "StudentProfile",
      "className": "StudentProfileRepository",
      "packageName": "com.jobportal.repository",
      "idType": "Long",
      "hasCustomQueries": false,
      "customQueries": [],
      "hasSoftDelete": false,
      "hasAuthorization": true,
      "singleRecordPerUser": true,
      "enableCaching": false,
      "cacheNames": []
    }
  ]
}
```

#### Repository Properties (Complete)

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `entityName` | string | required | PascalCase entity class name — must match entity_layer |
| `className` | string | `"{entityName}Repository"` | Generated repository interface name |
| `packageName` | string | `"{groupId}.repository"` | Java package |
| `idType` | string | `"Long"` | Java type of the entity's primary key |
| `hasCustomQueries` | bool | `false` | Whether custom query methods exist (auto-set by CRUDManager) |
| `customQueries` | array | `[]` | Array of custom query definitions (see below) |
| `hasSoftDelete` | bool | `false` | If `true`, generates `findAllByIsDeletedFalse()` and overrides delete to set `is_deleted=true` |
| `hasAuthorization` | bool | `false` | If `true`, generates `findByUserId()` and `findByIdAndUserId()` methods |
| `singleRecordPerUser` | bool | `false` | If `true`, generates `findByUserId()` returning `Mono<Entity>` instead of `Flux<Entity>` |
| `enableCaching` | bool | `false` | If `true`, generates `@Cacheable`/`@CacheEvict` annotations on repository methods |
| `cacheNames` | array | `[]` | Cache region names (e.g. `["studentProfiles"]`) |

#### Custom Query Format

```json
{
  "name": "findByEmail",
  "query": "SELECT * FROM user_profile WHERE email = :email",
  "returnType": "Mono",
  "parameters": [
    {"name": "email", "type": "String"}
  ]
}
```

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Method name in the repository interface |
| `query` | string | Raw R2DBC SQL query with `:paramName` placeholders |
| `returnType` | string | `"Mono"` (single) or `"Flux"` (multiple) |
| `parameters` | array | Array of `{name, type}` parameter definitions |

---

### 2.7 webflux_service_layer.json

**Purpose:** Service layer configuration — controls business logic generation including authorization, transactions, validation rules, and custom methods.

```json
{
  "layerType": "service",
  "description": "Service layer configuration - controls business logic and authorization",
  "services": [
    {
      "entityName": "StudentProfile",
      "className": "StudentProfileService",
      "packageName": "com.jobportal.service",
      "repositoryName": "StudentProfileRepository",
      "isRootEntity": true,
      "hasAuthorization": true,
      "singleRecordPerUser": true,
      "authorizationConfig": {
        "checkOnCreate": false,
        "checkOnRead": false,
        "checkOnUpdate": false,
        "checkOnDelete": false,
        "allowPublicRead": false,
        "requireOwnership": false
      },
      "transactionManagement": {
        "enabled": true,
        "propagation": "REQUIRED",
        "isolation": "DEFAULT",
        "timeout": 30
      },
      "customMethods": [],
      "validationRules": {
        "onCreate": [],
        "onUpdate": [],
        "onDelete": []
      }
    }
  ]
}
```

#### Service Properties (Complete)

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `entityName` | string | required | PascalCase entity class name |
| `className` | string | `"{entityName}Service"` | Generated service class name |
| `packageName` | string | `"{groupId}.service"` | Java package |
| `repositoryName` | string | `"{entityName}Repository"` | Injected repository name |
| `isRootEntity` | bool | `false` | Marks the root entity (first entity = `true`) |
| `hasAuthorization` | bool | `false` | If `true`, service methods inject `userId` from security context and filter by ownership |
| `singleRecordPerUser` | bool | `false` | If `true`, create checks for existing record, getAll returns only user's record |
| `authorizationConfig` | object | all `false` | Fine-grained authorization control (see below) |
| `transactionManagement` | object | see below | Transaction configuration |
| `customMethods` | array | `[]` | Custom service method definitions |
| `validationRules` | object | empty arrays | Validation rules per operation |

#### authorizationConfig Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `checkOnCreate` | bool | `false` | Validate user permissions before creating |
| `checkOnRead` | bool | `false` | Filter reads by user ownership |
| `checkOnUpdate` | bool | `false` | Verify user owns the record before updating |
| `checkOnDelete` | bool | `false` | Verify user owns the record before deleting |
| `allowPublicRead` | bool | `false` | If `true`, getAll/getById skip ownership check |
| `requireOwnership` | bool | `false` | If `true`, all operations require the user to own the record |

#### transactionManagement Properties

| Property | Type | Default | Valid Values | Description |
|----------|------|---------|-------------|-------------|
| `enabled` | bool | `true` | — | Whether `@Transactional` is applied |
| `propagation` | string | `"REQUIRED"` | `"REQUIRED"`, `"REQUIRES_NEW"`, `"SUPPORTS"`, `"NOT_SUPPORTED"`, `"MANDATORY"`, `"NEVER"` | Transaction propagation behavior |
| `isolation` | string | `"DEFAULT"` | `"DEFAULT"`, `"READ_UNCOMMITTED"`, `"READ_COMMITTED"`, `"REPEATABLE_READ"`, `"SERIALIZABLE"` | Transaction isolation level |
| `timeout` | int | `30` | — | Transaction timeout in seconds |

#### validationRules Format

```json
{
  "onCreate": [
    {"field": "email", "rule": "notBlank", "message": "Email is required"},
    {"field": "email", "rule": "email", "message": "Invalid email format"}
  ],
  "onUpdate": [],
  "onDelete": []
}
```

**Generated code behavior:**
- `hasAuthorization=true` + `singleRecordPerUser=true`: Create method checks if user already has a record, returns existing or creates new. GetAll returns only the user's single record.
- `hasAuthorization=true` + `singleRecordPerUser=false`: CRUD methods filter by `userId` from JWT token.
- `requireOwnership=true`: All operations verify the authenticated user owns the target record.

---

### 2.8 webflux_controller_layer.json

**Purpose:** Controller layer configuration — controls REST endpoint generation including CRUD endpoints, custom endpoints, CORS, rate limiting, and authentication.

```json
{
  "layerType": "controller",
  "description": "Controller layer configuration - controls REST endpoint generation",
  "controllers": [
    {
      "entityName": "StudentProfile",
      "className": "StudentProfileController",
      "packageName": "com.jobportal.controller",
      "serviceName": "StudentProfileService",
      "basePath": "/api/student_profiles",
      "isRootEntity": true,
      "singleRecordPerUser": true,
      "endpoints": {
        "create": {
          "enabled": true,
          "path": "",
          "method": "POST",
          "requiresAuth": true,
          "roles": ["USER"],
          "rateLimitPerMinute": 10
        },
        "getById": {
          "enabled": true,
          "path": "/{id}",
          "method": "GET",
          "requiresAuth": true,
          "roles": ["USER"],
          "rateLimitPerMinute": 60
        },
        "getAll": {
          "enabled": true,
          "path": "",
          "method": "GET",
          "requiresAuth": true,
          "roles": ["USER"],
          "rateLimitPerMinute": 30,
          "defaultPageSize": 20,
          "supportsPagination": true,
          "supportsFiltering": true,
          "supportsSorting": true
        },
        "update": {
          "enabled": true,
          "path": "/{id}",
          "method": "PUT",
          "requiresAuth": true,
          "roles": ["USER"],
          "rateLimitPerMinute": 10
        },
        "delete": {
          "enabled": true,
          "path": "/{id}",
          "method": "DELETE",
          "requiresAuth": true,
          "roles": ["USER"],
          "rateLimitPerMinute": 5
        }
      },
      "customEndpoints": [],
      "corsConfig": {
        "enabled": true,
        "allowedOrigins": ["*"],
        "allowedMethods": ["GET", "POST", "PUT", "DELETE"],
        "allowedHeaders": ["*"],
        "maxAge": 3600
      }
    }
  ]
}
```

#### Controller-Level Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `entityName` | string | required | PascalCase entity class name |
| `className` | string | `"{entityName}Controller"` | Generated controller class name |
| `packageName` | string | `"{groupId}.controller"` | Java package |
| `serviceName` | string | `"{entityName}Service"` | Injected service name |
| `basePath` | string | `"/api/{table_name}s"` | REST base path for all endpoints |
| `isRootEntity` | bool | `false` | Marks the root entity |
| `singleRecordPerUser` | bool | `false` | Mirrors service layer flag |

#### Standard Endpoint Properties (create, getById, getAll, update, delete)

| Property | Type | Default | Applies To | Description |
|----------|------|---------|-----------|-------------|
| `enabled` | bool | `true` | all | Whether the endpoint is generated |
| `path` | string | varies | all | Path suffix appended to `basePath` |
| `method` | string | varies | all | HTTP method (`GET`, `POST`, `PUT`, `DELETE`) |
| `requiresAuth` | bool | `false` | all | If `true`, generates `@PreAuthorize` or JWT validation |
| `roles` | array | `[]` | all | Required roles (e.g. `["USER"]`, `["ADMIN"]`) |
| `rateLimitPerMinute` | int | varies | all | Rate limit per user per minute |
| `defaultPageSize` | int | `20` | getAll | Default page size for pagination |
| `supportsPagination` | bool | `true` | getAll | Generates `page`/`size` query parameters |
| `supportsFiltering` | bool | `true` | getAll | Generates filter DTO query parameters |
| `supportsSorting` | bool | `true` | getAll | Generates `sort`/`direction` query parameters |

#### Default Endpoint Paths and Methods

| Endpoint | Path | Method | Default Rate Limit |
|----------|------|--------|-------------------|
| `create` | `""` (basePath) | `POST` | 10/min |
| `getById` | `"/{id}"` | `GET` | 60/min |
| `getAll` | `""` (basePath) | `GET` | 30/min |
| `update` | `"/{id}"` | `PUT` | 10/min |
| `delete` | `"/{id}"` | `DELETE` | 5/min |

#### Custom Endpoint Format

```json
{
  "name": "search",
  "path": "/search",
  "method": "GET",
  "requiresAuth": true,
  "roles": ["USER"],
  "rateLimitPerMinute": 30,
  "description": "Full-text search endpoint"
}
```

#### CORS Configuration

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enabled` | bool | `true` | Whether CORS is enabled for this controller |
| `allowedOrigins` | array | `["*"]` | Allowed origin domains |
| `allowedMethods` | array | `["GET","POST","PUT","DELETE"]` | Allowed HTTP methods |
| `allowedHeaders` | array | `["*"]` | Allowed request headers |
| `maxAge` | int | `3600` | Preflight cache duration in seconds |

---

### 2.9 webflux_dto_layer.json

**Purpose:** DTO layer configuration — controls Data Transfer Object generation with field inclusion, validation, and widget support.

```json
{
  "layerType": "dto",
  "description": "DTO layer configuration - controls Data Transfer Object generation with validation",
  "dtos": [
    {
      "entityName": "JobPosting",
      "dtoType": "Input",
      "className": "JobPostingInputDTO",
      "packageName": "com.jobportal.dto",
      "fields": [
        {
          "fieldName": "title",
          "javaType": "String",
          "includeInDTO": true
        },
        {
          "fieldName": "description",
          "javaType": "String",
          "includeInDTO": true,
          "fieldWidget": "richText"
        }
      ]
    },
    {
      "entityName": "JobPosting",
      "dtoType": "Output",
      "className": "JobPostingOutputDTO",
      "packageName": "com.jobportal.dto",
      "fields": [
        {
          "fieldName": "jobPostingId",
          "javaType": "Long",
          "includeInDTO": true
        },
        {
          "fieldName": "title",
          "javaType": "String",
          "includeInDTO": true
        },
        {
          "fieldName": "createdAt",
          "javaType": "LocalDateTime",
          "includeInDTO": true
        },
        {
          "fieldName": "updatedAt",
          "javaType": "LocalDateTime",
          "includeInDTO": true
        }
      ]
    },
    {
      "entityName": "JobPosting",
      "dtoType": "Filter",
      "className": "JobPostingFilterDTO",
      "packageName": "com.jobportal.dto",
      "fields": [
        {
          "fieldName": "title",
          "javaType": "String",
          "includeInDTO": true
        }
      ]
    }
  ]
}
```

#### DTO-Level Properties

| Property | Type | Description |
|----------|------|-------------|
| `entityName` | string | PascalCase entity class name |
| `dtoType` | string | `"Input"`, `"Output"`, or `"Filter"` |
| `className` | string | `"{entityName}{dtoType}DTO"` |
| `packageName` | string | `"{groupId}.dto"` |
| `fields` | array | Array of DTO field definitions |

#### DTO Field Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `fieldName` | string | yes | camelCase field name |
| `javaType` | string | yes | Java type |
| `includeInDTO` | bool | yes | If `false`, field is excluded from the generated DTO class |
| `fieldWidget` | string | no | UI widget hint for React frontend (see below) |
| `language` | string | no | Programming language for `codeEditor` widget |

#### fieldWidget Valid Values

| Value | Description | Generated Behavior |
|-------|-------------|-------------------|
| `"text"` | Plain text input | Standard `<input type="text">` |
| `"richText"` | Rich text editor | WYSIWYG editor component (e.g. TipTap/Quill) |
| `"codeEditor"` | Code editor with syntax highlighting | Monaco/CodeMirror component. Requires `language` field |
| `"markdown"` | Markdown editor with preview | Split-pane markdown editor |
| `"json"` | JSON editor with validation | JSON editor with schema validation |

#### DTO Type Behavior

| DTO Type | Includes PK | Includes User Fields | Includes Audit Fields | Purpose |
|----------|-------------|---------------------|----------------------|---------|
| Input | No | Yes | No | Request body for create/update |
| Output | Yes | Yes | Yes | Response body for all reads |
| Filter | No | Yes | No | Query parameters for getAll filtering |

---

### 2.10 webflux_document_storage_layer.json

**Purpose:** Document storage configuration — file storage, JSON column mappings, document collections, and entity attachments.

```json
{
  "fileStorage": {
    "enabled": false
  },
  "jsonColumns": [],
  "documentCollections": [],
  "entityAttachments": []
}
```

#### Top-Level Properties

| Property | Type | Description |
|----------|------|-------------|
| `fileStorage` | object | File storage configuration |
| `jsonColumns` | array | JSON column mappings for entities |
| `documentCollections` | array | Named document collections |
| `entityAttachments` | array | File attachment configurations per entity |

#### fileStorage Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enabled` | bool | `false` | Whether file storage is enabled |

#### jsonColumns Entry

```json
{
  "entityName": "UserProfile",
  "columnName": "preferences_json",
  "fieldName": "preferencesJson"
}
```

| Property | Type | Description |
|----------|------|-------------|
| `entityName` | string | PascalCase entity name |
| `columnName` | string | SQL column name storing JSON |
| `fieldName` | string | Java field name |

#### documentCollections Entry

```json
{
  "name": "CourseDocuments",
  "tableName": "course_documents",
  "description": "Uploaded course materials"
}
```

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | PascalCase collection name |
| `tableName` | string | SQL table name |
| `description` | string | Human-readable description |

---

### 2.11 webflux_ai_layer.json

**Purpose:** AI layer configuration — the most complex definition file. Controls all AI/ML capabilities including providers, entity AI capabilities, standalone operations, assistants, RAG, evaluators, orchestration, MCP servers, observability, token budgets, audit logging, and session cleanup.

```json
{
  "schemaVersion": "1.0",
  "providers": [],
  "entityCapabilities": [],
  "standaloneOperations": [],
  "promptTemplates": [],
  "assistants": [],
  "ragSources": [],
  "evaluators": [],
  "vectorStore": null,
  "documentIngestion": null,
  "documentProcessing": null,
  "orchestrator": null,
  "mcpServers": [],
  "observability": null,
  "rateLimiting": null,
  "tokenBudget": null,
  "chatSessionCleanup": null,
  "auditLog": null
}
```

All 18+ sections are documented in detail in [Section 10: AI Layer Reference](#10-ai-layer-reference).

---

### 2.12 react_ai_config.json

**Purpose:** React frontend AI configuration — controls chat panel, entity AI features, standalone feature pages, theme, evaluation display, and RAG features.

```json
{
  "schemaVersion": "1.0",
  "chatPanel": {
    "enabled": false,
    "position": "sidebar",
    "defaultAssistant": "",
    "showOnPages": [],
    "streamingEnabled": true
  },
  "entityFeatures": [],
  "standaloneFeatures": [],
  "theme": {
    "accentColor": "#6366f1",
    "chatBubbleStyle": "rounded",
    "loadingAnimation": "dots"
  },
  "evaluationDisplay": null,
  "ragFeatures": null
}
```

All sections are documented in detail in [Section 11: React AI Config Reference](#11-react-ai-config-reference).

---

## 3. Entity Layer Field Reference

### Complete Field Property Reference

Every field in `webflux_entity_layer.json` → `entities[].fields[]` has these properties:

| Property | Type | Description | Generated Code Impact |
|----------|------|-------------|----------------------|
| `columnName` | string | snake_case SQL column name | DDL `CREATE TABLE` column name, R2DBC `@Column("...")` |
| `fieldName` | string | camelCase Java field name | Entity class field, getter/setter, DTO field |
| `javaType` | string | Java type name | Entity field type, DTO field type, import statements |
| `isPrimaryKey` | bool | Primary key flag | `@Id` annotation, `AUTO_INCREMENT` in DDL, excluded from Input DTO |
| `isNullable` | bool | Nullable flag | `NOT NULL` in DDL, `@NotNull` validation annotation |
| `columnDefinition` | string | Verbatim SQL type | Used directly in DDL generation (takes precedence over type mapping) |

### Auto-Generated Fields

When scaffolding or adding an entity, these fields are automatically added:

| Field | columnName | fieldName | javaType | isPrimaryKey | isNullable | columnDefinition | Notes |
|-------|-----------|-----------|----------|-------------|-----------|-----------------|-------|
| Primary Key | `{table_name}_id` | `{tableName}Id` | `Long` | `true` | `false` | `BIGINT UNSIGNED` | Auto-increment |
| Created At | `created_at` | `createdAt` | `LocalDateTime` | `false` | `false` | `TIMESTAMP` | Set on insert |
| Updated At | `updated_at` | `updatedAt` | `LocalDateTime` | `false` | `false` | `TIMESTAMP` | Set on insert + update |
| Soft Delete | `is_deleted` | `isDeleted` | `Boolean` | `false` | `false` | `BOOLEAN` | Only if `hasSoftDelete=true` |

### Java Type → SQL Type Mapping

When `columnDefinition` is empty or needs inference, the scaffolder uses this mapping (defined in `JAVA_TO_SQL_FALLBACK`):

| Java Type | SQL Type | Notes |
|-----------|----------|-------|
| `Long` | `BIGINT UNSIGNED` | Primary keys, large integers |
| `Integer` | `INT` | Standard integers |
| `Short` | `SMALLINT` | Small integers |
| `Byte` | `TINYINT` | Tiny integers |
| `String` | `VARCHAR(255)` | Default string type |
| `Boolean` | `BOOLEAN` | True/false flags |
| `LocalDate` | `DATE` | Date without time |
| `LocalDateTime` | `TIMESTAMP` | Date with time |
| `LocalTime` | `TIME` | Time without date |
| `BigDecimal` | `DECIMAL(19,4)` | Monetary/precise values |
| `Float` | `FLOAT` | Single-precision floating point |
| `Double` | `DOUBLE` | Double-precision floating point |
| `byte[]` | `BLOB` | Binary data |
| `UUID` | `VARCHAR(36)` | UUID strings |

Unknown types default to `VARCHAR(255)` with a warning.

### How Fields Map to Generated Code

For a field like:
```json
{
  "columnName": "salary_min",
  "fieldName": "salarymin",
  "javaType": "BigDecimal",
  "isPrimaryKey": false,
  "isNullable": true,
  "columnDefinition": "DECIMAL(19,4)"
}
```

| Layer | Generated Code |
|-------|---------------|
| **Entity class** | `private BigDecimal salarymin;` with `@Column("salary_min")` |
| **Repository** | Part of `SELECT *` queries, available in custom query parameters |
| **Service** | Mapped in create/update methods via DTO → Entity conversion |
| **Controller** | Exposed via Input/Output/Filter DTOs |
| **Input DTO** | `private BigDecimal salarymin;` (for create/update request body) |
| **Output DTO** | `private BigDecimal salarymin;` (in response body) |
| **Filter DTO** | `private BigDecimal salarymin;` (as query parameter for filtering) |
| **SQL DDL** | `salary_min DECIMAL(19,4)` in `CREATE TABLE` |

---

## 4. Repository Layer Reference

### All Properties and Generated Code Effects

| Property | Effect on Generated Code |
|----------|------------------------|
| `entityName` | Determines which entity class the repository manages |
| `className` | Name of the generated `interface {className} extends ReactiveCrudRepository<{Entity}, {idType}>` |
| `packageName` | Package declaration in generated file |
| `idType` | Generic type parameter for `ReactiveCrudRepository<Entity, {idType}>` |
| `hasCustomQueries` | If `true`, custom `@Query` methods are generated |
| `customQueries[]` | Each entry generates a method with `@Query` annotation |
| `hasSoftDelete` | Generates `findAllByIsDeletedFalse()`, overrides `deleteById` to set `is_deleted=true` |
| `hasAuthorization` | Generates `findByUserId(Long userId)` and `findByIdAndUserId(Long id, Long userId)` |
| `singleRecordPerUser` | Changes `findByUserId` return type from `Flux<Entity>` to `Mono<Entity>` |
| `enableCaching` | Adds `@Cacheable` on read methods, `@CacheEvict` on write methods |
| `cacheNames` | Specifies cache region names for `@Cacheable(cacheNames = {...})` |

### Custom Queries

Custom queries generate methods like:
```java
@Query("SELECT * FROM user_profile WHERE email = :email")
Mono<UserProfile> findByEmail(@Param("email") String email);
```

### Caching Behavior

When `enableCaching=true`:
- `findById` → `@Cacheable(cacheNames = "...", key = "#id")`
- `findAll` → `@Cacheable(cacheNames = "...")`
- `save` → `@CacheEvict(cacheNames = "...", allEntries = true)`
- `deleteById` → `@CacheEvict(cacheNames = "...", allEntries = true)`

### Soft-Delete Behavior

When `hasSoftDelete=true`:
- `findAll` is replaced with `findAllByIsDeletedFalse()`
- `deleteById` is replaced with an update that sets `is_deleted = true`
- `findById` adds a check for `is_deleted = false`

---

## 5. Service Layer Reference

### All Properties and Generated Code Effects

| Property | Effect on Generated Code |
|----------|------------------------|
| `entityName` | Determines which entity the service manages |
| `className` | Name of the generated `@Service` class |
| `repositoryName` | Injected via constructor: `private final {repositoryName} repository;` |
| `isRootEntity` | May affect initialization order or special handling |
| `hasAuthorization` | Injects `userId` from JWT SecurityContext into all CRUD methods |
| `singleRecordPerUser` | Create checks for existing record; getAll returns single user record |
| `authorizationConfig.*` | Fine-grained control over which operations check ownership |
| `transactionManagement.*` | `@Transactional` annotation with propagation/isolation/timeout |
| `customMethods[]` | Additional service methods beyond standard CRUD |
| `validationRules.*` | Validation logic in create/update/delete methods |

### Authorization Configuration Detail

When `hasAuthorization=true`:

| Config | Behavior |
|--------|----------|
| `checkOnCreate=true` | Validates user has permission to create (role check) |
| `checkOnRead=true` | Filters reads by `userId` — user only sees own records |
| `checkOnUpdate=true` | Verifies user owns the record before allowing update |
| `checkOnDelete=true` | Verifies user owns the record before allowing delete |
| `allowPublicRead=true` | getAll/getById skip ownership check (public data) |
| `requireOwnership=true` | All operations require `userId` match on the record |

### singleRecordPerUser Behavior

When `singleRecordPerUser=true`:
- **Create:** Checks if user already has a record → returns existing if found, creates new if not
- **GetAll:** Returns only the authenticated user's single record (not a list)
- **Update:** Only allows updating the user's own record
- **Delete:** Only allows deleting the user's own record

### Transaction Management

Generated `@Transactional` annotation:
```java
@Transactional(
    propagation = Propagation.REQUIRED,
    isolation = Isolation.DEFAULT,
    timeout = 30
)
```

---

## 6. Controller Layer Reference

### Standard CRUD Endpoints

| Endpoint | HTTP | Path | Request Body | Response | Description |
|----------|------|------|-------------|----------|-------------|
| `create` | POST | `{basePath}` | InputDTO | OutputDTO | Create new record |
| `getById` | GET | `{basePath}/{id}` | — | OutputDTO | Get single record by ID |
| `getAll` | GET | `{basePath}` | — (query params) | Page\<OutputDTO\> | List with pagination/filtering/sorting |
| `update` | PUT | `{basePath}/{id}` | InputDTO | OutputDTO | Update existing record |
| `delete` | DELETE | `{basePath}/{id}` | — | Void/204 | Delete record |

### Custom Endpoint Format

```json
{
  "name": "searchByTitle",
  "path": "/search",
  "method": "GET",
  "requiresAuth": true,
  "roles": ["USER"],
  "rateLimitPerMinute": 30,
  "description": "Search by title keyword"
}
```

### CORS Configuration

Applied at the controller class level via `@CrossOrigin`:
```java
@CrossOrigin(
    origins = {"*"},
    methods = {RequestMethod.GET, RequestMethod.POST, RequestMethod.PUT, RequestMethod.DELETE},
    allowedHeaders = {"*"},
    maxAge = 3600
)
```

### Rate Limiting

Each endpoint's `rateLimitPerMinute` generates rate limiting logic (typically via a filter or annotation) that limits requests per authenticated user per minute.

### Authentication/Authorization

When `requiresAuth=true` and `roles` is non-empty:
```java
@PreAuthorize("hasAnyRole('USER')")
```

### Pagination, Filtering, Sorting (getAll)

When enabled on the `getAll` endpoint:
- **Pagination:** `?page=0&size=20` query parameters
- **Filtering:** FilterDTO fields become query parameters (e.g. `?title=Engineer&location=NYC`)
- **Sorting:** `?sort=title&direction=ASC` query parameters

---

## 7. DTO Layer Reference

### Input DTO Generation

- Contains only user-defined fields (excludes PK, audit, soft-delete)
- Used as `@RequestBody` in create and update endpoints
- Fields with `includeInDTO=false` are excluded

### Output DTO Generation

- Contains PK + user fields + audit fields
- Used as response body for all read operations
- Includes `createdAt` and `updatedAt` timestamps

### Filter DTO Generation

- Contains only user-defined fields (same as Input)
- Used as query parameters for the `getAll` endpoint
- All fields are optional (nullable) for partial filtering

### fieldWidget Support

The `fieldWidget` property on DTO fields controls React frontend rendering:

| Widget | React Component | Use Case |
|--------|----------------|----------|
| `text` | `<input type="text">` | Short text fields |
| `richText` | WYSIWYG editor (TipTap/Quill) | Formatted content (descriptions, bios) |
| `codeEditor` | Monaco/CodeMirror | Source code fields. Requires `language` property |
| `markdown` | Split-pane MD editor | Documentation, README-style content |
| `json` | JSON editor with validation | Configuration objects, metadata |

### includeInDTO Flag

When `includeInDTO=false`:
- The field is excluded from the generated DTO class
- The field still exists in the entity and database
- Useful for internal fields that shouldn't be exposed via API

---

## 8. Relationship Reference

### Relationship Types

| Type | Description | Source Entity | Target Entity |
|------|-------------|--------------|---------------|
| `ManyToOne` | Many source records → one target | Has FK column | Referenced by FK |
| `OneToMany` | One source record → many targets | Referenced by FK | Has FK column |
| `ManyToMany` | Many-to-many via join table | Has join table | Has join table |

### Generated Code by Relationship Type

#### ManyToOne
- **Source Entity:** Adds FK field (e.g. `private Long jobPostingId;`)
- **Source Table DDL:** Adds FK column with `FOREIGN KEY` constraint
- **Repository:** Generates `findByJobPostingId(Long jobPostingId)` method
- **entities.json:** Adds column with `foreignKey: "job_posting.job_posting_id"`

#### OneToMany
- **Target Entity:** No change (FK is on the "many" side)
- **Repository:** Generates collection query method
- **Service:** May generate cascade delete logic

#### ManyToMany
- **DDL:** Generates join table (e.g. `user_skill` with `user_id` + `skill_id`)
- **Both Entities:** May generate collection fields
- **Repository:** Generates join query methods

### Cascade Types

| Value | Behavior |
|-------|----------|
| `ALL` | All operations cascade (persist, merge, remove, refresh, detach) |
| `PERSIST` | Only persist cascades |
| `MERGE` | Only merge cascades |
| `REMOVE` | Only remove cascades |
| `NONE` | No cascading |

---

## 9. Document Storage Layer Reference

### File Storage Configuration

When `fileStorage.enabled=true`, generates:
- File upload/download endpoints
- File storage service with configurable backend
- File metadata entity and repository

### JSON Column Mappings

JSON columns allow storing structured JSON data in a single database column:

```json
{
  "entityName": "UserProfile",
  "columnName": "preferences_json",
  "fieldName": "preferencesJson"
}
```

**Generated code:**
- Entity field: `private String preferencesJson;` with `@Column("preferences_json")`
- JSON converter: Custom R2DBC converter for JSON serialization/deserialization
- DDL: `preferences_json JSON` or `preferences_json TEXT` column

### Document Collections

Named collections for document management:

```json
{
  "name": "CourseDocuments",
  "tableName": "course_documents",
  "description": "Uploaded course materials"
}
```

**Generated code:**
- Dedicated entity class for the collection
- Repository with document-specific queries
- Service with upload/download/list operations
- DDL: Creates the collection table

---

## 10. AI Layer Reference

The `webflux_ai_layer.json` file contains 18+ configuration sections. Each section is documented below with complete field definitions.

### 10.1 schemaVersion

| Field | Type | Value | Description |
|-------|------|-------|-------------|
| `schemaVersion` | string | `"1.0"` | AI layer schema version |

### 10.2 providers

Array of AI provider configurations. Each provider represents a connection to an AI service (OpenAI, Ollama, etc.).

```json
{
  "name": "openai-main",
  "type": "openai",
  "model": "gpt-4",
  "apiKeyEnvVar": "OPENAI_API_KEY",
  "temperature": 0.7,
  "maxTokens": 2048,
  "embeddingModel": "text-embedding-3-small",
  "baseUrl": null,
  "chatOptions": {},
  "supportedParameters": [],
  "parameterFallbacks": {},
  "supportedRoles": [],
  "roleFallbacks": {},
  "resilience": {
    "retry": { "maxAttempts": 3, "backoffMs": 1000 },
    "circuitBreaker": { "failureThreshold": 5, "resetTimeoutMs": 60000 }
  }
}
```

| Field | Type | Required | Default | Valid Values | Description |
|-------|------|----------|---------|-------------|-------------|
| `name` | string | yes | — | unique string | Provider identifier (referenced by other sections) |
| `type` | string | yes | — | `"openai"`, `"ollama"` | Provider type |
| `model` | string | yes | — | — | Model name (e.g. `"gpt-4"`, `"llama3"`) |
| `apiKeyEnvVar` | string | no | `"OPENAI_API_KEY"` | — | Environment variable holding the API key |
| `temperature` | float | no | `0.7` | 0.0–2.0 | Sampling temperature |
| `maxTokens` | int | no | `2048` | — | Maximum tokens per response |
| `embeddingModel` | string | no | — | — | Embedding model for RAG/vector operations |
| `baseUrl` | string | no | — | — | Custom API base URL (for Ollama or proxies) |
| `chatOptions` | object | no | `{}` | — | Additional chat completion options |
| `supportedParameters` | array | no | `[]` | — | List of supported API parameters |
| `parameterFallbacks` | object | no | `{}` | — | Fallback values for unsupported parameters |
| `supportedRoles` | array | no | `[]` | — | Supported message roles |
| `roleFallbacks` | object | no | `{}` | — | Fallback role mappings |
| `resilience` | object | no | — | — | Retry and circuit breaker configuration |

#### resilience.retry Properties

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `maxAttempts` | int | `3` | Maximum retry attempts |
| `backoffMs` | int | `1000` | Backoff delay in milliseconds |

#### resilience.circuitBreaker Properties

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `failureThreshold` | int | `5` | Failures before circuit opens |
| `resetTimeoutMs` | int | `60000` | Time before circuit half-opens (ms) |

### 10.3 entityCapabilities

Array of per-entity AI capability configurations.

```json
{
  "entityName": "JobPosting",
  "providerName": "openai-main",
  "enabledOperations": ["summarize", "generate", "search"],
  "searchableFields": ["title", "description", "location"],
  "evaluatorNames": ["relevancy-eval"],
  "ragSourceNames": ["job-knowledge-base"],
  "chatOptions": {},
  "rolePromptSequence": [],
  "responseType": {}
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `entityName` | string | yes | PascalCase entity name (must exist in entity_layer) |
| `providerName` | string | yes | Provider name (must exist in `providers[]`) |
| `enabledOperations` | array | yes | List of enabled AI operations (e.g. `"summarize"`, `"generate"`, `"search"`, `"classify"`) |
| `searchableFields` | array | no | Entity fields available for AI-powered search |
| `evaluatorNames` | array | no | Evaluator names to apply (must exist in `evaluators[]`) |
| `ragSourceNames` | array | no | RAG source names to use (must exist in `ragSources[]`) |
| `chatOptions` | object | no | Override chat options for this entity |
| `rolePromptSequence` | array | no | Ordered prompt sequence with role assignments |
| `responseType` | object | no | Structured response format specification |

### 10.4 standaloneOperations

Array of standalone AI operations not tied to a specific entity.

```json
{
  "name": "career-advisor",
  "type": "chat",
  "providerName": "openai-main",
  "basePath": "/api/ai/career-advisor",
  "systemPrompt": "You are a career advisor...",
  "enabledActions": ["chat", "generate"],
  "rolePromptSequence": [],
  "assistantName": "career-assistant",
  "chatOptions": {},
  "stateTable": true,
  "evaluatorNames": [],
  "responseType": {},
  "ragSourceNames": []
}
```

| Field | Type | Required | Valid Values | Description |
|-------|------|----------|-------------|-------------|
| `name` | string | yes | unique string | Operation identifier |
| `type` | string | yes | `"chat"`, `"generate"`, `"query"`, `"workflow"` | Operation type |
| `providerName` | string | yes | — | Provider name (must exist) |
| `basePath` | string | yes | — | REST API base path |
| `systemPrompt` | string | yes | — | System prompt for the AI |
| `enabledActions` | array | yes | — | List of enabled actions |
| `rolePromptSequence` | array | no | — | Ordered prompt sequence |
| `assistantName` | string | no | — | Associated assistant (must exist in `assistants[]`) |
| `chatOptions` | object | no | — | Override chat options |
| `stateTable` | bool | no | — | Whether to persist conversation state |
| `evaluatorNames` | array | no | — | Evaluators to apply |
| `responseType` | object | no | — | Structured response format |
| `ragSourceNames` | array | no | — | RAG sources to use |

### 10.5 promptTemplates

Array of reusable prompt templates.

```json
{
  "name": "summarize-job",
  "operation": "summarize",
  "template": "Summarize the following job posting: {{content}}",
  "entityName": "JobPosting",
  "targetRole": "user"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Unique template name |
| `operation` | string | yes | Operation this template is for |
| `template` | string | yes | Template text with `{{variable}}` placeholders |
| `entityName` | string | no | Entity this template applies to |
| `targetRole` | string | no | Target message role |

### 10.6 assistants

Array of AI assistant configurations with memory and session management.

```json
{
  "name": "career-assistant",
  "systemPrompt": "You are a helpful career advisor...",
  "providerName": "openai-main",
  "entityScope": "all",
  "memoryWindowSize": 20,
  "rolePromptSequence": [],
  "sessionTtlDays": 30,
  "chatOptions": {}
}
```

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | yes | — | Unique assistant name |
| `systemPrompt` | string | yes | — | System prompt defining assistant behavior |
| `providerName` | string | yes | — | Provider name (must exist) |
| `entityScope` | string | yes | — | Entity scope (`"all"` or specific entity name) |
| `memoryWindowSize` | int | no | `20` | Number of messages to keep in context window |
| `rolePromptSequence` | array | no | — | Ordered prompt sequence |
| `sessionTtlDays` | int | no | — | Session time-to-live in days |
| `chatOptions` | object | no | — | Override chat options |

### 10.7 ragSources

Array of Retrieval-Augmented Generation source configurations.

```json
{
  "name": "job-knowledge-base",
  "type": "semantic",
  "enabled": true,
  "providerName": "openai-main",
  "targets": ["JobPosting", "TrainingProgram"],
  "securityMode": "public",
  "chunkSize": 512,
  "chunkOverlap": 50,
  "topK": 5,
  "similarityThreshold": 0.7
}
```

| Field | Type | Required | Valid Values | Default | Description |
|-------|------|----------|-------------|---------|-------------|
| `name` | string | yes | unique string | — | RAG source identifier |
| `type` | string | yes | `"semantic"`, `"heuristic"` | — | RAG type |
| `enabled` | bool | no | — | `false` | Whether the source is active |
| `providerName` | string | semantic only | — | — | Provider for embeddings (required for semantic) |
| `targets` | array | no | — | — | Entity names this source covers |
| `securityMode` | string | no | `"public"`, `"role_restricted"` | `"public"` | Access control mode |
| `chunkSize` | int | no | — | — | Document chunk size in tokens |
| `chunkOverlap` | int | no | — | — | Overlap between chunks |
| `topK` | int | no | — | — | Number of top results to retrieve |
| `similarityThreshold` | float | no | — | — | Minimum similarity score |
| `rules` | array | no | — | — | Heuristic matching rules |
| `maxResults` | int | no | — | — | Maximum results to return |

### 10.8 evaluators

Array of AI output evaluation configurations.

```json
{
  "name": "relevancy-eval",
  "type": "relevancy",
  "providerName": "openai-main",
  "evaluationPrompt": "Rate the relevancy of this response...",
  "scoringMechanism": "numeric",
  "mode": "async",
  "failureAction": "none",
  "threshold": 0.7,
  "categories": [],
  "maxRetries": 3
}
```

| Field | Type | Required | Valid Values | Default | Description |
|-------|------|----------|-------------|---------|-------------|
| `name` | string | yes | unique string | — | Evaluator identifier |
| `type` | string | yes | `"relevancy"`, `"correctness"`, `"safety"`, `"custom"` | — | Evaluation type |
| `providerName` | string | yes | — | — | Provider for evaluation (must exist) |
| `evaluationPrompt` | string | yes | — | — | Prompt used for evaluation |
| `scoringMechanism` | string | yes | `"numeric"`, `"pass_fail"`, `"categorical"` | — | How results are scored |
| `mode` | string | no | `"sync"`, `"async"` | `"async"` | Execution mode |
| `failureAction` | string | no | `"none"`, `"retry"`, `"warn"` | `"none"` | Action on evaluation failure |
| `threshold` | float | no | — | — | Score threshold for pass/fail |
| `categories` | array | no | — | — | Categories for categorical scoring |
| `maxRetries` | int | no | — | — | Max retries on failure |

**Constraint:** `mode="async"` cannot have `failureAction="retry"`.

### 10.9 vectorStore

Vector database configuration for RAG embeddings.

```json
{
  "type": "milvus",
  "host": "localhost",
  "port": 19530,
  "collectionPrefix": "ai_",
  "maxConnections": 10,
  "connectTimeoutMs": 5000,
  "idleTimeoutMs": 60000,
  "apiKey": null,
  "database": null
}
```

| Field | Type | Default | Valid Values | Description |
|-------|------|---------|-------------|-------------|
| `type` | string | `"milvus"` | `"milvus"`, `"qdrant"`, `"pgvector"`, `"in_memory"` | Vector store type |
| `host` | string | `"localhost"` | — | Host address |
| `port` | int | `19530` | — | Port number |
| `collectionPrefix` | string | `"ai_"` | — | Prefix for collection names |
| `maxConnections` | int | `10` | — | Connection pool size |
| `connectTimeoutMs` | int | `5000` | — | Connection timeout (ms) |
| `idleTimeoutMs` | int | `60000` | — | Idle connection timeout (ms) |
| `apiKey` | string | `null` | — | API key for cloud vector stores |
| `database` | string | `null` | — | Database name (for pgvector) |

### 10.10 documentIngestion

Document upload and indexing configuration.

```json
{
  "enabled": true,
  "allowedMimeTypes": ["application/pdf", "text/plain"],
  "maxFileSizeBytes": 10485760,
  "metadataFields": [],
  "autoIndexOnUpload": true,
  "sources": [],
  "maxTotalStorageBytes": null,
  "targetRagSourceName": "job-knowledge-base"
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | bool | `true` | Whether ingestion is enabled |
| `allowedMimeTypes` | array | `["application/pdf", "text/plain"]` | Accepted file types |
| `maxFileSizeBytes` | int | `10485760` (10MB) | Max file size |
| `metadataFields` | array | `[]` | Custom metadata fields |
| `autoIndexOnUpload` | bool | `true` | Auto-index after upload |
| `sources` | array | `[]` | Document source configurations |
| `maxTotalStorageBytes` | int | `null` | Total storage limit |
| `targetRagSourceName` | string | — | RAG source to index into (must exist in `ragSources[]`) |

### 10.11 documentProcessing

AI-powered document processing tasks.

```json
{
  "enabled": true,
  "defaultProviderName": "openai-main",
  "tasks": [
    {
      "name": "summarize-doc",
      "taskType": "summarization",
      "providerName": "openai-main",
      "promptTemplate": "Summarize: {{content}}",
      "eligibleProviders": [],
      "chatOptions": {},
      "responseFormat": null,
      "targetScope": null,
      "targetLanguage": null,
      "categories": [],
      "requiresSecondDocument": false
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | bool | Whether processing is enabled |
| `defaultProviderName` | string | Default provider (must exist) |
| `tasks` | array | Processing task definitions |

**Prerequisite:** `documentIngestion` must be configured before `documentProcessing`.

#### Task Properties

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | yes | Unique task name |
| `taskType` | string | yes | Task type (e.g. `"summarization"`, `"classification"`, `"extraction"`, `"translation"`, `"comparison"`) |
| `providerName` | string | yes | Provider for this task (must exist) |
| `promptTemplate` | string | yes | Prompt template with `{{content}}` placeholder |
| `eligibleProviders` | array | no | Alternative providers |
| `chatOptions` | object | no | Override chat options |
| `responseFormat` | object | no | Structured response format |
| `targetScope` | string | no | Scope of processing |
| `targetLanguage` | string | no | Target language for translation |
| `categories` | array | no | Categories for classification |
| `requiresSecondDocument` | bool | no | Whether comparison requires two documents |

### 10.12 orchestrator

Central AI orchestration configuration with prompt security and moderation.

```json
{
  "providerName": "openai-main",
  "systemPrompt": "You are the orchestrator...",
  "chatOptions": {},
  "accessDeniedMessage": "Access denied.",
  "promptSecurity": {
    "safeGuardAdvisor": {
      "enabled": true,
      "sensitiveWords": ["password", "secret"]
    },
    "canaryWordAdvisor": {
      "enabled": true,
      "canaryTokens": ["CANARY_TOKEN_1"]
    },
    "inputSanitization": {
      "enabled": true,
      "rules": []
    },
    "outputFiltering": {
      "enabled": true,
      "rules": []
    }
  },
  "moderation": {
    "enabled": true,
    "providerName": "openai-main",
    "categories": ["hate", "violence", "sexual"],
    "preModeration": true,
    "postModeration": true,
    "failureAction": "block"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `providerName` | string | yes | Provider for orchestration (must exist) |
| `systemPrompt` | string | no | System prompt for the orchestrator |
| `chatOptions` | object | no | Chat completion options |
| `accessDeniedMessage` | string | no | Message shown when access is denied |
| `promptSecurity` | object | no | Prompt security configuration (see below) |
| `moderation` | object | no | Content moderation configuration (see below) |

**Prerequisite:** Orchestrator must be configured before MCP servers.

#### promptSecurity Sub-Sections

**safeGuardAdvisor:**

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | bool | Whether safeguard is active |
| `sensitiveWords` | array | Words to detect and block |

**canaryWordAdvisor:**

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | bool | Whether canary detection is active |
| `canaryTokens` | array | Canary tokens to inject and monitor |

**inputSanitization:**

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | bool | Whether input sanitization is active |
| `rules` | array | Sanitization rules |

**outputFiltering:**

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | bool | Whether output filtering is active |
| `rules` | array | Filtering rules |

#### moderation Properties

| Field | Type | Valid Values | Default | Description |
|-------|------|-------------|---------|-------------|
| `enabled` | bool | — | — | Whether moderation is active |
| `providerName` | string | — | — | Provider for moderation (must exist) |
| `categories` | array | — | — | Content categories to moderate |
| `preModeration` | bool | — | `true` | Moderate input before processing |
| `postModeration` | bool | — | `true` | Moderate output before returning |
| `failureAction` | string | `"block"`, `"warn"`, `"log"` | `"block"` | Action on moderation failure |

### 10.13 mcpServers

Array of Model Context Protocol server configurations.

```json
{
  "name": "code-tools",
  "transportType": "stdio",
  "requiredRoles": ["ADMIN"],
  "enabled": false,
  "envVars": {},
  "auth": {},
  "exposedTools": [],
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-code"],
  "url": null,
  "sseEndpoint": null
}
```

| Field | Type | Required | Valid Values | Description |
|-------|------|----------|-------------|-------------|
| `name` | string | yes | unique string | MCP server identifier |
| `transportType` | string | yes | `"stdio"`, `"sse"` | Transport protocol |
| `requiredRoles` | array | yes | — | Roles required to access this server |
| `enabled` | bool | no | — | Whether the server is active |
| `envVars` | object | no | — | Environment variables for the server |
| `auth` | object | no | — | Authentication configuration |
| `exposedTools` | array | no | — | List of tools exposed by this server |
| `command` | string | no | — | Command to start stdio server |
| `args` | array | no | — | Command arguments |
| `url` | string | no | — | SSE server URL |
| `sseEndpoint` | string | no | — | SSE endpoint path |

**Prerequisite:** Orchestrator must be configured before adding MCP servers.

### 10.14 observability

Monitoring and observability configuration.

```json
{
  "enabled": true,
  "prometheus": {},
  "grafana": {
    "url": "http://localhost:3000",
    "apiKeyEnvVar": "GRAFANA_API_KEY"
  },
  "dashboards": [
    {
      "name": "ai-overview",
      "panels": [
        {"title": "Request Rate", "type": "graph", "metric": "ai_requests_total"}
      ],
      "layout": {}
    }
  ]
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `enabled` | bool | yes | Whether observability is active |
| `prometheus` | object | no | Prometheus configuration |
| `grafana` | object | no | Grafana configuration (requires `url` and `apiKeyEnvVar`) |
| `dashboards` | array | no | Dashboard definitions |

### 10.15 rateLimiting

AI-specific rate limiting configuration.

```json
{
  "defaultRpm": 20,
  "overrides": {
    "entity": 30,
    "standalone": 15,
    "rag": 10,
    "evaluations": 5,
    "documentIngestion": 5,
    "documentProcessing": 5,
    "orchestrator": 20,
    "observability": 100
  }
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `defaultRpm` | int | `20` | Default requests per minute |
| `overrides` | object | — | Per-category RPM overrides |

**Valid override categories:** `"entity"`, `"standalone"`, `"rag"`, `"evaluations"`, `"documentIngestion"`, `"documentProcessing"`, `"orchestrator"`, `"observability"`

### 10.16 tokenBudget

Token usage budget and enforcement.

```json
{
  "enabled": true,
  "defaultDailyLimitPerUser": 100000,
  "defaultMonthlyLimitPerUser": 2000000,
  "warningThresholdPercent": 80,
  "enforcementAction": "warn",
  "providerOverrides": {
    "openai-main": {
      "dailyLimit": 50000,
      "monthlyLimit": 1000000
    }
  }
}
```

| Field | Type | Default | Valid Values | Description |
|-------|------|---------|-------------|-------------|
| `enabled` | bool | `true` | — | Whether budget enforcement is active |
| `defaultDailyLimitPerUser` | int | — | — | Default daily token limit per user |
| `defaultMonthlyLimitPerUser` | int | — | — | Default monthly token limit per user |
| `warningThresholdPercent` | int | — | 0–100 | Percentage at which to warn |
| `enforcementAction` | string | — | `"block"`, `"warn"`, `"log"` | Action when budget exceeded |
| `providerOverrides` | object | — | — | Per-provider budget overrides (provider must exist) |

### 10.17 chatSessionCleanup

Chat session lifecycle management.

```json
{
  "enabled": true,
  "defaultTtlDays": 30,
  "cleanupCronExpression": "0 0 2 * * *",
  "batchSize": 1000,
  "topicSummarization": {
    "enabled": true,
    "providerName": "openai-main",
    "maxTopicsPerSession": 5
  }
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | bool | `true` | Whether cleanup is active |
| `defaultTtlDays` | int | `30` | Session time-to-live in days |
| `cleanupCronExpression` | string | `"0 0 2 * * *"` | Cron expression for cleanup job |
| `batchSize` | int | `1000` | Sessions to clean per batch |
| `topicSummarization` | object | — | Topic summarization before cleanup |

#### topicSummarization Properties

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | bool | Whether to summarize topics before cleanup |
| `providerName` | string | Provider for summarization (must exist) |
| `maxTopicsPerSession` | int | Max topics to extract per session |

### 10.18 auditLog

AI operation audit logging.

```json
{
  "enabled": true,
  "retentionDays": 90,
  "cleanupCronExpression": "0 0 3 * * *",
  "loggedEvents": [
    "orchestrator_request",
    "tool_invocation",
    "moderation_flag",
    "security_violation",
    "budget_exceeded"
  ]
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | bool | `true` | Whether audit logging is active |
| `retentionDays` | int | `90` | Days to retain audit logs |
| `cleanupCronExpression` | string | `"0 0 3 * * *"` | Cron expression for log cleanup |
| `loggedEvents` | array | — | Event types to log |

**Valid audit event types:** `"orchestrator_request"`, `"tool_invocation"`, `"moderation_flag"`, `"security_violation"`, `"budget_exceeded"`, `"session_created"`, `"document_ingested"`, `"provider_error"`, `"circuit_breaker_state_change"`

---

## 11. React AI Config Reference

The `react_ai_config.json` file controls the React frontend's AI features.

### 11.1 chatPanel

```json
{
  "enabled": false,
  "position": "sidebar",
  "defaultAssistant": "",
  "showOnPages": [],
  "streamingEnabled": true
}
```

| Field | Type | Default | Valid Values | Description |
|-------|------|---------|-------------|-------------|
| `enabled` | bool | `false` | — | Whether the chat panel is shown |
| `position` | string | `"sidebar"` | `"sidebar"`, `"bottom"`, `"floating"` | Chat panel position |
| `defaultAssistant` | string | `""` | — | Default assistant name (must exist in AI layer `assistants[]`) |
| `showOnPages` | array | `[]` | — | Page routes where chat is visible (empty = all pages) |
| `streamingEnabled` | bool | `true` | — | Whether to stream responses token-by-token |

### 11.2 entityFeatures

Array of per-entity AI feature configurations for the React frontend.

```json
{
  "entityName": "JobPosting",
  "smartSearch": true,
  "contentGeneration": [
    {
      "fieldName": "description",
      "buttonLabel": "Generate Description",
      "promptTemplate": "Generate a job description for: {{title}}"
    }
  ],
  "suggestions": [
    {
      "fieldName": "title",
      "triggerOn": "blur",
      "maxSuggestions": 5
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `entityName` | string | PascalCase entity name |
| `smartSearch` | bool | Enable AI-powered search on entity list page |
| `contentGeneration` | array | Fields with AI content generation buttons |
| `suggestions` | array | Fields with AI-powered suggestions |

#### contentGeneration Entry

| Field | Type | Description |
|-------|------|-------------|
| `fieldName` | string | Target field name |
| `buttonLabel` | string | Button text in the UI |
| `promptTemplate` | string | Prompt template with `{{field}}` placeholders |

#### suggestions Entry

| Field | Type | Description |
|-------|------|-------------|
| `fieldName` | string | Target field name |
| `triggerOn` | string | When to trigger (`"blur"`, `"type"`, `"focus"`) |
| `maxSuggestions` | int | Maximum suggestions to show |

### 11.3 standaloneFeatures

Array of standalone AI feature page configurations.

```json
{
  "operationName": "career-advisor",
  "pageRoute": "/ai/career-advisor",
  "pageTitle": "Career Advisor",
  "componentType": "chat",
  "showInNav": true
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `operationName` | string | required | Standalone operation name (must exist in AI layer) |
| `pageRoute` | string | required | React Router path |
| `pageTitle` | string | required | Page title in browser/nav |
| `componentType` | string | `"chat"` | Component type (`"chat"`, `"form"`, `"dashboard"`) |
| `showInNav` | bool | `true` | Whether to show in navigation menu |

### 11.4 theme

AI feature theme configuration.

```json
{
  "accentColor": "#6366f1",
  "chatBubbleStyle": "rounded",
  "loadingAnimation": "dots"
}
```

| Field | Type | Default | Valid Values | Description |
|-------|------|---------|-------------|-------------|
| `accentColor` | string | `"#6366f1"` | CSS color | Primary accent color for AI features |
| `chatBubbleStyle` | string | `"rounded"` | `"rounded"`, `"square"`, `"minimal"` | Chat message bubble style |
| `loadingAnimation` | string | `"dots"` | `"dots"`, `"spinner"`, `"pulse"`, `"skeleton"` | Loading indicator style |

### 11.5 evaluationDisplay

```json
{
  "enabled": true,
  "badgeStyle": "compact",
  "showScores": true,
  "showDetails": false
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | bool | — | Whether evaluation badges are shown |
| `badgeStyle` | string | `"compact"` | Badge display style (`"compact"`, `"detailed"`, `"minimal"`) |
| `showScores` | bool | `true` | Show numeric scores |
| `showDetails` | bool | `false` | Show evaluation details on click |

### 11.6 ragFeatures

```json
{
  "enabled": true,
  "adminPageRoute": "/admin/rag",
  "showSourceCitations": true,
  "allowDocumentUpload": true
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled` | bool | — | Whether RAG features are shown |
| `adminPageRoute` | string | `"/admin/rag"` | Admin page for RAG management |
| `showSourceCitations` | bool | `true` | Show source citations in AI responses |
| `allowDocumentUpload` | bool | `true` | Allow users to upload documents |

---

## 12. CLI Command Reference

All commands are invoked via: `py app_def_manager/cli.py <command> [args]`

### Core CRUD Commands

#### scaffold
Create a new application with all 12 definition files.
```bash
py app_def_manager/cli.py scaffold \
  --name my_app \
  --entities '[{"name":"User","fields":[{"name":"email","type":"String"}]}]' \
  [--db-name my_db] \
  [--base-package com.example] \
  [--force]
```

| Arg | Required | Default | Description |
|-----|----------|---------|-------------|
| `--name` | yes | — | Application name (used as folder name) |
| `--entities` | yes | — | JSON array of entity descriptions |
| `--db-name` | no | snake_case of name | Database name |
| `--base-package` | no | `com.example` | Java base package |
| `--force` | no | `false` | Overwrite existing directory |

#### add-entity
Add entity to all 6 layer files.
```bash
py app_def_manager/cli.py add-entity \
  --app my_app \
  --name Product \
  --fields '[{"name":"title","type":"String"},{"name":"price","type":"BigDecimal"}]'
```

#### remove-entity
Remove entity from all 6 layer files.
```bash
py app_def_manager/cli.py remove-entity --app my_app --name Product
```

#### add-field
Add field to entity_layer + entities + dto_layer (3 files).
```bash
py app_def_manager/cli.py add-field \
  --app my_app \
  --entity User \
  --field '{"name":"age","type":"Integer"}'
```

Supports `fieldWidget`:
```bash
py app_def_manager/cli.py add-field \
  --app my_app \
  --entity User \
  --field '{"name":"bio","type":"String","fieldWidget":"richText"}'
```

#### remove-field
```bash
py app_def_manager/cli.py remove-field --app my_app --entity User --field age
```

#### modify-field
```bash
py app_def_manager/cli.py modify-field \
  --app my_app \
  --entity User \
  --field age \
  --updates '{"type":"Long","isNullable":false}'
```

Supports `fieldWidget` updates:
```bash
py app_def_manager/cli.py modify-field \
  --app my_app \
  --entity User \
  --field bio \
  --updates '{"fieldWidget":"markdown"}'
```

#### add-endpoint
```bash
py app_def_manager/cli.py add-endpoint \
  --app my_app \
  --entity User \
  --endpoint '{"name":"search","path":"/search","method":"GET","requiresAuth":true,"roles":["USER"]}'
```

#### remove-endpoint
```bash
py app_def_manager/cli.py remove-endpoint --app my_app --entity User --endpoint search
```

#### add-query
```bash
py app_def_manager/cli.py add-query \
  --app my_app \
  --entity User \
  --query '{"name":"findByEmail","query":"SELECT * FROM user WHERE email = :email","returnType":"Mono","parameters":[{"name":"email","type":"String"}]}'
```

#### remove-query
```bash
py app_def_manager/cli.py remove-query --app my_app --entity User --query findByEmail
```

#### add-relationship
```bash
py app_def_manager/cli.py add-relationship \
  --app my_app \
  --relationship '{"sourceEntity":"Order","targetEntity":"Product","type":"ManyToOne","sourceColumn":"product_id","targetColumn":"product_id"}'
```

#### remove-relationship
```bash
py app_def_manager/cli.py remove-relationship --app my_app --source Order --target Product
```

### Document Storage Commands

#### add-json-column
```bash
py app_def_manager/cli.py add-json-column --app my_app --entity User --column preferences_json --field preferencesJson
```

#### remove-json-column
```bash
py app_def_manager/cli.py remove-json-column --app my_app --entity User --field preferencesJson
```

#### add-document-collection
```bash
py app_def_manager/cli.py add-document-collection --app my_app --name CourseDocuments --table course_documents --description "Course materials"
```

#### remove-document-collection
```bash
py app_def_manager/cli.py remove-document-collection --app my_app --name CourseDocuments
```

### Status Commands

#### status
```bash
py app_def_manager/cli.py status --app my_app
```

#### mark-clean
```bash
py app_def_manager/cli.py mark-clean --app my_app [--file webflux_entity_layer.json]
```

#### mark-dirty
```bash
py app_def_manager/cli.py mark-dirty --app my_app [--file webflux_entity_layer.json]
```

### Discovery Commands

#### list-apps
```bash
py app_def_manager/cli.py list-apps
```

#### list-entities
```bash
py app_def_manager/cli.py list-entities --app my_app
```

#### describe
```bash
# Table format (default)
py app_def_manager/cli.py describe --app my_app

# Markdown format
py app_def_manager/cli.py describe --app my_app --format markdown

# Single entity detail
py app_def_manager/cli.py describe --app my_app --entity UserProfile

# AI layer summary
py app_def_manager/cli.py describe --app my_app --ai-layer

# React AI config summary
py app_def_manager/cli.py describe --app my_app --ai-react
```

### Batch Operations

#### batch
Run multiple commands from a JSON file.
```bash
py app_def_manager/cli.py batch --file ops.json
```

**Batch file format:**
```json
[
  {"command": "add-entity", "app": "my_app", "name": "Product",
   "fields": [{"name": "title", "type": "String"}]},
  {"command": "remove-field", "app": "my_app", "entity": "Order", "field": "old_col"},
  {"command": "add-relationship", "app": "my_app",
   "relationship": {"sourceEntity": "Order", "targetEntity": "Product", "type": "ManyToOne"}}
]
```

#### bulk-update
Batch-update entity-level flags across service/repository/controller layers.
```bash
# Enable auth on all entities
py app_def_manager/cli.py bulk-update --app my_app --entities ALL \
  --set hasAuthorization=true --set requiresAuth=true --set roles=USER

# Enable singleRecordPerUser on specific entities
py app_def_manager/cli.py bulk-update --app my_app \
  --entities UserProfile,StudentProfile --set singleRecordPerUser=true
```

| Arg | Required | Description |
|-----|----------|-------------|
| `--app` | yes | Application name |
| `--entities` | yes | Comma-separated entity names or `ALL` |
| `--set` | yes (repeatable) | `key=value` pair to set |

**Supported flags:** `hasAuthorization`, `singleRecordPerUser`, `requiresAuth`, `roles`, `enableCaching`, and any other entity-level JSON key.

**Endpoint-level keys** (`requiresAuth`, `roles`) are applied to all endpoints within matching controllers.

### AI CRUD Commands

All AI commands follow the pattern: `ai-<action>-<target>`

#### Providers
```bash
py app_def_manager/cli.py ai-add-provider --app my_app --name openai-main --type openai --model gpt-4 [--api-key-env-var OPENAI_API_KEY]
py app_def_manager/cli.py ai-remove-provider --app my_app --name openai-main
```

#### Entity Capabilities
```bash
py app_def_manager/cli.py ai-add-capability --app my_app --entity JobPosting --provider openai-main --operations summarize,generate,search
py app_def_manager/cli.py ai-remove-capability --app my_app --entity JobPosting
```

#### Prompt Templates
```bash
py app_def_manager/cli.py ai-add-prompt-template --app my_app --name summarize-job --operation summarize --template "Summarize: {{content}}"
py app_def_manager/cli.py ai-remove-prompt-template --app my_app --name summarize-job
```

#### Assistants
```bash
py app_def_manager/cli.py ai-add-assistant --app my_app --name career-assistant --system-prompt "You are a career advisor" --provider openai-main --entity-scope all
py app_def_manager/cli.py ai-remove-assistant --app my_app --name career-assistant
```

#### Standalone Operations
```bash
py app_def_manager/cli.py ai-add-standalone --app my_app --name career-advisor --type chat --provider openai-main --base-path /api/ai/career --system-prompt "You are a career advisor" --actions chat,generate
py app_def_manager/cli.py ai-remove-standalone --app my_app --name career-advisor
```

#### RAG Sources
```bash
py app_def_manager/cli.py ai-add-rag-source --app my_app --name job-kb --type semantic --provider openai-main --enabled
py app_def_manager/cli.py ai-remove-rag-source --app my_app --name job-kb
```

#### Evaluators
```bash
py app_def_manager/cli.py ai-add-evaluator --app my_app --name relevancy-eval --type relevancy --provider openai-main --prompt "Rate relevancy..." --scoring numeric
py app_def_manager/cli.py ai-remove-evaluator --app my_app --name relevancy-eval
```

#### Orchestrator
```bash
py app_def_manager/cli.py ai-set-orchestrator --app my_app --provider openai-main
py app_def_manager/cli.py ai-remove-orchestrator --app my_app
```

#### MCP Servers
```bash
py app_def_manager/cli.py ai-add-mcp-server --app my_app --name code-tools --transport stdio --roles ADMIN
py app_def_manager/cli.py ai-remove-mcp-server --app my_app --name code-tools
```

#### Vector Store
```bash
py app_def_manager/cli.py ai-set-vector-store --app my_app --type milvus
py app_def_manager/cli.py ai-remove-vector-store --app my_app
```

#### Observability
```bash
py app_def_manager/cli.py ai-set-observability --app my_app
py app_def_manager/cli.py ai-remove-observability --app my_app
```

#### Token Budget
```bash
py app_def_manager/cli.py ai-set-token-budget --app my_app --daily-limit 100000 --monthly-limit 2000000
py app_def_manager/cli.py ai-remove-token-budget --app my_app
```

#### Rate Limiting
```bash
py app_def_manager/cli.py ai-set-rate-limiting --app my_app --default-rpm 20
py app_def_manager/cli.py ai-remove-rate-limiting --app my_app
```

#### Session Cleanup
```bash
py app_def_manager/cli.py ai-set-session-cleanup --app my_app --ttl-days 30
py app_def_manager/cli.py ai-remove-session-cleanup --app my_app
```

#### Audit Log
```bash
py app_def_manager/cli.py ai-set-audit-log --app my_app --retention-days 90
py app_def_manager/cli.py ai-remove-audit-log --app my_app
```

#### Document Ingestion
```bash
py app_def_manager/cli.py ai-set-document-ingestion --app my_app
py app_def_manager/cli.py ai-remove-document-ingestion --app my_app
```

#### Document Processing
```bash
py app_def_manager/cli.py ai-set-document-processing --app my_app
py app_def_manager/cli.py ai-remove-document-processing --app my_app
```

#### Moderation
```bash
py app_def_manager/cli.py ai-set-moderation --app my_app --provider openai-main --categories hate,violence,sexual
py app_def_manager/cli.py ai-remove-moderation --app my_app
```

---

## 13. Status Tracking & Dirty/Clean System

### How _generation_status.json Works

The `_generation_status.json` file tracks the state of each definition file:

```json
{
  "app_name": "job_portal",
  "schema_version": "1.0",
  "files": {
    "webflux_entity_layer.json": {
      "status": "clean",
      "last_modified": "2026-04-12T10:09:59Z",
      "last_generated": "2026-04-12T10:55:18Z",
      "content_hash": "sha256:286c29d6bae6b065d080ba822058d7d221aa5c3109cf33f995c5023334ed0526"
    }
  },
  "last_full_generation": null
}
```

#### Per-File Status Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `"dirty"` or `"clean"` |
| `last_modified` | string | ISO 8601 UTC timestamp of last definition change |
| `last_generated` | string\|null | ISO 8601 UTC timestamp of last code generation |
| `content_hash` | string | `"sha256:{hex}"` hash of the file contents |

### SHA-256 Hash-Based External Edit Detection

The StatusTracker detects external edits (manual JSON file changes outside the tool) by comparing stored hashes:

1. When a file is marked **clean**, its SHA-256 hash is stored in `content_hash`
2. On any status query (`get_dirty_files`, `get_clean_files`, `is_dirty`), the tracker:
   - Recomputes the current SHA-256 hash of each clean file
   - Compares against the stored `content_hash`
   - If they differ → auto-marks the file as **dirty** with a warning
3. This ensures external edits are never missed

### Status Lifecycle

```
scaffold/add/remove/modify → mark_dirty() → [files are dirty]
                                                    │
                                                    ▼
                                    Phase 3 reads dirty files
                                    DependencyMapper resolves outputs
                                    IncrementalGenerator regenerates
                                                    │
                                                    ▼
                                            mark_clean() → [files are clean]
                                                    │
                                                    ▼
                                    External edit detected? → auto mark_dirty()
```

### Dependency Mapping (Which Files Trigger Which Regeneration)

| Definition File | Triggers Regeneration Of |
|----------------|--------------------------|
| `webflux_entity_layer.json` | Entity, all DTOs, Repository, Service, Controller, SQL |
| `webflux_entities.json` | Entity, SQL |
| `webflux_relationships.json` | Entity, Repository, SQL |
| `webflux_repository_layer.json` | Repository |
| `webflux_service_layer.json` | Service |
| `webflux_controller_layer.json` | Controller |
| `webflux_dto_layer.json` | Input/Output/Filter DTOs |
| `webflux_project_metadata.json` | Config, POM, SQL |
| `webflux_document_storage_layer.json` | File storage, JSON converter, Document collection, SQL |
| `webflux_ai_layer.json` | AI service, AI controller, AI entity, AI config, AI DTO, AI repository, AI provider, AI RAG, AI evaluator, AI ingestion, AI processing, AI vectorstore, AI orchestrator, AI tools, AI MCP, AI observability, AI budget, AI audit, SQL |

### SQL Trigger Files

These definition files trigger SQL DDL regeneration when dirty:
- `webflux_entity_layer.json`
- `webflux_entities.json`
- `webflux_relationships.json`
- `webflux_project_metadata.json`
- `webflux_document_storage_layer.json`
- `webflux_ai_layer.json`

---

## 14. Cross-Layer Consistency

### How CRUD Operations Maintain Consistency

The CRUDManager ensures that mutations are applied consistently across all affected definition files.

#### Entity Operations (6 files affected)

When adding an entity, CRUDManager writes to all 6 files atomically:

| File | What Gets Added |
|------|----------------|
| `webflux_entity_layer.json` | Entity definition with fields (PK + user + audit) |
| `webflux_entities.json` | Column-level view with SQL types |
| `webflux_repository_layer.json` | Repository definition with defaults |
| `webflux_service_layer.json` | Service definition with auth/transaction defaults |
| `webflux_controller_layer.json` | Controller with 5 CRUD endpoints + CORS |
| `webflux_dto_layer.json` | Input, Output, and Filter DTOs |

When removing an entity, all 6 files are cleaned up.

#### Field Operations (3 files affected)

| File | What Gets Modified |
|------|-------------------|
| `webflux_entity_layer.json` | Field added/removed/modified in entity's `fields[]` |
| `webflux_entities.json` | Column added/removed/modified in entity's `columns[]` |
| `webflux_dto_layer.json` | Field added/removed/modified in Input, Output, and Filter DTOs |

#### Single-File Operations

| Operation | File Affected |
|-----------|--------------|
| add/remove endpoint | `webflux_controller_layer.json` |
| add/remove query | `webflux_repository_layer.json` |
| add/remove relationship | `webflux_relationships.json` |
| add/remove json-column | `webflux_document_storage_layer.json` |
| add/remove document-collection | `webflux_document_storage_layer.json` |
| All AI operations | `webflux_ai_layer.json` and/or `react_ai_config.json` |

### Dependency Removal Checks (ValueError on Dangling References)

The AiCRUDManager enforces referential integrity:

| Operation | Checks Before Removal |
|-----------|----------------------|
| Remove provider | Checks entityCapabilities, standaloneOperations, assistants, ragSources, evaluators, orchestrator, moderation, documentProcessing, tokenBudget.providerOverrides, chatSessionCleanup.topicSummarization |
| Remove assistant | Checks standaloneOperations for `assistantName` references |
| Remove RAG source | Checks entityCapabilities, standaloneOperations for `ragSourceNames` references, documentIngestion for `targetRagSourceName` |
| Remove evaluator | Checks entityCapabilities, standaloneOperations for `evaluatorNames` references |
| Remove orchestrator | Checks mcpServers (requires orchestrator) |
| Remove documentIngestion | Checks documentProcessing (depends on ingestion) |

If dependencies exist, a `ValueError` is raised listing all dependents:
```
ValueError: Cannot remove provider 'openai-main': referenced by entityCapability 'JobPosting', standaloneOperation 'career-advisor', assistant 'career-assistant'
```

### Bulk Update Consistency

The BulkUpdater applies updates across service, repository, and controller layers simultaneously:
- Entity-level keys (e.g. `hasAuthorization`, `singleRecordPerUser`) → applied to service, repository, and controller entries
- Endpoint-level keys (`requiresAuth`, `roles`) → applied to all endpoints within matching controllers
- All affected files are marked dirty after update

---

## 15. Generated Code Behavior

### Entity Class Generation

From entity_layer definition:
```json
{
  "tableName": "job_posting",
  "className": "JobPosting",
  "packageName": "com.jobportal.entity",
  "fields": [
    {"columnName": "job_posting_id", "fieldName": "jobPostingId", "javaType": "Long", "isPrimaryKey": true, "isNullable": false, "columnDefinition": "BIGINT UNSIGNED"},
    {"columnName": "title", "fieldName": "title", "javaType": "String", "isPrimaryKey": false, "isNullable": true, "columnDefinition": "VARCHAR(255)"},
    {"columnName": "salary_min", "fieldName": "salarymin", "javaType": "BigDecimal", "isPrimaryKey": false, "isNullable": true, "columnDefinition": "DECIMAL(19,4)"}
  ],
  "hasAuditFields": true,
  "hasSoftDelete": false
}
```

Generates:
```java
package com.jobportal.entity;

@Table("job_posting")
public class JobPosting {
    @Id
    @Column("job_posting_id")
    private Long jobPostingId;

    @Column("title")
    private String title;

    @Column("salary_min")
    private BigDecimal salarymin;

    @Column("created_at")
    private LocalDateTime createdAt;

    @Column("updated_at")
    private LocalDateTime updatedAt;

    // getters, setters, constructors
}
```

### Repository Generation (R2DBC)

From repository_layer definition:
```json
{
  "entityName": "JobPosting",
  "className": "JobPostingRepository",
  "idType": "Long",
  "hasAuthorization": true,
  "singleRecordPerUser": false
}
```

Generates:
```java
package com.jobportal.repository;

public interface JobPostingRepository extends ReactiveCrudRepository<JobPosting, Long> {
    Flux<JobPosting> findByUserId(Long userId);
    Mono<JobPosting> findByIdAndUserId(Long id, Long userId);
}
```

### Service Generation

From service_layer definition with `hasAuthorization=true`, `singleRecordPerUser=true`:

Generates service methods that:
- Extract `userId` from JWT SecurityContext
- Create: Check if user already has a record → return existing or create new
- GetAll: Return only the user's single record
- Update/Delete: Verify ownership before proceeding

### Controller Generation

From controller_layer definition:

Generates:
```java
@RestController
@RequestMapping("/api/job_postings")
@CrossOrigin(origins = "*", methods = {...}, maxAge = 3600)
public class JobPostingController {

    @PostMapping
    @PreAuthorize("hasAnyRole('USER')")
    public Mono<ResponseEntity<JobPostingOutputDTO>> create(@RequestBody JobPostingInputDTO input) { ... }

    @GetMapping("/{id}")
    @PreAuthorize("hasAnyRole('USER')")
    public Mono<ResponseEntity<JobPostingOutputDTO>> getById(@PathVariable Long id) { ... }

    @GetMapping
    @PreAuthorize("hasAnyRole('USER')")
    public Mono<ResponseEntity<Page<JobPostingOutputDTO>>> getAll(
        @RequestParam(defaultValue = "0") int page,
        @RequestParam(defaultValue = "20") int size,
        @RequestParam(required = false) String sort,
        JobPostingFilterDTO filter) { ... }

    @PutMapping("/{id}")
    @PreAuthorize("hasAnyRole('USER')")
    public Mono<ResponseEntity<JobPostingOutputDTO>> update(@PathVariable Long id, @RequestBody JobPostingInputDTO input) { ... }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasAnyRole('USER')")
    public Mono<ResponseEntity<Void>> delete(@PathVariable Long id) { ... }
}
```

### DTO Generation

**Input DTO** (user fields only):
```java
public class JobPostingInputDTO {
    private String title;
    private String description;
    private BigDecimal salarymin;
    private BigDecimal salarymax;
    private String jobtype;
    private Boolean isactive;
    // getters, setters
}
```

**Output DTO** (PK + user + audit):
```java
public class JobPostingOutputDTO {
    private Long jobPostingId;
    private String title;
    private String description;
    private BigDecimal salarymin;
    private BigDecimal salarymax;
    private String jobtype;
    private Boolean isactive;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    // getters, setters
}
```

**Filter DTO** (user fields, all nullable):
```java
public class JobPostingFilterDTO {
    private String title;
    private String description;
    private BigDecimal salarymin;
    private BigDecimal salarymax;
    private String jobtype;
    private Boolean isactive;
    // getters, setters
}
```

### SQL DDL Generation

From entity_layer + entities definitions:
```sql
CREATE TABLE job_posting (
    job_posting_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    title VARCHAR(255),
    description VARCHAR(255),
    location VARCHAR(255),
    salary_min DECIMAL(19,4),
    salary_max DECIMAL(19,4),
    job_type VARCHAR(255),
    is_active BOOLEAN,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    PRIMARY KEY (job_posting_id)
);
```

---

*End of App Definition Manager Reference*
