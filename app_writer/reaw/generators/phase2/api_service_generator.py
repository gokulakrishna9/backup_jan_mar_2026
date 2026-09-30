"""API service generator — produces apiClient.js and per-entity service files."""

import os
from typing import List

from jinja2 import Template

from models.react_definition_models import ReactAppDefinition
from transformers.phase2.api_service_transformer import ApiServiceTransformer
from templates.api_service_templates import API_CLIENT, ENTITY_SERVICE
from utils.file_writer import FileWriter
from utils.string_utils import to_camel_case, to_pascal_case


class ApiServiceGenerator:
    @staticmethod
    def generate(react_def: ReactAppDefinition, output_dir: str) -> List[str]:
        client_props, service_list = ApiServiceTransformer.transform(
            react_def.api_services, react_def.layout,
            refresh_token_enabled=react_def.auth_config.refreshTokenEnabled if react_def.auth_config else True,
        )
        files = []

        # apiClient.js
        content = Template(API_CLIENT).render(**client_props.model_dump())
        path = os.path.join(output_dir, "src", "services", "apiClient.js")
        FileWriter.write_file(path, content)
        files.append(path)

        # Per-entity service files
        for svc in service_list:
            ctx = svc.model_dump()
            ctx["entityNamePascal"] = to_pascal_case(svc.entityName)
            content = Template(ENTITY_SERVICE).render(**ctx)
            path = os.path.join(output_dir, "src", "services", f"{to_camel_case(svc.entityName)}Service.js")
            FileWriter.write_file(path, content)
            files.append(path)

        return files
