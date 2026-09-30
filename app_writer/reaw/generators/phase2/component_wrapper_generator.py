"""Component wrapper generator — produces 10 PrimeReact wrapper files."""

import os
from typing import List

from jinja2 import Template

from transformers.phase2.component_wrapper_transformer import ComponentWrapperTransformer
from templates.component_wrapper_templates import COMPONENT_WRAPPER
from utils.file_writer import FileWriter


class ComponentWrapperGenerator:
    @staticmethod
    def generate(output_dir: str) -> List[str]:
        wrappers = ComponentWrapperTransformer.transform()
        files = []

        for w in wrappers:
            content = Template(COMPONENT_WRAPPER).render(**w.model_dump())
            path = os.path.join(output_dir, "src", "components", "wrappers", f"{w.componentName}.jsx")
            FileWriter.write_file(path, content)
            files.append(path)

        return files
