# Task 16: Third-Party Authentication Code Generation Prompts - COMPLETE

## Summary
Updated the Authentication DDL Generator prompt to include third-party authentication support (OAuth2, SAML, OIDC) with comprehensive table generation functions.

---

## What Was Updated

### File Updated
**File:** `spring_webflux_application_writer_code_generation_prompts/13_AUTHENTICATION_DDL_GENERATOR.md`

**Changes:**
1. Added version 2.1 with third-party auth support
2. Added 2 new table generation functions
3. Added default providers data function
4. Updated configuration options
5. Updated drop statements
6. Updated documentation and examples

---

## New Configuration Options

```javascript
AuthenticationDDLGenerator {
  // ... existing options ...
  
  // NEW OPTIONS
  includeDefaultProviders: boolean,  // Include default OAuth2/OIDC providers
  includeThirdPartyAuth: boolean,    // Enable third-party auth tables
}
```

**Usage:**
```javascript
const config = {
  databaseName: 'emotisense_db',
  includeThirdPartyAuth: true,       // Enable OAuth2/SAML/OIDC
  includeDefaultProviders: true,     // Add Google, GitHub, etc.
  includeDefaultRoles: true,
  outputPath: 'output/authentication_authorization_schema.sql'
};
```

---

## New Table Generation Functions

### 1. generateAuthProviderTable()

**Purpose:** Generate `ems_auth_provider` table

**Output:**
```sql
CREATE TABLE ems_auth_provider (
    provider_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    provider_name VARCHAR(50) NOT NULL UNIQUE,
    provider_type VARCHAR(20) NOT NULL,  -- OAUTH2, SAML, OIDC
    display_name VARCHAR(100) NOT NULL,
    
    -- OAuth2/OIDC config
    client_id VARCHAR(255),
    client_secret VARCHAR(255),
    authorization_uri VARCHAR(500),
    token_uri VARCHAR(500),
    user_info_uri VARCHAR(500),
    jwks_uri VARCHAR(500),
    issuer VARCHAR(500),
    
    -- SAML config
    saml_entity_id VARCHAR(500),
    saml_sso_url VARCHAR(500),
    saml_certificate TEXT,
    
    -- Settings
    is_enabled BOOLEAN DEFAULT TRUE,
    auto_create_user BOOLEAN DEFAULT TRUE,
    auto_verify_email BOOLEAN DEFAULT TRUE,
    scopes TEXT,
    
    -- Audit fields
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME NULL,
    
    -- Indexes
    INDEX idx_provider_name (provider_name),
    INDEX idx_provider_type (provider_type),
    INDEX idx_enabled (is_enabled, deleted_at)
);
```

### 2. generateAuthUserProviderTable()

**Purpose:** Generate `ems_auth_user_provider` table

**Output:**
```sql
CREATE TABLE ems_auth_user_provider (
    user_provider_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    
    -- Relationship
    auth_user_id BIGINT NOT NULL,
    provider_id BIGINT NOT NULL,
    
    -- Provider user identification
    provider_user_id VARCHAR(255) NOT NULL,
    provider_username VARCHAR(255),
    provider_email VARCHAR(255),
    
    -- Provider data
    provider_profile JSON,
    
    -- OAuth2 tokens
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at DATETIME,
    id_token TEXT,
    
    -- SAML session
    saml_session_index VARCHAR(255),
    saml_name_id VARCHAR(255),
    
    -- Metadata
    first_login_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login_at DATETIME,
    login_count INT DEFAULT 1,
    
    -- Audit fields
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME NULL,
    
    -- Indexes
    INDEX idx_auth_user (auth_user_id, deleted_at),
    INDEX idx_provider (provider_id, deleted_at),
    INDEX idx_provider_user (provider_id, provider_user_id),
    INDEX idx_provider_email (provider_id, provider_email),
    
    -- Foreign keys
    FOREIGN KEY (auth_user_id) REFERENCES ems_auth_user(auth_user_id) ON DELETE CASCADE,
    FOREIGN KEY (provider_id) REFERENCES ems_auth_provider(provider_id) ON DELETE CASCADE,
    
    -- Unique constraints
    UNIQUE KEY uk_auth_user_provider (auth_user_id, provider_id, deleted_at),
    UNIQUE KEY uk_provider_user (provider_id, provider_user_id, deleted_at)
);
```

### 3. generateDefaultProvidersData()

**Purpose:** Insert default authentication providers

**Output:**
```sql
INSERT INTO ems_auth_provider (provider_name, provider_type, display_name, is_enabled, auto_create_user, auto_verify_email) VALUES
('google', 'OAUTH2', 'Google', FALSE, TRUE, TRUE),
('github', 'OAUTH2', 'GitHub', FALSE, TRUE, TRUE),
('facebook', 'OAUTH2', 'Facebook', FALSE, TRUE, TRUE),
('microsoft', 'OAUTH2', 'Microsoft', FALSE, TRUE, TRUE),
('azure_ad', 'OIDC', 'Azure Active Directory', FALSE, TRUE, TRUE),
('okta', 'OIDC', 'Okta', FALSE, TRUE, TRUE);
```

