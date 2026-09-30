"""Auth config transformer — derives auth configuration from security and authorization layers."""

from typing import List

from models.definition_models import AuthorizationLayerDef, ControllerLayerDef, SecurityLayerDef
from models.react_definition_models import AuthConfig
from utils.string_utils import to_kebab_case


class AuthConfigTransformer:
    """Transforms security and authorization layers into auth config."""

    @staticmethod
    def transform(
        security_layer: SecurityLayerDef,
        authorization_layer: AuthorizationLayerDef,
        controller_layer: ControllerLayerDef,
    ) -> AuthConfig:
        """Produce auth configuration from security settings.

        Args:
            security_layer: Parsed security layer with JWT/OAuth2 config.
            authorization_layer: Parsed authorization layer.
            controller_layer: Parsed controller layer for protected routes.

        Returns:
            AuthConfig with JWT/OAuth2 flags and protected routes.
        """
        jwt_enabled = False
        refresh_enabled = False
        oauth2_enabled = False
        oauth2_providers: List[str] = []

        if security_layer.jwt:
            jwt_enabled = security_layer.jwt.enabled
            if security_layer.jwt.refreshToken:
                refresh_enabled = security_layer.jwt.refreshToken.enabled

        if security_layer.oauth2:
            oauth2_enabled = security_layer.oauth2.enabled
            oauth2_providers = [p.name for p in security_layer.oauth2.providers]

        # Collect protected routes from controllers with requiresAuth endpoints
        protected_routes: List[str] = []
        for ctrl in controller_layer.controllers:
            has_auth_endpoint = any(
                ep.requiresAuth for ep in ctrl.endpoints.values() if ep.enabled
            )
            if has_auth_endpoint:
                kebab = to_kebab_case(ctrl.entityName)
                protected_routes.append(f"/{kebab}")

        # Derive auth endpoints from publicEndpoints in security layer
        login_endpoint = "/api/auth/login"
        register_endpoint = "/api/auth/register"
        permissions_endpoint = "/api/auth/permissions"
        for ep in security_layer.publicEndpoints:
            ep_str = ep if isinstance(ep, str) else ""
            ep_lower = ep_str.lower()
            if "login" in ep_lower and "oauth" not in ep_lower:
                login_endpoint = ep_str.rstrip("*").rstrip("/") if ep_str.endswith("/**") else ep_str
            elif "register" in ep_lower:
                register_endpoint = ep_str.rstrip("*").rstrip("/") if ep_str.endswith("/**") else ep_str

        # Derive permissions endpoint from login endpoint prefix
        # e.g. /api/v1/auth/login -> /api/v1/auth/permissions
        auth_prefix = login_endpoint.rsplit("/login", 1)[0] if "/login" in login_endpoint else "/api/auth"
        permissions_endpoint = f"{auth_prefix}/permissions"

        return AuthConfig(
            jwtEnabled=jwt_enabled,
            oauth2Enabled=oauth2_enabled,
            oauth2Providers=oauth2_providers,
            refreshTokenEnabled=refresh_enabled,
            protectedRoutes=sorted(protected_routes),
            permissionsEndpoint=permissions_endpoint,
            loginEndpoint=login_endpoint,
            registerEndpoint=register_endpoint,
            registerEnabled=True,
        )
