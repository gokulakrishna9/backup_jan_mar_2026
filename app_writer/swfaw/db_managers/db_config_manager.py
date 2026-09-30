"""Database app config manager — CRUD on swfaw_app_config (Tier 4b)."""

import json
from typing import Optional, Dict, Any
from .db_connection import DbConnection


class DbConfigManager:
    """CRUD operations on swfaw_app_config (replaces config_layer.json).
    
    Singleton table — one row per app_definition_id.
    
    Usage:
        cm = DbConfigManager(db, app_id=1)
        config = cm.get_config()
        cm.update_config(server_port=8082, java_version="21")
        cm.set_logging(log_level_root="DEBUG", log_file_enabled=1)
        cm.set_swagger(swagger_enabled=1, swagger_title="My API")
    """

    TABLE = "swfaw_app_config"

    def __init__(self, db: DbConnection, app_id: int):
        self.db = db
        self.app_id = app_id

    def get_config(self) -> Optional[Dict[str, Any]]:
        """Get the app config."""
        row = self.db.fetch_one(
            f"SELECT * FROM {self.TABLE} WHERE app_definition_id = %s",
            (self.app_id,),
        )
        if row:
            for key in list(row.keys()):
                if key.endswith("_json") and isinstance(row[key], str):
                    try:
                        row[key] = json.loads(row[key])
                    except (json.JSONDecodeError, TypeError):
                        pass
        return row

    def create_config(self, **kwargs) -> int:
        """Create the app config row."""
        kwargs.setdefault("app_definition_id", self.app_id)
        for col in list(kwargs.keys()):
            if col.endswith("_json") and not isinstance(kwargs[col], str) and kwargs[col] is not None:
                kwargs[col] = json.dumps(kwargs[col])
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["%s"] * len(kwargs))
        sql = f"INSERT INTO {self.TABLE} ({columns}) VALUES ({placeholders})"
        return self.db.insert(sql, tuple(kwargs.values()))

    def update_config(self, **kwargs) -> int:
        """Update app config fields.
        
        Example:
            cm.update_config(server_port=8082, java_version="21",
                             spring_boot_version="3.3.0")
        """
        if not kwargs:
            return 0
        for col in list(kwargs.keys()):
            if col.endswith("_json") and not isinstance(kwargs[col], str) and kwargs[col] is not None:
                kwargs[col] = json.dumps(kwargs[col])
        set_clause = ", ".join(f"{col} = %s" for col in kwargs)
        sql = f"UPDATE {self.TABLE} SET {set_clause} WHERE app_definition_id = %s"
        return self.db.execute(sql, tuple(kwargs.values()) + (self.app_id,))

    # ------------------------------------------------------------------
    # Convenience methods for common config sections
    # ------------------------------------------------------------------

    def set_logging(self, **kwargs) -> int:
        """Update logging-related config fields.
        
        Example:
            cm.set_logging(log_level_root="DEBUG", log_file_enabled=1)
        """
        log_fields = {k: v for k, v in kwargs.items() if k.startswith("log_")}
        return self.update_config(**log_fields) if log_fields else 0

    def set_swagger(self, **kwargs) -> int:
        """Update Swagger/OpenAPI config fields."""
        swagger_fields = {k: v for k, v in kwargs.items() if k.startswith("swagger_")}
        return self.update_config(**swagger_fields) if swagger_fields else 0

    def set_caching(self, **kwargs) -> int:
        """Update caching config fields."""
        cache_fields = {k: v for k, v in kwargs.items() if k.startswith("caching_")}
        return self.update_config(**cache_fields) if cache_fields else 0

    def set_email(self, **kwargs) -> int:
        """Update email config fields."""
        email_fields = {k: v for k, v in kwargs.items() if k.startswith("email_")}
        return self.update_config(**email_fields) if email_fields else 0

    def set_r2dbc_pool(self, **kwargs) -> int:
        """Update R2DBC connection pool config fields."""
        pool_fields = {k: v for k, v in kwargs.items() if k.startswith("r2dbc_")}
        return self.update_config(**pool_fields) if pool_fields else 0

    def config_exists(self) -> bool:
        """Check if the app config row exists."""
        row = self.db.fetch_one(
            f"SELECT id FROM {self.TABLE} WHERE app_definition_id = %s",
            (self.app_id,),
        )
        return row is not None

    def delete_config(self) -> int:
        """Delete the app config row."""
        return self.db.execute(
            f"DELETE FROM {self.TABLE} WHERE app_definition_id = %s",
            (self.app_id,),
        )
