"""Entity component generator — produces per-entity Form.jsx and DataTable.jsx."""

import os
from typing import List

from jinja2 import Template

from models.react_definition_models import ReactAppDefinition
from transformers.phase2.entity_component_transformer import EntityComponentTransformer
from templates.entity_component_templates import ENTITY_FORM, ENTITY_DATATABLE
from utils.file_writer import FileWriter
from utils.string_utils import to_camel_case


class EntityComponentGenerator:
    @staticmethod
    def generate(react_def: ReactAppDefinition, output_dir: str) -> List[str]:
        results = EntityComponentTransformer.transform(
            react_def.component_mappings,
            react_def.api_services,
            react_def.form_groupings,
            react_def.redux_store,
            react_def.page_definitions,
        )
        files = []

        for form_props, table_props in results:
            entity_dir = os.path.join(
                output_dir, "src", "components", "entities",
                to_camel_case(form_props.entityName),
            )

            # Form
            content = Template(ENTITY_FORM).render(**form_props.model_dump())
            path = os.path.join(entity_dir, f"{form_props.entityNamePascal}Form.jsx")
            FileWriter.write_file(path, content)
            files.append(path)

            # DataTable
            content = Template(ENTITY_DATATABLE).render(**table_props.model_dump())
            path = os.path.join(entity_dir, f"{table_props.entityNamePascal}DataTable.jsx")
            FileWriter.write_file(path, content)
            files.append(path)

        return files
