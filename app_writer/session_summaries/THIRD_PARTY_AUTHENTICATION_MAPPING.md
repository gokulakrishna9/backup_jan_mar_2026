# Third-Party Authentication Mapping

## Overview
This document explains how third-party authentication (OAuth2, SAML, OIDC) is mapped to the database schema.

---

## Architecture

### Three-Table Design

```
┌─────────────────────┐
│  ems_auth_user      │  ← Core authentication user
│  - auth_user_id     │
│  - email            │
│  - auth_type        │  (LOCAL, OAUTH2, SAML, OIDC, HYBRID)
└──────────┬──────────┘
           │
           │ 1:N
           ▼
┌─────────────────────────────┐
│  ems_auth_user_provider     │  ← Links user to providers
│  - auth_user_id             │
│  - provider_id              │
│  - provider_user_id         │  ← User ID from provider
│  - access_token             │
│  - refresh_token            │
│  - provider_profile (JSON)  │
└──────────┬──────────────────┘
           │ N:1
           ▼
┌─────────────────────┐
│  ems_auth_provider  │  ← Provider configuration
│  - provider_id      │
│  - provider_name    │  (google, github, azure_ad)
│  - provider_type    │  (OAUTH2, SAML, OIDC)
│  - client_id        │
│  - client_secret    │
└─────────────────────┘
```

---

## Table 1: ems_auth_user (Updated)

### Purpose
Core authentication user that supports BOTH local and third-party authentication.

### Key Changes

**Added Fields:**
```sql
auth_type VARCHAR(20) DEFAULT 'LOCAL'  -- LOCAL, OAUTH2, SAML, OIDC, HYBRID
```

**Made Optional (for third-party only users):**
```sql
username VARCHAR(50) UNIQUE,  -- NULL for OAuth2-only users
password VARCHAR(255),        -- NULL for OAuth2-only users
```

### Authentication Types

1. **LOCAL** - Traditional username/password
   - `username` and `password` required
   - Email verification optional

2. **OAUTH2** - OAuth2 providers (Google, GitHub, Facebook)
   - `username` and `password` NULL
   - Email from provider
   - Linked via `ems_auth_user_provider`

3. **SAML** - SAML 2.0 providers (Enterprise SSO)
   - `username` and `password` NULL
   - Email from SAML assertion
   - Linked via `ems_auth_user_provider`

4. **OIDC** - OpenID Connect providers (Azure AD, Okta)
   - `username` and `password` NULL
   - Email from ID token
   - Linked via `ems_auth_user_provider`

5. **HYBRID** - Both local AND third-party
   - `username` and `password` present
   - Can login with password OR OAuth2
   - Multiple providers supported

---

## Table 2: ems_auth_provider (NEW)

### Purpose
Stores configuration for third-party authentication providers.

### Schema

```sql
CREATE TABLE ems_auth_provider (
    provider_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    
    -- Identification
    provider_name VARCHAR(50) NOT NULL UNIQUE,  -- 'google', 'github', 'azure_ad'
    provider_type VARCHAR(20) NOT NULL,         -- OAUTH2, SAML, OIDC
    display_name VARCHAR(100) NOT NULL,         -- 'Google', 'GitHub'
    
    -- OAuth2/OIDC Configuration
    client_id VARCHAR(255),
    client_secret VARCHAR(255),
    authorization_uri VARCHAR(500),
    token_uri VARCHAR(500),
    user_info_uri VARCHAR(500),
    jwks_uri VARCHAR(500),
    issuer VARCHAR(500),
    
    -- SAML Configuration
    saml_entity_id VARCHAR(500),
    saml_sso_url VARCHAR(500),
    saml_certificate TEXT,
    
    -- Settings
    is_enabled BOOLEAN DEFAULT TRUE,
    auto_create_user BOOLEAN DEFAULT TRUE,
    auto_verify_email BOOLEAN DEFAULT TRUE,
    scopes TEXT,  -- JSON array
    
    -- Audit
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME NULL
);
```

### Default Providers

```sql
INSERT INTO ems_auth_provider (provider_name, provider_type, display_name) VALUES
('google', 'OAUTH2', 'Google'),
('github', 'OAUTH2', 'GitHub'),
('facebook', 'OAUTH2', 'Facebook'),
('microsoft', 'OAUTH2', 'Microsoft'),
('azure_ad', 'OIDC', 'Azure Active Directory'),
('okta', 'OIDC', 'Okta');
```

---

## Table 3: ems_auth_user_provider (NEW)

### Purpose
Links authentication users to third-party providers. Stores provider-specific data.

### Schema

