# Task 15: Authentication DDL Generator - COMPLETE

## Summary
Created a comprehensive DDL generator layer that produces SQL schema for authentication and authorization tables. This is a fixed layer that always generates the same core tables regardless of application domain.

---

## What Was Created

### 1. Generator Prompt Document
**File:** `spring_webflux_application_writer_code_generation_prompts/13_AUTHENTICATION_DDL_GENERATOR.md`

**Purpose:** Documents how to generate DDL for authentication/authorization tables

**Contents:**
- Generator object structure
- Generation functions for each table
- Configuration options
- Usage examples
- Integration notes

### 2. DDL Output File
**File:** `code_output/authentication_authorization_schema.sql`

**Purpose:** Ready-to-execute SQL script for database setup

**Contents:**
- 7 core tables with complete DDL
- Comprehensive comments and documentation
- Optimized indexes for performance
- Foreign key constraints
- Check constraints
- Default roles data
- Example admin user creation

---

## Tables Generated

### 1. ems_auth_user
**Purpose:** Authentication credentials only

**Key Fields:**
- `auth_user_id` - Primary key
- `username` - Unique login
- `email` - Unique email
- `password` - BCrypt hashed
- Status fields (is_active, is_email_verified)
- Token fields (email verification, password reset)
- `last_login_at` - Track logins

**Indexes:**
- Username, email, active status, deleted_at

### 2. ems_role
**Purpose:** System and entity-level roles

**Key Fields:**
- `role_id` - Primary key
- `role_name` - Unique role name
- `description` - Role description

**Default Roles:**
- USER - Basic access
- ADMIN - Elevated privileges
- SYSTEM_ADMIN - Bypasses all checks
- COURSE_CREATOR, INSTITUTION_CREATOR, etc.

### 3. ems_auth_user_role
**Purpose:** Assign roles to auth users

**Key Fields:**
- `auth_user_role_id` - Primary key
- `auth_user_id` - References ems_auth_user
- `role_id` - References ems_role

**Constraints:**
- Unique per user-role pair
- Cascade delete

### 4. ems_auth_user_link
**Purpose:** Link auth users to application users

**Key Fields:**
- `link_id` - Primary key
- `auth_user_id` - References ems_auth_user
- `app_user_table` - Application table name (e.g., 'ems_user')
- `app_user_id` - ID in application table

**Features:**
- Convention-based linking
- Supports multiple app user types per auth user
- Flexible and extensible

### 5. ems_user_group
**Purpose:** User groups for authorization

**Key Fields:**
- `group_id` - Primary key
- `group_name` - Unique group name
- `description` - Group description
- `created_by_auth_user_id` - Creator

**Use Cases:**
- Departments, teams, projects
- Role-based groups
- Organizational units

### 6. ems_user_group_membership
**Purpose:** Track group membership

**Key Fields:**
- `membership_id` - Primary key
- `auth_user_id` - References ems_auth_user
- `group_id` - References ems_user_group
- `added_by_auth_user_id` - Who added
- `expires_at` - Optional expiration

**Features:**
- Users can belong to multiple groups
- Time-based expiration
- Audit trail

### 7. ems_entity_authorization
**Purpose:** Unified authorization for ALL entities

**Key Fields:**
- `authorization_id` - Primary key
- `entity_type` - Entity name (e.g., 'Course')
- `entity_id` - Record ID
- `auth_user_id` - User access (NULL if group)
- `group_id` - Group access (NULL if user)
- `access_level` - READ, CREATE, UPDATE, DELETE, ADMIN
- `granted_by_auth_user_id` - Who granted
- `expires_at` - Optional expiration

**Features:**
- Single table for all entities
- User-based OR group-based
- Check constraint enforces exclusivity
- Comprehensive indexes for performance
- Supports expiration

---

## Key Features

### 1. Comprehensive Comments
Every table includes:
- Purpose statement
- Field descriptions
- Usage notes
- Examples

### 2. Optimized Indexes
Strategic indexes for:
- Authentication queries (username, email)
- Authorization checks (entity_type + entity_id + auth_user_id)
- Group membership lookups
- Soft delete filtering
- Expiration checks

