# Task 8: Table Admin Authorization Clarification - COMPLETE

## Status: ✅ DONE

## User Clarification

**User stated:** "Table level admin has access to create a record, but can view, update, or delete only if he is given access."

This is a critical clarification that changes the authorization model significantly.

## Previous (Incorrect) Model

**Before:**
- SYSTEM_ADMIN → Full access to all tables and all records
- TABLE_ADMIN (e.g., COURSE_ADMIN) → Full access to all records in that table
- Regular users → Need record-level authorization

**Problem:** TABLE_ADMIN could access ANY record in their table, which is too permissive.

## Corrected Model

**After:**
- SYSTEM_ADMIN → Full access to all tables and all records (ONLY role that bypasses record-level checks)
- TABLE_ADMIN (e.g., COURSE_ADMIN) → Can CREATE new records, but needs record-level authorization for READ/UPDATE/DELETE
- TABLE_CREATOR → Can CREATE new records, but needs record-level authorization for READ/UPDATE/DELETE
- Regular users → Need record-level authorization for all operations

**Key Change:** TABLE_ADMIN and TABLE_CREATOR can only CREATE. For READ/UPDATE/DELETE, they need explicit authorization just like regular users.

## Authorization Flow

### CREATE Operation
```
User has TABLE_ADMIN or TABLE_CREATOR role?
├─ YES → ALLOW (can create)
└─ NO → Check record-level authorization
```

### READ/UPDATE/DELETE Operations
```
User has SYSTEM_ADMIN role?
├─ YES → ALLOW (bypass record-level checks)
└─ NO → Check record-level authorization
    ├─ Has authorization record? → ALLOW
    └─ No authorization record? → DENY
```

## Examples

### Example 1: COURSE_ADMIN creates a course
```
User: John (COURSE_ADMIN)
Action: Create Course

Result: ✓ ALLOWED (has COURSE_ADMIN role)
- Course created
- John gets 4 authorization records (CREATE, READ, UPDATE, DELETE)
- John can now access THIS course
```

### Example 2: COURSE_ADMIN tries to access another admin's course
```
User: John (COURSE_ADMIN)
Action: Read Course #123 (created by Alice)

Check:
1. Has SYSTEM_ADMIN? NO
2. Operation is READ (not CREATE)
3. Check record-level authorization
4. John has NO authorization records for Course #123

Result: ✗ DENIED
```

### Example 3: SYSTEM_ADMIN accesses any course
```
User: SuperAdmin (SYSTEM_ADMIN)
Action: Read Course #123

Check:
1. Has SYSTEM_ADMIN? YES

Result: ✓ ALLOWED (bypass record-level checks)
```

### Example 4: COURSE_ADMIN granted access to specific course
```
User: John (COURSE_ADMIN)
Action: Read Course #123
Previous: Alice granted John READ access

Check:
1. Has SYSTEM_ADMIN? NO
2. Operation is READ (not CREATE)
3. Check record-level authorization
4. John has READ authorization record for Course #123

Result: ✓ ALLOWED
```

## Code Changes

### AuthorizationService.hasAccess()

**Before:**
```java
if (hasSystemAdminRole(user)) {
    return Mono.just(true);
}

String tableAdminRole = entityType.toUpperCase() + "_ADMIN";
if (hasRole(user, tableAdminRole)) {
    return Mono.just(true);  // ← TABLE_ADMIN bypassed all checks
}

return checkRecordLevelAccess(...);
```

**After:**
```java
// SYSTEM_ADMIN bypasses ALL checks
if (hasSystemAdminRole(user)) {
    return Mono.just(true);
}

// For CREATE operations, check table-level roles
if ("CREATE".equalsIgnoreCase(accessLevel)) {
    String tableAdminRole = entityType.toUpperCase() + "_ADMIN";
    String tableCreatorRole = entityType.toUpperCase() + "_CREATOR";
    
    if (hasRole(user, tableAdminRole) || hasRole(user, tableCreatorRole)) {
        return Mono.just(true);  // ← Only for CREATE
    }
}

// For READ/UPDATE/DELETE, check record-level authorization
// (TABLE_ADMIN also needs record-level authorization)
return checkRecordLevelAccess(...);
```

### AuthorizationService.findAccessibleEntityIds()

**Before:**
```java
// Table-level admins have access to all entities
if (hasSystemAdminRole(user) || hasTableAdminRole(user, entityType)) {
    return Flux.empty(); // Special case: means "all"
}

return authorizationRepository.findAccessibleEntityIds(...);
```

**After:**
```java
// Only SYSTEM_ADMIN has access to all entities
if (hasSystemAdminRole(user)) {
    return Flux.empty(); // Special case: means "all"
}

// TABLE_ADMIN also needs record-level authorization
return authorizationRepository.findAccessibleEntityIds(...);
```

## Files Updated

1. **RECORD_LEVEL_AUTHORIZATION_SPECIFICATION.md**
   - Updated authorization flow diagram
   - Updated access levels description
   - Updated Example 2 (COURSE_ADMIN creates course)
   - Added Example 3 (COURSE_ADMIN tries to access another admin's course)
   - Added Example 4 (SYSTEM_ADMIN accesses any course)
   - Updated AuthorizationService.hasAccess() code
   - Updated AuthorizationService.findAccessibleEntityIds() code
   - Updated service layer findAccessibleForCurrentUser() code
   - Updated Key Features section
   - Updated Authorization Layers section

## Impact

### Security Improvement
- More granular control over access
- TABLE_ADMIN cannot access all records (prevents unauthorized access)
- Only SYSTEM_ADMIN has unrestricted access

### Use Cases
1. **Multiple Course Admins**: Each COURSE_ADMIN can create courses, but can only access courses they created or were granted access to
2. **Department Isolation**: COURSE_ADMIN for Math department cannot access COURSE_ADMIN's courses from Science department
3. **Privacy**: User profiles can only be accessed by the user themselves or those granted access (even USER_ADMIN needs authorization)

### When TABLE_ADMIN Gets Access
When a TABLE_ADMIN creates a record, they automatically get 4 authorization records:
```sql
INSERT INTO ems_entity_authorization VALUES
('Course', 123, admin_user_id, 'CREATE', admin_user_id),
('Course', 123, admin_user_id, 'READ', admin_user_id),
('Course', 123, admin_user_id, 'UPDATE', admin_user_id),
('Course', 123, admin_user_id, 'DELETE', admin_user_id);
```

This gives them full access to THAT specific record.

### Granting Access Between Admins
If Alice (COURSE_ADMIN) wants to give John (COURSE_ADMIN) access to her course:
```java
authorizationService.grantAccess("Course", 123L, johnUserId, "READ");
// Or grant full access
authorizationService.grantAccess("Course", 123L, johnUserId, "CREATE");
authorizationService.grantAccess("Course", 123L, johnUserId, "READ");
authorizationService.grantAccess("Course", 123L, johnUserId, "UPDATE");
authorizationService.grantAccess("Course", 123L, johnUserId, "DELETE");
```

## Summary

The corrected authorization model provides:
- **Tighter security**: TABLE_ADMIN cannot access all records
- **Granular control**: Per-record authorization for everyone (except SYSTEM_ADMIN)
- **Clear separation**: CREATE vs READ/UPDATE/DELETE permissions
- **Flexibility**: Admins can grant access to each other when needed
- **Privacy**: Records are private by default, even from table admins

This model is more secure and provides better isolation between users, even those with admin roles.
