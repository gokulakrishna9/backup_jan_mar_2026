"""Auth entity generator - generates authentication/authorization entities."""

from jinja2 import Template
from templates.auth_entity_templates import AuthEntityTemplates


class AuthEntityGenerator:
    """Generates authentication and authorization entity Java code."""
    
    # --- Retained entities ---

    @staticmethod
    def generate_system_config(package_name: str) -> str:
        context = {'packageName': f"{package_name}.entity"}
        template = Template(AuthEntityTemplates.SYSTEM_CONFIG_ENTITY)
        return template.render(context)
    
    @staticmethod
    def generate_auth_user(package_name: str) -> str:
        context = {'packageName': f"{package_name}.entity"}
        template = Template(AuthEntityTemplates.AUTH_USER_ENTITY)
        return template.render(context)
    
    @staticmethod
    def generate_access_audit_log(package_name: str) -> str:
        context = {'packageName': f"{package_name}.entity"}
        template = Template(AuthEntityTemplates.ACCESS_AUDIT_LOG_ENTITY)
        return template.render(context)

    # --- New entities ---

    @staticmethod
    def generate_user_role(package_name: str) -> str:
        context = {'packageName': f"{package_name}.entity"}
        template = Template(AuthEntityTemplates.USER_ROLE_ENTITY)
        return template.render(context)

    @staticmethod
    def generate_record_owner(package_name: str) -> str:
        context = {'packageName': f"{package_name}.entity"}
        template = Template(AuthEntityTemplates.RECORD_OWNER_ENTITY)
        return template.render(context)

    @staticmethod
    def generate_query_group(package_name: str) -> str:
        context = {'packageName': f"{package_name}.entity"}
        template = Template(AuthEntityTemplates.QUERY_GROUP_ENTITY)
        return template.render(context)

    @staticmethod
    def generate_query_group_query(package_name: str) -> str:
        context = {'packageName': f"{package_name}.entity"}
        template = Template(AuthEntityTemplates.QUERY_GROUP_QUERY_ENTITY)
        return template.render(context)

    @staticmethod
    def generate_query_group_member(package_name: str) -> str:
        context = {'packageName': f"{package_name}.entity"}
        template = Template(AuthEntityTemplates.QUERY_GROUP_MEMBER_ENTITY)
        return template.render(context)

    @staticmethod
    def generate_query_group_record(package_name: str) -> str:
        context = {'packageName': f"{package_name}.entity"}
        template = Template(AuthEntityTemplates.QUERY_GROUP_RECORD_ENTITY)
        return template.render(context)
