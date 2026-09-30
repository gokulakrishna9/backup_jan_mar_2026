# swfaw — Spring WebFlux Application Writer — Complete Reference

> **Version:** 2.5.0 · **Manifest Version:** 2.5 · **Supported Manifests:** 2.2, 2.3, 2.4, 2.5

---

## 1. Overview

**swfaw** (Spring WebFlux Application Writer) is a Python code generator that creates complete, production-ready Spring WebFlux reactive applications from SQL database schemas or JSON definitions.

### What It Does

- Parses SQL schemas or JSON definitions into a `DatabaseDefinition` model
- Generates 850+ files per application: entities, DTOs, repositories, services, controllers, auth, security, admin UI, exception handling, activity tracking, AI layer, and more
- Supports 100+ tables per application
- Produces R2DBC reactive database access (not JPA)
- Generates JWT + OAuth2 authentication, document-based authorization, audit logging, admin UI

### Version History

| Version | Changes |
|---------|---------|
| 2.5.0 | Removed dynamic SQL generation from authorization layer |
| 2.4.0 | Query and filter layers for custom R2DBC queries |
| 2.3.0 | Layer definitions with application-wide configurations |
| 2.2.0 | Split definitions by layer (manifest, entities, relationships) |
| 2.1.0 | Two-phase architecture |
| 2.0.0 | Initial release |

### Architecture: Three Phases

**Phase 1:** SQL/JSON → `DatabaseDefinition` → split definition JSON files (`application_definitions/`)
**Phase 2:** Layer definition JSON files → Java source code via generators + templates
**Phase 3:** Definition-first pipeline — reads `application_definitions/<app>/` directly, supports incremental generation via dirty tracking (`StatusTracker` + `DependencyMapper`)

---

## 2. Entry Points & Scripts

### `main.py` — Legacy Single-Phase Mode

Generates a complete Spring WebFlux application from a `DatabaseDefinition` object. Contains both the legacy transformer-based path and the newer layer-definition-based path.

```
py swfaw/main.py --input <json_file> --output <output_dir>
```

**Key functions:**
- `load_database_definition(input_file)` → `DatabaseDefinition`
- `generate_application(db_def, output_dir, definitions_dir=None)` — main generation entry point
- `generate_from_transformers(db_def, dirs, package_name, all_entities)` — legacy path
- `generate_from_layer_definitions(db_def, layer_definitions, dirs, package_name, all_entities)` — v2.3+ path

### `generate_app.py` — Unified Phase 1 + Phase 2

Runs both phases in a single command. Also supports `--with-react` to chain REAW generation.

```
py swfaw/generate_app.py --input <schema.sql|json> --output <output_dir> [--phase 1|2|both] [--storage json|db|both] [--with-react] [--react-definition-only]
```

| Argument | Description |
|----------|-------------|
| `--input`, `-i` | Input SQL or JSON file (required) |
| `--output`, `-o` | Output directory (default: `../generated_application/<db_name>_<timestamp>`) |
| `--phase`, `-p` | Which phase: `1`, `2`, or `both` (default: `both`) |
| `--storage`, `-s` | Storage backend: `json`, `db`, `both` (default: `json`) |
| `--app-id` | App definition ID (for `--storage db` with `--phase 2`) |
| `--db-config` | Path to DB config file (default: `~/.swfaw/db_config.json`) |
| `--with-react` | After Phase 2, run REAW (both phases) for React frontend |
| `--react-definition-only` | After Phase 2, run only REAW Phase 1 |

### `phase1_generate_definition.py` — Phase 1 Only

Parses SQL/JSON input and saves split definition files to `application_definitions/`.

```
py swfaw/phase1_generate_definition.py --input <schema.sql|json> [--output <dir>] [--storage json|db|both]
```

**Key functions:**
- `load_or_parse_definition(input_file)` — loads JSON or parses SQL via `SQLParser`
- `save_application_definition(db_def, output_dir, storage, db_config)` — saves via `JsonStore`/`DbStore`
- `print_summary(db_def)` — prints project/table statistics

### `phase2_generate_code.py` — Phase 2 Only

Loads definitions from output directory (or database) and generates all code.

```
py swfaw/phase2_generate_code.py --output <output_dir> [--storage json|db] [--app-id <id>]
```

**Key functions:**
- `load_application_definition(output_dir)` → `DatabaseDefinition` (from split JSON files)
- `load_from_db(app_id, db_config)` → `(DatabaseDefinition, layer_definitions)`

### `phase3_definition_first.py` — Definition-First Pipeline

Reads definitions from `application_definitions/<app>/`, generates SQL DDL + Java code. Supports incremental generation via dirty tracking.

```
py swfaw/phase3_definition_first.py --app <app_name> --output <output_dir> [--full] [--skip-sql] [--skip-java] [--sql-file <name>]
```

| Argument | Description |
|----------|-------------|
| `--app`, `-a` | Application name (required) — maps to `application_definitions/<app>/` |
| `--output`, `-o` | Output directory (required) |
| `--full` | Force full regeneration (ignore dirty tracking) |
| `--skip-sql` | Skip SQL schema generation |
| `--skip-java` | Skip Java code generation |
| `--sql-file` | Output SQL filename (default: `schema.sql`) |

**Generation mode determination:**
1. `--full` flag → FULL
2. No status file exists → FULL (first run)
3. No prior `webflux_app/` directory → FULL (fallback)
4. Dirty files exist → INCREMENTAL
5. No dirty files + status file exists → nothing to do

**Full generation:** DDL + all Java code + document storage + AI layer → mark all clean
**Incremental generation:** `DependencyMapper.resolve_affected_outputs()` → `IncrementalGenerator.regenerate_affected()` → mark dirty files clean

### `convert_sql.py` — SQL to JSON Converter (Legacy)

Converts MySQL SQL schemas to `application_definition.json` format.

```
py swfaw/convert_sql.py <sql_file> [--output <json_file>]
```

Extracts: database name, table names, column definitions, primary keys, foreign keys. Skips `created_by_id` and `updated_by_id` columns.

---

## 3. Generation Pipeline

### Phase 1: SQL → DatabaseDefinition → Layer Definition JSON Files

```
SQL file
  ↓ SQLParser.parse_file()
DatabaseDefinition (Pydantic model)
  ↓ split_definition() / generate_all_layer_definitions()
application_definitions/<app>/
  ├── webflux_manifest.json
  ├── webflux_project_metadata.json
  ├── webflux_entities.json
  ├── webflux_relationships.json
  ├── webflux_entity_layer.json
  ├── webflux_repository_layer.json
  ├── webflux_service_layer.json
  ├── webflux_controller_layer.json
  ├── webflux_dto_layer.json
  ├── webflux_query_layer.json
  ├── webflux_filter_layer.json
  ├── webflux_security_layer.json
  ├── webflux_config_layer.json
  ├── webflux_exception_layer.json
  ├── webflux_audit_logging_layer.json
  ├── webflux_authorization_layer.json
  ├── webflux_group_definition_layer.json
  ├── webflux_custom_queries_layer.json
  ├── webflux_document_storage_layer.json  (optional)
  └── webflux_ai_layer.json               (optional)
```

### Phase 2: Layer Definitions → Java Source Code

```
Layer definition JSON files
  ↓ load_layer_definitions_if_exist() or load_all_definitions()
In-memory layer objects (EntityLayerObject, DTOLayerObject, etc.)
  ↓ Generators (EntityGenerator, DTOGenerator, etc.)
Java source files via Python string templates
  ↓ write_file()
output_dir/webflux_app/src/main/java/...
```

