# Prompt Coverage Comparison

**Date:** 2026-02-24  
**Purpose:** Compare coverage between `emotisense-ai/prompts/code_generators/` and `ai_generated_documents/backend_prompts/`

---

## Comparison Table

| Feature/Requirement | emotisense-ai/prompts/ | backend_prompts/ | Status | Notes |
|---------------------|------------------------|------------------|--------|-------|
| **Core Layers** |
| Entity Generator | ✅ PROMPT 01 | ✅ PROMPT 03 | ✅ COVERED | Both present |
| DTO Generator | ✅ PROMPT 02 | ✅ PROMPT 04 | ✅ COVERED | Both present |
| Repository Generator | ✅ PROMPT 03 | ✅ PROMPT 05 | ✅ COVERED | Both present |
| Service Generator | ✅ PROMPT 04 | ✅ PROMPT 06 | ✅ COVERED | Both present |
| Controller Generator | ✅ PROMPT 05 | ✅ PROMPT 07 | ✅ COVERED | Both present |
| Exception Handler | ✅ PROMPT 18 | ✅ PROMPT 08 | ✅ COVERED | Both present |
| **Authentication** |
| JWT Authentication | ✅ PROMPT 08 | ✅ PROMPT 09 | ✅ COVERED | Both present |
| Auth Tables/Entities | ✅ PROMPT 13 | ✅ PROMPT 09A | ✅ COVERED | Both present |
| Security Config | ✅ PROMPT 07 | ✅ PROMPT 09B | ✅ COVERED | Both present |
| Application Config | ✅ PROMPT 09 | ✅ PROMPT 09C | ✅ COVERED | Both present |
| **Build & Config** |
| POM Generator | ✅ PROMPT 10 | ✅ PROMPT 10 | ✅ COVERED | Both present |
| Swagger/OpenAPI | ✅ PROMPT 17 | ❌ Missing | ⚠️ GAP | Only in emotisense-ai |
| **Authorization** |
| Authorization Service | ✅ PROMPT 06 | ❌ Missing (stub) | ⚠️ GAP | emotisense-ai has full impl |
| Security Core Concepts | ❌ Missing | ✅ PROMPT 15 | ⚠️ GAP | Only in backend_prompts |
| Security Entity Layer | ❌ Missing | ✅ PROMPT 16 | ⚠️ GAP | Only in backend_prompts |
| Security Repository Layer | ❌ Missing | ✅ PROMPT 17 | ⚠️ GAP | Only in backend_prompts |
| Security Service Layer | ❌ Missing | ✅ PROMPT 18 | ⚠️ GAP | Only in backend_prompts |
| Security Controller Layer | ❌ Missing | ✅ PROMPT 19 | ⚠️ GAP | Only in backend_prompts |
| Security DTO Layer | ❌ Missing | ✅ PROMPT 20 | ⚠️ GAP | Only in backend_prompts |
| **Group Management** |
| Group Management Layer | ❌ Missing | ✅ PROMPT 22 | ⚠️ GAP | Only in backend_prompts |
| Group-Based Authorization | ❌ Missing | ✅ PROMPT 23 | ⚠️ GAP | Only in backend_prompts |
| **Testing** |
| Test Generator | ✅ PROMPT 11 | ❌ Missing (stub) | ⚠️ GAP | emotisense-ai has impl |
| Security Unit Tests | ❌ Missing | ✅ PROMPT 21A | ⚠️ GAP | Only in backend_prompts |
| Security Integration Tests | ❌ Missing | ✅ PROMPT 21B | ⚠️ GAP | Only in backend_prompts |
| Public Entity Tests | ❌ Missing | ✅ PROMPT 21C | ⚠️ GAP | Only in backend_prompts |
| **User Management** |
| Role Service | ✅ PROMPT 14 | ❌ Missing | ⚠️ GAP | Only in emotisense-ai |
| User Profile Service | ✅ PROMPT 15 | ❌ Missing | ⚠️ GAP | Only in emotisense-ai |
| First-Time Admin Setup | ✅ PROMPT 16 | ❌ Missing | ⚠️ GAP | Only in emotisense-ai |
| Account Controller | ✅ PROMPT 19 | ❌ Missing | ⚠️ GAP | Only in emotisense-ai |
| **Advanced Features** |
| Custom Query Generator | ✅ PROMPT 20 | ✅ PROMPT 13 | ✅ COVERED | Both present |
| SQL Parser | ✅ PROMPT 12 | ❌ Missing | ⚠️ GAP | Only in emotisense-ai |
| App Definition JSON | ✅ PROMPT 21 | ❌ Missing | ⚠️ GAP | Only in emotisense-ai |
| Utility Generators | ❌ Missing | ✅ PROMPT 11 | ⚠️ GAP | Only in backend_prompts |
| File Regeneration | ❌ Missing | ✅ PROMPT 14 | ⚠️ GAP | Only in backend_prompts |
| **Foundation** |
| Project Setup | ❌ Missing | ✅ PROMPT 01 | ⚠️ GAP | Only in backend_prompts |
| Base Generator | ❌ Missing | ✅ PROMPT 02 | ⚠️ GAP | Only in backend_prompts |

