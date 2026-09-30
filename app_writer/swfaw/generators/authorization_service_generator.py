"""Authorization service generator - generates role-based authorization components."""

from jinja2 import Template
from templates.authorization_service_templates import AuthorizationServiceTemplates


class AuthorizationServiceGenerator:
    """Generates authorization service Java code."""

    @staticmethod
    def generate_role_authorization_service(package_name: str) -> str:
        """Generate RoleAuthorizationService Java code."""
        context = {
            'packageName': f"{package_name}.service",
            'repositoryPackage': f"{package_name}.repository"
        }
        template = Template(AuthorizationServiceTemplates.ROLE_AUTHORIZATION_SERVICE)
        return template.render(context)

    @staticmethod
    def generate_authorization_web_filter(package_name: str) -> str:
        """Generate AuthorizationWebFilter Java code."""
        context = {
            'packageName': f"{package_name}.security",
            'entityPackage': f"{package_name}.entity",
            'repositoryPackage': f"{package_name}.repository",
            'securityPackage': f"{package_name}.security",
            'servicePackage': f"{package_name}.service",
            'authPackage': f"{package_name}.auth"
        }
        template = Template(AuthorizationServiceTemplates.AUTHORIZATION_WEB_FILTER)
        return template.render(context)

    @staticmethod
    def generate_entity_table_annotation(package_name: str) -> str:
        """Generate @EntityTable annotation Java code."""
        context = {
            'packageName': f"{package_name}.security"
        }
        template = Template(AuthorizationServiceTemplates.ENTITY_TABLE_ANNOTATION)
        return template.render(context)

    @staticmethod
    def generate_table_access_annotation(package_name: str) -> str:
        """Generate @TableAccess annotation Java code."""
        context = {
            'packageName': f"{package_name}.security"
        }
        template = Template(AuthorizationServiceTemplates.TABLE_ACCESS_ANNOTATION)
        return template.render(context)

    @staticmethod
    def generate_query_access_annotation(package_name: str) -> str:
        """Generate @QueryAccess annotation Java code."""
        context = {
            'packageName': f"{package_name}.security"
        }
        template = Template(AuthorizationServiceTemplates.QUERY_ACCESS_ANNOTATION)
        return template.render(context)

    @staticmethod
    def generate_authorization_aspect(package_name: str) -> str:
        """Generate AuthorizationAspect Java code."""
        context = {
            'packageName': f"{package_name}.security",
            'entityPackage': f"{package_name}.entity",
            'repositoryPackage': f"{package_name}.repository",
            'securityPackage': f"{package_name}.security",
            'servicePackage': f"{package_name}.service",
            'authPackage': f"{package_name}.auth"
        }
        template = Template(AuthorizationServiceTemplates.AUTHORIZATION_ASPECT)
        return template.render(context)
