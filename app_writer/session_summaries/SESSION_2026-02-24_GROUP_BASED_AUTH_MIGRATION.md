# Session Summary: Migration to Group-Based Authorization

**Date:** February 24, 2026  
**Topic:** Transition from Role-Based to Pure Group-Based Authorization  
**Status:** In Progress

---

## Overview

Migrated the Spring WebFlux Application Generator from a hybrid role-based + group-based authorization system to a pure group-based system with only 5 operations.

---

## Key Changes

### 1. Authorization Model

**OLD MODEL:**
- Roles (ems_role, ems_auth_user_role) for table-level permissions
- Groups (ems_user_group, ems_user_group_membership) for record-level permissions
- Complex access levels (READ, CREATE, UPDATE, DELETE, ADMIN)

**NEW MODEL:**
- Groups ONLY (ems_user_group, ems_user_group_membership) for ALL permissions
- Five operations: CREATE, READ, UPDATE, DELETE, GRANT_ACCESS
- Simplified hierarchy: GRANT_ACCESS > DELETE > UPDATE > CREATE > READ
- Admin group management with table-level permissions
- Default groups for automatic assignment on registration

### 2. Database Schema Changes

**REMOVED TABLES:**
- `ems_role` - No longer needed
- `ems_auth_user_role` - No longer needed

**MODIFIED TABLES:**
- `ems_user_group` - Added `group_type` field ('SYSTEM', 'TABLE', 'RECORD', 'CUSTOM')
- `ems_user_group` - Added `is_default_group` field (for auto-assignment on registration)
- `ems_entity_authorization` - Changed `access_level` to `access_operation` (5 operations only)

**NEW TABLES:**
- `ems_group_table_permission` - Stores table-level permissions for groups (canCreate, canManageAll)

**KEPT TABLES:**
- `ems_auth_user` - Authentication credentials
- `ems_auth_user_link` - Links auth to app users
- `ems_user_group` - User groups
- `ems_user_group_membership` - Group memberships
- `ems_entity_authorization` - Authorization records (group-based only)

### 3. Default Groups (Replaces Default Roles)

**System Groups:**
```sql
INSERT INTO ems_user_group (group_name, group_type, description) VALUES
('SYSTEM_ADMINS', 'SYSTEM', 'System administrators with full access');
```

**Table Groups (Generated per entity):**
```sql
INSERT INTO ems_user_group (group_name, group_type, description) VALUES
('COURSE_ADMINS', 'TABLE', 'Can create and manage all courses'),
('COURSE_CREATORS', 'TABLE', 'Can create courses and manage own courses'),
('INSTITUTION_ADMINS', 'TABLE', 'Can create and manage all institutions'),
('INSTITUTION_CREATORS', 'TABLE', 'Can create institutions and manage own institutions');
```

**Personal Groups (Created automatically):**
- Format: `USER_{auth_user_id}_PERSONAL`
- Created when user creates their first entity
- Used for creator's default access

### 4. Authorization Flow Changes

**OLD FLOW:**
1. Check if user has SYSTEM_ADMIN role → Allow
2. Check if user has TABLE_ADMIN or TABLE_CREATOR role → Allow CREATE
3. Check record-level authorization (user-based or group-based)

**NEW FLOW:**
1. Check if user is in SYSTEM_ADMINS group → Allow
2. Check if user is in {TABLE}_ADMINS or {TABLE}_CREATORS group → Allow CREATE
3. Check record-level authorization (group-based only)

### 5. Entity Creation Pattern

**OLD PATTERN (4 records):**
```sql
INSERT INTO ems_entity_authorization VALUES
('Course', 123, 5, NULL, 'CREATE', 5),   -- user_id=5
('Course', 123, 5, NULL, 'READ', 5),
('Course', 123, 5, NULL, 'UPDATE', 5),
('Course', 123, 5, NULL, 'DELETE', 5);
```

**NEW PATTERN (5 records via personal group):**
```sql
-- 1. Create/get personal group
INSERT INTO ems_user_group (group_name, group_type, created_by_auth_user_id)
VALUES ('USER_5_PERSONAL', 'RECORD', 5);  -- group_id=10

-- 2. Add user to personal group
INSERT INTO ems_user_group_membership (auth_user_id, group_id, added_by_auth_user_id)
VALUES (5, 10, 5);

-- 3. Grant 5 operations to personal group
INSERT INTO ems_entity_authorization VALUES
('Course', 123, 10, 'READ', 5),          -- group_id=10
('Course', 123, 10, 'CREATE', 5),
('Course', 123, 10, 'UPDATE', 5),
('Course', 123, 10, 'DELETE', 5),
('Course', 123, 10, 'GRANT_ACCESS', 5);
```

