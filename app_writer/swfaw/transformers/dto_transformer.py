"""DTO transformer - converts entity properties to DTO properties."""

from typing import List
from models.layer_objects import EntityLayerObject, DTOLayerObject, Field


class DTOTransformer:
    """Transforms entity properties into DTO properties."""
    
    @staticmethod
    def transform(entity: EntityLayerObject, dto_type: str) -> DTOLayerObject:
        """Transform entity to DTO properties with validation configurations.
        
        Args:
            entity: Entity layer object
            dto_type: Type of DTO (Input, Output, Filter)
            
        Returns:
            DTOLayerObject with appropriate fields and configurations
        """
        # Filter fields based on DTO type
        fields = DTOTransformer._filter_fields_for_dto_type(entity.fields, dto_type)
        
        # Generate field configurations with validation rules
        field_configs = DTOTransformer._generate_field_configs(fields, dto_type)
        
        return DTOLayerObject(
            entityName=entity.className,
            className=f"{entity.className}{dto_type}DTO",
            packageName=entity.packageName.replace('.entity', '.dto'),
            fields=fields,
            dtoType=dto_type,
            isRootEntity=entity.isRootEntity,
            fieldConfigs=field_configs,
            customValidators=[],
            excludeSensitiveFields=["password", "encryptedPassword"] if dto_type == "Output" else [],
            includeRelationships=True if dto_type == "Output" else False
        )
    
    @staticmethod
    def _filter_fields_for_dto_type(fields: List[Field], dto_type: str) -> List[Field]:
        """Filter fields based on DTO type.
        
        Args:
            fields: All entity fields
            dto_type: Input, Output, or Filter
            
        Returns:
            Filtered list of fields
        """
        if dto_type == 'Input':
            # Input DTO: exclude ID only
            filtered_fields = [f for f in fields if not f.isPrimaryKey]
            return filtered_fields
        
        elif dto_type == 'Output':
            # Output DTO: include all fields
            return fields
        
        elif dto_type == 'Filter':
            # Filter DTO: only include searchable fields (String, numeric, boolean)
            searchable_types = ['String', 'Long', 'Integer', 'Boolean', 'LocalDate', 'LocalDateTime']
            return [
                f for f in fields 
                if f.javaType in searchable_types
            ]
        
        return fields
    
    @staticmethod
    def _generate_field_configs(fields: List[Field], dto_type: str) -> List[dict]:
        """Generate field configurations with validation rules.
        
        Args:
            fields: List of fields
            dto_type: Type of DTO
            
        Returns:
            List of field configuration dictionaries
        """
        configs = []
        
        for field in fields:
            config = {
                "fieldName": field.fieldName,
                "javaType": field.javaType,
                "includeInDTO": True
            }
            
            if dto_type == 'Input':
                # Generate validation rules for Input DTOs
                validation = {}
                
                # Required validation
                if not field.isNullable:
                    validation["required"] = True
                    validation["requiredMessage"] = f"{field.fieldName.capitalize()} is required"
                
                # String validations
                if field.javaType == "String":
                    # Email validation
                    if "email" in field.fieldName.lower():
                        validation["email"] = True
                        validation["emailMessage"] = "Please provide a valid email address"
                    
                    # Extract max length from column definition (e.g., VARCHAR(255))
                    if "VARCHAR" in field.columnDefinition.upper():
                        try:
                            max_len = int(field.columnDefinition.split('(')[1].split(')')[0])
                            validation["maxLength"] = max_len
                            validation["maxLengthMessage"] = f"{field.fieldName.capitalize()} cannot exceed {max_len} characters"
                        except:
                            pass
                
                # Numeric validations
                if field.javaType in ["Integer", "Long", "BigDecimal"]:
                    if "age" in field.fieldName.lower():
                        validation["min"] = 0
                        validation["minMessage"] = f"{field.fieldName.capitalize()} must be positive"
                
                if validation:
                    config["validation"] = validation
            
            elif dto_type == 'Filter':
                # Add filter type for Filter DTOs
                if field.javaType == "String":
                    config["filterType"] = "LIKE"
                else:
                    config["filterType"] = "EQUALS"
            
            elif dto_type == 'Output':
                # Add format for date fields
                if field.javaType in ["LocalDateTime", "LocalDate"]:
                    config["format"] = "yyyy-MM-dd'T'HH:mm:ss" if field.javaType == "LocalDateTime" else "yyyy-MM-dd"
            
            configs.append(config)
        
        return configs
