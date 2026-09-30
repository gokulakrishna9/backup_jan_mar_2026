"""Database entity manager — CRUD on swfaw_entity table."""

import json
from typing import Optional, Dict, Any, List
from .db_connection import DbConnection


class DbEntityManager:
    """CRUD operations on swfaw_entity (replaces entities.json).
    
    Each row stores one table definition with its columns as a JSON blob.
    
    Usage:
        db = DbConnection.from_config()
        em = DbEntityManager(db, app_id=1)
        
        # Add entity
        entity_id = em.add_entity("users", columns=[
            {"name": "id", "type": "BIGINT", "primaryKey": True, "nullable": False, "autoIncrement": True},
            {"name": "email", "type": "VARCHAR(255)", "nullable": False, "unique": True},
        ])
        
        # List / get
        entities = em.list_entities()
        entity = em.get_entity("users")
        
        # Update
        em.update_entity("users", columns_json=[...], primary_key_column="id")
        
        # Remove
        em.remove_entity("users")
    """

    TABLE = "swfaw_entity"

    def __init__(self, db: DbConnection, app_id: int):
        self.db = db
        self.app_id = app_id

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    def add_entity(
        self,
        table_name: str,
        columns: Optional[List[Dict[str, Any]]] = None,
        primary_key_column: Optional[str] = None,
        sort_order: int = 0,
    ) -> int:
        """Add a new entity (table) definition.
        
        Args:
            table_name: SQL table name
            columns: List of column dicts (stored as JSON)
            primary_key_column: Name of the PK column
            sort_order: Display order
            
        Returns:
            New entity row ID
        """
        if self.entity_exists(table_name):
            raise ValueError(f"Entity '{table_name}' already exists for app {self.app_id}")

        if columns is None:
            columns = [
                {"name": "id", "type": "BIGINT", "primaryKey": True,
                 "nullable": False, "autoIncrement": True}
            ]

        if primary_key_column is None:
            for col in columns:
                if col.get("primaryKey"):
                    primary_key_column = col["name"]
                    break

        columns_json = json.dumps(columns)
        column_count = len(columns)

        sql = (
            f"INSERT INTO {self.TABLE} "
            "(app_definition_id, table_name, columns_json, column_count, "
            "primary_key_column, sort_order) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        return self.db.insert(sql, (
            self.app_id, table_name, columns_json, column_count,
            primary_key_column, sort_order,
        ))

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------

    def get_entity(self, table_name: str) -> Optional[Dict[str, Any]]:
        """Get an entity by table name."""
        row = self.db.fetch_one(
            f"SELECT * FROM {self.TABLE} "
            "WHERE app_definition_id = %s AND table_name = %s",
            (self.app_id, table_name),
        )
        if row and row.get("columns_json"):
            row["columns"] = json.loads(row["columns_json"]) if isinstance(row["columns_json"], str) else row["columns_json"]
        return row

    def get_entity_by_id(self, entity_id: int) -> Optional[Dict[str, Any]]:
        """Get an entity by its row ID."""
        row = self.db.fetch_one(
            f"SELECT * FROM {self.TABLE} WHERE id = %s", (entity_id,)
        )
        if row and row.get("columns_json"):
            row["columns"] = json.loads(row["columns_json"]) if isinstance(row["columns_json"], str) else row["columns_json"]
        return row

    def list_entities(self) -> List[Dict[str, Any]]:
        """List all entities for this app, ordered by sort_order."""
        rows = self.db.fetch_all(
            f"SELECT * FROM {self.TABLE} "
            "WHERE app_definition_id = %s ORDER BY sort_order, table_name",
            (self.app_id,),
        )
        for row in rows:
            if row.get("columns_json"):
                row["columns"] = json.loads(row["columns_json"]) if isinstance(row["columns_json"], str) else row["columns_json"]
        return rows

    def list_entity_names(self) -> List[str]:
        """List just the table names."""
        rows = self.db.fetch_all(
            f"SELECT table_name FROM {self.TABLE} "
            "WHERE app_definition_id = %s ORDER BY sort_order, table_name",
            (self.app_id,),
        )
        return [r["table_name"] for r in rows]

    def entity_exists(self, table_name: str) -> bool:
        """Check if an entity exists."""
        row = self.db.fetch_one(
            f"SELECT id FROM {self.TABLE} "
            "WHERE app_definition_id = %s AND table_name = %s",
            (self.app_id, table_name),
        )
        return row is not None

    def get_entity_details(self, table_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed info about an entity including relationship counts."""
        entity = self.get_entity(table_name)
        if entity is None:
            return None

        rel_count = self.db.fetch_one(
            "SELECT COUNT(*) as cnt FROM swfaw_relationship "
            "WHERE app_definition_id = %s AND (source_table = %s OR target_table = %s)",
            (self.app_id, table_name, table_name),
        )

        return {
            "id": entity["id"],
            "table_name": entity["table_name"],
            "columns": entity.get("columns", []),
            "column_count": entity["column_count"],
            "primary_key_column": entity["primary_key_column"],
            "sort_order": entity["sort_order"],
            "relationship_count": rel_count["cnt"] if rel_count else 0,
        }

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------

    def update_entity(self, table_name: str, **kwargs) -> int:
        """Update entity fields.
        
        Accepts: columns_json (or columns), primary_key_column, sort_order, table_name (rename).
        If 'columns' is passed as a list, it's serialized to columns_json automatically.
        """
        if "columns" in kwargs and "columns_json" not in kwargs:
            cols = kwargs.pop("columns")
            kwargs["columns_json"] = json.dumps(cols)
            kwargs["column_count"] = len(cols)

        allowed = {"table_name", "columns_json", "column_count", "primary_key_column", "sort_order"}
        updates = {k: v for k, v in kwargs.items() if k in allowed}
        if not updates:
            return 0

        set_clause = ", ".join(f"{col} = %s" for col in updates)
        sql = (
            f"UPDATE {self.TABLE} SET {set_clause} "
            "WHERE app_definition_id = %s AND table_name = %s"
        )
        params = tuple(updates.values()) + (self.app_id, table_name)
        return self.db.execute(sql, params)

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    def remove_entity(self, table_name: str) -> int:
        """Remove an entity by table name. CASCADE deletes child layer rows."""
        return self.db.execute(
            f"DELETE FROM {self.TABLE} "
            "WHERE app_definition_id = %s AND table_name = %s",
            (self.app_id, table_name),
        )
