"""Route transformer — derives routes from controller, filter, and query layers."""

from typing import Dict, List

from models.definition_models import (
    ControllerLayerDef,
    FilterLayerDef,
    QueryLayerDef,
)
from models.react_definition_models import RouteDefinition
from utils.string_utils import to_pascal_case, to_display_label, to_kebab_case, to_snake_case


def _derive_nav_group(entity_name: str) -> str:
    """Derive a navigation group name from an entity name prefix.

    Groups entities by their first word when the name has multiple parts.
    E.g., 'EmsUser' -> 'Ems', 'OrderItem' -> 'Order', 'User' -> 'User'.
    """
    snake = to_snake_case(entity_name)
    parts = snake.split("_")
    if len(parts) > 1:
        return to_display_label(parts[0])
    return to_display_label(entity_name)


class RouteTransformer:
    """Transforms controller/filter/query layers into route definitions."""

    @staticmethod
    def transform(
        controller_layer: ControllerLayerDef,
        filter_layer: FilterLayerDef,
        query_layer: QueryLayerDef,
    ) -> List[RouteDefinition]:
        """Produce route definitions for entity, filter, and query pages.

        Args:
            controller_layer: Parsed controller layer with endpoint configs.
            filter_layer: Parsed filter layer with filter definitions.
            query_layer: Parsed query layer with query definitions.

        Returns:
            List of RouteDefinition for all page types.
        """
        routes: List[RouteDefinition] = []

        # Build lookup of entities with at least one enabled endpoint
        entity_controllers: Dict[str, bool] = {}
        entity_is_root: Dict[str, bool] = {}
        entity_requires_auth: Dict[str, bool] = {}

        for ctrl in controller_layer.controllers:
            has_enabled = any(ep.enabled for ep in ctrl.endpoints.values())
            if has_enabled:
                entity_controllers[ctrl.entityName] = True
                entity_is_root[ctrl.entityName] = ctrl.isRootEntity
                entity_requires_auth[ctrl.entityName] = any(
                    ep.requiresAuth for ep in ctrl.endpoints.values() if ep.enabled
                )

        # Entity pages
        for entity_name in entity_controllers:
            pascal = to_pascal_case(entity_name)
            kebab = to_kebab_case(entity_name)
            routes.append(RouteDefinition(
                path=f"/{kebab}",
                pageComponent=f"{pascal}Page",
                pageType="entity",
                pageFolder="entitys",
                entityName=entity_name,
                navLabel=to_display_label(entity_name),
                navGroup=_derive_nav_group(entity_name),
                requiresAuth=entity_requires_auth.get(entity_name, True),
            ))

        # Filter pages
        for entity_name in filter_layer.filters:
            if entity_name not in entity_controllers:
                continue
            filter_def = filter_layer.filters[entity_name]
            if not filter_def.fields:
                continue
            pascal = to_pascal_case(entity_name)
            kebab = to_kebab_case(entity_name)
            routes.append(RouteDefinition(
                path=f"/{kebab}/filter",
                pageComponent=f"{pascal}FilterPage",
                pageType="filter",
                pageFolder="filters",
                entityName=entity_name,
                navLabel=f"{to_display_label(entity_name)} Filters",
                navGroup=_derive_nav_group(entity_name),
                requiresAuth=entity_requires_auth.get(entity_name, True),
            ))

        # Query pages
        for entity_name in query_layer.queries:
            if entity_name not in entity_controllers:
                continue
            queries = query_layer.queries[entity_name]
            if not queries:
                continue
            pascal = to_pascal_case(entity_name)
            kebab = to_kebab_case(entity_name)
            routes.append(RouteDefinition(
                path=f"/{kebab}/queries",
                pageComponent=f"{pascal}QueryPage",
                pageType="query",
                pageFolder="queries",
                entityName=entity_name,
                navLabel=f"{to_display_label(entity_name)} Queries",
                navGroup=_derive_nav_group(entity_name),
                requiresAuth=entity_requires_auth.get(entity_name, True),
            ))

        return routes
