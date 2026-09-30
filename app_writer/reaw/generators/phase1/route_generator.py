"""Route generator — produces routes.json."""

import os

from models.definition_models import AppDefinition
from models.react_definition_models import RouteDefinition
from transformers.phase1.route_transformer import RouteTransformer
from utils.file_writer import FileWriter


class RouteGenerator:
    @staticmethod
    def generate(app_def: AppDefinition, output_dir: str) -> str:
        routes = RouteTransformer.transform(
            app_def.controller_layer,
            app_def.filter_layer,
            app_def.query_layer,
        )
        path = os.path.join(output_dir, "react_routes.json")
        FileWriter.write_json(path, [r.model_dump() for r in routes])
        return path
