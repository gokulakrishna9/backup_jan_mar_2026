# Tier 1: Foundation Tables

These two tables form the root of the entire definition store.
Every other table references `swfaw_app_definition.id`.

---

## Table 1: `swfaw_app_definition`

**Replaces:** `manifest.json` + `project_metadata.json`

This is the root row for an entire application definition. One row = one generated app.

```sql
CREATE TABLE swfaw_app_definition (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    -- Manifest info (from manifest.json)
    version             VARCHAR(10)     NOT NULL DEFAULT '2.5',
    format              VARCHAR(20)     NOT NULL DEFAULT 'database',
    description         TEXT,

    -- Project metadata (from project_metadata.json → projectMetadata)
    project_name        VARCHAR(255)    NOT NULL,
    application_name    VARCHAR(255)    NOT NULL,
    group_id            VARCHAR(255)    NOT NULL DEFAULT 'com.example',
    artifact_id         VARCHAR(255)    NOT NULL,
    project_version     VARCHAR(50)     NOT NULL DEFAULT '1.0.0',
    port                INT             NOT NULL DEFAULT 8081,
    sql_file_name       VARCHAR(255),

    -- Database config (from project_metadata.json → projectMetadata.database)
    db_type             VARCHAR(50)     NOT NULL DEFAULT 'mysql',
    db_host             VARCHAR(255)    NOT NULL DEFAULT 'localhost',
    db_port             INT             NOT NULL DEFAULT 3306,
    db_name             VARCHAR(255)    NOT NULL,
    db_url              VARCHAR(500),
    db_username         VARCHAR(255)    NOT NULL DEFAULT 'root',
    db_password         VARCHAR(255)    NOT NULL DEFAULT 'password',

    -- Statistics (denormalized from manifest.json → statistics)
    total_entities      INT             NOT NULL DEFAULT 0,
    total_relationships INT             NOT NULL DEFAULT 0,
    total_columns       INT             NOT NULL DEFAULT 0,

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by          VARCHAR(255),
    is_active           TINYINT(1)      NOT NULL DEFAULT 1,

    UNIQUE KEY uk_artifact (group_id, artifact_id, project_version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Field Mapping

| JSON Source | DB Column | Notes |
|-------------|-----------|-------|
| `manifest.version` | `version` | Definition format version |
| `manifest.format` | `format` | Was "split", now "database" |
| `manifest.statistics.*` | `total_entities`, etc. | Denormalized for quick access |
| `projectMetadata.name` | `project_name` | e.g. "ems-recruitment-portal" |
| `projectMetadata.applicationName` | `application_name` | Display name |
| `projectMetadata.groupId` | `group_id` | Maven group |
| `projectMetadata.artifactId` | `artifact_id` | Maven artifact |
| `projectMetadata.version` | `project_version` | App version |
| `projectMetadata.port` | `port` | Server port |
| `projectMetadata.sqlFileName` | `sql_file_name` | Original SQL file |
| `projectMetadata.database.*` | `db_*` columns | Flattened 1:1 |

### Design Decisions

- **Database config flattened** into the same table (always 1:1 with the definition).
  If multi-profile support is needed later (dev/test/prod), a separate
  `swfaw_db_profile` table can be added without breaking this schema.
- **Statistics are denormalized** — they could be computed via COUNT queries,
  but storing them matches the current manifest behavior and avoids expensive joins.
- **Unique key on (group_id, artifact_id, project_version)** prevents duplicate
  definitions for the same project version.

---

## Table 2: `swfaw_entity`

**Replaces:** `entities.json`

Each row represents one database table (entity) in the application.
Columns are stored as a JSON array since they're always loaded as a batch
and their structure is well-defined but variable in count.

```sql
CREATE TABLE swfaw_entity (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- From entities.json → entities[].name
    table_name          VARCHAR(255)    NOT NULL,

    -- Columns stored as JSON array
    -- Each element: {name, type, primaryKey, nullable, foreignKey, unique, defaultValue}
    columns_json        JSON            NOT NULL,

    -- Derived/cached counts
    column_count        INT             NOT NULL DEFAULT 0,
    primary_key_column  VARCHAR(255),

    -- Housekeeping
    sort_order          INT             NOT NULL DEFAULT 0,
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_entity_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_entity_table (app_definition_id, table_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### columns_json Structure

```json
[
  {
    "name": "user_id",
    "type": "BIGINT UNSIGNED",
    "primaryKey": true,
    "nullable": false,
    "foreignKey": null,
    "unique": false,
    "defaultValue": null
  },
  {
    "name": "first_name",
    "type": "VARCHAR(100)",
    "primaryKey": false,
    "nullable": false,
    "foreignKey": null,
    "unique": false,
    "defaultValue": null
  }
]
```

### Design Decisions

- **Columns as JSON rather than a separate table.** Rationale:
  - Columns are always loaded/saved as a complete set per entity
  - The column structure is uniform (same 7 fields every time)
  - Avoids a table with potentially 700+ rows for a 100-entity app
  - MySQL JSON functions allow querying into the array if needed:
    `JSON_EXTRACT(columns_json, '$[0].name')`
  - The FieldManager already operates on the full column list in memory
- **`primary_key_column`** is denormalized for quick access — many layers need
  to know the PK column without parsing JSON.
- **`sort_order`** preserves the original table ordering from the SQL schema.

### Alternative Considered: Fully Normalized Columns

If you later need to query individual columns across entities (e.g., "find all
VARCHAR(255) columns"), a normalized `swfaw_entity_column` table would be better:

```sql
-- ALTERNATIVE: Only use if cross-entity column queries are needed
CREATE TABLE swfaw_entity_column (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    entity_id           BIGINT UNSIGNED NOT NULL,
    column_name         VARCHAR(255)    NOT NULL,
    column_type         VARCHAR(255)    NOT NULL,
    is_primary_key      TINYINT(1)      NOT NULL DEFAULT 0,
    is_nullable         TINYINT(1)      NOT NULL DEFAULT 1,
    foreign_key_json    JSON,
    is_unique           TINYINT(1)      NOT NULL DEFAULT 0,
    default_value       VARCHAR(500),
    sort_order          INT             NOT NULL DEFAULT 0,
    CONSTRAINT fk_col_entity
        FOREIGN KEY (entity_id) REFERENCES swfaw_entity(id) ON DELETE CASCADE,
    UNIQUE KEY uk_entity_col (entity_id, column_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

This is provided as a reference. The primary design uses JSON columns.
