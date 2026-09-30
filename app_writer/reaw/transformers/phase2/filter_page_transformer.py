"""Filter page transformer — produces filter page properties from page definitions."""

from typing import List

from models.property_objects import EntityPageProperties
from models.react_definition_models import PageDefinition
from utils.string_utils import to_pascal_case, to_camel_case


class FilterPageTransformer:
    """Transforms filter-type page definitions into page properties."""

    @staticmethod
    def transform(page_definitions: List[PageDefinition]) -> List[EntityPageProperties]:
        """Produce page properties for filter pages.

        Args:
            page_definitions: All page definitions from page_definitions.json.

        Returns:
            List of EntityPageProperties for filter-type pages only.
        """
        return [
            EntityPageProperties(
                entityName=page.entityName,
                entityNamePascal=to_pascal_case(page.entityName),
                entityNameCamel=to_camel_case(page.entityName),
                pageType=page.pageType,
                gridTemplate=page.gridTemplate,
                componentPlacements=page.componentPlacements,
                isGroupedForm=False,
                groupTabs=None,
            )
            for page in page_definitions
            if page.pageType == "filter"
        ]
