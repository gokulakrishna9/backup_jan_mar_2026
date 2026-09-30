"""React code generator — orchestrates all Phase 2 generators.

Produces the complete React application source code from a parsed
ReactAppDefinition.
"""

from pathlib import Path
from typing import Any, Dict, List

from models.react_definition_models import ReactAppDefinition
from generators.phase2.theme_generator import Phase2ThemeGenerator
from generators.phase2.scaffold_generator import ScaffoldGenerator
from generators.phase2.api_service_generator import ApiServiceGenerator
from generators.phase2.redux_generator import ReduxGenerator
from generators.phase2.component_wrapper_generator import ComponentWrapperGenerator
from generators.phase2.auth_generator import AuthGenerator
from generators.phase2.permission_generator import PermissionGenerator
from generators.phase2.chart_generator import ChartGenerator
from generators.phase2.widget_generator import WidgetGenerator
from generators.phase2.entity_component_generator import EntityComponentGenerator
from generators.phase2.filter_component_generator import FilterComponentGenerator
from generators.phase2.query_component_generator import QueryComponentGenerator
from generators.phase2.grouped_form_generator import GroupedFormGenerator
from generators.phase2.entity_page_generator import EntityPageGenerator
from generators.phase2.filter_page_generator import FilterPageGenerator
from generators.phase2.query_page_generator import QueryPageGenerator
from generators.phase2.grid_layout_generator import GridLayoutGenerator
from generators.ai_react_generator import AiReactGenerator


class ReactCodeGenerator:
    """Orchestrates all Phase 2 generators in dependency order."""

    @staticmethod
    def generate(
        react_def: ReactAppDefinition,
        output_dir: str,
        filter_entities: Dict[str, List[Dict]] = None,
        query_entities: Dict[str, List[Dict]] = None,
        ai_layer: Dict[str, Any] | None = None,
    ) -> List[str]:
        """Run all Phase 2 generators and produce the React application.

        Args:
            react_def: Parsed React Application Definition.
            output_dir: Target output directory for the React app.
            filter_entities: Optional dict of entity → filter field dicts.
            query_entities: Optional dict of entity → query dicts.
            ai_layer: Optional parsed webflux_ai_layer.json dict for AI generation.

        Returns:
            List of all generated file paths.
        """
        if filter_entities is None:
            filter_entities = {}
        if query_entities is None:
            query_entities = {}

        files: List[str] = []

        # 1. Theme (no dependencies)
        files.extend(Phase2ThemeGenerator.generate(react_def, output_dir))

        # 2. Scaffold (routes, app name)
        files.extend(ScaffoldGenerator.generate(react_def, output_dir))

        # 3. API services
        files.extend(ApiServiceGenerator.generate(react_def, output_dir))

        # 4. Redux store + slices
        files.extend(ReduxGenerator.generate(react_def, output_dir))

        # 5. Component wrappers
        files.extend(ComponentWrapperGenerator.generate(output_dir))

        # 6. Auth
        files.extend(AuthGenerator.generate(react_def, output_dir))

        # 7. Permissions
        files.extend(PermissionGenerator.generate(react_def, output_dir))

        # 8. Charts
        files.extend(ChartGenerator.generate(react_def, output_dir))

        # 8.5. Widget components (before entity components that import them)
        files.extend(WidgetGenerator.generate(react_def, output_dir))

        # 9. Entity components (forms + DataTables)
        files.extend(EntityComponentGenerator.generate(react_def, output_dir))

        # 10. Filter components
        files.extend(FilterComponentGenerator.generate(react_def, output_dir, filter_entities))

        # 11. Query components
        files.extend(QueryComponentGenerator.generate(react_def, output_dir, query_entities))

        # 12. Grouped forms
        files.extend(GroupedFormGenerator.generate(react_def, output_dir))

        # 13. Entity pages
        files.extend(EntityPageGenerator.generate(react_def, output_dir))

        # 14. Filter pages
        files.extend(FilterPageGenerator.generate(react_def, output_dir))

        # 15. Query pages
        files.extend(QueryPageGenerator.generate(react_def, output_dir))

        # 16. Grid layout (last — wraps everything)
        files.extend(GridLayoutGenerator.generate(react_def, output_dir))

        # 17. AI React components (when react_ai_config is present)
        if react_def.react_ai_config is not None and ai_layer is not None:
            react_defs = {
                m.entityName: m for m in react_def.component_mappings
            }
            gen = AiReactGenerator()
            ai_files = gen.generate(
                react_ai_config=react_def.react_ai_config,
                ai_layer=ai_layer,
                react_definitions=react_defs,
                output_dir=Path(output_dir),
            )
            files.extend([str(p) for p in ai_files])

        return files
