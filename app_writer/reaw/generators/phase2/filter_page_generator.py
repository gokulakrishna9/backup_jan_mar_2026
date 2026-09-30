"""Filter page generator — produces per-entity FilterPage.jsx."""

import os
from typing import List

from jinja2 import Template

from models.react_definition_models import ReactAppDefinition
from transformers.phase2.filter_page_transformer import FilterPageTransformer
from templates.filter_page_templates import FILTER_PAGE
from utils.file_writer import FileWriter
from utils.string_utils import to_camel_case


class FilterPageGenerator:
    @staticmethod
    def generate(react_def: ReactAppDefinition, output_dir: str) -> List[str]:
        pages = FilterPageTransformer.transform(react_def.page_definitions)
        files = []

        for page in pages:
            ctx = page.model_dump()
            ctx["entityNameCamel"] = to_camel_case(page.entityName)
            content = Template(FILTER_PAGE).render(**ctx)
            path = os.path.join(
                output_dir, "src", "pages", "filters",
                f"{page.entityNamePascal}FilterPage.jsx",
            )
            FileWriter.write_file(path, content)
            files.append(path)

        return files