Two code paths in `main.py`:
- **Layer definitions path** (v2.3+): Reads `webflux_*_layer.json` files, constructs layer objects, passes to generators
- **Transformer path** (legacy): Uses `EntityTransformer`, `DTOTransformer`, etc. to derive layer objects from `DatabaseDefinition`

### Phase 3: Definition-First with Incremental Generation

```
application_definitions/<app>/
  ↓ load_all_definitions() → DefinitionBundle
  ↓ StatusTracker.get_dirty_files()
  ↓ DependencyMapper.resolve_affected_outputs()
  ↓ IncrementalGenerator.regenerate_affected() (or full via generate_application())
generated_application/<app>/
  ├── schema.sql
  └── webflux_app/
```

### Dirty/Clean Tracking

- `StatusTracker` (from `app_def_manager`) maintains a status file in the definitions directory
- Each definition JSON file is tracked as dirty or clean
- When a definition file is modified (via App Def Manager or manually), it's marked dirty
- Phase 3 reads dirty files, resolves affected outputs via `DependencyMapper`, regenerates only those files
- After generation, processed files are marked clean

---

## 4. Data Models (`swfaw/models/`)

### `database_definition.py` — Input Models

#### `DatabaseConfig`
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `type` | `str` | `"mysql"` | Database type |
| `host` | `str` | `"localhost"` | Database host |
| `port` | `int` | `3306` | Database port |
| `name` | `str` | — | Database name (required) |
| `url` | `Optional[str]` | `None` | Full JDBC URL (optional) |
| `username` | `str` | `"root"` | Database username |
| `password` | `str` | `"password"` | Database password |

#### `ProjectMetadata`
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | — | Project name (required) |
| `applicationName` | `str` | — | Display name (required) |
| `groupId` | `str` | `"com.example"` | Maven group ID |
| `artifactId` | `str` | — | Maven artifact ID (required) |
| `version` | `str` | `"1.0.0"` | Project version |
| `port` | `int` | `8081` | Server port |
| `sqlFileName` | `Optional[str]` | `None` | Original SQL file name |
| `dateCreated` | `Optional[str]` | `None` | ISO date string |
| `database` | `DatabaseConfig` | — | Database configuration (required) |

#### `Column`
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | — | Column name (required) |
| `type` | `str` | — | SQL type (required) |
| `primaryKey` | `bool` | `False` | Is primary key |
| `nullable` | `bool` | `True` | Is nullable |
| `foreignKey` | `Optional[dict]` | `None` | Foreign key reference |
| `unique` | `bool` | `False` | Has unique constraint |
| `defaultValue` | `Optional[str]` | `None` | Default value |

#### `Relationship`
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `type` | `str` | — | OneToMany, ManyToOne, ManyToMany (required) |
| `targetTable` | `str` | — | Target table name (required) |
| `foreignKey` | `Optional[str]` | `None` | Foreign key column |
| `joinTable` | `Optional[str]` | `None` | Join table for ManyToMany |

#### `Table`
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | — | Table name (required) |
| `columns` | `List[Column]` | — | Column definitions (required) |
| `relationships` | `List[Relationship]` | `[]` | Relationships |

#### `DatabaseDefinition`
| Field | Type | Description |
|-------|------|-------------|
| `projectMetadata` | `ProjectMetadata` | Project configuration |
| `tables` | `List[Table]` | All table definitions |

### `layer_objects.py` — Generator Input Models

#### `Field`
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `columnName` | `str` | — | Database column name |
| `fieldName` | `str` | — | Java field name |
| `javaType` | `str` | — | Java type (String, Long, etc.) |
| `isPrimaryKey` | `bool` | `False` | Is primary key |
| `isNullable` | `bool` | `True` | Is nullable |
| `columnDefinition` | `str` | `""` | Column definition string |

#### `EntityLayerObject`
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `tableName` | `str` | — | Database table name |
| `className` | `str` | — | Java class name |
| `packageName` | `str` | — | Java package |
| `fields` | `List[Field]` | — | Entity fields |
| `isRootEntity` | `bool` | — | Is root entity (no parent FK) |
| `parentEntity` | `Optional[str]` | `None` | Parent entity name |
| `hasPublicFlag` | `bool` | — | Has `is_public` column |
| `hasAuditFields` | `bool` | `True` | Has created_at/updated_at |
| `hasSoftDelete` | `bool` | `True` | Has deleted_at |

#### `DTOLayerObject`
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `entityName` | `str` | — | Source entity name |
| `className` | `str` | — | DTO class name |
| `packageName` | `str` | — | Java package |
| `fields` | `List[Field]` | — | DTO fields |
| `dtoType` | `str` | — | `Input`, `Output`, or `Filter` |
| `isRootEntity` | `bool` | — | Is root entity |
| `fieldConfigs` | `List[dict]` | `[]` | Field-level configs (validation, format) |
| `customValidators` | `List[dict]` | `[]` | Custom validator classes |
| `excludeSensitiveFields` | `List[str]` | `[]` | Fields excluded from Output DTOs |
| `includeRelationships` | `bool` | `False` | Include related entities in Output |

#### `RepositoryLayerObject`
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `entityName` | `str` | — | Entity name |
| `className` | `str` | — | Repository class name |
| `packageName` | `str` | — | Java package |
| `idType` | `str` | — | Primary key Java type |
| `hasCustomQueries` | `bool` | `False` | Has custom query methods |
| `customQueries` | `List[dict]` | `[]` | Custom query definitions |
| `hasSoftDelete` | `bool` | `False` | Soft delete support |
| `hasAuthorization` | `bool` | `False` | Authorization checks |
| `singleRecordPerUser` | `bool` | `False` | One record per user |
| `tableName` | `Optional[str]` | `None` | Database table name |
| `idColumn` | `Optional[str]` | `None` | Primary key column name |

#### `ServiceLayerObject`
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `entityName` | `str` | — | Entity name |
| `className` | `str` | — | Service class name |
| `packageName` | `str` | — | Java package |
| `repositoryName` | `str` | — | Repository bean name |
| `isRootEntity` | `bool` | — | Is root entity |
| `hasAuthorization` | `bool` | — | Authorization enabled |
| `singleRecordPerUser` | `bool` | `False` | One record per user |

#### `ControllerLayerObject`
| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `entityName` | `str` | — | Entity name |
| `className` | `str` | — | Controller class name |
| `packageName` | `str` | — | Java package |
| `serviceName` | `str` | — | Service bean name |
| `basePath` | `str` | — | REST base path |
| `isRootEntity` | `bool` | — | Is root entity |
| `endpoints` | `dict` | `{}` | Endpoint configs (create, getById, getAll, update, delete) |
| `customEndpoints` | `List[dict]` | `[]` | Custom endpoint definitions |
| `corsConfig` | `dict` | `{}` | CORS configuration |
| `singleRecordPerUser` | `bool` | `False` | One record per user |

#### Other Layer Objects

| Class | Purpose |
|-------|---------|
| `AuthorizationServiceLayerObject` | Authorization service config (`packageName`, `rootEntities`) |
| `SecurityConfigLayerObject` | Security config (`packageName`, `jwtSecret`, `jwtExpiration`) |
| `JWTAuthenticationLayerObject` | JWT config (`jwtSecret`, `jwtExpiration`, `refreshExpiration`) |
| `ApplicationConfigLayerObject` | App config (`projectName`, `groupId`, `port`, database settings) |
| `POMLayerObject` | POM config (`groupId`, `artifactId`, `version`, `javaVersion`, `springBootVersion`) |
| `TestLayerObject` | Test config (`entityName`, `className`, `serviceName`, `isRootEntity`) |
| `QueryParameter` | Query param (`name`, `type`, `required`, `defaultValue`) |
| `QueryJoin` | Query join (`type`, `table`, `alias`, `on`) |
| `CustomQuery` | Custom query (`name`, `description`, `returnType`, `select`, `from_`, `joins`, `where`, `groupBy`, `having`, `orderBy`, `pagination`, `parameters`, `authorization`) |
| `QueryLayerObject` | Per-entity queries (`entityName`, `queries`, `packageName`) |
| `FilterField` | Filter field (`name`, `type`, `operators[]`) |
| `FilterLayerObject` | Per-entity filters (`entityName`, `fields`, `packageName`) |

