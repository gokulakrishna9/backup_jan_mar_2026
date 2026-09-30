"""Auth config generator — produces auth_config.json."""

import os

from models.definition_models import AppDefinition
from transformers.phase1.auth_config_transformer import AuthConfigTransformer
from utils.file_writer import FileWriter


class AuthConfigGenerator:
    @staticmethod
    def generate(app_def: AppDefinition, output_dir: str) -> str:
        auth = AuthConfigTransformer.transform(
            app_def.security_layer,
            app_def.authorization_layer,
            app_def.controller_layer,
        )
        path = os.path.join(output_dir, "react_auth_config.json")
        FileWriter.write_json(path, auth.model_dump())
        return path
