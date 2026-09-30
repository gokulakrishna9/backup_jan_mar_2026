# Code Generator Pipeline Analysis

**Date:** 2026-02-23  
**Time Started:** 19:14  
**Task:** Analyze code generator dependencies and create generation pipeline

---

## Analysis Approach

1. Read each numbered prompt (00-21)
2. Identify what each generator produces
3. Identify dependencies (what it needs as input)
4. Sort into layers: no dependencies → with dependencies
5. Create proper generation pipeline

---

## Generator Inventory

### Phase 0: Input Processing
- **12_SQL_PARSER** - Converts SQL DDL to JSON (FIRST STEP)

### Phase 1: Authentication Layer (Fixed Infrastructure)
- **13_AUTHENTICATION_DDL_GENERATOR** - Authentication schema SQL
- **Auth Entities** (generated from fixed schema, not from prompts)
- **Auth Repositories** (generated from auth entities)
- **14_ROLE_SERVICE_GENERATOR** - Role management service
- **15_USER_PROFILE_SERVICE_GENERATOR** - User profile service
- **16_FIRST_TIME_ADMIN_SETUP_GENERATOR** - Admin setup controller + service
- **08_JWT_AUTHENTICATION** - JWT service + auth controller
- **19_ACCOUNT_CONTROLLER_GENERATOR** - Account management controller + service
- **OAuth2 Components** (service + controller, part of auth layer)

### Phase 2: Business Layer (SQL-Driven)
- **01_ENTITY_LAYER** - Entity classes from SQL
- **02_DTO_LAYER** - DTOs (depends on entities)
- **03_REPOSITORY_LAYER** - Repositories (depends on entities)
- **04_SERVICE_LAYER** - Services (depends on entities, repositories, DTOs)
- **05_CONTROLLER_LAYER** - Controllers (depends on services, DTOs)
- **20_CUSTOM_QUERY_GENERATOR** - Custom queries (depends on repositories)

### Phase 3: Integration & Configuration
- **06_AUTHORIZATION_SERVICE** - Authorization service (depends on auth + business entities)
- **07_SECURITY_CONFIG** - Security configuration (depends on JWT, auth services)
- **09_APPLICATION_CONFIG** - Application configuration
- **10_POM_GENERATOR** - Maven POM file
- **11_TEST_GENERATOR** - Tests (depends on all layers)
- **17_SWAGGER_OPENAPI_CONFIG** - API documentation (depends on controllers)
- **18_GLOBAL_EXCEPTION_HANDLER** - Exception handling
- **21_APPLICATION_DEFINITION_JSON_GENERATOR** - Application documentation (depends on everything)

---

## Dependency Analysis

### Layer 0: No Dependencies (Input Processing)

**12_SQL_PARSER**
- **Input:** SQL DDL file
- **Output:** Database definition JSON
- **Dependencies:** None
- **Used by:** All business layer generators

---

### Layer 1: Authentication Infrastructure (Fixed, No SQL Input)

**13_AUTHENTICATION_DDL_GENERATOR**
- **Input:** Configuration only
- **Output:** authentication_authorization_schema.sql
- **Dependencies:** None
- **Used by:** Database setup

**Auth Entity Generation** (implicit, not a separate prompt)
- **Input:** Fixed schema definition
- **Output:** 9 entity classes
- **Dependencies:** None
- **Used by:** Auth repositories, services

**Auth Repository Generation** (implicit)
- **Input:** Auth entities
- **Output:** 9 repository interfaces
- **Dependencies:** Auth entities
- **Used by:** Auth services

**14_ROLE_SERVICE_GENERATOR**
- **Input:** Auth entities, auth repositories
- **Output:** RoleService.java
- **Dependencies:** AuthUser, Role, AuthUserRole entities/repositories
- **Used by:** Registration, admin functions

**15_USER_PROFILE_SERVICE_GENERATOR**
- **Input:** Auth entities, business entities (user tables)
- **Output:** UserProfileService.java
- **Dependencies:** AuthUserLink entity/repository, business user entities
- **Used by:** Registration, profile management

**08_JWT_AUTHENTICATION**
- **Input:** Auth entities
- **Output:** JwtAuthenticationService.java, AuthController.java
- **Dependencies:** AuthUser entity/repository
- **Used by:** Security config, all authenticated endpoints

