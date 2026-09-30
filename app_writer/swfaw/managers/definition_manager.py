"""Main definition manager for loading and saving application definitions."""

import json
from pathlib import Path
from typing import Optional, Dict, Any, List
from models.database_definition import DatabaseDefinition, ProjectMetadata, DatabaseConfig, Table
from utils.definition_splitter import split_definition, load_split_definition


class DefinitionManager:
    """Manages loading, saving, and basic operations on application definitions.

    Supports an optional DefinitionStore backend. When provided, load() and save()
    delegate to the store. When omitted, the original JSON file behavior is used.
    """
    
    def __init__(self, output_dir: str, store=None):
        """Initialize the definition manager.
        
        Args:
            output_dir: Path to the application output directory
            store: Optional DefinitionStore backend (JsonStore or DbStore).
                   If None, uses the original JSON file operations directly.
        """
        self.output_dir = Path(output_dir)
        self.definitions_dir = self.output_dir / "application_definitions"
        self.db_def: Optional[DatabaseDefinition] = None
        self._store = store
        self._store_identifier: Optional[str] = None  # app_id for DB, output_dir for JSON
        
    def load(self, identifier: str = None) -> DatabaseDefinition:
        """Load application definition.

        When a store is configured, delegates to store.load().
        Otherwise uses the original JSON file loading.
        
        Args:
            identifier: For DB store, the app_id string. Ignored for JSON store.
        
        Returns:
            DatabaseDefinition object
        """
        if self._store is not None:
            ident = identifier or str(self.output_dir)
            self._store_identifier = ident
            self.db_def = self._store.load(ident)
            return self.db_def

        # Original JSON behavior
        if not self.definitions_dir.exists():
            raise FileNotFoundError(f"Definitions directory not found: {self.definitions_dir}")
        
        manifest_path = self.definitions_dir / "webflux_manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest file not found: {manifest_path}")
        
        self.db_def = load_split_definition(str(self.output_dir))
        return self.db_def
    
    def save(self) -> Dict[str, str]:
        """Save the current application definition.
        
        When a store is configured, delegates to store.save().
        Otherwise uses the original JSON file saving.
        
        Returns:
            Dictionary of file paths (JSON) or {"identifier": app_id} (DB)
        """
        if self.db_def is None:
            raise ValueError("No definition loaded. Call load() first.")

        if self._store is not None:
            result = self._store.save(self.db_def, str(self.output_dir))
            self._store_identifier = result
            return {"identifier": result}
        
        # Original JSON behavior
        file_paths = split_definition(self.db_def, str(self.output_dir))
        return file_paths
    
    def get_definition(self) -> DatabaseDefinition:
        """Get the current database definition.
        
        Returns:
            DatabaseDefinition object
            
        Raises:
            ValueError: If no definition is loaded
        """
        if self.db_def is None:
            raise ValueError("No definition loaded. Call load() first.")
        return self.db_def
    
    def get_project_metadata(self) -> ProjectMetadata:
        """Get project metadata.
        
        Returns:
            ProjectMetadata object
        """
        if self.db_def is None:
            raise ValueError("No definition loaded. Call load() first.")
        return self.db_def.projectMetadata
    
    def update_project_metadata(self, **kwargs) -> None:
        """Update project metadata fields.
        
        Args:
            **kwargs: Fields to update (name, applicationName, groupId, etc.)
        """
        if self.db_def is None:
            raise ValueError("No definition loaded. Call load() first.")
        
        metadata = self.db_def.projectMetadata
        for key, value in kwargs.items():
            if hasattr(metadata, key):
                setattr(metadata, key, value)
    
    def get_database_config(self) -> DatabaseConfig:
        """Get database configuration.
        
        Returns:
            DatabaseConfig object
        """
        if self.db_def is None:
            raise ValueError("No definition loaded. Call load() first.")
        return self.db_def.projectMetadata.database
    
    def update_database_config(self, **kwargs) -> None:
        """Update database configuration fields.
        
        Args:
            **kwargs: Fields to update (type, host, port, name, etc.)
        """
        if self.db_def is None:
            raise ValueError("No definition loaded. Call load() first.")
        
        db_config = self.db_def.projectMetadata.database
        for key, value in kwargs.items():
            if hasattr(db_config, key):
                setattr(db_config, key, value)
    
    def list_tables(self) -> List[str]:
        """List all table names in the definition.
        
        Returns:
            List of table names
        """
        if self.db_def is None:
            raise ValueError("No definition loaded. Call load() first.")
        return [table.name for table in self.db_def.tables]
    
    def get_table(self, table_name: str) -> Optional[Table]:
        """Get a table by name.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Table object or None if not found
        """
        if self.db_def is None:
            raise ValueError("No definition loaded. Call load() first.")
        
        for table in self.db_def.tables:
            if table.name == table_name:
                return table
        return None
    
    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists.
        
        Args:
            table_name: Name of the table
            
        Returns:
            True if table exists, False otherwise
        """
        return self.get_table(table_name) is not None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the application definition.
        
        Returns:
            Dictionary with statistics
        """
        if self.db_def is None:
            raise ValueError("No definition loaded. Call load() first.")
        
        total_columns = sum(len(table.columns) for table in self.db_def.tables)
        tables_with_relationships = sum(1 for table in self.db_def.tables if table.relationships)
        total_relationships = sum(len(table.relationships) for table in self.db_def.tables)
        
        return {
            "project_name": self.db_def.projectMetadata.applicationName,
            "total_tables": len(self.db_def.tables),
            "total_columns": total_columns,
            "tables_with_relationships": tables_with_relationships,
            "total_relationships": total_relationships,
            "database_type": self.db_def.projectMetadata.database.type,
            "database_name": self.db_def.projectMetadata.database.name
        }
