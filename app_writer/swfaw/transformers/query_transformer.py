"""Query transformer - creates query layer properties from entities."""

from typing import List
from models.layer_objects import EntityLayerObject, QueryLayerObject


class QueryTransformer:
    """Transforms entity list into query layer properties."""
    
    @staticmethod
    def transform(entities: List[EntityLayerObject], package_name: str = "com.example") -> List[QueryLayerObject]:
        """Transform entities to query layer properties.
        
        Args:
            entities: List of all entity layer objects
            package_name: Base package name
            
        Returns:
            List of QueryLayerObject (one per entity, initially empty)
        """
        query_layers = []
        
        for entity in entities:
            query_layer = QueryLayerObject(
                entityName=entity.className,
                queries=[],  # Empty by default - user will add custom queries
                packageName=f"{package_name}.query"
            )
            query_layers.append(query_layer)
        
        return query_layers