**19_ACCOUNT_CONTROLLER_GENERATOR**
- **Input:** Auth entities
- **Output:** AccountController.java, AccountService.java
- **Dependencies:** AuthUser entity/repository
- **Used by:** User self-service

**16_FIRST_TIME_ADMIN_SETUP_GENERATOR**
- **Input:** Auth services
- **Output:** FirstTimeSetupController.java, FirstTimeSetupService.java, HTML templates
- **Dependencies:** RoleService, AuthUser repository
- **Used by:** Initial application setup

**OAuth2 Components** (implicit in auth layer)
- **Input:** Auth entities
- **Output:** OAuth2Service.java, OAuth2Controller.java
- **Dependencies:** AuthProvider, AuthUserProvider entities/repositories
- **Used by:** Third-party authentication

---

### Layer 2: Business Domain (SQL-Driven)

**01_ENTITY_LAYER**
- **Input:** Database definition JSON (from SQL Parser)
- **Output:** Entity classes (one per table)
- **Dependencies:** SQL Parser output
- **Used by:** DTOs, Repositories, Services

**02_DTO_LAYER**
- **Input:** Entity definitions
- **Output:** InputDTO, OutputDTO, FilterDTO (3 per entity)
- **Dependencies:** Entity layer
- **Used by:** Services, Controllers

**03_REPOSITORY_LAYER**
- **Input:** Entity definitions
- **Output:** Repository interfaces (one per entity)
- **Dependencies:** Entity layer
- **Used by:** Services

**04_SERVICE_LAYER**
- **Input:** Entities, DTOs, Repositories, Authorization service
- **Output:** Service classes (one per entity)
- **Dependencies:** Entity layer, DTO layer, Repository layer, Authorization service
- **Used by:** Controllers

**20_CUSTOM_QUERY_GENERATOR**
- **Input:** Entities, Repositories, custom query definitions
- **Output:** Custom query methods in repositories
- **Dependencies:** Entity layer, Repository layer
- **Used by:** Services

**05_CONTROLLER_LAYER**
- **Input:** Services, DTOs
- **Output:** REST controllers (one per entity)
- **Dependencies:** Service layer, DTO layer
- **Used by:** API consumers

---

### Layer 3: Integration & Cross-Cutting Concerns

**06_AUTHORIZATION_SERVICE**
- **Input:** Auth entities, Business entities
- **Output:** AuthorizationService.java
- **Dependencies:** EntityAuthorization, UserGroup entities/repositories, all business entities
- **Used by:** All business services

**18_GLOBAL_EXCEPTION_HANDLER**
- **Input:** None (cross-cutting)
- **Output:** GlobalExceptionHandler.java, ErrorResponse.java, Custom exceptions
- **Dependencies:** None
- **Used by:** All controllers

**07_SECURITY_CONFIG**
- **Input:** JWT service, Authorization service
- **Output:** SecurityConfig.java
- **Dependencies:** JwtAuthenticationService, AuthorizationService
- **Used by:** Spring Security

**09_APPLICATION_CONFIG**
- **Input:** None
- **Output:** ApplicationConfig.java, application.yml
- **Dependencies:** None
- **Used by:** Spring Boot

**10_POM_GENERATOR**
- **Input:** Project metadata
- **Output:** pom.xml
- **Dependencies:** None
- **Used by:** Maven build

**11_TEST_GENERATOR**
- **Input:** All layers
- **Output:** Unit tests, Integration tests
- **Dependencies:** Services, Controllers, Repositories
- **Used by:** Testing

**17_SWAGGER_OPENAPI_CONFIG**
- **Input:** Controllers
- **Output:** OpenApiConfig.java, controller annotations
- **Dependencies:** All controllers
- **Used by:** API documentation

**21_APPLICATION_DEFINITION_JSON_GENERATOR**
- **Input:** Everything
- **Output:** application_definition.json
- **Dependencies:** All entities, all components
- **Used by:** Documentation, tooling

---

## Generation Pipeline (Proper Order)

### Stage 0: Input Processing
```
1. SQL_PARSER (12)
   └─> Database definition JSON
```

### Stage 1: Authentication Infrastructure (Parallel)
```
2. AUTHENTICATION_DDL_GENERATOR (13)
   └─> authentication_authorization_schema.sql

3. Auth Entity Generation (implicit)
   └─> 9 auth entity classes

4. Auth Repository Generation (implicit)
   └─> 9 auth repository interfaces
```

