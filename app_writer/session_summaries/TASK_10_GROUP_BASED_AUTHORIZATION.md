# Task 10: Group-Based Authorization - COMPLETE

## Status: ✅ DONE

## User Request

"We can also grant access to record, document, custom queries to user groups as well, a user can belong to multiple groups."

## Summary

Extended the authorization system to support user groups. Users can now:
- Belong to multiple groups
- Inherit permissions from all their groups
- Be granted access individually OR through group membership
- Automatically gain/lose access when added/removed from groups

This provides powerful permission management capabilities while maintaining the single-table authorization model.

## Database Schema Changes

### New Tables

#### 1. ems_user_group
Stores user groups (departments, teams, roles, etc.)

```sql
CREATE TABLE ems_user_group (
    group_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    group_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_by_user_id BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL
);
```

#### 2. ems_user_group_membership
Tracks which users belong to which groups

```sql
CREATE TABLE ems_user_group_membership (
    membership_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    group_id BIGINT NOT NULL,
    added_by_user_id BIGINT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    
    UNIQUE KEY uk_user_group (user_id, group_id, deleted_at)
);
```

### Modified Table

#### ems_entity_authorization
Now supports EITHER user_id OR group_id (not both)

```sql
CREATE TABLE ems_entity_authorization (
    authorization_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    entity_type VARCHAR(100) NOT NULL,
    entity_id BIGINT NOT NULL,
    
    -- EITHER user_id OR group_id (not both)
    user_id BIGINT NULL,      -- User who has access (NULL if group-based)
    group_id BIGINT NULL,     -- Group that has access (NULL if user-based)
    
    access_level VARCHAR(50) NOT NULL,
    granted_by_user_id BIGINT,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP NULL,
    
    -- Constraint: Either user_id or group_id must be set (not both, not neither)
    CHECK ((user_id IS NOT NULL AND group_id IS NULL) OR (user_id IS NULL AND group_id IS NOT NULL))
);
```

## Authorization Model

### User-Based Authorization (Existing)
```sql
-- Grant READ access to specific user
INSERT INTO ems_entity_authorization VALUES
('Course', 123, 10, NULL, 'READ', 5);  -- user_id=10
```

### Group-Based Authorization (NEW)
```sql
-- Grant READ access to entire group
INSERT INTO ems_entity_authorization VALUES
('Course', 123, NULL, 1, 'READ', 5);  -- group_id=1
```

### Combined Authorization
Users get the HIGHEST access level from:
1. Direct user-based grants
2. All group memberships

## Use Cases

### 1. Department-Based Access

```
Groups:
- Math Department (group_id=1)
- Science Department (group_id=2)

Users:
- Alice: Math Department
- Bob: Science Department
- Charlie: Math Department

Grant READ access to Math Department for Course #123:
→ Alice and Charlie can read Course #123
→ Bob cannot (different department)
```

### 2. Role-Based Access

```
Groups:
- Course Reviewers (group_id=3)
- Content Editors (group_id=4)

Users:
- Alice: Math Department + Course Reviewers
- Charlie: Math Department + Content Editors

Grant UPDATE access to Content Editors for Course #123:
→ Charlie can update Course #123
→ Alice cannot update (only reviewer, not editor)
```

### 3. Project-Based Access

```
Groups:
- Project Alpha Team (group_id=5)
- Project Beta Team (group_id=6)

Grant access to all Project Alpha resources to group_id=5:
→ All team members automatically get access
→ New team members automatically get access when added
→ Removed team members automatically lose access
```

## Implementation

### Granting Access to Groups

```java
/**
 * Grant access to a group for specific record.
 * All group members inherit this access.
 */
public Mono<EntityAuthorization> grantAccessToGroup(
    String entityType,
    Long entityId,
    Long groupId,
    String accessLevel
) {
    EntityAuthorization authorization = EntityAuthorization.builder()
        .entityType(entityType)
        .entityId(entityId)
        .groupId(groupId)  // Group-based
        .userId(null)      // Not user-based
        .accessLevel(accessLevel)
        .grantedByUserId(currentUser.getUserId())
        .build();
    
    return authorizationRepository.save(authorization);
}
```

### Checking Access (Including Groups)

```java
/**
 * Check if user has access (including group memberships).
 */
private Mono<Boolean> checkRecordLevelAccessWithGroups(
    Long userId, 
    String entityType, 
    Long entityId, 
    String requiredAccessLevel
) {
    return authorizationRepository
        .findValidAuthorizationsForUserAndEntityIncludingGroups(
            userId, 
            entityType, 
            entityId
        )
        .any(auth -> hasRequiredAccessLevel(auth.getAccessLevel(), requiredAccessLevel));
}
```

### Repository Query (Including Groups)

