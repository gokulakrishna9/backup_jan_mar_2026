"""Generic database layer manager — DB equivalent of LayerManager.

Provides get/set/update/delete/find/filter operations against any swfaw_ table
using table aliases (like LayerManager uses file aliases).

Includes MySQL JSON function support for searching/modifying JSON columns:
  - Predicate-based: use $ syntax in find/filter/get/exists/count/delete
  - Direct methods: json_extract, json_contains, json_search, json_value, etc.
"""

import json
from typing import Optional, Dict, Any, List, Union
from .db_connection import DbConnection


class DbLayerManager:
    """Generic CRUD on any swfaw_ table using table aliases.
    
    Mirrors the LayerManager API but operates on DB rows instead of JSON files.
    Table aliases map to actual table names, just like file aliases map to filenames.
    
    Usage:
        lm = DbLayerManager(db, app_id=1)
        
        # GET — read rows
        row = lm.get("security_config")
        rows = lm.get("entity_layer")
        
        # SET — update a single column on a matched row
        lm.set("security_config", "jwt_expiration", 7200000)
        
        # UPDATE — update multiple columns
        lm.update("security_config", {"jwt_expiration": 7200000, "jwt_issuer": "acme"})
        
        # DELETE — remove rows
        lm.delete("security_public_endpoint", {"endpoint_pattern": "/api/health"})
        
        # FIND — find one row matching criteria
        row = lm.find("entity_layer", {"table_name": "users"})
        
        # FILTER — find all rows matching criteria
        rows = lm.filter("dto_layer", {"entity_name": "users"})
        
        # EXISTS — check existence
        lm.exists("security_config")
        
        # JSON search in predicates ($ syntax — works in find/filter/get/exists/count/delete):
        #   "col$path"                → JSON_EXTRACT(col, path) = value
        #   "col$path$$contains"      → JSON_CONTAINS(col, value, path)
        #   "col$$contains"           → JSON_CONTAINS(col, value)
        #   "col$path$$exists"        → JSON_CONTAINS_PATH(col, 'one', path)
        #   "col$path$$type"          → JSON_TYPE(JSON_EXTRACT(col, path)) = value
        #   "col$path$$overlaps"      → JSON_OVERLAPS(JSON_EXTRACT(col, path), value)
        #   "col$path$$length"        → JSON_LENGTH(JSON_EXTRACT(col, path)) = value
        #
        # Direct MySQL JSON methods:
        #   json_extract, json_value, json_contains, json_contains_path,
        #   json_search, json_keys, json_length, json_overlaps, json_type,
        #   json_set, json_insert, json_replace, json_remove, json_array_append
    """

    # Alias → actual table name (without swfaw_ prefix for brevity)
    TABLE_ALIASES = {
        # Tier 1
        "app_definition":       "swfaw_app_definition",
        "entity":               "swfaw_entity",
        # Tier 2
        "relationship":         "swfaw_relationship",
        "entity_layer":         "swfaw_entity_layer",
        "entity_layer_field":   "swfaw_entity_layer_field",
        "repository_layer":     "swfaw_repository_layer",
        "service_layer":        "swfaw_service_layer",
        "controller_layer":     "swfaw_controller_layer",
        "dto_layer":            "swfaw_dto_layer",
        # Tier 3
        "query":                "swfaw_query",
        "query_join":           "swfaw_query_join",
        "query_parameter":      "swfaw_query_parameter",
        "filter":               "swfaw_filter",
        "filter_field":         "swfaw_filter_field",
        # Tier 4
        "security_config":      "swfaw_security_config",
        "security_oauth2":      "swfaw_security_oauth2_provider",
        "security_cors":        "swfaw_security_cors",
        "security_public_endpoint": "swfaw_security_public_endpoint",
        "app_config":           "swfaw_app_config",
        "exception_config":     "swfaw_exception_config",
        "exception_definition": "swfaw_exception_definition",
        "exception_message":    "swfaw_exception_message",
        "audit_config":         "swfaw_audit_config",
        "audit_event":          "swfaw_audit_event",
        "audit_alert":          "swfaw_audit_alert",
        "authorization_config": "swfaw_authorization_config",
        "entity_access_control":"swfaw_entity_access_control",
        "group_config":         "swfaw_group_config",
        "group_definition":     "swfaw_group_definition",
        "custom_query_template":"swfaw_custom_query_template",
    }

    # Tables that link to app_definition_id directly
    APP_LINKED_TABLES = {
        "swfaw_app_definition", "swfaw_entity", "swfaw_relationship",
        "swfaw_entity_layer", "swfaw_repository_layer", "swfaw_service_layer",
        "swfaw_controller_layer", "swfaw_dto_layer", "swfaw_query", "swfaw_filter",
        "swfaw_security_config", "swfaw_app_config", "swfaw_exception_config",
        "swfaw_exception_definition", "swfaw_exception_message",
        "swfaw_audit_config", "swfaw_authorization_config",
        "swfaw_group_config", "swfaw_group_definition",
        "swfaw_custom_query_template",
    }

    # Tables that link through a parent config table (not directly to app_definition)
    CHILD_TABLES = {
        "swfaw_entity_layer_field":       ("entity_layer_id",  "swfaw_entity_layer"),
        "swfaw_query_join":               ("query_id",         "swfaw_query"),
        "swfaw_query_parameter":          ("query_id",         "swfaw_query"),
        "swfaw_filter_field":             ("filter_id",        "swfaw_filter"),
        "swfaw_security_oauth2_provider": ("security_config_id","swfaw_security_config"),
        "swfaw_security_cors":            ("security_config_id","swfaw_security_config"),
        "swfaw_security_public_endpoint": ("security_config_id","swfaw_security_config"),
        "swfaw_audit_event":              ("audit_config_id",  "swfaw_audit_config"),
        "swfaw_audit_alert":              ("audit_config_id",  "swfaw_audit_config"),
        "swfaw_entity_access_control":    ("authorization_config_id", "swfaw_authorization_config"),
    }

    def __init__(self, db: DbConnection, app_id: int):
        self.db = db
        self.app_id = app_id

    # ------------------------------------------------------------------
    # Resolve helpers
    # ------------------------------------------------------------------

    def _resolve_table(self, alias: str) -> str:
        """Resolve a table alias to the actual table name."""
        if alias in self.TABLE_ALIASES:
            return self.TABLE_ALIASES[alias]
        # Allow full table name too
        if alias.startswith("swfaw_"):
            return alias
        raise ValueError(
            f"Unknown table alias '{alias}'. "
            f"Available: {sorted(self.TABLE_ALIASES.keys())}"
        )

    # ------------------------------------------------------------------
    # JSON predicate parsing
    # ------------------------------------------------------------------

    # Supported operators in $$ suffix (maps to MySQL JSON functions)
    _JSON_OPERATORS = {"contains", "exists", "type", "overlaps", "length"}

    @staticmethod
    def _normalize_json_path(path: str) -> str:
        """Ensure a JSON path starts with '$'."""
        if not path:
            return "$"
        return path if path.startswith("$") else "$." + path

    @staticmethod
    def _parse_json_predicate(key: str):
        """Parse a predicate key into (column, json_path_or_None, operator_or_None).

        Formats:
            "table_name"                  → ("table_name", None, None)       regular column
            "columns_json$.name"          → ("columns_json", "$.name", None) JSON_EXTRACT equality
            "columns_json$[0].name"       → ("columns_json", "$[0].name", None)
            "columns_json$$contains"      → ("columns_json", None, "contains")
            "columns_json$.path$$exists"  → ("columns_json", "$.path", "exists")
        """
        op = None
        rest = key
        if "$$" in key:
            rest, op = key.rsplit("$$", 1)

        if "$" in rest:
            col, json_path = rest.split("$", 1)
            json_path = DbLayerManager._normalize_json_path(json_path)
            return col, json_path, op

        return rest, None, op

    def _build_where(self, table: str, predicate: Optional[Dict[str, Any]] = None):
        """Build a WHERE clause scoped to this app_id + optional predicate.

        Regular predicates use column = value equality.
        JSON predicates use MySQL JSON functions via $ syntax in keys:

            {"columns_json$.name": "email"}
                → JSON_EXTRACT(columns_json, '$.name') = CAST(%s AS JSON)

            {"columns_json$$contains": {"name": "email"}}
                → JSON_CONTAINS(columns_json, CAST(%s AS JSON))

            {"columns_json$.items$$contains": {"name": "email"}}
                → JSON_CONTAINS(columns_json, CAST(%s AS JSON), %s)

            {"columns_json$.path$$exists": True}
                → JSON_CONTAINS_PATH(columns_json, 'one', %s)

            {"columns_json$.path$$type": "ARRAY"}
                → JSON_TYPE(JSON_EXTRACT(columns_json, %s)) = %s

            {"columns_json$.items$$overlaps": [1, 2]}
                → JSON_OVERLAPS(JSON_EXTRACT(columns_json, %s), CAST(%s AS JSON))

            {"columns_json$.items$$length": 3}
                → JSON_LENGTH(JSON_EXTRACT(columns_json, %s)) = %s

        Returns (where_sql, params_tuple).
        """
        conditions = []
        params = []

        # Scope to app
        if table in self.APP_LINKED_TABLES:
            if table == "swfaw_app_definition":
                conditions.append("id = %s")
            else:
                conditions.append("app_definition_id = %s")
            params.append(self.app_id)
        elif table in self.CHILD_TABLES:
            fk_col, parent_table = self.CHILD_TABLES[table]
            if parent_table == "swfaw_app_definition":
                conditions.append(f"{fk_col} IN (SELECT id FROM {parent_table} WHERE id = %s)")
            else:
                conditions.append(
                    f"{fk_col} IN (SELECT id FROM {parent_table} WHERE app_definition_id = %s)"
                )
            params.append(self.app_id)

        # Add predicate conditions (regular + JSON)
        if predicate:
            for key, val in predicate.items():
                col, json_path, op = self._parse_json_predicate(key)

                if json_path is None and op is None:
                    # --- Regular column predicate ---
                    if val is None:
                        conditions.append(f"{col} IS NULL")
                    else:
                        conditions.append(f"{col} = %s")
                        params.append(val)

                elif op == "contains":
                    # JSON_CONTAINS(col, candidate [, path])
                    json_val = json.dumps(val) if not isinstance(val, str) else val
                    if json_path:
                        conditions.append(f"JSON_CONTAINS({col}, CAST(%s AS JSON), %s)")
                        params.extend([json_val, json_path])
                    else:
                        conditions.append(f"JSON_CONTAINS({col}, CAST(%s AS JSON))")
                        params.append(json_val)

                elif op == "exists":
                    # JSON_CONTAINS_PATH(col, 'one', path)
                    path = json_path or "$"
                    conditions.append(f"JSON_CONTAINS_PATH({col}, 'one', %s)")
                    params.append(path)

                elif op == "type":
                    # JSON_TYPE(JSON_EXTRACT(col, path)) = val
                    path = json_path or "$"
                    conditions.append(f"JSON_TYPE(JSON_EXTRACT({col}, %s)) = %s")
                    params.extend([path, val])

                elif op == "overlaps":
                    # JSON_OVERLAPS(JSON_EXTRACT(col, path), candidate)
                    path = json_path or "$"
                    json_val = json.dumps(val) if not isinstance(val, str) else val
                    conditions.append(f"JSON_OVERLAPS(JSON_EXTRACT({col}, %s), CAST(%s AS JSON))")
                    params.extend([path, json_val])

                elif op == "length":
                    # JSON_LENGTH(JSON_EXTRACT(col, path)) = val
                    path = json_path or "$"
                    conditions.append(f"JSON_LENGTH(JSON_EXTRACT({col}, %s)) = %s")
                    params.extend([path, val])

                else:
                    # Default: JSON_EXTRACT equality
                    json_val = json.dumps(val) if not isinstance(val, str) else val
                    conditions.append(f"JSON_EXTRACT({col}, %s) = CAST(%s AS JSON)")
                    params.extend([json_path, json_val])

        where_sql = " AND ".join(conditions) if conditions else "1=1"
        return where_sql, tuple(params)

    def _decode_json_columns(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """Auto-decode any column ending in _json from string to Python object."""
        if row is None:
            return row
        for key in list(row.keys()):
            if key.endswith("_json") and isinstance(row[key], str):
                try:
                    row[key] = json.loads(row[key])
                except (json.JSONDecodeError, TypeError):
                    pass
        return row

    # ------------------------------------------------------------------
    # GET
    # ------------------------------------------------------------------

    def get(
        self, alias: str, predicate: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Get rows from a table. Returns a single dict for singleton tables,
        or a list of dicts for multi-row tables.
        
        Args:
            alias: Table alias (e.g. "security_config", "entity_layer")
            predicate: Optional column-value filter dict
            
        Returns:
            Dict for singleton tables, List[Dict] for multi-row tables
        """
        table = self._resolve_table(alias)
        where, params = self._build_where(table, predicate)
        sql = f"SELECT * FROM {table} WHERE {where}"
        rows = self.db.fetch_all(sql, params)
        rows = [self._decode_json_columns(r) for r in rows]

        # Singleton tables return a single dict
        singleton_tables = {
            "swfaw_app_definition", "swfaw_security_config", "swfaw_security_cors",
            "swfaw_app_config", "swfaw_exception_config", "swfaw_audit_config",
            "swfaw_authorization_config", "swfaw_group_config",
        }
        if table in singleton_tables:
            return rows[0] if rows else None

        return rows

    def get_value(self, alias: str, column: str, predicate: Optional[Dict[str, Any]] = None) -> Any:
        """Get a single column value from a table.
        
        Args:
            alias: Table alias
            column: Column name to retrieve
            predicate: Optional filter
            
        Returns:
            The column value, or None
        """
        table = self._resolve_table(alias)
        where, params = self._build_where(table, predicate)
        sql = f"SELECT {column} FROM {table} WHERE {where} LIMIT 1"
        row = self.db.fetch_one(sql, params)
        if row is None:
            return None
        val = row.get(column)
        # Auto-decode JSON
        if isinstance(val, str) and column.endswith("_json"):
            try:
                return json.loads(val)
            except (json.JSONDecodeError, TypeError):
                pass
        return val

    # ------------------------------------------------------------------
    # SET
    # ------------------------------------------------------------------

    def set(
        self,
        alias: str,
        column: str,
        value: Any,
        predicate: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Set a single column value on matching rows.
        
        Args:
            alias: Table alias
            column: Column name to update
            value: New value (dicts/lists auto-serialized to JSON for _json columns)
            predicate: Optional filter to narrow which rows to update
            
        Returns:
            Number of affected rows
            
        Example:
            lm.set("security_config", "jwt_expiration", 7200000)
            lm.set("entity_layer", "has_audit_fields", 1, {"table_name": "users"})
        """
        table = self._resolve_table(alias)
        # Auto-serialize JSON columns
        if column.endswith("_json") and not isinstance(value, str):
            value = json.dumps(value)

        where, params = self._build_where(table, predicate)
        sql = f"UPDATE {table} SET {column} = %s WHERE {where}"
        return self.db.execute(sql, (value,) + params)

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------

    def update(
        self,
        alias: str,
        updates: Dict[str, Any],
        predicate: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Update multiple columns on matching rows.
        
        Args:
            alias: Table alias
            updates: Dict of column-value pairs
            predicate: Optional filter
            
        Returns:
            Number of affected rows
            
        Example:
            lm.update("security_config", {
                "jwt_expiration": 7200000,
                "jwt_issuer": "acme",
                "jwt_algorithm": "HS512"
            })
        """
        if not updates:
            return 0

        table = self._resolve_table(alias)

        # Auto-serialize JSON columns
        serialized = {}
        for col, val in updates.items():
            if col.endswith("_json") and not isinstance(val, str):
                serialized[col] = json.dumps(val)
            else:
                serialized[col] = val

        set_clause = ", ".join(f"{col} = %s" for col in serialized)
        set_params = tuple(serialized.values())

        where, where_params = self._build_where(table, predicate)
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        return self.db.execute(sql, set_params + where_params)

    # ------------------------------------------------------------------
    # INSERT (append equivalent)
    # ------------------------------------------------------------------

    def insert(self, alias: str, data: Dict[str, Any]) -> int:
        """Insert a new row into a table.
        
        Automatically injects app_definition_id for app-linked tables.
        Auto-serializes _json columns.
        
        Args:
            alias: Table alias
            data: Column-value dict for the new row
            
        Returns:
            New row ID
            
        Example:
            lm.insert("entity_layer", {
                "table_name": "products",
                "class_name": "Product",
                "package_name": "com.example.entity",
            })
        """
        table = self._resolve_table(alias)

        # Auto-inject app_definition_id
        if table in self.APP_LINKED_TABLES and table != "swfaw_app_definition":
            data.setdefault("app_definition_id", self.app_id)

        # Auto-serialize JSON columns
        serialized = {}
        for col, val in data.items():
            if col.endswith("_json") and not isinstance(val, str) and val is not None:
                serialized[col] = json.dumps(val)
            else:
                serialized[col] = val

        columns = ", ".join(serialized.keys())
        placeholders = ", ".join(["%s"] * len(serialized))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return self.db.insert(sql, tuple(serialized.values()))

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    def delete(
        self,
        alias: str,
        predicate: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Delete rows matching the predicate.
        
        Args:
            alias: Table alias
            predicate: Column-value filter (required for safety on multi-row tables)
            
        Returns:
            Number of deleted rows
            
        Example:
            lm.delete("security_public_endpoint", {"endpoint_pattern": "/api/health"})
            lm.delete("entity_layer", {"table_name": "old_table"})
        """
        table = self._resolve_table(alias)
        where, params = self._build_where(table, predicate)
        sql = f"DELETE FROM {table} WHERE {where}"
        return self.db.execute(sql, params)

    # ------------------------------------------------------------------
    # FIND / FILTER
    # ------------------------------------------------------------------

    def find(self, alias: str, predicate: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find the first row matching a predicate.
        
        Args:
            alias: Table alias
            predicate: Column-value filter
            
        Returns:
            Row dict or None
            
        Example:
            row = lm.find("entity_layer", {"table_name": "users"})
        """
        table = self._resolve_table(alias)
        where, params = self._build_where(table, predicate)
        sql = f"SELECT * FROM {table} WHERE {where} LIMIT 1"
        row = self.db.fetch_one(sql, params)
        return self._decode_json_columns(row) if row else None

    def filter(self, alias: str, predicate: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter rows matching a predicate.
        
        Args:
            alias: Table alias
            predicate: Column-value filter
            
        Returns:
            List of matching row dicts
            
        Example:
            rows = lm.filter("dto_layer", {"entity_name": "users"})
        """
        table = self._resolve_table(alias)
        where, params = self._build_where(table, predicate)
        sql = f"SELECT * FROM {table} WHERE {where}"
        rows = self.db.fetch_all(sql, params)
        return [self._decode_json_columns(r) for r in rows]

    # ------------------------------------------------------------------
    # EXISTS
    # ------------------------------------------------------------------

    def exists(self, alias: str, predicate: Optional[Dict[str, Any]] = None) -> bool:
        """Check if any rows exist matching the criteria.
        
        Args:
            alias: Table alias
            predicate: Optional filter
            
        Returns:
            True if at least one row matches
            
        Example:
            lm.exists("security_config")
            lm.exists("entity_layer", {"table_name": "users"})
        """
        table = self._resolve_table(alias)
        where, params = self._build_where(table, predicate)
        sql = f"SELECT 1 FROM {table} WHERE {where} LIMIT 1"
        row = self.db.fetch_one(sql, params)
        return row is not None

    # ------------------------------------------------------------------
    # COUNT
    # ------------------------------------------------------------------

    def count(self, alias: str, predicate: Optional[Dict[str, Any]] = None) -> int:
        """Count rows matching the criteria.
        
        Args:
            alias: Table alias
            predicate: Optional filter
            
        Returns:
            Row count
        """
        table = self._resolve_table(alias)
        where, params = self._build_where(table, predicate)
        sql = f"SELECT COUNT(*) as cnt FROM {table} WHERE {where}"
        row = self.db.fetch_one(sql, params)
        return row["cnt"] if row else 0

    # ------------------------------------------------------------------
    # UTILITY
    # ------------------------------------------------------------------

    def list_tables(self) -> List[str]:
        """List all available table aliases."""
        return sorted(self.TABLE_ALIASES.keys())

    def describe(self, alias: str) -> List[Dict[str, Any]]:
        """Get column metadata for a table (DESCRIBE equivalent).
        
        Returns:
            List of column info dicts with Field, Type, Null, Key, Default, Extra
        """
        table = self._resolve_table(alias)
        return self.db.fetch_all(f"DESCRIBE {table}")

    # ------------------------------------------------------------------
    # MySQL JSON Functions — Read
    # ------------------------------------------------------------------

    def _json_query(
        self,
        alias: str,
        column: str,
        sql_template: str,
        query_params: list,
        predicate: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Shared helper for JSON read queries. Builds the full SELECT with
        app-scoped WHERE + optional predicate, returns decoded rows.

        Args:
            alias: Table alias
            column: JSON column name (used only for documentation; actual col is in sql_template)
            sql_template: SQL fragment for SELECT ... FROM {table} WHERE {where} AND <extra>
                          Must contain {table} and {where} placeholders.
            query_params: Parameters for the sql_template placeholders (before where params)
            predicate: Optional additional column-value filter
        """
        table = self._resolve_table(alias)
        where, where_params = self._build_where(table, predicate)
        sql = sql_template.format(table=table, where=where)
        rows = self.db.fetch_all(sql, tuple(query_params) + where_params)
        return [self._decode_json_columns(r) for r in rows]

    def json_extract(
        self,
        alias: str,
        column: str,
        path: str,
        predicate: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        """MySQL JSON_EXTRACT — extract values at a JSON path from matching rows.

        Args:
            alias: Table alias
            column: JSON column name (e.g. "columns_json")
            path: JSON path (e.g. "$.name", "$[0].type", "$[*].name")
            predicate: Optional row filter

        Returns:
            List of extracted values (auto-parsed from JSON)

        Example:
            # Get all column names from the users entity
            names = lm.json_extract("entity", "columns_json", "$[*].name",
                                    {"table_name": "users"})
        """
        path = self._normalize_json_path(path)
        sql = (
            f"SELECT JSON_EXTRACT({column}, %s) AS jval "
            f"FROM {{table}} WHERE {{where}}"
        )
        rows = self._json_query(alias, column, sql, [path], predicate)
        results = []
        for r in rows:
            v = r.get("jval")
            if v is None:
                results.append(None)
            elif isinstance(v, str):
                try:
                    results.append(json.loads(v))
                except (json.JSONDecodeError, TypeError):
                    results.append(v)
            else:
                results.append(v)
        return results

    def json_value(
        self,
        alias: str,
        column: str,
        path: str,
        predicate: Optional[Dict[str, Any]] = None,
    ) -> List[Optional[str]]:
        """MySQL JSON_VALUE — extract a scalar string at a JSON path.

        Unlike json_extract, this returns an unquoted scalar string (no JSON wrapper).

        Args:
            alias: Table alias
            column: JSON column name
            path: JSON path to a scalar value
            predicate: Optional row filter

        Returns:
            List of scalar string values (or None)

        Example:
            emails = lm.json_value("entity", "columns_json", "$[1].name",
                                   {"table_name": "users"})
        """
        path = self._normalize_json_path(path)
        sql = (
            f"SELECT JSON_VALUE({column}, %s) AS jval "
            f"FROM {{table}} WHERE {{where}}"
        )
        rows = self._json_query(alias, column, sql, [path], predicate)
        return [r.get("jval") for r in rows]

    def json_contains(
        self,
        alias: str,
        column: str,
        candidate: Any,
        path: Optional[str] = None,
        predicate: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """MySQL JSON_CONTAINS — find rows where JSON column contains candidate.

        Args:
            alias: Table alias
            column: JSON column name
            candidate: Value to search for (auto-serialized to JSON)
            path: Optional JSON path to scope the search within
            predicate: Optional row filter

        Returns:
            Matching rows (decoded)

        Example:
            # Find entities that have a column named "email"
            rows = lm.json_contains("entity", "columns_json",
                                    {"name": "email"})

            # Check inside a specific path
            rows = lm.json_contains("entity", "columns_json",
                                    "email", path="$[0].name")
        """
        json_candidate = json.dumps(candidate) if not isinstance(candidate, str) else candidate
        if path:
            path = self._normalize_json_path(path)
            sql = (
                f"SELECT * FROM {{table}} WHERE {{where}} "
                f"AND JSON_CONTAINS({column}, CAST(%s AS JSON), %s)"
            )
            params = [json_candidate, path]
        else:
            sql = (
                f"SELECT * FROM {{table}} WHERE {{where}} "
                f"AND JSON_CONTAINS({column}, CAST(%s AS JSON))"
            )
            params = [json_candidate]
        return self._json_query(alias, column, sql, params, predicate)

    def json_contains_path(
        self,
        alias: str,
        column: str,
        *paths: str,
        mode: str = "one",
        predicate: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """MySQL JSON_CONTAINS_PATH — find rows where JSON path(s) exist.

        Args:
            alias: Table alias
            column: JSON column name
            *paths: One or more JSON paths to check
            mode: 'one' (any path exists) or 'all' (all paths exist)
            predicate: Optional row filter

        Returns:
            Matching rows (decoded)

        Example:
            # Entities that have a "name" key somewhere in columns_json
            rows = lm.json_contains_path("entity", "columns_json", "$[*].name")

            # Entities that have both "name" and "type" keys
            rows = lm.json_contains_path("entity", "columns_json",
                                         "$[*].name", "$[*].type", mode="all")
        """
        if not paths:
            raise ValueError("At least one JSON path is required")
        if mode not in ("one", "all"):
            raise ValueError("mode must be 'one' or 'all'")

        normalized = [self._normalize_json_path(p) for p in paths]
        placeholders = ", ".join(["%s"] * len(normalized))
        sql = (
            f"SELECT * FROM {{table}} WHERE {{where}} "
            f"AND JSON_CONTAINS_PATH({column}, %s, {placeholders})"
        )
        params = [mode] + normalized
        return self._json_query(alias, column, sql, params, predicate)

    def json_search(
        self,
        alias: str,
        column: str,
        search_str: str,
        mode: str = "one",
        path: Optional[str] = None,
        predicate: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """MySQL JSON_SEARCH — find rows where a string value matches.

        Supports LIKE-style wildcards: % (any chars) and _ (one char).

        Args:
            alias: Table alias
            column: JSON column name
            search_str: String to search for (supports % and _ wildcards)
            mode: 'one' (first match) or 'all' (all matches)
            path: Optional JSON path to scope the search
            predicate: Optional row filter

        Returns:
            Matching rows (decoded)

        Example:
            # Find entities with any column name containing "email"
            rows = lm.json_search("entity", "columns_json", "%email%")

            # Search only within column names
            rows = lm.json_search("entity", "columns_json", "email",
                                  path="$[*].name")
        """
        if mode not in ("one", "all"):
            raise ValueError("mode must be 'one' or 'all'")

        if path:
            path = self._normalize_json_path(path)
            sql = (
                f"SELECT * FROM {{table}} WHERE {{where}} "
                f"AND JSON_SEARCH({column}, %s, %s, NULL, %s) IS NOT NULL"
            )
            params = [mode, search_str, path]
        else:
            sql = (
                f"SELECT * FROM {{table}} WHERE {{where}} "
                f"AND JSON_SEARCH({column}, %s, %s) IS NOT NULL"
            )
            params = [mode, search_str]
        return self._json_query(alias, column, sql, params, predicate)

    def json_keys(
        self,
        alias: str,
        column: str,
        path: Optional[str] = None,
        predicate: Optional[Dict[str, Any]] = None,
    ) -> List[Any]:
        """MySQL JSON_KEYS — get keys of a JSON object at a path.

        Args:
            alias: Table alias
            column: JSON column name
            path: Optional JSON path (defaults to root '$')
            predicate: Optional row filter

        Returns:
            List of key arrays (one per matching row, auto-parsed)

        Example:
            keys = lm.json_keys("app_config", "config_json")
        """
        path = self._normalize_json_path(path) if path else "$"
        sql = (
            f"SELECT JSON_KEYS({column}, %s) AS jval "
            f"FROM {{table}} WHERE {{where}}"
        )
        rows = self._json_query(alias, column, sql, [path], predicate)
        results = []
        for r in rows:
            v = r.get("jval")
            if v is None:
                results.append(None)
            elif isinstance(v, str):
                try:
                    results.append(json.loads(v))
                except (json.JSONDecodeError, TypeError):
                    results.append(v)
            else:
                results.append(v)
        return results

    def json_length(
        self,
        alias: str,
        column: str,
        path: Optional[str] = None,
        predicate: Optional[Dict[str, Any]] = None,
    ) -> List[Optional[int]]:
        """MySQL JSON_LENGTH — get length of JSON value at a path.

        Args:
            alias: Table alias
            column: JSON column name
            path: Optional JSON path (defaults to root '$')
            predicate: Optional row filter

        Returns:
            List of lengths (one per matching row)

        Example:
            # How many columns does each entity have in its JSON?
            lengths = lm.json_length("entity", "columns_json")
        """
        path = self._normalize_json_path(path) if path else "$"
        sql = (
            f"SELECT JSON_LENGTH({column}, %s) AS jval "
            f"FROM {{table}} WHERE {{where}}"
        )
        rows = self._json_query(alias, column, sql, [path], predicate)
        return [r.get("jval") for r in rows]

    def json_type(
        self,
        alias: str,
        column: str,
        path: Optional[str] = None,
        predicate: Optional[Dict[str, Any]] = None,
    ) -> List[Optional[str]]:
        """MySQL JSON_TYPE — get the type of JSON value at a path.

        Returns MySQL JSON type strings: OBJECT, ARRAY, STRING, INTEGER,
        DOUBLE, BOOLEAN, NULL.

        Args:
            alias: Table alias
            column: JSON column name
            path: Optional JSON path (defaults to root '$')
            predicate: Optional row filter

        Returns:
            List of type strings (one per matching row)

        Example:
            types = lm.json_type("entity", "columns_json")  # → ["ARRAY"]
        """
        if path:
            path = self._normalize_json_path(path)
            sql = (
                f"SELECT JSON_TYPE(JSON_EXTRACT({column}, %s)) AS jval "
                f"FROM {{table}} WHERE {{where}}"
            )
            params = [path]
        else:
            sql = (
                f"SELECT JSON_TYPE({column}) AS jval "
                f"FROM {{table}} WHERE {{where}}"
            )
            params = []
        rows = self._json_query(alias, column, sql, params, predicate)
        return [r.get("jval") for r in rows]

    def json_overlaps(
        self,
        alias: str,
        column: str,
        candidate: Any,
        path: Optional[str] = None,
        predicate: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """MySQL JSON_OVERLAPS — find rows where JSON has any common elements.

        Args:
            alias: Table alias
            column: JSON column name
            candidate: Value to check overlap with (auto-serialized)
            path: Optional JSON path to scope the check
            predicate: Optional row filter

        Returns:
            Matching rows (decoded)

        Example:
            # Find entities whose columns include any of these types
            rows = lm.json_overlaps("entity", "columns_json",
                                    ["VARCHAR", "TEXT"], path="$[*].type")
        """
        json_candidate = json.dumps(candidate) if not isinstance(candidate, str) else candidate
        if path:
            path = self._normalize_json_path(path)
            sql = (
                f"SELECT * FROM {{table}} WHERE {{where}} "
                f"AND JSON_OVERLAPS(JSON_EXTRACT({column}, %s), CAST(%s AS JSON))"
            )
            params = [path, json_candidate]
        else:
            sql = (
                f"SELECT * FROM {{table}} WHERE {{where}} "
                f"AND JSON_OVERLAPS({column}, CAST(%s AS JSON))"
            )
            params = [json_candidate]
        return self._json_query(alias, column, sql, params, predicate)

    # ------------------------------------------------------------------
    # MySQL JSON Functions — Write
    # ------------------------------------------------------------------

    def _json_modify(
        self,
        alias: str,
        column: str,
        func: str,
        path_value_pairs: List[tuple],
        predicate: Optional[Dict[str, Any]] = None,
    ) -> int:
        """Shared helper for JSON modification functions (SET, INSERT, REPLACE, REMOVE).

        Args:
            alias: Table alias
            column: JSON column name
            func: MySQL function name (JSON_SET, JSON_INSERT, JSON_REPLACE, JSON_REMOVE)
            path_value_pairs: List of (path, value) tuples. For JSON_REMOVE, value is ignored.
            predicate: Optional row filter

        Returns:
            Number of affected rows
        """
        table = self._resolve_table(alias)
        where, where_params = self._build_where(table, predicate)

        if func == "JSON_REMOVE":
            # JSON_REMOVE(col, path1, path2, ...)
            paths = [self._normalize_json_path(p) for p, _ in path_value_pairs]
            path_placeholders = ", ".join(["%s"] * len(paths))
            sql = (
                f"UPDATE {table} SET {column} = "
                f"JSON_REMOVE({column}, {path_placeholders}) "
                f"WHERE {where}"
            )
            return self.db.execute(sql, tuple(paths) + where_params)
        else:
            # JSON_SET/INSERT/REPLACE(col, path1, val1, path2, val2, ...)
            fragments = []
            params = []
            for path, val in path_value_pairs:
                path = self._normalize_json_path(path)
                fragments.extend(["%s", "CAST(%s AS JSON)"])
                params.extend([path, json.dumps(val) if not isinstance(val, str) else val])
            args_sql = ", ".join(fragments)
            sql = (
                f"UPDATE {table} SET {column} = "
                f"{func}({column}, {args_sql}) "
                f"WHERE {where}"
            )
            return self.db.execute(sql, tuple(params) + where_params)

    def json_set(
        self,
        alias: str,
        column: str,
        path_value_pairs: Union[Dict[str, Any], List[tuple]],
        predicate: Optional[Dict[str, Any]] = None,
    ) -> int:
        """MySQL JSON_SET — set values at paths (insert or update).

        Args:
            alias: Table alias
            column: JSON column name
            path_value_pairs: Dict of {path: value} or list of (path, value) tuples
            predicate: Optional row filter

        Returns:
            Number of affected rows

        Example:
            lm.json_set("entity", "columns_json", {"$[0].nullable": False},
                         {"table_name": "users"})
        """
        pairs = list(path_value_pairs.items()) if isinstance(path_value_pairs, dict) else path_value_pairs
        return self._json_modify(alias, column, "JSON_SET", pairs, predicate)

    def json_insert(
        self,
        alias: str,
        column: str,
        path_value_pairs: Union[Dict[str, Any], List[tuple]],
        predicate: Optional[Dict[str, Any]] = None,
    ) -> int:
        """MySQL JSON_INSERT — insert values only at paths that don't exist yet.

        Args:
            alias: Table alias
            column: JSON column name
            path_value_pairs: Dict of {path: value} or list of (path, value) tuples
            predicate: Optional row filter

        Returns:
            Number of affected rows

        Example:
            lm.json_insert("entity", "columns_json",
                           {"$[0].comment": "Primary key"},
                           {"table_name": "users"})
        """
        pairs = list(path_value_pairs.items()) if isinstance(path_value_pairs, dict) else path_value_pairs
        return self._json_modify(alias, column, "JSON_INSERT", pairs, predicate)

    def json_replace(
        self,
        alias: str,
        column: str,
        path_value_pairs: Union[Dict[str, Any], List[tuple]],
        predicate: Optional[Dict[str, Any]] = None,
    ) -> int:
        """MySQL JSON_REPLACE — replace values only at paths that already exist.

        Args:
            alias: Table alias
            column: JSON column name
            path_value_pairs: Dict of {path: value} or list of (path, value) tuples
            predicate: Optional row filter

        Returns:
            Number of affected rows

        Example:
            lm.json_replace("entity", "columns_json",
                            {"$[0].type": "BIGINT UNSIGNED"},
                            {"table_name": "users"})
        """
        pairs = list(path_value_pairs.items()) if isinstance(path_value_pairs, dict) else path_value_pairs
        return self._json_modify(alias, column, "JSON_REPLACE", pairs, predicate)

    def json_remove(
        self,
        alias: str,
        column: str,
        *paths: str,
        predicate: Optional[Dict[str, Any]] = None,
    ) -> int:
        """MySQL JSON_REMOVE — remove values at paths.

        Args:
            alias: Table alias
            column: JSON column name
            *paths: JSON paths to remove
            predicate: Optional row filter

        Returns:
            Number of affected rows

        Example:
            lm.json_remove("entity", "columns_json", "$[2]",
                           predicate={"table_name": "users"})
        """
        if not paths:
            raise ValueError("At least one JSON path is required")
        pairs = [(p, None) for p in paths]
        return self._json_modify(alias, column, "JSON_REMOVE", pairs, predicate)

    def json_array_append(
        self,
        alias: str,
        column: str,
        path: str,
        value: Any,
        predicate: Optional[Dict[str, Any]] = None,
    ) -> int:
        """MySQL JSON_ARRAY_APPEND — append a value to a JSON array at a path.

        Args:
            alias: Table alias
            column: JSON column name
            path: JSON path to the array
            value: Value to append (auto-serialized)
            predicate: Optional row filter

        Returns:
            Number of affected rows

        Example:
            # Add a new column definition to an entity's columns_json array
            lm.json_array_append("entity", "columns_json", "$",
                                 {"name": "status", "type": "VARCHAR(50)"},
                                 {"table_name": "users"})
        """
        table = self._resolve_table(alias)
        where, where_params = self._build_where(table, predicate)
        path = self._normalize_json_path(path)
        json_val = json.dumps(value) if not isinstance(value, str) else value
        sql = (
            f"UPDATE {table} SET {column} = "
            f"JSON_ARRAY_APPEND({column}, %s, CAST(%s AS JSON)) "
            f"WHERE {where}"
        )
        return self.db.execute(sql, (path, json_val) + where_params)
