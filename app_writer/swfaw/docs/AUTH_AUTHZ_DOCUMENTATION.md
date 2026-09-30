# Authentication & Authorization System Documentation

## Overview

The swfaw_v2 code generator produces Spring WebFlux applications with a comprehensive, enterprise-grade authentication and authorization system. This document describes the complete architecture, components, and usage.

**Version:** 2.1  
**Date:** March 5, 2026  
**Status:** Production Ready

**New in v2.1:**
- OAuth2/OpenID Connect authentication support
- External identity linking (Google, GitHub, Microsoft, etc.)
- Automatic user account creation from OAuth2 providers
- Multi-provider authentication per user

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Database Schema](#database-schema)
3. [Authentication Layer](#authentication-layer)
4. [OAuth2 Authentication](#oauth2-authentication)
5. [Authorization Layer](#authorization-layer)
6. [Audit Logging](#audit-logging)
7. [Admin UI](#admin-ui)
8. [API Reference](#api-reference)
9. [Configuration](#configuration)
10. [Security Best Practices](#security-best-practices)
11. [Troubleshooting](#troubleshooting)

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Application                       │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP + JWT Token
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Spring WebFlux Application                  │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         JwtAuthenticationFilter                       │  │
│  │  (Validates JWT, Sets SecurityContextHolder)         │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                     │
│                         ▼                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Controllers                              │  │
│  │  (Setup, Auth, Business, Admin, Audit)               │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                     │
│                         ▼                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Services                                 │  │
│  │  • AuthService (login, register)                     │  │
│  │  • AuthorizationService (access checks)              │  │
│  │  • AuditLoggingService (logging)                     │  │
│  │  • AdminService (management)                         │  │
│  │  • Business Services (with auth checks)              │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                     │
│                         ▼                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Authorization Components                      │  │
│  │  • DocumentGroupMatcher                              │  │
│  │  • QueryExecutor                                     │  │
│  │  • PermissionResolver                                │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                     │
│                         ▼                                     │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Repositories (R2DBC)                         │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    MySQL Database                            │
│  • Business Tables                                           │
│  • Auth/Authz Tables (11 tables)                            │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

- **Framework:** Spring WebFlux (Reactive)
- **Database:** MySQL with R2DBC (Reactive)
- **Authentication:** JWT (JSON Web Tokens)
- **Password Hashing:** BCrypt
- **UI:** Thymeleaf (for setup and admin)
- **API Documentation:** Swagger/OpenAPI

---

## Database Schema

### Schema Overview

The system uses 11 dedicated tables for authentication and authorization:

#### 1. System & User Management (4 tables)

**system_config**
- Stores application-wide settings
- Tracks setup completion status

**auth_user**
- User accounts with credentials
- Fields: username, email, password_hash, is_super_user
- BCrypt password hashing

**user_group**
- Groups for organizing users
- Fields: group_name, description, is_default_group, is_super_group
- Default groups auto-assigned to new users
- Super groups have full access to all resources

**user_group_membership**
- Links users to groups
- Time-based validity (valid_from, valid_until)
- Supports temporary group memberships

#### 2. Authorization Framework (5 tables)

**access_control**
- 8 predefined access controls:
  1. READ - View records
  2. CREATE - Create new records
  3. UPDATE - Modify existing records
  4. DELETE - Remove records
  5. GRANT_ACCESS - Give access to others
  6. EXPORT - Export data
  7. SHARE - Share with external users
  8. AUDIT - View audit logs

**document_group_type**
- 6 types of document groups:
  1. SINGLE_RECORD - One specific record
  2. MULTIPLE_RECORDS - Multiple specific records
  3. ENTIRE_TABLE - All records in a table
  4. MULTIPLE_TABLES - All records in multiple tables
  5. CUSTOM_QUERY - Records matching query (requires record IDs)
  6. CUSTOM_QUERY_ALL - All records matching query (ignores record IDs)

**document_group**
- Named groups of documents/records
- Links to document_group_type

**document_group_definition**
- Defines what records belong to each group
- Fields:
  - table_name: Target table
  - record_ids: Explicit record IDs (optional)
  - query_definition: JSON query for CUSTOM_QUERY types

**document_permission**
- Links document groups to users/groups with access controls
- Can grant to individual users OR user groups
- Time-based validity (valid_from, valid_until)

#### 3. Audit & Compliance (2 tables)

**access_audit_log**
- Logs every access attempt (granted and denied)
- Fields: auth_user_id, action, table_name, record_id, access_granted, denial_reason, accessed_at

**super_user_action_log**
- Logs super user actions with justification
- Fields: auth_user_id, action, target_table, target_record_id, justification, performed_at
- Justification required for DELETE operations

### Schema SQL

The complete schema is generated in `auth-schema.sql` and includes:
- Table definitions with indexes
- Foreign key constraints
- Pre-populated reference data (access controls, document group types)
- Default "Super Administrators" group

---

## Authentication Layer

### Components

#### 1. JWT Configuration

**JwtConfig** (`auth/JwtConfig.java`)
- Configurable secret key
- Configurable expiration time
- Loaded from application.yml

**JwtService** (`auth/JwtService.java`)
- `generateToken(username)` - Creates JWT token
- `validateToken(token)` - Validates and extracts username
- `extractUsername(token)` - Gets username from token

#### 2. Authentication Service

**AuthService** (`service/AuthService.java`)

**Methods:**
- `register(username, email, password)` - Create new user account
  - Validates input
  - Hashes password with BCrypt
  - Auto-assigns default groups
  - Returns JWT token

- `login(username, password)` - Authenticate user
  - Validates credentials
  - Generates JWT token
  - Returns token for subsequent requests

- `changePassword(userId, oldPassword, newPassword)` - Update password
  - Validates old password
  - Hashes new password
  - Updates database

#### 3. Security Filter

**JwtAuthenticationFilter** (`security/JwtAuthenticationFilter.java`)
- Intercepts all HTTP requests
- Extracts JWT from Authorization header
- Validates token
- Sets SecurityContextHolder with current user
- Allows public endpoints (/setup, /api/auth/**, /swagger-ui/**)

**SecurityContextHolder** (`security/SecurityContextHolder.java`)
- Thread-local storage for current authenticated user
- `getCurrentUser()` - Returns Mono<AuthUser>
- Used by services to get current user ID

#### 4. Setup Process

**SetupController** (`controller/SetupController.java`)
- `GET /setup` - Thymeleaf form for super user creation
- `POST /setup` - Creates first super user
- Only accessible on first launch
- Redirects to login after completion

**SetupService** (`service/SetupService.java`)
- Checks if setup is complete
- Creates super user account
- Creates "Super Administrators" group
- Marks setup as complete in system_config

### Authentication Flow

```
1. User Registration/Login
   ↓
2. AuthService validates credentials
   ↓
3. JwtService generates token
   ↓
4. Token returned to client
   ↓
5. Client includes token in Authorization header
   ↓
6. JwtAuthenticationFilter validates token
   ↓
7. SecurityContextHolder stores current user
   ↓
8. Services access current user via SecurityContextHolder
```

---

## OAuth2 Authentication

### Overview

The system supports OAuth2/OpenID Connect authentication, allowing users to sign in with external identity providers like Google, GitHub, and Microsoft. OAuth2 users are automatically linked to local accounts and use the same document-based authorization system.

### Components

#### 1. OAuth2 Entities

**OAuth2Provider** (`entity/OAuth2Provider.java`)
- Stores OAuth2 provider configuration
- Fields:
  - providerId (PK)
  - providerName (google, github, microsoft, etc.)
  - displayName (user-friendly name)
  - clientId, clientSecret
  - authorizationUri, tokenUri, userInfoUri
  - jwkSetUri, issuerUri
  - scope (OAuth2 scopes)
  - isEnabled (enable/disable provider)

**OAuth2LinkedAccount** (`entity/OAuth2LinkedAccount.java`)
- Links external OAuth2 identities to local users
- Fields:
  - linkedAccountId (PK)
  - authUserId (FK to auth_user)
  - providerId (FK to oauth2_provider)
  - providerUserId (external user ID from provider)
  - providerUsername, providerEmail
  - accessToken, refreshToken
  - tokenExpiresAt
  - linkedAt, lastLoginAt

#### 2. OAuth2 Repositories

**OAuth2ProviderRepository** (`repository/OAuth2ProviderRepository.java`)
- `findByProviderName(String)` - Get provider by name
- `findAllEnabled()` - Get all enabled providers

**OAuth2LinkedAccountRepository** (`repository/OAuth2LinkedAccountRepository.java`)
- `findByAuthUserId(Long)` - Get user's linked accounts
- `findByProviderAndUserId(Long, String)` - Find specific linked account

#### 3. OAuth2 Service

**OAuth2Service** (`service/OAuth2Service.java`)

**Methods:**

- `getEnabledProviders()` - List all enabled OAuth2 providers
- `getProviderByName(String)` - Get specific provider configuration
- `generateAuthorizationUrl(String, String, String)` - Generate OAuth2 authorization URL
- `exchangeCodeForToken(String, String, String)` - Exchange authorization code for access token
- `getUserInfo(String, String)` - Fetch user info from OAuth2 provider
- `linkOrCreateUser(String, Map, String, String)` - Link external identity to local user or create new user

**OAuth2 Flow:**

1. Frontend calls `/api/oauth2/login/{providerName}`
2. Backend generates authorization URL with state parameter
3. User redirects to OAuth2 provider (Google, GitHub, etc.)
4. User authenticates with provider
5. Provider redirects to `/api/oauth2/callback/{providerName}?code=...`
6. Backend exchanges code for access token
7. Backend fetches user info from provider
8. Backend finds or creates local user account
9. Backend links external identity to local account
10. Backend generates JWT token
11. Frontend receives JWT token for API access

**User Linking Logic:**

- If external identity exists → Update tokens and last login time
- If external identity doesn't exist → Create new local user and link identity
- Users can have multiple linked accounts (Google + GitHub)
- OAuth2 users have no password (passwordHash = null)

#### 4. OAuth2 Controller

**OAuth2Controller** (`controller/OAuth2Controller.java`)

**Endpoints:**

- `GET /api/oauth2/providers` - List enabled OAuth2 providers
  ```json
  [
    {
      "providerId": 1,
      "providerName": "google",
      "displayName": "Google",
      "isEnabled": true
    }
  ]
  ```

- `GET /api/oauth2/login/{providerName}?redirectUri=...` - Initiate OAuth2 flow
  ```json
  {
    "authorizationUrl": "https://accounts.google.com/o/oauth2/v2/auth?client_id=...",
    "state": "uuid-state-parameter"
  }
  ```

- `GET /api/oauth2/callback/{providerName}?code=...&state=...` - Handle OAuth2 callback
  ```json
  {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "username": "john.doe",
    "email": "john@example.com"
  }
  ```

### Database Schema

**oauth2_provider table:**
```sql
CREATE TABLE oauth2_provider (
    provider_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    provider_name VARCHAR(50) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    client_id VARCHAR(255) NOT NULL,
    client_secret VARCHAR(255) NOT NULL,
    authorization_uri VARCHAR(500),
    token_uri VARCHAR(500),
    user_info_uri VARCHAR(500),
    jwk_set_uri VARCHAR(500),
    issuer_uri VARCHAR(500),
    scope VARCHAR(255) DEFAULT 'openid profile email',
    is_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

**oauth2_linked_account table:**
```sql
CREATE TABLE oauth2_linked_account (
    linked_account_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    auth_user_id BIGINT UNSIGNED NOT NULL,
    provider_id BIGINT UNSIGNED NOT NULL,
    provider_user_id VARCHAR(255) NOT NULL,
    provider_username VARCHAR(255),
    provider_email VARCHAR(255),
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMP NULL,
    linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP NULL,
    FOREIGN KEY (auth_user_id) REFERENCES auth_user(auth_user_id) ON DELETE CASCADE,
    FOREIGN KEY (provider_id) REFERENCES oauth2_provider(provider_id) ON DELETE CASCADE,
    UNIQUE KEY unique_provider_account (provider_id, provider_user_id)
);
```

**Pre-configured Providers:**

The schema pre-populates three common OAuth2 providers (disabled by default):

1. **Google** - OpenID Connect provider
2. **GitHub** - OAuth2 provider
3. **Microsoft** - Azure AD / Microsoft Account

To enable a provider:
1. Update client_id and client_secret in oauth2_provider table
2. Set is_enabled = true
3. Configure redirect URI in provider's developer console

### Configuration

**Provider Setup:**

1. Register application with OAuth2 provider (Google, GitHub, etc.)
2. Get client ID and client secret
3. Configure redirect URI: `http://localhost:8080/api/oauth2/callback/{providerName}`
4. Update oauth2_provider table with credentials
5. Enable provider (is_enabled = true)

**Example - Google OAuth2:**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:8080/api/oauth2/callback/google`
6. Copy client ID and client secret

```sql
UPDATE oauth2_provider 
SET client_id = 'YOUR_GOOGLE_CLIENT_ID',
    client_secret = 'YOUR_GOOGLE_CLIENT_SECRET',
    is_enabled = true
WHERE provider_name = 'google';
```

**Example - GitHub OAuth2:**

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create new OAuth App
3. Set Authorization callback URL: `http://localhost:8080/api/oauth2/callback/github`
4. Copy client ID and client secret

```sql
UPDATE oauth2_provider 
SET client_id = 'YOUR_GITHUB_CLIENT_ID',
    client_secret = 'YOUR_GITHUB_CLIENT_SECRET',
    is_enabled = true
WHERE provider_name = 'github';
```

**Example - Microsoft OAuth2:**

1. Go to [Azure Portal](https://portal.azure.com/)
2. Register new application
3. Add redirect URI: `http://localhost:8080/api/oauth2/callback/microsoft`
4. Copy application (client) ID and client secret

```sql
UPDATE oauth2_provider 
SET client_id = 'YOUR_MICROSOFT_CLIENT_ID',
    client_secret = 'YOUR_MICROSOFT_CLIENT_SECRET',
    is_enabled = true
WHERE provider_name = 'microsoft';
```

### Security Considerations

1. **Client Secrets**
   - Store securely (consider encryption at rest)
   - Never expose in API responses
   - Rotate regularly

2. **State Parameter**
   - UUID generated for CSRF protection
   - Should be validated on callback (not currently implemented)

3. **Token Storage**
   - Access tokens stored for potential API calls to provider
   - Refresh tokens for token renewal
   - Consider encryption at rest for production

4. **Redirect URI Validation**
   - Whitelist allowed redirect URIs
   - Validate on callback

5. **Provider Trust**
   - Only enable trusted OAuth2 providers
   - Verify provider certificates
   - Use HTTPS in production

### Integration with Authorization

OAuth2 users are treated identically to local users for authorization:

- Same document-based access control
- Same group memberships
- Same permission resolution
- Same audit logging

The only difference is authentication method - OAuth2 users authenticate via external provider instead of password.

### Multi-Provider Support

Users can link multiple OAuth2 providers to a single account:

- Link Google account
- Link GitHub account
- Link Microsoft account
- All linked to same local user

This allows users to sign in with any linked provider.

### Future Enhancements

**Not Yet Implemented:**

1. **State Parameter Validation** - CSRF protection on callback
2. **Token Refresh** - Automatic access token renewal using refresh tokens
3. **Account Unlinking** - API to unlink OAuth2 accounts
4. **Provider Discovery** - OpenID Connect discovery endpoint support
5. **Admin UI** - Manage OAuth2 providers through admin interface
6. **Login Page Integration** - OAuth2 provider buttons on login page

---

## Authorization Layer

### Document-Based Access Control

The system uses a flexible document-based authorization model where:
- **Documents** = Records in database tables
- **Document Groups** = Collections of documents
- **Permissions** = Access controls granted on document groups

### Components

#### 1. Authorization Service

**AuthorizationService** (`service/AuthorizationService.java`)

**Main Method:**
```java
Mono<Boolean> hasAccess(Long authUserId, String tableName, Long recordId, String accessControl)
Mono<Boolean> hasAccess(Long authUserId, String tableName, Long recordId, String accessControl, String justification)
```

**Authorization Logic:**
1. Check if user is super user → Grant access
2. Check if user is in super group → Grant access
3. Find document groups containing the record
4. Resolve user's permissions on those groups
5. Check if user has required access control
6. Log access attempt to audit table
7. Return true/false

**Special Cases:**
- Super users need justification for DELETE operations
- Justification must be at least 10 characters
- Table-level CREATE checks use recordId = 0

#### 2. Document Group Matcher

**DocumentGroupMatcher** (`service/DocumentGroupMatcher.java`)

Matches records to document groups based on type:

**SINGLE_RECORD:**
- Checks if record_ids contains the specific record ID

**MULTIPLE_RECORDS:**
- Parses record_ids as JSON array
- Checks if record ID is in the array

**ENTIRE_TABLE:**
- Matches if table_name equals target table

**MULTIPLE_TABLES:**
- Matches if table_name equals target table

**CUSTOM_QUERY:**
- Requires record ID in record_ids list
- AND custom query must match
- Both conditions required

**CUSTOM_QUERY_ALL:**
- Only checks if custom query matches
- Ignores record_ids completely
- Grants access to all query results

#### 3. Query Executor

**QueryExecutor** (`service/QueryExecutor.java`)

Executes custom queries safely:

**QueryDefinition Model:**
```json
{
  "table": "users",
  "conditions": [
    {
      "field": "status",
      "operator": "EQUALS",
      "value": "active"
    },
    {
      "field": "department",
      "operator": "IN",
      "value": ["sales", "marketing"]
    }
  ],
  "logic": "AND"
}
```

**Supported Operators:**
- EQUALS, NOT_EQUALS
- GREATER_THAN, LESS_THAN
- LIKE
- IN, NOT_IN

**Security Features:**
- Table/field name sanitization (alphanumeric + underscore only)
- SQL value escaping (prevents injection)
- Parameterized queries via R2DBC

#### 4. Permission Resolver

**PermissionResolver** (`service/PermissionResolver.java`)

Resolves permissions using union logic:

**Process:**
1. Get user's direct permissions on document groups
2. Get user's group permissions on document groups
3. Combine all permissions (union)
4. Return set of access control names
5. Most permissive permission wins

**Time-Based Permissions:**
- Checks valid_from and valid_until
- Only includes active permissions
- Expired permissions automatically excluded

### Authorization Flow

```
1. Service calls AuthorizationService.hasAccess()
   ↓
2. Check super user/super group
   ↓
3. DocumentGroupMatcher finds matching document groups
   ↓
4. For CUSTOM_QUERY types, QueryExecutor runs queries
   ↓
5. PermissionResolver gets user's permissions
   ↓
6. Check if required access control is present
   ↓
7. AuditLoggingService logs the attempt
   ↓
8. Return true/false
```

### Service Layer Integration

All business services integrate authorization:

```java
public Mono<EntityOutputDTO> findById(Long id) {
    return SecurityContextHolder.getCurrentUser()
        .flatMap(user -> 
            authorizationService.hasAccess(
                user.getAuthUserId(), 
                "table_name", 
                id, 
                "READ"
            )
            .flatMap(hasAccess -> {
                if (!hasAccess) {
                    return Mono.error(new RuntimeException("Access denied"));
                }
                return repository.findById(id);
            })
        )
        .map(this::toOutputDTO);
}
```

**Permission Checks:**
- CREATE: Table-level (recordId = 0)
- READ: Record-level
- UPDATE: Record-level
- DELETE: Record-level (with optional justification)

---

## Audit Logging

### Components

**AuditLoggingService** (`service/AuditLoggingService.java`)

**Methods:**

1. `logAccessAttempt(userId, table, recordId, accessControl, granted, reason)`
   - Logs every access check
   - Records granted and denied attempts
   - Includes denial reason

2. `logSuperUserAction(userId, action, table, recordId, justification)`
   - Logs super user actions
   - Requires justification for DELETE

3. `validateSuperUserJustification(userId, action, justification)`
   - Validates DELETE justification
   - Minimum 10 characters required

4. `getAccessAuditLogs(userId, startTime, endTime)`
   - Query access logs by user and time range

5. `getDeniedAccessAttempts(startTime, endTime)`
   - Security monitoring for denied access

### Audit Controller

**AuditController** (`controller/AuditController.java`)

**Endpoints:**
- `GET /api/audit/access-logs/me` - Current user's access logs
- `GET /api/audit/super-user-logs/me` - Current user's super user logs
- `GET /api/audit/access-logs/user/{userId}` - User logs (admin only)
- `GET /api/audit/denied-access` - Denied access attempts (admin only)

### Audit Data

**Access Audit Log Fields:**
- auth_user_id
- action (access control name)
- table_name
- record_id
- access_granted (boolean)
- denial_reason
- ip_address
- user_agent
- accessed_at

**Super User Action Log Fields:**
- auth_user_id
- action
- target_table
- target_record_id
- justification
- performed_at

---

## Admin UI

### Overview

Thymeleaf-based web interface for managing users, groups, and permissions.

**Access:** Only super users and super admin group members

**Base URL:** `/admin`

### Pages

#### 1. Dashboard (`/admin`)
- Overview of admin functions
- Links to all management pages
- Current user display

#### 2. User Groups (`/admin/groups`)
- List all user groups
- Create new groups
- Edit existing groups
- Delete groups
- Mark groups as "default" (auto-assigned to new users)
- Mark groups as "super" (full access)

#### 3. Users (`/admin/users`)
- List all users
- View user details
- Manage group memberships
- Add users to groups
- Remove users from groups
- View user permissions

#### 4. Document Groups (`/admin/document-groups`)
- List all document groups
- Create new document groups
- Select document group type
- Add document definitions (table, record IDs, queries)
- Grant permissions to users/groups
- View existing permissions

### Admin Service

**AdminService** (`service/AdminService.java`)

**User Group Management:**
- `getAllGroups()` - List all groups
- `createGroup(name, description, isDefault, isSuperGroup)` - Create group
- `updateGroup(id, ...)` - Update group
- `deleteGroup(id)` - Delete group
- `getDefaultGroups()` - Get auto-assigned groups

**User Management:**
- `getAllUsers()` - List all users
- `getUserById(id)` - Get user details
- `getUserGroups(userId)` - Get user's groups
- `addUserToGroup(userId, groupId, validFrom, validUntil)` - Add membership
- `removeUserFromGroup(userId, groupId)` - Remove membership

**Document Group Management:**
- `getAllDocumentGroups()` - List all document groups
- `createDocumentGroup(name, description, typeId)` - Create group
- `addDocumentGroupDefinition(groupId, table, recordIds, query)` - Add definition
- `getDocumentGroupDefinitions(groupId)` - Get definitions

**Permission Management:**
- `getAllAccessControls()` - List access controls
- `grantPermission(docGroupId, userId, groupId, accessControlId, validFrom, validUntil)` - Grant permission
- `getDocumentGroupPermissions(docGroupId)` - Get permissions
- `revokePermission(permissionId)` - Revoke permission

### UI Features

- **Responsive Design:** Works on desktop and mobile
- **Inline CSS:** No external dependencies
- **Form Validation:** Required fields, input validation
- **Success Messages:** Confirmation after actions
- **Clean Layout:** Modern, professional appearance

---

## API Reference

### Authentication Endpoints

**POST /api/auth/register**
```json
Request:
{
  "username": "john.doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "username": "john.doe",
  "email": "john@example.com"
}
```

**POST /api/auth/login**
```json
Request:
{
  "username": "john.doe",
  "password": "SecurePass123"
}

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "expiresIn": 86400
}
```

**POST /api/auth/change-password**
```json
Request:
{
  "oldPassword": "OldPass123",
  "newPassword": "NewPass456"
}

Response:
{
  "message": "Password changed successfully"
}
```

### OAuth2 Endpoints

**GET /api/oauth2/providers**

List all enabled OAuth2 providers.

```json
Response:
[
  {
    "providerId": 1,
    "providerName": "google",
    "displayName": "Google",
    "authorizationUri": "https://accounts.google.com/o/oauth2/v2/auth",
    "scope": "openid profile email",
    "isEnabled": true
  },
  {
    "providerId": 2,
    "providerName": "github",
    "displayName": "GitHub",
    "authorizationUri": "https://github.com/login/oauth/authorize",
    "scope": "read:user user:email",
    "isEnabled": true
  }
]
```

**GET /api/oauth2/login/{providerName}?redirectUri=...**

Initiate OAuth2 authentication flow.

Parameters:
- `providerName` (path) - Provider name (google, github, microsoft)
- `redirectUri` (query, optional) - Custom redirect URI

```json
Response:
{
  "authorizationUrl": "https://accounts.google.com/o/oauth2/v2/auth?client_id=...&redirect_uri=...&response_type=code&scope=openid+profile+email&state=uuid",
  "state": "550e8400-e29b-41d4-a716-446655440000"
}
```

**GET /api/oauth2/callback/{providerName}?code=...&state=...&redirectUri=...**

Handle OAuth2 callback and return JWT token.

Parameters:
- `providerName` (path) - Provider name
- `code` (query) - Authorization code from provider
- `state` (query) - State parameter for CSRF protection
- `redirectUri` (query, optional) - Custom redirect URI

```json
Response (Success):
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "username": "john.doe",
  "email": "john@example.com"
}

Response (Error):
{
  "error": "OAuth2 authentication failed: Invalid authorization code"
}
```

### Business Endpoints

All business endpoints require JWT token in Authorization header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Standard CRUD Operations:**
- `POST /api/{entity}` - Create (requires CREATE permission)
- `GET /api/{entity}/{id}` - Read (requires READ permission)
- `GET /api/{entity}` - List (filters by READ permission)
- `PUT /api/{entity}/{id}` - Update (requires UPDATE permission)
- `DELETE /api/{entity}/{id}` - Delete (requires DELETE permission)
- `DELETE /api/{entity}/{id}/with-justification?justification=...` - Delete with justification (super users)

### Admin Endpoints

**User Groups:**
- `GET /admin/groups` - List groups page
- `GET /admin/groups/new` - Create group form
- `POST /admin/groups` - Create group
- `GET /admin/groups/{id}/edit` - Edit group form
- `POST /admin/groups/{id}` - Update group
- `POST /admin/groups/{id}/delete` - Delete group

**Users:**
- `GET /admin/users` - List users page
- `GET /admin/users/{id}` - User detail page
- `POST /admin/users/{userId}/groups/{groupId}/add` - Add to group
- `POST /admin/users/{userId}/groups/{groupId}/remove` - Remove from group

**Document Groups:**
- `GET /admin/document-groups` - List document groups page
- `GET /admin/document-groups/new` - Create document group form
- `POST /admin/document-groups` - Create document group
- `GET /admin/document-groups/{id}` - Document group detail page
- `POST /admin/document-groups/{id}/definitions` - Add definition
- `POST /admin/document-groups/{id}/permissions` - Grant permission

### Audit Endpoints

- `GET /api/audit/access-logs/me?startTime=...&endTime=...` - Current user's logs
- `GET /api/audit/super-user-logs/me?startTime=...&endTime=...` - Current user's super user logs
- `GET /api/audit/access-logs/user/{userId}?startTime=...&endTime=...` - User logs (admin)
- `GET /api/audit/denied-access?startTime=...&endTime=...` - Denied attempts (admin)

---

## Configuration

### application.yml

```yaml
# JWT Configuration
jwt:
  secret: your-secret-key-change-in-production
  expiration: 86400000  # 24 hours in milliseconds

# Security Configuration
security:
  csrf:
    enabled: false
  cors:
    enabled: false
  https:
    enabled: false

# Database Configuration
spring:
  r2dbc:
    url: r2dbc:mysql://localhost:3306/your_database
    username: root
    password: password
```

### Security Settings

**CSRF Protection:**
- Disabled by default (stateless JWT)
- Can be enabled in application.yml

**CORS:**
- Disabled by default
- Configure allowed origins in application.yml

**HTTPS:**
- Disabled by default
- Enable for production environments

**Public Endpoints:**
- `/setup` - Initial setup
- `/api/auth/**` - Authentication
- `/swagger-ui/**` - API documentation
- `/v3/api-docs/**` - OpenAPI spec

---

## Security Best Practices

### Password Security

1. **BCrypt Hashing:** All passwords hashed with BCrypt (cost factor 10)
2. **No Plain Text:** Passwords never stored in plain text
3. **Validation:** Minimum password requirements enforced
4. **Change Password:** Requires old password verification

### JWT Security

1. **Secret Key:** Use strong, random secret key in production
2. **Expiration:** Tokens expire after configured time
3. **HTTPS Only:** Use HTTPS in production to protect tokens
4. **Token Storage:** Store tokens securely on client (httpOnly cookies recommended)

### Authorization Security

1. **Principle of Least Privilege:** Grant minimum required permissions
2. **Time-Limited Permissions:** Use valid_until for temporary access
3. **Regular Audits:** Review audit logs regularly
4. **Super User Justification:** Require justification for sensitive operations
5. **SQL Injection Prevention:** Query executor sanitizes all inputs

### Database Security

1. **Separate Schema:** Auth tables in dedicated schema
2. **Foreign Keys:** Enforce referential integrity
3. **Indexes:** Optimize query performance
4. **Backups:** Regular backups of auth tables

### Operational Security

1. **Setup Once:** Setup endpoint disabled after first use
2. **Admin Access:** Restrict admin UI to trusted networks
3. **Audit Monitoring:** Monitor denied access attempts
4. **Password Rotation:** Encourage regular password changes
5. **Group Review:** Regularly review group memberships

---

## Troubleshooting

### Common Issues

**1. Cannot access /setup**
- Check if setup is already complete in system_config table
- Verify application is running
- Check logs for errors

**2. JWT token invalid**
- Check token expiration
- Verify secret key matches between token generation and validation
- Ensure Authorization header format: `Bearer <token>`

**3. Access denied errors**
- Verify user has required permission
- Check document group definitions
- Review audit logs for denial reason
- Confirm user is in correct groups

**4. Super user cannot delete**
- Provide justification parameter
- Use `/with-justification` endpoint
- Ensure justification is at least 10 characters

**5. Custom query not working**
- Validate JSON query definition format
- Check table and field names
- Review query executor logs
- Test query manually in database

**6. Admin UI not accessible**
- Verify user is super user or in super group
- Check SecurityContextHolder has current user
- Review JWT token validity

### Debug Tips

1. **Enable Debug Logging:**
```yaml
logging:
  level:
    com.yourpackage.service: DEBUG
    com.yourpackage.security: DEBUG
```

2. **Check Audit Logs:**
```sql
SELECT * FROM access_audit_log 
WHERE auth_user_id = ? 
ORDER BY accessed_at DESC 
LIMIT 100;
```

3. **Verify Permissions:**
```sql
SELECT dp.*, ac.control_name, dg.group_name
FROM document_permission dp
JOIN access_control ac ON dp.access_control_id = ac.control_id
JOIN document_group dg ON dp.document_group_id = dg.document_group_id
WHERE dp.auth_user_id = ?
  AND (dp.valid_until IS NULL OR dp.valid_until > NOW());
```

4. **Check Group Memberships:**
```sql
SELECT ugm.*, ug.group_name
FROM user_group_membership ugm
JOIN user_group ug ON ugm.group_id = ug.group_id
WHERE ugm.auth_user_id = ?
  AND (ugm.valid_until IS NULL OR ugm.valid_until > NOW());
```

---

## Appendix

### File Structure

```
swfaw_v2/
├── templates/
│   ├── auth_schema_templates.py          # Database schema
│   ├── auth_entity_templates.py          # Auth entities
│   ├── auth_repository_templates.py      # Auth repositories
│   ├── auth_service_templates.py         # Authentication service
│   ├── authorization_service_templates.py # Authorization service
│   ├── audit_logging_templates.py        # Audit logging
│   ├── setup_templates.py                # Setup UI
│   ├── admin_ui_templates.py             # Admin service/controller
│   ├── admin_html_templates.py           # Admin HTML pages
│   └── oauth2_templates.py               # OAuth2 components (NEW)
├── generators/
│   ├── auth_schema_generator.py
│   ├── auth_entity_generator.py
│   ├── auth_repository_generator.py
│   ├── auth_service_generator.py
│   ├── authorization_service_generator.py
│   ├── audit_logging_generator.py
│   ├── setup_generator.py
│   ├── admin_ui_generator.py
│   └── oauth2_generator.py               # OAuth2 generator (NEW)
└── main.py                               # Main generator
```

### Generated Files

**Per Application:**
- 11 auth entity classes
- 11 auth repository interfaces
- 2 OAuth2 entity classes (NEW)
- 2 OAuth2 repository interfaces (NEW)
- 1 OAuth2 service (NEW)
- 1 OAuth2 controller (NEW)
- 1 auth schema SQL file
- 5 auth service classes
- 3 auth controllers
- 10 Thymeleaf HTML templates
- Security configuration classes
- JWT components

**Total:** ~76 files, ~11,000 lines of code

### Version History

**v2.1 (March 5, 2026)**
- Added OAuth2/OpenID Connect authentication
- OAuth2Provider and OAuth2LinkedAccount entities
- OAuth2Service with complete OAuth2 flow
- OAuth2Controller with 3 REST endpoints
- External identity linking
- Multi-provider support per user
- Pre-configured providers (Google, GitHub, Microsoft)

**v2.0 (March 5, 2026)**
- Complete redesign of auth/authz system
- Document-based authorization
- 6 document group types
- Custom query support
- Audit logging
- Admin UI
- Super user justification

**v1.0 (Previous)**
- Basic JWT authentication
- Simple role-based authorization
- No audit logging
- No admin UI

---

## Support

For issues, questions, or contributions:
- Review this documentation
- Check troubleshooting section
- Review generated code
- Examine audit logs
- Test with simple scenarios first

---

**End of Documentation**