```sql
CREATE TABLE ems_auth_user_provider (
    user_provider_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    
    -- Relationship
    auth_user_id BIGINT NOT NULL,
    provider_id BIGINT NOT NULL,
    
    -- Provider User Identification
    provider_user_id VARCHAR(255) NOT NULL,     -- User ID from provider
    provider_username VARCHAR(255),             -- Username from provider
    provider_email VARCHAR(255),                -- Email from provider
    
    -- Provider Data
    provider_profile JSON,                      -- Full profile from provider
    
    -- OAuth2 Tokens
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at DATETIME,
    id_token TEXT,
    
    -- SAML Session
    saml_session_index VARCHAR(255),
    saml_name_id VARCHAR(255),
    
    -- Metadata
    first_login_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login_at DATETIME,
    login_count INT DEFAULT 1,
    
    -- Audit
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME NULL,
    
    -- Constraints
    UNIQUE KEY uk_auth_user_provider (auth_user_id, provider_id, deleted_at),
    UNIQUE KEY uk_provider_user (provider_id, provider_user_id, deleted_at)
);
```

### Key Fields Explained

**provider_user_id:**
- The user's ID in the provider's system
- Examples:
  - Google: `"1234567890"` (Google user ID)
  - GitHub: `"12345678"` (GitHub user ID)
  - Azure AD: `"a1b2c3d4-e5f6-7890-abcd-ef1234567890"` (Azure AD object ID)

**provider_profile (JSON):**
- Full profile data from provider
- Examples:
```json
{
  "id": "1234567890",
  "email": "user@gmail.com",
  "name": "John Doe",
  "picture": "https://...",
  "given_name": "John",
  "family_name": "Doe",
  "locale": "en"
}
```

**access_token:**
- OAuth2 access token
- Used to call provider APIs
- Should be encrypted in production

**refresh_token:**
- OAuth2 refresh token
- Used to get new access tokens
- Should be encrypted in production

**id_token:**
- OIDC ID token (JWT)
- Contains user claims
- Can be validated

---

## Authentication Flows

### Flow 1: OAuth2 Login (First Time)

```
1. User clicks "Login with Google"
   ↓
2. Redirect to Google authorization endpoint
   ↓
3. User authorizes application
   ↓
4. Google redirects back with authorization code
   ↓
5. Exchange code for tokens (access_token, refresh_token, id_token)
   ↓
6. Get user profile from Google
   ↓
7. Check if user exists:
   - Query: SELECT * FROM ems_auth_user_provider 
            WHERE provider_id = ? AND provider_user_id = ?
   ↓
8. User NOT found → Create new user:
   a. INSERT INTO ems_auth_user (email, auth_type, is_email_verified)
      VALUES (google_email, 'OAUTH2', TRUE)
   
   b. INSERT INTO ems_auth_user_provider 
      (auth_user_id, provider_id, provider_user_id, provider_email, 
       access_token, refresh_token, provider_profile)
      VALUES (new_auth_user_id, google_provider_id, google_user_id, ...)
   
   c. Assign default USER role
   
   d. Create application user (ems_user)
   
   e. Link auth user to app user (ems_auth_user_link)
   ↓
9. Generate JWT token with auth_user_id
   ↓
10. Return JWT to client
```

### Flow 2: OAuth2 Login (Returning User)

```
1. User clicks "Login with Google"
   ↓
2-6. Same as first time
   ↓
7. Check if user exists:
   - Query: SELECT aup.*, au.* 
            FROM ems_auth_user_provider aup
            JOIN ems_auth_user au ON aup.auth_user_id = au.auth_user_id
            WHERE aup.provider_id = ? AND aup.provider_user_id = ?
            AND aup.deleted_at IS NULL AND au.deleted_at IS NULL
   ↓
8. User FOUND → Update tokens:
   - UPDATE ems_auth_user_provider
     SET access_token = ?, refresh_token = ?, 
         token_expires_at = ?, last_login_at = NOW(),
         login_count = login_count + 1
     WHERE user_provider_id = ?
   
   - UPDATE ems_auth_user
     SET last_login_at = NOW()
     WHERE auth_user_id = ?
   ↓
9. Generate JWT token with auth_user_id
   ↓
10. Return JWT to client
```

### Flow 3: Hybrid Login (Local + OAuth2)

```
User has BOTH local password AND Google account linked

Option A: Login with password
1. User enters username/password
2. Validate credentials
3. Generate JWT with auth_user_id
4. Return JWT

Option B: Login with Google
1. OAuth2 flow (as above)
2. Find existing auth_user by provider_user_id
3. Generate JWT with SAME auth_user_id
4. Return JWT

Result: Same auth_user_id, same authorization, same app user
```

### Flow 4: Link Provider to Existing Account

