"""Database relationship manager — CRUD on swfaw_relationship table."""

from typing import Optional, Dict, Any, List
from .db_connection import DbConnection


class DbRelationshipManager:
    """CRUD operations on swfaw_relationship (replaces relationships.json).
    
    Usage:
        rm = DbRelationshipManager(db, app_id=1)
        
        rel_id = rm.add_relationship("orders", "users", "ManyToOne", foreign_key_column="user_id")
        rels = rm.get_relationships("orders")
        rm.remove_relationship(rel_id)
    """

    TABLE = "swfaw_relationship"

    def __init__(self, db: DbConnection, app_id: int):
        self.db = db
        self.app_id = app_id

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    def add_relationship(
        self,
        source_table: str,
        target_table: str,
        relationship_type: str,
        foreign_key_column: Optional[str] = None,
        join_table: Optional[str] = None,
    ) -> int:
        """Add a relationship between two tables.
        
        Args:
            source_table: The owning side table
            target_table: The referenced table
            relationship_type: OneToOne, OneToMany, ManyToOne, ManyToMany
            foreign_key_column: FK column name (for non-ManyToMany)
            join_table: Join table name (for ManyToMany)
            
        Returns:
            New relationship row ID
        """
        valid_types = {"OneToOne", "OneToMany", "ManyToOne", "ManyToMany"}
        if relationship_type not in valid_types:
            raise ValueError(f"Invalid relationship type '{relationship_type}'. Must be one of {valid_types}")

        sql = (
            f"INSERT INTO {self.TABLE} "
            "(app_definition_id, source_table, target_table, relationship_type, "
            "foreign_key_column, join_table) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        return self.db.insert(sql, (
            self.app_id, source_table, target_table, relationship_type,
            foreign_key_column, join_table,
        ))

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------

    def get_relationship(self, rel_id: int) -> Optional[Dict[str, Any]]:
        """Get a relationship by its row ID."""
        return self.db.fetch_one(
            f"SELECT * FROM {self.TABLE} WHERE id = %s", (rel_id,)
        )

    def get_relationships(self, table_name: str) -> List[Dict[str, Any]]:
        """Get all relationships where table_name is the source."""
        return self.db.fetch_all(
            f"SELECT * FROM {self.TABLE} "
            "WHERE app_definition_id = %s AND source_table = %s",
            (self.app_id, table_name),
        )

    def get_incoming_relationships(self, table_name: str) -> List[Dict[str, Any]]:
        """Get all relationships where table_name is the target."""
        return self.db.fetch_all(
            f"SELECT * FROM {self.TABLE} "
            "WHERE app_definition_id = %s AND target_table = %s",
            (self.app_id, table_name),
        )

    def get_all_relationships(self, table_name: str) -> List[Dict[str, Any]]:
        """Get all relationships involving a table (source or target)."""
        return self.db.fetch_all(
            f"SELECT * FROM {self.TABLE} "
            "WHERE app_definition_id = %s AND (source_table = %s OR target_table = %s)",
            (self.app_id, table_name, table_name),
        )

    def list_relationships(self) -> List[Dict[str, Any]]:
        """List all relationships for this app."""
        return self.db.fetch_all(
            f"SELECT * FROM {self.TABLE} WHERE app_definition_id = %s "
            "ORDER BY source_table, target_table",
            (self.app_id,),
        )

    def relationship_exists(
        self, source_table: str, target_table: str, relationship_type: str
    ) -> bool:
        """Check if a specific relationship already exists."""
        row = self.db.fetch_one(
            f"SELECT id FROM {self.TABLE} "
            "WHERE app_definition_id = %s AND source_table = %s "
            "AND target_table = %s AND relationship_type = %s",
            (self.app_id, source_table, target_table, relationship_type),
        )
        return row is not None

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------

    def update_relationship(self, rel_id: int, **kwargs) -> int:
        """Update relationship fields.
        
        Accepts: source_table, target_table, relationship_type,
                 foreign_key_column, join_table
        """
        allowed = {"source_table", "target_table", "relationship_type",
                    "foreign_key_column", "join_table"}
        updates = {k: v for k, v in kwargs.items() if k in allowed}
        if not updates:
            return 0

        set_clause = ", ".join(f"{col} = %s" for col in updates)
        sql = f"UPDATE {self.TABLE} SET {set_clause} WHERE id = %s"
        params = tuple(updates.values()) + (rel_id,)
        return self.db.execute(sql, params)

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    def remove_relationship(self, rel_id: int) -> int:
        """Remove a relationship by ID."""
        return self.db.execute(
            f"DELETE FROM {self.TABLE} WHERE id = %s", (rel_id,)
        )

    def remove_relationships_for_table(self, table_name: str) -> int:
        """Remove all relationships involving a table."""
        return self.db.execute(
            f"DELETE FROM {self.TABLE} "
            "WHERE app_definition_id = %s AND (source_table = %s OR target_table = %s)",
            (self.app_id, table_name, table_name),
        )
