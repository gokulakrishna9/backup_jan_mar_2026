"""Entity generator - populates entity templates."""

from jinja2 import Template
from models.layer_objects import EntityLayerObject
from templates.entity_templates import EntityTemplates


class EntityGenerator:
    """Generates entity Java code from entity layer object."""
    
    @staticmethod
    def generate(entity: EntityLayerObject) -> str:
        """Generate entity Java code.
        
        Args:
            entity: Entity layer object with all properties
            
        Returns:
            Generated Java code as string
        """
        # Separate regular fields from audit/soft delete fields
        audit_field_names = ['createdAt', 'updatedAt', 'deletedAt']
        regular_fields = [f for f in entity.fields if f.fieldName not in audit_field_names]
        
        # Prepare template context
        context = {
            'packageName': entity.packageName,
            'tableName': entity.tableName,
            'className': entity.className,
            'isRootEntity': entity.isRootEntity,
            'parentEntity': entity.parentEntity,
            'regularFields': regular_fields,
            'hasAuditFields': entity.hasAuditFields,
            'hasSoftDelete': entity.hasSoftDelete
        }
        
        # Render template
        template = Template(EntityTemplates.ENTITY_TEMPLATE)
        return template.render(context)
