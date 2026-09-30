# swfaw_v2 - Layer-Specific Documentation

## Overview

swfaw_v2 (Spring WebFlux App Writer v2) generates a complete Spring WebFlux application from a SQL schema.
This document describes each layer, what it generates, known bugs fixed, and current status.

---

## Layer 1: SQL-to-JSON Conversion (`convert_sql.py`)

**Purpose:** Parses a MySQL `.sql` file and produces `database_definition.json` consumed by all generators.

**Usage:**
```bash
cd emotisense-ai/swfaw_v2
python convert_sql.py ../mysql_database_design/ems_recruitment_portal.sql
```

**Bugs Fixed:**
- Inline `PRIMARY KEY` columns (e.g. `course_id BIGINT PRIMARY KEY`) were being skipped because the `KEY` keyword check was too broad — it matched `PRIMARY KEY` and triggered a `continue` before the column was added.
  - Fix: Changed the KEY skip condition to exclude lines containing `PRIMARY KEY`.
- Multiple columns were being marked as `primaryKey: true` — the fallback logic that searched for the first `_id` column was running even when a primary key had already been found inline.
  - Fix: Removed the fallback logic entirely since inline detection now works correctly.

**Output:** `database_definition.json` with all tables, columns, and correct `primaryKey` flags.

---

## Layer 2: Entity Layer (`transformers/entity_transformer.py`, `generators/entity_generator.py`, `templates/entity_templates.py`)

**Purpose:** Generates JPA/R2DBC `@Table` entity classes for each database table.

**What it generates:**
- `@Id` annotation on the primary key field
- `@Column` annotations for all fields
- `@CreatedDate` / `@LastModifiedDate` for audit fields
- Soft delete `deletedAt` field
- `isPublic` flag for root entities (User, Course, Institution, Community, JobPost)

**Bugs Fixed:**
- The `@Id` annotation was not appearing on any entity because the primary key column was missing from the database definition entirely (caused by the `convert_sql.py` bug above).
  - Fix: Resolved by fixing the SQL parser to correctly include inline `PRIMARY KEY` columns.

**Status:** ✅ Working — all 100 entities generate with correct `@Id` fields.

---

## Layer 3: DTO Layer (`transformers/dto_transformer.py`, `generators/dto_generator.py`)

**Purpose:** Generates three DTO classes per entity: `InputDTO`, `OutputDTO`, `FilterDTO`.

**What it generates:**
- `InputDTO` — fields for create/update requests
- `OutputDTO` — fields for API responses (includes audit fields)
- `FilterDTO` — fields for search/filter queries

**Status:** ✅ Working — 300 DTOs generated correctly.

---

## Layer 4: Repository Layer (`transformers/repository_transformer.py`, `generators/repository_generator.py`)

**Purpose:** Generates Spring Data R2DBC repository interfaces.

**What it generates:**
- `ReactiveCrudRepository<Entity, Long>` interface
- Custom finder methods: `findByIdAndDeletedAtIsNull`, `findAllByDeletedAtIsNull`
- Auth-specific finders: `findByUsername`, `findByEmail`, etc.

**Status:** ✅ Working — 113 repositories loaded at runtime (confirmed in Spring Boot startup log).

---

## Layer 5: Service Layer (`transformers/service_transformer.py`, `generators/service_generator.py`, `templates/service_templates.py`)

**Purpose:** Generates service classes with CRUD operations and authorization checks.

**What it generates:**
- `create`, `findById`, `findAll`, `update`, `delete`, `deleteWithJustification` methods
- Authorization checks via `AuthorizationService.hasAccess()` for root entities
- Soft delete support
- Correct ID getter calls (e.g. `entity.getCourseId()`)

**Bugs Fixed:**
- Service template was calling `entity.get<EntityName>Id()` (e.g. `getCourseId()`) but the entity's actual primary key field was named differently or missing entirely.
  - Root cause: `convert_sql.py` was not including the primary key column in the JSON.
  - Fix: Fixed `convert_sql.py` (see Layer 1). The `ServiceGenerator` already correctly reads the primary key field name from the entity object.

**Status:** ✅ Working — all services compile and use correct ID getter names.

---

## Layer 6: Controller Layer (`transformers/controller_transformer.py`, `generators/controller_generator.py`)

**Purpose:** Generates REST controllers with standard CRUD endpoints.

**What it generates:**
- `GET /api/{entity}` — list all
- `GET /api/{entity}/{id}` — get by ID
- `POST /api/{entity}` — create
- `PUT /api/{entity}/{id}` — update
- `DELETE /api/{entity}/{id}` — delete

**Status:** ✅ Working.

---

## Layer 7: Authentication Layer (`templates/auth_service_templates.py`)

**Purpose:** Generates JWT-based authentication.

**What it generates:**
- `AuthService` — register, login, token refresh
- `AuthController` — `/api/auth/register`, `/api/auth/login`
- `JwtService` — token generation and validation
- `JwtAuthenticationFilter` — WebFlux security filter
- `SecurityContextHolder` — reactive user context utility

**Status:** ✅ Working.

---

## Layer 8: Authorization Layer (`templates/authorization_service_templates.py`)

**Purpose:** Generates document-based access control with 6 group types.

**What it generates:**
- `AuthorizationService` — `hasAccess(userId, tableName, recordId, action)` method
- `DocumentGroupMatcher` — matches records to document groups
- `QueryExecutor` — executes dynamic queries for group definitions
- `PermissionResolver` — resolves user/group permissions

