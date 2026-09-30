"""Service transformer - converts entity properties to service properties."""

from models.layer_objects import EntityLayerObject, ServiceLayerObject


class ServiceTransformer:
    """Transforms entity properties into service properties."""
    
    @staticmethod
    def transform(entity: EntityLayerObject) -> ServiceLayerObject:
        """Transform entity to service properties.
        
        Args:
            entity: Entity layer object
            
        Returns:
            ServiceLayerObject
        """
        return ServiceLayerObject(
            entityName=entity.className,
            className=f"{entity.className}Service",
            packageName=entity.packageName.replace('.entity', '.service'),
            repositoryName=f"{entity.className}Repository",
            isRootEntity=entity.isRootEntity,
            hasAuthorization=True
        )
