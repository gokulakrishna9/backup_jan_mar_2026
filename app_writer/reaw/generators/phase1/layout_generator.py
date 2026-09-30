"""Layout generator — produces layout.json."""

import os

from models.definition_models import AppDefinition
from transformers.phase1.layout_transformer import LayoutTransformer
from utils.file_writer import FileWriter


class LayoutGenerator:
    @staticmethod
    def generate(app_def: AppDefinition, output_dir: str) -> str:
        layout = LayoutTransformer.transform(
            app_def.entity_layer,
            app_def.controller_layer,
            app_def.project_metadata,
        )
        path = os.path.join(output_dir, "react_layout.json")
        FileWriter.write_json(path, layout.model_dump())
        return path
