"""Theme generator — produces theme-variables.css and primereact-theme-overrides.css."""

import os
from typing import List

from jinja2 import Template

from models.react_definition_models import ReactAppDefinition
from transformers.phase2.theme_transformer import Phase2ThemeTransformer
from templates.theme_templates import THEME_VARIABLES, PRIMEREACT_OVERRIDES
from utils.file_writer import FileWriter


class Phase2ThemeGenerator:
    @staticmethod
    def generate(react_def: ReactAppDefinition, output_dir: str) -> List[str]:
        props = Phase2ThemeTransformer.transform(react_def.theme)
        ctx = props.model_dump()
        files = []

        for template_str, filename in [
            (THEME_VARIABLES, "theme-variables.css"),
            (PRIMEREACT_OVERRIDES, "primereact-theme-overrides.css"),
        ]:
            content = Template(template_str).render(**ctx)
            path = os.path.join(output_dir, "src", "styles", filename)
            FileWriter.write_file(path, content)
            files.append(path)

        return files
