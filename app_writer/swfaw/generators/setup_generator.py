"""Setup generator - generates setup controller, service, and Thymeleaf templates."""

from jinja2 import Template
from templates.setup_templates import SetupTemplates


class SetupGenerator:
    """Generates setup components for initial super user creation."""
    
    @staticmethod
    def generate_setup_controller(package_name: str) -> str:
        """Generate SetupController Java code."""
        context = {
            'packageName': f"{package_name}.controller",
            'servicePackage': f"{package_name}.service"
        }
        template = Template(SetupTemplates.SETUP_CONTROLLER)
        return template.render(context)
    
    @staticmethod
    def generate_setup_service(package_name: str) -> str:
        """Generate SetupService Java code."""
        context = {
            'packageName': f"{package_name}.service",
            'entityPackage': f"{package_name}.entity",
            'repositoryPackage': f"{package_name}.repository"
        }
        template = Template(SetupTemplates.SETUP_SERVICE)
        return template.render(context)
    
    @staticmethod
    def generate_setup_page() -> str:
        """Generate Thymeleaf setup page HTML."""
        return SetupTemplates.THYMELEAF_SETUP_PAGE
    
    @staticmethod
    def generate_login_page() -> str:
        """Generate Thymeleaf login page HTML."""
        return SetupTemplates.THYMELEAF_LOGIN_PAGE
