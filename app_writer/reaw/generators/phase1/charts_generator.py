"""Charts generator — produces charts.json."""

import os

from transformers.phase1.charts_transformer import ChartsTransformer
from utils.file_writer import FileWriter


class ChartsGenerator:
    @staticmethod
    def generate(output_dir: str) -> str:
        charts = ChartsTransformer.transform()
        path = os.path.join(output_dir, "react_charts.json")
        FileWriter.write_json(path, charts.model_dump())
        return path