```sql
SELECT DISTINCT ea.* 
FROM ems_entity_authorization ea 
LEFT JOIN ems_user_group_membership ugm ON 
    ea.group_id = ugm.group_id AND ugm.deleted_at IS NULL 
WHERE ea.entity_type = :entityType 
  AND ea.entity_id = :entityId 
  AND ea.deleted_at IS NULL 
  AND (ea.user_id = :userId OR ugm.user_id = :userId)
```

## Examples

### Example 1: Grant Access to Group

```
Admin: Alice (ADMIN access to Course #123)
Action: Grant READ access to Math Department (group_id=1)

SQL:
INSERT INTO ems_entity_authorization VALUES
('Course', 123, NULL, 1, 'READ', 5);

Result: All Math Department members can now read Course #123
```

### Example 2: User Accesses via Group

```
User: Charlie (member of Math Department)
Action: Read Course #123

Query:
SELECT * FROM ems_entity_authorization ea
LEFT JOIN ems_user_group_membership ugm ON ea.group_id = ugm.group_id
WHERE ea.entity_type = 'Course' 
  AND ea.entity_id = 123
  AND (ea.user_id = 15 OR ugm.user_id = 15)

Found: 1 record (group_id=1, READ)
Charlie is member of group_id=1

Result: ✓ ALLOWED
```

### Example 3: User in Multiple Groups

```
User: Alice
Groups: 
- Math Department (READ access to Course #456)
- Course Reviewers (UPDATE access to Course #456)

Action: Update Course #456

Authorization check finds:
- group_id=1, READ (via Math Department)
- group_id=3, UPDATE (via Course Reviewers)

Highest access level: UPDATE

Result: ✓ ALLOWED (via Course Reviewers group)
```

### Example 4: User Removed from Group

```
User: Charlie
Action: Remove from Math Department

SQL:
UPDATE ems_user_group_membership 
SET deleted_at = NOW()
WHERE user_id = 15 AND group_id = 1

Result: Charlie immediately loses access to all courses granted to Math Department
```

### Example 5: Efficiency Comparison

```
Scenario: Grant READ access to 50 users

Option 1: Individual grants
- 50 INSERT statements
- 50 authorization records
- Must update each user individually

Option 2: Group grant
- 1 INSERT statement
- 1 authorization record
- All 50 users automatically get access
- New users automatically get access when added to group

Result: Group grant is much more efficient
```

## Benefits

### 1. Simplified Permission Management
- Grant access to entire group instead of individual users
- One record grants access to many users
- Easier to manage large teams

### 2. Automatic Access Propagation
- New group members automatically get access
- Removed group members automatically lose access
- No manual permission updates needed

### 3. Organizational Structure
- Model departments, teams, projects
- Align permissions with organization
- Clear permission hierarchy

### 4. Flexibility
- Users can belong to multiple groups
- Inherit permissions from all groups
- Combine user-based and group-based grants
- Highest access level wins

### 5. Scalability
- Efficient for large user bases
- Reduces number of authorization records
- Faster permission checks with proper indexing

### 6. Auditability
- Track which groups have access
- See all group members with access
- Audit group membership changes

## Integration with Existing Features

### Works with Aggregates
```
Grant READ access to Math Department for Course #123
→ All members can read Course #123 + modules + content + enrollments
```

### Works with Custom Queries
```sql
-- Find courses accessible to user (including groups)
SELECT DISTINCT c.* 
FROM ems_course c
INNER JOIN ems_entity_authorization ea ON 
    ea.entity_type = 'Course' AND ea.entity_id = c.course_id
LEFT JOIN ems_user_group_membership ugm ON 
    ea.group_id = ugm.group_id AND ugm.deleted_at IS NULL
WHERE (ea.user_id = :userId OR ugm.user_id = :userId)
  AND ea.deleted_at IS NULL
```

### Works with Access Hierarchy
```
Group has UPDATE access
→ Members can UPDATE, CREATE, and READ (via hierarchy)
```

## Files Updated

1. **RECORD_LEVEL_AUTHORIZATION_SPECIFICATION.md**
   - Added user groups tables schema
   - Modified entity_authorization table to support group_id
   - Added example records showing user and group authorization
   - Added "Who Has Access" example showing effective permissions
   - Updated query examples to include group joins
   - Added comprehensive "Group-Based Authorization" section
   - Added group management code examples
   - Added repository queries with group support
   - Added 5 detailed examples

## Key Takeaways

1. **Single table model preserved** - Still one authorization table for all entities
2. **Either user OR group** - Each authorization record is for user OR group (not both)
3. **Users inherit from groups** - Users get permissions from all their groups
4. **Highest access wins** - If user has multiple access levels, highest applies
5. **Automatic propagation** - Group membership changes immediately affect access
6. **Efficient management** - Grant to group instead of individual users
7. **Works everywhere** - Groups work with entities, aggregates, and custom queries

The authorization system now provides enterprise-grade permission management with group support while maintaining simplicity and performance.
