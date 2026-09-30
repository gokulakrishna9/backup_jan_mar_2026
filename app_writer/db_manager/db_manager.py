"""Database Manager — create, drop, list, and setup MySQL databases.

Default connection: mysql on Docker port 3306, root/password.

Setup reads SQL from:
  - mysql_database_design/<db_name>.sql  (business tables)
  - generated_application/current_application/webflux_app/auth-schema.sql
  - generated_application/current_application/webflux_app/activity-tracking-schema.sql
"""

import argparse
import os
import sys

try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    print("❌ mysql-connector-python is required. Install with: pip install mysql-connector-python")
    sys.exit(1)


DEFAULT_HOST = "localhost"
DEFAULT_PORT = 3306
DEFAULT_USER = "root"
DEFAULT_PASSWORD = "password"

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUSINESS_SQL_DIR = os.path.join(WORKSPACE_ROOT, "mysql_database_design")
GENERATED_APP_DIR = os.path.join(WORKSPACE_ROOT, "generated_application")


def _connect(host: str, port: int, user: str, password: str, database: str = None):
    """Connect to MySQL server."""
    try:
        kwargs = dict(host=host, port=port, user=user, password=password)
        if database:
            kwargs["database"] = database
        conn = mysql.connector.connect(**kwargs)
        return conn
    except Error as e:
        print(f"❌ Connection failed: {e}")
        sys.exit(1)


def _execute_sql_file(cursor, filepath: str, db_name: str):
    """Read and execute a SQL file, statement by statement."""
    if not os.path.isfile(filepath):
        print(f"  ⚠️  Skipped (not found): {filepath}")
        return 0

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split on semicolons, filter empty
    statements = [s.strip() for s in content.split(";") if s.strip()]
    executed = 0
    for stmt in statements:
        # Skip USE statements — we already selected the database
        if stmt.upper().startswith("USE "):
            continue
        # Skip CREATE DATABASE — we already created it
        if "CREATE DATABASE" in stmt.upper():
            continue
        try:
            cursor.execute(stmt)
            executed += 1
        except Error as e:
            # Non-fatal: log and continue (e.g. duplicate key on INSERT)
            if e.errno in (1062, 1065):  # duplicate entry, empty query
                continue
            print(f"  ⚠️  Statement warning: {e}")
            executed += 1
    return executed


def _resolve_app_dir(app_dir: str = None) -> str:
    """Resolve the webflux_app directory. Uses current_application if not specified."""
    if app_dir:
        return app_dir

    current = os.path.join(GENERATED_APP_DIR, "current_application", "webflux_app")
    if os.path.isdir(current):
        return current

    # Fallback: find the latest generated app folder
    if os.path.isdir(GENERATED_APP_DIR):
        folders = sorted(
            [d for d in os.listdir(GENERATED_APP_DIR)
             if os.path.isdir(os.path.join(GENERATED_APP_DIR, d)) and d != "current_application"],
            reverse=True
        )
        if folders:
            resolved = os.path.join(GENERATED_APP_DIR, folders[0], "webflux_app")
            if os.path.isdir(resolved):
                return resolved

    return current  # return default path even if missing, will show clear error