---

## Updated Generation Flow

### With Third-Party Auth Enabled

```javascript
function generateAuthenticationDDL(config) {
  const ddl = [];
  
  // 1. Database selection
  if (config.databaseName) {
    ddl.push(`USE ${config.databaseName};`);
  }
  
  // 2. Drop statements (if enabled)
  if (config.includeDropStatements) {
    ddl.push(...generateDropStatements());
  }
  
  // 3. Core authentication tables
  ddl.push(...generateAuthUserTable(config));
  ddl.push(...generateRoleTable(config));
  ddl.push(...generateAuthUserRoleTable(config));
  ddl.push(...generateAuthUserLinkTable(config));
  
  // 4. Third-party authentication tables (NEW)
  if (config.includeThirdPartyAuth) {
    ddl.push(...generateAuthProviderTable(config));
    ddl.push(...generateAuthUserProviderTable(config));
  }
  
  // 5. Authorization tables
  ddl.push(...generateUserGroupTable(config));
  ddl.push(...generateUserGroupMembershipTable(config));
  ddl.push(...generateEntityAuthorizationTable(config));
  
  // 6. Default roles data
  if (config.includeDefaultRoles) {
    ddl.push(...generateDefaultRolesData(config));
  }
  
  // 7. Default providers data (NEW)
  if (config.includeDefaultProviders && config.includeThirdPartyAuth) {
    ddl.push(...generateDefaultProvidersData(config));
  }
  
  // 8. Write to file
  writeToFile(config.outputPath, ddl.join('\n'));
  
  return {
    success: true,
    outputPath: config.outputPath,
    tablesGenerated: config.includeThirdPartyAuth ? 9 : 7,
    linesGenerated: ddl.length
  };
}
```

---

## Updated Drop Statements

```javascript
function generateDropStatements() {
  return [
    'DROP TABLE IF EXISTS ems_entity_authorization;',
    'DROP TABLE IF EXISTS ems_user_group_membership;',
    'DROP TABLE IF EXISTS ems_user_group;',
    'DROP TABLE IF EXISTS ems_auth_user_link;',
    'DROP TABLE IF EXISTS ems_auth_user_provider;',  // NEW
    'DROP TABLE IF EXISTS ems_auth_provider;',       // NEW
    'DROP TABLE IF EXISTS ems_auth_user_role;',
    'DROP TABLE IF EXISTS ems_role;',
    'DROP TABLE IF EXISTS ems_auth_user;',
  ];
}
```

---

## Table Count

### Basic Configuration (includeThirdPartyAuth: false)
**7 Tables:**
1. ems_auth_user
2. ems_role
3. ems_auth_user_role
4. ems_auth_user_link
5. ems_user_group
6. ems_user_group_membership
7. ems_entity_authorization

### Full Configuration (includeThirdPartyAuth: true)
**9 Tables:**
1. ems_auth_user
2. ems_auth_provider ← NEW
3. ems_auth_user_provider ← NEW
4. ems_role
5. ems_auth_user_role
6. ems_auth_user_link
7. ems_user_group
8. ems_user_group_membership
9. ems_entity_authorization

---

## Updated Documentation

### Key Features Section

**Added:**
- Third-Party Auth Support: Optional OAuth2, SAML, OIDC provider tables
- Default Data: Includes default system roles and authentication providers
- Flexible Configuration: Enable/disable third-party auth as needed

### Notes Section

**Updated:**
- Generates 7 tables (basic) or 9 tables (with third-party auth)
- Third-party auth tables are optional - enable via `includeThirdPartyAuth` config

---

## Integration with Existing Files

### Related Files

**1. DDL Output (v2):**
- `code_output/authentication_authorization_schema_v2.sql`
- Complete schema with third-party auth tables
- Ready to execute

**2. Documentation:**
- `THIRD_PARTY_AUTHENTICATION_MAPPING.md`
- Explains how third-party auth is mapped
- Provider-specific examples
- Authentication flows

**3. Original DDL (v1):**
- `code_output/authentication_authorization_schema.sql`
- Basic schema without third-party auth
- Still valid for simple use cases

---

## Usage Examples

### Example 1: Basic Auth Only

```javascript
const config = {
  databaseName: 'my_app_db',
  includeThirdPartyAuth: false,  // No OAuth2/SAML
  includeDefaultRoles: true,
  outputPath: 'output/auth_schema.sql'
};

generateAuthenticationDDL(config);
// Generates 7 tables
```

### Example 2: Full Auth with Third-Party

