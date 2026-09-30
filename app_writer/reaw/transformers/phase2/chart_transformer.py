"""Chart transformer — produces chart component, registry, and mapping engine properties."""

from typing import List, Tuple

from models.property_objects import (
    ChartComponentProperties,
    ChartMappingEngineProperties,
    ChartRegistryProperties,
)
from models.react_definition_models import ChartsDefinition
from utils.string_utils import to_pascal_case


class ChartTransformer:
    """Transforms charts definition into chart-related template properties."""

    @staticmethod
    def transform(
        charts: ChartsDefinition,
    ) -> Tuple[List[ChartComponentProperties], ChartRegistryProperties, ChartMappingEngineProperties]:
        """Produce chart component, registry, and mapping engine properties.

        Args:
            charts: Charts definition from charts.json.

        Returns:
            Tuple of (list of ChartComponentProperties, ChartRegistryProperties,
            ChartMappingEngineProperties).
        """
        # Only include enabled chart types
        chart_components: List[ChartComponentProperties] = []
        for ct in charts.chartTypes:
            if not ct.enabled:
                continue
            component_name = to_pascal_case(ct.typeId) + "Chart"
            chart_components.append(ChartComponentProperties(
                typeId=ct.typeId,
                componentName=component_name,
                defaultOption=ct.defaultOption,
            ))

        registry = ChartRegistryProperties(chartTypes=chart_components)
        mapping_engine = ChartMappingEngineProperties(mappingRules=charts.mappingRules)

        return chart_components, registry, mapping_engine