---

## 5. Generators (`swfaw/generators/`)

### Core Generators

| Generator | File | Produces |
|-----------|------|----------|
| `EntityGenerator` | `entity_generator.py` | R2DBC entity classes with `@Table`, `@Column`, `@Id` annotations, audit fields, soft delete |
| `DTOGenerator` | `dto_generator.py` | Input/Output/Filter DTOs with Jakarta validation annotations (`@NotNull`, `@Size`, `@Email`, etc.) |
| `RepositoryGenerator` | `repository_generator.py` | `ReactiveCrudRepository` interfaces with custom `@Query` methods, soft delete filters, authorization checks |
| `ServiceGenerator` | `service_generator.py` | `@Service` classes with CRUD operations, authorization integration, `@Transactional`, audit field population |
| `ControllerGenerator` | `controller_generator.py` | `@RestController` classes with CRUD endpoints, CORS config, rate limiting, Swagger annotations |
| `DDLGenerator` | `ddl_generator.py` | SQL `CREATE TABLE` statements from entity layer definitions |
| `POMGenerator` | `pom_generator.py` | Maven `pom.xml` with Spring Boot, R2DBC, security, Swagger, Thymeleaf dependencies |
| `ConfigGenerator` | `config_generator.py` | `application.yml` configuration (server, database, R2DBC pool, logging) |
| `IncrementalGenerator` | `incremental_generator.py` | Targeted regeneration of only affected files based on `AffectedOutputs` from `DependencyMapper` |
| `TestGenerator` | `test_generator.py` | Test class stubs |

### Auth/Security Generators

| Generator | File | Produces |
|-----------|------|----------|
| `SecurityGenerator` | `security_generator.py` | `SecurityConfig.java`, `PasswordEncoderConfig.java`, `WebSecurityProperties.java` |
| `JWTGenerator` | `jwt_generator.py` | `JwtConfig.java`, `JwtService.java`, `JwtAuthenticationFilter.java`, `AuthController.java`, `AuthService.java` |
| `OAuth2Generator` | `oauth2_generator.py` | `OAuth2Provider.java`, `OAuth2LinkedAccount.java` entities + repositories + `OAuth2Service.java` + `OAuth2Controller.java` |
| `AuthEntityGenerator` | `auth_entity_generator.py` | Auth entities: `SystemConfig`, `AuthUser`, `AccessAuditLog`, `UserRole`, `RecordOwner`, `QueryGroup`, `QueryGroupQuery`, `QueryGroupMember`, `QueryGroupRecord` |
| `AuthRepositoryGenerator` | `auth_repository_generator.py` | Repositories for all auth entities (9 repositories) |
| `AuthServiceGenerator` | `auth_service_generator.py` | `AuthService.java` with login, registration, password management |
| `AuthorizationServiceGenerator` | `authorization_service_generator.py` | `RoleAuthorizationService.java`, `AuthorizationWebFilter.java`, `AuthorizationAspect.java`, `@EntityTable`, `@TableAccess`, `@QueryAccess` annotations |
| `AuthorizationGenerator` | `authorization_generator.py` | Authorization-related code |
| `PermissionsGenerator` | `permissions_generator.py` | Permission constants and helpers |
| `SetupGenerator` | `setup_generator.py` | `/setup` endpoint for initial super user creation |
| `AuthSchemaGenerator` | `auth_schema_generator.py` | `auth-schema.sql` DDL for all auth tables |

### Advanced Feature Generators

| Generator | File | Produces |
|-----------|------|----------|
| `AdminUIGenerator` | `admin_ui_generator.py` | `AdminService.java`, `AdminController.java`, 8 Thymeleaf HTML templates (dashboard, groups, users, document groups, forms, details) |
| `AuditLoggingGenerator` | `audit_logging_generator.py` | `AuditLoggingService.java`, `AuditController.java` |
| `ActivityTrackingGenerator` | `activity_tracking_generator.py` | `CrudActivityLog`, `DeletedRecord`, `LoginActivityLog`, `GrantActivityLog` entities + repositories + `ActivityTrackingService.java` + `ActivityTrackingController.java` |
| `ActivityTrackingSchemaGenerator` | `activity_tracking_schema_generator.py` | `activity-tracking-schema.sql` DDL |
| `ExceptionGenerator` | `exception_generator.py` | `GlobalExceptionHandler.java`, `ErrorResponse.java`, `ValidationErrorResponse.java`, `EntityNotFoundException.java`, `AccessDeniedException.java`, `DuplicateEntityException.java`, `PageResponse.java` |
| `TestDataGenerator` | `test_data_generator.py` | `test-data.json` with sample data |
| `CustomQueryGenerator` | `custom_query_generator.py` | Custom R2DBC query methods |
| `FileStorageGenerator` | `file_storage_generator.py` | File storage service/controller for document storage layer |
| `JsonColumnGenerator` | `json_column_generator.py` | JSON column converters and document collection classes |
| `DocumentStorageSchemaGenerator` | `document_storage_schema_generator.py` | DDL for document storage tables |

### AI Layer Generators (24 Sub-Generators + Coordinator + Validator)

The AI layer is coordinated by `AiGenerator` which orchestrates 24 sub-generators in dependency order. All AI generators use Jinja2 templates from `templates/ai/`.

| # | Generator | File | Produces |
|---|-----------|------|----------|
| — | `AiGenerator` (coordinator) | `ai_generator.py` | Orchestrates all 24 sub-generators, validates, writes files |
| — | `AiValidator` | `ai_validator.py` | Validates AI layer definition, returns warnings |
| 1 | `ProviderGenerator` | `ai_provider_generator.py` | `ChatClient`/`EmbeddingModel` Spring beans per provider |
| 2 | `PromptGenerator` | `ai_prompt_generator.py` | `PromptTemplateEngine` service |
| 3 | `ConversationGenerator` | `ai_conversation_generator.py` | Chat session/message entities, repositories, services |
| 4 | `EntityAiGenerator` | `ai_entity_generator.py` | Per-entity AI services and controllers (summarize, classify, extract, etc.) |
| 5 | `StandaloneAiGenerator` | `ai_standalone_generator.py` | Standalone AI operation services/controllers (not tied to entities) |
| 6 | `TypedResponseGenerator` | `ai_typed_response_generator.py` | Typed response DTOs for structured AI outputs |
| 7 | `VectorStoreGenerator` | `ai_vectorstore_generator.py` | Vector store implementations (PGVector, Redis, etc.) |
| 8 | `RagGenerator` | `ai_rag_generator.py` | RAG services — semantic search and heuristic retrieval |
| 9 | `EvaluatorGenerator` | `ai_evaluator_generator.py` | AI evaluation pipeline (quality, relevance, safety) |
| 10 | `DocumentIngestionGenerator` | `ai_document_ingestion_generator.py` | Document upload, extraction, chunking pipeline |
| 11 | `DocumentProcessingGenerator` | `ai_document_processing_generator.py` | LLM-powered document processing tasks |
| 12 | `OrchestratorGenerator` | `ai_orchestrator_generator.py` | AI orchestrator service for multi-step workflows |
| 13 | `ToolFunctionGenerator` | `ai_tool_generator.py` | `@Tool` annotated functions for Spring AI function calling |
| 14 | `McpGenerator` | `ai_mcp_generator.py` | MCP (Model Context Protocol) client services |
| 15 | `SecurityGenerator` (AI) | `ai_security_generator.py` | Prompt security, input sanitization, content moderation |
| 16 | `ExceptionGenerator` (AI) | `ai_exception_generator.py` | AI-specific exception handler |
| 17 | `ObservabilityGenerator` | `ai_observability_generator.py` | AI metrics, health checks, Grafana dashboards |
| 18 | `TokenBudgetGenerator` | `ai_token_budget_generator.py` | Token usage tracking and budget enforcement |
| 19 | `AuditGenerator` (AI) | `ai_audit_generator.py` | AI audit logging (prompts, responses, costs) |
| 20 | `SessionCleanupGenerator` | `ai_session_cleanup_generator.py` | Chat session cleanup scheduler, topic summarization |
| 21 | `AiDdlGenerator` | `ai_ddl_generator.py` | `ai_tables.sql` DDL for AI-related database tables |
| 22 | `AiDtoGenerator` | `ai_dto_generator.py` | Shared AI DTOs (request/response objects) |
| 23 | `AiPomGenerator` | `ai_pom_generator.py` | `ai_dependencies.xml` — Maven dependencies for Spring AI |
| 24 | `AiAppPropertiesGenerator` | `ai_app_properties_generator.py` | `ai_application.properties` — AI-specific configuration |