### Stage 2: Authentication Services (Sequential)
```
5. JWT_AUTHENTICATION (08)
   └─> JwtAuthenticationService, AuthController

6. ROLE_SERVICE_GENERATOR (14)
   └─> RoleService

7. ACCOUNT_CONTROLLER_GENERATOR (19)
   └─> AccountController, AccountService

8. OAuth2 Components (implicit)
   └─> OAuth2Service, OAuth2Controller
```

### Stage 3: Business Domain - Data Layer (Sequential)
```
9. ENTITY_LAYER (01)
   └─> Business entity classes

10. DTO_LAYER (02)
    └─> InputDTO, OutputDTO, FilterDTO

11. REPOSITORY_LAYER (03)
    └─> Business repository interfaces

12. CUSTOM_QUERY_GENERATOR (20)
    └─> Custom query methods
```

### Stage 4: Integration Services (Parallel after Stage 3)
```
13. AUTHORIZATION_SERVICE (06)
    └─> AuthorizationService

14. USER_PROFILE_SERVICE_GENERATOR (15)
    └─> UserProfileService
```

### Stage 5: Business Logic Layer (Sequential after Stage 4)
```
15. SERVICE_LAYER (04)
    └─> Business service classes

16. CONTROLLER_LAYER (05)
    └─> REST controllers
```

### Stage 6: Admin & Setup (After Stage 2)
```
17. FIRST_TIME_ADMIN_SETUP_GENERATOR (16)
    └─> FirstTimeSetupController, FirstTimeSetupService, HTML templates
```

### Stage 7: Configuration & Cross-Cutting (Parallel)
```
18. GLOBAL_EXCEPTION_HANDLER (18)
    └─> Exception handling

19. SECURITY_CONFIG (07)
    └─> SecurityConfig

20. APPLICATION_CONFIG (09)
    └─> ApplicationConfig, application.yml

21. POM_GENERATOR (10)
    └─> pom.xml
```

### Stage 8: Documentation & Testing (Last)
```
22. SWAGGER_OPENAPI_CONFIG (17)
    └─> OpenApiConfig, API documentation

23. TEST_GENERATOR (11)
    └─> Unit tests, Integration tests

24. APPLICATION_DEFINITION_JSON_GENERATOR (21)
    └─> application_definition.json
```

---

## Dependency Graph

```
SQL_PARSER (12)
    │
    ├─> ENTITY_LAYER (01)
    │       │
    │       ├─> DTO_LAYER (02)
    │       │       │
    │       │       └─> CONTROLLER_LAYER (05)
    │       │               │
    │       │               └─> SWAGGER (17)
    │       │
    │       ├─> REPOSITORY_LAYER (03)
    │       │       │
    │       │       ├─> CUSTOM_QUERY (20)
    │       │       │
    │       │       └─> SERVICE_LAYER (04)
    │       │               │
    │       │               └─> CONTROLLER_LAYER (05)
    │       │
    │       └─> AUTHORIZATION_SERVICE (06)
    │               │
    │               └─> SERVICE_LAYER (04)
    │
    └─> USER_PROFILE_SERVICE (15)

AUTH_DDL (13)
    │
    └─> Auth Entities (implicit)
            │
            ├─> Auth Repositories (implicit)
            │       │
            │       ├─> JWT_AUTH (08)
            │       │       │
            │       │       └─> SECURITY_CONFIG (07)
            │       │
            │       ├─> ROLE_SERVICE (14)
            │       │       │
            │       │       └─> FIRST_TIME_SETUP (16)
            │       │
            │       ├─> ACCOUNT_CONTROLLER (19)
            │       │
            │       └─> OAuth2 Components (implicit)
            │
            └─> AUTHORIZATION_SERVICE (06)

EXCEPTION_HANDLER (18) ─┐
APPLICATION_CONFIG (09) ─┼─> All Controllers
POM_GENERATOR (10) ──────┘

All Components ──> TEST_GENERATOR (11)
All Components ──> APP_DEFINITION_JSON (21)
```

---

## Critical Dependencies

### Must Generate Before Business Layer:
1. SQL Parser (12) - Provides database definition
2. Auth DDL (13) - Provides auth schema
3. Auth Entities - Needed for authorization
4. Auth Repositories - Needed for auth services
5. Authorization Service (06) - Needed for business services

### Must Generate Before Controllers:
1. Services (04) - Controllers depend on services
2. DTOs (02) - Controllers use DTOs for request/response

