"""Env transformer — produces EnvDefinition from swfaw AppDefinition."""

from models.definition_models import AppDefinition
from models.react_definition_models import EnvDefinition, EnvVariable


class EnvTransformer:
    """Transforms swfaw app definition into env config for the React app."""

    @staticmethod
    def transform(app_def: AppDefinition) -> EnvDefinition:
        port = app_def.project_metadata.projectMetadata.port if app_def.project_metadata else 8081
        return EnvDefinition(
            variables=[
                EnvVariable(
                    key="VITE_API_URL",
                    value=f"http://localhost:{port}",
                    comment="Backend API base URL. Leave empty to use Vite proxy in dev.",
                ),
                EnvVariable(
                    key="VITE_ENABLE_LOGGING",
                    value="true",
                    comment="Enable client-side logging (API errors, network errors, data errors). Set to false to disable.",
                ),
            ]
        )
