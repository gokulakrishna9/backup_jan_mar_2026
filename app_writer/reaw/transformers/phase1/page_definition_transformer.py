"""Page definition transformer — generates default page grid layouts."""

from typing import Dict, List, Set

from models.definition_models import EntityLayerDef, FilterLayerDef, QueryLayerDef
from models.react_definition_models import (
    ComponentPlacement,
    FormButton,
    FormGrouping,
    FormLayout,
    GridTemplate,
    PageDefinition,
)
from utils.string_utils import to_snake_case


class PageDefinitionTransformer:
    """Transforms entity/filter/query layers into page definitions with grid layouts."""

    @staticmethod
    def transform(
        entity_layer: EntityLayerDef,
        filter_layer: FilterLayerDef,
        query_layer: QueryLayerDef,
        form_groupings: List[FormGrouping],
    ) -> List[PageDefinition]:
        """Produce default page definitions for entity, filter, and query pages.

        Args:
            entity_layer: Parsed entity layer.
            filter_layer: Parsed filter layer.
            query_layer: Parsed query layer.
            form_groupings: Already-transformed form groupings.

        Returns:
            List of PageDefinition with default grid templates.
        """
        pages: List[PageDefinition] = []

        # Track which entities are grouped parents (uses className)
        grouped_parents: Set[str] = set()
        for group in form_groupings:
            grouped_parents.add(group.parentEntity)

        # Entity names from entity layer (use className for consistency)
        entity_names = [e.className for e in entity_layer.entities]

        # Entity pages
        for entity_name in entity_names:
            snake = to_snake_case(entity_name)
            is_grouped = entity_name in grouped_parents

            if is_grouped:
                # Grouped form page: single area for the tabbed component
                pages.append(PageDefinition(
                    pageId=f"{snake}_entity_page",
                    pageType="entity",
                    entityName=entity_name,
                    gridTemplate=GridTemplate(
                        gridTemplateRows="1fr",
                        gridTemplateColumns="1fr",
                        gridTemplateAreas=["grouped-form"],
                    ),
                    componentPlacements=[
                        ComponentPlacement(
                            componentType="groupedForm",
                            entityName=entity_name,
                            gridArea="grouped-form",
                        ),
                    ],
                ))
            else:
                # Standard entity page: form on top, table below
                default_layout = FormLayout(
                    columnsLg=3,
                    columnsMd=2,
                    columnsSm=1,
                    fullWidthComponentTypes=["InputTextarea"],
                )
                default_buttons = [
                    FormButton(label="New", icon="pi pi-plus", action="create", className="p-button-success p-button-sm", visibleWhen="always"),
                    FormButton(label="Edit", icon="pi pi-pencil", action="edit", className="p-button-info p-mr-2", visibleWhen="viewMode"),
                    FormButton(label="Save", icon="pi pi-check", action="submit", className="p-button-success p-mr-2", visibleWhen="editMode"),
                    FormButton(label="Cancel", icon="pi pi-times", action="cancel", className="p-button-secondary", visibleWhen="editMode"),
                ]
                pages.append(PageDefinition(
                    pageId=f"{snake}_entity_page",
                    pageType="entity",
                    entityName=entity_name,
                    gridTemplate=GridTemplate(
                        gridTemplateRows="auto 1fr",
                        gridTemplateColumns="1fr",
                        gridTemplateAreas=["form", "table"],
                    ),
                    componentPlacements=[
                        ComponentPlacement(
                            componentType="form",
                            entityName=entity_name,
                            gridArea="form",
                            formLayout=default_layout,
                            formButtons=default_buttons,
                        ),
                        ComponentPlacement(
                            componentType="dataTable",
                            entityName=entity_name,
                            gridArea="table",
                        ),
                    ],
                ))

        # Filter pages
        for entity_name in filter_layer.filters:
            filter_def = filter_layer.filters[entity_name]
            if not filter_def.fields:
                continue
            snake = to_snake_case(entity_name)
            pages.append(PageDefinition(
                pageId=f"{snake}_filter_page",
                pageType="filter",
                entityName=entity_name,
                gridTemplate=GridTemplate(
                    gridTemplateRows="auto 1fr",
                    gridTemplateColumns="1fr",
                    gridTemplateAreas=["filters", "results"],
                ),
                componentPlacements=[
                    ComponentPlacement(
                        componentType="filterPanel",
                        entityName=entity_name,
                        gridArea="filters",
                    ),
                    ComponentPlacement(
                        componentType="dataTable",
                        entityName=entity_name,
                        gridArea="results",
                    ),
                ],
            ))

        # Query pages
        for entity_name in query_layer.queries:
            queries = query_layer.queries[entity_name]
            if not queries:
                continue
            snake = to_snake_case(entity_name)
            pages.append(PageDefinition(
                pageId=f"{snake}_query_page",
                pageType="query",
                entityName=entity_name,
                gridTemplate=GridTemplate(
                    gridTemplateRows="auto 1fr",
                    gridTemplateColumns="1fr",
                    gridTemplateAreas=["query", "results"],
                ),
                componentPlacements=[
                    ComponentPlacement(
                        componentType="querySection",
                        entityName=entity_name,
                        gridArea="query",
                    ),
                    ComponentPlacement(
                        componentType="dataTable",
                        entityName=entity_name,
                        gridArea="results",
                    ),
                ],
            ))

        return pages
