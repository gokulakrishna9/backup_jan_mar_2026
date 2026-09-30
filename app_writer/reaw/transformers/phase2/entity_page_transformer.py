"""Entity page transformer — produces EntityPageProperties from page definitions."""

from typing import Dict, List, Optional

from models.property_objects import EntityPageProperties
from models.react_definition_models import FormGrouping, PageDefinition
from utils.string_utils import to_pascal_case, to_camel_case, to_display_label


class EntityPageTransformer:
    """Transforms page definitions into entity page properties."""

    @staticmethod
    def transform(
        page_definitions: List[PageDefinition],
        form_groupings: List[FormGrouping],
    ) -> List[EntityPageProperties]:
        """Produce entity page properties for each page definition.

        Args:
            page_definitions: Page definitions from page_definitions.json.
            form_groupings: Form groupings from form_groupings.json.

        Returns:
            List of EntityPageProperties.
        """
        # Build parent entity → grouping lookup
        grouping_map: Dict[str, FormGrouping] = {
            g.parentEntity: g for g in form_groupings
        }

        results: List[EntityPageProperties] = []
        for page in page_definitions:
            grouping = grouping_map.get(page.entityName)
            is_grouped = grouping is not None and page.pageType == "entity"

            # Build page title from entity name and page type
            title = to_display_label(page.entityName)
            if page.pageType == "filter":
                title += " — Filters"
            elif page.pageType == "query":
                title += " — Queries"

            results.append(EntityPageProperties(
                entityName=page.entityName,
                entityNamePascal=to_pascal_case(page.entityName),
                entityNameCamel=to_camel_case(page.entityName),
                pageTitle=title,
                pageType=page.pageType,
                gridTemplate=page.gridTemplate,
                componentPlacements=page.componentPlacements,
                isGroupedForm=is_grouped,
                groupTabs=grouping.tabs if is_grouped else None,
            ))

        return results
