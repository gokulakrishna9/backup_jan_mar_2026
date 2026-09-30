"""Database security manager — CRUD on security tables (Tier 4a).

Covers: swfaw_security_config, swfaw_security_oauth2_provider,
        swfaw_security_cors, swfaw_security_public_endpoint
"""

import json
from typing import Optional, Dict, Any, List
from .db_connection import DbConnection


class DbSecurityManager:
    """CRUD operations on security configuration tables.
    
    Usage:
        sm = DbSecurityManager(db, app_id=1)
        
        # Get/create security config
        config = sm.get_config()
        config_id = sm.create_config(jwt_expiration=86400000)
        
        # Update JWT settings
        sm.update_config(jwt_expiration=7200000, jwt_algorithm="HS512")
        
        # CORS
        sm.set_cors(allowed_origins_json=["http://localhost:3000"])
        
        # OAuth2 providers
        sm.add_oauth2_provider("google", client_id="...", client_secret="...")
        
        # Public endpoints
        sm.add_public_endpoint("/api/health")
    """

    def __init__(self, db: DbConnection, app_id: int):
        self.db = db
        self.app_id = app_id

    # ------------------------------------------------------------------
    # Security Config (singleton per app)
    # ------------------------------------------------------------------

    def get_config(self) -> Optional[Dict[str, Any]]:
        """Get the security config for this app."""
        return self.db.fetch_one(
            "SELECT * FROM swfaw_security_config WHERE app_definition_id = %s",
            (self.app_id,),
        )

    def get_config_id(self) -> Optional[int]:
        """Get the security_config row ID (needed for child tables)."""
        row = self.db.fetch_one(
            "SELECT id FROM swfaw_security_config WHERE app_definition_id = %s",
            (self.app_id,),
        )
        return row["id"] if row else None

    def create_config(self, **kwargs) -> int:
        """Create the security config row. Returns the new row ID."""
        kwargs.setdefault("app_definition_id", self.app_id)
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join(["%s"] * len(kwargs))
        sql = f"INSERT INTO swfaw_security_config ({columns}) VALUES ({placeholders})"
        return self.db.insert(sql, tuple(kwargs.values()))

    def update_config(self, **kwargs) -> int:
        """Update security config fields.
        
        Example:
            sm.update_config(jwt_expiration=7200000, jwt_algorithm="HS512")
        """
        if not kwargs:
            return 0
        set_clause = ", ".join(f"{col} = %s" for col in kwargs)
        sql = f"UPDATE swfaw_security_config SET {set_clause} WHERE app_definition_id = %s"
        return self.db.execute(sql, tuple(kwargs.values()) + (self.app_id,))

    # ------------------------------------------------------------------
    # OAuth2 Providers
    # ------------------------------------------------------------------

    def list_oauth2_providers(self) -> List[Dict[str, Any]]:
        """List all OAuth2 providers for this app's security config."""
        config_id = self.get_config_id()
        if config_id is None:
            return []
        rows = self.db.fetch_all(
            "SELECT * FROM swfaw_security_oauth2_provider WHERE security_config_id = %s",
            (config_id,),
        )
        for r in rows:
            if isinstance(r.get("scopes_json"), str):
                r["scopes_json"] = json.loads(r["scopes_json"])
        return rows

    def add_oauth2_provider(
        self,
        provider_name: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scopes: Optional[List[str]] = None,
    ) -> int:
        """Add an OAuth2 provider."""
        config_id = self.get_config_id()
        if config_id is None:
            raise ValueError("Security config not found. Create it first.")
        scopes_json = json.dumps(scopes or ["openid", "profile", "email"])
        sql = (
            "INSERT INTO swfaw_security_oauth2_provider "
            "(security_config_id, provider_name, client_id, client_secret, "
            "redirect_uri, scopes_json) VALUES (%s, %s, %s, %s, %s, %s)"
        )
        return self.db.insert(sql, (
            config_id, provider_name, client_id, client_secret,
            redirect_uri, scopes_json,
        ))

    def remove_oauth2_provider(self, provider_name: str) -> int:
        """Remove an OAuth2 provider by name."""
        config_id = self.get_config_id()
        if config_id is None:
            return 0
        return self.db.execute(
            "DELETE FROM swfaw_security_oauth2_provider "
            "WHERE security_config_id = %s AND provider_name = %s",
            (config_id, provider_name),
        )

    # ------------------------------------------------------------------
    # CORS
    # ------------------------------------------------------------------

    def get_cors(self) -> Optional[Dict[str, Any]]:
        """Get the CORS config."""
        config_id = self.get_config_id()
        if config_id is None:
            return None
        row = self.db.fetch_one(
            "SELECT * FROM swfaw_security_cors WHERE security_config_id = %s",
            (config_id,),
        )
        if row:
            for key in ("allowed_origins_json", "allowed_methods_json",
                        "allowed_headers_json", "exposed_headers_json"):
                if isinstance(row.get(key), str):
                    row[key] = json.loads(row[key])
        return row

    def set_cors(self, **kwargs) -> int:
        """Create or update the CORS config.
        
        Example:
            sm.set_cors(
                cors_enabled=1,
                allowed_origins_json=["http://localhost:3000"],
                allowed_methods_json=["GET", "POST", "PUT", "DELETE"],
            )
        """
        config_id = self.get_config_id()
        if config_id is None:
            raise ValueError("Security config not found. Create it first.")

        # Auto-serialize JSON columns
        for col in list(kwargs.keys()):
            if col.endswith("_json") and not isinstance(kwargs[col], str):
                kwargs[col] = json.dumps(kwargs[col])

        existing = self.db.fetch_one(
            "SELECT id FROM swfaw_security_cors WHERE security_config_id = %s",
            (config_id,),
        )
        if existing:
            set_clause = ", ".join(f"{col} = %s" for col in kwargs)
            sql = f"UPDATE swfaw_security_cors SET {set_clause} WHERE security_config_id = %s"
            return self.db.execute(sql, tuple(kwargs.values()) + (config_id,))
        else:
            kwargs["security_config_id"] = config_id
            columns = ", ".join(kwargs.keys())
            placeholders = ", ".join(["%s"] * len(kwargs))
            sql = f"INSERT INTO swfaw_security_cors ({columns}) VALUES ({placeholders})"
            return self.db.insert(sql, tuple(kwargs.values()))

    # ------------------------------------------------------------------
    # Public Endpoints
    # ------------------------------------------------------------------

    def list_public_endpoints(self) -> List[str]:
        """List all public endpoint patterns."""
        config_id = self.get_config_id()
        if config_id is None:
            return []
        rows = self.db.fetch_all(
            "SELECT endpoint_pattern FROM swfaw_security_public_endpoint "
            "WHERE security_config_id = %s ORDER BY sort_order",
            (config_id,),
        )
        return [r["endpoint_pattern"] for r in rows]

    def add_public_endpoint(self, pattern: str, sort_order: int = 0) -> int:
        """Add a public endpoint pattern."""
        config_id = self.get_config_id()
        if config_id is None:
            raise ValueError("Security config not found. Create it first.")
        sql = (
            "INSERT INTO swfaw_security_public_endpoint "
            "(security_config_id, endpoint_pattern, sort_order) VALUES (%s, %s, %s)"
        )
        return self.db.insert(sql, (config_id, pattern, sort_order))

    def remove_public_endpoint(self, pattern: str) -> int:
        """Remove a public endpoint by pattern."""
        config_id = self.get_config_id()
        if config_id is None:
            return 0
        return self.db.execute(
            "DELETE FROM swfaw_security_public_endpoint "
            "WHERE security_config_id = %s AND endpoint_pattern = %s",
            (config_id, pattern),
        )
