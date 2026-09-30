# Authorization Layer - Dynamic Query Removal - v2.5.0

**Date:** March 13, 2026  
**Version:** 2.5.0  
**Status:** ✅ Complete

## Overview

Removed dynamic SQL generation from the authorization layer and updated it to use the new schema design with pre-generated custom queries from the v2.4.0 custom query layer.

## Problem Identified

The authorization layer had dynamic SQL generation in the `QueryExecutor` class that built SQL queries at runtime using string concatenation. This was used for `CUSTOM_QUERY` and `CUSTOM_QUERY_ALL` document group types.

### Security Concerns:
- Runtime SQL string building (even with sanitization)
- Potential for SQL injection if sanitization failed
- Complex query building logic
- Difficult to audit and validate queries

### Schema Mismatch:
- Authorization service templates used old schema with `document_group_definition` table
- Auth schema had been updated to new design with separate scope tables
- `document_group_query_scope` table references `query_name` from custom_queries_layer.json
- Templates didn't align with the actual database schema

## Changes Made

### 1. Updated Authorization Service Templates

**File:** `emotisense-ai/swfaw/templates/authorization_service_templates.py`

**Removed:**
- `QUERY_DEFINITION_MODEL` - Dynamic query definition model
- `QUERY_EXECUTOR` - Dynamic SQL builder with runtime string concatenation

**Added:**
- `ACCESS_CONTROL_CONSTANTS` - Constants for 8 access operations
- `CUSTOM_QUERY_REGISTRY` - Registry for pre-generated custom query executors

**Updated:**
- `DOCUMENT_GROUP_MATCHER` - Complete rewrite to use new schema tables:
  - `document_group_table_scope` - For table-level permissions
  - `document_group_table_record_scope` - For record-level permissions
  - `document_group_query_scope` - For query-based permissions
  - `document_group_query_record_scope` - For specific query records
  - Supports all 9 document group types from new schema
  - Extracts permissions from scope tables (8 ACL flags per scope)
  
- `PERMISSION_RESOLVER` - Updated to work with new schema:
  - Uses `document_group_membership` table
  - Resolves permissions from document group scopes
  - Returns union of all permissions
  
- `AUTHORIZATION_SERVICE_REWRITTEN` - Updated authorization flow:
  - Simplified permission checking
  - Uses PermissionResolver with new schema
  - Removed dependency on old document_group_definition table

### 2. Updated Authorization Service Generator

**File:** `emotisense-ai/swfaw/generators/authorization_service_generator.py`

**Removed methods:**
- `generate_query_definition_model()` - No longer needed
- `generate_query_executor()` - No longer needed

**Added methods:**
- `generate_access_control_constants()` - Generates access control constants
- `generate_custom_query_registry()` - Generates query registry

**Kept methods:**
- `generate_document_group_matcher()` - Updated to use new template
- `generate_permission_resolver()` - Updated to use new template
- `generate_authorization_service_rewritten()` - Updated to use new template

### 3. Updated Main Generation Script

**File:** `emotisense-ai/swfaw/main.py`

**Changed authorization component generation:**
```python
# OLD:
# - Generate QueryDefinition model
# - Generate QueryExecutor
# - Generate AccessLevelConstants (from AuthorizationGenerator)

# NEW:
# - Generate AccessControlConstants (from AuthorizationServiceGenerator)
# - Generate CustomQueryRegistry
# - No more QueryDefinition or QueryExecutor
```

### 4. Updated Version

**File:** `emotisense-ai/swfaw/version.py`

- Bumped version to `2.5.0`
- Updated manifest version to `2.5`
- Added version history entry

## New Authorization Flow

### Document Group Types (9 types):

1. **CREATOR_RECORDS** - Records created by the user (checked at service layer)
2. **SINGLE_RECORD** - Single specific record
3. **MULTIPLE_RECORDS** - Multiple specific records
4. **TABLE_USER** - Entire table with user-level permissions (typically READ only)
5. **TABLE_ADMIN** - Entire table with admin-level permissions (full CRUD)
6. **TABLE_MULTIPLE_USER** - Multiple tables with user-level permissions
7. **TABLE_MULTIPLE_ADMIN** - Multiple tables with admin-level permissions
8. **QUERY_SPECIFIC** - Query with specific records (READ-only, must be in record list AND match query)
9. **QUERY_ALL** - All records matching query (READ-only, grants access to all query results)

