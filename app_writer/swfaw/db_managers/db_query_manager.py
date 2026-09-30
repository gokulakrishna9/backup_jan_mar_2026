"""Database query manager — CRUD on query tables (Tier 3).

Covers: swfaw_query, swfaw_query_join, swfaw_query_parameter
"""

import json
from typing import Optional, Dict, Any, List
from .db_connection import DbConnection


class DbQueryManager:
    """CRUD operations on custom query definition tables.
    
    Usage:
        qm = DbQueryManager(db, app_id=1)
        
        query_id = qm.add_query("users", "findActiveUsers",
            return_type="UserDto",
            select_fields=["u.id", "u.email"],
            from_clause="users u",
        )
        qm.add_join(query_id, "LEFT JOIN", "profiles p", "u.id = p.user_id")
        qm.add_parameter(query_id, "status", "String", is_required=True)
    """

    def __init__(self, db: DbConnection, app_id: int):
        self.db = db
        self.app_id = app_id

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def list_queries(self, entity_name: Optional[str] = None) -> List[Dict[str, Any]]:
        if entity_name:
            rows = self.db.fetch_all(
                "SELECT * FROM swfaw_query "
                "WHERE app_definition_id = %s AND entity_name = %s ORDER BY query_name",
                (self.app_id, entity_name),
            )
        else:
            rows = self.db.fetch_all(
                "SELECT * FROM swfaw_query "
                "WHERE app_definition_id = %s ORDER BY entity_name, query_name",
                (self.app_id,),
            )
        for r in rows:
            for key in list(r.keys()):
                if key.endswith("_json") and isinstance(r[key], str):
                    try:
                        r[key] = json.loads(r[key])
                    except (json.JSONDecodeError, TypeError):
                        pass
        return rows

    def get_query(self, entity_name: str, query_name: str) -> Optional[Dict[str, Any]]:
        row = self.db.fetch_one(
            "SELECT * FROM swfaw_query "
            "WHERE app_definition_id = %s AND entity_name = %s AND query_name = %s",
            (self.app_id, entity_name, query_name),
        )
        if row:
            for key in list(row.keys()):
                if key.endswith("_json") and isinstance(row[key], str):
                    try:
                        row[key] = json.loads(row[key])
                    except (json.JSONDecodeError, TypeError):
                        pass
        return row

    def add_query(
        self,
        entity_name: str,
        query_name: str,
        return_type: str,
        select_fields: List[str],
        from_clause: str,
        description: Optional[str] = None,
        where_clauses: Optional[List] = None,
        group_by: Optional[List[str]] = None,
        having: Optional[List] = None,
        order_by: Optional[List] = None,
        pagination: bool = True,
        authz_enabled: bool = True,
        authz_document_field: Optional[str] = None,
    ) -> int:
        sql = (
            "INSERT INTO swfaw_query "
            "(app_definition_id, entity_name, query_name, description, return_type, "
            "select_fields_json, from_clause, where_clauses_json, group_by_json, "
            "having_json, order_by_json, pagination, authz_enabled, authz_document_field) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        return self.db.insert(sql, (
            self.app_id, entity_name, query_name, description, return_type,
            json.dumps(select_fields), from_clause,
            json.dumps(where_clauses) if where_clauses else None,
            json.dumps(group_by) if group_by else None,
            json.dumps(having) if having else None,
            json.dumps(order_by) if order_by else None,
            int(pagination), int(authz_enabled), authz_document_field,
        ))

    def remove_query(self, entity_name: str, query_name: str) -> int:
        return self.db.execute(
            "DELETE FROM swfaw_query "
            "WHERE app_definition_id = %s AND entity_name = %s AND query_name = %s",
            (self.app_id, entity_name, query_name),
        )

    # ------------------------------------------------------------------
    # Query Joins
    # ------------------------------------------------------------------

    def list_joins(self, query_id: int) -> List[Dict[str, Any]]:
        return self.db.fetch_all(
            "SELECT * FROM swfaw_query_join WHERE query_id = %s ORDER BY sort_order",
            (query_id,),
        )

    def add_join(
        self,
        query_id: int,
        join_type: str,
        join_table: str,
        join_condition: str,
        join_alias: Optional[str] = None,
        sort_order: int = 0,
    ) -> int:
        sql = (
            "INSERT INTO swfaw_query_join "
            "(query_id, join_type, join_table, join_alias, join_condition, sort_order) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        return self.db.insert(sql, (
            query_id, join_type, join_table, join_alias, join_condition, sort_order,
        ))

    def remove_join(self, join_id: int) -> int:
        return self.db.execute("DELETE FROM swfaw_query_join WHERE id = %s", (join_id,))

    # ------------------------------------------------------------------
    # Query Parameters
    # ------------------------------------------------------------------

    def list_parameters(self, query_id: int) -> List[Dict[str, Any]]:
        return self.db.fetch_all(
            "SELECT * FROM swfaw_query_parameter WHERE query_id = %s ORDER BY sort_order",
            (query_id,),
        )

    def add_parameter(
        self,
        query_id: int,
        param_name: str,
        param_type: str,
        is_required: bool = True,
        default_value: Optional[str] = None,
        sort_order: int = 0,
    ) -> int:
        sql = (
            "INSERT INTO swfaw_query_parameter "
            "(query_id, param_name, param_type, is_required, default_value, sort_order) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        return self.db.insert(sql, (
            query_id, param_name, param_type, int(is_required), default_value, sort_order,
        ))

    def remove_parameter(self, param_id: int) -> int:
        return self.db.execute("DELETE FROM swfaw_query_parameter WHERE id = %s", (param_id,))

    # ------------------------------------------------------------------
    # Full query with joins + params
    # ------------------------------------------------------------------

    def get_full_query(self, entity_name: str, query_name: str) -> Optional[Dict[str, Any]]:
        """Get a query with its joins and parameters included."""
        query = self.get_query(entity_name, query_name)
        if query is None:
            return None
        query["joins"] = self.list_joins(query["id"])
        query["parameters"] = self.list_parameters(query["id"])
        return query
