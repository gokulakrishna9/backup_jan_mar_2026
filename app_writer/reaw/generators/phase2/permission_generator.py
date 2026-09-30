"""Permission generator — produces usePermissions.js."""

import os
from typing import List

from jinja2 import Template

from models.react_definition_models import ReactAppDefinition
from transformers.phase2.permission_transformer import PermissionTransformer
from templates.permission_templates import USE_PERMISSIONS
from utils.file_writer import FileWriter


class PermissionGenerator:
    @staticmethod
    def generate(react_def: ReactAppDefinition, output_dir: str) -> List[str]:
        props = PermissionTransformer.transform(react_def.auth_config)
        content = Template(USE_PERMISSIONS).render(**props)
        path = os.path.join(output_dir, "src", "hooks", "usePermissions.js")
        FileWriter.write_file(path, content)
        return [path]
