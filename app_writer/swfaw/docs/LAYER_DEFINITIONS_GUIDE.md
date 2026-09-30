# Layer Definitions Guide (v2.3)

## Overview

Layer definitions give you complete control over code generation in swfaw_v2 v2.3. Instead of generating code directly from SQL, Phase 1 creates customizable JSON configuration files that you can modify before Phase 2 generates the actual code.

## What Are Layer Definitions?

Layer definitions are JSON files that describe how each layer of your application should be generated:

- **Per-Entity Layers**: Configure behavior for each entity (table)
- **Application-Wide Layers**: Configure global settings for the entire application

## File Structure

After running Phase 1, you'll find 15 files in `application_definitions/`:

```
application_definitions/
├── manifest.json                    # Version and file index
├── project_metadata.json            # Project configuration
├── entities.json                    # Table definitions
├── relationships.json               # Entity relationships
├── entity_layer.json               # Entity configurations
├── repository_layer.json           # Repository configurations
├── service_layer.json              # Service configurations
├── controller_layer.json           # Controller configurations
├── dto_layer.json                  # DTO configurations
├── security_layer.json             # Security settings
├── config_layer.json               # Application config
├── exception_layer.json            # Exception handling
├── audit_logging_layer.json        # Audit logging
├── authorization_layer.json        # Access control
└── custom_queries_layer.json       # Query templates
```

---

## Per-Entity Layer Definitions

### 1. entity_layer.json

Controls how JPA entities are generated.

**Key Settings:**
- `hasAuditFields`: Include created_at, updated_at, created_by, updated_by
- `hasSoftDelete`: Include deleted_at field for soft deletes
- `relationships`: Define entity relationships

**Example:**
```json
{
  "tableName": "users",
  "className": "User",
  "hasAuditFields": true,
  "hasSoftDelete": true,
  "relationships": [
    {
      "type": "OneToMany",
      "targetTable": "orders",
      "foreignKey": "user_id"
    }
  ]
}
```

### 2. repository_layer.json

Controls how R2DBC repositories are generated.

**Key Settings:**
- `hasCustomQueries`: Enable custom query methods
- `customQueries`: Define custom query methods
- `hasSoftDelete`: Filter soft-deleted records
- `enableCaching`: Enable repository-level caching

**Example:**
```json
{
  "entityName": "User",
  "className": "UserRepository",
  "hasCustomQueries": true,
  "customQueries": [
    {
      "methodName": "findByEmail",
      "query": "SELECT * FROM users WHERE email = :email",
      "returnType": "User"
    }
  ],
  "enableCaching": true,
  "cacheNames": ["users"]
}
```

### 3. service_layer.json

Controls how service classes are generated.

**Key Settings:**
- `hasAuthorization`: Enable authorization checks
- `authorizationConfig`: Configure authorization behavior
- `transactionManagement`: Configure transaction settings

**Example:**
```json
{
  "entityName": "User",
  "className": "UserService",
  "hasAuthorization": true,
  "authorizationConfig": {
    "checkOnCreate": true,
    "checkOnRead": true,
    "checkOnUpdate": true,
    "checkOnDelete": true,
    "allowPublicRead": false
  },
  "transactionManagement": {
    "enabled": true,
    "propagation": "REQUIRED",
    "timeout": 30
  }
}
```

### 4. controller_layer.json

Controls how REST controllers are generated.

**Key Settings:**
- `endpoints`: Enable/disable specific endpoints
- `corsConfig`: Configure CORS per controller
- `rateLimitPerMinute`: Set rate limits per endpoint

**Example:**
```json
{
  "entityName": "User",
  "className": "UserController",
  "basePath": "/api/v1/users",
  "endpoints": {
    "create": {
      "enabled": true,
      "requiresAuth": true,
      "roles": ["USER", "ADMIN"],
      "rateLimitPerMinute": 10
    },
    "delete": {
      "enabled": false  // Disable delete endpoint
    },
    "getAll": {
      "enabled": true,
      "supportsPagination": true,
      "supportsFiltering": true,
      "supportsSorting": true
    }
  }
}
```

### 5. dto_layer.json

Controls how DTOs are generated with validation rules.

**Key Settings:**
- `validation`: Validation rules per field
- `customValidators`: Custom validation logic
- `excludeSensitiveFields`: Fields to exclude from output DTOs

**Example:**
```json
{
  "entityName": "User",
  "dtoType": "Input",
  "className": "UserInputDTO",
  "fields": [
    {
      "fieldName": "email",
      "javaType": "String",
      "validation": {
        "required": true,
        "requiredMessage": "Email is required",
        "email": true,
        "emailMessage": "Please provide a valid email address",
        "maxLength": 255,
        "maxLengthMessage": "Email cannot exceed 255 characters"
      }
    },
    {
      "fieldName": "age",
      "javaType": "Integer",
      "validation": {
        "min": 18,
        "minMessage": "Must be at least 18 years old",
        "max": 120,
        "maxMessage": "Age cannot exceed 120"
      }
    }
  ]
}
```