---

## New Features

### 1. Admin Group Management (PROMPT 22A)

System administrators can now:

**Create Groups with Permissions:**
```json
POST /api/admin/groups
{
  "groupName": "COURSE_CREATORS",
  "groupType": "TABLE",
  "description": "Users who can create courses",
  "isDefaultGroup": false,
  "tablePermissions": [
    {
      "entityType": "Course",
      "canCreate": true,
      "canManageAll": false
    }
  ]
}
```

**Set Default Groups:**
```
PUT /api/admin/groups/5/default?isDefault=true
```

**Update Group Permissions:**
```json
PUT /api/admin/groups/5/permissions
[
  {
    "entityType": "Course",
    "canCreate": true,
    "canManageAll": false
  }
]
```

### 2. Default Group Assignment

- Groups can be marked as "default" (`is_default_group = true`)
- New users are automatically added to all default groups during registration
- Simplifies onboarding and permission management
- Multiple default groups supported

### 3. Table-Level Permissions

New table: `ems_group_table_permission`

**Fields:**
- `canCreate` - Group members can create entities of this type
- `canManageAll` - Group members can manage ALL entities of this type (admin-level)

**Example:**
- COURSE_CREATORS group: canCreate=true, canManageAll=false
- COURSE_ADMINS group: canCreate=true, canManageAll=true
VALUES ('USER_5_PERSONAL', 'RECORD', 5);  -- group_id=10

-- 2. Add user to personal group
INSERT INTO ems_user_group_membership (auth_user_id, group_id, added_by_auth_user_id)
VALUES (5, 10, 5);

