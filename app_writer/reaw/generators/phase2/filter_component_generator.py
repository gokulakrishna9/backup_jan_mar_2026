"""Filter component generator — produces per-entity FilterPanel.jsx."""

import os
from typing import Dict, List

from jinja2 import Template

from models.react_definition_models import ReactAppDefinition
from transformers.phase2.filter_component_transformer import FilterComponentTransformer
from templates.filter_component_templates import FILTER_PANEL
from utils.file_writer import FileWriter
from utils.string_utils import to_camel_case


class FilterComponentGenerator:
    @staticmethod
    def generate(react_def: ReactAppDefinition, output_dir: str, filter_entities: Dict[str, List[Dict]]) -> List[str]:
        panels = FilterComponentTransformer.transform(
            react_def.component_mappings, filter_entities
        )
        files = []

        for panel in panels:
            entity_dir = os.path.join(
                output_dir, "src", "components", "entities",
                to_camel_case(panel.entityName),
            )
            content = Template(FILTER_PANEL).render(**panel.model_dump())
            path = os.path.join(entity_dir, f"{panel.entityNamePascal}FilterPanel.jsx")
            FileWriter.write_file(path, content)
            files.append(path)

        return files
