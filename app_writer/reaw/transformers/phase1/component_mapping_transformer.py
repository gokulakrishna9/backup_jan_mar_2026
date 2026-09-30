"""Component mapping transformer — maps entity fields to PrimeReact components."""

from typing import Dict, List, Optional, Set

from models.definition_models import DtoLayerDef, EntityLayerDef, RelationshipsDef
from models.react_definition_models import ComponentMapping, FieldMapping, ValidationConfig
from utils.string_utils import to_camel_case, to_display_label
from utils.type_mapping import TypeMapper

# Widget override: if fieldWidget is set and not "text", use widget componentType
WIDGET_COMPONENT_MAP = {
    "richText": "QuillEditor",
    "codeEditor": "MonacoEditor",
    "markdown": "MarkdownEditor",
    "json": "MonacoEditor",
}


class ComponentMappingTransformer:
    """Transforms DTO layer fields into component mappings."""

    @staticmethod
    def transform(
        dto_layer: DtoLayerDef,
        relationships: RelationshipsDef,
        entity_layer: EntityLayerDef,
    ) -> List[ComponentMapping]:
        """Produce component mappings for each entity's form fields.

        Maps each Input DTO field to its PrimeReact component using TypeMapper.
        Relationship fields become AutoComplete with display field and multiSelect.

        Args:
            dto_layer: Parsed DTO layer with field definitions.
            relationships: Parsed relationships for FK detection.
            entity_layer: Parsed entity layer for table→className mapping.

        Returns:
            List of ComponentMapping per entity.
        """
        # Build table→className lookup
        table_to_class: Dict[str, str] = {}
        for entry in entity_layer.entities:
            table_to_class[entry.tableName] = entry.className

        # Build relationship lookups using className as keys
        # Relationships use sourceTable/targetTable (raw table names)
        fk_fields: Dict[str, Dict[str, dict]] = {}  # className -> {fieldName -> rel_info}
        for rel in relationships.relationships:
            if rel.type in ("ManyToOne", "OneToMany"):
                target_class = table_to_class.get(rel.targetTable, rel.targetTable)
                if target_class not in fk_fields:
                    fk_fields[target_class] = {}
                # The FK field on the child side (convert column name to camelCase)
                if rel.foreignKey:
                    fk_field_name = to_camel_case(rel.foreignKey)
                    source_class = table_to_class.get(rel.sourceTable, rel.sourceTable)
                    fk_fields[target_class][fk_field_name] = {
                        "relatedEntity": source_class,
                        "type": rel.type,
                        "isLinkEntity": bool(rel.joinTable),
                    }
            if rel.type == "ManyToMany":
                source_class = table_to_class.get(rel.sourceTable, rel.sourceTable)
                if source_class not in fk_fields:
                    fk_fields[source_class] = {}
                if rel.foreignKey:
                    fk_field_name = to_camel_case(rel.foreignKey)
                    target_class = table_to_class.get(rel.targetTable, rel.targetTable)
                    fk_fields[source_class][fk_field_name] = {
                        "relatedEntity": target_class,
                        "type": rel.type,
                        "isLinkEntity": True,
                    }

        mappings: List[ComponentMapping] = []

        # Group DTOs by entity
        entity_dtos: Dict[str, dict] = {}
        for dto in dto_layer.dtos:
            entity = dto.entityName
            if entity not in entity_dtos:
                entity_dtos[entity] = {"input": None, "output": None}
            if dto.dtoType == "Input":
                entity_dtos[entity]["input"] = dto
            elif dto.dtoType == "Output":
                entity_dtos[entity]["output"] = dto

        for entity_name, dtos in entity_dtos.items():
            input_dto = dtos.get("input")
            output_dto = dtos.get("output")
            if not input_dto:
                continue

            entity_fks = fk_fields.get(entity_name, {})
            exclude_sensitive = []
            if output_dto:
                exclude_sensitive = output_dto.excludeSensitiveFields

            fields: List[FieldMapping] = []
            for field in input_dto.fields:
                # Build validation config (shared by both widget and standard paths)
                validation = None
                if field.validation:
                    validation = ValidationConfig(
                        required=field.validation.required,
                        requiredMessage=field.validation.requiredMessage,
                        maxLength=field.validation.maxLength,
                        maxLengthMessage=field.validation.maxLengthMessage,
                        email=field.validation.email,
                        emailMessage=field.validation.emailMessage,
                        minLength=field.validation.minLength,
                        minLengthMessage=field.validation.minLengthMessage,
                        pattern=field.validation.pattern,
                        patternMessage=field.validation.patternMessage,
                    )

                # Widget override path: fieldWidget present and in the map
                widget_type = getattr(field, "fieldWidget", None)
                if widget_type and widget_type in WIDGET_COMPONENT_MAP:
                    comp_type = WIDGET_COMPONENT_MAP[widget_type]
                    widget_props: Dict = {"fieldWidget": widget_type}
                    if widget_type == "codeEditor":
                        widget_props["language"] = getattr(field, "language", None) or "javascript"
                    elif widget_type == "json":
                        widget_props["language"] = "json"
                    elif widget_type == "markdown":
                        widget_props["language"] = "markdown"

                    fields.append(FieldMapping(
                        fieldName=field.fieldName,
                        fieldLabel=to_display_label(field.fieldName),
                        componentType=comp_type,
                        javaType=field.javaType,
                        props=widget_props,
                        validation=validation,
                        includeInDTO=field.includeInDTO,
                    ))
                    continue

                # Standard TypeMapper path
                rel_info = entity_fks.get(field.fieldName)
                is_rel = rel_info is not None
                is_multi = rel_info.get("isLinkEntity", False) if rel_info else False
                related_entity = rel_info.get("relatedEntity") if rel_info else None
                rel_type = rel_info.get("type") if rel_info else None

                comp = TypeMapper.map_to_component(
                    java_type=field.javaType,
                    column_definition="",
                    relationship_type=rel_type,
                    is_link_entity=is_multi,
                )

                props: Dict = {}
                if comp.mode:
                    props["mode"] = comp.mode
                if is_rel and related_entity:
                    props["relatedEntity"] = related_entity
                    props["multiSelect"] = is_multi
                    # Display field: first non-ID string field (resolved at generation time)
                    props["displayField"] = "name"

                # Determine display field for autocomplete
                autocomplete_display: Optional[str] = None
                if is_rel and related_entity:
                    autocomplete_display = _find_display_field(
                        related_entity, entity_dtos
                    )

                fields.append(FieldMapping(
                    fieldName=field.fieldName,
                    fieldLabel=to_display_label(field.fieldName),
                    componentType=comp.component_type,
                    javaType=field.javaType,
                    props=props,
                    validation=validation,
                    isRelationshipField=is_rel,
                    relatedEntityName=related_entity,
                    isMultiSelect=is_multi,
                    autocompleteDisplayField=autocomplete_display,
                    includeInDTO=field.includeInDTO,
                ))

            mappings.append(ComponentMapping(
                entityName=entity_name,
                fields=fields,
                excludeSensitiveFields=exclude_sensitive,
            ))

        return mappings


def _find_display_field(entity_name: str, entity_dtos: Dict) -> str:
    """Find the first non-ID string field from an entity's Output DTO."""
    dtos = entity_dtos.get(entity_name, {})
    output_dto = dtos.get("output")
    if output_dto:
        for field in output_dto.fields:
            if field.javaType == "String" and not field.fieldName.lower().endswith("id"):
                return field.fieldName
    return "name"