-- 3. Grant 5 operations to personal group
INSERT INTO ems_entity_authorization VALUES
('Course', 123, 10, 'READ', 5),          -- group_id=10
('Course', 123, 10, 'CREATE', 5),
('Course', 123, 10, 'UPDATE', 5),
('Course', 123, 10, 'DELETE', 5),
('Course', 123, 10, 'GRANT_ACCESS', 5);
```

---

## Files Updated

### ✅ Completed

1. **00_AUTHORIZATION_SYSTEM_OVERVIEW.md**
   - Completely rewritten for group-based model
   - Updated architecture diagrams
   - Changed from 3-tier to 2-tier model
   - Updated all examples and queries

2. **12_AUTHENTICATION_DDL.md** (Partial)
   - Removed role table definitions
   - Added group table definitions
   - Updated default data from roles to groups
   - Updated permission matrix
   - Updated example scenarios

3. **22_GROUP_MANAGEMENT_LAYER.md** (Updated)
   - Added `group_type` field to UserGroup entity
   - Added `is_default_group` field to UserGroup entity

4. **22A_ADMIN_GROUP_MANAGEMENT.md** (NEW)
   - Admin-only group creation with permissions
   - Table-level permission management (canCreate, canManageAll)
   - Default group assignment for new user registration
   - Group permission CRUD operations
   - Integration with registration flow

5. **26_FIRST_TIME_ADMIN_SETUP.md**
   - Updated to use SYSTEM_ADMINS group instead of SYSTEM_ADMIN role
   - Changed admin creation to add user to group
   - Updated all references and examples

### 🔄 Needs Update

3. **13_AUTHORIZATION_SERVICE.md**
   - Remove role-checking methods
   - Update to use group membership checks
   - Change `hasRole()` to `isInGroup()`
   - Update `hasAccess()` to check groups only
   - Update `createDefaultAuthorization()` to create personal group + 5 records

4. **22_GROUP_MANAGEMENT_LAYER.md**
   - Already mostly correct (groups exist)
   - Add group_type field handling
   - Add personal group creation logic
   - Update to support SYSTEM, TABLE, RECORD, CUSTOM types

5. **23_GROUP_BASED_AUTHORIZATION.md**
   - Already correct (group-based auth exists)
   - Update to reflect it's the ONLY auth method (not hybrid)
   - Remove references to user-based authorization
   - Update to 5 operations model

6. **24_ROLE_SERVICE.md**
   - DELETE THIS FILE (no longer needed)
   - Replace with group management in 22_GROUP_MANAGEMENT_LAYER.md

7. **06_SERVICE_LAYER.md**
   - Remove `@PreAuthorize("hasRole(...)")` annotations
   - Update authorization checks to use AuthorizationService
   - Remove role-based CREATE checks
   - Add group-based CREATE checks

8. **07_CONTROLLER_LAYER.md**
   - Remove `@PreAuthorize("hasRole(...)")` annotations
   - Update to use service-layer authorization
   - Remove role references from documentation

9. **09_JWT_AUTHENTICATION.md**
   - Remove role claims from JWT
   - Add group membership to JWT (optional)
   - Update token generation/validation

10. **10_SECURITY_CONFIG.md**
    - Remove role-based security rules
    - Update to authentication-only (authorization in services)

11. **16_SECURITY_ENTITY_LAYER.md**
    - Remove Role, AuthUserRole entities
    - Ensure UserGroup, UserGroupMembership entities are correct

12. **17_SECURITY_REPOSITORY_LAYER.md**
    - Remove RoleRepository, AuthUserRoleRepository
    - Ensure UserGroupRepository, UserGroupMembershipRepository are correct

18. **18_SECURITY_SERVICE_LAYER.md**
    - Remove RoleService
    - Update AuthorizationService to group-based only
    - Update UserProfileService to use groups

19. **19_SECURITY_CONTROLLER_LAYER.md**
    - Remove role management endpoints
    - Keep group management endpoints
    - Update authorization endpoints

20. **25_USER_PROFILE_SERVICE.md**
    - Remove role assignment logic
    - Add default group assignment logic
    - Update registration to add users to appropriate groups

26. **26_FIRST_TIME_ADMIN_SETUP.md**
    - Change from assigning SYSTEM_ADMIN role
    - Change to adding user to SYSTEM_ADMINS group

### 📋 Reference Documents

27. **RECORD_LEVEL_AUTHORIZATION_SPECIFICATION.md**
    - Update all role references to groups
    - Update access levels to 5 operations
    - Update code examples

28. **ROLES_CONFIGURATION_SPECIFICATION.md**
    - RENAME to GROUPS_CONFIGURATION_SPECIFICATION.md
    - Update all role references to groups
    - Update configuration schema

29. **TWO_PHASE_ARCHITECTURE_SUMMARY.md** (reference)
    - Update role references to groups

30. **DEFAULT_ROLES_AND_GROUPS_CONFIGURATION.md** (reference)
    - RENAME to DEFAULT_GROUPS_CONFIGURATION.md
    - Remove role sections
    - Keep only group sections

---

## Code Generation Changes

### Entity Layer

**Remove:**
- `Role.java`
- `AuthUserRole.java`

**Keep/Update:**
- `AuthUser.java` - Change `List<Role> roles` to `List<UserGroup> groups`
- `UserGroup.java` - Add `groupType` field
- `UserGroupMembership.java` - Already correct
- `EntityAuthorization.java` - Change `accessLevel` to `accessOperation`

### Repository Layer

**Remove:**
- `RoleRepository.java`
- `AuthUserRoleRepository.java`

**Keep:**
- `UserGroupRepository.java`
- `UserGroupMembershipRepository.java`
- `EntityAuthorizationRepository.java` - Update queries for operations

### Service Layer

**Remove:**
- `RoleService.java`

**Update:**
- `AuthorizationService.java` - Group-based only, 5 operations
- `UserGroupService.java` - Add group type handling
- `UserProfileService.java` - Use groups instead of roles
- `FirstTimeSetupService.java` - Add to SYSTEM_ADMINS group

**All Entity Services:**
- Remove `@PreAuthorize("hasRole(...)")` annotations
- Add authorization checks via `AuthorizationService`
- Update CREATE checks to use group membership

### Controller Layer

**Remove:**
- Role management endpoints

**Keep:**
- Group management endpoints
- Authorization endpoints (grant/revoke)

**Update:**
- Remove `@PreAuthorize("hasRole(...)")` annotations
- Authorization handled in service layer

---

## Migration Strategy

### Phase 1: Core Schema (Completed)
- ✅ Update authorization overview document
- ✅ Update authentication DDL (partial)
- ✅ Define new group structure

### Phase 2: Service Layer (Next)
- Update AuthorizationService
- Update UserGroupService
- Remove RoleService
- Update entity services

### Phase 3: Controller Layer
- Remove role endpoints
- Update authorization endpoints
- Remove @PreAuthorize annotations

### Phase 4: Security Configuration
- Update JWT to exclude roles
- Update SecurityConfig
- Update authentication flow

### Phase 5: Testing & Documentation
- Update test files
- Update reference documents
- Update configuration specifications

---

## Key Concepts for Developers

### 1. No More Roles
- Everything is group-based
- Users belong to groups
- Groups have permissions on entities

### 2. Five Operations Only
- CREATE - Can create child entities
- READ - Can view entity
- UPDATE - Can modify entity (includes READ)
- DELETE - Can delete entity (includes UPDATE, READ)
- GRANT_ACCESS - Can grant/revoke access (includes all)

### 3. Group Types
- **SYSTEM** - System-wide groups (SYSTEM_ADMINS)
- **TABLE** - Table-level groups ({TABLE}_ADMINS, {TABLE}_CREATORS)
- **RECORD** - Record-level groups (personal groups, team groups)
- **CUSTOM** - User-defined groups

### 4. Personal Groups
- Every user gets a personal group on first entity creation
- Format: `USER_{auth_user_id}_PERSONAL`
- Used for creator's default access
- Automatically granted all 5 operations on created entities

### 5. Authorization Checks
```java
// OLD (role-based)
@PreAuthorize("hasRole('COURSE_ADMIN')")
public Mono<Void> delete(Long id) { }

