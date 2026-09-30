# Two-Phase Architecture Documentation

## Overview

swfaw_v2 uses a two-phase architecture that separates application definition generation from code generation.

**Version 2.3** introduces layer definitions - customizable JSON configuration files that give you complete control over code generation.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         PHASE 1                              │
│              Generate Application Definition                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Input: SQL or JSON                                          │
│     ↓                                                        │
│  Parse/Load                                                  │
│     ↓                                                        │
│  Validate                                                    │
│     ↓                                                        │
│  Transform to Layer Definitions (v2.3)                       │
│     ↓                                                        │
│  Output: 15 definition files in application_definitions/     │
│    - 4 core files (manifest, metadata, entities, rels)      │
│    - 5 per-entity layers (entity, repo, service, ctrl, dto) │
│    - 6 application-wide layers (security, config, etc.)     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                            ↓
                    (User can customize)
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                         PHASE 2                              │
│                Generate Application Code                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Input: Layer definition files (v2.3)                        │
│     ↓                                                        │
│  Load Layer Definitions                                      │
│     ↓                                                        │
│  Generate Code from Definitions                              │
│     ↓                                                        │
│  Output: Spring WebFlux Application (780+ files)             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Phase 1: Generate Application Definition

### Purpose
Convert SQL schemas or JSON definitions into customizable layer definition files.

### Input Formats
- **SQL**: MySQL CREATE TABLE statements
- **JSON**: Existing application definition

### Output (v2.3)
15 definition files in `<output_dir>/application_definitions/`:

**Core Definition Files (4):**
1. `manifest.json` - Version, file index, statistics
2. `project_metadata.json` - Project and database configuration
3. `entities.json` - All table definitions
4. `relationships.json` - Entity relationships

**Per-Entity Layer Definitions (5):**
5. `entity_layer.json` - Entity configurations (audit fields, soft delete, relationships)
6. `repository_layer.json` - Repository configurations (custom queries, caching)
7. `service_layer.json` - Service configurations (authorization, transactions)
8. `controller_layer.json` - Controller configurations (endpoints, CORS, rate limiting)
9. `dto_layer.json` - DTO configurations with validation rules

**Application-Wide Layer Definitions (6):**
10. `security_layer.json` - JWT, OAuth2, CORS, password policies
11. `config_layer.json` - Database, server, logging, features
12. `exception_layer.json` - Custom exceptions, error handling
13. `audit_logging_layer.json` - Audit events, storage, alerting
14. `authorization_layer.json` - Entity access controls
15. `custom_queries_layer.json` - Authorization query templates

### Script
```bash
python phase1_generate_definition.py --input schema.sql --output ../generated_application/my_app
```

### What It Does
1. Parses SQL or loads JSON
2. Extracts database schema (tables, columns, relationships)
3. Validates structure
4. Generates intelligent defaults for all layers
5. Creates 15 layer definition files
6. Saves all files to `<output_dir>/application_definitions/`
7. Prints summary

### Benefits
- **Complete Control**: Customize every aspect of code generation
- **Intelligent Defaults**: All settings generated with smart defaults from SQL
- **Review Before Generate**: Modify definitions before creating 780+ files
- **Version Control**: Layer definitions can be committed to git
- **Team Collaboration**: Share and review configurations
- **Incremental Adoption**: Can adopt layer definitions gradually

## Phase 2: Generate Application Code

### Purpose
Generate complete Spring WebFlux application from layer definition files.

### Input
- Output directory containing `application_definitions/` folder with layer definition files

### Output
- Complete Spring WebFlux application (780+ files) in the same directory

### Script
```bash
python phase2_generate_code.py --output ../generated_application/my_app
```

### What It Does
1. Reads layer definition files from `<output_dir>/application_definitions/`
2. Detects version (v2.3 with layer definitions or v2.2 legacy)
3. Loads all 11 layer definition files (if v2.3)
4. Generates code from customized configurations
5. Writes all files to the output directory

### Generated Components
- 100+ Entity classes (JPA with R2DBC)
- 300+ DTOs (Input, Output, Filter with custom validation)
- 100+ Repositories (R2DBC with custom queries)
- 100+ Services (with authorization and transactions)
- 100+ REST Controllers (with configurable endpoints)
- Authentication layer (JWT, OAuth2)
- Authorization layer (document-based access control)
- Security configuration (from security_layer.json)
- Application configuration (from config_layer.json)
- Exception handling (from exception_layer.json)
- Audit logging (from audit_logging_layer.json)
- Setup UI and admin pages
- Maven POM
- SQL schemas (auth-schema.sql, activity-tracking-schema.sql)
- Test data (test-data.json)

