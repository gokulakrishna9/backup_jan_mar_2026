"""Service generator - populates service templates."""

from jinja2 import Template
from models.layer_objects import ServiceLayerObject, EntityLayerObject
from templates.service_templates import ServiceTemplates


class ServiceGenerator:
    """Generates service Java code from service layer object."""
    
    @staticmethod
    def generate(service: ServiceLayerObject, entity: EntityLayerObject = None) -> str:
        """Generate service Java code.
        
        Args:
            service: Service layer object with all properties
            entity: Optional entity layer object for field information
            
        Returns:
            Generated Java code as string
        """
        # Determine package names
        base_package = service.packageName.replace('.service', '')
        entity_package = f"{base_package}.entity"
        dto_package = f"{base_package}.dto"
        repository_package = f"{base_package}.repository"
        security_package = f"{base_package}.security"
        service_package = f"{base_package}.service"
        exception_package = f"{base_package}.exception"
        
        # Prepare fields from entity
        fields = []
        all_fields = []
        has_audit_fields = False
        has_soft_delete = False
        
        # Audit field names to exclude from regular field lists
        audit_field_names = ['createdById', 'updatedById', 'createdOn', 'updatedOn',
                             'createdAt', 'updatedAt', 'deletedAt', 'isDeleted']
        
        # Sensitive fields to exclude from output DTO mapping
        sensitive_field_names = ['password', 'encryptedPassword']
        
        output_fields = []
        
        if entity and entity.fields:
            has_audit_fields = entity.hasAuditFields
            has_soft_delete = entity.hasSoftDelete
            
            for f in entity.fields:
                if f.fieldName in audit_field_names:
                    continue
                field_cap = f.fieldName[0].upper() + f.fieldName[1:]
                field_data = {
                    'fieldName': f.fieldName,
                    'fieldNameCapitalized': field_cap,
                    'javaType': f.javaType,
                    'isPrimaryKey': f.isPrimaryKey
                }
                all_fields.append(field_data)
                # Exclude sensitive fields from output DTO mapping
                if f.fieldName not in sensitive_field_names:
                    output_fields.append(field_data)
                # Exclude primary key from input fields
                if not f.isPrimaryKey:
                    fields.append(field_data)
        
        # Get the actual ID field name from entity if available
        if entity and entity.fields:
            id_field = next((f for f in entity.fields if f.isPrimaryKey), None)
            if id_field:
                id_field_capitalized = id_field.fieldName[0].upper() + id_field.fieldName[1:]
            else:
                id_field_capitalized = service.entityName + "Id"
        else:
            id_field_capitalized = service.entityName + "Id"
        
        # Convert entity name to table name (camelCase to snake_case)
        table_name = ''.join(['_' + c.lower() if c.isupper() else c for c in service.entityName]).lstrip('_')
        
        # Activity tracking is enabled when authorization is enabled
        has_activity_tracking = service.hasAuthorization
        
        # Prepare template context
        context = {
            'packageName': service.packageName,
            'entityPackage': entity_package,
            'dtoPackage': dto_package,
            'repositoryPackage': repository_package,
            'securityPackage': security_package,
            'servicePackage': service_package,
            'exceptionPackage': exception_package,
            'authPackage': f"{base_package}.auth",
            'entityName': service.entityName,
            'tableName': table_name,
            'className': service.className,
            'repositoryName': service.repositoryName,
            'hasAuthorization': service.hasAuthorization,
            'singleRecordPerUser': service.singleRecordPerUser,
            'hasAuditFields': has_audit_fields,
            'hasSoftDelete': has_soft_delete,
            'hasActivityTracking': has_activity_tracking,
            'fields': fields,
            'allFields': all_fields,
            'outputFields': output_fields,
            'idFieldCapitalized': id_field_capitalized
        }
        
        # Render template
        template = Template(ServiceTemplates.SERVICE_TEMPLATE)
        return template.render(context)
