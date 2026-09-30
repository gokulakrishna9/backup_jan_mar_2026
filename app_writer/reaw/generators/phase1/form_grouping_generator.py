"""Form grouping generator — produces form_groupings.json."""

import os

from models.definition_models import AppDefinition
from transformers.phase1.form_grouping_transformer import FormGroupingTransformer
from utils.file_writer import FileWriter


class FormGroupingGenerator:
    @staticmethod
    def generate(app_def: AppDefinition, output_dir: str) -> str:
        groupings = FormGroupingTransformer.transform(
            app_def.relationships,
            app_def.entity_layer,
        )
        path = os.path.join(output_dir, "react_form_groupings.json")
        FileWriter.write_json(path, [g.model_dump() for g in groupings])
        return path
