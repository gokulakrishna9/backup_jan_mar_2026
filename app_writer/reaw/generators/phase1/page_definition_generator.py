"""Page definition generator — produces page_definitions.json."""

import os
from typing import List

from models.definition_models import AppDefinition
from models.react_definition_models import FormGrouping
from transformers.phase1.page_definition_transformer import PageDefinitionTransformer
from utils.file_writer import FileWriter


class PageDefinitionGenerator:
    @staticmethod
    def generate(
        app_def: AppDefinition,
        output_dir: str,
        form_groupings: List[FormGrouping],
    ) -> str:
        pages = PageDefinitionTransformer.transform(
            app_def.entity_layer,
            app_def.filter_layer,
            app_def.query_layer,
            form_groupings,
        )
        path = os.path.join(output_dir, "react_page_definitions.json")
        FileWriter.write_json(path, [p.model_dump() for p in pages])
        return path
