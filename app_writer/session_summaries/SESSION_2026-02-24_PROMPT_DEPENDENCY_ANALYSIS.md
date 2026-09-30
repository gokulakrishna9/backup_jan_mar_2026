# Prompt Dependency Analysis & Streamlining Plan

**Date:** 2026-02-24  
**Purpose:** Analyze dependencies and create execution order for all code generator prompts

---

## Dependency Analysis

### Layer 0: No Dependencies (Foundation)
These prompts can run first, in any order:

1. **14_SQL_PARSER.md** - Converts SQL to JSON
   - Input: SQL DDL file
   - Output: database_definition.json
   - No dependencies

2. **01_PROJECT_SETUP.md** - Main orchestrator
   - Input: Application definition JSON
   - Output: Project structure, BackendWriter class
   - No dependencies

3. **02_BASE_GENERATOR.md** - Utility methods (EMPTY FILE - needs creation)
   - Input: None
   - Output: Type mapping, naming conventions, utilities
   - No dependencies

### Layer 1: Database Definition Required
These prompts need the parsed database definition:

4. **03_ENTITY_LAYER.md** - Generate entities
   - Input: Database definition JSON
   - Requires: 14_SQL_PARSER
   - Output: Entity classes

5. **12_AUTHENTICATION_DDL.md** - Auth schema
   - Input: Project metadata
   - Requires: None (fixed schema)
   - Output: authentication_authorization_schema.sql, Auth entities

### Layer 2: Entity Layer Required
These prompts need entities to exist:

6. **04_DTO_LAYER.md** - Generate DTOs
   - Input: Entity definitions
   - Requires: 03_ENTITY_LAYER
   - Output: InputDTO, OutputDTO, FilterDTO

7. **05_REPOSITORY_LAYER.md** - Generate repositories
   - Input: Entity definitions
   - Requires: 03_ENTITY_LAYER
   - Output: Repository interfaces

### Layer 3: Authentication Components
These prompts build authentication infrastructure:

8. **09_JWT_AUTHENTICATION.md** - JWT service
   - Input: Auth entities
   - Requires: 12_AUTHENTICATION_DDL
   - Output: JwtAuthenticationService, AuthController, Auth DTOs

9. **10_SECURITY_CONFIG.md** - Security configuration
   - Input: None (fixed config)
   - Requires: 09_JWT_AUTHENTICATION
   - Output: SecurityConfig.java

10. **11_APPLICATION_CONFIG.md** - Application config
    - Input: Project metadata
    - Requires: None
    - Output: application.yml, DatabaseConfig, SwaggerConfig

### Layer 4: Authorization Service
This prompt needs auth entities and repositories:

11. **13_AUTHORIZATION_SERVICE.md** - Authorization logic
    - Input: Auth entities (EntityAuthorization, UserGroup, UserGroupMembership)
    - Requires: 12_AUTHENTICATION_DDL
    - Output: AuthorizationService.java

### Layer 5: Business Logic
These prompts need repositories and authorization:

12. **06_SERVICE_LAYER.md** - Generate services
    - Input: Entity, DTO, Repository definitions
    - Requires: 03_ENTITY_LAYER, 04_DTO_LAYER, 05_REPOSITORY_LAYER, 13_AUTHORIZATION_SERVICE
    - Output: Service classes

13. **08_EXCEPTION_HANDLER.md** - Exception handling
    - Input: None
    - Requires: None
    - Output: Custom exceptions, GlobalExceptionHandler

### Layer 6: API Layer
These prompts need services:

14. **07_CONTROLLER_LAYER.md** - Generate controllers
    - Input: Service and DTO definitions
    - Requires: 04_DTO_LAYER, 06_SERVICE_LAYER
    - Output: Controller classes

### Layer 7: User Management
These prompts extend authentication:

15. **24_ROLE_SERVICE.md** - Role management
    - Input: Role, AuthUserRole entities
    - Requires: 12_AUTHENTICATION_DDL
    - Output: RoleService.java

16. **25_USER_PROFILE_SERVICE.md** - User profile service
    - Input: User entities, AuthUserLink
    - Requires: 03_ENTITY_LAYER, 12_AUTHENTICATION_DDL
    - Output: UserProfileService.java

17. **26_FIRST_TIME_ADMIN_SETUP.md** - Admin setup
    - Input: AuthUser, Role entities
    - Requires: 12_AUTHENTICATION_DDL
    - Output: FirstTimeSetupController, FirstTimeSetupService, HTML templates

18. **27_ACCOUNT_CONTROLLER.md** - Account management
    - Input: AuthUser entity
    - Requires: 12_AUTHENTICATION_DDL
    - Output: AccountController, AccountService

### Layer 8: Advanced Features
These prompts extend existing layers:

19. **28_CUSTOM_QUERY_GENERATOR.md** - Custom queries
    - Input: Repository, Service definitions
    - Requires: 05_REPOSITORY_LAYER, 06_SERVICE_LAYER
    - Output: Custom query methods

