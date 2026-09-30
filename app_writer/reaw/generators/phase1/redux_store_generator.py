"""Redux store generator — produces redux_store.json."""

import os
from typing import List, Optional

from models.definition_models import EntityLayerDef
from models.react_definition_models import ApiServiceDefinition
from transformers.phase1.redux_store_transformer import ReduxStoreTransformer
from utils.file_writer import FileWriter


class ReduxStoreGenerator:
    @staticmethod
    def generate(
        api_services: List[ApiServiceDefinition],
        entity_layer: Optional[EntityLayerDef],
        output_dir: str,
    ) -> str:
        store_defs = ReduxStoreTransformer.transform(api_services, entity_layer)
        path = os.path.join(output_dir, "react_redux_store.json")
        FileWriter.write_json(path, [s.model_dump() for s in store_defs])
        return path