**AiGenerator orchestration order:** Providers → Prompt → Conversation → EntityAi → StandaloneAi → TypedResponse → VectorStore → RAG → Evaluator → DocumentIngestion → DocumentProcessing → Orchestrator → ToolFunction → MCP → Security → Exception → Observability → TokenBudget → Audit → SessionCleanup → DDL → DTO → POM → AppProperties

**AI layer definition sections consumed:**
- `providers[]` — AI model providers
- `entityCapabilities[]` — per-entity AI features
- `standaloneOperations[]` — standalone AI operations
- `assistants[]` — chat assistants
- `ragSources[]` — RAG data sources
- `evaluators[]` — evaluation configs
- `vectorStore` — vector store config
- `documentIngestion` — document ingestion config
- `documentProcessing` — document processing config
- `orchestrator` — orchestrator config
- `mcpServers[]` — MCP server configs
- `observability` — metrics/health config
- `tokenBudget` — token budget config
- `chatSessionCleanup` — session cleanup config
- `auditLog` — AI audit config

---

## 6. Templates (`swfaw/templates/`)

### Core Templates (Python String Templates)

Templates are Python modules containing string template constants used by generators.

| Template File | Used By | Content |
|---------------|---------|---------|
| `entity_templates.py` | `EntityGenerator` | R2DBC entity class structure |
| `dto_templates.py` | `DTOGenerator` | Input/Output/Filter DTO classes |
| `repository_templates.py` | `RepositoryGenerator` | Repository interface templates |
| `service_templates.py` | `ServiceGenerator` | Service class with CRUD logic |
| `controller_templates.py` | `ControllerGenerator` | REST controller endpoints |
| `config_templates.py` | `ConfigGenerator` | `application.yml` template |
| `pom_templates.py` | `POMGenerator` | Maven POM XML |
| `security_templates.py` | `SecurityGenerator` | Security configuration classes |
| `jwt_templates.py` | `JWTGenerator` | JWT components |
| `auth_entity_templates.py` | `AuthEntityGenerator` | Auth entity classes |
| `auth_repository_templates.py` | `AuthRepositoryGenerator` | Auth repository interfaces |
| `auth_service_templates.py` | `AuthServiceGenerator` | Auth service class |
| `auth_schema_templates.py` | `AuthSchemaGenerator` | Auth SQL schema |
| `auth_schema_template.sql` | `AuthSchemaGenerator` | Raw SQL template |
| `authorization_service_templates.py` | `AuthorizationServiceGenerator` | Authorization service/aspect |
| `authorization_templates.py` | `AuthorizationGenerator` | Authorization code |
| `permissions_templates.py` | `PermissionsGenerator` | Permission constants |
| `setup_templates.py` | `SetupGenerator` | Setup endpoint |
| `oauth2_templates.py` | `OAuth2Generator` | OAuth2 components |
| `admin_ui_templates.py` | `AdminUIGenerator` | Admin service/controller |
| `admin_html_templates.py` | `AdminUIGenerator` | Thymeleaf HTML pages |
| `audit_logging_templates.py` | `AuditLoggingGenerator` | Audit logging components |
| `activity_tracking_templates.py` | `ActivityTrackingGenerator` | Activity tracking components |
| `exception_templates.py` | `ExceptionGenerator` | Exception classes |
| `test_templates.py` | `TestGenerator` | Test class stubs |
| `custom_query_templates.py` | `CustomQueryGenerator` | Custom query methods |
| `sql_builder.py` | `DDLGenerator` | SQL DDL builder utilities |
| `file_storage_templates.py` | `FileStorageGenerator` | File storage components |
| `json_column_templates.py` | `JsonColumnGenerator` | JSON column converters |
| `document_collection_templates.py` | — | Document collection templates |
| `document_storage_schema_templates.py` | `DocumentStorageSchemaGenerator` | Document storage DDL |

### AI Templates (Jinja2 — `templates/ai/`)

AI generators use Jinja2 templates organized in subdirectories under `templates/ai/`:

```
templates/ai/
├── audit/          — AI audit logging templates
├── budget/         — Token budget templates
├── config/         — AI configuration templates
├── controller/     — AI controller templates
├── ddl/            — AI DDL SQL templates
├── dto/            — AI DTO templates
├── entity/         — AI entity templates
├── evaluator/      — Evaluation pipeline templates
├── ingestion/      — Document ingestion templates
├── mcp/            — MCP client templates
├── observability/  — Metrics/health/Grafana templates
├── orchestrator/   — AI orchestrator templates
├── pom/            — AI Maven dependency templates
├── processing/     — Document processing templates
├── provider/       — AI provider bean templates
├── rag/            — RAG service templates
├── repository/     — AI repository templates
├── scheduler/      — Session cleanup scheduler templates
├── service/        — AI service templates
├── tools/          — @Tool function templates
└── vectorstore/    — Vector store templates
```

**Jinja2 environment configuration:**
- `loader`: `FileSystemLoader` pointing to `swfaw/templates/`
- `keep_trailing_newline`: `True`
- `trim_blocks`: `True`
- `lstrip_blocks`: `True`

**Template rendering pattern:** Each AI sub-generator receives the `jinja_env`, loads its templates via `jinja_env.get_template("ai/<subdir>/<template>.java.j2")`, renders with context variables, and returns `(filepath, content)` tuples.

---

## 7. Utilities (`swfaw/utils/`)

### `definition_loader.py` — Definition Loading & Validation

**`DefinitionBundle`** (dataclass) — Container for all loaded definition data:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `app_name` | `str` | Yes | Application name (directory name) |
| `definitions_dir` | `Path` | Yes | Path to definitions directory |
| `manifest` | `dict` | Yes | Manifest JSON |
| `project_metadata` | `dict` | Yes | Project metadata JSON |
| `entity_layer` | `dict` | Yes | Entity layer JSON |
| `entities` | `dict` | Yes | Entities JSON |
| `relationships` | `dict` | Yes | Relationships JSON |
| `repository_layer` | `dict` | Yes | Repository layer JSON |
| `service_layer` | `dict` | Yes | Service layer JSON |
| `controller_layer` | `dict` | Yes | Controller layer JSON |
| `dto_layer` | `dict` | Yes | DTO layer JSON |
| `query_layer` | `dict | None` | No | Query layer JSON |
| `filter_layer` | `dict | None` | No | Filter layer JSON |
| `security_layer` | `dict | None` | No | Security layer JSON |
| `config_layer` | `dict | None` | No | Config layer JSON |
| `custom_queries_layer` | `dict | None` | No | Custom queries JSON |
| `group_definition_layer` | `dict | None` | No | Group definition JSON |
| `authorization_layer` | `dict | None` | No | Authorization JSON |
| `audit_logging_layer` | `dict | None` | No | Audit logging JSON |
| `exception_layer` | `dict | None` | No | Exception layer JSON |
| `document_storage_layer` | `dict | None` | No | Document storage JSON |
| `ai_layer` | `dict | None` | No | AI layer JSON |