---

## Summary Statistics

### emotisense-ai/prompts/code_generators/
- **Total Prompts:** 21
- **Unique Features:** 8 (Swagger, Role Service, Profile Service, Admin Setup, Account Controller, SQL Parser, App Definition, Test Generator)
- **Missing Features:** 12 (Security Layer 15-23, Utilities, File Regeneration, Project Setup, Base Generator)

### ai_generated_documents/backend_prompts/
- **Total Prompts:** 23
- **Unique Features:** 12 (Security Layer 15-23, Utilities, File Regeneration, Project Setup, Base Generator)
- **Missing Features:** 8 (Swagger, Role Service, Profile Service, Admin Setup, Account Controller, SQL Parser, App Definition, Test Generator)

### Combined Coverage
- **Total Unique Features:** 29
- **Covered in Both:** 10
- **Covered in One Only:** 19
- **Coverage Gap:** 66% of features exist in only one location

---

## Key Differences

### 1. Authorization Approach

**emotisense-ai/prompts/**
- Single PROMPT 06 (Authorization Service)
- Implements record-level authorization
- Dual-layer model (table-level + record-level)
- 4 authorization records pattern
- Group-based authorization included

**backend_prompts/**
- Multiple prompts (15-23): 9 prompts for security layer
- Entity-prefixed access levels (COURSE_READ, INSTITUTION_UPDATE)
- Separate prompts for entity, repository, service, controller, DTO layers
- Dedicated group management prompts (22-23)
- Comprehensive test prompts (21A-21C)

**Question 1:** Which authorization approach should we use?
- Option A: Keep emotisense-ai single-prompt approach (simpler)
- Option B: Adopt backend_prompts multi-prompt approach (more detailed)
- Option C: Merge both approaches

---

### 2. User Management Features

**emotisense-ai/prompts/**
- ✅ PROMPT 14: Role Service (role assignment, management)
- ✅ PROMPT 15: User Profile Service (one-to-one enforcement)
- ✅ PROMPT 16: First-Time Admin Setup (Thymeleaf UI)
- ✅ PROMPT 19: Account Controller (self-service account management)

**backend_prompts/**
- ❌ None of these features

**Question 2:** Should we add these user management features to backend_prompts?
- These are practical features for production applications
- First-time admin setup is especially useful
- Account self-service is standard requirement

---

### 3. API Documentation

**emotisense-ai/prompts/**
- ✅ PROMPT 17: Swagger/OpenAPI Config (comprehensive API docs)

**backend_prompts/**
- ❌ Missing

**Question 3:** Should we add Swagger/OpenAPI to backend_prompts?
- Essential for API documentation
- Enables interactive testing
- Standard in modern APIs

---

### 4. Input Processing

**emotisense-ai/prompts/**
- ✅ PROMPT 12: SQL Parser (converts SQL DDL to JSON)
- ✅ PROMPT 21: Application Definition JSON Generator

**backend_prompts/**
- ❌ Missing both

**Question 4:** Should we add SQL Parser to backend_prompts?
- Allows SQL DDL as input (not just JSON)
- More flexible for users
- Application Definition JSON is useful for documentation

---

### 5. Foundation Components

**emotisense-ai/prompts/**
- ❌ Missing Project Setup orchestrator
- ❌ Missing Base Generator utilities

**backend_prompts/**
- ✅ PROMPT 01: Project Setup (BackendWriter orchestrator)
- ✅ PROMPT 02: Base Generator (utility methods)

**Question 5:** Should we add these to emotisense-ai/prompts/?
- These define the generator's internal structure
- Essential for building the generator itself
- Currently emotisense-ai prompts assume these exist

---

### 6. Advanced Features

**emotisense-ai/prompts/**
- ✅ Test Generator (PROMPT 11) - Full implementation
- ❌ Missing Utility Generators
- ❌ Missing File Regeneration

**backend_prompts/**
- ✅ PROMPT 11: Utility Generators (File storage, CSV, Excel)
- ✅ PROMPT 14: File Regeneration Strategy
- ❌ Test Generator is stub only

**Question 6:** Which test generator should we use?
- emotisense-ai has full implementation
- backend_prompts has only stub

---

## Recommended Actions

### Priority 1: Clarify Authorization Approach
**Need Decision:** Which authorization model to use as the standard?

### Priority 2: Merge Unique Features
**Action:** Add missing features from each location to the other

### Priority 3: Consolidate into Single Location
**Action:** Decide which folder should be the authoritative source

---

## Questions for User (One at a Time)

### Question 1: Authorization Approach

We have two different authorization implementations:

**A. emotisense-ai/prompts/ (Single Prompt)**
- PROMPT 06: Authorization Service
- All authorization logic in one place
- Simpler structure

**B. backend_prompts/ (Multi-Prompt)**
- PROMPT 15-23: 9 separate prompts
- Entity-prefixed access levels
- More detailed, layered approach
- Includes group management

**Which approach should we use as the standard?**
- Keep A (simpler, single prompt)
- Keep B (detailed, multi-layer)
- Merge both (combine best of both)
