"""Auth service generator - generates authentication service components."""

from jinja2 import Template
from templates.auth_service_templates import AuthServiceTemplates


class AuthServiceGenerator:
    """Generates authentication service Java code."""
    
    @staticmethod
    def generate_auth_service(package_name: str) -> str:
        """Generate AuthService Java code."""
        context = {
            'packageName': f"{package_name}.service",
            'entityPackage': f"{package_name}.entity",
            'repositoryPackage': f"{package_name}.repository",
            'authPackage': f"{package_name}.auth"
        }
        template = Template(AuthServiceTemplates.AUTH_SERVICE)
        return template.render(context)
    
    @staticmethod
    def generate_auth_controller(package_name: str) -> str:
        """Generate updated AuthController Java code."""
        context = {
            'packageName': f"{package_name}.controller",
            'servicePackage': f"{package_name}.service"
        }
        template = Template(AuthServiceTemplates.AUTH_CONTROLLER_UPDATED)
        return template.render(context)
    
    @staticmethod
    def generate_jwt_filter(package_name: str) -> str:
        """Generate JwtAuthenticationFilter Java code."""
        context = {
            'packageName': f"{package_name}.security",
            'authPackage': f"{package_name}.auth",
            'servicePackage': f"{package_name}.service",
            'exceptionPackage': f"{package_name}.exception"
        }
        template = Template(AuthServiceTemplates.JWT_AUTHENTICATION_FILTER)
        return template.render(context)
    
    @staticmethod
    def generate_security_context_holder(package_name: str) -> str:
        """Generate SecurityContextHolder utility Java code."""
        context = {
            'packageName': f"{package_name}.security",
            'entityPackage': f"{package_name}.entity",
            'authPackage': f"{package_name}.auth",
            'repositoryPackage': f"{package_name}.repository",
        }
        template = Template(AuthServiceTemplates.SECURITY_CONTEXT_HOLDER)
        return template.render(context)
    
    @staticmethod
    def generate_authorization_denied_handler(package_name: str) -> str:
        """Generate AuthorizationDeniedHandler Java code."""
        context = {
            'packageName': f"{package_name}.security",
            'exceptionPackage': f"{package_name}.exception"
        }
        template = Template(AuthServiceTemplates.AUTHORIZATION_DENIED_HANDLER)
        return template.render(context)
