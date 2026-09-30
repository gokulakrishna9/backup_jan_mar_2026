"""Repository generator - populates repository templates."""

from jinja2 import Template
from models.layer_objects import RepositoryLayerObject
from templates.repository_templates import RepositoryTemplates
from templates.sql_builder import (
    auth_paged_query, auth_count_query,
    paged_query, simple_count_query,
)


class RepositoryGenerator:
    """Generates repository Java code from repository layer object."""
    
    @staticmethod
    def generate(repository: RepositoryLayerObject) -> str:
        """Generate repository Java code.
        
        Args:
            repository: Repository layer object with all properties
            
        Returns:
            Generated Java code as string
        """
        # Determine entity package and table name
        entity_package = repository.packageName.replace('.repository', '.entity')
        
        # Use definition-provided tableName/idColumn if available, otherwise derive (legacy)
        if repository.tableName:
            table_name = repository.tableName
        else:
            table_name = ('ems_'
                + ''.join(['_' + c.lower() if c.isupper() else c
                           for c in repository.entityName]).lstrip('_'))
        
        if repository.idColumn:
            id_column = repository.idColumn
        else:
            id_column = repository.entityName.lower() + '_id'
        
        # Check if this is an authorization-related repository
        is_entity_authorization = repository.entityName == 'EntityAuthorization'
        is_user_group_membership = repository.entityName == 'UserGroupMembership'
        
        # Build SQL queries via sql_builder (PyPika)
        sd = repository.hasSoftDelete
        paged_sql = paged_query(table_name, id_column, soft_delete=sd)
        count_sql = simple_count_query(table_name, soft_delete=sd)

        auth_paged_sql = ""
        auth_count_sql = ""
        if repository.hasAuthorization:
            auth_paged_sql = auth_paged_query(table_name, id_column, soft_delete=sd)
            auth_count_sql = auth_count_query(table_name, id_column, soft_delete=sd)
        
        # Prepare template context
        context = {
            'packageName': repository.packageName,
            'entityPackage': entity_package,
            'entityName': repository.entityName,
            'className': repository.className,
            'idType': repository.idType,
            'tableName': table_name,
            'idColumn': id_column,
            'hasSoftDelete': repository.hasSoftDelete,
            'hasAuthorization': repository.hasAuthorization,
            'singleRecordPerUser': repository.singleRecordPerUser,
            'isEntityAuthorization': is_entity_authorization,
            'isUserGroupMembership': is_user_group_membership,
            # Pre-built SQL from sql_builder
            'pagedQuery': paged_sql,
            'countQuery': count_sql,
            'authPagedQuery': auth_paged_sql,
            'authCountQuery': auth_count_sql,
        }
        
        # Render template
        template = Template(RepositoryTemplates.REPOSITORY_TEMPLATE)
        return template.render(context)