**Status:** ✅ Working.

---

## Layer 9: Admin UI Layer (`templates/admin_ui_templates.py`)

**Purpose:** Generates Thymeleaf-based admin interface for managing users, groups, and permissions.

**What it generates:**
- `AdminService` — user/group/permission management methods
- `AdminController` — Thymeleaf controller at `/admin`
- 8 HTML templates: dashboard, groups, group-form, users, user-detail, document-groups, document-group-form, document-group-detail

**Bugs Fixed:**
- `AdminController.addUserToGroup()` was calling `adminService.addUserToGroup(userId, groupId, null, null)` with two nulls, but `AdminService.addUserToGroup()` only takes a single `LocalDateTime expiresAt` parameter.
  - Fix: Changed to `adminService.addUserToGroup(userId, groupId, null)`.
- `AdminController.grantPermission()` was calling `adminService.grantPermission(..., null, null)` with two nulls, but the method only takes a single `LocalDateTime expiresAt`.
  - Fix: Changed to `adminService.grantPermission(..., null)`.
- `AdminService` was referencing non-existent fields: `isDefaultGroup`, `validFrom`, `validUntil`, `createdAt` setters on auth entities.
  - Fix: Removed all invalid field references and aligned with actual auth entity schema.
- Accessing `/admin` without being logged in caused a Whitelabel Error Page instead of redirecting to login.
  - Root cause: All handler methods used `isAdmin()` which called `SecurityContextHolder.getCurrentUser()`. When no user is in context, it returned empty and Spring WebFlux had no error view configured.
  - Fix: Replaced `isAdmin()` with a new `requireAdmin(Supplier<Mono<String>> action)` helper that uses `.switchIfEmpty(Mono.error(...))` and `.onErrorResume(e -> Mono.just("redirect:/login?message=Please+login+to+access+admin"))`. All 13 handler methods now use this pattern, eliminating all the repetitive `if (!admin)` checks.

- Accessing `/admin` and being redirected to `/login` resulted in a 404 Whitelabel Error because `SetupController` had no `GET /login` mapping — only the Thymeleaf template existed.
  - Fix: Added `GET /login` handler to `SetupController` that renders the `login` view, or redirects to `/setup` if initial setup has not been completed yet.

**Status:** ✅ Working — `/admin` → 303 redirect → `/login?message=Please+login+to+access+admin` → 200.

---

## Layer 10: OAuth2 Layer (`templates/oauth2_templates.py`)

**Purpose:** Generates OAuth2 provider support (Google, GitHub, etc.).

**What it generates:**
- `OAuth2Provider` entity and repository
- `OAuth2LinkedAccount` entity and repository
- `OAuth2Service` — handles OAuth2 token exchange and account linking
- `OAuth2Controller` — `/api/oauth2/...` endpoints

**Bugs Fixed:**
- `OAuth2ProviderRepository` had malformed code with incorrect imports mixed into the interface body.
  - Fix: Cleaned up the repository template to be a valid Java interface.
- `OAuth2Service` had type inference issues with unchecked Map casts.
  - Fix: Added `@SuppressWarnings("unchecked")` and explicit `Map<String, Object>` casting.

**Status:** ✅ Working.

---

## Layer 11: Audit Logging Layer (`templates/audit_logging_templates.py`)

**Purpose:** Generates audit logging for access attempts and super user actions.

**What it generates:**
- `AuditLoggingService` — logs to `access_audit_log` and `super_user_action_log` tables
- `AuditController` — `/api/audit/...` endpoints for viewing logs

**Status:** ✅ Working.

---

## Layer 12: Configuration Layer (`templates/config_templates.py`)

**Purpose:** Generates application configuration files.

**What it generates:**
- `application.yml` — R2DBC datasource, JWT config, security settings
- `DatabaseConfig.java` — R2DBC repository enablement
- `SecurityConfig.java` — Spring Security WebFlux configuration
- `SwaggerConfig.java` — OpenAPI/Swagger UI configuration

**Bugs Fixed:**
- `SwaggerConfig` did not include JWT Bearer token authentication, so Swagger UI had no "Authorize" button.
  - Fix: Added `SecurityScheme` with `HTTP bearer` type and `SecurityRequirement` applied globally to all endpoints.

**Status:** ✅ Working — Swagger UI at `/swagger-ui.html` shows 🔒 Authorize button for JWT.

---

## End-to-End Verified Run

**Schema:** `emotisense-ai/mysql_database_design/ems_recruitment_portal.sql` (100 tables)

**Generated:** 752 Java files including:
- 100 entities, 300 DTOs, 113 repositories, 100 services, 100 controllers
- Full auth/authz/audit/admin/OAuth2 layers

**Compilation:** ✅ `mvn clean compile` — BUILD SUCCESS

**Runtime:** ✅ Spring Boot started in ~8s on port 8080, 113 repositories loaded

**Database:** MySQL (Docker) — `ems_recruitment_portal` database with 13 auth tables

**Endpoints verified:**
- `http://localhost:8080/setup` → HTTP 200
- `http://localhost:8080/swagger-ui.html` → HTTP 200 (with JWT Authorize button)
- `http://localhost:8080/admin` → 303 redirect → `/login?message=Please+login+to+access+admin` → HTTP 200
- `http://localhost:8080/login` → HTTP 200 (login page, or redirect to `/setup` if not yet configured)