**Required file keys:** `project_metadata`, `entities`, `relationships`, `entity_layer`, `repository_layer`, `service_layer`, `controller_layer`, `dto_layer`

**Optional file keys:** `query_layer`, `filter_layer`, `security_layer`, `config_layer`, `custom_queries_layer`, `group_definition_layer`, `authorization_layer`, `audit_logging_layer`, `exception_layer`, `document_storage_layer`, `ai_layer`

**Key functions:**
- `load_all_definitions(definitions_dir)` → `DefinitionBundle` — loads manifest, validates version, loads all required + optional files, validates entity_layer structure
- `reconstruct_database_definition(bundle)` → `DatabaseDefinition` — reconstructs from bundle for Phase 2 compatibility

### `dependency_mapper.py` — Incremental Generation Mapping

**`AffectedOutputs`** (dataclass):
- `regenerate_sql: bool` — whether SQL DDL needs regeneration
- `affected_entities: set[str]` — entity classNames needing regeneration
- `affected_file_types: dict[str, set[str]]` — per-entity file types to regenerate

**`DependencyMapper`** class:
- `DEPENDENCY_MAP` — maps definition files to affected generated file types (see Section 12)
- `resolve_affected_outputs(dirty_files, bundle)` → `AffectedOutputs`
- `get_generated_file_paths(entity_name, file_type, dirs, package_name)` → `list[Path]`

### `file_writer.py` — File System Operations

- `create_directory_structure(base_path, package_name)` → `dict` — creates Maven directory tree, returns path dict with keys: `base`, `src_main_java`, `src_main_resources`, `entity`, `dto`, `model`, `repository`, `service`, `controller`, `security`, `auth`, `config`, `exception`, `templates`, `templates_admin`, `static`, `test_service`, `test_controller`
- `write_file(file_path, content, base_path=None)` — writes text file, creates parent dirs
- `write_binary_file(file_path, content, base_path=None)` — writes binary file
- `get_java_file_path(package_name, layer, class_name)` → relative path string
- `get_test_file_path(package_name, layer, class_name)` → relative path string

### `string_utils.py` — Naming Conversions

- `to_pascal_case(text)` — `ems_course` → `Course`, `user_profile` → `UserProfile` (strips `ems_` prefix)
- `to_camel_case(text)` — `course_id` → `courseId`
- `map_sql_type_to_java(sql_type)` — maps SQL types to Java types (BIGINT→Long, VARCHAR→String, DATETIME→LocalDateTime, DECIMAL→BigDecimal, etc.)
- `pluralize(word)` — simple English pluralization
- `singularize(word)` — simple English singularization

### `layer_definition_generator.py` — Layer Definition Generation

Generates all layer definition JSON files from a `DatabaseDefinition`. Used by Phase 1.

**Per-entity layer generators:**
- `generate_entity_layer_definition(db_def)` — entity layer with fields, audit, soft delete
- `generate_repository_layer_definition(db_def)` — repository layer with caching placeholders
- `generate_service_layer_definition(db_def)` — service layer with authorization, transaction config
- `generate_controller_layer_definition(db_def)` — controller layer with endpoints, CORS
- `generate_dto_layer_definition(db_def)` — Input/Output/Filter DTOs with validation rules
- `generate_query_layer_definition(db_def)` — custom query definitions
- `generate_filter_layer_definition(db_def)` — filter field definitions

**Application-wide layer generators:**
- `generate_security_layer_definition(db_def)` — JWT, OAuth2, password policy, CORS, CSRF, rate limiting
- `generate_config_layer_definition(db_def)` — project, server, database, logging, features (Swagger, actuator, caching, email)
- `generate_exception_layer_definition(db_def)` — custom exceptions, error response format, global handling
- `generate_audit_logging_layer_definition(db_def)` — audit events (auth, data access, authorization, system), storage, filtering
- `generate_authorization_layer_definition(db_def)` — authorization configuration
- `generate_group_definition_layer(db_def)` — group definition configuration
- `generate_custom_queries_layer_definition(db_def)` — custom queries configuration

**Orchestrator:**
- `generate_all_layer_definitions(db_def, output_dir)` → `dict[str, str]` — generates all layers, writes to `application_definitions/`

### `definition_splitter.py` — Definition Splitting & Loading

- `split_definition(db_def, output_dir)` — splits `DatabaseDefinition` into multiple JSON files + generates layer definitions + writes manifest
- `load_split_definition(output_dir)` → `DatabaseDefinition` — loads from split files, reconstructs tables with relationships
- `load_layer_definitions_if_exist(output_dir)` → `dict | None` — loads layer definition files if v2.3+ manifest exists

---

## 8. Managers (`swfaw/managers/`)

JSON-based CRUD managers for manipulating application definition files.

### `definition_manager.py` — `DefinitionManager`

Core manager that loads/saves `DatabaseDefinition`. Supports optional `DefinitionStore` backend (JSON or DB).

| Method | Description |
|--------|-------------|
| `load(identifier=None)` | Load definition from JSON files or store |
| `save()` | Save current definition |
| `get_definition()` | Get loaded `DatabaseDefinition` |
| `get_project_metadata()` | Get `ProjectMetadata` |
| `update_project_metadata(**kwargs)` | Update metadata fields |
| `get_database_config()` | Get `DatabaseConfig` |
| `update_database_config(**kwargs)` | Update database fields |
| `list_tables()` | List all table names |
| `get_table(table_name)` | Get `Table` by name |
| `table_exists(table_name)` | Check if table exists |
| `get_statistics()` | Get project statistics |

### `entity_manager.py` — `EntityManager`

CRUD operations on entities (tables).

| Method | Description |
|--------|-------------|
| `add_entity(table_name, columns=None)` | Add new table (default: id BIGINT PK) |
| `remove_entity(table_name)` | Remove table + clean up relationships |
| `update_entity(table_name, new_name=None)` | Rename table + update relationship references |
| `get_entity(table_name)` | Get `Table` object |
| `list_entities()` | List all table names |
| `entity_exists(table_name)` | Check existence |
| `get_entity_details(table_name)` | Get full details dict |

### `field_manager.py` — `FieldManager`

CRUD operations on fields (columns) within entities.

| Method | Description |
|--------|-------------|
| `add_field(table_name, field_name, field_type, ...)` | Add column |
| `remove_field(table_name, field_name)` | Remove column |
| `update_field(table_name, field_name, ...)` | Update column properties |
| `get_field(table_name, field_name)` | Get `Column` object |
| `list_fields(table_name)` | List field names |
| `field_exists(table_name, field_name)` | Check existence |
| `get_field_details(table_name, field_name)` | Get details dict |
| `get_primary_keys(table_name)` | List PK field names |

### `relationship_manager.py` — `RelationshipManager`

CRUD operations on entity relationships.

