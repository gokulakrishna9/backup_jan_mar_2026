"""Test transformer - converts entity properties to test properties."""

from models.layer_objects import EntityLayerObject, TestLayerObject


class TestTransformer:
    """Transforms entity properties into test properties."""
    
    @staticmethod
    def transform(entity: EntityLayerObject) -> TestLayerObject:
        """Transform entity to test properties.
        
        Args:
            entity: Entity layer object
            
        Returns:
            TestLayerObject
        """
        return TestLayerObject(
            entityName=entity.className,
            className=f"{entity.className}ServiceTest",
            packageName=entity.packageName.replace('.entity', '.service'),
            serviceName=f"{entity.className}Service",
            isRootEntity=entity.isRootEntity
        )