### 3. Referential Integrity
- Foreign key constraints
- Cascade deletes where appropriate
- SET NULL for audit fields

### 4. Soft Delete Pattern
All tables support soft delete:
- `deleted_at` field
- Indexes include deleted_at
- Unique constraints include deleted_at

### 5. Audit Trail
All tables include:
- `created_at` - Timestamp
- `updated_at` - Auto-update timestamp
- Creator/granter tracking

### 6. Check Constraints
- Entity authorization: Either user OR group (not both)
- Enforces data integrity at database level

### 7. Default Data
Includes default roles:
- System roles (USER, ADMIN, SYSTEM_ADMIN)
- Entity creator roles (COURSE_CREATOR, etc.)

---

## Generator Configuration

```javascript
{
  databaseName: 'emotisense_db',
  useIfNotExists: true,
  includeDropStatements: false,
  includeComments: true,
  includeDefaultRoles: true,
  includeIndexes: true,
  includeConstraints: true,
  outputPath: 'output/authentication_authorization_schema.sql'
}
```

**Options:**
- `databaseName` - Target database
- `useIfNotExists` - Use IF NOT EXISTS clause
- `includeDropStatements` - Include DROP TABLE statements
- `includeComments` - Include SQL comments
- `includeDefaultRoles` - Insert default roles
- `includeIndexes` - Create indexes
- `includeConstraints` - Add foreign keys and checks

---

## Integration with Generator

### Execution Order

1. **SQL Parser** - Parse application SQL schema
2. **Authentication DDL Generator** ← NEW (this layer)
3. **Entity Generator** - Generate application entities
4. **DTO Generator** - Generate DTOs
5. **Repository Generator** - Generate repositories
6. **Service Generator** - Generate services
7. **Controller Generator** - Generate controllers

### Output Location

```
code_output/
├── authentication_authorization_schema.sql  ← NEW
├── entities/
│   ├── Course.java
│   ├── User.java
│   └── ...
├── dtos/
├── repositories/
├── services/
└── controllers/
```

---

## Usage Instructions

### 1. Execute DDL Script

```bash
# MySQL
mysql -u root -p emotisense_db < authentication_authorization_schema.sql

# PostgreSQL (with minor modifications)
psql -U postgres -d emotisense_db -f authentication_authorization_schema.sql
```

### 2. Create Initial Admin User

```sql
-- Create auth user
INSERT INTO ems_auth_user (username, email, password, is_active, is_email_verified)
VALUES ('admin', 'admin@example.com', '$2a$10$...', TRUE, TRUE);

-- Assign SYSTEM_ADMIN role
INSERT INTO ems_auth_user_role (auth_user_id, role_id)
SELECT auth_user_id, role_id 
FROM ems_auth_user, ems_role 
WHERE username = 'admin' AND role_name = 'SYSTEM_ADMIN';
```

### 3. Generate Application Tables

Run the entity generator to create application-specific tables (ems_user, ems_course, etc.)

### 4. Link Auth User to App User

```sql
-- Create application user
INSERT INTO ems_user (first_name, last_name, auth_user_id)
VALUES ('Admin', 'User', 1);

-- Link them
INSERT INTO ems_auth_user_link (auth_user_id, app_user_table, app_user_id)
VALUES (1, 'ems_user', 1);
```

---

## Database Compatibility

### MySQL/MariaDB
- Fully compatible
- Uses InnoDB engine
- UTF8MB4 charset

### PostgreSQL
Minor modifications needed:
- Change `AUTO_INCREMENT` → `SERIAL`
- Change `DATETIME` → `TIMESTAMP`
- Change `BOOLEAN` → `BOOLEAN` (same)
- Change `TEXT` → `TEXT` (same)

### SQL Server
Moderate modifications needed:
- Change `AUTO_INCREMENT` → `IDENTITY(1,1)`
- Change `DATETIME` → `DATETIME2`
- Change `BOOLEAN` → `BIT`
- Change backticks to square brackets

---

## Performance Considerations

### Index Strategy

**High-frequency queries:**
1. Authentication: `idx_username`, `idx_email`
2. Authorization check: `idx_entity_auth_user`, `idx_entity_group`
3. User entities: `idx_auth_user_entity`
4. Group entities: `idx_group_entity`

