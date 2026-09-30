# Spring WebFlux Application Writer v2 (swfaw_v2)

A Python code generator that creates complete Spring WebFlux applications from SQL database schemas or JSON definitions.

## Features

- Generates complete Spring WebFlux applications (reactive)
- **Custom Query & Filter Layers** (NEW in v2.4) - Define R2DBC queries with joins, aggregations, and filters
- Document-based authorization system with 8 operations
- JWT authentication + OAuth2 support (Google, GitHub, Microsoft)
- Admin UI for managing users, groups, and permissions
- Audit logging for all access attempts
- R2DBC for reactive database access
- REST APIs with Swagger documentation
- 100+ tables supported

## Quick Start

### Two-Phase Workflow (Recommended)

The application writer now works in two phases:

**Phase 1:** Generate application definition in output folder (SQL/JSON → output_dir/application_definitions/)
**Phase 2:** Generate application code from definition in same folder

**New in v2.2:** Application definitions are now split into multiple files by layer for better organization:
- `project_metadata.json` - Project and database configuration
- `entities.json` - All table/entity definitions
- `relationships.json` - All relationships extracted separately
- `manifest.json` - Index file that references all parts

```bash
cd emotisense-ai/swfaw_v2

# Option A: Run both phases at once (unified workflow)
# Automatic timestamp: ../generated_application/<db_name>_<timestamp>
python generate_app.py --input ../mysql_database_design/your_schema.sql

# Or specify custom output directory
python generate_app.py --input ../mysql_database_design/your_schema.sql --output ../generated_application/my_app

# Option B: Run phases separately
# Phase 1: Generate definition in output folder (automatic timestamp)
# Splits into multiple files by layer
python phase1_generate_definition.py --input ../mysql_database_design/your_schema.sql

# Or specify custom output directory
python phase1_generate_definition.py --input ../mysql_database_design/your_schema.sql --output ../generated_application/my_app

# Phase 2: Generate code (reads application_definition.json from output folder)
python phase2_generate_code.py --output ../generated_application/ems_recruitment_portal_20260310_191236

# Setup database and run
mysql -u root -p -e "CREATE DATABASE your_database_name;"
mysql -u root -p your_database_name < ../mysql_database_design/your_schema.sql
mysql -u root -p your_database_name < ../generated_application/ems_recruitment_portal_20260310_191236/auth-schema.sql
mysql -u root -p your_database_name < ../generated_application/ems_recruitment_portal_20260310_191236/activity-tracking-schema.sql

cd ../generated_application/ems_recruitment_portal_20260310_191236
mvn clean install
mvn spring-boot:run

# Complete setup at http://localhost:8081/setup
```

### Legacy Single-Phase Workflow

```bash
cd emotisense-ai/swfaw_v2

# Convert SQL to JSON (if starting from SQL)
python convert_sql.py ../mysql_database_design/your_schema.sql

# Generate application (single phase)
python main.py --input ../mysql_database_design/application_definition.json --output ../generated_application/my_app
```

## Two-Phase Architecture

### Why Two Phases?

The two-phase architecture separates concerns:

**Phase 1 Benefits:**
- Review and modify application definition before code generation
- Share definitions across teams
- Version control for application structure
- Validate schema before generating thousands of files
- Support multiple input formats (SQL, JSON, future: GraphQL, OpenAPI)

**Phase 2 Benefits:**
- Fast regeneration from definition
- Consistent code generation
- Easy to update templates without re-parsing SQL
- Support for incremental generation (future)

### Phase Scripts

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `phase1_generate_definition.py` | Generate definition | SQL or JSON + output dir | output_dir/application_definitions/ (split files) |
| `phase2_generate_code.py` | Generate code | output dir (reads definition from it) | Spring WebFlux app in same dir |
| `generate_app.py` | Run both phases | SQL or JSON + output dir | Spring WebFlux app with definition |
| `main.py` (legacy) | Single-phase mode | JSON only | Spring WebFlux app |
| `convert_sql.py` (legacy) | SQL to JSON | SQL | application_definition.json |

## File Structure

```
swfaw_v2/                        # Generator code only (no app-specific files)
├── models/                      # Data models
├── transformers/                # DB → Properties converters
├── templates/                   # Jinja2 code templates
├── generators/                  # Template → Code generators
├── utils/                       # Helper functions
├── parsers/                     # SQL parser
├── phase1_generate_definition.py  # Phase 1: Generate definition
├── phase2_generate_code.py        # Phase 2: Generate code
├── generate_app.py                # Unified workflow (both phases)
├── main.py                        # Legacy single-phase mode
├── convert_sql.py                 # Legacy SQL converter
└── requirements.txt

mysql_database_design/           # SQL schemas and definitions
├── your_schema.sql
└── application_definition.json  # Generated by Phase 1

generated_application/           # Generated applications
└── my_app/
    ├── application_definitions/     # Split definition files
    │   ├── manifest.json           # Index file
    │   ├── project_metadata.json   # Project & database config
    │   ├── entities.json           # All table definitions
    │   └── relationships.json      # All relationships
    ├── auth-schema.sql
    ├── activity-tracking-schema.sql
    ├── test-data.json
    ├── pom.xml
    └── src/
```

## SQL to JSON Conversion

The `convert_sql.py` script converts MySQL SQL schemas to JSON format:

```bash
# Default: creates application_definition.json in same directory as SQL file
python convert_sql.py ../mysql_database_design/your_schema.sql

# Custom output location
python convert_sql.py ../mysql_database_design/your_schema.sql --output ../generated_application/my_app/application_definition.json
```

**What it extracts:**
- Database name
- Table names
- Column definitions (name, type, nullable, unique)
- Primary keys
- Foreign keys (basic detection)

