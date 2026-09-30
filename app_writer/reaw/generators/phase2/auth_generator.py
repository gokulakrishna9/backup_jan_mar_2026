"""Auth generator — produces LoginPage, RegisterPage, AuthContext, ProtectedRoute."""

import os
from typing import List

from jinja2 import Template

from models.react_definition_models import ReactAppDefinition
from transformers.phase2.auth_transformer import AuthTransformer
from templates.auth_templates import LOGIN_PAGE, REGISTER_PAGE, AUTH_CONTEXT, PROTECTED_ROUTE
from utils.file_writer import FileWriter


class AuthGenerator:
    @staticmethod
    def generate(react_def: ReactAppDefinition, output_dir: str) -> List[str]:
        props = AuthTransformer.transform(react_def.auth_config, react_def.component_mappings)
        ctx = props.model_dump()
        files = []

        for template_str, filename in [
            (LOGIN_PAGE, "LoginPage.jsx"),
            (REGISTER_PAGE, "RegisterPage.jsx"),
            (AUTH_CONTEXT, "AuthContext.jsx"),
            (PROTECTED_ROUTE, "ProtectedRoute.jsx"),
        ]:
            content = Template(template_str).render(**ctx)
            path = os.path.join(output_dir, "src", "auth", filename)
            FileWriter.write_file(path, content)
            files.append(path)

        return files
