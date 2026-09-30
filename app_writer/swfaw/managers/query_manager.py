"""Query manager for CRUD operations on query definitions."""

from typing import List, Dict, Any, Optional
from .layer_manager import LayerManager


class QueryManager:
    """Manager for query layer operations."""
    
    def __init__(self, layer_manager: LayerManager):
        """Initialize QueryManager.
        
        Args:
            layer_manager: LayerManager instance
        """
        self.layer_manager = layer_manager
    
    def add_query(self, entity_name: str, query_def: Dict[str, Any]) -> bool:
        """Add a custom query to an entity.
        
        Args:
            entity_name: Entity name
            query_def: Query definition dictionary
            
        Returns:
            True if successful
        """
        # Get existing queries for entity
        queries = self.layer_manager.get("query", f"queries.{entity_name}", [])
        
        # Add new query
        queries.append(query_def)
        
        # Update
        self.layer_manager.set("query", f"queries.{entity_name}", queries)
        return True
    
    def remove_query(self, entity_name: str, query_name: str) -> bool:
        """Remove a query from an entity.
        
        Args:
            entity_name: Entity name
            query_name: Query name to remove
            
        Returns:
            True if successful
        """
        queries = self.layer_manager.get("query", f"queries.{entity_name}", [])
        queries = [q for q in queries if q.get('name') != query_name]
        self.layer_manager.set("query", f"queries.{entity_name}", queries)
        return True

    
    def get_query(self, entity_name: str, query_name: str) -> Optional[Dict[str, Any]]:
        """Get a specific query definition.
        
        Args:
            entity_name: Entity name
            query_name: Query name
            
        Returns:
            Query definition or None
        """
        queries = self.layer_manager.get("query", f"queries.{entity_name}", [])
        for query in queries:
            if query.get('name') == query_name:
                return query
        return None
    
    def update_query(self, entity_name: str, query_name: str, updates: Dict[str, Any]) -> bool:
        """Update a query definition.
        
        Args:
            entity_name: Entity name
            query_name: Query name
            updates: Fields to update
            
        Returns:
            True if successful
        """
        queries = self.layer_manager.get("query", f"queries.{entity_name}", [])
        for query in queries:
            if query.get('name') == query_name:
                query.update(updates)
                break
        self.layer_manager.set("query", f"queries.{entity_name}", queries)
        return True
    
    def list_queries(self, entity_name: str) -> List[Dict[str, Any]]:
        """List all queries for an entity.
        
        Args:
            entity_name: Entity name
            
        Returns:
            List of query definitions
        """
        return self.layer_manager.get("query", f"queries.{entity_name}", [])
    
    def list_all_queries(self) -> Dict[str, List[Dict[str, Any]]]:
        """List all queries for all entities.
        
        Returns:
            Dictionary mapping entity names to query lists
        """
        all_queries = self.layer_manager.get("query", "queries", {})
        return all_queries
