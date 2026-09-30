"""Redux store transformer — derives Redux store config from API services."""

from typing import Dict, List, Optional

from models.definition_models import EntityLayerDef
from models.react_definition_models import (
    ApiServiceDefinition,
    PaginationStateDef,
    ReduxStoreDefinition,
    StateShapeDef,
)


# Map API endpoint names to Redux thunk names
_ENDPOINT_TO_THUNK = {
    "getAll": "fetchAll",
    "getById": "fetchById",
    "create": "create",
    "update": "update",
    "delete": "delete",
}


class ReduxStoreTransformer:
    """Transforms API service definitions into Redux store definitions."""

    @staticmethod
    def _build_pk_map(entity_layer: Optional[EntityLayerDef]) -> Dict[str, str]:
        """Build entity name → PK field name map from entity layer."""
        pk_map: Dict[str, str] = {}
        if not entity_layer:
            return pk_map
        for entity in entity_layer.entities:
            for field in entity.fields:
                if field.isPrimaryKey:
                    pk_map[entity.className] = field.fieldName
                    break
        return pk_map

    @staticmethod
    def transform(
        api_services: List[ApiServiceDefinition],
        entity_layer: Optional[EntityLayerDef] = None,
    ) -> List[ReduxStoreDefinition]:
        """Produce Redux store definitions derived from API services.

        Derives thunks from enabled API endpoints. Sets state shape and
        pagination config based on getAll support.

        Args:
            api_services: Already-transformed API service definitions.
            entity_layer: Entity layer definition for PK field lookup.

        Returns:
            List of ReduxStoreDefinition per entity.
        """
        pk_map = ReduxStoreTransformer._build_pk_map(entity_layer)
        store_defs: List[ReduxStoreDefinition] = []

        for svc in api_services:
            thunks = {}
            has_pagination = False

            for ep_name, ep_def in svc.endpoints.items():
                thunk_name = _ENDPOINT_TO_THUNK.get(ep_name)
                if thunk_name:
                    thunks[thunk_name] = ep_def.enabled

                if ep_name == "getAll" and ep_def.enabled and ep_def.supportsPagination:
                    has_pagination = True

            pagination = None
            if has_pagination:
                pagination = PaginationStateDef(
                    currentPage=0,
                    pageSize=20,
                    totalCount=0,
                )

            pk_field = pk_map.get(svc.entityName, "id")

            store_defs.append(ReduxStoreDefinition(
                entityName=svc.entityName,
                pkField=pk_field,
                thunks=thunks,
                stateShape=StateShapeDef(
                    listState=True,
                    singleItemState=True,
                    mutationState=True,
                ),
                pagination=pagination,
            ))

        return store_defs
