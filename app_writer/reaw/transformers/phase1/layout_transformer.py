"""Layout transformer — derives application layout from entities and project metadata."""

from typing import Dict, List

from models.definition_models import ControllerLayerDef, EntityLayerDef, ProjectMetadataDef
from models.react_definition_models import LayoutDefinition, LayoutRegion, NavGroup, NavItem
from utils.string_utils import to_display_label, to_kebab_case


class LayoutTransformer:
    """Transforms entity and project metadata into layout definition."""

    @staticmethod
    def transform(
        entity_layer: EntityLayerDef,
        controller_layer: ControllerLayerDef,
        project_metadata: ProjectMetadataDef,
    ) -> LayoutDefinition:
        """Produce layout definition with nav groups and application metadata.

        Groups Root_Entities by domain prefix for navigation.

        Args:
            entity_layer: Parsed entity layer with root entity flags.
            controller_layer: Parsed controller layer for enabled entities.
            project_metadata: Parsed project metadata for app name and port.

        Returns:
            LayoutDefinition with default collapsible regions and nav groups.
        """
        # Build set of entities with enabled endpoints (uses className)
        enabled_entities = set()
        for ctrl in controller_layer.controllers:
            if any(ep.enabled for ep in ctrl.endpoints.values()):
                enabled_entities.add(ctrl.entityName)

        # Build root entity lookup (use className to match enabled_entities)
        root_entities = set()
        for entry in entity_layer.entities:
            if entry.isRootEntity and entry.className in enabled_entities:
                root_entities.add(entry.className)

        # Group entities by domain prefix (className is PascalCase, use tableName for grouping)
        class_to_table: Dict[str, str] = {}
        for entry in entity_layer.entities:
            class_to_table[entry.className] = entry.tableName

        groups: Dict[str, List[NavItem]] = {}
        for entity_name in enabled_entities:
            table_name = class_to_table.get(entity_name, entity_name)
            parts = table_name.split("_")
            group_key = parts[0] if len(parts) > 1 else table_name
            group_label = to_display_label(group_key)
            if group_label not in groups:
                groups[group_label] = []
            groups[group_label].append(NavItem(
                label=to_display_label(entity_name),
                path=f"/{to_kebab_case(entity_name)}",
            ))

        # Sort entities within each group
        nav_groups = [
            NavGroup(groupName=name, entities=sorted(entities, key=lambda e: e.label))
            for name, entities in sorted(groups.items())
        ]

        meta = project_metadata.projectMetadata

        return LayoutDefinition(
            applicationName=meta.applicationName or meta.name or meta.artifactId or "Application",
            apiPort=meta.port,
            header=LayoutRegion(visible=True, collapsible=True, defaultCollapsed=False),
            footer=LayoutRegion(visible=True, collapsible=True, defaultCollapsed=False),
            leftNav=LayoutRegion(visible=True, collapsible=True, defaultCollapsed=False),
            content=LayoutRegion(visible=True, collapsible=False, defaultCollapsed=False),
            navGroups=nav_groups,
        )
