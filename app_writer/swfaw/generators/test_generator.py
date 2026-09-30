"""Test generator - populates test templates."""

from jinja2 import Template
from models.layer_objects import TestLayerObject
from templates.test_templates import TestTemplates


class TestGenerator:
    """Generates test Java code from test layer object."""
    
    @staticmethod
    def generate(test: TestLayerObject) -> str:
        """Generate test Java code.
        
        Args:
            test: Test layer object with all properties
            
        Returns:
            Generated Java code as string
        """
        # Determine package names
        base_package = test.packageName.replace('.service', '')
        entity_package = f"{base_package}.entity"
        service_package = f"{base_package}.service"
        
        # Prepare template context
        context = {
            'packageName': test.packageName,
            'entityPackage': entity_package,
            'servicePackage': service_package,
            'entityName': test.entityName,
            'className': test.className,
            'serviceName': test.serviceName
        }
        
        # Render template
        template = Template(TestTemplates.TEST_TEMPLATE)
        return template.render(context)
