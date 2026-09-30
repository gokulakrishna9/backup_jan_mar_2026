"""Config generator - populates configuration templates."""

from jinja2 import Template
from models.layer_objects import ApplicationConfigLayerObject
from templates.config_templates import ConfigTemplates


class ConfigGenerator:
    """Generates application configuration files."""
    
    @staticmethod
    def generate_application_yml(config: ApplicationConfigLayerObject) -> str:
        """Generate application.yml file."""
        context = {
            'projectName': config.projectName,
            'databaseType': config.databaseType,
            'databaseHost': config.databaseHost,
            'databasePort': config.databasePort,
            'databaseName': config.databaseName,
            'port': config.port,
            'packageName': config.packageName
        }
        template = Template(ConfigTemplates.APPLICATION_YML_TEMPLATE)
        return template.render(context)
    
    @staticmethod
    def generate_database_config(config: ApplicationConfigLayerObject) -> str:
        """Generate DatabaseConfig Java code."""
        context = {'packageName': f"{config.packageName}.config"}
        template = Template(ConfigTemplates.DATABASE_CONFIG_TEMPLATE)
        return template.render(context)
    
    @staticmethod
    def generate_swagger_config(config: ApplicationConfigLayerObject) -> str:
        """Generate SwaggerConfig Java code."""
        context = {
            'packageName': f"{config.packageName}.config",
            'projectName': config.projectName
        }
        template = Template(ConfigTemplates.SWAGGER_CONFIG_TEMPLATE)
        return template.render(context)
    
    @staticmethod
    def generate_main_application(config: ApplicationConfigLayerObject) -> str:
        """Generate main Application Java code."""
        context = {'packageName': config.packageName}
        template = Template(ConfigTemplates.MAIN_APPLICATION_TEMPLATE)
        return template.render(context)
