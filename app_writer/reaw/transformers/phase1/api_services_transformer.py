"""API services transformer — derives per-entity API service config from controller layer."""

from typing import List

from models.definition_models import ControllerLayerDef
from models.react_definition_models import ApiEndpointDef, ApiServiceDefinition


class ApiServicesTransformer:
    """Transforms controller layer into API service definitions."""

    @staticmethod
    def transform(controller_layer: ControllerLayerDef) -> List[ApiServiceDefinition]:
        """Produce API service definitions for each entity.

        Maps each entity's controller endpoints to API service config with
        enabled flags, HTTP methods, and pagination/filtering/sorting support.

        Args:
            controller_layer: Parsed controller layer with endpoint configs.

        Returns:
            List of ApiServiceDefinition per entity.
        """
        services: List[ApiServiceDefinition] = []

        for ctrl in controller_layer.controllers:
            has_enabled = any(ep.enabled for ep in ctrl.endpoints.values())
            if not has_enabled:
                continue

            endpoints = {}
            for ep_name, ep_def in ctrl.endpoints.items():
                endpoints[ep_name] = ApiEndpointDef(
                    enabled=ep_def.enabled,
                    method=ep_def.method,
                    supportsPagination=ep_def.supportsPagination,
                    supportsFiltering=ep_def.supportsFiltering,
                    supportsSorting=ep_def.supportsSorting,
                )

            services.append(ApiServiceDefinition(
                entityName=ctrl.entityName,
                basePath=ctrl.basePath,
                endpoints=endpoints,
            ))

        return services
