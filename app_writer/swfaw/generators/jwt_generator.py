"""JWT generator - populates JWT templates."""

from jinja2 import Template
from models.layer_objects import JWTAuthenticationLayerObject
from templates.jwt_templates import JWTTemplates


class JWTGenerator:
    """Generates JWT authentication Java code."""
    
    @staticmethod
    def generate_jwt_config(jwt_config: JWTAuthenticationLayerObject) -> str:
        """Generate JwtConfig Java code."""
        context = {
            'packageName': jwt_config.packageName,
            'jwtSecret': jwt_config.jwtSecret,
            'jwtExpiration': jwt_config.jwtExpiration,
            'refreshExpiration': jwt_config.refreshExpiration
        }
        template = Template(JWTTemplates.JWT_CONFIG_TEMPLATE)
        return template.render(context)
    
    @staticmethod
    def generate_jwt_service(jwt_config: JWTAuthenticationLayerObject) -> str:
        """Generate JwtService Java code."""
        context = {'packageName': jwt_config.packageName}
        template = Template(JWTTemplates.JWT_SERVICE_TEMPLATE)
        return template.render(context)
    
    @staticmethod
    def generate_auth_controller(jwt_config: JWTAuthenticationLayerObject) -> str:
        """Generate AuthController Java code."""
        context = {'packageName': jwt_config.packageName}
        template = Template(JWTTemplates.AUTH_CONTROLLER_TEMPLATE)
        return template.render(context)