// NEW (group-based, in service)
public Mono<Void> delete(Long id) {
    return authorizationService.hasAccess("Course", id, "DELETE")
        .flatMap(hasAccess -> {
            if (!hasAccess) return Mono.error(new AccessDeniedException(...));
            return repository.deleteById(id);
        });
}
```

### 6. CREATE Permission Checks
```java
// OLD (role-based)
@PreAuthorize("hasAnyRole('COURSE_CREATOR', 'COURSE_ADMIN', 'SYSTEM_ADMIN')")
public Mono<CourseOutputDTO> create(CourseInputDTO dto) { }

// NEW (group-based)
public Mono<CourseOutputDTO> create(CourseInputDTO dto) {
    return authorizationService.canCreateEntity("Course")
        .flatMap(canCreate -> {
            if (!canCreate) return Mono.error(new AccessDeniedException(...));
            // Create entity + personal group + 5 authorization records
            return createEntityWithAuthorization(dto);
        });
}
```

---

## Benefits of Group-Based Model

1. **Simpler** - One authorization mechanism (groups) instead of two (roles + groups)
2. **More Flexible** - Groups can be created dynamically by users
3. **Team-Oriented** - Natural fit for team collaboration
4. **Scalable** - Easier to manage permissions for large teams
5. **Clearer** - 5 operations instead of complex access levels
6. **Consistent** - Same mechanism for table-level and record-level permissions

---

## Next Steps

1. Complete updating 12_AUTHENTICATION_DDL.md
2. Update 13_AUTHORIZATION_SERVICE.md
3. Update 22_GROUP_MANAGEMENT_LAYER.md
4. Delete 24_ROLE_SERVICE.md
5. Update all service layer prompts (06_SERVICE_LAYER.md)
6. Update all controller layer prompts (07_CONTROLLER_LAYER.md)
7. Update security configuration prompts
8. Update reference documents
9. Create migration guide for existing applications
10. Update test generation prompts

---

## Questions & Decisions

### Q1: Should JWT tokens include group membership?
**Decision:** Optional. Groups can be loaded on-demand from database. Including in JWT makes token larger but reduces database queries.

### Q2: Can users create their own groups?
**Decision:** Yes. Any authenticated user can create CUSTOM type groups. Only admins can create SYSTEM and TABLE type groups.

### Q3: How to handle first-time setup?
**Decision:** First user is automatically added to SYSTEM_ADMINS group. Subsequent admins must be added by existing admins.

### Q4: Can a user belong to multiple groups?
**Decision:** Yes. Users inherit permissions from ALL their groups. Highest operation level wins.

### Q5: What happens to existing applications using roles?
**Decision:** Migration script needed to:
1. Create groups from roles
2. Convert role assignments to group memberships
3. Update authorization records
4. Drop role tables

---

## Status

**Current:** Phase 1 partially complete  
**Next:** Complete Phase 1, begin Phase 2  
**Estimated Completion:** 2-3 days for all prompts

---

**End of Session Summary**
