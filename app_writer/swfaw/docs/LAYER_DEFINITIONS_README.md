# Layer Definition Files

These JSON schema files define the structure of configuration files that will be generated in each application's `application_definitions/` folder during Phase 1.

## Purpose

After Phase 1 generates the application definitions, you can modify these files to customize code generation behavior before running Phase 2.

## Workflow

1. **Phase 1**: Generates definition files in `generated_application/<app_name>/application_definitions/`
2. **Review & Modify**: Edit the generated definition files to customize behavior
3. **Phase 2**: Reads the modified definitions and generates code accordingly

## Layer Definition Files

- `entity_definition.json` - Entity layer configuration (per entity)
- `repository_definition.json` - Repository layer configuration (per entity)
- `service_definition.json` - Service layer configuration (per entity)
- `controller_definition.json` - Controller layer configuration (per entity)
- `dto_definition.json` - DTO layer configuration (per entity)
- `security_definition.json` - Security configuration (application-wide)
- `config_definition.json` - Application configuration (application-wide)
- `exception_definition.json` - Exception handling configuration (application-wide)
- `audit_logging_definition.json` - Audit logging configuration (application-wide)
- `jwt_definition.json` - JWT authentication configuration (application-wide)
- `authorization_definition.json` - Authorization configuration (application-wide)

## Example Use Cases

- Disable soft delete for specific entities
- Add custom validation messages for DTOs
- Change JWT expiration time
- Enable/disable authorization for specific services
- Customize REST endpoint paths
- Add custom repository queries
