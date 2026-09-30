"""Authorization templates - DEPRECATED.

This module is deprecated. The old AUTHORIZATION_SERVICE_TEMPLATE and
ACCESS_LEVEL_CONSTANTS_TEMPLATE have been replaced by the simplified
role-based authorization model.

Use authorization_service_templates.py instead, which provides:
- ROLE_AUTHORIZATION_SERVICE
- AUTHORIZATION_WEB_FILTER
- ENTITY_TABLE_ANNOTATION
- TABLE_ACCESS_ANNOTATION
- QUERY_ACCESS_ANNOTATION
"""


class AuthorizationTemplates:
    """DEPRECATED: Use AuthorizationServiceTemplates instead.
    
    This class is retained only for backward compatibility with imports.
    All old templates have been removed.
    """
    pass
