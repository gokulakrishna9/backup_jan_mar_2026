"""Audit logging generator - generates audit logging service and controller."""

from jinja2 import Template
from templates.audit_logging_templates import AuditLoggingTemplates


class AuditLoggingGenerator:
    """Generates audit logging service Java code."""
    
    @staticmethod
    def generate_audit_logging_service(package_name: str) -> str:
        """Generate AuditLoggingService Java code."""
        context = {
            'packageName': f"{package_name}.service",
            'entityPackage': f"{package_name}.entity",
            'repositoryPackage': f"{package_name}.repository"
        }
        template = Template(AuditLoggingTemplates.AUDIT_LOGGING_SERVICE)
        return template.render(context)
    
    @staticmethod
    def generate_audit_controller(package_name: str) -> str:
        """Generate AuditController Java code."""
        context = {
            'packageName': f"{package_name}.controller",
            'servicePackage': f"{package_name}.service",
            'entityPackage': f"{package_name}.entity",
            'securityPackage': f"{package_name}.security"
        }
        template = Template(AuditLoggingTemplates.AUDIT_CONTROLLER)
        return template.render(context)
