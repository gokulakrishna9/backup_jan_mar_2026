"""POM generator - populates POM templates."""

from jinja2 import Template
from models.layer_objects import POMLayerObject
from templates.pom_templates import POMTemplates


class POMGenerator:
    """Generates Maven POM file."""
    
    @staticmethod
    def generate(pom: POMLayerObject) -> str:
        """Generate pom.xml file.
        
        Args:
            pom: POM layer object with all properties
            
        Returns:
            Generated XML as string
        """
        context = {
            'groupId': pom.groupId,
            'artifactId': pom.artifactId,
            'version': pom.version,
            'projectName': pom.projectName,
            'javaVersion': pom.javaVersion,
            'springBootVersion': pom.springBootVersion
        }
        
        template = Template(POMTemplates.POM_TEMPLATE)
        return template.render(context)
