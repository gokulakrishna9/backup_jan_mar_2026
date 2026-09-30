"""Filter manager for CRUD operations on filter definitions."""

from typing import List, Dict, Any, Optional
from .layer_manager import LayerManager


class FilterManager:
    """Manager for filter layer operations."""
    
    def __init__(self, layer_manager: LayerManager):
        """Initialize FilterManager.
        
        Args:
            layer_manager: LayerManager instance
        """
        self.layer_manager = layer_manager
    
    def add_filter_field(self, entity_name: str, field_def: Dict[str, Any]) -> bool:
        """Add a filter field to an entity.
        
        Args:
            entity_name: Entity name
            field_def: Filter field definition
            
        Returns:
            True if successful
        """
        fields = self.layer_manager.get("filter", f"filters.{entity_name}.fields", [])
        fields.append(field_def)
        self.layer_manager.set("filter", f"filters.{entity_name}.fields", fields)
        return True
    
    def remove_filter_field(self, entity_name: str, field_name: str) -> bool:
        """Remove a filter field from an entity.
        
        Args:
            entity_name: Entity name
            field_name: Field name to remove
            
        Returns:
            True if successful
        """
        fields = self.layer_manager.get("filter", f"filters.{entity_name}.fields", [])
        fields = [f for f in fields if f.get('name') != field_name]
        self.layer_manager.set("filter", f"filters.{entity_name}.fields", fields)
        return True

    
    def get_filter_field(self, entity_name: str, field_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific filter field definition.
        
        Args:
            entity_name: Entity name
            field_name: Field name
            
        Returns:
            Filter field definition or None
        """
        fields = self.layer_manager.get("filter", f"filters.{entity_name}.fields", [])
        for field in fields:
            if field.get('name') == field_name:
                return field
        return None
    
    def update_filter_field(self, entity_name: str, field_name: str, updates: Dict[str, Any]) -> bool:
        """Update a filter field definition.
        
        Args:
            entity_name: Entity name
            field_name: Field name
            updates: Fields to update
            
        Returns:
            True if successful
        """
        fields = self.layer_manager.get("filter", f"filters.{entity_name}.fields", [])
        for field in fields:
            if field.get('name') == field_name:
                field.update(updates)
                break
        self.layer_manager.set("filter", f"filters.{entity_name}.fields", fields)
        return True
    
    def list_filter_fields(self, entity_name: str) -> List[Dict[str, Any]]:
        """List all filter fields for an entity.
        
        Args:
            entity_name: Entity name
            
        Returns:
            List of filter field definitions
        """
        return self.layer_manager.get("filter", f"filters.{entity_name}.fields", [])
    
    def list_all_filters(self) -> Dict[str, Any]:
        """List all filters for all entities.
        
        Returns:
            Dictionary mapping entity names to filter definitions
        """
        return self.layer_manager.get("filter", "filters", {})
