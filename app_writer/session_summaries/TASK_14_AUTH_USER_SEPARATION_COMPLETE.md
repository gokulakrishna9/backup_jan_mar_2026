# Task 14: Separate Authentication User from Application User - COMPLETE

## Summary
Successfully separated authentication users (`ems_auth_user`) from application-level user entities with a flexible link table (`ems_auth_user_link`) that supports multiple application user types.

---

## Problem Statement

The original design used a single `ems_user` table for both:
1. Authentication (username, password, email)
2. Application profile (first_name, last_name, business data)

This created limitations:
- Cannot have multiple user types (Student, Instructor, Admin, etc.)
- Mixes authentication concerns with business domain
- Application user tables cannot be regular root entities
- Difficult to extend with domain-specific user types

---

## Solution: Three-Table Architecture

### 1. Authentication User Table (`ems_auth_user`)
**Purpose:** Authentication credentials ONLY

**Fields:**
- `auth_user_id` - Primary key
- `username` - Unique login identifier
- `email` - Unique email
- `password` - BCrypt hashed
- Authentication status fields (is_active, is_email_verified, tokens)
- NO business domain fields

### 2. Link Table (`ems_auth_user_link`)
**Purpose:** Connect authentication to application users

**Fields:**
- `auth_user_id` - References `ems_auth_user`
- `app_user_table` - Name of application user table (e.g., 'ems_user', 'ems_student')
- `app_user_id` - ID in the application user table

**Key Features:**
- One auth user can link to multiple application user types
- Convention-based table naming: `ems_{user_type}`
- Convention-based primary key: `{user_type}_id`
- Flexible and extensible

### 3. Application User Tables (Convention-Based)
**Purpose:** Business domain user entities

**Examples:**
- `ems_user` (user_id) - General user profile
- `ems_student` (student_id) - Student-specific data
- `ems_instructor` (instructor_id) - Instructor-specific data
- `ems_admin` (admin_id) - Admin-specific data

**Key Features:**
- Generated as regular root entities
- Subject to record-level authorization
- Can have domain-specific fields and relationships
- Optional `auth_user_id` foreign key for convenience

---

## Naming Conventions

### Application User Tables
- **Table name:** `ems_{user_type}` (e.g., `ems_user`, `ems_student`, `ems_instructor`)
- **Primary key:** `{user_type}_id` (e.g., `user_id`, `student_id`, `instructor_id`)
- **Auth link field (optional):** `auth_user_id` BIGINT

### Examples
```sql
-- General user
CREATE TABLE ems_user (
    user_id BIGINT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    auth_user_id BIGINT,
    ...
);

-- Student
CREATE TABLE ems_student (
    student_id BIGINT PRIMARY KEY,
    student_number VARCHAR(50),
    major VARCHAR(100),
    gpa DECIMAL(3,2),
    auth_user_id BIGINT,
    ...
);

-- Instructor
CREATE TABLE ems_instructor (
    instructor_id BIGINT PRIMARY KEY,
    employee_number VARCHAR(50),
    department VARCHAR(100),
    auth_user_id BIGINT,
    ...
);
```

---

## Authorization Integration

### Key Changes

**Before (OLD):**
```sql
-- Authorization referenced ems_user
FOREIGN KEY (user_id) REFERENCES ems_user(user_id)
```

**After (NEW):**
```sql
-- Authorization references ems_auth_user
FOREIGN KEY (auth_user_id) REFERENCES ems_auth_user(auth_user_id)
```

### Updated Tables

1. **ems_entity_authorization**
   - Changed `user_id` → `auth_user_id`
   - Changed `granted_by_user_id` → `granted_by_auth_user_id`
   - References `ems_auth_user` table

2. **ems_user_group_membership**
   - Changed `user_id` → `auth_user_id`
   - Changed `added_by_user_id` → `added_by_auth_user_id`
   - References `ems_auth_user` table

3. **ems_auth_user_role** (renamed from `ems_user_role`)
   - Changed `user_id` → `auth_user_id`
   - Changed `user_role_id` → `auth_user_role_id`
   - References `ems_auth_user` table

---

## Files Updated

### 1. Authentication Tables Document
**File:** `ai_generated_documents/backend_prompts/09A_AUTHENTICATION_TABLES.md`

**Changes:**
- Renamed `ems_user` → `ems_auth_user`
- Added `ems_auth_user_link` table
- Added application user table conventions
- Updated all entity classes (User → AuthUser, UserRole → AuthUserRole)
- Updated all repository interfaces
- Added example usage scenarios
- Added integration notes

### 2. Authorization System Overview
**File:** `emotisense-ai/spring_webflux_application_writer_code_generation_prompts/00_AUTHORIZATION_SYSTEM_OVERVIEW.md`

**Changes:**
- Updated `ems_user_group_membership` to use `auth_user_id`
- Updated `ems_entity_authorization` to use `auth_user_id`
- Added note about authorization using auth_user_id

---

## Benefits

### 1. Separation of Concerns
- Authentication logic separate from business domain
- Clear boundaries between security and application layers
- Easier to maintain and test

### 2. Flexibility
- Support multiple application user types
- One person can have multiple roles (student + instructor)
- Easy to add new user types without changing authentication

### 3. Domain-Driven Design
- Application user tables are proper domain entities
- Can have rich domain models
- Subject to authorization like other entities

### 4. Extensibility
- Easy to add new user types
- Can link to external authentication systems
- Supports complex organizational structures