---

## Application-Wide Layer Definitions

### 6. security_layer.json

Controls security configuration for the entire application.

**Key Settings:**
- `jwt`: JWT authentication configuration
- `oauth2`: OAuth2 provider configuration
- `passwordPolicy`: Password requirements
- `cors`: Global CORS settings
- `rateLimiting`: Global rate limiting

**Example:**
```json
{
  "jwt": {
    "enabled": true,
    "secret": "your-secret-key-change-in-production",
    "expiration": 86400000,  // 24 hours
    "issuer": "my-company",
    "audience": "my-users"
  },
  "oauth2": {
    "enabled": true,
    "providers": [
      {
        "name": "google",
        "clientId": "${GOOGLE_CLIENT_ID}",
        "clientSecret": "${GOOGLE_CLIENT_SECRET}",
        "scope": ["email", "profile"]
      }
    ]
  },
  "passwordPolicy": {
    "minLength": 8,
    "requireUppercase": true,
    "requireDigit": true,
    "requireSpecialChar": true
  }
}
```

### 7. config_layer.json

Controls application configuration.

**Key Settings:**
- `project`: Project metadata
- `server`: Server configuration
- `database`: Database connection settings
- `logging`: Logging configuration
- `features`: Feature flags (Swagger, Actuator, caching, email)

**Example:**
```json
{
  "project": {
    "name": "my-app",
    "displayName": "My Application",
    "version": "1.0.0"
  },
  "server": {
    "port": 8080,
    "compression": {
      "enabled": true
    }
  },
  "database": {
    "type": "mysql",
    "host": "localhost",
    "port": 3306,
    "name": "my_database"
  },
  "features": {
    "swagger": {
      "enabled": true,
      "title": "My API"
    },
    "caching": {
      "enabled": true,
      "type": "redis"
    }
  }
}
```

### 8. exception_layer.json

Controls exception handling.

**Key Settings:**
- `customExceptions`: Define custom exception classes
- `errorResponseFormat`: Configure error response structure
- `exceptionMessages`: Entity-specific error messages

**Example:**
```json
{
  "customExceptions": [
    {
      "className": "ResourceNotFoundException",
      "httpStatus": 404,
      "defaultMessage": "Resource not found"
    }
  ],
  "exceptionMessages": {
    "ResourceNotFoundException": {
      "User": "User not found with the provided ID",
      "Product": "Product not found in our catalog"
    }
  }
}
```

### 9. audit_logging_layer.json

Controls audit logging.

**Key Settings:**
- `auditEvents`: Configure which events to log
- `storage`: Configure where logs are stored
- `filtering`: Exclude specific users/endpoints
- `alerting`: Configure alerts for suspicious activity

**Example:**
```json
{
  "enabled": true,
  "auditEvents": {
    "authentication": {
      "enabled": true,
      "events": ["LOGIN_SUCCESS", "LOGIN_FAILURE", "LOGOUT"]
    },
    "dataAccess": {
      "enabled": true,
      "events": [
        {
          "eventType": "DELETE",
          "entities": ["User", "Product", "Order"]
        }
      ]
    }
  },
  "alerting": {
    "enabled": true,
    "alerts": [
      {
        "eventType": "MULTIPLE_LOGIN_FAILURES",
        "threshold": 5,
        "timeWindowMinutes": 15,
        "action": "SEND_EMAIL"
      }
    ]
  }
}
```

### 10. authorization_layer.json

Controls document-based access control.

**Key Settings:**
- `accessControls`: Define access control types (READ, CREATE, UPDATE, DELETE, etc.)
- `documentGroupTypes`: Define how documents are grouped
- `entityAccessControl`: Configure access control per entity
- `userGroups`: Define default user groups

**Example:**
```json
{
  "enabled": true,
  "entityAccessControl": [
    {
      "entityName": "User",
      "tableName": "users",
      "enableAccessControl": true,
      "checkOnCreate": true,
      "checkOnRead": true,
      "checkOnUpdate": true,
      "checkOnDelete": true
    }
  ],
  "userGroups": {
    "defaultGroups": [
      {
        "groupName": "Super Administrators",
        "isSuperGroup": true,
        "autoAssignToNewUsers": false
      },
      {
        "groupName": "Standard Users",
        "isDefaultGroup": true,
        "autoAssignToNewUsers": true
      }
    ]
  }
}
```

### 11. custom_queries_layer.json

Controls authorization query templates.

**Key Settings:**
- `queries`: Define custom query templates
- `queryFormat`: Query structure documentation

**Example:**
```json
{
  "queries": [
    {
      "queryName": "ActiveUsers",
      "description": "All active user accounts",
      "table": "users",
      "conditions": [
        {
          "field": "status",
          "operator": "EQUALS",
          "value": "active"
        }
      ],
      "logic": "AND"
    }
  ]
}
```

---

## Common Customization Scenarios