**Limitations:**
- Skips `created_by_id` and `updated_by_id` columns
- Basic foreign key detection
- MySQL-specific syntax

## Generated Application

### What Gets Generated

**Per Table (100 tables = 600 files):**
- Entity class (JPA + R2DBC)
- Input DTO
- Output DTO
- Filter DTO
- Repository interface
- Service class (with authorization)
- REST Controller

**Authentication & Authorization (~80 files):**
- 11 auth entities (SystemConfig, AuthUser, UserGroup, etc.)
- 11 auth repositories
- 2 OAuth2 entities + repositories
- AuthService, AuthorizationService, AuditLoggingService
- AdminService + AdminController
- OAuth2Service + OAuth2Controller
- 8 Thymeleaf HTML pages (admin UI)
- JWT components
- Security configuration

**Configuration Files:**
- pom.xml (Maven)
- application.yml
- auth-schema.sql
- README.md
- test-data.json

**Total:** ~850+ files

### Running Generated Application

```bash
cd ../generated_application

# 1. Create database and run auth schema
mysql -u root -p ems_recruitment_portal < auth-schema.sql

# 2. Build application
mvn clean install

# 3. Run application
mvn spring-boot:run

# 4. Complete setup
# Open: http://localhost:8080/setup
# Create super user account

# 5. Access application
# API: http://localhost:8080
# Swagger: http://localhost:8080/swagger-ui.html
# Admin: http://localhost:8080/admin
```

## Authorization System

### 8 Access Operations

1. READ - View records
2. CREATE - Create new records
3. UPDATE - Modify existing records
4. DELETE - Remove records
5. GRANT_ACCESS - Give access to others
6. EXPORT - Export data
7. SHARE - Share with external users
8. AUDIT - View audit logs

### 6 Document Group Types

1. SINGLE_RECORD - One specific record
2. MULTIPLE_RECORDS - Multiple specific records
3. ENTIRE_TABLE - All records in a table
4. MULTIPLE_TABLES - All records in multiple tables
5. CUSTOM_QUERY - Records matching query (requires record IDs)
6. CUSTOM_QUERY_ALL - All records matching query (ignores record IDs)

### Features

- Group-based authorization (no roles)
- Document-based access control
- Union-based permission resolution (most permissive wins)
- Time-based permissions (valid_from, valid_until)
- Super user with justification for DELETE
- Complete audit logging

## OAuth2 Support

Pre-configured providers (disabled by default):
- Google (OpenID Connect)
- GitHub
- Microsoft/Azure AD

**Setup:**
1. Register app with OAuth2 provider
2. Get client ID and client secret
3. Update `oauth2_provider` table
4. Set `is_enabled = true`

**Features:**
- External identity linking
- Automatic user creation
- Multi-provider support per user
- JWT token generation after OAuth2 auth

## Dependencies

```bash
pip install -r requirements.txt
```

**Required:**
- pydantic
- jinja2

## Configuration

### Database Definition JSON Schema

```json
{
  "projectMetadata": {
    "name": "project-name",
    "applicationName": "Project Name",
    "groupId": "com.example",
    "artifactId": "project-name",
    "version": "1.0.0",
    "port": 8080,
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

## Customization

### Modify Templates

Edit files in `templates/` directory:
- `entity_templates.py` - Entity class structure
- `service_templates.py` - Service logic
- `controller_templates.py` - REST endpoints
- `auth_*_templates.py` - Auth/authz components

### Modify Transformers

Edit files in `transformers/` directory to change how database definitions are converted to properties.

### Modify Generators

Edit files in `generators/` directory to change how templates are populated.

## Documentation

**Main documentation:**
- `README.md` - This file (quick start and overview)

**Detailed documentation (in `docs/` folder):**
- `docs/USAGE_GUIDE.md` - Complete usage instructions
- `docs/AUTH_AUTHZ_DOCUMENTATION.md` - Authentication & authorization system (v2.1)
- `docs/LAYERS_DOCUMENTATION.md` - Layer-by-layer implementation details
- `docs/ACTIVITY_TRACKING_DOCUMENTATION.md` - Activity tracking and audit logging
- `docs/EXCEPTION_HANDLING_DOCUMENTATION.md` - Exception handling system

## Troubleshooting

### SQL Conversion Issues

**Problem:** Tables not detected  
**Solution:** Check SQL syntax, ensure CREATE TABLE statements are properly formatted

**Problem:** Primary keys not detected  
**Solution:** Ensure PRIMARY KEY is explicitly defined or column ends with `_id`

### Generation Issues

**Problem:** Import errors  
**Solution:** Clear `__pycache__` directories: `find . -type d -name __pycache__ -exec rm -rf {} +`

**Problem:** File not found  
**Solution:** Ensure paths are relative to swfaw_v2 directory

### Generated Application Issues

**Problem:** Compilation errors  
**Solution:** Check generated code, ensure all imports are correct

**Problem:** Database connection fails  
**Solution:** Update application.yml with correct database credentials

## Version History

**v2.2 (March 10, 2026)**
- Split application definition into multiple files by layer
- Better organization for large schemas
- Improved maintainability and version control

**v2.1 (March 5, 2026)**
- Added OAuth2/OpenID Connect authentication
- External identity linking
- Multi-provider support

**v2.0 (March 5, 2026)**
- Complete auth/authz redesign
- Document-based authorization
- Admin UI
- Audit logging

**v1.0 (Previous)**
- Basic code generation
- Simple authorization

## License

Internal use only.

## Support

For issues or questions, refer to:
- `docs/AUTH_AUTHZ_DOCUMENTATION.md` for auth/authz details
- `docs/USAGE_GUIDE.md` for detailed usage instructions
- `docs/LAYERS_DOCUMENTATION.md` for implementation details
- Session summaries in `../session_summaries/`
- Generated application README.md