### 5. Authorization Clarity
- All authorization uses `auth_user_id`
- Consistent across all authorization tables
- No confusion about which user ID to use

---

## Example Usage Scenarios

### Scenario 1: Simple Application (Single User Type)

```sql
-- 1. Create authentication user
INSERT INTO ems_auth_user (username, email, password) 
VALUES ('john_doe', 'john@example.com', '$2a$10$...');
-- auth_user_id = 1

-- 2. Create application user
INSERT INTO ems_user (first_name, last_name, auth_user_id) 
VALUES ('John', 'Doe', 1);
-- user_id = 101

-- 3. Link them
INSERT INTO ems_auth_user_link (auth_user_id, app_user_table, app_user_id) 
VALUES (1, 'ems_user', 101);

-- 4. Assign role
INSERT INTO ems_auth_user_role (auth_user_id, role_id) 
VALUES (1, 1);  -- USER role

-- 5. Grant authorization (uses auth_user_id)
INSERT INTO ems_entity_authorization (entity_type, entity_id, auth_user_id, access_level)
VALUES ('Course', 123, 1, 'READ');
```

### Scenario 2: Learning Management System (Multiple User Types)

```sql
-- 1. Create authentication user
INSERT INTO ems_auth_user (username, email, password) 
VALUES ('jane_smith', 'jane@example.com', '$2a$10$...');
-- auth_user_id = 2

-- 2. Create student profile
INSERT INTO ems_student (student_number, major, auth_user_id) 
VALUES ('S12345', 'Computer Science', 2);
-- student_id = 201

-- 3. Link auth user to student
INSERT INTO ems_auth_user_link (auth_user_id, app_user_table, app_user_id) 
VALUES (2, 'ems_student', 201);

-- 4. Later, same person becomes an instructor
INSERT INTO ems_instructor (employee_number, department, auth_user_id) 
VALUES ('I67890', 'Computer Science', 2);
-- instructor_id = 301

-- 5. Link auth user to instructor (same auth user, different app user)
INSERT INTO ems_auth_user_link (auth_user_id, app_user_table, app_user_id) 
VALUES (2, 'ems_instructor', 301);

-- 6. Assign roles
INSERT INTO ems_auth_user_role (auth_user_id, role_id) 
VALUES (2, 1),  -- USER role
       (2, 4);  -- COURSE_CREATOR role

-- 7. Grant authorization (uses auth_user_id, not student_id or instructor_id)
INSERT INTO ems_entity_authorization (entity_type, entity_id, auth_user_id, access_level)
VALUES ('Course', 456, 2, 'ADMIN');
```

### Scenario 3: Authorization Check in Code

```java
// Get current auth user from JWT token
AuthUser authUser = getCurrentAuthUser();
Long authUserId = authUser.getAuthUserId();  // Use this for authorization

// Check if auth user has access to Course #123
boolean hasAccess = authorizationService.hasAccess(
    authUserId,  // Use auth_user_id, NOT app user ID
    "Course", 
    123L, 
    AccessLevel.COURSE_READ
);

// Get linked application user (if needed for business logic)
AuthUserLink link = authUserLinkRepository
    .findByAuthUserIdAndAppUserTableAndDeletedAtIsNull(
        authUserId, 
        "ems_user"
    );

if (link != null) {
    User appUser = userRepository.findById(link.getAppUserId());
    // Use appUser for business logic (display name, profile, etc.)
}
```

---

## Migration Path

### For Existing Applications

If you have existing applications using `ems_user` for authentication:

1. **Create new tables:**
   ```sql
   CREATE TABLE ems_auth_user (...);
   CREATE TABLE ems_auth_user_link (...);
   ```

2. **Migrate data:**
   ```sql
   -- Copy authentication data to ems_auth_user
   INSERT INTO ems_auth_user (username, email, password, ...)
   SELECT username, email, password, ... FROM ems_user;
   
   -- Create links
   INSERT INTO ems_auth_user_link (auth_user_id, app_user_table, app_user_id)
   SELECT auth_user_id, 'ems_user', user_id FROM ems_user;
   
   -- Update authorization tables
   UPDATE ems_entity_authorization ea
   JOIN ems_user u ON ea.user_id = u.user_id
   SET ea.auth_user_id = u.auth_user_id;
   ```

3. **Remove authentication fields from ems_user:**
   ```sql
   ALTER TABLE ems_user 
   DROP COLUMN username,
   DROP COLUMN email,
   DROP COLUMN password,
   ADD COLUMN auth_user_id BIGINT;
   ```

### For New Applications

Start with the new architecture from the beginning:
1. Create `ems_auth_user` for authentication
2. Create `ems_auth_user_link` for linking
3. Create application user tables as regular root entities
4. All authorization uses `auth_user_id`

---

## Key Takeaways

1. **Authentication vs Application:**
   - `ems_auth_user` = Login credentials
   - Application user tables = Business domain entities

2. **Authorization Always Uses auth_user_id:**
   - `ems_entity_authorization` uses `auth_user_id`
   - `ems_user_group_membership` uses `auth_user_id`
   - `ems_auth_user_role` uses `auth_user_id`

3. **Flexible User Types:**
   - One auth user can link to multiple app user types
   - Application user tables follow naming conventions
   - Easy to add new user types

4. **Clear Separation:**
   - Authentication layer (security)
   - Application layer (business domain)
   - Link layer (connection)

---

## Status: COMPLETE ✅

All authentication and authorization documentation has been updated to separate authentication users from application users with a flexible link table architecture.
