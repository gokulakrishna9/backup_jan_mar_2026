"""Charts transformer — generates default chart types and mapping rules."""

from models.react_definition_models import ChartMappingRule, ChartsDefinition, ChartTypeDef


# All 19 2D chart types with default ECharts option templates
_DEFAULT_CHART_TYPES = [
    ChartTypeDef(typeId="bar", enabled=True, defaultOption={
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category"},
        "yAxis": {"type": "value"},
        "series": [{"type": "bar"}],
    }),
    ChartTypeDef(typeId="line", enabled=True, defaultOption={
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category"},
        "yAxis": {"type": "value"},
        "series": [{"type": "line", "smooth": True}],
    }),
    ChartTypeDef(typeId="area", enabled=True, defaultOption={
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category"},
        "yAxis": {"type": "value"},
        "series": [{"type": "line", "areaStyle": {}, "smooth": True}],
    }),
    ChartTypeDef(typeId="pie", enabled=True, defaultOption={
        "tooltip": {"trigger": "item"},
        "series": [{"type": "pie", "radius": "60%"}],
    }),
    ChartTypeDef(typeId="donut", enabled=True, defaultOption={
        "tooltip": {"trigger": "item"},
        "series": [{"type": "pie", "radius": ["40%", "70%"]}],
    }),
    ChartTypeDef(typeId="scatter", enabled=True, defaultOption={
        "tooltip": {"trigger": "item"},
        "xAxis": {"type": "value"},
        "yAxis": {"type": "value"},
        "series": [{"type": "scatter"}],
    }),
    ChartTypeDef(typeId="bubble", enabled=True, defaultOption={
        "tooltip": {"trigger": "item"},
        "xAxis": {"type": "value"},
        "yAxis": {"type": "value"},
        "series": [{"type": "scatter", "symbolSize": "function(val){return val[2]*2;}"}],
    }),
    ChartTypeDef(typeId="radar", enabled=True, defaultOption={
        "tooltip": {},
        "radar": {"indicator": []},
        "series": [{"type": "radar"}],
    }),
    ChartTypeDef(typeId="heatmap", enabled=True, defaultOption={
        "tooltip": {"position": "top"},
        "xAxis": {"type": "category"},
        "yAxis": {"type": "category"},
        "visualMap": {"min": 0, "max": 100},
        "series": [{"type": "heatmap"}],
    }),
    ChartTypeDef(typeId="treemap", enabled=True, defaultOption={
        "tooltip": {},
        "series": [{"type": "treemap"}],
    }),
    ChartTypeDef(typeId="funnel", enabled=True, defaultOption={
        "tooltip": {"trigger": "item"},
        "series": [{"type": "funnel", "left": "10%", "width": "80%"}],
    }),
    ChartTypeDef(typeId="gauge", enabled=True, defaultOption={
        "tooltip": {},
        "series": [{"type": "gauge"}],
    }),
    ChartTypeDef(typeId="candlestick", enabled=True, defaultOption={
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category"},
        "yAxis": {"type": "value"},
        "series": [{"type": "candlestick"}],
    }),
    ChartTypeDef(typeId="boxplot", enabled=True, defaultOption={
        "tooltip": {"trigger": "item"},
        "xAxis": {"type": "category"},
        "yAxis": {"type": "value"},
        "series": [{"type": "boxplot"}],
    }),
    ChartTypeDef(typeId="sankey", enabled=True, defaultOption={
        "tooltip": {},
        "series": [{"type": "sankey", "layout": "none"}],
    }),
    ChartTypeDef(typeId="sunburst", enabled=True, defaultOption={
        "tooltip": {},
        "series": [{"type": "sunburst"}],
    }),
    ChartTypeDef(typeId="histogram", enabled=True, defaultOption={
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category"},
        "yAxis": {"type": "value"},
        "series": [{"type": "bar", "barWidth": "99%"}],
    }),
    ChartTypeDef(typeId="parallel", enabled=True, defaultOption={
        "parallelAxis": [],
        "series": [{"type": "parallel"}],
    }),
    ChartTypeDef(typeId="pictorialBar", enabled=True, defaultOption={
        "tooltip": {"trigger": "axis"},
        "xAxis": {"type": "category"},
        "yAxis": {"type": "value"},
        "series": [{"type": "pictorialBar"}],
    }),
]

