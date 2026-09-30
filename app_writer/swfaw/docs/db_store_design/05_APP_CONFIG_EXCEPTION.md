# Tier 4b: Application Config & Exception Tables

---

## Table 19: `swfaw_app_config`

**Replaces:** `config_layer.json`

The config layer has deeply nested structures (server, database, logging,
features with sub-objects for swagger, actuator, caching, email, etc.).
We use a hybrid approach: flat columns for the most-queried settings,
JSON for the nested feature configs.

```sql
CREATE TABLE swfaw_app_config (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Project config (from config_layer.json → project)
    package_name        VARCHAR(255)    NOT NULL DEFAULT 'com.example',
    java_version        VARCHAR(10)     NOT NULL DEFAULT '17',
    spring_boot_version VARCHAR(20)     NOT NULL DEFAULT '3.2.0',

    -- Server config (from config_layer.json → server)
    server_port         INT             NOT NULL DEFAULT 8081,
    server_context_path VARCHAR(100)    NOT NULL DEFAULT '/',
    server_compression_enabled  TINYINT(1) NOT NULL DEFAULT 1,
    server_http2_enabled        TINYINT(1) NOT NULL DEFAULT 1,
    server_ssl_enabled          TINYINT(1) NOT NULL DEFAULT 0,
    server_ssl_json             JSON,      -- {keyStore, keyStorePassword, keyStoreType}
    server_compression_types    JSON,      -- Array of MIME type strings

    -- Database config (from config_layer.json → database)
    -- Note: Core db connection info lives on swfaw_app_definition.
    -- This table stores R2DBC pool and SQL formatting settings.
    r2dbc_pool_initial_size     INT         NOT NULL DEFAULT 10,
    r2dbc_pool_max_size         INT         NOT NULL DEFAULT 50,
    r2dbc_pool_max_idle_time    VARCHAR(20) NOT NULL DEFAULT '30m',
    r2dbc_pool_max_life_time    VARCHAR(20) NOT NULL DEFAULT '60m',
    r2dbc_pool_max_acquire_time VARCHAR(20) NOT NULL DEFAULT '3s',
    r2dbc_pool_max_create_time  VARCHAR(20) NOT NULL DEFAULT '3s',
    db_show_sql                 TINYINT(1)  NOT NULL DEFAULT 0,
    db_format_sql               TINYINT(1)  NOT NULL DEFAULT 1,

    -- Logging config (from config_layer.json → logging)
    log_level_root          VARCHAR(20) NOT NULL DEFAULT 'INFO',
    log_level_application   VARCHAR(20) NOT NULL DEFAULT 'DEBUG',
    log_level_spring        VARCHAR(20) NOT NULL DEFAULT 'INFO',
    log_level_hibernate     VARCHAR(20) NOT NULL DEFAULT 'WARN',
    log_pattern_console     VARCHAR(500),
    log_pattern_file        VARCHAR(500),
    log_file_enabled        TINYINT(1)  NOT NULL DEFAULT 1,
    log_file_name           VARCHAR(255) DEFAULT 'logs/application.log',
    log_file_max_size       VARCHAR(20) DEFAULT '10MB',
    log_file_max_history    INT         NOT NULL DEFAULT 30,
    log_file_total_size_cap VARCHAR(20) DEFAULT '1GB',

    -- Feature flags (from config_layer.json → features)
    -- Swagger
    swagger_enabled         TINYINT(1)  NOT NULL DEFAULT 1,
    swagger_title           VARCHAR(255),
    swagger_description     TEXT,
    swagger_version         VARCHAR(50),
    swagger_contact_name    VARCHAR(255),
    swagger_contact_email   VARCHAR(255),

    -- Actuator
    actuator_enabled        TINYINT(1)  NOT NULL DEFAULT 1,
    actuator_base_path      VARCHAR(100) DEFAULT '/actuator',
    actuator_endpoints_json JSON,       -- ["health", "info", "metrics", "prometheus"]

    -- Caching
    caching_enabled         TINYINT(1)  NOT NULL DEFAULT 0,
    caching_type            VARCHAR(50) DEFAULT 'redis',
    caching_redis_json      JSON,       -- {host, port, password, database}
    caching_ttl             INT         NOT NULL DEFAULT 3600,

    -- Email
    email_enabled           TINYINT(1)  NOT NULL DEFAULT 0,
    email_host              VARCHAR(255),
    email_port              INT,
    email_username          VARCHAR(255),
    email_password          VARCHAR(255),
    email_from              VARCHAR(255),
    email_tls               TINYINT(1)  NOT NULL DEFAULT 1,

    -- Profiles (from config_layer.json → profiles)
    active_profile          VARCHAR(50) NOT NULL DEFAULT 'dev',
    available_profiles_json JSON,       -- ["dev", "test", "prod"]

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_appconfig_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_appconfig (app_definition_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Design Decisions

- **One wide table** — config_layer.json is always 1:1 with the app definition.
  Yes, it's ~50 columns, but it's one row per app and every field is a simple
  scalar or small JSON array. No joins needed to load the full config.
- **R2DBC pool settings flattened** — always present, always the same structure.
- **Logging flattened** — same reasoning. The log levels and file settings are
  always present with fixed keys.
- **Feature sub-configs (swagger, actuator, caching, email)** kept in the same
  table with prefixed column names. Each has an `_enabled` flag for quick filtering.
  The alternative (4 separate tables) would add complexity for rarely-queried data.
- **Redis config as JSON** — only relevant when caching is enabled. A separate
  table for 4 fields that are only used conditionally isn't worth it.

---

## Table 20: `swfaw_exception_definition`

**Replaces:** `exception_layer.json → customExceptions[]` + error response format
+ global exception handling settings

```sql
CREATE TABLE swfaw_exception_definition (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Custom exception class definition
    class_name          VARCHAR(255)    NOT NULL,
    package_name        VARCHAR(255)    NOT NULL DEFAULT 'com.example.exception',
    http_status         INT             NOT NULL,
    default_message     TEXT            NOT NULL,
    include_timestamp   TINYINT(1)      NOT NULL DEFAULT 1,
    include_stack_trace TINYINT(1)      NOT NULL DEFAULT 0,
    include_field_errors TINYINT(1)     NOT NULL DEFAULT 0,

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_excdef_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_excdef (app_definition_id, class_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## Table 21: `swfaw_exception_config`

**Replaces:** `exception_layer.json → errorResponseFormat` +
`globalExceptionHandling` + `logging`

One row per app — the global exception handling settings.

```sql
CREATE TABLE swfaw_exception_config (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Error response format (from exception_layer.json → errorResponseFormat)
    resp_include_timestamp      TINYINT(1) NOT NULL DEFAULT 1,
    resp_include_status         TINYINT(1) NOT NULL DEFAULT 1,
    resp_include_error          TINYINT(1) NOT NULL DEFAULT 1,
    resp_include_message        TINYINT(1) NOT NULL DEFAULT 1,
    resp_include_path           TINYINT(1) NOT NULL DEFAULT 1,
    resp_include_stack_trace    TINYINT(1) NOT NULL DEFAULT 0,
    resp_include_field_errors   TINYINT(1) NOT NULL DEFAULT 1,
    resp_timestamp_format       VARCHAR(100) DEFAULT 'yyyy-MM-dd''T''HH:mm:ss.SSS''Z''',

    -- Global exception handling flags
    handle_validation_errors        TINYINT(1) NOT NULL DEFAULT 1,
    handle_method_arg_not_valid     TINYINT(1) NOT NULL DEFAULT 1,
    handle_constraint_violation     TINYINT(1) NOT NULL DEFAULT 1,
    handle_http_msg_not_readable    TINYINT(1) NOT NULL DEFAULT 1,
    handle_access_denied            TINYINT(1) NOT NULL DEFAULT 1,
    handle_authentication_error     TINYINT(1) NOT NULL DEFAULT 1,
    handle_internal_server_error    TINYINT(1) NOT NULL DEFAULT 1,

    -- Logging
    log_exceptions      TINYINT(1)      NOT NULL DEFAULT 1,
    log_stack_trace     TINYINT(1)      NOT NULL DEFAULT 1,
    log_level           VARCHAR(20)     NOT NULL DEFAULT 'ERROR',

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_excconfig_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_excconfig (app_definition_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## Table 22: `swfaw_exception_message`

**Replaces:** `exception_layer.json → exceptionMessages`

The exception messages map is a two-level structure:
`exceptionMessages[ExceptionClass][EntityOrField] = "message"`

```sql
CREATE TABLE swfaw_exception_message (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Message mapping
    exception_class     VARCHAR(255)    NOT NULL,  -- e.g. "ResourceNotFoundException"
    target_name         VARCHAR(255)    NOT NULL,  -- Entity name or field name
    message             TEXT            NOT NULL,

    CONSTRAINT fk_excmsg_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_excmsg (app_definition_id, exception_class, target_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Design Decisions

- **Normalized into rows** rather than a JSON blob. Rationale:
  - The current JSON has 100+ entity-specific messages for ResourceNotFoundException
  - Individual messages are frequently edited (customizing per-entity error text)
  - Queries like "find all messages for User entity" become trivial
  - The LayerManager currently navigates this with path notation like
    `exceptionMessages.ResourceNotFoundException.User` — the DB equivalent is
    a simple WHERE clause
- **No FK to swfaw_exception_definition** — messages can reference exception
  classes that aren't custom-defined (e.g., built-in Spring exceptions).
  The `exception_class` is a logical key, not a strict FK.

### Example Data

| exception_class | target_name | message |
|----------------|-------------|---------|
| ResourceNotFoundException | User | User not found with the provided ID |
| ResourceNotFoundException | Course | Course not found with the provided ID |
| ValidationException | email | Please provide a valid email address |
| ValidationException | phone | Please provide a valid phone number |