**Composite indexes:**
- `(entity_type, entity_id, auth_user_id)` - Most common authorization query
- `(auth_user_id, group_id)` - Group membership lookup
- `(is_active, deleted_at)` - Active user filtering

### Query Optimization

**Authorization check query:**
```sql
-- Optimized with idx_entity_auth_user
SELECT * FROM ems_entity_authorization
WHERE entity_type = 'Course'
  AND entity_id = 123
  AND auth_user_id = 1
  AND deleted_at IS NULL
  AND (expires_at IS NULL OR expires_at > NOW());
```

**Group-based authorization:**
```sql
-- Optimized with idx_entity_group + idx_auth_user_group
SELECT ea.* 
FROM ems_entity_authorization ea
JOIN ems_user_group_membership ugm ON ea.group_id = ugm.group_id
WHERE ea.entity_type = 'Course'
  AND ea.entity_id = 123
  AND ugm.auth_user_id = 1
  AND ea.deleted_at IS NULL
  AND ugm.deleted_at IS NULL;
```

---

## Security Considerations

### 1. Password Storage
- Always use BCrypt (or Argon2)
- Never store plain text passwords
- Use strong salt (BCrypt handles this)

### 2. Token Security
- Email verification tokens: UUID or secure random
- Password reset tokens: UUID or secure random
- Set expiration times
- Invalidate after use

### 3. Soft Delete
- Deleted records remain in database
- Prevents accidental data loss
- Allows audit trail
- Can be purged later

### 4. Foreign Key Constraints
- CASCADE delete for dependent records
- SET NULL for audit fields
- Maintains referential integrity

---

## Maintenance

### Regular Tasks

1. **Purge soft-deleted records:**
```sql
-- Delete records older than 90 days
DELETE FROM ems_entity_authorization 
WHERE deleted_at < DATE_SUB(NOW(), INTERVAL 90 DAY);
```

2. **Clean expired authorizations:**
```sql
-- Soft delete expired authorizations
UPDATE ems_entity_authorization 
SET deleted_at = NOW()
WHERE expires_at < NOW() AND deleted_at IS NULL;
```

3. **Monitor table sizes:**
```sql
-- Check table sizes
SELECT 
    table_name,
    ROUND(((data_length + index_length) / 1024 / 1024), 2) AS size_mb
FROM information_schema.TABLES
WHERE table_schema = 'emotisense_db'
  AND table_name LIKE 'ems_%'
ORDER BY (data_length + index_length) DESC;
```

---

## Testing

### Sample Test Data

```sql
-- Create test auth user
INSERT INTO ems_auth_user (username, email, password, is_active)
VALUES ('testuser', 'test@example.com', '$2a$10$...', TRUE);

-- Assign USER role
INSERT INTO ems_auth_user_role (auth_user_id, role_id)
SELECT auth_user_id, role_id 
FROM ems_auth_user, ems_role 
WHERE username = 'testuser' AND role_name = 'USER';

-- Create test group
INSERT INTO ems_user_group (group_name, description)
VALUES ('Test Group', 'Group for testing');

-- Add user to group
INSERT INTO ems_user_group_membership (auth_user_id, group_id)
SELECT au.auth_user_id, ug.group_id
FROM ems_auth_user au, ems_user_group ug
WHERE au.username = 'testuser' AND ug.group_name = 'Test Group';

-- Grant authorization
INSERT INTO ems_entity_authorization (entity_type, entity_id, auth_user_id, access_level)
VALUES ('Course', 1, 1, 'READ');
```

---

## Status: COMPLETE ✅

Successfully created:
1. ✅ Generator prompt document (13_AUTHENTICATION_DDL_GENERATOR.md)
2. ✅ DDL output file (authentication_authorization_schema.sql)
3. ✅ Complete schema with 7 tables
4. ✅ Comprehensive comments and documentation
5. ✅ Optimized indexes
6. ✅ Foreign key constraints
7. ✅ Default roles data
8. ✅ Usage examples

The authentication and authorization DDL layer is ready for use in the code generation workflow!