```javascript
const config = {
  databaseName: 'my_app_db',
  includeThirdPartyAuth: true,      // Enable OAuth2/SAML/OIDC
  includeDefaultProviders: true,    // Add Google, GitHub, etc.
  includeDefaultRoles: true,
  outputPath: 'output/auth_schema_full.sql'
};

generateAuthenticationDDL(config);
// Generates 9 tables + default providers
```

### Example 3: Custom Providers Only

```javascript
const config = {
  databaseName: 'my_app_db',
  includeThirdPartyAuth: true,      // Enable tables
  includeDefaultProviders: false,   // Don't add default providers
  includeDefaultRoles: true,
  outputPath: 'output/auth_schema_custom.sql'
};

generateAuthenticationDDL(config);
// Generates 9 tables, no default providers
// Add your own providers manually
```

---

## Provider Configuration Examples

### Google OAuth2

```javascript
// After running generator, configure Google:
const googleConfig = {
  provider_name: 'google',
  client_id: 'your-client-id.apps.googleusercontent.com',
  client_secret: 'your-client-secret',
  authorization_uri: 'https://accounts.google.com/o/oauth2/v2/auth',
  token_uri: 'https://oauth2.googleapis.com/token',
  user_info_uri: 'https://www.googleapis.com/oauth2/v2/userinfo',
  scopes: '["openid", "profile", "email"]',
  is_enabled: true
};

// Update provider in database
UPDATE ems_auth_provider 
SET client_id = ?, client_secret = ?, is_enabled = TRUE
WHERE provider_name = 'google';
```

### Azure AD (OIDC)

```javascript
const azureConfig = {
  provider_name: 'azure_ad',
  client_id: 'your-azure-client-id',
  client_secret: 'your-azure-client-secret',
  authorization_uri: 'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize',
  token_uri: 'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token',
  jwks_uri: 'https://login.microsoftonline.com/{tenant}/discovery/v2.0/keys',
  issuer: 'https://login.microsoftonline.com/{tenant}/v2.0',
  scopes: '["openid", "profile", "email"]',
  is_enabled: true
};
```

---

## Benefits

### 1. Flexibility
- Enable/disable third-party auth as needed
- Start with basic auth, add OAuth2 later
- No code changes required

### 2. Completeness
- All provider types supported (OAuth2, SAML, OIDC)
- Common providers pre-configured
- Easy to add custom providers

### 3. Consistency
- Same generator for all auth types
- Unified schema design
- Consistent naming conventions

### 4. Maintainability
- Single source of truth (generator prompt)
- Easy to update all projects
- Version controlled

### 5. Documentation
- Comprehensive comments in generated SQL
- Usage examples included
- Provider-specific guidance

---

## Testing

### Test Configuration

```javascript
// Test with third-party auth
const testConfig = {
  databaseName: 'test_db',
  includeThirdPartyAuth: true,
  includeDefaultProviders: true,
  includeDefaultRoles: true,
  includeDropStatements: true,  // Clean slate
  outputPath: 'test/auth_schema.sql'
};

const result = generateAuthenticationDDL(testConfig);

// Verify
assert(result.success === true);
assert(result.tablesGenerated === 9);
assert(fs.existsSync(result.outputPath));
```

---

## Migration Path

### From v1 (Basic) to v2 (Third-Party)

**Step 1: Generate new schema**
```javascript
const config = {
  includeThirdPartyAuth: true,
  includeDefaultProviders: true,
  outputPath: 'migration/add_third_party_auth.sql'
};
```

**Step 2: Extract only new tables**
```sql
-- From generated file, extract:
CREATE TABLE ems_auth_provider (...);
CREATE TABLE ems_auth_user_provider (...);
INSERT INTO ems_auth_provider (...);
```

**Step 3: Apply migration**
```bash
mysql -u root -p my_db < migration/add_third_party_auth.sql
```

**Step 4: Update auth_user table**
```sql
-- Add auth_type column
ALTER TABLE ems_auth_user 
ADD COLUMN auth_type VARCHAR(20) DEFAULT 'LOCAL' AFTER password;

-- Make username and password nullable for OAuth2 users
ALTER TABLE ems_auth_user 
MODIFY COLUMN username VARCHAR(50) UNIQUE,
MODIFY COLUMN password VARCHAR(255);
```

---

## Status: COMPLETE ✅

Successfully updated:
1. ✅ Generator prompt with third-party auth support
2. ✅ Added 2 new table generation functions
3. ✅ Added default providers data function
4. ✅ Updated configuration options
5. ✅ Updated drop statements
6. ✅ Updated documentation and examples
7. ✅ Updated table count (7 → 9)
8. ✅ Added usage examples
9. ✅ Added migration guidance

The Authentication DDL Generator now fully supports third-party authentication with comprehensive code generation prompts!
