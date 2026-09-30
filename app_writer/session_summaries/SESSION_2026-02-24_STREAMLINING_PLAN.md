# Prompt Streamlining Plan - Code Generator Prompts

**Date:** 2026-02-24  
**Status:** Plan Created  
**Total Prompts:** 35 (to be streamlined to 25)

---

## Executive Summary

All prompts in `emotisense-ai/prompts/code_generators/` need to be:
1. **Sorted by dependency order** (10 execution phases)
2. **Streamlined** - Remove redundancies while maintaining atomicity
3. **Renumbered** - Sequential numbering based on execution order

---

## Dependency-Based Execution Order

### Phase 1: Foundation (6 prompts - Parallel)
- **00_SQL_PARSER** ← 14_SQL_PARSER.md
- **01_PROJECT_SETUP** ← 01_PROJECT_SETUP.md
- **02_BASE_GENERATOR** ← 02_BASE_GENERATOR.md (EMPTY - needs creation)
- **03_AUTHENTICATION_DDL** ← 12_AUTHENTICATION_DDL.md
- **04_POM_GENERATOR** ← 33_POM_GENERATOR.md
- **05_APPLICATION_CONFIG** ← 11_APPLICATION_CONFIG.md

### Phase 2: Core Layers (3 prompts - Sequential)
- **06_ENTITY_LAYER** ← 03_ENTITY_LAYER.md
- **07_DTO_LAYER** ← 04_DTO_LAYER.md
- **08_REPOSITORY_LAYER** ← 05_REPOSITORY_LAYER.md

### Phase 3: Authentication (3 prompts - Sequential)
- **09_JWT_AUTHENTICATION** ← 09_JWT_AUTHENTICATION.md
- **10_SECURITY_CONFIG** ← 10_SECURITY_CONFIG.md
- **11_AUTHORIZATION_SERVICE** ← 13_AUTHORIZATION_SERVICE.md

### Phase 4: Business Logic (3 prompts - Sequential)
- **12_EXCEPTION_HANDLER** ← 08_EXCEPTION_HANDLER.md
- **13_SERVICE_LAYER** ← 06_SERVICE_LAYER.md
- **14_CONTROLLER_LAYER** ← 07_CONTROLLER_LAYER.md

### Phase 5: User Management (4 prompts - Parallel)
- **15_ROLE_SERVICE** ← 24_ROLE_SERVICE.md
- **16_USER_PROFILE_SERVICE** ← 25_USER_PROFILE_SERVICE.md
- **17_FIRST_TIME_ADMIN_SETUP** ← 26_FIRST_TIME_ADMIN_SETUP.md
- **18_ACCOUNT_CONTROLLER** ← 27_ACCOUNT_CONTROLLER.md

### Phase 6: Advanced Features (4 prompts - Parallel)
- **19_CUSTOM_QUERY_GENERATOR** ← 28_CUSTOM_QUERY_GENERATOR.md
- **20_SWAGGER_OPENAPI_CONFIG** ← 29_SWAGGER_OPENAPI_CONFIG.md
- **21_GLOBAL_EXCEPTION_HANDLER** ← 30_GLOBAL_EXCEPTION_HANDLER.md
- **22_UTILITY_GENERATORS** ← 31_UTILITY_GENERATORS.md

### Phase 7: Testing & Documentation (2 prompts - Sequential)
- **23_TEST_GENERATOR** ← 34_TEST_GENERATOR.md
- **24_APPLICATION_DEFINITION_JSON** ← 35_APPLICATION_DEFINITION_JSON.md

---

## Streamlining Rules

### Keep Only These Sections

1. **Header**
   ```markdown
   # [Prompt Name]
   
   **Phase:** X
   **Dependencies:** [List]
   ```

2. **Input**
   ```markdown
   ## Input
   - Data structure/file needed
   - Source of input
   ```

3. **Output**
   ```markdown
   ## Output
   - Files to generate
   - Package locations
   ```

4. **Generation Steps**
   ```markdown
   ## Steps
   1. Parse input
   2. Transform data
   3. Generate code
   4. Write files
   ```

5. **Code Templates**
   ```markdown
   ## Templates
   [Actual code to generate]
   ```

6. **Type Mappings** (if applicable)
   ```markdown
   ## Mappings
   SQL Type → Java Type
   ```

### Remove These Sections

1. ❌ "Purpose" - Redundant with title
2. ❌ "Key Principles" - Move to overview docs
3. ❌ "Why we need this" - Not needed for generation
4. ❌ "Benefits" - Not needed for generation
5. ❌ "Architecture diagrams" - Move to overview docs
6. ❌ "Version History" - Not needed for generation
7. ❌ "References" - Dependencies section covers this
8. ❌ "Validation Checklist" - Implicit in generation
9. ❌ Long explanations - Keep only essential info
10. ❌ Duplicate examples - One canonical example only

---

## Streamlining Template

```markdown
# [Prompt Name]

**Phase:** X  
**Dependencies:** [Comma-separated list]

## Input
- [Data structure needed]
- [Source: Previous prompt or file]

## Output
- [File 1]: `path/to/file.java`
- [File 2]: `path/to/file.java`

## Steps

### 1. Parse Input
[Pseudocode or description]

### 2. Transform Data
[Transformation logic]

### 3. Generate Code
[Code generation logic]

### 4. Write Files
[File writing logic]

## Templates

### [Template Name]
```java
[Actual code template]
```

## Mappings (if applicable)
| Input | Output |
|-------|--------|
| X | Y |
```

---

## Example: Streamlined Entity Layer