def create_database(name: str, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT,
                    user: str = DEFAULT_USER, password: str = DEFAULT_PASSWORD,
                    charset: str = "utf8mb4", collation: str = "utf8mb4_unicode_ci"):
    """Create a database if it doesn't already exist."""
    conn = _connect(host, port, user, password)
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{name}` "
                       f"CHARACTER SET {charset} COLLATE {collation}")
        print(f"✅ Database '{name}' created (charset={charset}, collation={collation})")
    except Error as e:
        print(f"❌ Failed to create database '{name}': {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()


def drop_database(name: str, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT,
                  user: str = DEFAULT_USER, password: str = DEFAULT_PASSWORD,
                  force: bool = False):
    """Drop a database. Prompts for confirmation unless --force is used."""
    if not force:
        confirm = input(f"⚠️  Drop database '{name}'? This cannot be undone. [y/N]: ").strip().lower()
        if confirm != "y":
            print("Cancelled.")
            return

    conn = _connect(host, port, user, password)
    cursor = conn.cursor()
    try:
        cursor.execute(f"DROP DATABASE IF EXISTS `{name}`")
        print(f"✅ Database '{name}' dropped")
    except Error as e:
        print(f"❌ Failed to drop database '{name}': {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()


def list_databases(host: str = DEFAULT_HOST, port: int = DEFAULT_PORT,
                   user: str = DEFAULT_USER, password: str = DEFAULT_PASSWORD):
    """List all databases on the server."""
    conn = _connect(host, port, user, password)
    cursor = conn.cursor()
    try:
        cursor.execute("SHOW DATABASES")
        dbs = [row[0] for row in cursor.fetchall()]
        print(f"Databases ({len(dbs)}):")
        for db in dbs:
            print(f"  {db}")
    except Error as e:
        print(f"❌ Failed to list databases: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()


def setup_database(name: str, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT,
                   user: str = DEFAULT_USER, password: str = DEFAULT_PASSWORD,
                   app_dir: str = None, skip_auth: bool = False,
                   skip_activity: bool = False, skip_business: bool = False):
    """Create database and execute all SQL schemas.

    Order: business tables → auth schema → activity tracking schema.

    Args:
        name: Database name (must match the .sql filename in mysql_database_design/)
        app_dir: Path to webflux_app/ dir. Defaults to current_application or latest generated.
        skip_auth: Skip auth-schema.sql
        skip_activity: Skip activity-tracking-schema.sql
        skip_business: Skip business schema from mysql_database_design/
    """
    # 1. Create database
    conn = _connect(host, port, user, password)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{name}` "
                       f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✅ Database '{name}' created/verified")
    except Error as e:
        print(f"❌ Failed to create database: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()

    # 2. Connect to the specific database
    conn = _connect(host, port, user, password, database=name)
    cursor = conn.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    total = 0

    try:
        # Business tables
        if not skip_business:
            business_sql = os.path.join(BUSINESS_SQL_DIR, f"{name}.sql")
            print(f"\n📄 Business schema: {business_sql}")
            count = _execute_sql_file(cursor, business_sql, name)
            print(f"   Executed {count} statements")
            total += count
            conn.commit()

        # Auth schema
        webflux_dir = _resolve_app_dir(app_dir)
        if not skip_auth:
            auth_sql = os.path.join(webflux_dir, "auth-schema.sql")
            print(f"\n📄 Auth schema: {auth_sql}")
            count = _execute_sql_file(cursor, auth_sql, name)
            print(f"   Executed {count} statements")
            total += count
            conn.commit()

        # Activity tracking schema
        if not skip_activity:
            activity_sql = os.path.join(webflux_dir, "activity-tracking-schema.sql")
            print(f"\n📄 Activity tracking schema: {activity_sql}")
            count = _execute_sql_file(cursor, activity_sql, name)
            print(f"   Executed {count} statements")
            total += count
            conn.commit()

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        print(f"\n✅ Setup complete — {total} total statements executed on '{name}'")

    except Error as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()


def execute_sql_file(name: str, filepath: str, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT,
                     user: str = DEFAULT_USER, password: str = DEFAULT_PASSWORD):
    """Execute a SQL file against a specific database.

    Args:
        name: Database name to execute against.
        filepath: Path to the SQL file.
    """
    if not os.path.isfile(filepath):
        print(f"❌ File not found: {filepath}")
        sys.exit(1)

    conn = _connect(host, port, user, password, database=name)
    cursor = conn.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")

    try:
        print(f"📄 Executing: {filepath} → database '{name}'")
        count = _execute_sql_file(cursor, filepath, name)
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        print(f"✅ Done — {count} statements executed")
    except Error as e:
        print(f"❌ Execution failed: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()


# --- Allowed SQL functions (whitelist for safety) ---
ALLOWED_FUNCTIONS = {
    "LENGTH", "UPPER", "LOWER", "TRIM", "LTRIM", "RTRIM",
    "LEFT", "RIGHT", "SUBSTRING", "CONCAT",
    "COUNT", "SUM", "AVG", "MIN", "MAX",
    "ABS", "ROUND", "CEIL", "FLOOR",
    "NOW", "DATE", "YEAR", "MONTH", "DAY",
    "COALESCE", "IFNULL", "IF",
    "HEX", "UNHEX", "MD5", "SHA1", "SHA2",
}


def _build_select_column(col_spec):
    """Build a SELECT column expression from a string or dict.
    
    String: "username" → `username`
    Dict: {"col": "password_hash", "fn": "LENGTH"} → LENGTH(`password_hash`)
    Dict with alias: {"col": "password_hash", "fn": "LENGTH", "alias": "pwd_len"} → LENGTH(`password_hash`) AS `pwd_len`
    """
    if isinstance(col_spec, str):
        if col_spec == "*":
            return "*"
        return f"`{col_spec}`"
    
    col = col_spec["col"]
    fn = col_spec.get("fn")
    alias = col_spec.get("alias")
    
    expr = f"`{col}`"
    if fn:
        fn_upper = fn.upper()
        if fn_upper not in ALLOWED_FUNCTIONS:
            raise ValueError(f"Function '{fn}' not allowed. Allowed: {', '.join(sorted(ALLOWED_FUNCTIONS))}")
        expr = f"{fn_upper}({expr})"
    
    if alias:
        expr += f" AS `{alias}`"
    
    return expr


def _build_where_clause(where: dict):
    """Build WHERE clause and params from a dict.
    
    Simple: {"username": "james29"} → WHERE `username` = %s
    With function: {"username": {"fn": "UPPER", "value": "JAMES29"}} → WHERE UPPER(`username`) = %s
    With operator: {"age": {"op": ">", "value": 18}} → WHERE `age` > %s
    With both: {"name": {"fn": "LOWER", "op": "LIKE", "value": "%john%"}} → WHERE LOWER(`name`) LIKE %s
    NULL check: {"email": null} → WHERE `email` IS NULL
    """
    if not where:
        return "", []
    
    clauses = []
    params = []
    allowed_ops = {"=", "!=", "<>", "<", ">", "<=", ">=", "LIKE", "NOT LIKE", "IN", "NOT IN", "IS", "IS NOT"}
    
    for col, spec in where.items():
        if spec is None:
            clauses.append(f"`{col}` IS NULL")
        elif isinstance(spec, dict):
            fn = spec.get("fn")
            op = spec.get("op", "=").upper()
            value = spec.get("value")
            
            if op not in allowed_ops:
                raise ValueError(f"Operator '{op}' not allowed. Allowed: {', '.join(sorted(allowed_ops))}")
            
            expr = f"`{col}`"
            if fn:
                fn_upper = fn.upper()
                if fn_upper not in ALLOWED_FUNCTIONS:
                    raise ValueError(f"Function '{fn}' not allowed.")
                expr = f"{fn_upper}({expr})"
            
            if value is None:
                clauses.append(f"{expr} IS NULL")
            elif op in ("IN", "NOT IN") and isinstance(value, list):
                placeholders = ", ".join(["%s"] * len(value))
                clauses.append(f"{expr} {op} ({placeholders})")
                params.extend(value)
            else:
                clauses.append(f"{expr} {op} %s")
                params.append(value)
        else:
            clauses.append(f"`{col}` = %s")
            params.append(spec)
    
    return " WHERE " + " AND ".join(clauses), params


def query_database(name: str, query_json: str, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT,
                   user: str = DEFAULT_USER, password: str = DEFAULT_PASSWORD):
    """Run a JSON-defined query and print results.
    
    JSON format:
        {
            "table": "auth_user",
            "columns": ["username", {"col": "password_hash", "fn": "LENGTH", "alias": "pwd_len"}],
            "where": {"is_active": 1, "username": {"fn": "UPPER", "value": "JAMES29"}},
            "orderBy": "username",
            "limit": 10
        }
    """
    import json
    
    try:
        q = json.loads(query_json)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {e}")
        sys.exit(1)
    
    table = q.get("table")
    if not table:
        print("❌ 'table' is required in query JSON")
        sys.exit(1)
    
    # Build SELECT columns
    columns = q.get("columns", ["*"])
    select_parts = [_build_select_column(c) for c in columns]
    select_clause = ", ".join(select_parts)
    
    # Build WHERE
    where_clause, params = _build_where_clause(q.get("where", {}))
    
    # Build ORDER BY
    order_by = ""
    if "orderBy" in q:
        ob = q["orderBy"]
        if isinstance(ob, str):
            order_by = f" ORDER BY `{ob}`"
        elif isinstance(ob, dict):
            direction = ob.get("dir", "ASC").upper()
            if direction not in ("ASC", "DESC"):
                direction = "ASC"
            order_by = f" ORDER BY `{ob['col']}` {direction}"
    
    # Build LIMIT
    limit = ""
    if "limit" in q:
        limit = f" LIMIT {int(q['limit'])}"
    
    sql = f"SELECT {select_clause} FROM `{table}`{where_clause}{order_by}{limit}"
    
    conn = _connect(host, port, user, password, database=name)
    cursor = conn.cursor()
    
    try:
        cursor.execute(sql, params)
        
        if cursor.description:
            col_names = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            
            if not rows:
                print("(no rows)")
                return
            
            # Calculate column widths (cap at 60)
            widths = [len(c) for c in col_names]
            str_rows = []
            for row in rows:
                str_row = [str(v) if v is not None else "NULL" for v in row]
                str_rows.append(str_row)
                for i, v in enumerate(str_row):
                    widths[i] = max(widths[i], min(len(v), 60))
            
            # Print header
            header = " | ".join(c.ljust(widths[i]) for i, c in enumerate(col_names))
            print(header)
            print("-+-".join("-" * w for w in widths))
            
            # Print rows
            for str_row in str_rows:
                line = " | ".join(str_row[i][:60].ljust(widths[i]) for i in range(len(col_names)))
                print(line)
            
            print(f"\n({len(rows)} row{'s' if len(rows) != 1 else ''})")
        else:
            print("(no results)")
    except Error as e:
        print(f"❌ Query failed: {e}")
        sys.exit(1)
    finally:
        cursor.close()
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="MySQL Database Manager — create, drop, list, setup databases")
    parser.add_argument("--host", default=DEFAULT_HOST, help=f"MySQL host (default: {DEFAULT_HOST})")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"MySQL port (default: {DEFAULT_PORT})")
    parser.add_argument("--user", default=DEFAULT_USER, help=f"MySQL user (default: {DEFAULT_USER})")
    parser.add_argument("--password", default=DEFAULT_PASSWORD, help=f"MySQL password (default: {DEFAULT_PASSWORD})")

    sub = parser.add_subparsers(dest="command")

    # create
    p_create = sub.add_parser("create", help="Create a database")
    p_create.add_argument("name", help="Database name")
    p_create.add_argument("--charset", default="utf8mb4", help="Character set (default: utf8mb4)")
    p_create.add_argument("--collation", default="utf8mb4_unicode_ci", help="Collation (default: utf8mb4_unicode_ci)")

    # drop
    p_drop = sub.add_parser("drop", help="Drop a database")
    p_drop.add_argument("name", help="Database name")
    p_drop.add_argument("--force", action="store_true", help="Skip confirmation prompt")

    # list
    sub.add_parser("list", help="List all databases")

    # setup
    p_setup = sub.add_parser("setup", help="Create database and execute all SQL schemas")
    p_setup.add_argument("name", help="Database name (must match .sql filename in mysql_database_design/)")
    p_setup.add_argument("--app-dir", default=None, help="Path to webflux_app/ (default: current_application or latest)")
    p_setup.add_argument("--skip-auth", action="store_true", help="Skip auth-schema.sql")
    p_setup.add_argument("--skip-activity", action="store_true", help="Skip activity-tracking-schema.sql")
    p_setup.add_argument("--skip-business", action="store_true", help="Skip business schema")

    # execute
    p_exec = sub.add_parser("execute", help="Execute a SQL file against a database")
    p_exec.add_argument("name", help="Database name")
    p_exec.add_argument("--file", required=True, help="Path to SQL file to execute")

    # query
    p_query = sub.add_parser("query", help="Run a JSON-defined SELECT query against a database")
    p_query.add_argument("name", help="Database name")
    p_query.add_argument("--json", required=True, dest="query_json",
                         help='JSON query: {"table":"x","columns":[...],"where":{...},"orderBy":"col","limit":N}')

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "create":
        create_database(args.name, args.host, args.port, args.user, args.password,
                        args.charset, args.collation)
    elif args.command == "drop":
        drop_database(args.name, args.host, args.port, args.user, args.password, args.force)
    elif args.command == "list":
        list_databases(args.host, args.port, args.user, args.password)
    elif args.command == "setup":
        setup_database(args.name, args.host, args.port, args.user, args.password,
                       args.app_dir, args.skip_auth, args.skip_activity, args.skip_business)
    elif args.command == "execute":
        execute_sql_file(args.name, args.file, args.host, args.port, args.user, args.password)
    elif args.command == "query":
        query_database(args.name, args.query_json, args.host, args.port, args.user, args.password)


if __name__ == "__main__":
    main()
