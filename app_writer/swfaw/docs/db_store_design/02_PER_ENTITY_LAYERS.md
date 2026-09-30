# Tier 2: Per-Entity Layer Tables

These tables store the per-entity generation configurations.
Each has a 1:1 relationship with `swfaw_entity` (one config row per entity).

All tables reference `app_definition_id` for direct access and
`entity_name` as the logical link to the entity.

---

## Table 3: `swfaw_relationship`

**Replaces:** `relationships.json`

```sql
CREATE TABLE swfaw_relationship (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Relationship definition
    source_table        VARCHAR(255)    NOT NULL,
    target_table        VARCHAR(255)    NOT NULL,
    relationship_type   VARCHAR(50)     NOT NULL,  -- OneToOne, OneToMany, ManyToOne, ManyToMany
    foreign_key_column  VARCHAR(255),
    join_table          VARCHAR(255),              -- For ManyToMany

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_rel_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    INDEX idx_rel_source (app_definition_id, source_table),
    INDEX idx_rel_target (app_definition_id, target_table)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## Table 4: `swfaw_entity_layer`

**Replaces:** `entity_layer.json` (the header per entity, without fields)

```sql
CREATE TABLE swfaw_entity_layer (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- From entity_layer.json → entities[]
    table_name          VARCHAR(255)    NOT NULL,
    class_name          VARCHAR(255)    NOT NULL,
    package_name        VARCHAR(255)    NOT NULL DEFAULT 'com.example.entity',

    -- Entity flags
    is_root_entity      TINYINT(1)      NOT NULL DEFAULT 0,
    parent_entity       VARCHAR(255),
    has_public_flag     TINYINT(1)      NOT NULL DEFAULT 0,
    has_audit_fields    TINYINT(1)      NOT NULL DEFAULT 1,
    has_soft_delete     TINYINT(1)      NOT NULL DEFAULT 1,

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_entlayer_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_entlayer (app_definition_id, table_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## Table 5: `swfaw_entity_layer_field`

**Replaces:** `entity_layer.json → entities[].fields[]`

Fields are normalized into their own table because:
- They're individually referenced by DTO and filter layers
- Field-level queries are common (e.g., "find all primary key fields")
- The field count per entity varies significantly (3 to 20+)

```sql
CREATE TABLE swfaw_entity_layer_field (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    entity_layer_id     BIGINT UNSIGNED NOT NULL,

    -- From entity_layer.json → entities[].fields[]
    column_name         VARCHAR(255)    NOT NULL,
    field_name          VARCHAR(255)    NOT NULL,
    java_type           VARCHAR(100)    NOT NULL,
    is_primary_key      TINYINT(1)      NOT NULL DEFAULT 0,
    is_nullable         TINYINT(1)      NOT NULL DEFAULT 1,
    column_definition   VARCHAR(500)    NOT NULL DEFAULT '',

    -- Ordering
    sort_order          INT             NOT NULL DEFAULT 0,

    CONSTRAINT fk_entfield_layer
        FOREIGN KEY (entity_layer_id) REFERENCES swfaw_entity_layer(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_entfield (entity_layer_id, column_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Field Mapping

| JSON Path | DB Column |
|-----------|-----------|
| `fields[].columnName` | `column_name` |
| `fields[].fieldName` | `field_name` |
| `fields[].javaType` | `java_type` |
| `fields[].isPrimaryKey` | `is_primary_key` |
| `fields[].isNullable` | `is_nullable` |
| `fields[].columnDefinition` | `column_definition` |

---

## Table 6: `swfaw_repository_layer`

**Replaces:** `repository_layer.json → repositories[]`

```sql
CREATE TABLE swfaw_repository_layer (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- From repository_layer.json → repositories[]
    entity_name         VARCHAR(255)    NOT NULL,
    class_name          VARCHAR(255)    NOT NULL,
    package_name        VARCHAR(255)    NOT NULL DEFAULT 'com.example.repository',
    id_type             VARCHAR(50)     NOT NULL DEFAULT 'Long',

    -- Feature flags
    has_custom_queries  TINYINT(1)      NOT NULL DEFAULT 0,
    custom_queries_json JSON,           -- Array of custom query objects (legacy, pre-query_layer)
    has_soft_delete     TINYINT(1)      NOT NULL DEFAULT 0,
    has_authorization   TINYINT(1)      NOT NULL DEFAULT 0,
    enable_caching      TINYINT(1)      NOT NULL DEFAULT 0,
    cache_names_json    JSON,           -- Array of cache name strings

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_repolayer_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_repolayer (app_definition_id, entity_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## Table 7: `swfaw_service_layer`

**Replaces:** `service_layer.json → services[]`

```sql
CREATE TABLE swfaw_service_layer (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- From service_layer.json → services[]
    entity_name         VARCHAR(255)    NOT NULL,
    class_name          VARCHAR(255)    NOT NULL,
    package_name        VARCHAR(255)    NOT NULL DEFAULT 'com.example.service',
    repository_name     VARCHAR(255)    NOT NULL,
    is_root_entity      TINYINT(1)      NOT NULL DEFAULT 0,
    has_authorization   TINYINT(1)      NOT NULL DEFAULT 0,

    -- Authorization config (from services[].authorizationConfig)
    auth_check_on_create    TINYINT(1)  NOT NULL DEFAULT 1,
    auth_check_on_read      TINYINT(1)  NOT NULL DEFAULT 1,
    auth_check_on_update    TINYINT(1)  NOT NULL DEFAULT 1,
    auth_check_on_delete    TINYINT(1)  NOT NULL DEFAULT 1,
    auth_allow_public_read  TINYINT(1)  NOT NULL DEFAULT 0,
    auth_require_ownership  TINYINT(1)  NOT NULL DEFAULT 1,

    -- Transaction config (from services[].transactionManagement)
    tx_enabled          TINYINT(1)      NOT NULL DEFAULT 1,
    tx_propagation      VARCHAR(50)     NOT NULL DEFAULT 'REQUIRED',
    tx_isolation        VARCHAR(50)     NOT NULL DEFAULT 'DEFAULT',
    tx_timeout          INT             NOT NULL DEFAULT 30,

    -- Extensible configs stored as JSON
    custom_methods_json     JSON,       -- Array of custom method definitions
    validation_rules_json   JSON,       -- {onCreate: [], onUpdate: [], onDelete: []}

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_svclayer_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_svclayer (app_definition_id, entity_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Design Decisions

- **Authorization config flattened** — these 6 booleans are frequently queried
  and always present. No need for a nested JSON object.
- **Transaction config flattened** — same reasoning, always 1:1 with the service.
- **custom_methods and validation_rules as JSON** — these are variable-length
  arrays that are loaded as a batch. Normalizing them would add complexity
  without clear query benefits.


---

## Table 8: `swfaw_controller_layer`

**Replaces:** `controller_layer.json → controllers[]`

```sql
CREATE TABLE swfaw_controller_layer (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- From controller_layer.json → controllers[]
    entity_name         VARCHAR(255)    NOT NULL,
    class_name          VARCHAR(255)    NOT NULL,
    package_name        VARCHAR(255)    NOT NULL DEFAULT 'com.example.controller',
    service_name        VARCHAR(255)    NOT NULL,
    base_path           VARCHAR(255)    NOT NULL,
    is_root_entity      TINYINT(1)      NOT NULL DEFAULT 0,

    -- Standard CRUD endpoints config (from controllers[].endpoints)
    -- Each stored as JSON: {enabled, path, method, requiresAuth, roles[], rateLimitPerMinute, ...}
    endpoint_create_json    JSON,
    endpoint_get_by_id_json JSON,
    endpoint_get_all_json   JSON,
    endpoint_update_json    JSON,
    endpoint_delete_json    JSON,

    -- Custom endpoints (from controllers[].customEndpoints)
    custom_endpoints_json   JSON,       -- Array of custom endpoint objects

    -- CORS config (from controllers[].corsConfig)
    cors_enabled            TINYINT(1)  NOT NULL DEFAULT 1,
    cors_allowed_origins    JSON,       -- Array of origin strings
    cors_allowed_methods    JSON,       -- Array of method strings
    cors_allowed_headers    JSON,       -- Array of header strings
    cors_max_age            INT         NOT NULL DEFAULT 3600,

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_ctrllayer_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_ctrllayer (app_definition_id, entity_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Design Decisions

- **Each CRUD endpoint as a separate JSON column** rather than one big `endpoints_json`.
  This allows queries like "find all controllers where create is disabled":
  `WHERE JSON_EXTRACT(endpoint_create_json, '$.enabled') = false`
- **CORS config partially flattened** — `cors_enabled` is a flat boolean for quick
  filtering, while the arrays remain JSON since they're variable-length lists.
- **Custom endpoints as JSON** — these are rare and variable in structure, so
  normalizing them would add a table that's mostly empty.

---

## Table 9: `swfaw_dto_layer`

**Replaces:** `dto_layer.json → dtos[]`

Each entity produces up to 3 DTOs (Input, Output, Filter). Each DTO row contains
its field configurations as JSON since they include nested validation rules.

```sql
CREATE TABLE swfaw_dto_layer (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- From dto_layer.json → dtos[]
    entity_name         VARCHAR(255)    NOT NULL,
    dto_type            VARCHAR(20)     NOT NULL,  -- 'Input', 'Output', 'Filter'
    class_name          VARCHAR(255)    NOT NULL,
    package_name        VARCHAR(255)    NOT NULL DEFAULT 'com.example.dto',
    is_root_entity      TINYINT(1)      NOT NULL DEFAULT 0,

    -- Field configs with validation rules (from dtos[].fields)
    -- Each element: {fieldName, javaType, includeInDTO, validation: {required, maxLength, email, ...}}
    field_configs_json  JSON            NOT NULL,

    -- Additional DTO settings
    custom_validators_json      JSON,   -- Array of custom validator class definitions
    exclude_sensitive_fields    JSON,   -- Array of field names to exclude from Output DTOs
    include_relationships       TINYINT(1) NOT NULL DEFAULT 0,

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_dtolayer_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_dtolayer (app_definition_id, entity_name, dto_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Design Decisions

- **field_configs as JSON** — Each field has nested validation rules with varying
  properties (required, maxLength, email, pattern, min, max, etc.). Normalizing
  this into separate tables would require:
  - `swfaw_dto_field` (one row per field per DTO)
  - `swfaw_dto_field_validation` (one row per validation rule per field)
  That's potentially 3 DTOs × 10 fields × 3 rules = 90 rows per entity.
  JSON keeps it manageable and matches how the generator consumes it.
- **Unique key on (app_definition_id, entity_name, dto_type)** — ensures one
  Input DTO, one Output DTO, and one Filter DTO per entity.

### field_configs_json Structure

```json
[
  {
    "fieldName": "firstName",
    "javaType": "String",
    "includeInDTO": true,
    "validation": {
      "required": true,
      "requiredMessage": "Firstname is required",
      "maxLength": 100,
      "maxLengthMessage": "Firstname cannot exceed 100 characters"
    }
  },
  {
    "fieldName": "emailAddress",
    "javaType": "String",
    "includeInDTO": true,
    "validation": {
      "required": true,
      "requiredMessage": "Email is required",
      "email": true,
      "emailMessage": "Please provide a valid email address",
      "maxLength": 255,
      "maxLengthMessage": "Email cannot exceed 255 characters"
    }
  }
]
```
