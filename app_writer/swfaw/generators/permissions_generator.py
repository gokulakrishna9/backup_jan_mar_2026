"""Permissions generator — produces PermissionsService, PermissionsController,
and EntityApiRegistry Java files."""

from typing import List, Dict
from jinja2 import Template
from templates.permissions_templates import PermissionsTemplates


class PermissionsGenerator:
    """Generates permissions endpoint Java code."""

    @staticmethod
    def generate_entity_api_registry(
        package_name: str,
        controller_entries: List[Dict[str, str]],
    ) -> str:
        """Generate EntityApiRegistry.java.

        Args:
            package_name: Base package (e.g. com.example).
            controller_entries: List of dicts with 'tableName' and 'basePath'.
        """
        context = {
            "packageName": f"{package_name}.service",
            "entries": controller_entries,
        }
        return Template(PermissionsTemplates.ENTITY_API_REGISTRY).render(context)

    @staticmethod
    def generate_permissions_service(package_name: str) -> str:
        """Generate PermissionsService.java."""
        context = {
            "packageName": f"{package_name}.service",
            "entityPackage": f"{package_name}.entity",
            "repositoryPackage": f"{package_name}.repository",
        }
        return Template(PermissionsTemplates.PERMISSIONS_SERVICE).render(context)

    @staticmethod
    def generate_permissions_controller(package_name: str) -> str:
        """Generate PermissionsController.java."""
        context = {
            "packageName": f"{package_name}.controller",
            "servicePackage": f"{package_name}.service",
            "securityPackage": f"{package_name}.security",
        }
        return Template(PermissionsTemplates.PERMISSIONS_CONTROLLER).render(context)
