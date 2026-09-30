"""Entity transformer - converts database table to entity properties."""

from typing import List
from models.database_definition import Table, Column
from models.layer_objects import EntityLayerObject, Field
from utils.string_utils import to_pascal_case, to_camel_case, map_sql_type_to_java


class EntityTransformer:
    """Transforms database table definition into entity properties."""
    
    ROOT_ENTITIES = ['course', 'institution', 'jobpost', 'community', 'user']
    
    @staticmethod
    def determine_if_root_entity(table: Table) -> bool:
        """Determine if table represents a root entity."""
        entity_name = table.name.replace('ems_', '').lower()
        return entity_name in EntityTransformer.ROOT_ENTITIES
    
    @staticmethod
    def find_parent_entity(table: Table) -> str:
        """Find parent entity if this is a sub-entity."""
        for column in table.columns:
            if column.name.endswith('_id') and column.foreignKey:
                return to_pascal_case(column.foreignKey.get('table', ''))
        return None
    
    @staticmethod
    def transform(table: Table, package_name: str = "com.example") -> EntityLayerObject:
        """Transform database table to entity properties.
        
        Args:
            table: Database table definition
            package_name: Java package name
            
        Returns:
            EntityLayerObject with all properties
        """
        is_root_entity = EntityTransformer.determine_if_root_entity(table)
        parent_entity = EntityTransformer.find_parent_entity(table)
        
        # Process columns to fields
        fields = []
        
        for column in table.columns:
            field_name = to_camel_case(column.name)
            
            field = Field(
                columnName=column.name,
                fieldName=field_name,
                javaType=map_sql_type_to_java(column.type),
                isPrimaryKey=column.primaryKey,
                isNullable=column.nullable,
                columnDefinition=column.type
            )
            fields.append(field)
        
        # Add is_public field for root entities
        if is_root_entity:
            fields.append(Field(
                columnName='is_public',
                fieldName='isPublic',
                javaType='Boolean',
                isPrimaryKey=False,
                isNullable=False,
                columnDefinition='BOOLEAN DEFAULT FALSE'
            ))
        
        return EntityLayerObject(
            tableName=table.name,
            className=to_pascal_case(table.name),
            packageName=f"{package_name}.entity",
            fields=fields,
            isRootEntity=is_root_entity,
            parentEntity=parent_entity,
            hasPublicFlag=is_root_entity,
            hasAuditFields=False,
            hasSoftDelete=False
        )
