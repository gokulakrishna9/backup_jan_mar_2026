"""Chart generator — produces BaseChart, per-type wrappers, chartRegistry, chartMappingEngine."""

import json
import os
from typing import List

from jinja2 import Template

from models.react_definition_models import ReactAppDefinition
from transformers.phase2.chart_transformer import ChartTransformer
from templates.chart_templates import BASE_CHART, CHART_TYPE_WRAPPER, CHART_REGISTRY, CHART_MAPPING_ENGINE
from utils.file_writer import FileWriter


class ChartGenerator:
    @staticmethod
    def generate(react_def: ReactAppDefinition, output_dir: str) -> List[str]:
        chart_components, registry, mapping_engine = ChartTransformer.transform(react_def.charts)
        files = []
        charts_dir = os.path.join(output_dir, "src", "components", "charts")

        # BaseChart.jsx
        path = os.path.join(charts_dir, "BaseChart.jsx")
        FileWriter.write_file(path, BASE_CHART)
        files.append(path)

        # Per-type chart wrappers
        for cc in chart_components:
            ctx = cc.model_dump()
            ctx["defaultOption"] = json.dumps(ctx["defaultOption"], indent=2)
            content = Template(CHART_TYPE_WRAPPER).render(**ctx)
            path = os.path.join(charts_dir, f"{cc.componentName}.jsx")
            FileWriter.write_file(path, content)
            files.append(path)

        # chartRegistry.js
        content = Template(CHART_REGISTRY).render(chartTypes=chart_components)
        path = os.path.join(charts_dir, "chartRegistry.js")
        FileWriter.write_file(path, content)
        files.append(path)

        # chartMappingEngine.js
        rules_json = json.dumps([r.model_dump() for r in mapping_engine.mappingRules], indent=2)
        content = Template(CHART_MAPPING_ENGINE).render(mappingRules=rules_json)
        path = os.path.join(output_dir, "src", "utils", "chartMappingEngine.js")
        FileWriter.write_file(path, content)
        files.append(path)

        return files