| Method | Description |
|--------|-------------|
| `add_relationship(source, target, type, fk, ref_col)` | Add relationship |
| `remove_relationship(source, target, fk=None)` | Remove relationship(s) |
| `update_relationship(source, target, fk, ...)` | Update relationship |
| `get_relationships(table_name)` | Get all relationships for table |
| `get_relationship(source, target, fk)` | Get specific relationship |
| `list_relationships(table_name)` | List with details |
| `relationship_exists(source, target, fk)` | Check existence |
| `get_incoming_relationships(table_name)` | Get relationships pointing to this table |

### `query_manager.py` — `QueryManager`

CRUD operations on custom query definitions. Wraps `LayerManager`.

| Method | Description |
|--------|-------------|
| `add_query(entity_name, query_def)` | Add custom query |
| `remove_query(entity_name, query_name)` | Remove query |
| `get_query(entity_name, query_name)` | Get query definition |
| `update_query(entity_name, query_name, updates)` | Update query |
| `list_queries(entity_name)` | List queries for entity |
| `list_all_queries()` | List all queries for all entities |

### `filter_manager.py` — `FilterManager`

CRUD operations on filter definitions. Wraps `LayerManager`.

| Method | Description |
|--------|-------------|
| `add_filter_field(entity_name, field_def)` | Add filter field |
| `remove_filter_field(entity_name, field_name)` | Remove filter field |
| `get_filter_field(entity_name, field_name)` | Get filter field |
| `update_filter_field(entity_name, field_name, updates)` | Update filter field |
| `list_filter_fields(entity_name)` | List filter fields for entity |
| `list_all_filters()` | List all filters |

### `layer_manager.py` — `LayerManager`

Generic JSON CRUD manager for any layer definition file. Supports dot-notation paths and array indexing.

**Layer file aliases:**

| Alias | File |
|-------|------|
| `entity` | `webflux_entity_layer.json` |
| `repository` | `webflux_repository_layer.json` |
| `service` | `webflux_service_layer.json` |
| `controller` | `webflux_controller_layer.json` |
| `dto` | `webflux_dto_layer.json` |
| `security` | `webflux_security_layer.json` |
| `config` | `webflux_config_layer.json` |
| `exception` | `webflux_exception_layer.json` |
| `audit` | `webflux_audit_logging_layer.json` |
| `authorization` | `webflux_authorization_layer.json` |
| `custom_queries` | `webflux_custom_queries_layer.json` |
| `group_definition` | `webflux_group_definition_layer.json` |
| `manifest` | `webflux_manifest.json` |
| `project_metadata` | `webflux_project_metadata.json` |
| `entities` | `webflux_entities.json` |
| `relationships` | `webflux_relationships.json` |

| Method | Description |
|--------|-------------|
| `get(file_name, path=None)` | Get data at dot-notation path |
| `set(file_name, path, value)` | Set value at path |
| `update(file_name, path, updates)` | Update multiple fields |
| `delete(file_name, path)` | Delete value at path |
| `append(file_name, path, value)` | Append to array |
| `find(file_name, path, predicate)` | Find item in array |
| `filter(file_name, path, predicate)` | Filter array items |
| `exists(file_name, path=None)` | Check file/path existence |
| `list_files()` | List all JSON files |
| `list_layers()` | List all layer aliases |

---

## 9. Database Managers (`swfaw/db_managers/`)

MySQL-based CRUD managers that mirror the JSON managers API but operate on the `swfaw_definition_store` database. Used when `--storage db` or `--storage both` is specified.

### `db_connection.py` — `DbConnection`

MySQL connection management with connection pooling.

- Config file: `~/.swfaw/db_config.json`
- Default database: `swfaw_definition_store`
- Default pool size: 5
- Methods: `fetch_all()`, `fetch_one()`, `execute()`, `insert()`, `execute_many()`, `execute_transaction()`, `table_exists()`

### All 14 Database Manager Modules

| Module | Class | Description |
|--------|-------|-------------|
| `db_connection.py` | `DbConnection` | Connection pooling, query helpers, transaction support |
| `db_store_manager.py` | `DbStoreManager` | Top-level app definition CRUD (save/load/list/delete) |
| `db_entity_manager.py` | `DbEntityManager` | Entity (table) CRUD in database |
| `db_relationship_manager.py` | `DbRelationshipManager` | Relationship CRUD in database |
| `db_layer_manager.py` | `DbLayerManager` | Generic layer definition CRUD in database |
| `db_security_manager.py` | `DbSecurityManager` | Security layer operations |
| `db_config_manager.py` | `DbConfigManager` | Config layer operations |
| `db_exception_manager.py` | `DbExceptionManager` | Exception layer operations |
| `db_audit_manager.py` | `DbAuditManager` | Audit logging layer operations |
| `db_authorization_manager.py` | `DbAuthorizationManager` | Authorization layer operations |
| `db_group_manager.py` | `DbGroupManager` | Group definition operations |
| `db_query_manager.py` | `DbQueryManager` | Query layer operations |
| `db_filter_manager.py` | `DbFilterManager` | Filter layer operations |
| `db_dto_manager.py` | `DbDtoManager` | DTO layer operations |

---

## 10. Transformers (`swfaw/transformers/`)

Transformers convert `DatabaseDefinition` models (tables, columns) into layer objects consumed by generators. Used in the legacy transformer-based code path and by `layer_definition_generator.py` to produce initial layer definitions.

| Transformer | File | Input → Output |
|-------------|------|----------------|
| `EntityTransformer` | `entity_transformer.py` | `Table` + `package_name` → `EntityLayerObject` |
| `DTOTransformer` | `dto_transformer.py` | `EntityLayerObject` + `dto_type` → `DTOLayerObject` |
| `RepositoryTransformer` | `repository_transformer.py` | `EntityLayerObject` → `RepositoryLayerObject` |
| `ServiceTransformer` | `service_transformer.py` | `EntityLayerObject` → `ServiceLayerObject` |
| `ControllerTransformer` | `controller_transformer.py` | `EntityLayerObject` → `ControllerLayerObject` |
| `AuthorizationTransformer` | `authorization_transformer.py` | Authorization-related transformations |
| `SecurityTransformer` | `security_transformer.py` | `package_name` → `SecurityConfigLayerObject` |
| `JWTTransformer` | `jwt_transformer.py` | `package_name` → `JWTAuthenticationLayerObject` |
| `ConfigTransformer` | `config_transformer.py` | `DatabaseDefinition` → `ApplicationConfigLayerObject` |
| `POMTransformer` | `pom_transformer.py` | `DatabaseDefinition` → `POMLayerObject` |
| `TestTransformer` | `test_transformer.py` | `EntityLayerObject` → `TestLayerObject` |
| `QueryTransformer` | `query_transformer.py` | Entity + query config → `QueryLayerObject` |
| `DefaultQueryTransformer` | `default_query_transformer.py` | Entity → default query definitions |
| `FilterTransformer` | `filter_transformer.py` | Entity → `FilterLayerObject` |

**Transformation chain (legacy path):**
```
Table → EntityTransformer → EntityLayerObject
  → DTOTransformer → DTOLayerObject (×3: Input, Output, Filter)
  → RepositoryTransformer → RepositoryLayerObject
  → ServiceTransformer → ServiceLayerObject
  → ControllerTransformer → ControllerLayerObject
```

---

## 11. Generated Application Structure

A generated Spring WebFlux application has this directory tree:

