"""Component mapping generator — produces component_mappings.json."""

import os

from models.definition_models import AppDefinition
from transformers.phase1.component_mapping_transformer import ComponentMappingTransformer
from utils.file_writer import FileWriter


class ComponentMappingGenerator:
    @staticmethod
    def generate(app_def: AppDefinition, output_dir: str) -> str:
        mappings = ComponentMappingTransformer.transform(
            app_def.dto_layer,
            app_def.relationships,
            app_def.entity_layer,
        )
        path = os.path.join(output_dir, "react_component_mappings.json")
        FileWriter.write_json(path, [m.model_dump() for m in mappings])
        return path
