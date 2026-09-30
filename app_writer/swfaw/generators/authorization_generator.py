"""Authorization generator - DEPRECATED.

This module is deprecated. The old AuthorizationService and AccessLevelConstants
templates have been replaced by the simplified role-based authorization model.

Use authorization_service_generator.py instead, which provides:
- generate_role_authorization_service
- generate_authorization_web_filter
- generate_entity_table_annotation
- generate_table_access_annotation
- generate_query_access_annotation
"""

from generators.authorization_service_generator import AuthorizationServiceGenerator


class AuthorizationGenerator:
    """DEPRECATED: Use AuthorizationServiceGenerator instead.
    
    This class is retained only for backward compatibility with imports.
    All old methods (generate, generate_access_level_constants) have been removed.
    """
    pass