### Scenario 1: Change Validation Messages

**Goal**: Use friendly, user-facing validation messages

**File**: `dto_layer.json`

**Change**:
```json
{
  "fieldName": "email",
  "validation": {
    "requiredMessage": "We need your email to send you updates",
    "emailMessage": "Hmm, that doesn't look like a valid email"
  }
}
```

### Scenario 2: Disable Dangerous Endpoints

**Goal**: Prevent users from deleting records via API

**File**: `controller_layer.json`

**Change**:
```json
{
  "endpoints": {
    "delete": {
      "enabled": false
    }
  }
}
```

### Scenario 3: Add Custom Repository Methods

**Goal**: Add a method to find users by email

**File**: `repository_layer.json`

**Change**:
```json
{
  "hasCustomQueries": true,
  "customQueries": [
    {
      "methodName": "findByEmail",
      "query": "SELECT * FROM users WHERE email = :email AND deleted_at IS NULL",
      "returnType": "User",
      "parameters": ["email"]
    }
  ]
}
```

### Scenario 4: Configure JWT Expiration

**Goal**: Change JWT token expiration to 1 hour

**File**: `security_layer.json`

**Change**:
```json
{
  "jwt": {
    "expiration": 3600000  // 1 hour in milliseconds
  }
}
```

### Scenario 5: Enable Caching

**Goal**: Enable Redis caching for frequently accessed entities

**File**: `config_layer.json`

**Change**:
```json
{
  "features": {
    "caching": {
      "enabled": true,
      "type": "redis",
      "redis": {
        "host": "localhost",
        "port": 6379
      }
    }
  }
}
```

Then in `repository_layer.json`:
```json
{
  "enableCaching": true,
  "cacheNames": ["users", "products"]
}
```

---

## Workflow

### Step 1: Generate Layer Definitions
```bash
cd emotisense-ai/swfaw_v2
python phase1_generate_definition.py --input ../mysql_database_design/schema.sql --output ../generated_application/my_app
```

### Step 2: Review Generated Definitions
```bash
cd ../generated_application/my_app/application_definitions
ls -la
```

You'll see 15 JSON files with intelligent defaults.

### Step 3: Customize (Optional)
Edit any of the 11 layer definition files to customize code generation.

### Step 4: Generate Code
```bash
cd ../../../swfaw_v2
python phase2_generate_code.py --output ../generated_application/my_app
```

Phase 2 will use your customized configurations to generate code.

### Step 5: Regenerate Anytime
If you update templates or want to regenerate:
```bash
python phase2_generate_code.py --output ../generated_application/my_app
```

Your customizations in the layer definition files are preserved!

---

## Tips and Best Practices

### 1. Start with Defaults
Don't customize everything at once. Start with the generated defaults and only modify what you need.

### 2. Version Control Layer Definitions
Commit the `application_definitions/` folder to git. This allows:
- Team collaboration on configurations
- Review changes before code generation
- Rollback to previous configurations

### 3. Document Your Changes
Add comments in a separate `CUSTOMIZATIONS.md` file explaining why you made specific changes.

### 4. Test After Customization
After modifying layer definitions, regenerate and test the application to ensure your changes work as expected.

### 5. Use Consistent Naming
When adding custom queries or methods, follow the existing naming conventions in the generated code.

### 6. Backup Before Major Changes
Before making significant changes to layer definitions, backup the `application_definitions/` folder.

---

## Troubleshooting

### Issue: Phase 2 Fails After Customization

**Solution**: Check that your JSON is valid. Use a JSON validator or IDE with JSON support.

### Issue: Custom Validation Not Working

**Solution**: Ensure the validation rules in `dto_layer.json` match the supported validation types (required, email, min, max, pattern, etc.).

### Issue: Custom Query Not Generated

**Solution**: Verify that `hasCustomQueries` is set to `true` in `repository_layer.json` and the query syntax is correct.

### Issue: Endpoint Still Generated After Disabling

**Solution**: Make sure you set `"enabled": false` (boolean, not string) in `controller_layer.json`.

---

## Advanced Topics

### Custom Validation Rules

You can add custom validation annotations by modifying the DTO generator template and adding validation rules in `dto_layer.json`.

### Multiple Environments

Create different layer definition sets for different environments (dev, staging, prod) and switch between them.

### Automated Customization

Write scripts to programmatically modify layer definitions based on business rules or conventions.

---

## Migration from v2.2

If you have existing v2.2 applications:

1. Run Phase 1 again with your SQL schema
2. This generates the new layer definition files
3. Your existing application continues to work
4. Gradually adopt layer definitions for new features

---

## Summary

Layer definitions give you:
- ✅ Complete control over code generation
- ✅ Intelligent defaults from SQL schema
- ✅ Customizable validation messages
- ✅ Configurable endpoints and features
- ✅ Version control for application structure
- ✅ Team collaboration on configurations
- ✅ Fast regeneration without re-parsing SQL

Start using layer definitions today to take full control of your generated applications!
