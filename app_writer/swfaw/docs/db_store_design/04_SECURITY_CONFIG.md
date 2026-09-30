# Tier 4a: Security Configuration Tables

These tables store the security layer configuration — JWT, OAuth2, password
policy, session management, CORS, CSRF, and rate limiting.

The `security_layer.json` is the most deeply nested JSON file. We split it
into 4 tables to balance normalization with practicality.

---

## Table 15: `swfaw_security_config`

**Replaces:** `security_layer.json` (core settings, excluding OAuth2 providers,
CORS details, and public endpoints)

```sql
CREATE TABLE swfaw_security_config (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- JWT config (from security_layer.json → jwt)
    jwt_enabled         TINYINT(1)      NOT NULL DEFAULT 1,
    jwt_secret          VARCHAR(500)    NOT NULL
                        DEFAULT 'your-secret-key-change-in-production-min-256-bits',
    jwt_expiration      BIGINT          NOT NULL DEFAULT 86400000,
    jwt_expiration_unit VARCHAR(20)     NOT NULL DEFAULT 'milliseconds',
    jwt_issuer          VARCHAR(255),
    jwt_audience        VARCHAR(255),
    jwt_algorithm       VARCHAR(20)     NOT NULL DEFAULT 'HS256',

    -- Refresh token (from jwt.refreshToken)
    refresh_token_enabled    TINYINT(1) NOT NULL DEFAULT 1,
    refresh_token_expiration BIGINT     NOT NULL DEFAULT 604800000,
    refresh_token_exp_unit   VARCHAR(20) NOT NULL DEFAULT 'milliseconds',

    -- Password policy (from security_layer.json → passwordPolicy)
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

    -- Session management (from security_layer.json → sessionManagement)
    session_max_concurrent  INT         NOT NULL DEFAULT 3,
    session_timeout         INT         NOT NULL DEFAULT 1800,
    session_timeout_unit    VARCHAR(20) NOT NULL DEFAULT 'seconds',

    -- CSRF config (from security_layer.json → csrf)
    csrf_enabled        TINYINT(1)      NOT NULL DEFAULT 0,
    csrf_cookie_name    VARCHAR(100)    DEFAULT 'XSRF-TOKEN',
    csrf_header_name    VARCHAR(100)    DEFAULT 'X-XSRF-TOKEN',

    -- Rate limiting (from security_layer.json → rateLimiting)
    rate_limit_enabled          TINYINT(1) NOT NULL DEFAULT 1,
    rate_limit_default_per_min  INT        NOT NULL DEFAULT 60,
    rate_limit_login_max        INT        NOT NULL DEFAULT 5,
    rate_limit_lockout_minutes  INT        NOT NULL DEFAULT 15,

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_secconfig_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_secconfig (app_definition_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Design Decisions

- **All scalar security settings in one table** — this is always a 1:1 relationship
  with the app definition. One row per app, ~30 columns. Wide but simple.
- **Password policy flattened** — every field is a simple scalar, always present.
- **Session, CSRF, rate limiting flattened** — same reasoning.
- **OAuth2 providers, CORS, and public endpoints** are in separate tables because
  they're variable-length lists.

---

## Table 16: `swfaw_security_oauth2_provider`

**Replaces:** `security_layer.json → oauth2.providers[]`

```sql
CREATE TABLE swfaw_security_oauth2_provider (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    security_config_id  BIGINT UNSIGNED NOT NULL,

    -- OAuth2 master switch lives on security_config, but we also track
    -- whether OAuth2 is enabled at the provider level
    provider_name       VARCHAR(100)    NOT NULL,  -- google, github, etc.
    client_id           VARCHAR(500)    NOT NULL,
    client_secret       VARCHAR(500)    NOT NULL,
    redirect_uri        VARCHAR(500)    NOT NULL,
    scopes_json         JSON            NOT NULL,  -- Array of scope strings

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_oauth2_sec
        FOREIGN KEY (security_config_id) REFERENCES swfaw_security_config(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_oauth2_provider (security_config_id, provider_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Note: We also need the OAuth2 enabled flag on the security_config table.
Adding it:

```sql
-- Add to swfaw_security_config (between jwt and password sections):
    oauth2_enabled      TINYINT(1)      NOT NULL DEFAULT 0,
```

---

## Table 17: `swfaw_security_cors`

**Replaces:** `security_layer.json → cors`

```sql
CREATE TABLE swfaw_security_cors (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    security_config_id  BIGINT UNSIGNED NOT NULL,

    -- CORS config
    cors_enabled        TINYINT(1)      NOT NULL DEFAULT 1,
    allowed_origins_json    JSON,       -- ["http://localhost:3000", ...]
    allowed_methods_json    JSON,       -- ["GET", "POST", ...]
    allowed_headers_json    JSON,       -- ["Authorization", "Content-Type", ...]
    exposed_headers_json    JSON,       -- ["Authorization"]
    allow_credentials       TINYINT(1)  NOT NULL DEFAULT 1,
    max_age                 INT         NOT NULL DEFAULT 3600,

    CONSTRAINT fk_cors_sec
        FOREIGN KEY (security_config_id) REFERENCES swfaw_security_config(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_cors (security_config_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Design Decision

- **Separate table rather than columns on security_config** — CORS has 7 fields
  including 4 JSON arrays. Keeping it separate avoids making the already-wide
  security_config table even wider, and CORS is conceptually a distinct concern.

---

## Table 18: `swfaw_security_public_endpoint`

**Replaces:** `security_layer.json → publicEndpoints[]`

```sql
CREATE TABLE swfaw_security_public_endpoint (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    security_config_id  BIGINT UNSIGNED NOT NULL,

    -- Endpoint pattern
    endpoint_pattern    VARCHAR(500)    NOT NULL,  -- e.g. "/api/v1/auth/login"

    -- Ordering
    sort_order          INT             NOT NULL DEFAULT 0,

    CONSTRAINT fk_pubep_sec
        FOREIGN KEY (security_config_id) REFERENCES swfaw_security_config(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_pubep (security_config_id, endpoint_pattern)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Design Decision

- **Normalized rather than JSON array** — public endpoints are frequently
  queried ("is this path public?") and modified individually. A separate
  table makes CRUD operations cleaner than JSON array manipulation.
