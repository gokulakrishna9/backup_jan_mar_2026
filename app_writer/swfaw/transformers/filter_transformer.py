"""Filter transformer - creates filter layer properties from entities."""

from typing import List
from models.layer_objects import EntityLayerObject, FilterLayerObject, FilterField


class FilterTransformer:
    """Transforms entity list into filter layer properties."""
    
    # Mapping of SQL types to Java types
    TYPE_MAPPING = {
        'VARCHAR': 'String',
        'CHAR': 'String',
        'TEXT': 'String',
        'LONGTEXT': 'String',
        'MEDIUMTEXT': 'String',
        'TINYTEXT': 'String',
        'INT': 'Integer',
        'INTEGER': 'Integer',
        'BIGINT': 'Long',
        'SMALLINT': 'Short',
        'TINYINT': 'Byte',
        'DECIMAL': 'BigDecimal',
        'NUMERIC': 'BigDecimal',
        'FLOAT': 'Float',
        'DOUBLE': 'Double',
        'BOOLEAN': 'Boolean',
        'BIT': 'Boolean',
        'DATE': 'LocalDate',
        'DATETIME': 'LocalDateTime',
        'TIMESTAMP': 'LocalDateTime',
        'TIME': 'LocalTime'
    }
    
    # Default operators by type
    STRING_OPERATORS = ['equals', 'contains', 'startsWith', 'endsWith', 'in']
    NUMERIC_OPERATORS = ['equals', 'greaterThan', 'lessThan', 'between', 'in']
    BOOLEAN_OPERATORS = ['equals']
    DATE_OPERATORS = ['equals', 'greaterThan', 'lessThan', 'between']
    
    @staticmethod
    def transform(entities: List[EntityLayerObject], package_name: str = "com.example") -> List[FilterLayerObject]:
        """Transform entities to filter layer properties.
        
        Args:
            entities: List of all entity layer objects
            package_name: Base package name
            
        Returns:
            List of FilterLayerObject (one per entity with default filters)
        """
        filter_layers = []
        
        for entity in entities:
            filter_fields = []
            
            # Create filter fields for each entity field (except audit fields)
            for field in entity.fields:
                # Skip audit fields and soft delete
                if field.fieldName in ['createdById', 'updatedById', 'createdDate', 'updatedDate', 'isDeleted']:
                    continue
                
                # Determine operators based on field type
                operators = FilterTransformer._get_operators_for_type(field.javaType)
                
                filter_field = FilterField(
                    name=field.fieldName,
                    type=field.javaType,
                    operators=operators
                )
                filter_fields.append(filter_field)
            
            filter_layer = FilterLayerObject(
                entityName=entity.className,
                fields=filter_fields,
                packageName=f"{package_name}.filter"
            )
            filter_layers.append(filter_layer)
        
        return filter_layers
    
    @staticmethod
    def _get_operators_for_type(java_type: str) -> List[str]:
        """Get default operators for a Java type."""
        if java_type in ['String']:
            return FilterTransformer.STRING_OPERATORS
        elif java_type in ['Integer', 'Long', 'Short', 'Byte', 'BigDecimal', 'Float', 'Double']:
            return FilterTransformer.NUMERIC_OPERATORS
        elif java_type in ['Boolean']:
            return FilterTransformer.BOOLEAN_OPERATORS
        elif java_type in ['LocalDate', 'LocalDateTime', 'LocalTime']:
            return FilterTransformer.DATE_OPERATORS
        else:
            # Default to basic operators
            return ['equals', 'in']
