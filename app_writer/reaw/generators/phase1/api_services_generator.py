"""API services generator — produces api_services.json."""

import os
from typing import List

from models.definition_models import AppDefinition
from models.react_definition_models import ApiServiceDefinition
from transformers.phase1.api_services_transformer import ApiServicesTransformer
from utils.file_writer import FileWriter


class ApiServicesGenerator:
    @staticmethod
    def generate(app_def: AppDefinition, output_dir: str) -> tuple:
        """Generate api_services.json and return (path, api_services list).

        Returns:
            Tuple of (file_path, list of ApiServiceDefinition) so redux_store
            generator can use the api_services as input.
        """
        api_services = ApiServicesTransformer.transform(app_def.controller_layer)
        path = os.path.join(output_dir, "react_api_services.json")
        FileWriter.write_json(path, [s.model_dump() for s in api_services])
        return path, api_services
