"""POM transformer - creates Maven POM properties."""

from models.database_definition import ProjectMetadata
from models.layer_objects import POMLayerObject


class POMTransformer:
    """Transforms project metadata into POM properties."""
    
    @staticmethod
    def transform(metadata: ProjectMetadata) -> POMLayerObject:
        """Transform project metadata to POM properties.
        
        Args:
            metadata: Project metadata from database definition
            
        Returns:
            POMLayerObject
        """
        return POMLayerObject(
            groupId=metadata.groupId,
            artifactId=metadata.artifactId,
            version=metadata.version,
            projectName=metadata.name,
            javaVersion="17",
            springBootVersion="3.2.0"
        )
