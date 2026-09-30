"""Form grouping transformer — derives parent-child tab groupings from relationships."""

from typing import Dict, List, Set

from models.definition_models import EntityLayerDef, RelationshipsDef
from models.react_definition_models import FormGrouping, FormGroupTab
from utils.string_utils import to_display_label


class FormGroupingTransformer:
    """Transforms relationships into form grouping definitions."""

    @staticmethod
    def transform(
        relationships: RelationshipsDef,
        entity_layer: EntityLayerDef,
    ) -> List[FormGrouping]:
        """Produce form groupings based on parent-child relationships.

        Groups child entities under their parent entity based on ONE_TO_MANY
        relationships. Each group becomes a tabbed entity page.

        Args:
            relationships: Parsed relationships definition.
            entity_layer: Parsed entity layer with root entity flags.

        Returns:
            List of FormGrouping definitions.
        """
        # Build table→className lookup and root entity set
        table_to_class: Dict[str, str] = {}
        root_entities: Set[str] = set()
        for entry in entity_layer.entities:
            table_to_class[entry.tableName] = entry.className
            if entry.isRootEntity:
                root_entities.add(entry.className)

        # Build parent → children map from OneToMany relationships
        parent_children: Dict[str, List[str]] = {}
        children_assigned: Set[str] = set()

        for rel in relationships.relationships:
            if rel.type == "OneToMany" and not rel.joinTable:
                parent = table_to_class.get(rel.sourceTable, rel.sourceTable)
                child = table_to_class.get(rel.targetTable, rel.targetTable)
                if parent not in parent_children:
                    parent_children[parent] = []
                if child not in children_assigned:
                    parent_children[parent].append(child)
                    children_assigned.add(child)

        groupings: List[FormGrouping] = []

        for parent, children in parent_children.items():
            if not children:
                continue

            tabs = [
                FormGroupTab(
                    entityName=parent,
                    tabLabel=to_display_label(parent),
                    tabOrder=0,
                    included=True,
                )
            ]
            for idx, child in enumerate(children, start=1):
                tabs.append(FormGroupTab(
                    entityName=child,
                    tabLabel=to_display_label(child),
                    tabOrder=idx,
                    included=True,
                ))

            groupings.append(FormGrouping(
                groupName=f"{to_display_label(parent)} Management",
                parentEntity=parent,
                tabs=tabs,
            ))

        return groupings
