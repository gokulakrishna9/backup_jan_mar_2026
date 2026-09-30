"""Query component generator — produces per-entity QuerySection.jsx."""

import os
from typing import Dict, List

from jinja2 import Template

from models.react_definition_models import ReactAppDefinition
from transformers.phase2.query_component_transformer import QueryComponentTransformer
from templates.query_component_templates import QUERY_SECTION
from utils.file_writer import FileWriter
from utils.string_utils import to_camel_case


class QueryComponentGenerator:
    @staticmethod
    def generate(react_def: ReactAppDefinition, output_dir: str, query_entities: Dict[str, List[Dict]]) -> List[str]:
        sections = QueryComponentTransformer.transform(query_entities)
        files = []

        for section in sections:
            entity_dir = os.path.join(
                output_dir, "src", "components", "entities",
                to_camel_case(section.entityName),
            )
            content = Template(QUERY_SECTION).render(**section.model_dump())
            path = os.path.join(entity_dir, f"{section.entityNamePascal}QuerySection.jsx")
            FileWriter.write_file(path, content)
            files.append(path)

        return files