```
<output_dir>/
├── schema.sql                          — DDL for all entity tables
├── application_definitions/            — Source of truth definition files
│   ├── webflux_manifest.json
│   ├── webflux_project_metadata.json
│   ├── webflux_entities.json
│   ├── webflux_relationships.json
│   ├── webflux_entity_layer.json
│   ├── webflux_repository_layer.json
│   ├── webflux_service_layer.json
│   ├── webflux_controller_layer.json
│   ├── webflux_dto_layer.json
│   ├── webflux_query_layer.json
│   ├── webflux_filter_layer.json
│   ├── webflux_security_layer.json
│   ├── webflux_config_layer.json
│   ├── webflux_exception_layer.json
│   ├── webflux_audit_logging_layer.json
│   ├── webflux_authorization_layer.json
│   ├── webflux_group_definition_layer.json
│   ├── webflux_custom_queries_layer.json
│   ├── webflux_document_storage_layer.json  (optional)
│   └── webflux_ai_layer.json               (optional)
│
└── webflux_app/
    ├── pom.xml
    ├── auth-schema.sql
    ├── activity-tracking-schema.sql
    ├── test-data.json
    ├── ai_dependencies.xml                  (if AI layer)
    │
    └── src/
        ├── main/
        │   ├── java/<group_id_path>/
        │   │   ├── entity/                  — R2DBC entity classes
        │   │   │   ├── <Entity>.java        — per table
        │   │   │   ├── SystemConfig.java    — auth entities (9 total)
        │   │   │   ├── AuthUser.java
        │   │   │   ├── AccessAuditLog.java
        │   │   │   ├── UserRole.java
        │   │   │   ├── RecordOwner.java
        │   │   │   ├── QueryGroup.java
        │   │   │   ├── QueryGroupQuery.java
        │   │   │   ├── QueryGroupMember.java
        │   │   │   ├── QueryGroupRecord.java
        │   │   │   ├── OAuth2Provider.java
        │   │   │   ├── OAuth2LinkedAccount.java
        │   │   │   ├── CrudActivityLog.java
        │   │   │   ├── DeletedRecord.java
        │   │   │   ├── LoginActivityLog.java
        │   │   │   └── GrantActivityLog.java
        │   │   │
        │   │   ├── dto/                     — Data Transfer Objects
        │   │   │   ├── <Entity>InputDTO.java
        │   │   │   ├── <Entity>OutputDTO.java
        │   │   │   ├── <Entity>FilterDTO.java
        │   │   │   └── PageResponse.java
        │   │   │
        │   │   ├── repository/              — R2DBC repositories
        │   │   │   ├── <Entity>Repository.java
        │   │   │   ├── SystemConfigRepository.java
        │   │   │   ├── AuthUserRepository.java
        │   │   │   ├── AccessAuditLogRepository.java
        │   │   │   ├── UserRoleRepository.java
        │   │   │   ├── RecordOwnerRepository.java
        │   │   │   ├── QueryGroupRepository.java
        │   │   │   ├── QueryGroupQueryRepository.java
        │   │   │   ├── QueryGroupMemberRepository.java
        │   │   │   ├── QueryGroupRecordRepository.java
        │   │   │   ├── OAuth2ProviderRepository.java
        │   │   │   ├── OAuth2LinkedAccountRepository.java
        │   │   │   ├── CrudActivityLogRepository.java
        │   │   │   ├── DeletedRecordRepository.java
        │   │   │   ├── LoginActivityLogRepository.java
        │   │   │   └── GrantActivityLogRepository.java
        │   │   │
        │   │   ├── service/                 — Business logic
        │   │   │   ├── <Entity>Service.java
        │   │   │   ├── RoleAuthorizationService.java
        │   │   │   ├── AuditLoggingService.java
        │   │   │   ├── AdminService.java
        │   │   │   ├── OAuth2Service.java
        │   │   │   └── ActivityTrackingService.java
        │   │   │
        │   │   ├── controller/              — REST endpoints
        │   │   │   ├── <Entity>Controller.java
        │   │   │   ├── AuditController.java
        │   │   │   ├── AdminController.java
        │   │   │   ├── OAuth2Controller.java
        │   │   │   └── ActivityTrackingController.java
        │   │   │
        │   │   ├── security/                — Security components
        │   │   │   ├── AuthorizationWebFilter.java
        │   │   │   ├── AuthorizationAspect.java
        │   │   │   ├── EntityTable.java     — annotation
        │   │   │   ├── TableAccess.java     — annotation
        │   │   │   └── QueryAccess.java     — annotation
        │   │   │
        │   │   ├── auth/                    — Authentication
        │   │   │   ├── JwtConfig.java
        │   │   │   ├── JwtService.java
        │   │   │   ├── JwtAuthenticationFilter.java
        │   │   │   ├── AuthController.java
        │   │   │   └── AuthService.java
        │   │   │
        │   │   ├── config/                  — Configuration
        │   │   │   ├── SecurityConfig.java
        │   │   │   ├── PasswordEncoderConfig.java
        │   │   │   └── WebSecurityProperties.java
        │   │   │
        │   │   ├── exception/               — Exception handling
        │   │   │   ├── GlobalExceptionHandler.java
        │   │   │   ├── ErrorResponse.java
        │   │   │   ├── ValidationErrorResponse.java
        │   │   │   ├── EntityNotFoundException.java
        │   │   │   ├── AccessDeniedException.java
        │   │   │   └── DuplicateEntityException.java
        │   │   │
        │   │   └── ai/                      — AI layer (if enabled)
        │   │       ├── config/
        │   │       ├── provider/
        │   │       ├── service/
        │   │       ├── controller/
        │   │       ├── dto/
        │   │       ├── entity/
        │   │       ├── repository/
        │   │       ├── rag/
        │   │       ├── evaluator/
        │   │       ├── ingestion/
        │   │       ├── processing/
        │   │       ├── vectorstore/
        │   │       ├── orchestrator/
        │   │       ├── tools/
        │   │       ├── mcp/
        │   │       ├── observability/
        │   │       ├── budget/
        │   │       ├── audit/
        │   │       └── scheduler/
        │   │
        │   └── resources/
        │       ├── application.yml
        │       ├── ai_tables.sql            (if AI layer)
        │       ├── ai_application.properties (if AI layer)
        │       ├── templates/admin/         — Thymeleaf templates
        │       │   ├── dashboard.html
        │       │   ├── groups.html
        │       │   ├── group-form.html
        │       │   ├── users.html
        │       │   ├── user-detail.html
        │       │   ├── document-groups.html
        │       │   ├── document-group-form.html
        │       │   └── document-group-detail.html
        │       └── static/
        │
        └── test/java/<group_id_path>/
            ├── service/
            └── controller/
```

### Generated File Counts (approximate, for N entity tables)

| Category | Count |
|----------|-------|
| Per-entity files (entity + 3 DTOs + repo + service + controller) | 7 × N |
| Auth entities | 9 |
| Auth repositories | 9 |
| OAuth2 entities + repos | 4 |
| Activity tracking entities + repos | 8 |
| Services (auth, admin, audit, OAuth2, activity, authorization) | 6 |
| Controllers (auth, admin, audit, OAuth2, activity) | 5 |
| Security components | 5 |
| Auth components (JWT) | 5 |
| Config classes | 3 |
| Exception classes | 7 |
| Admin HTML templates | 8 |
| Configuration files (pom.xml, application.yml, schemas, test-data) | ~5 |
| AI layer files (if enabled) | 50+ |
| **Total (100 tables, no AI)** | **~850+** |

---

## 12. Dependency Mapping

### Complete `DEPENDENCY_MAP`

Maps dirty definition files to the generated file types that need regeneration.

