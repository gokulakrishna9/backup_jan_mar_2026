"""Filter component transformer — produces FilterPanelProperties per entity."""

from typing import Dict, List

from models.property_objects import FilterFieldProperties, FilterPanelProperties
from models.react_definition_models import ComponentMapping
from utils.string_utils import to_camel_case, to_display_label, to_pascal_case
from utils.type_mapping import TypeMapper


class FilterComponentTransformer:
    """Transforms filter definitions from component mappings into filter panel properties."""

    @staticmethod
    def transform(
        component_mappings: List[ComponentMapping],
        filter_entities: Dict[str, List[Dict]],
    ) -> List[FilterPanelProperties]:
        """Produce filter panel properties for entities with filter definitions.

        Args:
            component_mappings: Component mappings from component_mappings.json.
            filter_entities: Dict of entityName → list of filter field dicts
                             (from filter_layer parsed during Phase 1, now embedded
                             in the react definition via page_definitions).

        Returns:
            List of FilterPanelProperties for entities with filters.
        """
        # Build component type lookup from component mappings
        comp_type_map: Dict[str, Dict[str, str]] = {}
        for mapping in component_mappings:
            field_map: Dict[str, str] = {}
            for field in mapping.fields:
                field_map[field.fieldName] = field.componentType
            comp_type_map[mapping.entityName] = field_map

        results: List[FilterPanelProperties] = []
        for entity_name, filter_fields in filter_entities.items():
            entity_comps = comp_type_map.get(entity_name, {})
            fields: List[FilterFieldProperties] = []

            for ff in filter_fields:
                field_name = ff.get("name", ff.get("fieldName", ""))
                java_type = ff.get("type", ff.get("javaType", "String"))
                operators = ff.get("operators", ["EQUALS"])
                comp_type = entity_comps.get(field_name, TypeMapper.map_to_component(java_type).component_type)

                fields.append(FilterFieldProperties(
                    fieldName=field_name,
                    fieldLabel=to_display_label(field_name),
                    javaType=java_type,
                    operators=operators,
                    componentType=comp_type,
                ))

            if fields:
                results.append(FilterPanelProperties(
                    entityName=entity_name,
                    entityNamePascal=to_pascal_case(entity_name),
                    entityNameCamel=to_camel_case(entity_name),
                    filterFields=fields,
                ))

        return results
