"""Grid layout generator — produces AppLayout.jsx and AppLayout.css."""

import os
from typing import List

from jinja2 import Template

from models.react_definition_models import ReactAppDefinition
from transformers.phase2.grid_layout_transformer import GridLayoutTransformer
from templates.grid_layout_templates import APP_LAYOUT_JSX, APP_LAYOUT_CSS
from utils.file_writer import FileWriter


class GridLayoutGenerator:
    @staticmethod
    def generate(react_def: ReactAppDefinition, output_dir: str) -> List[str]:
        props = GridLayoutTransformer.transform(react_def.layout)
        ctx = props.model_dump()
        files = []

        for template_str, filename in [
            (APP_LAYOUT_JSX, "AppLayout.jsx"),
            (APP_LAYOUT_CSS, "AppLayout.css"),
        ]:
            content = Template(template_str).render(**ctx)
            path = os.path.join(output_dir, "src", "layout", filename)
            FileWriter.write_file(path, content)
            files.append(path)

        return files
