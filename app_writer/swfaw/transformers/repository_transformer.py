"""Repository transformer - converts entity properties to repository properties."""

from models.layer_objects import EntityLayerObject, RepositoryLayerObject


class RepositoryTransformer:
    """Transforms entity properties into repository properties."""
    
    @staticmethod
    def transform(entity: EntityLayerObject) -> RepositoryLayerObject:
        """Transform entity to repository properties.
        
        Args:
            entity: Entity layer object
            
        Returns:
            RepositoryLayerObject
        """
        # Find ID type from primary key field
        id_type = 'Long'
        for field in entity.fields:
            if field.isPrimaryKey:
                id_type = field.javaType
                break
        
        return RepositoryLayerObject(
            entityName=entity.className,
            className=f"{entity.className}Repository",
            packageName=entity.packageName.replace('.entity', '.repository'),
            idType=id_type,
            hasCustomQueries=False,
            customQueries=[],
            hasSoftDelete=entity.hasSoftDelete,
            hasAuthorization=True
        )
