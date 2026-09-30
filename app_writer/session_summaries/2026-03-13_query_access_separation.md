# Session Summary: Query Access Separation from Table/Record Access

**Date:** March 13, 2026  
**Version:** 2.5.0  
**Status:** ✅ Complete

## Overview

Separated query-based access from table/record CRUD access in the authorization layer. Query access and table/record access are now two completely independent authorization paths.

## Problem Identified

The authorization flow was incorrectly treating query access as a criteria for granting CRUD access to tables and records:

1. `DocumentGroupMatcher.matchesDocumentGroup()` was evaluating QUERY_SPECIFIC and QUERY_ALL types
2. Query access was being mixed with table/record access in permission resolution
3. Query access (READ-only views) was being used to grant CRUD operations

**This was incorrect because:**
- Query access grants READ-only access to query results (custom query endpoints)
- Table/record access grants CRUD operations (entity endpoints)
- These are two different access paths and should NOT be mixed

## Changes Made

### 1. DocumentGroupMatcher - Separated Access Flows

**File:** `emotisense-ai/swfaw/templates/authorization_service_templates.py`

#### New Methods:

```java
// For TABLE/RECORD CRUD access only
public Mono<Map<Long, Set<String>>> findMatchingDocumentGroupsWithPermissions(
    String tableName, Long recordId)

// For query access only (separate flow)
public Mono<Map<Long, String>> findMatchingDocumentGroupsForQueryAccess(
    String queryName)

// Validate query access for specific records
public Mono<Boolean> hasQueryAccess(
    Long documentGroupId, String queryName, String tableName, Long recordId)
```

#### Updated Logic:

**matchesDocumentGroupForTableAccess()** - Handles 7 table/record types:
- CREATOR_RECORDS
- SINGLE_RECORD
- MULTIPLE_RECORDS
- TABLE_USER
- TABLE_ADMIN
- TABLE_MULTIPLE_USER
- TABLE_MULTIPLE_ADMIN
- **Excludes:** QUERY_SPECIFIC, QUERY_ALL (returns empty set)

**matchesDocumentGroupForQueryAccess()** - Handles 2 query types:
- QUERY_SPECIFIC
- QUERY_ALL
- Returns query name if access granted

### 2. AuthorizationService - New Query Access Method

**File:** `emotisense-ai/swfaw/templates/authorization_service_templates.py`

#### New Method:

```java
/**
 * Check if user has READ access to a custom query
 * Query access is completely separate from table/record CRUD access
 * Query access is always READ-only
 */
public Mono<Boolean> hasQueryAccess(
    Long authUserId, 
    String queryName,
    String tableName,
    Long recordId)
```

#### Authorization Flow for Query Access:

1. Check if user is super user → Grant access
2. Check if user is in super group → Grant access
3. Check document group memberships:
   - Get user's group memberships
   - Find document groups that grant this query access
   - Check if user has membership (direct or via group)
   - Verify query access for specific record (if applicable)

#### Helper Method:

```java
private Mono<Boolean> checkQueryAccessViaDocumentGroups(
    Long authUserId,
    String queryName,
    String tableName,
    Long recordId,
    LocalDateTime now)
```

### 3. PermissionResolver - Clarified Scope

**File:** `emotisense-ai/swfaw/templates/authorization_service_templates.py`

Added documentation clarifying that `resolvePermissions()` and `hasPermission()` are for TABLE/RECORD CRUD access only, NOT for query access.

### 4. Updated Dependencies

**AuthorizationService** now injects:
- `DocumentGroupMatcher` - For query access validation
- `DocumentGroupMembershipRepository` - For checking memberships

## Access Control Separation

### Table/Record Access (CRUD Operations)

**Purpose:** Grant CRUD permissions on entity endpoints

**Access Controls:**
- READ
- CREATE
- UPDATE
- DELETE
- GRANT_ACCESS
- EXPORT
- SHARE
- AUDIT

**Document Group Types:**
- CREATOR_RECORDS
- SINGLE_RECORD
- MULTIPLE_RECORDS
- TABLE_USER
- TABLE_ADMIN
- TABLE_MULTIPLE_USER
- TABLE_MULTIPLE_ADMIN

**Authorization Method:** `AuthorizationService.hasAccess()`

### Query Access (READ-Only Views)

**Purpose:** Grant READ-only access to custom query endpoints

**Access Controls:**
- READ only (always)

**Document Group Types:**
- QUERY_SPECIFIC (specific records)
- QUERY_ALL (all matching records)

**Authorization Method:** `AuthorizationService.hasQueryAccess()`

## Usage Examples

### Table/Record CRUD Access

```java
// Check if user can UPDATE a specific record
boolean canUpdate = authorizationService.hasAccess(
    authUserId, 
    "users", 
    userId, 
    "UPDATE"
).block();

// Check if user can CREATE in a table
boolean canCreate = authorizationService.hasTableAccess(
    authUserId, 
    "users", 
    "CREATE"
).block();
```

### Query Access

```java
// Check if user can access a custom query
boolean canAccessQuery = authorizationService.hasQueryAccess(
    authUserId,
    "findActiveUsers",  // query name from custom_queries_layer.json
    "users",            // optional: table name
    null                // optional: record ID for SPECIFIC_RECORDS mode
).block();

// Check query access for specific record
boolean canAccessRecord = authorizationService.hasQueryAccess(
    authUserId,
    "findActiveUsers",
    "users",
    userId  // specific record
).block();
```

## Schema Design

### Query Scope Tables

**document_group_query_scope:**
- Links document group to query name
- `scope_mode`: SPECIFIC_RECORDS or ALL_MATCHING
- Query name references `custom_queries_layer.json`

**document_group_query_record_scope:**
- For SPECIFIC_RECORDS mode only
- Lists specific records user can access via query

### No Dynamic SQL

Query access references pre-generated queries in `custom_queries_layer.json`. No SQL is stored or generated dynamically in the database.

## Benefits

1. **Clear Separation:** Query access and CRUD access are independent
2. **Security:** Query access is always READ-only
3. **Flexibility:** Users can have query access without CRUD permissions
4. **Maintainability:** Two separate authorization flows are easier to understand
5. **Correctness:** Query results don't grant CRUD operations

## Testing Recommendations

1. **Test query access doesn't grant CRUD:**
   - User with QUERY_ALL access should NOT be able to UPDATE/DELETE
   - Query access should only work on query endpoints

2. **Test CRUD access doesn't grant query access:**
   - User with TABLE_ADMIN access should NOT automatically access queries
   - Queries require explicit query-based document groups

3. **Test super user/group:**
   - Super users should have both CRUD and query access
   - Super groups should have both CRUD and query access

4. **Test SPECIFIC_RECORDS mode:**
   - User should only see records in query_record_scope table
   - Records not in scope should be denied

5. **Test ALL_MATCHING mode:**
   - User should see all results from the query
   - No record-level filtering

## Files Modified

1. `emotisense-ai/swfaw/templates/authorization_service_templates.py`
   - Updated `DocumentGroupMatcher` class
   - Updated `AuthorizationService` class
   - Updated `PermissionResolver` class

## Version

This change is part of swfaw_v2 version 2.5.0.

## Related Documentation

- `2026-03-13_authorization_dynamic_query_removal.md` - Removal of dynamic SQL generation
- `2026-03-13_v2.5_complete_summary.md` - Complete v2.5.0 summary
- `2026-03-13_v2.5_cleanup_status.md` - Cleanup status

## Next Steps

1. Generate a test application to validate the changes
2. Test both authorization flows independently
3. Update any custom query controllers to use `hasQueryAccess()`
4. Document query access patterns for end users
