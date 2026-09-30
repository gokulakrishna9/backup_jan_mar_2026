"""Redux generator — produces store.js, index.js, and per-entity slice files."""

import os
from typing import List

from jinja2 import Environment

from models.react_definition_models import ReactAppDefinition
from transformers.phase2.redux_slice_transformer import ReduxSliceTransformer
from templates.redux_templates import STORE_JS, STORE_INDEX, ENTITY_SLICE
from utils.file_writer import FileWriter
from utils.string_utils import to_camel_case


class ReduxGenerator:
    @staticmethod
    def generate(react_def: ReactAppDefinition, output_dir: str) -> List[str]:
        store_props, slice_list = ReduxSliceTransformer.transform(react_def.redux_store)
        files = []

        env = Environment()
        env.filters["camelCase"] = to_camel_case

        # store.js
        content = env.from_string(STORE_JS).render(entities=store_props.entities)
        path = os.path.join(output_dir, "src", "store", "store.js")
        FileWriter.write_file(path, content)
        files.append(path)

        # index.js
        content = env.from_string(STORE_INDEX).render()
        path = os.path.join(output_dir, "src", "store", "index.js")
        FileWriter.write_file(path, content)
        files.append(path)

        # Per-entity slice files
        for sl in slice_list:
            content = env.from_string(ENTITY_SLICE).render(**sl.model_dump())
            path = os.path.join(output_dir, "src", "store", "slices", f"{to_camel_case(sl.entityName)}Slice.js")
            FileWriter.write_file(path, content)
            files.append(path)

        return files
