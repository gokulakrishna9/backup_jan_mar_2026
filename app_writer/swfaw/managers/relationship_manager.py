"""Relationship manager for CRUD operations on entity relationships."""

from typing import Optional, List, Dict, Any
from models.database_definition import Relationship
from .definition_manager import DefinitionManager


class RelationshipManager:
    """Manages CRUD operations on relationships between entities."""
    
    def __init__(self, definition_manager: DefinitionManager):
        """Initialize the relationship manager.
        
        Args:
            definition_manager: DefinitionManager instance
        """
        self.def_manager = definition_manager
    
    def add_relationship(self, source_table: str, target_table: str,
                        relationship_type: str, foreign_key: str,
                        referenced_column: str = "id") -> Relationship:
        """Add a new relationship between entities.
        
        Args:
            source_table: Name of the source table
            target_table: Name of the target table
            relationship_type: Type of relationship (OneToOne, OneToMany, ManyToOne, ManyToMany)
            foreign_key: Foreign key column name
            referenced_column: Referenced column in target table (default: "id")
            
        Returns:
            The created Relationship object
            
        Raises:
            ValueError: If tables not found or relationship already exists
        """
        # Validate tables exist
        source = self.def_manager.get_table(source_table)
        if source is None:
            raise ValueError(f"Source table '{source_table}' not found")
        
        target = self.def_manager.get_table(target_table)
        if target is None:
            raise ValueError(f"Target table '{target_table}' not found")
        
        # Validate relationship type
        valid_types = ["OneToOne", "OneToMany", "ManyToOne", "ManyToMany"]
        if relationship_type not in valid_types:
            raise ValueError(f"Invalid relationship type. Must be one of: {', '.join(valid_types)}")
        
        # Check if relationship already exists
        for rel in source.relationships:
            if (rel.targetTable == target_table and 
                rel.foreignKey == foreign_key and
                rel.type == relationship_type):
                raise ValueError(
                    f"Relationship already exists: {source_table} -> {target_table} "
                    f"({relationship_type}, {foreign_key})"
                )
        
        # Create new relationship
        new_relationship = Relationship(
            type=relationship_type,
            targetTable=target_table,
            foreignKey=foreign_key,
            referencedColumn=referenced_column
        )
        
        # Add to source table
        source.relationships.append(new_relationship)
        
        return new_relationship
    
    def remove_relationship(self, source_table: str, target_table: str,
                          foreign_key: Optional[str] = None) -> bool:
        """Remove a relationship between entities.
        
        Args:
            source_table: Name of the source table
            target_table: Name of the target table
            foreign_key: Foreign key column name (optional, removes all if not specified)
            
        Returns:
            True if removed, False if not found
            
        Raises:
            ValueError: If source table not found
        """
        source = self.def_manager.get_table(source_table)
        if source is None:
            raise ValueError(f"Source table '{source_table}' not found")
        
        removed = False
        relationships_to_keep = []
        
        for rel in source.relationships:
            if rel.targetTable == target_table:
                if foreign_key is None or rel.foreignKey == foreign_key:
                    removed = True
                    continue
            relationships_to_keep.append(rel)
        
        source.relationships = relationships_to_keep
        return removed
    
    def update_relationship(self, source_table: str, target_table: str,
                          foreign_key: str, new_type: Optional[str] = None,
                          new_foreign_key: Optional[str] = None,
                          new_referenced_column: Optional[str] = None) -> bool:
        """Update a relationship's properties.
        
        Args:
            source_table: Name of the source table
            target_table: Name of the target table
            foreign_key: Current foreign key column name
            new_type: New relationship type (optional)
            new_foreign_key: New foreign key column name (optional)
            new_referenced_column: New referenced column (optional)
            
        Returns:
            True if updated, False if not found
            
        Raises:
            ValueError: If source table not found or invalid relationship type
        """
        source = self.def_manager.get_table(source_table)
        if source is None:
            raise ValueError(f"Source table '{source_table}' not found")
        
        # Find the relationship
        relationship = None
        for rel in source.relationships:
            if rel.targetTable == target_table and rel.foreignKey == foreign_key:
                relationship = rel
                break
        
        if relationship is None:
            return False
        
        # Update properties
        if new_type is not None:
            valid_types = ["OneToOne", "OneToMany", "ManyToOne", "ManyToMany"]
            if new_type not in valid_types:
                raise ValueError(f"Invalid relationship type. Must be one of: {', '.join(valid_types)}")
            relationship.type = new_type
        
        if new_foreign_key is not None:
            relationship.foreignKey = new_foreign_key
        
        if new_referenced_column is not None:
            relationship.referencedColumn = new_referenced_column
        
        return True
    
    def get_relationships(self, table_name: str) -> List[Relationship]:
        """Get all relationships for an entity.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of Relationship objects
            
        Raises:
            ValueError: If table not found
        """
        table = self.def_manager.get_table(table_name)
        if table is None:
            raise ValueError(f"Table '{table_name}' not found")
        
        return table.relationships
    
    def get_relationship(self, source_table: str, target_table: str,
                        foreign_key: str) -> Optional[Relationship]:
        """Get a specific relationship.
        
        Args:
            source_table: Name of the source table
            target_table: Name of the target table
            foreign_key: Foreign key column name
            
        Returns:
            Relationship object or None if not found
            
        Raises:
            ValueError: If source table not found
        """
        source = self.def_manager.get_table(source_table)
        if source is None:
            raise ValueError(f"Source table '{source_table}' not found")
        
        for rel in source.relationships:
            if rel.targetTable == target_table and rel.foreignKey == foreign_key:
                return rel
        
        return None
    
    def list_relationships(self, table_name: str) -> List[Dict[str, Any]]:
        """List all relationships for an entity with details.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of relationship details
            
        Raises:
            ValueError: If table not found
        """
        relationships = self.get_relationships(table_name)
        
        return [
            {
                "type": rel.type,
                "targetTable": rel.targetTable,
                "foreignKey": rel.foreignKey,
                "referencedColumn": rel.referencedColumn
            }
            for rel in relationships
        ]
    
    def relationship_exists(self, source_table: str, target_table: str,
                          foreign_key: str) -> bool:
        """Check if a relationship exists.
        
        Args:
            source_table: Name of the source table
            target_table: Name of the target table
            foreign_key: Foreign key column name
            
        Returns:
            True if exists, False otherwise
        """
        try:
            return self.get_relationship(source_table, target_table, foreign_key) is not None
        except ValueError:
            return False
    
    def get_incoming_relationships(self, table_name: str) -> List[Dict[str, Any]]:
        """Get all relationships pointing to this entity.
        
        Args:
            table_name: Name of the target table
            
        Returns:
            List of incoming relationship details
            
        Raises:
            ValueError: If table not found
        """
        if not self.def_manager.table_exists(table_name):
            raise ValueError(f"Table '{table_name}' not found")
        
        db_def = self.def_manager.get_definition()
        incoming = []
        
        for table in db_def.tables:
            for rel in table.relationships:
                if rel.targetTable == table_name:
                    incoming.append({
                        "sourceTable": table.name,
                        "type": rel.type,
                        "foreignKey": rel.foreignKey,
                        "referencedColumn": rel.referencedColumn
                    })
        
        return incoming
