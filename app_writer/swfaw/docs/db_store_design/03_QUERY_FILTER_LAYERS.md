# Tier 3: Query & Filter Layer Tables

These tables store the custom R2DBC query definitions and entity filter
configurations introduced in v2.4.

---

## Table 10: `swfaw_query`

**Replaces:** `query_layer.json → queries[EntityName][]`

Each row is one custom query for a specific entity. The query layer is the
most complex per-entity structure, so joins and parameters are normalized
into their own tables.

```sql
CREATE TABLE swfaw_query (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Query identity
    entity_name         VARCHAR(255)    NOT NULL,
    query_name          VARCHAR(255)    NOT NULL,
    description         TEXT,

    -- Query structure
    return_type         VARCHAR(255)    NOT NULL,
    select_fields_json  JSON            NOT NULL,  -- Array of SELECT field strings
    from_clause         VARCHAR(500)    NOT NULL,   -- e.g. "ems_user e"
    where_clauses_json  JSON,                       -- Array of WHERE condition strings
    group_by_json       JSON,                       -- Array of GROUP BY field strings
    having_json         JSON,                       -- Array of HAVING condition strings
    order_by_json       JSON,                       -- Array of ORDER BY strings

    -- Behavior
    pagination          TINYINT(1)      NOT NULL DEFAULT 1,

    -- Authorization
    authz_enabled       TINYINT(1)      NOT NULL DEFAULT 1,
    authz_document_field VARCHAR(255),

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_query_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_query (app_definition_id, entity_name, query_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Design Decisions

- **SELECT, WHERE, GROUP BY, HAVING, ORDER BY as JSON arrays** — these are
  string lists that are always loaded together. No benefit to normalizing.
- **Joins and parameters normalized** into separate tables (below) because:
  - Joins have structured fields (type, table, alias, on-condition)
  - Parameters have typed fields (name, type, required, default)
  - Both are independently useful for validation and code generation

---

## Table 11: `swfaw_query_join`

**Replaces:** `query_layer.json → queries[Entity][].joins[]`

```sql
CREATE TABLE swfaw_query_join (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    query_id            BIGINT UNSIGNED NOT NULL,

    -- Join definition
    join_type           VARCHAR(20)     NOT NULL,  -- INNER, LEFT, RIGHT, FULL
    join_table          VARCHAR(255)    NOT NULL,
    join_alias          VARCHAR(100),
    join_condition      VARCHAR(500)    NOT NULL,   -- e.g. "u.id = ur.user_id"

    -- Ordering
    sort_order          INT             NOT NULL DEFAULT 0,

    CONSTRAINT fk_qjoin_query
        FOREIGN KEY (query_id) REFERENCES swfaw_query(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## Table 12: `swfaw_query_parameter`

**Replaces:** `query_layer.json → queries[Entity][].parameters[]`

```sql
CREATE TABLE swfaw_query_parameter (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    query_id            BIGINT UNSIGNED NOT NULL,

    -- Parameter definition
    param_name          VARCHAR(255)    NOT NULL,
    param_type          VARCHAR(100)    NOT NULL,  -- Java type: String, Integer, etc.
    is_required         TINYINT(1)      NOT NULL DEFAULT 1,
    default_value       VARCHAR(500),

    -- Ordering
    sort_order          INT             NOT NULL DEFAULT 0,

    CONSTRAINT fk_qparam_query
        FOREIGN KEY (query_id) REFERENCES swfaw_query(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_qparam (query_id, param_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## Table 13: `swfaw_filter`

**Replaces:** `filter_layer.json → filters[EntityName]`

One row per entity that has filter definitions.

```sql
CREATE TABLE swfaw_filter (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    app_definition_id   BIGINT UNSIGNED NOT NULL,

    -- Filter identity
    entity_name         VARCHAR(255)    NOT NULL,

    -- Housekeeping
    date_created        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_modified       DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
                        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_filter_app
        FOREIGN KEY (app_definition_id) REFERENCES swfaw_app_definition(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_filter (app_definition_id, entity_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## Table 14: `swfaw_filter_field`

**Replaces:** `filter_layer.json → filters[EntityName].fields[]`

Each row is one filterable field with its allowed operators.

```sql
CREATE TABLE swfaw_filter_field (
    id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    filter_id           BIGINT UNSIGNED NOT NULL,

    -- Field definition
    field_name          VARCHAR(255)    NOT NULL,
    field_type          VARCHAR(100)    NOT NULL,  -- Java type: String, Long, LocalDate, etc.

    -- Operators stored as JSON array
    -- e.g. ["equals", "contains", "startsWith", "endsWith", "in"]
    operators_json      JSON            NOT NULL,

    -- Ordering
    sort_order          INT             NOT NULL DEFAULT 0,

    CONSTRAINT fk_ffield_filter
        FOREIGN KEY (filter_id) REFERENCES swfaw_filter(id)
        ON DELETE CASCADE,
    UNIQUE KEY uk_ffield (filter_id, field_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Design Decisions

- **Operators as JSON array** rather than a junction table. Rationale:
  - Operators are a small fixed set (equals, contains, startsWith, etc.)
  - They're always loaded as a batch per field
  - A junction table (`swfaw_filter_field_operator`) would add a table with
    potentially 5000+ rows (100 entities × 10 fields × 5 operators) for
    very little query benefit
- **Filter split into header + fields** rather than one JSON blob per entity.
  This allows field-level queries like "find all String fields with contains operator".

### Operator Values Reference

| Operator | Applies To | SQL Equivalent |
|----------|-----------|----------------|
| `equals` | All types | `= ?` |
| `contains` | String | `LIKE '%?%'` |
| `startsWith` | String | `LIKE '?%'` |
| `endsWith` | String | `LIKE '%?'` |
| `greaterThan` | Numeric, Date | `> ?` |
| `lessThan` | Numeric, Date | `< ?` |
| `between` | Numeric, Date | `BETWEEN ? AND ?` |
| `in` | All types | `IN (?, ?, ...)` |
