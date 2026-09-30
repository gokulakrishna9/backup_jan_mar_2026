"""Redux slice transformer — produces ReduxSliceProperties per entity and ReduxStoreProperties."""

from typing import List, Tuple

from models.property_objects import ReduxSliceProperties, ReduxStoreProperties
from models.react_definition_models import ReduxStoreDefinition
from utils.string_utils import to_camel_case, to_pascal_case


class ReduxSliceTransformer:
    """Transforms Redux store definitions into template-ready properties."""

    @staticmethod
    def transform(
        redux_stores: List[ReduxStoreDefinition],
    ) -> Tuple[ReduxStoreProperties, List[ReduxSliceProperties]]:
        """Produce Redux store and per-entity slice properties.

        Args:
            redux_stores: List of Redux store definitions from redux_store.json.

        Returns:
            Tuple of (ReduxStoreProperties, list of ReduxSliceProperties).
        """
        entities: List[str] = []
        slices: List[ReduxSliceProperties] = []

        for store in redux_stores:
            entities.append(store.entityName)

            has_pagination = store.pagination is not None
            page_size = store.pagination.pageSize if store.pagination else 20

            slices.append(ReduxSliceProperties(
                entityName=store.entityName,
                entityNameCamel=to_camel_case(store.entityName),
                entityNamePascal=to_pascal_case(store.entityName),
                pkField=store.pkField,
                thunks=store.thunks,
                hasPagination=has_pagination,
                pageSize=page_size,
            ))

        store_props = ReduxStoreProperties(entities=entities)
        return store_props, slices
