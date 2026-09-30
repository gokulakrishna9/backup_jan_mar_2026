"""Controller generator - populates controller templates."""

from jinja2 import Template
from models.layer_objects import ControllerLayerObject
from templates.controller_templates import ControllerTemplates


class ControllerGenerator:
    """Generates controller Java code from controller layer object."""
    
    @staticmethod
    def generate(controller: ControllerLayerObject, has_authorization: bool = False, table_name: str = "") -> str:
        """Generate controller Java code with endpoint configurations.
        
        Args:
            controller: Controller layer object with all properties
            has_authorization: Whether authorization is enabled (enables activity tracking)
            table_name: Database table name for @EntityTable annotation
            
        Returns:
            Generated Java code as string
        """
        # Determine package names
        base_package = controller.packageName.replace('.controller', '')
        dto_package = f"{base_package}.dto"
        service_package = f"{base_package}.service"
        exception_package = f"{base_package}.exception"
        security_package = f"{base_package}.security"
        
        # Activity tracking is enabled when authorization is enabled
        has_activity_tracking = has_authorization
        
        # Prepare template context
        context = {
            'packageName': controller.packageName,
            'dtoPackage': dto_package,
            'servicePackage': service_package,
            'exceptionPackage': exception_package,
            'securityPackage': security_package,
            'entityName': controller.entityName,
            'className': controller.className,
            'serviceName': controller.serviceName,
            'basePath': controller.basePath,
            'isRootEntity': controller.isRootEntity,
            'endpoints': controller.endpoints,
            'customEndpoints': controller.customEndpoints,
            'corsConfig': controller.corsConfig,
            'hasActivityTracking': has_activity_tracking,
            'tableName': table_name,
            'singleRecordPerUser': controller.singleRecordPerUser,
        }
        
        # Render template
        template = Template(ControllerTemplates.CONTROLLER_TEMPLATE)
        return template.render(context)

