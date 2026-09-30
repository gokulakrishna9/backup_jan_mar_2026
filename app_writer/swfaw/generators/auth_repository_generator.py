"""Auth repository generator - generates authentication/authorization repositories."""

from jinja2 import Template
from templates.auth_repository_templates import AuthRepositoryTemplates


class AuthRepositoryGenerator:
    """Generates authentication and authorization repository Java code."""

    # --- Retained repositories ---

    @staticmethod
    def generate_system_config_repository(package_name: str) -> str:
        context = {
            'packageName': f"{package_name}.repository",
            'entityPackage': f"{package_name}.entity"
        }
        template = Template(AuthRepositoryTemplates.SYSTEM_CONFIG_REPOSITORY)
        return template.render(context)

    @staticmethod
    def generate_auth_user_repository(package_name: str) -> str:
        context = {
            'packageName': f"{package_name}.repository",
            'entityPackage': f"{package_name}.entity"
        }
        template = Template(AuthRepositoryTemplates.AUTH_USER_REPOSITORY)
        return template.render(context)

    @staticmethod
    def generate_access_audit_log_repository(package_name: str) -> str:
        context = {
            'packageName': f"{package_name}.repository",
            'entityPackage': f"{package_name}.entity"
        }
        template = Template(AuthRepositoryTemplates.ACCESS_AUDIT_LOG_REPOSITORY)
        return template.render(context)

    # --- New repositories ---

    @staticmethod
    def generate_user_role_repository(package_name: str) -> str:
        context = {
            'packageName': f"{package_name}.repository",
            'entityPackage': f"{package_name}.entity"
        }
        template = Template(AuthRepositoryTemplates.USER_ROLE_REPOSITORY)
        return template.render(context)

    @staticmethod
    def generate_record_owner_repository(package_name: str) -> str:
        context = {
            'packageName': f"{package_name}.repository",
            'entityPackage': f"{package_name}.entity"
        }
        template = Template(AuthRepositoryTemplates.RECORD_OWNER_REPOSITORY)
        return template.render(context)

    @staticmethod
    def generate_query_group_repository(package_name: str) -> str:
        context = {
            'packageName': f"{package_name}.repository",
            'entityPackage': f"{package_name}.entity"
        }
        template = Template(AuthRepositoryTemplates.QUERY_GROUP_REPOSITORY)
        return template.render(context)

    @staticmethod
    def generate_query_group_query_repository(package_name: str) -> str:
        context = {
            'packageName': f"{package_name}.repository",
            'entityPackage': f"{package_name}.entity"
        }
        template = Template(AuthRepositoryTemplates.QUERY_GROUP_QUERY_REPOSITORY)
        return template.render(context)

    @staticmethod
    def generate_query_group_member_repository(package_name: str) -> str:
        context = {
            'packageName': f"{package_name}.repository",
            'entityPackage': f"{package_name}.entity"
        }
        template = Template(AuthRepositoryTemplates.QUERY_GROUP_MEMBER_REPOSITORY)
        return template.render(context)

    @staticmethod
    def generate_query_group_record_repository(package_name: str) -> str:
        context = {
            'packageName': f"{package_name}.repository",
            'entityPackage': f"{package_name}.entity"
        }
        template = Template(AuthRepositoryTemplates.QUERY_GROUP_RECORD_REPOSITORY)
        return template.render(context)
