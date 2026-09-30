# Tier 4c: Audit, Authorization & Group Definition Tables

---

## Table 23: `swfaw_audit_config`

**Replaces:** `audit_logging_layer.json` (top-level settings + storage +
filtering + format)

```sql
CREATE TABLE swfaw_audit_config (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Master switch
    audit_enabled       TINYINT(1)      NOT NULL DEFAULT 1,

    -- Category switches (from auditEvents.*.enabled)
    auth_events_enabled     TINYINT(1)  NOT NULL DEFAULT 1,
    data_events_enabled     TINYINT(1)  NOT NULL DEFAULT 1,
    authz_events_enabled    TINYINT(1)  NOT NULL DEFAULT 1,
    system_events_enabled   TINYINT(1)  NOT NULL DEFAULT 1,

    -- Storage config (from storage)
    storage_type            VARCHAR(50) NOT NULL DEFAULT 'database',
    storage_table_name      VARCHAR(255) DEFAULT 'audit_log',
    storage_retention_days  INT         NOT NULL DEFAULT 365,
    storage_archive_after   INT         NOT NULL DEFAULT 90,
    storage_archive_location VARCHAR(500),

    -- Filtering config (from filtering)
    exclude_users_json      JSON,       -- ["system", "health-check"]
    exclude_endpoints_json  JSON,       -- ["/actuator/health", ...]
    exclude_read_operations TINYINT(1)  NOT NULL DEFAULT 1,
    sensitive_fields_json   JSON,       -- ["password", "creditCard", ...]

    -- Format config (from format)
    fmt_timestamp_format    VARCHAR(100) DEFAULT 'yyyy-MM-dd''T''HH:mm:ss.SSS''Z''',
    fmt_include_request_id  TINYINT(1)  NOT NULL DEFAULT 1,
    fmt_include_session_id  TINYINT(1)  NOT NULL DEFAULT 1,
    fmt_include_correlation_id TINYINT(1) NOT NULL DEFAULT 1,

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_auditcfg_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_auditcfg (app_definition_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## Table 24: `swfaw_audit_event`

**Replaces:** `audit_logging_layer.json → auditEvents.*[].events[]`

Each row is one audit event definition. The `category` column indicates
which section it came from (authentication, dataAccess, authorization, systemEvents).

```sql
CREATE TABLE swfaw_audit_event (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    audit_config_id     BIGINT UNSIGNED NOT NULL,

    -- Event identity
    category            VARCHAR(50)     NOT NULL,  -- authentication, dataAccess, authorization, systemEvents
    event_type          VARCHAR(100)    NOT NULL,   -- LOGIN_SUCCESS, CREATE, ACCESS_DENIED, etc.
    log_level           VARCHAR(20)     NOT NULL DEFAULT 'INFO',
    message_template    TEXT            NOT NULL,   -- e.g. "User {username} logged in from IP {ipAddress}"

    -- Optional flags (vary by category)
    include_user_agent      TINYINT(1)  DEFAULT 0,
    include_location        TINYINT(1)  DEFAULT 0,
    include_entity_data     TINYINT(1)  DEFAULT 0,
    include_changes         TINYINT(1)  DEFAULT 0,
    include_reason          TINYINT(1)  DEFAULT 0,

    -- For dataAccess events: which entities to audit
    -- Empty array means "all entities" or "none" depending on context
    entities_json           JSON,       -- ["User", "Course", ...]

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audevt_cfg
        FOREIGN KEY (audit_config_id) REFERENCES swfaw_audit_config(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_audevt (audit_config_id, category, event_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## Table 25: `swfaw_audit_alert`

**Replaces:** `audit_logging_layer.json → alerting.alerts[]`

```sql
CREATE TABLE swfaw_audit_alert (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    audit_config_id     BIGINT UNSIGNED NOT NULL,

    -- Alert master switch lives on audit_config (adding below)
    event_type          VARCHAR(100)    NOT NULL,
    threshold           INT             NOT NULL,
    time_window_minutes INT             NOT NULL,
    action              VARCHAR(50)     NOT NULL DEFAULT 'SEND_EMAIL',
    recipients_json     JSON            NOT NULL,  -- ["security@example.com"]

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audalert_cfg
        FOREIGN KEY (audit_config_id) REFERENCES swfaw_audit_config(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_audalert (audit_config_id, event_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Note: Add alerting_enabled to swfaw_audit_config:

```sql
-- Add to swfaw_audit_config (after format section):
    alerting_enabled    TINYINT(1)      NOT NULL DEFAULT 1,
```

---

## Table 26: `swfaw_authorization_config`

**Replaces:** `authorization_layer.json` (top-level settings + access controls +
document group types + super user settings + entity access control)

```sql
CREATE TABLE swfaw_authorization_config (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Master settings
    authz_enabled           TINYINT(1)  NOT NULL DEFAULT 1,
    access_control_model    VARCHAR(50) NOT NULL DEFAULT 'document-based',

    -- Access control types (from accessControls[])
    -- Stored as JSON array since it's a fixed set of {name, description, enabled}
    access_controls_json    JSON        NOT NULL,

    -- Document group types (from documentGroupTypes[])
    -- Stored as JSON array — complex nested objects, rarely queried individually
    document_group_types_json JSON      NOT NULL,

    -- Super user settings (from superUserSettings)
    super_user_enabled              TINYINT(1) NOT NULL DEFAULT 1,
    super_user_bypass_all           TINYINT(1) NOT NULL DEFAULT 1,
    super_user_require_justification TINYINT(1) NOT NULL DEFAULT 1,
    super_user_justification_min_len INT       NOT NULL DEFAULT 10,
    super_user_log_all_actions      TINYINT(1) NOT NULL DEFAULT 1,

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_authzcfg_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_authzcfg (app_definition_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## Table 27: `swfaw_entity_access_control`

**Replaces:** `authorization_layer.json → entityAccessControl[]`

Per-entity authorization settings. One row per entity.

```sql
CREATE TABLE swfaw_entity_access_control (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    authorization_config_id BIGINT UNSIGNED NOT NULL,

    -- Entity identity
    entity_name         VARCHAR(255)    NOT NULL,
    table_name          VARCHAR(255)    NOT NULL,
    is_root_entity      TINYINT(1)      NOT NULL DEFAULT 0,

    -- Access control flags
    enable_access_control   TINYINT(1)  NOT NULL DEFAULT 1,
    check_on_create         TINYINT(1)  NOT NULL DEFAULT 1,
    check_on_read           TINYINT(1)  NOT NULL DEFAULT 1,
    check_on_update         TINYINT(1)  NOT NULL DEFAULT 1,
    check_on_delete         TINYINT(1)  NOT NULL DEFAULT 1,

    -- Custom rules (rarely used, variable structure)
    custom_rules_json       JSON,

    CONSTRAINT fk_entac_authz
        FOREIGN KEY (authorization_config_id)
        REFERENCES swfaw_authorization_config(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_entac (authorization_config_id, entity_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Design Decisions

- **access_controls and document_group_types as JSON** — these are application-wide
  configuration arrays with complex nested structures. They're loaded once and
  used as-is during code generation. Normalizing them would require 2-3 additional
  tables for data that's rarely queried at the field level.
- **Entity access control normalized** — unlike the above, these are per-entity
  rows with simple boolean flags that are frequently queried ("which entities
  have access control disabled?").
- **Super user settings flattened** — always 1:1, always present, simple scalars.

---

## Table 28: `swfaw_group_definition`

**Replaces:** `group_definition_layer.json` (system groups + table access groups +
group management settings + owner enrollment defaults)

This is a unified table for all group types. The `group_category` column
distinguishes between system groups and table access groups.

```sql
CREATE TABLE swfaw_group_definition (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Group identity
    group_name          VARCHAR(255)    NOT NULL,
    description         TEXT,
    group_category      VARCHAR(50)     NOT NULL,  -- 'SYSTEM' or 'TABLE_ACCESS'

    -- System group fields (from systemGroups[])
    is_super_group      TINYINT(1)      NOT NULL DEFAULT 0,
    is_default_group    TINYINT(1)      NOT NULL DEFAULT 0,
    auto_assign_new_users TINYINT(1)    NOT NULL DEFAULT 0,

    -- Table access group fields (from tableAccessGroups[])
    -- NULL for system groups
    table_name          VARCHAR(255),
    entity_name         VARCHAR(255),
    group_type          VARCHAR(50),    -- TABLE_USER, TABLE_ADMIN
    access_level        VARCHAR(50),    -- USER, ADMIN

    -- Permissions (from tableAccessGroups[].permissions)
    -- NULL for system groups
    allow_read          TINYINT(1)      DEFAULT NULL,
    allow_create        TINYINT(1)      DEFAULT NULL,
    allow_update        TINYINT(1)      DEFAULT NULL,
    allow_delete        TINYINT(1)      DEFAULT NULL,
    allow_grant_access  TINYINT(1)      DEFAULT NULL,
    allow_export        TINYINT(1)      DEFAULT NULL,
    allow_share         TINYINT(1)      DEFAULT NULL,
    allow_audit         TINYINT(1)      DEFAULT NULL,

    -- Ordering
    sort_order          INT             NOT NULL DEFAULT 0,

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_grpdef_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_grpdef (app_definition_id, group_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## Table 29: `swfaw_group_config`

**Replaces:** `group_definition_layer.json → groupManagement` +
`ownerEnrollmentDefaults`

One row per app — the global group management settings.

```sql
CREATE TABLE swfaw_group_config (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Group management (from groupManagement)
    allow_runtime_creation      TINYINT(1) NOT NULL DEFAULT 0,
    allow_runtime_deletion      TINYINT(1) NOT NULL DEFAULT 0,
    admin_can_grant_membership  TINYINT(1) NOT NULL DEFAULT 1,
    admin_can_revoke_membership TINYINT(1) NOT NULL DEFAULT 1,
    admin_group_name            VARCHAR(255) DEFAULT 'Administrators',

    -- Owner enrollment defaults (from ownerEnrollmentDefaults)
    ownership_check         VARCHAR(50) DEFAULT 'CREATOR_RECORDS',
    max_records_per_user    INT,
    allow_enroll            TINYINT(1)  NOT NULL DEFAULT 0,
    allow_unenroll          TINYINT(1)  NOT NULL DEFAULT 0,

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_grpcfg_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_grpcfg (app_definition_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Design Decisions

- **Unified group table** — system groups and table access groups share the same
  table with `group_category` as the discriminator. This avoids two nearly-identical
  tables and makes "list all groups" queries trivial.
- **Permission columns nullable** — system groups don't have table-level permissions,
  so these columns are NULL for `group_category = 'SYSTEM'`.
- **Group config separated** — the management settings and owner enrollment defaults
  are app-wide (not per-group), so they live in their own 1:1 table.

---

## Table 30: `swfaw_custom_query_template`

**Replaces:** `custom_queries_layer.json → queries[]`

These are authorization-level custom query templates (different from the
R2DBC queries in `swfaw_query`). They define record-matching conditions
for CUSTOM_QUERY and CUSTOM_QUERY_ALL document group types.

```sql
CREATE TABLE swfaw_custom_query_template (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Query template identity
    query_name          VARCHAR(255)    NOT NULL,
    description         TEXT,
    table_name          VARCHAR(255)    NOT NULL,

    -- Conditions stored as JSON array
    -- Each: {field, operator, value}
    conditions_json     JSON            NOT NULL,

    -- Logic combinator
    logic               VARCHAR(10)     NOT NULL DEFAULT 'AND',  -- AND or OR

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_cqtpl_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_cqtpl (app_definition_id, query_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Design Decisions

- **Conditions as JSON** — each query has 1-5 conditions with a simple
  {field, operator, value} structure. Normalizing into a separate table
  would add complexity for very little benefit.
- **Separate from swfaw_query** — these serve a completely different purpose
  (authorization record matching vs. R2DBC data queries). Keeping them
  separate avoids confusion and allows independent evolution.
