-- ============================================================================
-- SWFAW Definition Store - Database Schema
-- Version: 1.0.0
-- Description: Stores application definitions for swfaw_v2 code generator
-- Database: MySQL 8.0+
-- Generated: 2026-03-14
-- ============================================================================

CREATE DATABASE IF NOT EXISTS swfaw_definition_store
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE swfaw_definition_store;

-- ============================================================================
-- TIER 1: FOUNDATION TABLES
-- ============================================================================

-- Table 1: swfaw_app_definition
-- Replaces: manifest.json + project_metadata.json
-- One row = one complete application definition
CREATE TABLE swfaw_app_definition (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,

    -- Manifest info
    version             VARCHAR(10)     NOT NULL DEFAULT '2.5',
    format              VARCHAR(20)     NOT NULL DEFAULT 'database',
    description         TEXT,

    -- Project metadata
    project_name        VARCHAR(255)    NOT NULL,
    application_name    VARCHAR(255)    NOT NULL,
    group_id            VARCHAR(255)    NOT NULL DEFAULT 'com.example',
    artifact_id         VARCHAR(255)    NOT NULL,
    project_version     VARCHAR(50)     NOT NULL DEFAULT '1.0.0',
    port                INT             NOT NULL DEFAULT 8081,
    sql_file_name       VARCHAR(255),

    -- Database config
    db_type             VARCHAR(50)     NOT NULL DEFAULT 'mysql',
    db_host             VARCHAR(255)    NOT NULL DEFAULT 'localhost',
    db_port             INT             NOT NULL DEFAULT 3306,
    db_name             VARCHAR(255)    NOT NULL,
    db_url              VARCHAR(500),
    db_username         VARCHAR(255)    NOT NULL DEFAULT 'root',
    db_password         VARCHAR(255)    NOT NULL DEFAULT 'password',

    -- Statistics (denormalized)
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


-- Table 2: swfaw_entity
-- Replaces: entities.json
CREATE TABLE swfaw_entity (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    table_name          VARCHAR(255)    NOT NULL,
    columns_json        JSON            NOT NULL,
    column_count        INT             NOT NULL DEFAULT 0,
    primary_key_column  VARCHAR(255),
    sort_order          INT             NOT NULL DEFAULT 0,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_entity_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_entity_table (app_definition_id, table_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================================
-- TIER 2: PER-ENTITY LAYER TABLES
-- ============================================================================

-- Table 3: swfaw_relationship
-- Replaces: relationships.json
CREATE TABLE swfaw_relationship (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    source_table        VARCHAR(255)    NOT NULL,
    target_table        VARCHAR(255)    NOT NULL,
    relationship_type   VARCHAR(50)     NOT NULL,
    foreign_key_column  VARCHAR(255),
    join_table          VARCHAR(255),

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_rel_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    INDEX idx_rel_source (app_definition_id, source_table),
    INDEX idx_rel_target (app_definition_id, target_table)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 4: swfaw_entity_layer
-- Replaces: entity_layer.json (per-entity header)
CREATE TABLE swfaw_entity_layer (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    table_name          VARCHAR(255)    NOT NULL,
    class_name          VARCHAR(255)    NOT NULL,
    package_name        VARCHAR(255)    NOT NULL DEFAULT 'com.example.entity',
    is_root_entity      TINYINT(1)      NOT NULL DEFAULT 0,
    parent_entity       VARCHAR(255),
    has_public_flag     TINYINT(1)      NOT NULL DEFAULT 0,
    has_audit_fields    TINYINT(1)      NOT NULL DEFAULT 1,
    has_soft_delete     TINYINT(1)      NOT NULL DEFAULT 1,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_entlayer_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_entlayer (app_definition_id, table_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 5: swfaw_entity_layer_field
-- Replaces: entity_layer.json → entities[].fields[]
CREATE TABLE swfaw_entity_layer_field (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    entity_layer_id     BIGINT UNSIGNED NOT NULL,

    column_name         VARCHAR(255)    NOT NULL,
    field_name          VARCHAR(255)    NOT NULL,
    java_type           VARCHAR(100)    NOT NULL,
    is_primary_key      TINYINT(1)      NOT NULL DEFAULT 0,
    is_nullable         TINYINT(1)      NOT NULL DEFAULT 1,
    column_definition   VARCHAR(500)    NOT NULL DEFAULT '',
    sort_order          INT             NOT NULL DEFAULT 0,

    CONSTRAINT fk_entfield_layer
        FOREIGN KEY (entity_layer_id) REFERENCES swfaw_entity_layer(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_entfield (entity_layer_id, column_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 6: swfaw_repository_layer
-- Replaces: repository_layer.json
CREATE TABLE swfaw_repository_layer (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    entity_name         VARCHAR(255)    NOT NULL,
    class_name          VARCHAR(255)    NOT NULL,
    package_name        VARCHAR(255)    NOT NULL DEFAULT 'com.example.repository',
    id_type             VARCHAR(50)     NOT NULL DEFAULT 'Long',
    has_custom_queries  TINYINT(1)      NOT NULL DEFAULT 0,
    custom_queries_json JSON,
    has_soft_delete     TINYINT(1)      NOT NULL DEFAULT 0,
    has_authorization   TINYINT(1)      NOT NULL DEFAULT 0,
    enable_caching      TINYINT(1)      NOT NULL DEFAULT 0,
    cache_names_json    JSON,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_repolayer_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_repolayer (app_definition_id, entity_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 7: swfaw_service_layer
-- Replaces: service_layer.json
CREATE TABLE swfaw_service_layer (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    entity_name         VARCHAR(255)    NOT NULL,
    class_name          VARCHAR(255)    NOT NULL,
    package_name        VARCHAR(255)    NOT NULL DEFAULT 'com.example.service',
    repository_name     VARCHAR(255)    NOT NULL,
    is_root_entity      TINYINT(1)      NOT NULL DEFAULT 0,
    has_authorization   TINYINT(1)      NOT NULL DEFAULT 0,

    -- Authorization config (flattened)
    auth_check_on_create    TINYINT(1)  NOT NULL DEFAULT 1,
    auth_check_on_read      TINYINT(1)  NOT NULL DEFAULT 1,
    auth_check_on_update    TINYINT(1)  NOT NULL DEFAULT 1,
    auth_check_on_delete    TINYINT(1)  NOT NULL DEFAULT 1,
    auth_allow_public_read  TINYINT(1)  NOT NULL DEFAULT 0,
    auth_require_ownership  TINYINT(1)  NOT NULL DEFAULT 1,

    -- Transaction config (flattened)
    tx_enabled          TINYINT(1)      NOT NULL DEFAULT 1,
    tx_propagation      VARCHAR(50)     NOT NULL DEFAULT 'REQUIRED',
    tx_isolation        VARCHAR(50)     NOT NULL DEFAULT 'DEFAULT',
    tx_timeout          INT             NOT NULL DEFAULT 30,

    -- Extensible configs
    custom_methods_json     JSON,
    validation_rules_json   JSON,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_svclayer_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_svclayer (app_definition_id, entity_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 8: swfaw_controller_layer
-- Replaces: controller_layer.json
CREATE TABLE swfaw_controller_layer (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    entity_name         VARCHAR(255)    NOT NULL,
    class_name          VARCHAR(255)    NOT NULL,
    package_name        VARCHAR(255)    NOT NULL DEFAULT 'com.example.controller',
    service_name        VARCHAR(255)    NOT NULL,
    base_path           VARCHAR(255)    NOT NULL,
    is_root_entity      TINYINT(1)      NOT NULL DEFAULT 0,

    -- Standard CRUD endpoint configs (each as JSON object)
    endpoint_create_json    JSON,
    endpoint_get_by_id_json JSON,
    endpoint_get_all_json   JSON,
    endpoint_update_json    JSON,
    endpoint_delete_json    JSON,

    -- Custom endpoints
    custom_endpoints_json   JSON,

    -- Per-controller CORS config
    cors_enabled            TINYINT(1)  NOT NULL DEFAULT 1,
    cors_allowed_origins    JSON,
    cors_allowed_methods    JSON,
    cors_allowed_headers    JSON,
    cors_max_age            INT         NOT NULL DEFAULT 3600,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_ctrllayer_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_ctrllayer (app_definition_id, entity_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 9: swfaw_dto_layer
-- Replaces: dto_layer.json
CREATE TABLE swfaw_dto_layer (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    entity_name         VARCHAR(255)    NOT NULL,
    dto_type            VARCHAR(20)     NOT NULL,
    class_name          VARCHAR(255)    NOT NULL,
    package_name        VARCHAR(255)    NOT NULL DEFAULT 'com.example.dto',
    is_root_entity      TINYINT(1)      NOT NULL DEFAULT 0,

    -- Field configs with nested validation rules
    field_configs_json  JSON            NOT NULL,

    -- Additional DTO settings
    custom_validators_json      JSON,
    exclude_sensitive_fields    JSON,
    include_relationships       TINYINT(1) NOT NULL DEFAULT 0,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_dtolayer_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_dtolayer (app_definition_id, entity_name, dto_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================================
-- TIER 3: QUERY & FILTER LAYER TABLES
-- ============================================================================

-- Table 10: swfaw_query
-- Replaces: query_layer.json → queries[EntityName][]
CREATE TABLE swfaw_query (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    entity_name         VARCHAR(255)    NOT NULL,
    query_name          VARCHAR(255)    NOT NULL,
    description         TEXT,

    return_type         VARCHAR(255)    NOT NULL,
    select_fields_json  JSON            NOT NULL,
    from_clause         VARCHAR(500)    NOT NULL,
    where_clauses_json  JSON,
    group_by_json       JSON,
    having_json         JSON,
    order_by_json       JSON,

    pagination          TINYINT(1)      NOT NULL DEFAULT 1,

    authz_enabled       TINYINT(1)      NOT NULL DEFAULT 1,
    authz_document_field VARCHAR(255),

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_query_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_query (app_definition_id, entity_name, query_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 11: swfaw_query_join
-- Replaces: query_layer.json → queries[Entity][].joins[]
CREATE TABLE swfaw_query_join (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    query_id            BIGINT UNSIGNED NOT NULL,

    join_type           VARCHAR(20)     NOT NULL,
    join_table          VARCHAR(255)    NOT NULL,
    join_alias          VARCHAR(100),
    join_condition      VARCHAR(500)    NOT NULL,
    sort_order          INT             NOT NULL DEFAULT 0,

    CONSTRAINT fk_qjoin_query
        FOREIGN KEY (query_id) REFERENCES swfaw_query(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 12: swfaw_query_parameter
-- Replaces: query_layer.json → queries[Entity][].parameters[]
CREATE TABLE swfaw_query_parameter (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    query_id            BIGINT UNSIGNED NOT NULL,

    param_name          VARCHAR(255)    NOT NULL,
    param_type          VARCHAR(100)    NOT NULL,
    is_required         TINYINT(1)      NOT NULL DEFAULT 1,
    default_value       VARCHAR(500),
    sort_order          INT             NOT NULL DEFAULT 0,

    CONSTRAINT fk_qparam_query
        FOREIGN KEY (query_id) REFERENCES swfaw_query(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_qparam (query_id, param_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 13: swfaw_filter
-- Replaces: filter_layer.json → filters[EntityName]
CREATE TABLE swfaw_filter (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    entity_name         VARCHAR(255)    NOT NULL,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_filter_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_filter (app_definition_id, entity_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 14: swfaw_filter_field
-- Replaces: filter_layer.json → filters[EntityName].fields[]
CREATE TABLE swfaw_filter_field (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    filter_id           BIGINT UNSIGNED NOT NULL,

    field_name          VARCHAR(255)    NOT NULL,
    field_type          VARCHAR(100)    NOT NULL,
    operators_json      JSON            NOT NULL,
    sort_order          INT             NOT NULL DEFAULT 0,

    CONSTRAINT fk_ffield_filter
        FOREIGN KEY (filter_id) REFERENCES swfaw_filter(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_ffield (filter_id, field_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================================
-- TIER 4: APPLICATION-WIDE LAYER TABLES
-- ============================================================================

-- --------------------------------------------------------------------------
-- 4a: Security
-- --------------------------------------------------------------------------

-- Table 15: swfaw_security_config
-- Replaces: security_layer.json (core settings)
CREATE TABLE swfaw_security_config (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- JWT
    jwt_enabled         TINYINT(1)      NOT NULL DEFAULT 1,
    jwt_secret          VARCHAR(500)    NOT NULL DEFAULT 'your-secret-key-change-in-production-min-256-bits',
    jwt_expiration      BIGINT          NOT NULL DEFAULT 86400000,
    jwt_expiration_unit VARCHAR(20)     NOT NULL DEFAULT 'milliseconds',
    jwt_issuer          VARCHAR(255),
    jwt_audience        VARCHAR(255),
    jwt_algorithm       VARCHAR(20)     NOT NULL DEFAULT 'HS256',

    -- Refresh token
    refresh_token_enabled    TINYINT(1) NOT NULL DEFAULT 1,
    refresh_token_expiration BIGINT     NOT NULL DEFAULT 604800000,
    refresh_token_exp_unit   VARCHAR(20) NOT NULL DEFAULT 'milliseconds',

    -- OAuth2
    oauth2_enabled      TINYINT(1)      NOT NULL DEFAULT 0,

    -- Password policy
    pw_min_length       INT             NOT NULL DEFAULT 8,
    pw_max_length       INT             NOT NULL DEFAULT 128,
    pw_require_upper    TINYINT(1)      NOT NULL DEFAULT 1,
    pw_require_lower    TINYINT(1)      NOT NULL DEFAULT 1,
    pw_require_digit    TINYINT(1)      NOT NULL DEFAULT 1,
    pw_require_special  TINYINT(1)      NOT NULL DEFAULT 1,
    pw_special_chars    VARCHAR(100)    DEFAULT '!@#$%^&*()_+-=[]{}|;:,.<>?',
    pw_prevent_common   TINYINT(1)      NOT NULL DEFAULT 1,
    pw_expiration_days  INT             NOT NULL DEFAULT 90,
    pw_history_count    INT             NOT NULL DEFAULT 5,

    -- Session management
    session_max_concurrent  INT         NOT NULL DEFAULT 3,
    session_timeout         INT         NOT NULL DEFAULT 1800,
    session_timeout_unit    VARCHAR(20) NOT NULL DEFAULT 'seconds',

    -- CSRF
    csrf_enabled        TINYINT(1)      NOT NULL DEFAULT 0,
    csrf_cookie_name    VARCHAR(100)    DEFAULT 'XSRF-TOKEN',
    csrf_header_name    VARCHAR(100)    DEFAULT 'X-XSRF-TOKEN',

    -- Rate limiting
    rate_limit_enabled          TINYINT(1) NOT NULL DEFAULT 1,
    rate_limit_default_per_min  INT        NOT NULL DEFAULT 60,
    rate_limit_login_max        INT        NOT NULL DEFAULT 5,
    rate_limit_lockout_minutes  INT        NOT NULL DEFAULT 15,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_secconfig_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_secconfig (app_definition_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 16: swfaw_security_oauth2_provider
-- Replaces: security_layer.json → oauth2.providers[]
CREATE TABLE swfaw_security_oauth2_provider (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    security_config_id  BIGINT UNSIGNED NOT NULL,

    provider_name       VARCHAR(100)    NOT NULL,
    client_id           VARCHAR(500)    NOT NULL,
    client_secret       VARCHAR(500)    NOT NULL,
    redirect_uri        VARCHAR(500)    NOT NULL,
    scopes_json         JSON            NOT NULL,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_oauth2_sec
        FOREIGN KEY (security_config_id) REFERENCES swfaw_security_config(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_oauth2_provider (security_config_id, provider_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 17: swfaw_security_cors
-- Replaces: security_layer.json → cors
CREATE TABLE swfaw_security_cors (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    security_config_id  BIGINT UNSIGNED NOT NULL,

    cors_enabled        TINYINT(1)      NOT NULL DEFAULT 1,
    allowed_origins_json    JSON,
    allowed_methods_json    JSON,
    allowed_headers_json    JSON,
    exposed_headers_json    JSON,
    allow_credentials       TINYINT(1)  NOT NULL DEFAULT 1,
    max_age                 INT         NOT NULL DEFAULT 3600,

    CONSTRAINT fk_cors_sec
        FOREIGN KEY (security_config_id) REFERENCES swfaw_security_config(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_cors (security_config_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 18: swfaw_security_public_endpoint
-- Replaces: security_layer.json → publicEndpoints[]
CREATE TABLE swfaw_security_public_endpoint (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    security_config_id  BIGINT UNSIGNED NOT NULL,

    endpoint_pattern    VARCHAR(500)    NOT NULL,
    sort_order          INT             NOT NULL DEFAULT 0,

    CONSTRAINT fk_pubep_sec
        FOREIGN KEY (security_config_id) REFERENCES swfaw_security_config(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_pubep (security_config_id, endpoint_pattern)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- --------------------------------------------------------------------------
-- 4b: Application Config & Exceptions
-- --------------------------------------------------------------------------

-- Table 19: swfaw_app_config
-- Replaces: config_layer.json
CREATE TABLE swfaw_app_config (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Project config
    package_name        VARCHAR(255)    NOT NULL DEFAULT 'com.example',
    java_version        VARCHAR(10)     NOT NULL DEFAULT '17',
    spring_boot_version VARCHAR(20)     NOT NULL DEFAULT '3.2.0',

    -- Server config
    server_port         INT             NOT NULL DEFAULT 8081,
    server_context_path VARCHAR(100)    NOT NULL DEFAULT '/',
    server_compression_enabled  TINYINT(1) NOT NULL DEFAULT 1,
    server_compression_types    JSON,
    server_http2_enabled        TINYINT(1) NOT NULL DEFAULT 1,
    server_ssl_enabled          TINYINT(1) NOT NULL DEFAULT 0,
    server_ssl_json             JSON,

    -- Database R2DBC pool config
    r2dbc_pool_initial_size     INT         NOT NULL DEFAULT 10,
    r2dbc_pool_max_size         INT         NOT NULL DEFAULT 50,
    r2dbc_pool_max_idle_time    VARCHAR(20) NOT NULL DEFAULT '30m',
    r2dbc_pool_max_life_time    VARCHAR(20) NOT NULL DEFAULT '60m',
    r2dbc_pool_max_acquire_time VARCHAR(20) NOT NULL DEFAULT '3s',
    r2dbc_pool_max_create_time  VARCHAR(20) NOT NULL DEFAULT '3s',
    db_show_sql                 TINYINT(1)  NOT NULL DEFAULT 0,
    db_format_sql               TINYINT(1)  NOT NULL DEFAULT 1,

    -- Logging config
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
    actuator_endpoints_json JSON,

    -- Caching
    caching_enabled         TINYINT(1)  NOT NULL DEFAULT 0,
    caching_type            VARCHAR(50) DEFAULT 'redis',
    caching_redis_json      JSON,
    caching_ttl             INT         NOT NULL DEFAULT 3600,

    -- Email
    email_enabled           TINYINT(1)  NOT NULL DEFAULT 0,
    email_host              VARCHAR(255),
    email_port              INT,
    email_username          VARCHAR(255),
    email_password          VARCHAR(255),
    email_from              VARCHAR(255),
    email_tls               TINYINT(1)  NOT NULL DEFAULT 1,

    -- Profiles
    active_profile          VARCHAR(50) NOT NULL DEFAULT 'dev',
    available_profiles_json JSON,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_appconfig_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_appconfig (app_definition_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 20: swfaw_exception_config
-- Replaces: exception_layer.json (global settings)
CREATE TABLE swfaw_exception_config (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Error response format
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

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_excconfig_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_excconfig (app_definition_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 21: swfaw_exception_definition
-- Replaces: exception_layer.json → customExceptions[]
CREATE TABLE swfaw_exception_definition (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    class_name          VARCHAR(255)    NOT NULL,
    package_name        VARCHAR(255)    NOT NULL DEFAULT 'com.example.exception',
    http_status         INT             NOT NULL,
    default_message     TEXT            NOT NULL,
    include_timestamp   TINYINT(1)      NOT NULL DEFAULT 1,
    include_stack_trace TINYINT(1)      NOT NULL DEFAULT 0,
    include_field_errors TINYINT(1)     NOT NULL DEFAULT 0,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_excdef_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_excdef (app_definition_id, class_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 22: swfaw_exception_message
-- Replaces: exception_layer.json → exceptionMessages
CREATE TABLE swfaw_exception_message (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    exception_class     VARCHAR(255)    NOT NULL,
    target_name         VARCHAR(255)    NOT NULL,
    message             TEXT            NOT NULL,

    CONSTRAINT fk_excmsg_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_excmsg (app_definition_id, exception_class, target_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- --------------------------------------------------------------------------
-- 4c: Audit Logging
-- --------------------------------------------------------------------------

-- Table 23: swfaw_audit_config
-- Replaces: audit_logging_layer.json (top-level settings)
CREATE TABLE swfaw_audit_config (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Master switch
    audit_enabled       TINYINT(1)      NOT NULL DEFAULT 1,

    -- Category switches
    auth_events_enabled     TINYINT(1)  NOT NULL DEFAULT 1,
    data_events_enabled     TINYINT(1)  NOT NULL DEFAULT 1,
    authz_events_enabled    TINYINT(1)  NOT NULL DEFAULT 1,
    system_events_enabled   TINYINT(1)  NOT NULL DEFAULT 1,

    -- Storage config
    storage_type            VARCHAR(50) NOT NULL DEFAULT 'database',
    storage_table_name      VARCHAR(255) DEFAULT 'audit_log',
    storage_retention_days  INT         NOT NULL DEFAULT 365,
    storage_archive_after   INT         NOT NULL DEFAULT 90,
    storage_archive_location VARCHAR(500),

    -- Filtering config
    exclude_users_json      JSON,
    exclude_endpoints_json  JSON,
    exclude_read_operations TINYINT(1)  NOT NULL DEFAULT 1,
    sensitive_fields_json   JSON,

    -- Format config
    fmt_timestamp_format    VARCHAR(100) DEFAULT 'yyyy-MM-dd''T''HH:mm:ss.SSS''Z''',
    fmt_include_request_id  TINYINT(1)  NOT NULL DEFAULT 1,
    fmt_include_session_id  TINYINT(1)  NOT NULL DEFAULT 1,
    fmt_include_correlation_id TINYINT(1) NOT NULL DEFAULT 1,

    -- Alerting master switch
    alerting_enabled    TINYINT(1)      NOT NULL DEFAULT 1,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_auditcfg_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_auditcfg (app_definition_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 24: swfaw_audit_event
-- Replaces: audit_logging_layer.json → auditEvents.*[].events[]
CREATE TABLE swfaw_audit_event (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    audit_config_id     BIGINT UNSIGNED NOT NULL,

    category            VARCHAR(50)     NOT NULL,
    event_type          VARCHAR(100)    NOT NULL,
    log_level           VARCHAR(20)     NOT NULL DEFAULT 'INFO',
    message_template    TEXT            NOT NULL,

    include_user_agent      TINYINT(1)  DEFAULT 0,
    include_location        TINYINT(1)  DEFAULT 0,
    include_entity_data     TINYINT(1)  DEFAULT 0,
    include_changes         TINYINT(1)  DEFAULT 0,
    include_reason          TINYINT(1)  DEFAULT 0,

    entities_json           JSON,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audevt_cfg
        FOREIGN KEY (audit_config_id) REFERENCES swfaw_audit_config(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_audevt (audit_config_id, category, event_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 25: swfaw_audit_alert
-- Replaces: audit_logging_layer.json → alerting.alerts[]
CREATE TABLE swfaw_audit_alert (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    audit_config_id     BIGINT UNSIGNED NOT NULL,

    event_type          VARCHAR(100)    NOT NULL,
    threshold           INT             NOT NULL,
    time_window_minutes INT             NOT NULL,
    action              VARCHAR(50)     NOT NULL DEFAULT 'SEND_EMAIL',
    recipients_json     JSON            NOT NULL,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_audalert_cfg
        FOREIGN KEY (audit_config_id) REFERENCES swfaw_audit_config(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_audalert (audit_config_id, event_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- --------------------------------------------------------------------------
-- 4d: Authorization & Groups
-- --------------------------------------------------------------------------

-- Table 26: swfaw_authorization_config
-- Replaces: authorization_layer.json (top-level settings)
CREATE TABLE swfaw_authorization_config (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    authz_enabled           TINYINT(1)  NOT NULL DEFAULT 1,
    access_control_model    VARCHAR(50) NOT NULL DEFAULT 'document-based',

    -- Access control types and document group types as JSON
    access_controls_json    JSON        NOT NULL,
    document_group_types_json JSON      NOT NULL,

    -- Super user settings
    super_user_enabled              TINYINT(1) NOT NULL DEFAULT 1,
    super_user_bypass_all           TINYINT(1) NOT NULL DEFAULT 1,
    super_user_require_justification TINYINT(1) NOT NULL DEFAULT 1,
    super_user_justification_min_len INT       NOT NULL DEFAULT 10,
    super_user_log_all_actions      TINYINT(1) NOT NULL DEFAULT 1,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_authzcfg_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_authzcfg (app_definition_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 27: swfaw_entity_access_control
-- Replaces: authorization_layer.json → entityAccessControl[]
CREATE TABLE swfaw_entity_access_control (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    authorization_config_id BIGINT UNSIGNED NOT NULL,

    entity_name         VARCHAR(255)    NOT NULL,
    table_name          VARCHAR(255)    NOT NULL,
    is_root_entity      TINYINT(1)      NOT NULL DEFAULT 0,

    enable_access_control   TINYINT(1)  NOT NULL DEFAULT 1,
    check_on_create         TINYINT(1)  NOT NULL DEFAULT 1,
    check_on_read           TINYINT(1)  NOT NULL DEFAULT 1,
    check_on_update         TINYINT(1)  NOT NULL DEFAULT 1,
    check_on_delete         TINYINT(1)  NOT NULL DEFAULT 1,

    custom_rules_json       JSON,

    CONSTRAINT fk_entac_authz
        FOREIGN KEY (authorization_config_id)
        REFERENCES swfaw_authorization_config(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_entac (authorization_config_id, entity_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 28: swfaw_group_config
-- Replaces: group_definition_layer.json → groupManagement + ownerEnrollmentDefaults
CREATE TABLE swfaw_group_config (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Group management
    allow_runtime_creation      TINYINT(1) NOT NULL DEFAULT 0,
    allow_runtime_deletion      TINYINT(1) NOT NULL DEFAULT 0,
    admin_can_grant_membership  TINYINT(1) NOT NULL DEFAULT 1,
    admin_can_revoke_membership TINYINT(1) NOT NULL DEFAULT 1,
    admin_group_name            VARCHAR(255) DEFAULT 'Administrators',

    -- Owner enrollment defaults
    ownership_check         VARCHAR(50) DEFAULT 'CREATOR_RECORDS',
    max_records_per_user    INT,
    allow_enroll            TINYINT(1)  NOT NULL DEFAULT 0,
    allow_unenroll          TINYINT(1)  NOT NULL DEFAULT 0,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_grpcfg_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_grpcfg (app_definition_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 29: swfaw_group_definition
-- Replaces: group_definition_layer.json → systemGroups[] + tableAccessGroups[]
CREATE TABLE swfaw_group_definition (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Group identity
    group_name          VARCHAR(255)    NOT NULL,
    description         TEXT,
    group_category      VARCHAR(50)     NOT NULL,

    -- System group fields (NULL for TABLE_ACCESS groups)
    is_super_group      TINYINT(1)      NOT NULL DEFAULT 0,
    is_default_group    TINYINT(1)      NOT NULL DEFAULT 0,
    auto_assign_new_users TINYINT(1)    NOT NULL DEFAULT 0,

    -- Table access group fields (NULL for SYSTEM groups)
    table_name          VARCHAR(255),
    entity_name         VARCHAR(255),
    group_type          VARCHAR(50),
    access_level        VARCHAR(50),

    -- Permissions (NULL for SYSTEM groups)
    allow_read          TINYINT(1)      DEFAULT NULL,
    allow_create        TINYINT(1)      DEFAULT NULL,
    allow_update        TINYINT(1)      DEFAULT NULL,
    allow_delete        TINYINT(1)      DEFAULT NULL,
    allow_grant_access  TINYINT(1)      DEFAULT NULL,
    allow_export        TINYINT(1)      DEFAULT NULL,
    allow_share         TINYINT(1)      DEFAULT NULL,
    allow_audit         TINYINT(1)      DEFAULT NULL,

    sort_order          INT             NOT NULL DEFAULT 0,

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_grpdef_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_grpdef (app_definition_id, group_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- Table 30: swfaw_custom_query_template
-- Replaces: custom_queries_layer.json → queries[]
CREATE TABLE swfaw_custom_query_template (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    query_name          VARCHAR(255)    NOT NULL,
    description         TEXT,
    table_name          VARCHAR(255)    NOT NULL,
    conditions_json     JSON            NOT NULL,
    logic               VARCHAR(10)     NOT NULL DEFAULT 'AND',

    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_cqtpl_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_cqtpl (app_definition_id, query_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
-- Total: 30 tables
--
-- Tier 1 - Foundation (2):
--   1. swfaw_app_definition
--   2. swfaw_entity
--
-- Tier 2 - Per-Entity Layers (7):
--   3. swfaw_relationship
--   4. swfaw_entity_layer
--   5. swfaw_entity_layer_field
--   6. swfaw_repository_layer
--   7. swfaw_service_layer
--   8. swfaw_controller_layer
--   9. swfaw_dto_layer
--
-- Tier 3 - Query & Filter Layers (5):
--   10. swfaw_query
--   11. swfaw_query_join
--   12. swfaw_query_parameter
--   13. swfaw_filter
--   14. swfaw_filter_field
--
-- Tier 4 - Application-Wide Layers (16):
--   15. swfaw_security_config
--   16. swfaw_security_oauth2_provider
--   17. swfaw_security_cors
--   18. swfaw_security_public_endpoint
--   19. swfaw_app_config
--   20. swfaw_exception_config
--   21. swfaw_exception_definition
--   22. swfaw_exception_message
--   23. swfaw_audit_config
--   24. swfaw_audit_event
--   25. swfaw_audit_alert
--   26. swfaw_authorization_config
--   27. swfaw_entity_access_control
--   28. swfaw_group_config
--   29. swfaw_group_definition
--   30. swfaw_custom_query_template
-- ============================================================================
