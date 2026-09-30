"""Grouped form generator — produces per-parent GroupedForm.jsx."""

import os
from typing import List

from jinja2 import Environment

from models.react_definition_models import ReactAppDefinition
from templates.grouped_form_templates import GROUPED_FORM
from utils.file_writer import FileWriter
from utils.string_utils import to_camel_case, to_pascal_case


class GroupedFormGenerator:
    @staticmethod
    def generate(react_def: ReactAppDefinition, output_dir: str) -> List[str]:
        files = []
        env = Environment()
        env.filters["camelCase"] = to_camel_case
        env.filters["pascalCase"] = to_pascal_case

        # Build entity → PK field lookup from redux store
        pk_map = {store.entityName: store.pkField for store in react_def.redux_store}

        for grouping in react_def.form_groupings:
            entity_dir = os.path.join(
                output_dir, "src", "components", "entities",
                to_camel_case(grouping.parentEntity),
            )
            ctx = {
                "entityNamePascal": to_pascal_case(grouping.parentEntity),
                "pkField": pk_map.get(grouping.parentEntity, "id"),
                "groupTabs": [t.model_dump() for t in grouping.tabs],
            }
            content = env.from_string(GROUPED_FORM).render(**ctx)
            path = os.path.join(entity_dir, f"{to_pascal_case(grouping.parentEntity)}GroupedForm.jsx")
            FileWriter.write_file(path, content)
            files.append(path)

        return files
