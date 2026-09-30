"""Scaffold generator — produces package.json, vite.config.js, .env, index.html, main.jsx, App.jsx."""

import os
from typing import List

from jinja2 import Template

from models.react_definition_models import ReactAppDefinition
from transformers.phase2.scaffold_transformer import ScaffoldTransformer
from templates.scaffold_templates import PACKAGE_JSON, VITE_CONFIG, ENV_FILE, INDEX_HTML, MAIN_JSX, APP_JSX, LOGGER_UTIL, DASHBOARD_PAGE
from utils.file_writer import FileWriter


class ScaffoldGenerator:
    @staticmethod
    def generate(react_def: ReactAppDefinition, output_dir: str) -> List[str]:
        scaffold_props, env_props = ScaffoldTransformer.transform(react_def)
        scaffold_ctx = scaffold_props.model_dump()
        env_ctx = env_props.model_dump()
        files = []

        for template_str, rel_path, ctx in [
            (PACKAGE_JSON, "package.json", scaffold_ctx),
            (VITE_CONFIG, "vite.config.js", scaffold_ctx),
            (ENV_FILE, ".env", env_ctx),
            (INDEX_HTML, "index.html", scaffold_ctx),
            (MAIN_JSX, "src/main.jsx", scaffold_ctx),
            (APP_JSX, "src/App.jsx", scaffold_ctx),
            (LOGGER_UTIL, "src/utils/logger.js", {}),
        ]:
            content = Template(template_str).render(**ctx)
            path = os.path.join(output_dir, rel_path)
            FileWriter.write_file(path, content)
            files.append(path)

        # Generate DashboardPage if a dashboard route exists
        for route in react_def.routes:
            if route.pageComponent == "DashboardPage" and route.pageFolder:
                content = Template(DASHBOARD_PAGE).render(**scaffold_ctx)
                path = os.path.join(
                    output_dir, "src", "pages", route.pageFolder, "DashboardPage.jsx"
                )
                FileWriter.write_file(path, content)
                files.append(path)
                break

        return files
