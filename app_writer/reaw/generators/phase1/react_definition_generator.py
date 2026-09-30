"""React definition generator — orchestrates all Phase 1 generators.

Produces the react_*.json definition files from a parsed swfaw AppDefinition.
Files are written directly into the output directory (application_definitions/).
"""

from typing import List

from models.definition_models import AppDefinition
from generators.phase1.route_generator import RouteGenerator
from generators.phase1.form_grouping_generator import FormGroupingGenerator
from generators.phase1.component_mapping_generator import ComponentMappingGenerator
from generators.phase1.page_definition_generator import PageDefinitionGenerator
from generators.phase1.layout_generator import LayoutGenerator
from generators.phase1.auth_config_generator import AuthConfigGenerator
from generators.phase1.api_services_generator import ApiServicesGenerator
from generators.phase1.redux_store_generator import ReduxStoreGenerator
from generators.phase1.theme_generator import ThemeGenerator
from generators.phase1.charts_generator import ChartsGenerator
from generators.phase1.env_generator import EnvGenerator
from generators.phase1.manifest_generator import ManifestGenerator
from transformers.phase1.form_grouping_transformer import FormGroupingTransformer


class ReactDefinitionGenerator:
    """Orchestrates all Phase 1 generators in dependency order."""

    @staticmethod
    def generate(app_def: AppDefinition, output_dir: str) -> List[str]:
        """Run all Phase 1 generators and produce react_manifest.json.

        Args:
            app_def: Parsed swfaw application definition.
            output_dir: Output directory where react_*.json files will be written.

        Returns:
            List of all generated file paths.
        """
        files: List[str] = []

        # Independent generators
        files.append(RouteGenerator.generate(app_def, output_dir))

        # Form groupings (needed by page definitions)
        files.append(FormGroupingGenerator.generate(app_def, output_dir))
        form_groupings = FormGroupingTransformer.transform(
            app_def.relationships, app_def.entity_layer
        )

        files.append(ComponentMappingGenerator.generate(app_def, output_dir))

        # Page definitions depend on form groupings
        files.append(PageDefinitionGenerator.generate(app_def, output_dir, form_groupings))

        files.append(LayoutGenerator.generate(app_def, output_dir))
        files.append(AuthConfigGenerator.generate(app_def, output_dir))

        # API services must come before redux store (dependency chain)
        api_path, api_services = ApiServicesGenerator.generate(app_def, output_dir)
        files.append(api_path)
        files.append(ReduxStoreGenerator.generate(api_services, app_def.entity_layer, output_dir))

        files.append(ThemeGenerator.generate(output_dir))
        files.append(ChartsGenerator.generate(output_dir))
        files.append(EnvGenerator.generate(app_def, output_dir))

        # Manifest last — indexes all generated files
        files.append(ManifestGenerator.generate(files, output_dir))

        return files
