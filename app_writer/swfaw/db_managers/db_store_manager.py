"""Core database store manager — equivalent of DefinitionManager for the DB backend.

Manages app definitions (swfaw_app_definition) and provides the app_id context
that all other DB managers depend on.
"""

import json
from typing import Optional, Dict, Any, List
from .db_connection import DbConnection


class DbStoreManager:
    """CRUD operations on swfaw_app_definition — the root table.
    
    Every other DB manager requires an app_definition_id. This manager
    creates/loads that root row and exposes the id for downstream use.
    
    Usage:
        db = DbConnection.from_config()
        store = DbStoreManager(db)
        
        # Create a new app definition
        app_id = store.create_app(
            project_name="My Project",
            application_name="MyApp",
            artifact_id="my-app",
            db_name="my_database"
        )
        
        # Load an existing app
        app = store.get_app(app_id)
        
        # List all apps
        apps = store.list_apps()
        
        # Update fields
        store.update_app(app_id, port=8082, project_version="2.0.0")
        
        # Soft delete
        store.deactivate_app(app_id)
    """

    TABLE = "swfaw_app_definition"

    def __init__(self, db: DbConnection):
        self.db = db

    # ------------------------------------------------------------------
    # CREATE
    # ------------------------------------------------------------------

    def create_app(
        self,
        project_name: str,
        application_name: str,
        artifact_id: str,
        db_name: str,
        group_id: str = "com.example",
        project_version: str = "1.0.0",
        port: int = 8081,
        db_type: str = "mysql",
        db_host: str = "localhost",
        db_port: int = 3306,
        db_username: str = "root",
        db_password: str = "password",
        description: Optional[str] = None,
        sql_file_name: Optional[str] = None,
        created_by: Optional[str] = None,
    ) -> int:
        """Create a new application definition.
        
        Returns:
            The new app_definition_id
        """
        db_url = f"r2dbc:{db_type}://{db_host}:{db_port}/{db_name}"

        sql = (
            f"INSERT INTO {self.TABLE} "
            "(project_name, application_name, artifact_id, db_name, "
            "group_id, project_version, port, db_type, db_host, db_port, "
            "db_url, db_username, db_password, description, sql_file_name, created_by) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        params = (
            project_name, application_name, artifact_id, db_name,
            group_id, project_version, port, db_type, db_host, db_port,
            db_url, db_username, db_password, description, sql_file_name, created_by,
        )
        return self.db.insert(sql, params)

    # ------------------------------------------------------------------
    # READ
    # ------------------------------------------------------------------

    def get_app(self, app_id: int) -> Optional[Dict[str, Any]]:
        """Get an application definition by ID."""
        return self.db.fetch_one(
            f"SELECT * FROM {self.TABLE} WHERE id = %s", (app_id,)
        )

    def get_app_by_artifact(
        self, group_id: str, artifact_id: str, version: str = "1.0.0"
    ) -> Optional[Dict[str, Any]]:
        """Get an app definition by its unique artifact coordinates."""
        return self.db.fetch_one(
            f"SELECT * FROM {self.TABLE} "
            "WHERE group_id = %s AND artifact_id = %s AND project_version = %s",
            (group_id, artifact_id, version),
        )

    def list_apps(self, active_only: bool = True) -> List[Dict[str, Any]]:
        """List all application definitions.
        
        Args:
            active_only: If True, only return active (non-deleted) apps
        """
        sql = f"SELECT * FROM {self.TABLE}"
        if active_only:
            sql += " WHERE is_active = 1"
        sql += " ORDER BY date_modified DESC"
        return self.db.fetch_all(sql)

    def app_exists(self, app_id: int) -> bool:
        """Check if an app definition exists."""
        row = self.db.fetch_one(
            f"SELECT id FROM {self.TABLE} WHERE id = %s", (app_id,)
        )
        return row is not None

    def get_statistics(self, app_id: int) -> Dict[str, Any]:
        """Get statistics for an app definition."""
        app = self.get_app(app_id)
        if app is None:
            raise ValueError(f"App definition {app_id} not found")
        return {
            "project_name": app["project_name"],
            "application_name": app["application_name"],
            "total_entities": app["total_entities"],
            "total_relationships": app["total_relationships"],
            "total_columns": app["total_columns"],
            "database_type": app["db_type"],
            "database_name": app["db_name"],
        }

    # ------------------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------------------

    def update_app(self, app_id: int, **kwargs) -> int:
        """Update fields on an app definition.
        
        Args:
            app_id: The app definition ID
            **kwargs: Column-value pairs to update
            
        Returns:
            Number of affected rows
            
        Example:
            store.update_app(1, port=8082, project_version="2.0.0")
        """
        if not kwargs:
            return 0

        # Whitelist of updatable columns
        allowed = {
            "version", "format", "description",
            "project_name", "application_name", "group_id", "artifact_id",
            "project_version", "port", "sql_file_name",
            "db_type", "db_host", "db_port", "db_name", "db_url",
            "db_username", "db_password",
            "total_entities", "total_relationships", "total_columns",
            "created_by", "is_active",
        }
        updates = {k: v for k, v in kwargs.items() if k in allowed}
        if not updates:
            raise ValueError(f"No valid columns to update. Allowed: {sorted(allowed)}")

        set_clause = ", ".join(f"{col} = %s" for col in updates)
        sql = f"UPDATE {self.TABLE} SET {set_clause} WHERE id = %s"
        params = tuple(updates.values()) + (app_id,)
        return self.db.execute(sql, params)

    def refresh_statistics(self, app_id: int) -> Dict[str, int]:
        """Recalculate and update the denormalized statistics counters.
        
        Returns:
            Dict with total_entities, total_relationships, total_columns
        """
        entity_count = self.db.fetch_one(
            "SELECT COUNT(*) as cnt FROM swfaw_entity WHERE app_definition_id = %s",
            (app_id,),
        )
        rel_count = self.db.fetch_one(
            "SELECT COUNT(*) as cnt FROM swfaw_relationship WHERE app_definition_id = %s",
            (app_id,),
        )
        col_count = self.db.fetch_one(
            "SELECT COALESCE(SUM(column_count), 0) as cnt FROM swfaw_entity WHERE app_definition_id = %s",
            (app_id,),
        )

        stats = {
            "total_entities": entity_count["cnt"] if entity_count else 0,
            "total_relationships": rel_count["cnt"] if rel_count else 0,
            "total_columns": col_count["cnt"] if col_count else 0,
        }
        self.update_app(app_id, **stats)
        return stats

    # ------------------------------------------------------------------
    # DELETE
    # ------------------------------------------------------------------

    def deactivate_app(self, app_id: int) -> int:
        """Soft-delete an app definition (set is_active = 0)."""
        return self.db.execute(
            f"UPDATE {self.TABLE} SET is_active = 0 WHERE id = %s", (app_id,)
        )

    def activate_app(self, app_id: int) -> int:
        """Re-activate a soft-deleted app definition."""
        return self.db.execute(
            f"UPDATE {self.TABLE} SET is_active = 1 WHERE id = %s", (app_id,)
        )

    def delete_app(self, app_id: int) -> int:
        """Hard-delete an app definition and all child rows (CASCADE)."""
        return self.db.execute(
            f"DELETE FROM {self.TABLE} WHERE id = %s", (app_id,)
        )