20. **29_SWAGGER_OPENAPI_CONFIG.md** - API documentation
    - Input: None (configuration only)
    - Requires: None
    - Output: OpenApiConfig.java

21. **30_GLOBAL_EXCEPTION_HANDLER.md** - Exception handling
    - Input: None
    - Requires: None
    - Output: GlobalExceptionHandler.java

22. **31_UTILITY_GENERATORS.md** - Utilities
    - Input: None
    - Requires: None
    - Output: Utility classes

23. **32_FILE_REGENERATION.md** - Regeneration strategy
    - Input: None
    - Requires: None
    - Output: Regeneration logic

### Layer 9: Build & Testing
These prompts need all layers:

24. **33_POM_GENERATOR.md** - Maven POM
    - Input: Project metadata
    - Requires: None
    - Output: pom.xml

25. **34_TEST_GENERATOR.md** - Tests
    - Input: Service and Controller definitions
    - Requires: All layers
    - Output: Unit tests, integration tests

### Layer 10: Documentation
This prompt documents everything:

26. **35_APPLICATION_DEFINITION_JSON.md** - Application documentation
    - Input: All generated components
    - Requires: All layers
    - Output: application_definition.json

---

## Execution Order (Optimized)

### Phase 1: Foundation (Parallel)
```
14_SQL_PARSER → database_definition.json
01_PROJECT_SETUP → Project structure
02_BASE_GENERATOR → Utilities
12_AUTHENTICATION_DDL → Auth schema
33_POM_GENERATOR → pom.xml
11_APPLICATION_CONFIG → application.yml
```

### Phase 2: Core Layers (Sequential)
```
03_ENTITY_LAYER → Entities
  ↓
04_DTO_LAYER → DTOs
05_REPOSITORY_LAYER → Repositories
```

### Phase 3: Authentication (Sequential)
```
09_JWT_AUTHENTICATION → JWT service
  ↓
10_SECURITY_CONFIG → Security config
13_AUTHORIZATION_SERVICE → Authorization logic
```

### Phase 4: Business Logic (Sequential)
```
08_EXCEPTION_HANDLER → Exceptions
  ↓
06_SERVICE_LAYER → Services
  ↓
07_CONTROLLER_LAYER → Controllers
```

### Phase 5: User Management (Parallel)
```
24_ROLE_SERVICE
25_USER_PROFILE_SERVICE
26_FIRST_TIME_ADMIN_SETUP
27_ACCOUNT_CONTROLLER
```

### Phase 6: Advanced Features (Parallel)
```
28_CUSTOM_QUERY_GENERATOR
29_SWAGGER_OPENAPI_CONFIG
30_GLOBAL_EXCEPTION_HANDLER
31_UTILITY_GENERATORS
32_FILE_REGENERATION
```

### Phase 7: Testing & Documentation (Sequential)
```
34_TEST_GENERATOR → Tests
  ↓
35_APPLICATION_DEFINITION_JSON → Documentation
```

---

## Streamlining Strategy

### Redundancies to Remove

1. **Repeated Explanations**
   - Remove "What is X" sections
   - Remove "Why we need X" sections
   - Keep only "How to generate X"

2. **Duplicate Type Mappings**
   - Move to 02_BASE_GENERATOR
   - Reference from other prompts

3. **Duplicate Naming Conventions**
   - Move to 02_BASE_GENERATOR
   - Reference from other prompts

4. **Duplicate Validation Checklists**
   - Standardize format
   - Remove redundant items

5. **Duplicate Code Examples**
   - Keep only essential templates
   - Remove verbose examples

6. **Duplicate Architecture Diagrams**
   - Move to overview documents
   - Reference from prompts

### Atomicity Principles

Each prompt should contain ONLY:

1. **Input Definition**
   - What data is needed
   - Where it comes from

2. **Transformation Logic**
   - How to process input
   - What rules to apply

3. **Output Definition**
   - What to generate
   - Where to write it

4. **Template/Code**
   - Actual code to generate
   - No explanations

5. **Dependencies**
   - What must exist first
   - What this produces for others

### What to Keep

1. **Generation Steps** - Atomic, sequential steps
2. **Code Templates** - Actual code to generate
3. **Type Mappings** - SQL → Java conversions
4. **Naming Rules** - Conventions for names
5. **Dependencies** - What's required
6. **Output Specification** - What files to create

### What to Remove

1. **Architecture explanations** - Move to overview docs
2. **"Why" sections** - Not needed for generation
3. **Conceptual diagrams** - Move to overview docs
4. **Duplicate examples** - Keep one canonical example
5. **Version history** - Not needed for generation
6. **Long descriptions** - Keep only essential info

---

## Next Steps

1. Create streamlined versions of all prompts
2. Organize by execution order
3. Remove redundancies
4. Maintain atomicity
5. Test generation flow

