# DB Manager

MySQL database management tool — create, drop, list, setup, execute SQL files, and run JSON-defined queries.

Default connection: `localhost:3306`, `root`/`password` (Docker MySQL).

## Usage

```bash
py db_manager/db_manager.py <command> [args]
```

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `create` | Create a database | `create my_db [--charset utf8mb4] [--collation utf8mb4_unicode_ci]` |
| `drop` | Drop a database | `drop my_db [--force]` |
| `list` | List all databases | `list` |
| `setup` | Create DB + execute all SQL schemas | `setup my_db [--app-dir <webflux_app>] [--skip-auth] [--skip-activity] [--skip-business]` |
| `execute` | Execute a SQL file against a database | `execute my_db --file path/to/file.sql` |
| `query` | Run a JSON-defined SELECT query | `query my_db --json '<json>'` |

## Global Options

| Option | Default | Description |
|--------|---------|-------------|
| `--host` | localhost | MySQL host |
| `--port` | 3306 | MySQL port |
| `--user` | root | MySQL user |
| `--password` | password | MySQL password |

## Setup Command

`setup` creates the database and executes SQL schemas in order:

1. Business tables from `mysql_database_design/<db_name>.sql`
2. Auth schema from `<webflux_app>/auth-schema.sql`
3. Activity tracking from `<webflux_app>/activity-tracking-schema.sql`

Each step can be skipped with `--skip-business`, `--skip-auth`, `--skip-activity`.

If `--app-dir` is not specified, it looks for `generated_application/current_application/webflux_app/` or the latest generated app folder.

```bash
# Full setup
py db_manager/db_manager.py setup ems_recruitment_portal

# Skip auth and activity schemas
py db_manager/db_manager.py setup ems_recruitment_portal --skip-auth --skip-activity

# Point to specific webflux_app
py db_manager/db_manager.py setup ems_recruitment_portal --app-dir generated_application/my_app/webflux_app
```

## Query Command

Runs safe, parameterized SELECT queries defined as JSON. No raw SQL — the tool builds the query from structured input.

```bash
py db_manager/db_manager.py query ems_recruitment_portal --json '{"table":"auth_user","columns":["username","email"],"where":{"is_active":1},"limit":10}'
```

### Query JSON Format

```json
{
  "table": "auth_user",
  "columns": ["username", {"col": "password_hash", "fn": "LENGTH", "alias": "pwd_len"}],
  "where": {"is_active": 1, "username": {"fn": "UPPER", "value": "JAMES29"}},
  "orderBy": "username",
  "limit": 10
}
```

### Column Specs

| Format | Example | SQL Output |
|--------|---------|------------|
| String | `"username"` | `` `username` `` |
| Wildcard | `"*"` | `*` |
| With function | `{"col": "password_hash", "fn": "LENGTH"}` | `LENGTH(\`password_hash\`)` |
| With alias | `{"col": "password_hash", "fn": "LENGTH", "alias": "pwd_len"}` | `LENGTH(\`password_hash\`) AS \`pwd_len\`` |

### Where Clause Specs

| Format | Example | SQL Output |
|--------|---------|------------|
| Simple equality | `{"username": "james29"}` | `` WHERE `username` = %s `` |
| NULL check | `{"email": null}` | `` WHERE `email` IS NULL `` |
| With operator | `{"age": {"op": ">", "value": 18}}` | `` WHERE `age` > %s `` |
| With function | `{"name": {"fn": "LOWER", "op": "LIKE", "value": "%john%"}}` | `` WHERE LOWER(`name`) LIKE %s `` |
| IN list | `{"status": {"op": "IN", "value": ["active", "pending"]}}` | `` WHERE `status` IN (%s, %s) `` |

### Allowed Functions

`LENGTH`, `UPPER`, `LOWER`, `TRIM`, `CONCAT`, `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `ABS`, `ROUND`, `NOW`, `DATE`, `COALESCE`, `IFNULL`, `IF`, `HEX`, `MD5`, `SHA1`, `SHA2`

### Allowed Operators

`=`, `!=`, `<>`, `<`, `>`, `<=`, `>=`, `LIKE`, `NOT LIKE`, `IN`, `NOT IN`, `IS`, `IS NOT`

## Dependencies

```bash
pip install mysql-connector-python
```
