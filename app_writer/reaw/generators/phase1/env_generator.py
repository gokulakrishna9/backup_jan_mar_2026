"""Env generator — produces react_env.json."""

import os

from models.definition_models import AppDefinition
from transformers.phase1.env_transformer import EnvTransformer
from utils.file_writer import FileWriter


class EnvGenerator:
    @staticmethod
    def generate(app_def: AppDefinition, output_dir: str) -> str:
        env_def = EnvTransformer.transform(app_def)
        path = os.path.join(output_dir, "react_env.json")
        FileWriter.write_json(path, env_def.model_dump())
        return path
