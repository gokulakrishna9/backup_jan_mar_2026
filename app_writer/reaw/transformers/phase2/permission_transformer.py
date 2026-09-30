"""Permission transformer — produces permission hook properties from AuthConfig."""

from models.react_definition_models import AuthConfig


class PermissionTransformer:
    """Transforms auth config into permission hook properties."""

    @staticmethod
    def transform(auth_config: AuthConfig) -> dict:
        """Produce permission hook properties.

        Args:
            auth_config: Auth config from auth_config.json.

        Returns:
            Dict with permissionsEndpoint for the usePermissions hook template.
        """
        return {
            "permissionsEndpoint": auth_config.permissionsEndpoint,
        }
