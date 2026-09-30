"""Controller transformer - converts entity properties to controller properties."""

from models.layer_objects import EntityLayerObject, ControllerLayerObject
from utils.string_utils import to_camel_case


class ControllerTransformer:
    """Transforms entity properties into controller properties."""
    
    @staticmethod
    def transform(entity: EntityLayerObject) -> ControllerLayerObject:
        """Transform entity to controller properties.
        
        Args:
            entity: Entity layer object
            
        Returns:
            ControllerLayerObject with default endpoint configurations
        """
        # Generate base path from entity name
        base_path = f"/api/{to_camel_case(entity.className)}s"
        
        # Default endpoint configurations
        default_endpoints = {
            "create": {
                "enabled": True,
                "path": "",
                "method": "POST",
                "requiresAuth": True,
                "roles": ["USER", "ADMIN"],
                "rateLimitPerMinute": 10
            },
            "getById": {
                "enabled": True,
                "path": "/{id}",
                "method": "GET",
                "requiresAuth": True,
                "roles": ["USER", "ADMIN"],
                "rateLimitPerMinute": 60
            },
            "getAll": {
                "enabled": True,
                "path": "",
                "method": "GET",
                "requiresAuth": True,
                "roles": ["USER", "ADMIN"],
                "rateLimitPerMinute": 30,
                "defaultPageSize": 20,
                "supportsPagination": True,
                "supportsFiltering": True,
                "supportsSorting": True
            },
            "update": {
                "enabled": True,
                "path": "/{id}",
                "method": "PUT",
                "requiresAuth": True,
                "roles": ["USER", "ADMIN"],
                "rateLimitPerMinute": 10
            },
            "delete": {
                "enabled": True,
                "path": "/{id}",
                "method": "DELETE",
                "requiresAuth": True,
                "roles": ["ADMIN"],
                "rateLimitPerMinute": 5
            }
        }
        
        # Default CORS configuration
        default_cors = {
            "enabled": True,
            "allowedOrigins": ["*"],
            "allowedMethods": ["GET", "POST", "PUT", "DELETE"],
            "allowedHeaders": ["*"],
            "maxAge": 3600
        }
        
        return ControllerLayerObject(
            entityName=entity.className,
            className=f"{entity.className}Controller",
            packageName=entity.packageName.replace('.entity', '.controller'),
            serviceName=f"{entity.className}Service",
            basePath=base_path,
            isRootEntity=entity.isRootEntity,
            endpoints=default_endpoints,
            customEndpoints=[],
            corsConfig=default_cors
        )
