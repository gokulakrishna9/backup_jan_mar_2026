"""Auth transformer — produces AuthProperties from AuthConfig and component mappings."""

from typing import List, Optional

from models.property_objects import AuthProperties, FormFieldProperties
from models.react_definition_models import AuthConfig, ComponentMapping
from utils.string_utils import to_display_label


class AuthTransformer:
    """Transforms auth config into authentication properties."""

    @staticmethod
    def transform(
        auth_config: AuthConfig,
        component_mappings: List[ComponentMapping],
    ) -> AuthProperties:
        """Produce auth properties for login, register, AuthContext, ProtectedRoute.

        Args:
            auth_config: Auth config from auth_config.json.
            component_mappings: Component mappings to find User entity fields
                                for the registration page.

        Returns:
            AuthProperties for template rendering.
        """
        # Find User entity component mapping for registration form fields
        user_fields: List[FormFieldProperties] = []
        user_mapping: Optional[ComponentMapping] = None
        for mapping in component_mappings:
            if mapping.entityName.lower() in ("user", "users", "app_user", "app_users"):
                user_mapping = mapping
                break

        if user_mapping and auth_config.registerEnabled:
            for field in user_mapping.fields:
                if not field.includeInDTO:
                    continue
                user_fields.append(FormFieldProperties(
                    fieldName=field.fieldName,
                    fieldLabel=field.fieldLabel or to_display_label(field.fieldName),
                    componentType=field.componentType,
                    javaType=field.javaType,
                    columnDefinition=field.columnDefinition,
                    props=field.props,
                    validation=field.validation,
                    isRelationshipField=field.isRelationshipField,
                    relatedEntityName=field.relatedEntityName,
                    isMultiSelect=field.isMultiSelect,
                    autocompleteDisplayField=field.autocompleteDisplayField,
                ))

        return AuthProperties(
            jwtEnabled=auth_config.jwtEnabled,
            oauth2Enabled=auth_config.oauth2Enabled,
            oauth2Providers=auth_config.oauth2Providers,
            refreshTokenEnabled=auth_config.refreshTokenEnabled,
            permissionsEndpoint=auth_config.permissionsEndpoint,
            loginEndpoint=auth_config.loginEndpoint,
            registerEndpoint=auth_config.registerEndpoint,
            registerEnabled=auth_config.registerEnabled,
            userEntityInputFields=user_fields,
        )
