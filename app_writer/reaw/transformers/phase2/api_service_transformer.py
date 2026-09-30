"""API service transformer — produces ApiServiceProperties per entity and ApiClientProperties."""

from typing import List, Tuple

from models.property_objects import ApiClientProperties, ApiServiceProperties
from models.react_definition_models import ApiServiceDefinition, LayoutDefinition
from utils.string_utils import to_camel_case


class ApiServiceTransformer:
    """Transforms API service definitions into template-ready properties."""

    @staticmethod
    def transform(
        api_services: List[ApiServiceDefinition],
        layout: LayoutDefinition,
        refresh_token_enabled: bool = True,
    ) -> Tuple[ApiClientProperties, List[ApiServiceProperties]]:
        """Produce API client and per-entity service properties.

        Args:
            api_services: List of API service definitions from api_services.json.
            layout: Layout definition containing apiPort.
            refresh_token_enabled: Whether refresh token flow is enabled.

        Returns:
            Tuple of (ApiClientProperties, list of ApiServiceProperties).
        """
        client = ApiClientProperties(
            baseUrl="",
            refreshTokenEnabled=refresh_token_enabled,
        )

        services: List[ApiServiceProperties] = []
        for svc in api_services:
            services.append(ApiServiceProperties(
                entityName=svc.entityName,
                entityNameCamel=to_camel_case(svc.entityName),
                basePath=svc.basePath,
                endpoints=svc.endpoints,
            ))

        return client, services
