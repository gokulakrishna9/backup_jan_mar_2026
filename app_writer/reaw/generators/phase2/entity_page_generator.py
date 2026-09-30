"""Entity page generator — produces per-entity Page.jsx."""

import os
from typing import Dict, List

from jinja2 import Template

from models.react_definition_models import ReactAppDefinition
from transformers.phase2.entity_page_transformer import EntityPageTransformer
from templates.entity_page_templates import ENTITY_PAGE
from utils.file_writer import FileWriter
from utils.string_utils import to_camel_case


class EntityPageGenerator:
    @staticmethod
    def generate(react_def: ReactAppDefinition, output_dir: str) -> List[str]:
        pages = EntityPageTransformer.transform(
            react_def.page_definitions, react_def.form_groupings
        )

        # Build route lookup: pageComponent → pageFolder
        folder_map: Dict[str, str] = {}
        for route in react_def.routes:
            if route.pageFolder:
                folder_map[route.pageComponent] = route.pageFolder

        files = []

        for page in pages:
            if page.pageType != "entity":
                continue
            content = Template(ENTITY_PAGE).render(**page.model_dump())
            page_component = f"{page.entityNamePascal}Page"
            folder = folder_map.get(page_component, "entitys")
            path = os.path.join(
                output_dir, "src", "pages", folder,
                f"{page_component}.jsx",
            )
            FileWriter.write_file(path, content)
            files.append(path)

        return files