### Benefits
- **Customizable**: Uses your modified layer definitions
- **Fast Regeneration**: Regenerate from definitions without re-parsing SQL
- **Consistent**: Same definitions = same code
- **Backward Compatible**: Works with v2.2 applications (falls back to transformers)
- **Template Updates**: Easy to update templates and regenerate
- Can modify definition and regenerate

## Unified Workflow

### Script
```bash
python generate_app.py --input schema.sql --output ../generated_application/my_app
```

### Options
```bash
# Run both phases
python generate_app.py --input schema.sql --output ../generated_application/my_app

# Run Phase 1 only
python generate_app.py --input schema.sql --phase 1

# Run Phase 2 only
python generate_app.py --input app_def.json --phase 2 --output ../generated_application/my_app

# Custom definition location
python generate_app.py --input schema.sql --output ../generated_application/my_app --definition custom_def.json
```

## Legacy Mode

### Single-Phase Mode (Deprecated)
```bash
# Old way: convert SQL to JSON manually
python convert_sql.py schema.sql

# Old way: generate application
python main.py --input application_definition.json --output ../generated_application/my_app
```

The `main.py` script still works but shows a deprecation notice.

## Migration Guide

### From Legacy to Two-Phase

**Old Workflow:**
```bash
python convert_sql.py schema.sql
python main.py --input application_definition.json --output ../generated_application/my_app
```

**New Workflow (Option A - Unified):**
```bash
python generate_app.py --input schema.sql --output ../generated_application/my_app
```

**New Workflow (Option B - Separate Phases):**
```bash
python phase1_generate_definition.py --input schema.sql --output ../generated_application/my_app
python phase2_generate_code.py --output ../generated_application/my_app
```

## Use Cases

### Use Case 1: Quick Generation
**Scenario:** Generate app from SQL in one command

**Solution:**
```bash
python generate_app.py --input schema.sql --output ../generated_application/my_app
```

### Use Case 2: Review Before Generation
**Scenario:** Review and modify definition before generating code

**Solution:**
```bash
# Phase 1: Generate definition in output folder
python phase1_generate_definition.py --input schema.sql --output ../generated_application/my_app

# Review and edit ../generated_application/my_app/application_definition.json

# Phase 2: Generate code from the definition
python phase2_generate_code.py --output ../generated_application/my_app
```

### Use Case 3: Regenerate After Template Changes
**Scenario:** Updated templates, need to regenerate code

**Solution:**
```bash
# No need to re-parse SQL, just regenerate from existing definition
python phase2_generate_code.py --output ../generated_application/my_app
```

### Use Case 4: Multiple Environments
**Scenario:** Generate apps for dev, staging, prod with different configs

**Solution:**
```bash
# Generate base definition in first environment
python phase1_generate_definition.py --input schema.sql --output ../generated_application/my_app_dev

# Copy definition to other environments
cp ../generated_application/my_app_dev/application_definition.json ../generated_application/my_app_staging/
cp ../generated_application/my_app_dev/application_definition.json ../generated_application/my_app_prod/

# Edit each definition (ports, database names, etc.)
# Edit ../generated_application/my_app_staging/application_definition.json
# Edit ../generated_application/my_app_prod/application_definition.json

# Generate apps for each environment
python phase2_generate_code.py --output ../generated_application/my_app_dev
python phase2_generate_code.py --output ../generated_application/my_app_staging
python phase2_generate_code.py --output ../generated_application/my_app_prod
```

## Application Definition Format

### Structure
```json
{
  "projectMetadata": {
    "name": "project-name",
    "applicationName": "Project Name",
    "groupId": "com.example",
    "artifactId": "project-name",
    "version": "1.0.0",
    "port": 8081,
    "sqlFileName": "schema.sql",
    "dateCreated": "2026-03-10",
    "database": {
      "type": "mysql",
      "host": "localhost",
      "port": 3306,
      "name": "database_name",
      "username": "root",
      "password": "password"
    }
  },
  "tables": [
    {
      "name": "table_name",
      "columns": [
        {
          "name": "column_name",
          "type": "VARCHAR(255)",
          "primaryKey": true,
          "nullable": false,
          "unique": false
        }
      ],
      "relationships": []
    }
  ]
}
```