### Must Generate Last:
1. Tests (11) - Need all components to test
2. Swagger (17) - Need all controllers
3. App Definition JSON (21) - Need complete application

---

## Parallel Generation Opportunities

### Can Generate in Parallel (Same Stage):

**Stage 1:**
- Auth DDL (13)
- Auth Entities (all 9)
- Auth Repositories (all 9)

**Stage 2:**
- JWT Auth (08)
- Role Service (14)
- Account Controller (19)
- OAuth2 Components

**Stage 3:**
- All business entities (01) - one per table
- All DTOs (02) - after entities
- All repositories (03) - after entities

**Stage 4:**
- Authorization Service (06)
- User Profile Service (15)

**Stage 5:**
- All business services (04) - one per entity
- All controllers (05) - after services

**Stage 7:**
- Exception Handler (18)
- Security Config (07)
- Application Config (09)
- POM Generator (10)

---

## Generation Order Summary

### Sequential Order (Respecting Dependencies):

1. **SQL_PARSER** (12) - Parse SQL to JSON
2. **AUTH_DDL** (13) - Generate auth schema
3. **Auth Entities** - Generate 9 auth entities
4. **Auth Repositories** - Generate 9 auth repositories
5. **JWT_AUTH** (08) - JWT service + auth controller
6. **ROLE_SERVICE** (14) - Role management
7. **ACCOUNT_CONTROLLER** (19) - Account management
8. **OAuth2 Components** - OAuth2 service + controller
9. **ENTITY_LAYER** (01) - Business entities
10. **DTO_LAYER** (02) - Business DTOs
11. **REPOSITORY_LAYER** (03) - Business repositories
12. **CUSTOM_QUERY** (20) - Custom queries
13. **AUTHORIZATION_SERVICE** (06) - Authorization logic
14. **USER_PROFILE_SERVICE** (15) - Profile management
15. **SERVICE_LAYER** (04) - Business services
16. **CONTROLLER_LAYER** (05) - REST controllers
17. **FIRST_TIME_SETUP** (16) - Admin setup
18. **EXCEPTION_HANDLER** (18) - Exception handling
19. **SECURITY_CONFIG** (07) - Security configuration
20. **APPLICATION_CONFIG** (09) - App configuration
21. **POM_GENERATOR** (10) - Maven POM
22. **SWAGGER** (17) - API documentation
23. **TEST_GENERATOR** (11) - Tests
24. **APP_DEFINITION_JSON** (21) - Application documentation

---

## Optimized Pipeline (With Parallelization)

### Phase 0: Input (1 step)
```
Step 1: SQL_PARSER (12)
```

### Phase 1: Auth Infrastructure (4 parallel batches)
```
Batch 1: AUTH_DDL (13)
Batch 2: Auth Entities (9 in parallel)
Batch 3: Auth Repositories (9 in parallel)
Batch 4: JWT_AUTH (08), ROLE_SERVICE (14), ACCOUNT_CONTROLLER (19), OAuth2 (parallel)
```

### Phase 2: Business Data Layer (3 sequential batches)
```
Batch 5: ENTITY_LAYER (01) - all entities in parallel
Batch 6: DTO_LAYER (02), REPOSITORY_LAYER (03) - in parallel
Batch 7: CUSTOM_QUERY (20)
```

### Phase 3: Integration (1 batch)
```
Batch 8: AUTHORIZATION_SERVICE (06), USER_PROFILE_SERVICE (15) - in parallel
```

### Phase 4: Business Logic (2 sequential batches)
```
Batch 9: SERVICE_LAYER (04) - all services in parallel
Batch 10: CONTROLLER_LAYER (05) - all controllers in parallel
```

### Phase 5: Setup & Config (2 batches)
```
Batch 11: FIRST_TIME_SETUP (16)
Batch 12: EXCEPTION_HANDLER (18), SECURITY_CONFIG (07), APPLICATION_CONFIG (09), POM (10) - in parallel
```

### Phase 6: Documentation & Testing (1 batch)
```
Batch 13: SWAGGER (17), TEST_GENERATOR (11), APP_DEFINITION_JSON (21) - in parallel
```

**Total: 13 batches (vs 24 sequential steps)**

---

## Status

**Analysis Complete:** ✅  
**Pipeline Defined:** ✅  
**Optimization Identified:** ✅  

**Next Steps:**
- Validate dependencies by reading each prompt in detail
- Create implementation guide for pipeline
- Identify any circular dependencies
- Document error handling for failed generations

