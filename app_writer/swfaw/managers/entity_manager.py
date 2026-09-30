"""Entity manager for CRUD operations on entities (tables)."""

from typing import Optional, List, Dict, Any
from models.database_definition import Table, Column, Relationship
from .definition_manager import DefinitionManager


class EntityManager:
    """Manages CRUD operations on entities (tables) in the application definition."""
    
    def __init__(self, definition_manager: DefinitionManager):
        """Initialize the entity manager.
        
        Args:
            definition_manager: DefinitionManager instance
        """
        self.def_manager = definition_manager
    
    def add_entity(self, table_name: str, columns: Optional[List[Dict[str, Any]]] = None) -> Table:
        """Add a new entity (table) to the definition.
        
        Args:
            table_name: Name of the table
            columns: Optional list of column definitions
            
        Returns:
            The created Table object
            
        Raises:
            ValueError: If table already exists or definition not loaded
        """
        db_def = self.def_manager.get_definition()
        
        if self.def_manager.table_exists(table_name):
            raise ValueError(f"Table '{table_name}' already exists")
        
        # Create default columns if none provided
        if columns is None:
            columns = [
                {
                    "name": "id",
                    "type": "BIGINT",
                    "primaryKey": True,
                    "nullable": False,
                    "autoIncrement": True
                }
            ]
        
        # Create Column objects
        column_objects = []
        for col_def in columns:
            column = Column(
                name=col_def.get("name"),
                type=col_def.get("type"),
                primaryKey=col_def.get("primaryKey", False),
                nullable=col_def.get("nullable", True),
                unique=col_def.get("unique", False),
                autoIncrement=col_def.get("autoIncrement", False),
                defaultValue=col_def.get("defaultValue")
            )
            column_objects.append(column)
        
        # Create new table
        new_table = Table(
            name=table_name,
            columns=column_objects,
            relationships=[]
        )
        
        # Add to definition
        db_def.tables.append(new_table)
        
        return new_table
    
    def remove_entity(self, table_name: str) -> bool:
        """Remove an entity (table) from the definition.
        
        Args:
            table_name: Name of the table to remove
            
        Returns:
            True if removed, False if not found
            
        Raises:
            ValueError: If definition not loaded
        """
        db_def = self.def_manager.get_definition()
        
        for i, table in enumerate(db_def.tables):
            if table.name == table_name:
                # Remove the table
                db_def.tables.pop(i)
                
                # Remove relationships referencing this table
                for other_table in db_def.tables:
                    other_table.relationships = [
                        rel for rel in other_table.relationships
                        if rel.targetTable != table_name
                    ]
                
                return True
        
        return False
    
    def update_entity(self, table_name: str, new_name: Optional[str] = None) -> bool:
        """Update an entity's properties.
        
        Args:
            table_name: Current name of the table
            new_name: New name for the table (optional)
            
        Returns:
            True if updated, False if not found
            
        Raises:
            ValueError: If definition not loaded or new name already exists
        """
        db_def = self.def_manager.get_definition()
        
        table = self.def_manager.get_table(table_name)
        if table is None:
            return False
        
        if new_name:
            # Check if new name already exists
            if new_name != table_name and self.def_manager.table_exists(new_name):
                raise ValueError(f"Table '{new_name}' already exists")
            
            # Update table name
            old_name = table.name
            table.name = new_name
            
            # Update relationships referencing this table
            for other_table in db_def.tables:
                for rel in other_table.relationships:
                    if rel.targetTable == old_name:
                        rel.targetTable = new_name
        
        return True
    
    def get_entity(self, table_name: str) -> Optional[Table]:
        """Get an entity by name.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Table object or None if not found
        """
        return self.def_manager.get_table(table_name)
    
    def list_entities(self) -> List[str]:
        """List all entity names.
        
        Returns:
            List of table names
        """
        return self.def_manager.list_tables()
    
    def entity_exists(self, table_name: str) -> bool:
        """Check if an entity exists.
        
        Args:
            table_name: Name of the table
            
        Returns:
            True if exists, False otherwise
        """
        return self.def_manager.table_exists(table_name)
    
    def get_entity_details(self, table_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about an entity.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary with entity details or None if not found
        """
        table = self.get_entity(table_name)
        if table is None:
            return None
        
        return {
            "name": table.name,
            "columns": [
                {
                    "name": col.name,
                    "type": col.type,
                    "primaryKey": col.primaryKey,
                    "nullable": col.nullable,
                    "unique": col.unique,
                    "autoIncrement": col.autoIncrement,
                    "defaultValue": col.defaultValue
                }
                for col in table.columns
            ],
            "relationships": [
                {
                    "type": rel.type,
                    "targetTable": rel.targetTable,
                    "foreignKey": rel.foreignKey,
                    "referencedColumn": rel.referencedColumn
                }
                for rel in table.relationships
            ],
            "column_count": len(table.columns),
            "relationship_count": len(table.relationships)
        }
