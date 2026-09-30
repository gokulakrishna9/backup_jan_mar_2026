"""Field manager for CRUD operations on entity fields (columns)."""

from typing import Optional, List, Dict, Any
from models.database_definition import Column
from .definition_manager import DefinitionManager


class FieldManager:
    """Manages CRUD operations on fields (columns) within entities."""
    
    def __init__(self, definition_manager: DefinitionManager):
        """Initialize the field manager.
        
        Args:
            definition_manager: DefinitionManager instance
        """
        self.def_manager = definition_manager
    
    def add_field(self, table_name: str, field_name: str, field_type: str,
                  primary_key: bool = False, nullable: bool = True,
                  unique: bool = False, auto_increment: bool = False,
                  default_value: Optional[str] = None) -> Column:
        """Add a new field to an entity.
        
        Args:
            table_name: Name of the table
            field_name: Name of the field
            field_type: SQL type of the field
            primary_key: Whether this is a primary key
            nullable: Whether the field can be null
            unique: Whether the field must be unique
            auto_increment: Whether the field auto-increments
            default_value: Default value for the field
            
        Returns:
            The created Column object
            
        Raises:
            ValueError: If table not found or field already exists
        """
        table = self.def_manager.get_table(table_name)
        if table is None:
            raise ValueError(f"Table '{table_name}' not found")
        
        # Check if field already exists
        if self.field_exists(table_name, field_name):
            raise ValueError(f"Field '{field_name}' already exists in table '{table_name}'")
        
        # Create new column
        new_column = Column(
            name=field_name,
            type=field_type,
            primaryKey=primary_key,
            nullable=nullable,
            unique=unique,
            autoIncrement=auto_increment,
            defaultValue=default_value
        )
        
        # Add to table
        table.columns.append(new_column)
        
        return new_column
    
    def remove_field(self, table_name: str, field_name: str) -> bool:
        """Remove a field from an entity.
        
        Args:
            table_name: Name of the table
            field_name: Name of the field to remove
            
        Returns:
            True if removed, False if not found
            
        Raises:
            ValueError: If table not found
        """
        table = self.def_manager.get_table(table_name)
        if table is None:
            raise ValueError(f"Table '{table_name}' not found")
        
        for i, column in enumerate(table.columns):
            if column.name == field_name:
                table.columns.pop(i)
                return True
        
        return False
    
    def update_field(self, table_name: str, field_name: str,
                    new_name: Optional[str] = None,
                    new_type: Optional[str] = None,
                    primary_key: Optional[bool] = None,
                    nullable: Optional[bool] = None,
                    unique: Optional[bool] = None,
                    auto_increment: Optional[bool] = None,
                    default_value: Optional[str] = None) -> bool:
        """Update a field's properties.
        
        Args:
            table_name: Name of the table
            field_name: Current name of the field
            new_name: New name for the field (optional)
            new_type: New SQL type (optional)
            primary_key: New primary key status (optional)
            nullable: New nullable status (optional)
            unique: New unique status (optional)
            auto_increment: New auto-increment status (optional)
            default_value: New default value (optional)
            
        Returns:
            True if updated, False if not found
            
        Raises:
            ValueError: If table not found or new name already exists
        """
        table = self.def_manager.get_table(table_name)
        if table is None:
            raise ValueError(f"Table '{table_name}' not found")
        
        column = self.get_field(table_name, field_name)
        if column is None:
            return False
        
        # Check if new name already exists
        if new_name and new_name != field_name:
            if self.field_exists(table_name, new_name):
                raise ValueError(f"Field '{new_name}' already exists in table '{table_name}'")
            column.name = new_name
        
        # Update other properties if provided
        if new_type is not None:
            column.type = new_type
        if primary_key is not None:
            column.primaryKey = primary_key
        if nullable is not None:
            column.nullable = nullable
        if unique is not None:
            column.unique = unique
        if auto_increment is not None:
            column.autoIncrement = auto_increment
        if default_value is not None:
            column.defaultValue = default_value
        
        return True
    
    def get_field(self, table_name: str, field_name: str) -> Optional[Column]:
        """Get a field by name.
        
        Args:
            table_name: Name of the table
            field_name: Name of the field
            
        Returns:
            Column object or None if not found
            
        Raises:
            ValueError: If table not found
        """
        table = self.def_manager.get_table(table_name)
        if table is None:
            raise ValueError(f"Table '{table_name}' not found")
        
        for column in table.columns:
            if column.name == field_name:
                return column
        
        return None
    
    def list_fields(self, table_name: str) -> List[str]:
        """List all field names in an entity.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of field names
            
        Raises:
            ValueError: If table not found
        """
        table = self.def_manager.get_table(table_name)
        if table is None:
            raise ValueError(f"Table '{table_name}' not found")
        
        return [column.name for column in table.columns]
    
    def field_exists(self, table_name: str, field_name: str) -> bool:
        """Check if a field exists in an entity.
        
        Args:
            table_name: Name of the table
            field_name: Name of the field
            
        Returns:
            True if exists, False otherwise
        """
        try:
            return self.get_field(table_name, field_name) is not None
        except ValueError:
            return False
    
    def get_field_details(self, table_name: str, field_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a field.
        
        Args:
            table_name: Name of the table
            field_name: Name of the field
            
        Returns:
            Dictionary with field details or None if not found
        """
        column = self.get_field(table_name, field_name)
        if column is None:
            return None
        
        return {
            "name": column.name,
            "type": column.type,
            "primaryKey": column.primaryKey,
            "nullable": column.nullable,
            "unique": column.unique,
            "autoIncrement": column.autoIncrement,
            "defaultValue": column.defaultValue
        }
    
    def get_primary_keys(self, table_name: str) -> List[str]:
        """Get all primary key fields in an entity.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of primary key field names
            
        Raises:
            ValueError: If table not found
        """
        table = self.def_manager.get_table(table_name)
        if table is None:
            raise ValueError(f"Table '{table_name}' not found")
        
        return [column.name for column in table.columns if column.primaryKey]