```
User has local account, wants to add Google login

1. User is already logged in (has JWT)
2. User clicks "Link Google Account"
3. OAuth2 flow to get Google tokens
4. Check if Google account already linked to another user:
   - Query: SELECT * FROM ems_auth_user_provider
            WHERE provider_id = ? AND provider_user_id = ?
   
5. If NOT linked:
   - INSERT INTO ems_auth_user_provider
     (auth_user_id, provider_id, provider_user_id, ...)
     VALUES (current_auth_user_id, google_provider_id, ...)
   
   - UPDATE ems_auth_user
     SET auth_type = 'HYBRID'
     WHERE auth_user_id = current_auth_user_id

6. User can now login with password OR Google
```

---

## Provider-Specific Mappings

### Google OAuth2

**Provider Configuration:**
```sql
INSERT INTO ems_auth_provider (
    provider_name, provider_type, display_name,
    client_id, client_secret,
    authorization_uri, token_uri, user_info_uri,
    scopes
) VALUES (
    'google', 'OAUTH2', 'Google',
    'your-client-id.apps.googleusercontent.com',
    'your-client-secret',
    'https://accounts.google.com/o/oauth2/v2/auth',
    'https://oauth2.googleapis.com/token',
    'https://www.googleapis.com/oauth2/v2/userinfo',
    '["openid", "profile", "email"]'
);
```

**User Mapping:**
```sql
-- Google user profile
{
  "id": "1234567890",
  "email": "user@gmail.com",
  "verified_email": true,
  "name": "John Doe",
  "given_name": "John",
  "family_name": "Doe",
  "picture": "https://lh3.googleusercontent.com/...",
  "locale": "en"
}

-- Maps to:
INSERT INTO ems_auth_user_provider (
    auth_user_id, provider_id,
    provider_user_id,    -- "1234567890"
    provider_email,      -- "user@gmail.com"
    provider_username,   -- NULL (Google doesn't have username)
    provider_profile     -- Full JSON above
);
```

### GitHub OAuth2

**Provider Configuration:**
```sql
INSERT INTO ems_auth_provider (
    provider_name, provider_type, display_name,
    client_id, client_secret,
    authorization_uri, token_uri, user_info_uri,
    scopes
) VALUES (
    'github', 'OAUTH2', 'GitHub',
    'your-github-client-id',
    'your-github-client-secret',
    'https://github.com/login/oauth/authorize',
    'https://github.com/login/oauth/access_token',
    'https://api.github.com/user',
    '["user:email"]'
);
```

**User Mapping:**
```sql
-- GitHub user profile
{
  "id": 12345678,
  "login": "johndoe",
  "email": "john@example.com",
  "name": "John Doe",
  "avatar_url": "https://avatars.githubusercontent.com/...",
  "company": "Acme Corp",
  "location": "San Francisco"
}

-- Maps to:
INSERT INTO ems_auth_user_provider (
    auth_user_id, provider_id,
    provider_user_id,    -- "12345678"
    provider_email,      -- "john@example.com"
    provider_username,   -- "johndoe"
    provider_profile     -- Full JSON above
);
```

### Azure AD (OIDC)

**Provider Configuration:**
```sql
INSERT INTO ems_auth_provider (
    provider_name, provider_type, display_name,
    client_id, client_secret,
    authorization_uri, token_uri, jwks_uri, issuer,
    scopes
) VALUES (
    'azure_ad', 'OIDC', 'Azure Active Directory',
    'your-azure-client-id',
    'your-azure-client-secret',
    'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize',
    'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token',
    'https://login.microsoftonline.com/{tenant}/discovery/v2.0/keys',
    'https://login.microsoftonline.com/{tenant}/v2.0',
    '["openid", "profile", "email"]'
);
```

**User Mapping:**
```sql
-- Azure AD ID token claims
{
  "oid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "email": "user@company.com",
  "name": "John Doe",
  "preferred_username": "john.doe@company.com",
  "given_name": "John",
  "family_name": "Doe"
}

-- Maps to:
INSERT INTO ems_auth_user_provider (
    auth_user_id, provider_id,
    provider_user_id,    -- "a1b2c3d4-e5f6-7890-abcd-ef1234567890" (oid)
    provider_email,      -- "user@company.com"
    provider_username,   -- "john.doe@company.com"
    provider_profile,    -- Full claims
    id_token             -- Store ID token for validation
);
```

---

## Authorization Integration

### Key Point: Authorization Uses auth_user_id

**All authorization tables reference `auth_user_id`, NOT provider-specific IDs.**

```sql
-- Authorization check (same for local and OAuth2 users)
SELECT * FROM ems_entity_authorization
WHERE entity_type = 'Course'
  AND entity_id = 123
  AND auth_user_id = ?  -- Same auth_user_id regardless of login method
  AND deleted_at IS NULL;
```

