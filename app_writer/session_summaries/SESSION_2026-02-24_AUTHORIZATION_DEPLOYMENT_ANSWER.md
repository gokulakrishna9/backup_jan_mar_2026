# Authorization Layer Deployment - How It Works

**Date:** 2026-02-24  
**Question:** How is the authorization layer being added to the database?

---

## Answer: SQL DDL File Generation

The authorization layer is **automatically generated as a SQL file** that you need to run manually against your database.

---

## What Gets Generated

### 1. SQL DDL File
**File:** `authentication_authorization_schema.sql`  
**Location:** Root of generated code directory (same level as `pom.xml`)

**Contains:**
- Authentication tables (`ems_auth_user`, `ems_role`, `ems_auth_user_role`, `ems_auth_user_link`)
- Authorization tables (`ems_entity_authorization`, `ems_user_group`, `ems_user_group_membership`)
- Third-party auth tables (`ems_auth_provider`, `ems_auth_user_provider`) - optional
- Default roles data (USER, ADMIN, SYSTEM_ADMIN, entity creator roles)
- Default auth providers (Google, GitHub, etc.) - disabled by default
- All indexes, foreign keys, and constraints

### 2. Java Entity Classes
**Location:** `src/main/java/{package}/entity/`

**Files:**
- `AuthUser.java`
- `Role.java`
- `AuthUserRole.java`
- `AuthUserLink.java`
- `EntityAuthorization.java`
- `UserGroup.java`
- `UserGroupMembership.java`

### 3. Repository Interfaces
**Location:** `src/main/java/{package}/repository/`

**Files:**
- `AuthUserRepository.java`
- `RoleRepository.java`
- `AuthUserRoleRepository.java`
- `AuthUserLinkRepository.java`
- `EntityAuthorizationRepository.java`
- `UserGroupRepository.java`
- `UserGroupMembershipRepository.java`

---

## Deployment Process

### Step 1: Generate Code
Run the code generator, which creates:
```
generated-app/
├── pom.xml
├── authentication_authorization_schema.sql  ← SQL file here
├── README.md
└── src/
    └── main/
        └── java/
            └── com/
                └── example/
                    ├── entity/
                    ├── repository/
                    └── service/
```

### Step 2: Run SQL Script (Manual)
**You need to manually execute the SQL file against your database:**

#### MySQL
```bash
mysql -u root -p your_database < authentication_authorization_schema.sql
```

#### PostgreSQL
```bash
psql -U postgres -d your_database -f authentication_authorization_schema.sql
```

#### Using Database Client
1. Open your database client (MySQL Workbench, pgAdmin, DBeaver, etc.)
2. Connect to your database
3. Open `authentication_authorization_schema.sql`
4. Execute the entire script

### Step 3: Start Application
After the SQL script runs successfully:
1. All authentication and authorization tables exist
2. Default roles are inserted
3. Application can start and use the tables
4. JWT authentication works
5. Authorization checks work

---

## What the SQL Script Creates

### Authentication Tables

1. **ems_auth_user** - Authentication credentials
   - username, email, password (BCrypt hashed)
   - Email verification, password reset tokens
   - Active/inactive status
   - Last login tracking

2. **ems_role** - System and entity-level roles
   - role_name (USER, ADMIN, SYSTEM_ADMIN, COURSE_CREATOR, etc.)
   - description

3. **ems_auth_user_role** - User-role assignments
   - Links auth users to roles
   - Many-to-many relationship

4. **ems_auth_user_link** - Links auth to app users
   - Connects authentication to business entities
   - Supports multiple user types per auth user

### Authorization Tables

5. **ems_entity_authorization** - Record-level access control
   - entity_type (e.g., "Course", "Institution")
   - entity_id (specific record ID)
   - auth_user_id OR group_id (who has access)
   - access_level (READ, CREATE, UPDATE, DELETE, ADMIN)
   - Supports both user-based and group-based authorization

6. **ems_user_group** - User groups
   - group_name, description
   - Created by auth user

7. **ems_user_group_membership** - Group membership
   - Links auth users to groups
   - Supports expiration dates

### Third-Party Auth Tables (Optional)

8. **ems_auth_provider** - OAuth2/SAML providers
   - Google, GitHub, Facebook, Microsoft, Azure AD, Okta
   - OAuth2 configuration (client_id, client_secret, URIs)
   - SAML configuration (entity_id, SSO URL, certificate)
   - Disabled by default (requires configuration)

9. **ems_auth_user_provider** - Third-party auth links
   - Links auth users to provider accounts
   - Stores OAuth2 tokens
   - Stores SAML session data

### Default Data

