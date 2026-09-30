"""DTO generator - populates DTO templates."""

from jinja2 import Template
from models.layer_objects import DTOLayerObject
from templates.dto_templates import DTOTemplates


class DTOGenerator:
    """Generates DTO Java code from DTO layer object."""
    
    @staticmethod
    def generate(dto: DTOLayerObject) -> str:
        """Generate DTO Java code with validation configurations.
        
        Args:
            dto: DTO layer object with all properties
            
        Returns:
            Generated Java code as string
        """
        # Select template based on DTO type
        if dto.dtoType == 'Input':
            template_str = DTOTemplates.INPUT_DTO_TEMPLATE
            has_public_flag = dto.isRootEntity and not any(f.fieldName == 'isPublic' for f in dto.fields)
            has_audit_fields = False
        elif dto.dtoType == 'Output':
            template_str = DTOTemplates.OUTPUT_DTO_TEMPLATE
            has_public_flag = False
            has_audit_fields = True
        else:  # Filter
            template_str = DTOTemplates.FILTER_DTO_TEMPLATE
            has_public_flag = False
            has_audit_fields = False
        
        # Prepare template context
        context = {
            'packageName': dto.packageName,
            'entityName': dto.entityName,
            'className': dto.className,
            'fields': dto.fields,
            'fieldConfigs': dto.fieldConfigs,
            'customValidators': dto.customValidators,
            'excludeSensitiveFields': dto.excludeSensitiveFields,
            'includeRelationships': dto.includeRelationships,
            'hasPublicFlag': has_public_flag,
            'hasAuditFields': has_audit_fields
        }
        
        # Render template
        template = Template(template_str)
        return template.render(context)

