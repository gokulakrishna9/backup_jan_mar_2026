"""Entity component transformer — produces EntityFormProperties and EntityDataTableProperties."""

from typing import Dict, List, Optional, Set, Tuple

from models.property_objects import (
    DataTableColumnProperties,
    EntityDataTableProperties,
    EntityFormProperties,
    FormFieldProperties,
)
from models.react_definition_models import (
    ApiServiceDefinition,
    ComponentMapping,
    FormGrouping,
    PageDefinition,
    ReduxStoreDefinition,
)
from utils.string_utils import to_camel_case, to_display_label, to_pascal_case

# Widget fieldWidget values whose DataTable columns should not be sortable
WIDGET_NON_SORTABLE = {"richText", "codeEditor", "markdown", "json"}


class EntityComponentTransformer:
    """Transforms component mappings into entity form and DataTable properties."""

    @staticmethod
    def transform(
        component_mappings: List[ComponentMapping],
        api_services: List[ApiServiceDefinition],
        form_groupings: List[FormGrouping],
        redux_stores: Optional[List[ReduxStoreDefinition]] = None,
        page_definitions: Optional[List[PageDefinition]] = None,
    ) -> List[Tuple[EntityFormProperties, EntityDataTableProperties]]:
        """Produce form and DataTable properties for each entity.

        Args:
            component_mappings: Component mappings from component_mappings.json.
            api_services: API service definitions from api_services.json.
            form_groupings: Form groupings from form_groupings.json.
            page_definitions: Page definitions with formLayout/formButtons.

        Returns:
            List of (EntityFormProperties, EntityDataTableProperties) tuples.
        """
        # Build API service lookup
        svc_map: Dict[str, ApiServiceDefinition] = {
            svc.entityName: svc for svc in api_services
        }

        # Build entity → PK field name lookup from redux store definitions
        pk_map: Dict[str, str] = {}
        if redux_stores:
            for store in redux_stores:
                pk_map[store.entityName] = store.pkField

        # Build entity → formLayout/formButtons lookup from page definitions
        form_layout_map: Dict[str, any] = {}
        form_buttons_map: Dict[str, any] = {}
        if page_definitions:
            for page in page_definitions:
                for placement in page.componentPlacements:
                    if placement.componentType == "form":
                        if placement.formLayout:
                            form_layout_map[placement.entityName] = placement.formLayout
                        if placement.formButtons:
                            form_buttons_map[placement.entityName] = placement.formButtons

        # Build child → parent FK field lookup from form groupings
        child_parent_fk: Dict[str, str] = {}
        parent_entities: Set[str] = set()
        for grouping in form_groupings:
            parent_entities.add(grouping.parentEntity)
            for tab in grouping.tabs:
                if tab.entityName != grouping.parentEntity:
                    # Child entity — FK field is typically parentEntity + "Id"
                    fk_field = to_camel_case(grouping.parentEntity) + "Id"
                    child_parent_fk[tab.entityName] = fk_field

        # Build root entity set from API services (those with basePath starting with /api/)
        results: List[Tuple[EntityFormProperties, EntityDataTableProperties]] = []

        for mapping in component_mappings:
            entity = mapping.entityName
            svc = svc_map.get(entity)

            # Determine endpoint availability
            has_create = False
            has_update = False
            has_delete = False
            has_view = False
            has_pagination = False
            has_sorting = False

            if svc:
                ep = svc.endpoints
                has_create = ep.get("create", None) is not None and ep["create"].enabled
                has_update = ep.get("update", None) is not None and ep["update"].enabled
                has_delete = ep.get("delete", None) is not None and ep["delete"].enabled
                has_view = ep.get("getById", None) is not None and ep["getById"].enabled
                get_all = ep.get("getAll", None)
                if get_all and get_all.enabled:
                    has_pagination = get_all.supportsPagination
                    has_sorting = get_all.supportsSorting

            # Build form fields
            form_fields: List[FormFieldProperties] = []
            for field in mapping.fields:
                if not field.includeInDTO:
                    continue
                form_fields.append(FormFieldProperties(
                    fieldName=field.fieldName,
                    fieldLabel=field.fieldLabel or to_display_label(field.fieldName),
                    componentType=field.componentType,
                    javaType=field.javaType,
                    columnDefinition=field.columnDefinition,
                    props=field.props,
                    validation=field.validation,
                    isRelationshipField=field.isRelationshipField,
                    relatedEntityName=field.relatedEntityName,
                    isMultiSelect=field.isMultiSelect,
                    autocompleteDisplayField=field.autocompleteDisplayField,
                ))

            # Build DataTable columns (exclude sensitive fields)
            sensitive: Set[str] = set(mapping.excludeSensitiveFields)
            columns: List[DataTableColumnProperties] = []
            for field in mapping.fields:
                if field.fieldName in sensitive:
                    continue
                if not field.includeInDTO:
                    continue
                field_widget = field.props.get("fieldWidget") if field.props else None
                col_sortable = has_sorting and (field_widget not in WIDGET_NON_SORTABLE if field_widget else True)
                columns.append(DataTableColumnProperties(
                    fieldName=field.fieldName,
                    header=field.fieldLabel or to_display_label(field.fieldName),
                    sortable=col_sortable,
                    javaType=field.javaType,
                    fieldWidget=field_widget,
                ))

            # Determine if root entity (not a child in any grouping)
            is_root = entity not in child_parent_fk

            # Get basePath from API service definition
            base_path = svc.basePath if svc else ""

            # Get PK field name
            pk_field = pk_map.get(entity, "id")

            form_props = EntityFormProperties(
                entityName=entity,
                entityNamePascal=to_pascal_case(entity),
                entityNameCamel=to_camel_case(entity),
                basePath=base_path,
                pkField=pk_field,
                fields=form_fields,
                isRootEntity=is_root,
                hasCreateEndpoint=has_create,
                hasUpdateEndpoint=has_update,
                hasDeleteEndpoint=has_delete,
                parentForeignKey=child_parent_fk.get(entity),
                formLayout=form_layout_map.get(entity),
                formButtons=form_buttons_map.get(entity),
                singleRecordPerUser=mapping.singleRecordPerUser,
            )

            table_props = EntityDataTableProperties(
                entityName=entity,
                entityNamePascal=to_pascal_case(entity),
                entityNameCamel=to_camel_case(entity),
                basePath=base_path,
                pkField=pk_field,
                columns=columns,
                hasPagination=has_pagination,
                hasSorting=has_sorting,
                hasViewAction=has_view,
                hasUpdateAction=has_update,
                hasDeleteAction=has_delete,
            )

            results.append((form_props, table_props))

        return results
