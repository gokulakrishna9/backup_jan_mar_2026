"""Authorization transformer - creates authorization service properties."""

from typing import List
from models.layer_objects import EntityLayerObject, AuthorizationServiceLayerObject


class AuthorizationTransformer:
    """Transforms entity list into authorization service properties."""
    
    @staticmethod
    def transform(entities: List[EntityLayerObject], package_name: str = "com.example") -> AuthorizationServiceLayerObject:
        """Transform entities to authorization service properties.
        
        Args:
            entities: List of all entity layer objects
            package_name: Base package name
            
        Returns:
            AuthorizationServiceLayerObject
        """
        # Extract root entity names
        root_entities = [entity.className for entity in entities if entity.isRootEntity]
        
        return AuthorizationServiceLayerObject(
            packageName=f"{package_name}.security",
            rootEntities=root_entities
        )