| Definition File | Affected Generated File Types |
|----------------|-------------------------------|
| `webflux_entity_layer.json` | `entity`, `dto_input`, `dto_output`, `dto_filter`, `repository`, `service`, `controller`, `sql` |
| `webflux_entities.json` | `entity`, `sql` |
| `webflux_relationships.json` | `entity`, `repository`, `sql` |
| `webflux_repository_layer.json` | `repository` |
| `webflux_service_layer.json` | `service` |
| `webflux_controller_layer.json` | `controller` |
| `webflux_dto_layer.json` | `dto_input`, `dto_output`, `dto_filter` |
| `webflux_query_layer.json` | `repository`, `service`, `controller` |
| `webflux_filter_layer.json` | `dto_filter`, `controller` |
| `webflux_custom_queries_layer.json` | `repository` |
| `webflux_security_layer.json` | `security_config` |
| `webflux_config_layer.json` | `config` |
| `webflux_authorization_layer.json` | `service`, `controller` |
| `webflux_audit_logging_layer.json` | `service` |
| `webflux_exception_layer.json` | `exception` |
| `webflux_project_metadata.json` | `config`, `pom`, `sql` |
| `webflux_document_storage_layer.json` | `file_storage`, `json_converter`, `document_collection`, `sql` |
| `webflux_ai_layer.json` | `ai_service`, `ai_controller`, `ai_entity`, `ai_config`, `ai_dto`, `ai_repository`, `ai_provider`, `ai_rag`, `ai_evaluator`, `ai_ingestion`, `ai_processing`, `ai_vectorstore`, `ai_orchestrator`, `ai_tools`, `ai_mcp`, `ai_observability`, `ai_budget`, `ai_audit`, `sql` |

### SQL Trigger Files

These definition files trigger SQL DDL regeneration when dirty:

- `webflux_entity_layer.json`
- `webflux_entities.json`
- `webflux_relationships.json`
- `webflux_project_metadata.json`
- `webflux_document_storage_layer.json`
- `webflux_ai_layer.json`

### Entity-Scoped vs Global Files

**Entity-scoped files** (when dirty, all entities are marked affected for corresponding file types):
- `webflux_entity_layer.json`
- `webflux_entities.json`
- `webflux_relationships.json`
- `webflux_repository_layer.json`
- `webflux_service_layer.json`
- `webflux_controller_layer.json`
- `webflux_dto_layer.json`
- `webflux_query_layer.json`
- `webflux_filter_layer.json`
- `webflux_custom_queries_layer.json`
- `webflux_authorization_layer.json`
- `webflux_audit_logging_layer.json`
- `webflux_document_storage_layer.json`
- `webflux_ai_layer.json`

**Global files** (when dirty, all entities are marked affected):
- `webflux_security_layer.json`
- `webflux_config_layer.json`
- `webflux_project_metadata.json`
- `webflux_exception_layer.json`

### How Incremental Generation Resolves Affected Outputs

1. `StatusTracker.get_dirty_files()` returns list of dirty definition filenames
2. `DependencyMapper.resolve_affected_outputs(dirty_files, bundle)` iterates dirty files:
   - Looks up `DEPENDENCY_MAP` for each file → gets affected file types
   - Checks if file is in `_SQL_TRIGGER_FILES` → sets `regenerate_sql = True`
   - Marks ALL entities as affected for the resolved file types (simplified — no per-entity diffing)
3. `IncrementalGenerator.regenerate_affected(bundle, affected, output_dir)`:
   - For each affected entity + file type, reconstructs the layer object from bundle data
   - Calls the appropriate generator (EntityGenerator, DTOGenerator, etc.)
   - Writes the regenerated file
4. For document storage types (`file_storage`, `json_converter`), regenerates globally
5. For AI layer (`webflux_ai_layer.json` dirty), calls `AiGenerator.regenerate()`
6. `StatusTracker.mark_clean(dirty_files)` marks processed files as clean

---

## 13. AI Layer Integration

### How AiGenerator Coordinates 24 Sub-Generators

1. **Validation:** `AiValidator.validate(ai_layer, bundle)` checks definition structure, raises `ValueError` on errors, returns warnings
2. **Jinja2 setup:** Creates `jinja2.Environment` with `FileSystemLoader` pointing to `swfaw/templates/`
3. **Output directory resolution:** Maps logical directory names to filesystem paths under `src/main/java/<package>/ai/<subdir>/`
4. **Sub-generator execution:** Calls each sub-generator in dependency order (1–24), each returns `list[tuple[str, str]]` of `(filepath, content)` pairs
5. **File writing:** Writes all tuples to disk, creating parent directories as needed

### AI Output Directory Structure

```python
ai_dirs = {
    "config":        src_root / "ai" / "config",
    "provider":      src_root / "ai" / "provider",
    "service":       src_root / "ai" / "service",
    "controller":    src_root / "ai" / "controller",
    "dto":           src_root / "ai" / "dto",
    "entity":        src_root / "ai" / "entity",
    "repository":    src_root / "ai" / "repository",
    "rag":           src_root / "ai" / "rag",
    "evaluator":     src_root / "ai" / "evaluator",
    "ingestion":     src_root / "ai" / "ingestion",
    "processing":    src_root / "ai" / "processing",
    "vectorstore":   src_root / "ai" / "vectorstore",
    "orchestrator":  src_root / "ai" / "orchestrator",
    "tools":         src_root / "ai" / "tools",
    "mcp":           src_root / "ai" / "mcp",
    "observability": src_root / "ai" / "observability",
    "budget":        src_root / "ai" / "budget",
    "audit":         src_root / "ai" / "audit",
    "scheduler":     src_root / "ai" / "scheduler",
}
```

### Jinja2 Template Organization

Templates live under `swfaw/templates/ai/` with one subdirectory per concern:

```
templates/ai/
├── audit/          — AuditGenerator templates
├── budget/         — TokenBudgetGenerator templates
├── config/         — ProviderGenerator config templates
├── controller/     — EntityAiGenerator + StandaloneAiGenerator controller templates
├── ddl/            — AiDdlGenerator SQL templates
├── dto/            — AiDtoGenerator + TypedResponseGenerator templates
├── entity/         — ConversationGenerator entity templates
├── evaluator/      — EvaluatorGenerator templates
├── ingestion/      — DocumentIngestionGenerator templates
├── mcp/            — McpGenerator templates
├── observability/  — ObservabilityGenerator templates
├── orchestrator/   — OrchestratorGenerator templates
├── pom/            — AiPomGenerator dependency templates
├── processing/     — DocumentProcessingGenerator templates
├── provider/       — ProviderGenerator bean templates
├── rag/            — RagGenerator templates
├── repository/     — ConversationGenerator repository templates
├── scheduler/      — SessionCleanupGenerator templates
├── service/        — EntityAiGenerator + StandaloneAiGenerator service templates
├── tools/          — ToolFunctionGenerator templates
└── vectorstore/    — VectorStoreGenerator templates
```

### Integration with Phase 3 Pipeline

**Full generation:**
1. Phase 3 calls `generate_application()` for core Java code
2. Checks `bundle.ai_layer is not None`
3. Creates `AiGenerator()` and calls `ai_gen.generate(bundle, output_dir)`
4. AI files are written to `output_dir/webflux_app/src/main/java/<package>/ai/`

**Incremental generation:**
1. Phase 3 checks if `webflux_ai_layer.json` is in dirty files
2. If dirty and `bundle.ai_layer is not None`, calls `AiGenerator().regenerate(bundle, output_dir)`
3. `regenerate()` delegates to `generate()` — sub-generators are idempotent

### Special AI Output Files (Outside Java Source Tree)

| File | Location | Generator |
|------|----------|-----------|
| `ai_tables.sql` | `webflux_app/src/main/resources/ai_tables.sql` | `AiDdlGenerator` |
| `ai_application.properties` | `webflux_app/src/main/resources/ai_application.properties` | `AiAppPropertiesGenerator` |
| `ai_dependencies.xml` | `webflux_app/ai_dependencies.xml` | `AiPomGenerator` |

---

*End of swfaw reference document.*