### Example: User Logs In with Different Methods

```sql
-- User #1 (auth_user_id = 1)
-- Can login with:
--   1. Username/password (LOCAL)
--   2. Google (OAUTH2)
--   3. GitHub (OAUTH2)

-- All three methods result in SAME auth_user_id = 1
-- Therefore, SAME authorization applies

-- Authorization record:
INSERT INTO ems_entity_authorization (entity_type, entity_id, auth_user_id, access_level)
VALUES ('Course', 123, 1, 'READ');

-- User can access Course #123 regardless of login method
```

---

## Security Considerations

### 1. Token Storage

**Encrypt sensitive tokens:**
```sql
-- Before storing
access_token = encrypt(raw_access_token, encryption_key)
refresh_token = encrypt(raw_refresh_token, encryption_key)

-- When retrieving
raw_access_token = decrypt(access_token, encryption_key)
```

### 2. Token Expiration

**Check token expiration:**
```sql
SELECT * FROM ems_auth_user_provider
WHERE auth_user_id = ?
  AND provider_id = ?
  AND (token_expires_at IS NULL OR token_expires_at > NOW());
```

**Refresh expired tokens:**
```java
if (tokenExpired) {
    newAccessToken = refreshToken(refreshToken);
    updateTokens(authUserId, providerId, newAccessToken);
}
```

### 3. Provider User ID Uniqueness

**Enforce uniqueness:**
```sql
UNIQUE KEY uk_provider_user (provider_id, provider_user_id, deleted_at)
```

**Prevents:**
- Same Google account linked to multiple auth users
- Account takeover attacks

### 4. Email Verification

**Trust provider's email verification:**
```sql
-- If provider verifies email, trust it
INSERT INTO ems_auth_user (email, is_email_verified)
VALUES (provider_email, TRUE);  -- Trust Google's verification
```

---

## Query Examples

### Find User by Provider

```sql
-- Find auth user by Google ID
SELECT au.*
FROM ems_auth_user au
JOIN ems_auth_user_provider aup ON au.auth_user_id = aup.auth_user_id
JOIN ems_auth_provider ap ON aup.provider_id = ap.provider_id
WHERE ap.provider_name = 'google'
  AND aup.provider_user_id = '1234567890'
  AND aup.deleted_at IS NULL
  AND au.deleted_at IS NULL;
```

### Get All Providers for User

```sql
-- Get all linked providers for auth user
SELECT ap.provider_name, ap.display_name, aup.provider_email, aup.last_login_at
FROM ems_auth_user_provider aup
JOIN ems_auth_provider ap ON aup.provider_id = ap.provider_id
WHERE aup.auth_user_id = 1
  AND aup.deleted_at IS NULL
  AND ap.deleted_at IS NULL;
```

### Check if Provider Account Already Linked

```sql
-- Check if Google account already linked
SELECT aup.auth_user_id
FROM ems_auth_user_provider aup
JOIN ems_auth_provider ap ON aup.provider_id = ap.provider_id
WHERE ap.provider_name = 'google'
  AND aup.provider_user_id = '1234567890'
  AND aup.deleted_at IS NULL;
```

### Get User's Login Methods

```sql
-- Get all login methods for user
SELECT 
    au.auth_type,
    au.username,
    GROUP_CONCAT(ap.display_name) as providers
FROM ems_auth_user au
LEFT JOIN ems_auth_user_provider aup ON au.auth_user_id = aup.auth_user_id AND aup.deleted_at IS NULL
LEFT JOIN ems_auth_provider ap ON aup.provider_id = ap.provider_id AND ap.deleted_at IS NULL
WHERE au.auth_user_id = 1
  AND au.deleted_at IS NULL
GROUP BY au.auth_user_id;

-- Result:
-- auth_type | username | providers
-- HYBRID    | john_doe | Google,GitHub
```

---

## Summary

### Key Design Decisions

1. **Separate Provider Table** - Configuration separate from user data
2. **Link Table** - Many-to-many relationship (user can have multiple providers)
3. **Unified auth_user_id** - Same ID for local and OAuth2 users
4. **Flexible auth_type** - Supports LOCAL, OAUTH2, SAML, OIDC, HYBRID
5. **Token Storage** - Store tokens for API calls and refresh
6. **Provider Profile** - Store full profile as JSON for flexibility
7. **Authorization Integration** - All authorization uses auth_user_id

### Benefits

- ✅ Support multiple authentication methods
- ✅ Users can link multiple providers
- ✅ Unified authorization (same auth_user_id)
- ✅ Easy to add new providers
- ✅ Flexible and extensible
- ✅ Secure token storage
- ✅ Audit trail (login count, last login)
