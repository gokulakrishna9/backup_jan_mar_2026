"""Admin UI generator - generates admin service, controller, and Thymeleaf templates."""

from jinja2 import Template
from templates.admin_ui_templates import AdminUITemplates
from templates.admin_html_templates import AdminHTMLTemplates


class AdminUIGenerator:
    """Generates admin UI components."""
    
    @staticmethod
    def generate_admin_service(package_name: str) -> str:
        """Generate AdminService Java code."""
        context = {
            'packageName': f"{package_name}.service",
            'entityPackage': f"{package_name}.entity",
            'repositoryPackage': f"{package_name}.repository"
        }
        template = Template(AdminUITemplates.ADMIN_SERVICE)
        return template.render(context)
    
    @staticmethod
    def generate_admin_controller(package_name: str) -> str:
        """Generate AdminController Java code."""
        context = {
            'packageName': f"{package_name}.controller",
            'servicePackage': f"{package_name}.service",
            'entityPackage': f"{package_name}.entity",
            'securityPackage': f"{package_name}.security"
        }
        template = Template(AdminUITemplates.ADMIN_CONTROLLER)
        return template.render(context)
    
    @staticmethod
    def generate_dashboard_html() -> str:
        """Generate dashboard HTML."""
        return AdminHTMLTemplates.DASHBOARD_HTML
    
    @staticmethod
    def generate_groups_html() -> str:
        """Generate groups list HTML."""
        return AdminHTMLTemplates.GROUPS_HTML
    
    @staticmethod
    def generate_group_form_html() -> str:
        """Generate group form HTML."""
        return AdminHTMLTemplates.GROUP_FORM_HTML
    
    @staticmethod
    def generate_users_html() -> str:
        """Generate users list HTML."""
        return AdminHTMLTemplates.USERS_HTML
    
    @staticmethod
    def generate_user_detail_html() -> str:
        """Generate user detail HTML."""
        return AdminHTMLTemplates.USER_DETAIL_HTML
    
    @staticmethod
    def generate_document_groups_html() -> str:
        """Generate document groups list HTML."""
        return AdminHTMLTemplates.DOCUMENT_GROUPS_HTML
    
    @staticmethod
    def generate_document_group_form_html() -> str:
        """Generate document group form HTML."""
        return AdminHTMLTemplates.DOCUMENT_GROUP_FORM_HTML
    
    @staticmethod
    def generate_document_group_detail_html() -> str:
        """Generate document group detail HTML."""
        return AdminHTMLTemplates.DOCUMENT_GROUP_DETAIL_HTML