### Before (03_ENTITY_LAYER.md - ~200 lines)
- Purpose section
- Key Principles
- Dependencies
- Output
- Key Principles (duplicate)
- Generation Steps (6 steps)
- Type Mapping
- Naming Conventions
- Validation checklist
- References
- Version History

### After (06_ENTITY_LAYER.md - ~80 lines)
```markdown
# Entity Layer Generator

**Phase:** 2  
**Dependencies:** 00_SQL_PARSER

## Input
- Database definition JSON from SQL Parser
- Table definitions with columns, types, constraints

## Output
- `{EntityName}.java` per table
- Package: `com.example.entity`

## Steps

### 1. Parse Table
Extract: tableName, columns[], primaryKey, foreignKeys[]

### 2. Map Columns
For each column: columnName → fieldName (camelCase), sqlType → javaType

### 3. Add Audit Fields
createdAt, updatedAt, deletedAt (LocalDateTime)

### 4. Generate Entity
```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "{table_name}")
public class {ClassName} {
    @Id
    private {PkType} {pkField};
    private {JavaType} {fieldName};
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    private LocalDateTime deletedAt;
}
```

### 5. Write File
Path: `src/main/java/com/example/entity/{ClassName}.java`

## Mappings
| SQL Type | Java Type |
|----------|-----------|
| BIGINT | Long |
| VARCHAR | String |
| BOOLEAN | Boolean |
| DATETIME | LocalDateTime |
```

**Reduction:** 200 lines → 80 lines (60% reduction)

---

## Implementation Steps

### Step 1: Create Base Generator (NEW)
File: `02_BASE_GENERATOR.md`
- Type mappings (SQL → Java)
- Naming conventions (snake_case → camelCase, PascalCase)
- Utility functions (toCamelCase, toPascalCase, etc.)

### Step 2: Streamline Foundation Prompts (Phase 1)
- 00_SQL_PARSER
- 01_PROJECT_SETUP
- 03_AUTHENTICATION_DDL
- 04_POM_GENERATOR
- 05_APPLICATION_CONFIG

### Step 3: Streamline Core Layer Prompts (Phase 2)
- 06_ENTITY_LAYER
- 07_DTO_LAYER
- 08_REPOSITORY_LAYER

### Step 4: Streamline Authentication Prompts (Phase 3)
- 09_JWT_AUTHENTICATION
- 10_SECURITY_CONFIG
- 11_AUTHORIZATION_SERVICE

### Step 5: Streamline Business Logic Prompts (Phase 4)
- 12_EXCEPTION_HANDLER
- 13_SERVICE_LAYER
- 14_CONTROLLER_LAYER

### Step 6: Streamline User Management Prompts (Phase 5)
- 15_ROLE_SERVICE
- 16_USER_PROFILE_SERVICE
- 17_FIRST_TIME_ADMIN_SETUP
- 18_ACCOUNT_CONTROLLER

### Step 7: Streamline Advanced Features (Phase 6)
- 19_CUSTOM_QUERY_GENERATOR
- 20_SWAGGER_OPENAPI_CONFIG
- 21_GLOBAL_EXCEPTION_HANDLER
- 22_UTILITY_GENERATORS

### Step 8: Streamline Testing & Documentation (Phase 7)
- 23_TEST_GENERATOR
- 24_APPLICATION_DEFINITION_JSON

### Step 9: Move Overview Content
Create/update overview documents:
- `00_ARCHITECTURE_OVERVIEW.md` - System architecture
- `00_AUTHORIZATION_SYSTEM_OVERVIEW.md` - Already exists
- `00_TWO_PHASE_GENERATION_ARCHITECTURE.md` - Already exists

### Step 10: Clean Up
- Remove old numbered files (01-35)
- Keep only streamlined files (00-24)
- Update README.md with new structure

---

## Expected Results

### Before Streamlining
- 35 prompt files
- Average ~300 lines per file
- Total: ~10,500 lines
- Redundant content across files
- Unclear execution order

### After Streamlining
- 25 prompt files
- Average ~100 lines per file
- Total: ~2,500 lines (76% reduction)
- No redundancies
- Clear execution order (7 phases)
- Atomic, focused prompts

---

## Benefits

1. **Clarity** - Each prompt has single responsibility
2. **Efficiency** - No redundant content
3. **Maintainability** - Easier to update
4. **Execution Order** - Clear dependencies
5. **Atomicity** - Each prompt depends only on input, not explanations
6. **Completeness** - All necessary information retained

---

## Next Actions

1. ✅ Create dependency analysis (DONE)
2. ✅ Create streamlining plan (DONE - this document)
3. ⏳ Create 02_BASE_GENERATOR.md (NEW)
4. ⏳ Streamline Phase 1 prompts (6 files)
5. ⏳ Streamline Phase 2 prompts (3 files)
6. ⏳ Streamline Phase 3 prompts (3 files)
7. ⏳ Streamline Phase 4 prompts (3 files)
8. ⏳ Streamline Phase 5 prompts (4 files)
9. ⏳ Streamline Phase 6 prompts (4 files)
10. ⏳ Streamline Phase 7 prompts (2 files)
11. ⏳ Update overview documents
12. ⏳ Clean up old files
13. ⏳ Update README.md

---

## Conclusion

This plan provides a systematic approach to streamlining all 35 prompts into 25 focused, atomic prompts organized by execution order. The streamlining will reduce total content by ~76% while maintaining all essential information for code generation.

**Status:** Ready for implementation  
**Estimated Time:** 4-6 hours for complete streamlining  
**Priority:** High - Improves prompt clarity and usability

