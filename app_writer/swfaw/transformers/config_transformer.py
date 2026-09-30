"""Config transformer - creates application config properties."""

from models.database_definition import ProjectMetadata
from models.layer_objects import ApplicationConfigLayerObject


class ConfigTransformer:
    """Transforms project metadata into application config properties."""
    
    @staticmethod
    def transform(metadata: ProjectMetadata) -> ApplicationConfigLayerObject:
        """Transform project metadata to application config properties.
        
        Args:
            metadata: Project metadata from database definition
            
        Returns:
            ApplicationConfigLayerObject
        """
        return ApplicationConfigLayerObject(
            projectName=metadata.name,
            groupId=metadata.groupId,
            artifactId=metadata.artifactId,
            packageName=metadata.groupId,
            port=metadata.port,
            databaseType=metadata.database.type,
            databaseHost=metadata.database.host,
            databasePort=metadata.database.port,
            databaseName=metadata.database.name
        )
