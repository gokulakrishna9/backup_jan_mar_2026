"""Auth schema generator - generates authentication/authorization SQL schema.

Generates DDL from the static AUTH_SCHEMA_DDL template which contains
the simplified role-based authorization model (user_role, record_owner,
query_group, query_group_query, query_group_member, query_group_record)
plus retained tables (auth_user, system_config, access_audit_log, oauth2).

No dynamic INSERT statements are generated — the old group_definition_layer
prepopulation logic has been removed along with the document-group model.
"""

from templates.auth_schema_templates import AuthSchemaTemplates


class AuthSchemaGenerator:
    """Generates authentication and authorization database schema SQL."""

    @staticmethod
    def generate(group_definition=None) -> str:
        """Generate complete auth/authz schema SQL.

        Args:
            group_definition: Ignored. Retained for backward compatibility
                              with callers that still pass group_definition_layer data.

        Returns:
            SQL string with complete schema DDL for the simplified
            role-based authorization model.
        """
        sql_parts = [
            AuthSchemaTemplates.AUTH_SCHEMA_DDL,
            AuthSchemaTemplates.AUTH_SCHEMA_FOOTER,
        ]
        return "\n".join(sql_parts)
