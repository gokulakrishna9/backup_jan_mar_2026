"""Theme generator — produces theme.json."""

import os

from transformers.phase1.theme_transformer import ThemeTransformer
from utils.file_writer import FileWriter


class ThemeGenerator:
    @staticmethod
    def generate(output_dir: str) -> str:
        theme = ThemeTransformer.transform()
        path = os.path.join(output_dir, "react_theme.json")
        FileWriter.write_json(path, theme.model_dump())
        return path