**Default Roles Inserted:**
```sql
INSERT INTO ems_role (role_name, description) VALUES
('USER', 'Standard user with basic access'),
('ADMIN', 'Administrator with elevated privileges'),
('SYSTEM_ADMIN', 'System administrator with full access - bypasses all authorization checks'),
('COURSE_CREATOR', 'Can create courses and manage own courses'),
('INSTITUTION_CREATOR', 'Can create institutions and manage own institutions'),
('JOBPOST_CREATOR', 'Can create job posts and manage own job posts'),
('COMMUNITY_CREATOR', 'Can create communities and manage own communities');
```

**Default Providers Inserted (Disabled):**
```sql
INSERT INTO ems_auth_provider (provider_name, provider_type, display_name, is_enabled) VALUES
('google', 'OAUTH2', 'Google', FALSE),
('github', 'OAUTH2', 'GitHub', FALSE),
('facebook', 'OAUTH2', 'Facebook', FALSE),
('microsoft', 'OAUTH2', 'Microsoft', FALSE),
('azure_ad', 'OIDC', 'Azure Active Directory', FALSE),
('okta', 'OIDC', 'Okta', FALSE);
```

---

## Configuration Options

The DDL generator supports these options:

| Option | Default | Description |
|--------|---------|-------------|
| `includeThirdPartyAuth` | true | Include OAuth2/SAML tables |
| `includeDefaultRoles` | true | Insert default roles |
| `includeDefaultProviders` | true | Insert default providers (disabled) |
| `includeDropStatements` | false | Include DROP TABLE statements |

---

## Important Notes

### 1. Run Once
The SQL script should be run **ONCE** before the first application startup. Running it multiple times may cause errors due to unique constraints.

### 2. Manual Execution Required
The generator **does not automatically run the SQL script**. You must manually execute it against your database.

### 3. Database Must Exist
The database must already exist before running the script. The script uses:
```sql
USE your_database_name;
```

### 4. Order Matters
The script creates tables in the correct order to satisfy foreign key constraints:
1. ems_auth_user (no dependencies)
2. ems_role (no dependencies)
3. ems_auth_user_role (depends on auth_user and role)
4. ems_auth_user_link (depends on auth_user)
5. ems_user_group (depends on auth_user)
6. ems_user_group_membership (depends on auth_user and user_group)
7. ems_entity_authorization (depends on auth_user and user_group)

### 5. Third-Party Auth Optional
If you don't need OAuth2/SAML, you can:
- Set `includeThirdPartyAuth: false` in generator config
- Or simply ignore the provider tables (they won't be used)

---

## Example Workflow

### 1. Generate Code
```bash
python backend_generator.py --input database_definition.json --output generated-app
```

**Output:**
```
✓ Generated: generated-app/authentication_authorization_schema.sql
✓ Generated: generated-app/src/main/java/com/example/entity/AuthUser.java
✓ Generated: generated-app/src/main/java/com/example/repository/AuthUserRepository.java
... (more files)
```

### 2. Create Database
```bash
mysql -u root -p
CREATE DATABASE my_app_db;
EXIT;
```

### 3. Run SQL Script
```bash
mysql -u root -p my_app_db < generated-app/authentication_authorization_schema.sql
```

**Output:**
```
Query OK, 0 rows affected (0.05 sec)
Query OK, 0 rows affected (0.03 sec)
Query OK, 0 rows affected (0.04 sec)
... (table creation messages)
Query OK, 7 rows affected (0.01 sec)  -- Default roles inserted
Query OK, 6 rows affected (0.01 sec)  -- Default providers inserted
```

### 4. Verify Tables
```bash
mysql -u root -p my_app_db
SHOW TABLES;
```

**Expected Output:**
```
+----------------------------------+
| Tables_in_my_app_db              |
+----------------------------------+
| ems_auth_user                    |
| ems_role                         |
| ems_auth_user_role               |
| ems_auth_user_link               |
| ems_auth_provider                |
| ems_auth_user_provider           |
| ems_user_group                   |
| ems_user_group_membership        |
| ems_entity_authorization         |
| ... (your business tables)       |
+----------------------------------+
```

### 5. Start Application
```bash
cd generated-app
mvn spring-boot:run
```

**Application starts successfully:**
- Connects to database
- Finds authentication tables
- JWT authentication works
- Authorization checks work

---

## Summary

**Q: How is the authorization layer added to the database?**

**A: The generator creates a SQL file (`authentication_authorization_schema.sql`) that you manually run against your database before starting the application.**

**Process:**
1. ✅ Generator creates SQL file
2. ✅ You manually execute SQL file
3. ✅ Database tables created
4. ✅ Default roles inserted
5. ✅ Application starts and uses tables

**Yes, manual upload/execution is required.** This is intentional because:
- Database credentials shouldn't be in the generator
- You may need to review/modify the schema
- You control when and how the schema is deployed
- Supports different database environments (dev, staging, prod)