# Default data-to-chart mapping rules
_DEFAULT_MAPPING_RULES = [
    ChartMappingRule(
        ruleId="ohlc_candlestick", chartType="candlestick", priority=5,
        conditions={"hasColumns": ["open", "high", "low", "close"]},
    ),
    ChartMappingRule(
        ruleId="time_series_line", chartType="line", priority=10,
        conditions={"hasDateColumn": True, "numericColumnCount": {"min": 1}},
    ),
    ChartMappingRule(
        ruleId="time_series_area", chartType="area", priority=12,
        conditions={"hasDateColumn": True, "numericColumnCount": {"min": 2}},
    ),
    ChartMappingRule(
        ruleId="categorical_bar", chartType="bar", priority=20,
        conditions={"categoricalColumnCount": 1, "numericColumnCount": 1, "hasDateColumn": False},
    ),
    ChartMappingRule(
        ruleId="categorical_pie", chartType="pie", priority=25,
        conditions={"categoricalColumnCount": 1, "numericColumnCount": 1, "rowCount": {"max": 20}},
    ),
    ChartMappingRule(
        ruleId="two_numeric_scatter", chartType="scatter", priority=30,
        conditions={"numericColumnCount": 2, "hasDateColumn": False},
    ),
    ChartMappingRule(
        ruleId="three_numeric_bubble", chartType="bubble", priority=32,
        conditions={"numericColumnCount": {"min": 3}, "hasDateColumn": False},
    ),
    ChartMappingRule(
        ruleId="hierarchical_treemap", chartType="treemap", priority=35,
        conditions={"hasHierarchicalData": True},
    ),
    ChartMappingRule(
        ruleId="hierarchical_sunburst", chartType="sunburst", priority=36,
        conditions={"hasHierarchicalData": True, "depthLevels": {"min": 3}},
    ),
    ChartMappingRule(
        ruleId="flow_sankey", chartType="sankey", priority=38,
        conditions={"hasColumns": ["source", "target", "value"]},
    ),
    ChartMappingRule(
        ruleId="statistical_boxplot", chartType="boxplot", priority=40,
        conditions={"hasStatisticalData": True},
    ),
    ChartMappingRule(
        ruleId="distribution_histogram", chartType="histogram", priority=42,
        conditions={"numericColumnCount": 1, "categoricalColumnCount": 0, "rowCount": {"min": 20}},
    ),
    ChartMappingRule(
        ruleId="multi_dimension_radar", chartType="radar", priority=45,
        conditions={"numericColumnCount": {"min": 3}, "categoricalColumnCount": 1},
    ),
    ChartMappingRule(
        ruleId="multi_dimension_parallel", chartType="parallel", priority=48,
        conditions={"numericColumnCount": {"min": 4}},
    ),
    ChartMappingRule(
        ruleId="single_value_gauge", chartType="gauge", priority=50,
        conditions={"numericColumnCount": 1, "rowCount": {"max": 1}},
    ),
    ChartMappingRule(
        ruleId="funnel_stages", chartType="funnel", priority=52,
        conditions={"categoricalColumnCount": 1, "numericColumnCount": 1, "isOrdered": True},
    ),
]


class ChartsTransformer:
    """Generates default charts configuration."""

    @staticmethod
    def transform() -> ChartsDefinition:
        """Produce default ChartsDefinition with all 19 chart types and mapping rules.

        Returns:
            ChartsDefinition with all chart types enabled and default mapping rules.
        """
        return ChartsDefinition(
            chartTypes=list(_DEFAULT_CHART_TYPES),
            mappingRules=list(_DEFAULT_MAPPING_RULES),
        )