### Modifiable Fields

**Project Metadata:**
- `name`: Project identifier (kebab-case)
- `applicationName`: Display name
- `groupId`: Maven group ID
- `artifactId`: Maven artifact ID
- `version`: Application version
- `port`: Server port

**Database:**
- `type`: Database type (mysql, postgresql, etc.)
- `host`: Database host
- `port`: Database port
- `name`: Database name
- `username`: Database username
- `password`: Database password

**Tables:**
- Add/remove tables
- Modify column types
- Add/remove columns
- Define relationships

## Future Enhancements

### Planned Features
1. **Incremental Generation**: Generate only changed files
2. **Multiple Input Formats**: GraphQL schemas, OpenAPI specs
3. **Custom Templates**: User-defined templates
4. **Validation**: Schema validation before generation
5. **Diff Tool**: Compare definitions
6. **Merge Tool**: Merge multiple definitions

### Roadmap
- **v2.2**: Incremental generation
- **v2.3**: GraphQL schema support
- **v2.4**: Custom templates
- **v3.0**: Full IDE integration

## Troubleshooting

### Phase 1 Issues

**Problem:** SQL parsing fails  
**Solution:** Check SQL syntax, ensure CREATE TABLE statements are valid

**Problem:** Missing tables  
**Solution:** Verify SQL file contains CREATE TABLE statements

### Phase 2 Issues

**Problem:** Import errors  
**Solution:** Ensure application_definition.json is valid

**Problem:** Missing fields  
**Solution:** Check definition has all required fields

### General Issues

**Problem:** Files not generated  
**Solution:** Check output directory permissions

**Problem:** Compilation errors in generated code  
**Solution:** Verify definition is valid, check template versions

## Best Practices

1. **Version Control**: Commit application_definition.json
2. **Review Definitions**: Always review Phase 1 output before Phase 2
3. **Backup**: Keep backups of definitions
4. **Documentation**: Document custom modifications to definitions
5. **Testing**: Test generated applications before deployment

## Support

For issues or questions:
- Check `docs/USAGE_GUIDE.md`
- Check `docs/AUTH_AUTHZ_DOCUMENTATION.md`
- Review session summaries in `../session_summaries/`


## Customizing Layer Definitions (v2.3)

Between Phase 1 and Phase 2, you can customize any of the 11 layer definition files to control code generation.

### Example 1: Customize Validation Messages

Edit `dto_layer.json` to change validation messages:

```json
{
  "fieldName": "email",
  "validation": {
    "required": true,
    "requiredMessage": "We need your email to contact you",
    "email": true,
    "emailMessage": "That doesn't look like a valid email address"
  }
}
```

### Example 2: Disable Endpoints

Edit `controller_layer.json` to disable specific endpoints:

```json
{
  "entityName": "User",
  "endpoints": {
    "delete": {
      "enabled": false  // Disable delete endpoint
    }
  }
}
```

### Example 3: Configure Security

Edit `security_layer.json` to change JWT settings:

```json
{
  "jwt": {
    "enabled": true,
    "expiration": 3600000,  // 1 hour instead of 24
    "issuer": "my-company",
    "audience": "my-users"
  }
}
```

### Example 4: Customize Exception Messages

Edit `exception_layer.json` to add entity-specific messages:

```json
{
  "exceptionMessages": {
    "ResourceNotFoundException": {
      "User": "User account not found. Please check the ID.",
      "Product": "Product not found in our catalog."
    }
  }
}
```

### Example 5: Configure Audit Logging

Edit `audit_logging_layer.json` to track specific entities:

```json
{
  "auditEvents": {
    "dataAccess": {
      "events": [
        {
          "eventType": "DELETE",
          "entities": ["User", "Product", "Order"]  // Only audit these
        }
      ]
    }
  }
}
```

## Version Compatibility

### v2.3 (Current)
- 15 definition files in `application_definitions/` folder
- Layer definitions with customizable configurations
- Intelligent defaults generated from SQL schema
- Full control over all aspects of code generation

### v2.2 (Legacy)
- Single `application_definition.json` file
- Transformer-based generation (no customization)
- Phase 2 automatically detects and uses legacy mode
- Fully backward compatible

### Migration from v2.2 to v2.3
Simply run Phase 1 again with your SQL schema:
```bash
python phase1_generate_definition.py --input schema.sql --output ../generated_application/my_app
```

This will generate the new layer definition files. Your existing v2.2 applications continue to work.