### Access Control Operations (8 operations):

1. READ
2. CREATE
3. UPDATE
4. DELETE
5. GRANT_ACCESS
6. EXPORT
7. SHARE
8. AUDIT

### Authorization Check Flow:

```
1. Check if user is super user
   └─> If yes: Grant access (with justification for DELETE)
   
2. Check if user is in super group
   └─> If yes: Grant access
   
3. Find matching document groups for table/record
   └─> Query scope tables based on document group type
   └─> Extract permissions from scope (8 ACL flags)
   
4. Check if user has membership in any matching document groups
   └─> Check direct user membership
   └─> Check group membership (via user_group_membership)
   
5. Resolve permissions (union of all matching groups)
   └─> Return set of allowed access controls
   
6. Check if requested access control is in allowed set
   └─> Grant or deny access
   
7. Log access attempt to audit log
```

### Query-Based Authorization:

For `QUERY_SPECIFIC` and `QUERY_ALL` document group types:

1. Query scope references a `query_name` from `query_layer.json`
2. CustomQueryRegistry looks up the pre-generated query executor
3. Executor calls the type-safe custom query repository method
4. No dynamic SQL generation - all queries pre-built at code generation time

**Example:**
```java
// In CustomQueryRegistry initialization
queryExecutors.put("findActiveUsers", (tableName, recordId) -> 
    userCustomQueryRepository.checkActiveUser(recordId)
);

// At runtime
customQueryRegistry.executeQuery("findActiveUsers", "users", 123)
```

## Benefits

### Security:
- ✅ No dynamic SQL generation at runtime
- ✅ All queries pre-generated and type-safe
- ✅ Queries validated at code generation time
- ✅ No SQL injection risk
- ✅ Easier to audit and review queries

### Performance:
- ✅ No runtime query building overhead
- ✅ Queries can be optimized at generation time
- ✅ Better query plan caching

### Maintainability:
- ✅ Aligns with v2.4.0 custom query layer
- ✅ Consistent query definition approach
- ✅ Matches actual database schema
- ✅ Cleaner separation of concerns

### Flexibility:
- ✅ Still supports complex authorization queries
- ✅ Queries defined in JSON (version controlled)
- ✅ Can be customized before code generation
- ✅ Supports all 9 document group types

## Migration Notes

### For Existing Applications:

If you have an existing application generated with v2.4.0 or earlier:

1. **Database Schema:** The auth schema already has the new tables, so no migration needed
2. **Authorization Queries:** Define any custom authorization queries in `query_layer.json`
3. **Regenerate Code:** Run Phase 2 to regenerate with new authorization service
4. **Update Document Groups:** Migrate from old `document_group_definition` to new scope tables

### For New Applications:

1. Define custom queries in `query_layer.json` (Phase 1)
2. Reference query names in `document_group_query_scope` table
3. Authorization will use pre-generated query executors

## Files Modified

1. `templates/authorization_service_templates.py` - Complete rewrite
2. `generators/authorization_service_generator.py` - Updated methods
3. `main.py` - Updated authorization component generation
4. `version.py` - Bumped to 2.5.0

## Testing Recommendations

1. Test all 9 document group types
2. Test query-based authorization (QUERY_SPECIFIC, QUERY_ALL)
3. Test permission resolution (union of permissions)
4. Test super user and super group access
5. Test audit logging
6. Verify no SQL injection vulnerabilities
7. Performance test authorization checks

## Next Steps

1. Generate a test application to verify changes
2. Test authorization with all document group types
3. Update documentation
4. Consider adding authorization query examples
5. Add integration tests for authorization layer

---

**Implementation Status:** ✅ Complete  
**Version:** 2.5.0  
**Security:** ✅ No dynamic SQL generation  
**Schema Alignment:** ✅ Matches auth schema design
