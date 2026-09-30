"""Security generator - populates security templates."""

from jinja2 import Template
from models.layer_objects import SecurityConfigLayerObject
from templates.security_templates import SecurityTemplates


class SecurityGenerator:
    """Generates security configuration Java code."""

    @staticmethod
    def generate_web_security_properties(security_config: SecurityConfigLayerObject) -> str:
        """Generate WebSecurityProperties Java code."""
        context = {'packageName': security_config.packageName}
        template = Template(SecurityTemplates.WEB_SECURITY_PROPERTIES_TEMPLATE)
        return template.render(context)

    @staticmethod
    def generate_security_config(security_config: SecurityConfigLayerObject) -> str:
        """Generate SecurityConfig Java code."""
        base_package = security_config.packageName
        context = {
            'packageName': security_config.packageName,
            'securityPackage': f"{base_package.replace('.config', '.security')}",
            'exceptionPackage': f"{base_package.replace('.config', '.exception')}",
            'servicePackage': f"{base_package.replace('.config', '.service')}",
            'repositoryPackage': f"{base_package.replace('.config', '.repository')}",
            'authPackage': f"{base_package.replace('.config', '.auth')}",
        }
        template = Template(SecurityTemplates.SECURITY_CONFIG_TEMPLATE)
        return template.render(context)

    @staticmethod
    def generate_password_encoder_config(security_config: SecurityConfigLayerObject) -> str:
        """Generate PasswordEncoderConfig Java code."""
        context = {'packageName': security_config.packageName}
        template = Template(SecurityTemplates.PASSWORD_ENCODER_CONFIG_TEMPLATE)
        return template.render(context)
