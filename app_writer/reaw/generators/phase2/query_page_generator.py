"""Query page generator — produces per-entity QueryPage.jsx."""

import os
from typing import List

from jinja2 import Template

from models.react_definition_models import ReactAppDefinition
from transformers.phase2.query_page_transformer import QueryPageTransformer
from templates.query_page_templates import QUERY_PAGE
from utils.file_writer import FileWriter
from utils.string_utils import to_camel_case


class QueryPageGenerator:
    @staticmethod
    def generate(react_def: ReactAppDefinition, output_dir: str) -> List[str]:
        pages = QueryPageTransformer.transform(react_def.page_definitions)
        files = []

        for page in pages:
            ctx = page.model_dump()
            ctx["entityNameCamel"] = to_camel_case(page.entityName)
            content = Template(QUERY_PAGE).render(**ctx)
            path = os.path.join(
                output_dir, "src", "pages", "queries",
                f"{page.entityNamePascal}QueryPage.jsx",
            )
            FileWriter.write_file(path, content)
            files.append(path)

        return files
