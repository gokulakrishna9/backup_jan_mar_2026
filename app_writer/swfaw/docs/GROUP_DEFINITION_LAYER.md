# Group Definition Layer Documentation

## Overview

**Introduced in:** v2.5  
**Date:** March 2026  
**Status:** Production Ready

The group definition layer replaces runtime group management with a code-generation-time approach. All access groups (system groups, per-table USER/ADMIN groups, and query access groups) are defined in `group_definition_layer.json` during Phase 1 and prepopulated into the database via `auth-schema.sql` during Phase 2.

No runtime API exists to create, edit, or delete groups. Admin users can only grant or revoke group membership.

---

## Motivation

Previously, groups were created at runtime through the Admin UI and REST API. This introduced complexity around:
- Inconsistent group structures across environments
- Risk of accidental group deletion breaking authorization
- No version control over group definitions
- Difficulty reproducing authorization setups

The new approach treats groups as infrastructure — defined once, versioned in the application definition, and deployed consistently.

---

## Architecture

### Phase 1: Definition Generation

`layer_definition_generator.py` → `generate_group_definition_layer()` produces `group_definition_layer.json` containing:

- **systemGroups** — Super Administrators, Administrators, Standard Users
- **tableAccessGroups** — Per-table USER (read + export) and ADMIN (full CRUD) groups
- **queryAccessGroups** — Custom query-based groups (empty by default, user-configurable)

### Phase 2: Code Generation

1. `auth_schema_generator.py` reads `group_definition_layer.json`
2. Generates idempotent `INSERT ... ON DUPLICATE KEY UPDATE` statements for:
   - `user_group` table (system groups)
   - `document_group` + `document_group_table_scope` (table access groups)
   - `document_group` + `document_group_query_scope` (query access groups)
3. Writes them into `auth-schema.sql` between the DDL and footer sections

### Fallback Behavior

If `group_definition_layer.json` is missing (e.g., older v2.2 applications), the generator falls back to a single "Super Administrators" group INSERT for backward compatibility.

---

## JSON Structure

### group_definition_layer.json

```json
{
  "layerType": "group_definition",
  "description": "Prepopulated access groups...",
  "version": "1.0",

  "groupManagement": {
    "allowRuntimeCreation": false,
    "allowRuntimeDeletion": false,
    "adminCanGrantMembership": true,
    "adminCanRevokeMembership": true,
    "adminGroupName": "Administrators"
  },

  "ownerEnrollmentDefaults": {
    "ownershipCheck": "CREATOR_RECORDS",
    "maxRecordsPerUser": null,
    "allowEnroll": false,
    "allowUnenroll": false
  },

  "systemGroups": [
    {
      "groupName": "Super Administrators",
      "description": "Full system access - bypasses all authorization checks",
      "isSuperGroup": true,
      "isDefaultGroup": false,
      "autoAssignToNewUsers": false
    },
    {
      "groupName": "Administrators",
      "description": "Can grant/revoke group membership",
      "isSuperGroup": false,
      "isDefaultGroup": false,
      "autoAssignToNewUsers": false
    },
    {
      "groupName": "Standard Users",
      "description": "Default group for new users",
      "isSuperGroup": false,
      "isDefaultGroup": true,
      "autoAssignToNewUsers": true
    }
  ],

  "tableAccessGroups": [
    {
      "groupName": "EntityName Users",
      "description": "User-level access to table_name table",
      "tableName": "table_name",
      "entityName": "EntityName",
      "groupType": "TABLE_USER",
      "accessLevel": "USER",
      "permissions": {
        "allowRead": true,
        "allowCreate": false,
        "allowUpdate": false,
        "allowDelete": false,
        "allowGrantAccess": false,
        "allowExport": true,
        "allowShare": false,
        "allowAudit": false
      }
    },
    {
      "groupName": "EntityName Admins",
      "description": "Admin-level access to table_name table",
      "tableName": "table_name",
      "entityName": "EntityName",
      "groupType": "TABLE_ADMIN",
      "accessLevel": "ADMIN",
      "permissions": {
        "allowRead": true,
        "allowCreate": true,
        "allowUpdate": true,
        "allowDelete": true,
        "allowGrantAccess": true,
        "allowExport": true,
        "allowShare": true,
        "allowAudit": true
      }
    }
  ],

  "queryAccessGroups": []
}
```

---

## Table Access Groups

For each table in the SQL schema, two groups are generated:

| Group | Access Level | Permissions |
|-------|-------------|-------------|
| `{Entity} Users` | USER | Read, Export |
| `{Entity} Admins` | ADMIN | Full CRUD + Grant + Export + Share + Audit |

These map to `document_group` + `document_group_table_scope` rows in the database.

---

## Query Access Groups

Query access groups are empty by default. Users can add them to `group_definition_layer.json` before running Phase 2. Example:

```json
{
  "groupName": "Active Projects View",
  "description": "Shared view of active projects",
  "rootTable": "projects",
  "groupType": "QUERY_SPECIFIC",
  "scopeMode": "SPECIFIC_RECORDS",
  "ownerRecordEnrollment": {
    "allowEnroll": true,
    "allowUnenroll": true,
    "ownershipCheck": "CREATOR_RECORDS",
    "maxRecordsPerUser": null
  },
  "queryDefinition": {
    "table": "projects",
    "conditions": [
      { "field": "status", "operator": "EQUALS", "value": "active" }
    ],
    "logic": "AND"
  }
}
```

### Owner Record Enrollment

When `ownerRecordEnrollment.allowEnroll` is `true`, standard users can add their own records to a query group. Ownership is verified via:

1. **CREATOR_RECORDS** — checks the `document_group_definition` for a CREATOR_RECORDS document group type
2. **created_by column fallback** — checks if the record's `created_by` column matches the user ID

This enables self-service record sharing without admin intervention.

---

## Generated SQL

The auth schema generator produces SQL like:

```sql
-- Prepopulated Groups (from group_definition_layer.json)

-- System groups
INSERT INTO user_group (group_name, description, is_super_group)
VALUES ('Super Administrators', 'Full system access...', TRUE)
ON DUPLICATE KEY UPDATE group_name=group_name;

-- Table access groups
INSERT INTO document_group (group_name, description, group_type_id)
SELECT 'Project Users', 'User-level access...', type_id
FROM document_group_type WHERE type_name = 'TABLE_USER'
ON DUPLICATE KEY UPDATE group_name=group_name;

INSERT INTO document_group_table_scope
    (document_group_id, table_name, access_level, ...)
SELECT dg.document_group_id, 'projects', 'USER', ...
FROM document_group dg WHERE dg.group_name = 'Project Users'
ON DUPLICATE KEY UPDATE table_name=table_name;
```

All INSERTs are idempotent (`ON DUPLICATE KEY UPDATE`) so `auth-schema.sql` can be re-run safely.

---

## Files Changed

### New / Rewritten

| File | Change |
|------|--------|
| `utils/layer_definition_generator.py` | Added `generate_group_definition_layer()`, registered in `generate_all_layer_definitions()` |
| `generators/auth_schema_generator.py` | Full rewrite — accepts `group_definition` dict, generates dynamic INSERTs |
| `templates/auth_schema_templates.py` | Split into `AUTH_SCHEMA_DDL` + `AUTH_SCHEMA_FOOTER`, removed hardcoded Super Admin INSERT |

### Modified

| File | Change |
|------|--------|
| `utils/definition_splitter.py` | Added `group_definition_layer` to manifest |
| `main.py` | Loads `group_definition_layer.json` and passes to `AuthSchemaGenerator.generate()` |
| `managers/layer_manager.py` | Added `"group_definition": "group_definition_layer.json"` alias |
| `templates/admin_ui_templates.py` | Removed `createGroup()`, `updateGroup()`, `deleteGroup()`, `createDocumentGroup()`, `addDocumentGroupDefinition()` from AdminService. Removed corresponding POST endpoints from AdminController. |
| `templates/admin_html_templates.py` | Groups page: read-only with "System-Managed" badge. Group form: replaced with read-only notice. Document groups page: removed "Create" button. Document group form: replaced with read-only notice. Document group detail: removed "Add Definition" form, added "System-Managed" badge. |

### Removed from authorization_layer.json

The `userGroups` block was removed from `generate_authorization_layer_definition()`. Group definitions now live exclusively in `group_definition_layer.json`.

---

## Admin UI Behavior

After these changes, the admin UI is read-only for group and document group structures:

| Page | Before | After |
|------|--------|-------|
| Groups list | Create/Edit/Delete buttons | Read-only table with "System-Managed" badge |
| Group form | Full edit form | Notice page pointing to `group_definition_layer.json` |
| Document groups list | "Create New" button | Read-only table with "System-Managed" badge |
| Document group form | Full edit form | Notice page pointing to `group_definition_layer.json` |
| Document group detail | "Add Definition" form | Read-only definitions table with info note |

Admin users can still:
- View all groups and document groups
- Add/remove users from groups (membership management)
- Grant/revoke permissions on document groups

---

## LayerManager Access

The group definition layer is accessible via the LayerManager:

```python
from managers import DefinitionManager, LayerManager

def_manager = DefinitionManager("../generated_application/my_app")
def_manager.load()

layer_manager = LayerManager(def_manager)

# Read system groups
groups = layer_manager.get("group_definition", "systemGroups")

# Update a permission
layer_manager.set("group_definition", "tableAccessGroups[0].permissions.allowCreate", True)

# Add a query access group
layer_manager.append("group_definition", "queryAccessGroups", {
    "groupName": "Active Projects View",
    "rootTable": "projects",
    "groupType": "QUERY_SPECIFIC",
    "scopeMode": "SPECIFIC_RECORDS"
})

def_manager.save()
```

---

## Customization Workflow

1. Run Phase 1 to generate `group_definition_layer.json`
2. Edit the JSON to customize:
   - Add/remove table access groups
   - Adjust permissions per group
   - Add query access groups with owner enrollment
   - Modify system group names/descriptions
3. Run Phase 2 to generate code with your customizations
4. The generated `auth-schema.sql` will contain matching INSERT statements
