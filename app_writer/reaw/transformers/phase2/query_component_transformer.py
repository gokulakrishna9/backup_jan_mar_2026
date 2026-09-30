"""Query component transformer — produces QuerySectionProperties per entity."""

from typing import Dict, List

from models.property_objects import QueryParameterProperties, QueryProperties, QuerySectionProperties
from models.react_definition_models import ComponentMapping
from utils.string_utils import to_camel_case, to_pascal_case
from utils.type_mapping import TypeMapper


class QueryComponentTransformer:
    """Transforms query definitions into query section properties."""

    @staticmethod
    def transform(
        query_entities: Dict[str, List[Dict]],
    ) -> List[QuerySectionProperties]:
        """Produce query section properties for entities with query definitions.

        Args:
            query_entities: Dict of entityName → list of query dicts
                            (from query_layer parsed during Phase 1).

        Returns:
            List of QuerySectionProperties for entities with queries.
        """
        results: List[QuerySectionProperties] = []

        for entity_name, queries in query_entities.items():
            query_props: List[QueryProperties] = []

            for q in queries:
                name = q.get("name", "")
                description = q.get("description", "")
                has_pagination = q.get("pagination", True)
                params = q.get("parameters", [])

                param_props: List[QueryParameterProperties] = []
                for p in params:
                    p_name = p.get("name", "")
                    p_type = p.get("type", p.get("javaType", "String"))
                    p_required = p.get("required", False)
                    comp_type = TypeMapper.map_to_component(p_type).component_type

                    param_props.append(QueryParameterProperties(
                        name=p_name,
                        type=p_type,
                        required=p_required,
                        componentType=comp_type,
                    ))

                query_props.append(QueryProperties(
                    queryName=name,
                    queryNameCamel=to_camel_case(name),
                    description=description,
                    parameters=param_props,
                    hasPagination=has_pagination,
                ))

            if query_props:
                results.append(QuerySectionProperties(
                    entityName=entity_name,
                    entityNamePascal=to_pascal_case(entity_name),
                    entityNameCamel=to_camel_case(entity_name),
                    queries=query_props,
                ))

        return results
