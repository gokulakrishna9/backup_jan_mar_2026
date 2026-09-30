"""Scaffold transformer — produces ScaffoldProperties from ReactAppDefinition."""

from typing import Tuple

from models.property_objects import EnvProperties, EnvVariableProperties, ScaffoldProperties
from models.react_definition_models import ReactAppDefinition


class ScaffoldTransformer:
    """Transforms React definition into scaffold properties for project files."""

    @staticmethod
    def transform(react_def: ReactAppDefinition) -> Tuple[ScaffoldProperties, EnvProperties]:
        """Produce scaffold and env properties from the React Application Definition.

        Args:
            react_def: Parsed React Application Definition.

        Returns:
            Tuple of (ScaffoldProperties, EnvProperties).
        """
        # Scan component_mappings for widget componentTypes to determine npm deps
        widget_deps = {}
        WIDGET_NPM_DEPS = {
            "QuillEditor": {"quill": "^2.0.3", "react-quill-new": "^3.3.4", "katex": "^0.16.11"},
            "MonacoEditor": {"@monaco-editor/react": "^4.6.0", "monaco-editor": "^0.52.0"},
            "MarkdownEditor": {
                "@monaco-editor/react": "^4.6.0", "monaco-editor": "^0.52.0",
                "marked": "^15.0.0", "dompurify": "^3.2.0",
            },
        }
        for mapping in react_def.component_mappings:
            for field in mapping.fields:
                if field.componentType in WIDGET_NPM_DEPS:
                    widget_deps.update(WIDGET_NPM_DEPS[field.componentType])

        scaffold = ScaffoldProperties(
            applicationName=react_def.layout.applicationName,
            apiPort=react_def.layout.apiPort,
            routes=react_def.routes,
            hasAuth=react_def.auth_config.jwtEnabled or react_def.auth_config.oauth2Enabled,
            widgetDependencies=widget_deps,
        )

        env_vars = [
            EnvVariableProperties(key=v.key, value=v.value, comment=v.comment)
            for v in react_def.env_config.variables
        ]
        env = EnvProperties(variables=env_vars)

        return scaffold, env
