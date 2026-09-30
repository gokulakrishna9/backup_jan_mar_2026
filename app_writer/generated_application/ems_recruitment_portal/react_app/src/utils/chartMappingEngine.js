const mappingRules = "[\n  {\n    \"ruleId\": \"ohlc_candlestick\",\n    \"chartType\": \"candlestick\",\n    \"conditions\": {\n      \"hasColumns\": [\n        \"open\",\n        \"high\",\n        \"low\",\n        \"close\"\n      ]\n    },\n    \"priority\": 5\n  },\n  {\n    \"ruleId\": \"time_series_line\",\n    \"chartType\": \"line\",\n    \"conditions\": {\n      \"hasDateColumn\": true,\n      \"numericColumnCount\": {\n        \"min\": 1\n      }\n    },\n    \"priority\": 10\n  },\n  {\n    \"ruleId\": \"time_series_area\",\n    \"chartType\": \"area\",\n    \"conditions\": {\n      \"hasDateColumn\": true,\n      \"numericColumnCount\": {\n        \"min\": 2\n      }\n    },\n    \"priority\": 12\n  },\n  {\n    \"ruleId\": \"categorical_bar\",\n    \"chartType\": \"bar\",\n    \"conditions\": {\n      \"categoricalColumnCount\": 1,\n      \"numericColumnCount\": 1,\n      \"hasDateColumn\": false\n    },\n    \"priority\": 20\n  },\n  {\n    \"ruleId\": \"categorical_pie\",\n    \"chartType\": \"pie\",\n    \"conditions\": {\n      \"categoricalColumnCount\": 1,\n      \"numericColumnCount\": 1,\n      \"rowCount\": {\n        \"max\": 20\n      }\n    },\n    \"priority\": 25\n  },\n  {\n    \"ruleId\": \"two_numeric_scatter\",\n    \"chartType\": \"scatter\",\n    \"conditions\": {\n      \"numericColumnCount\": 2,\n      \"hasDateColumn\": false\n    },\n    \"priority\": 30\n  },\n  {\n    \"ruleId\": \"three_numeric_bubble\",\n    \"chartType\": \"bubble\",\n    \"conditions\": {\n      \"numericColumnCount\": {\n        \"min\": 3\n      },\n      \"hasDateColumn\": false\n    },\n    \"priority\": 32\n  },\n  {\n    \"ruleId\": \"hierarchical_treemap\",\n    \"chartType\": \"treemap\",\n    \"conditions\": {\n      \"hasHierarchicalData\": true\n    },\n    \"priority\": 35\n  },\n  {\n    \"ruleId\": \"hierarchical_sunburst\",\n    \"chartType\": \"sunburst\",\n    \"conditions\": {\n      \"hasHierarchicalData\": true,\n      \"depthLevels\": {\n        \"min\": 3\n      }\n    },\n    \"priority\": 36\n  },\n  {\n    \"ruleId\": \"flow_sankey\",\n    \"chartType\": \"sankey\",\n    \"conditions\": {\n      \"hasColumns\": [\n        \"source\",\n        \"target\",\n        \"value\"\n      ]\n    },\n    \"priority\": 38\n  },\n  {\n    \"ruleId\": \"statistical_boxplot\",\n    \"chartType\": \"boxplot\",\n    \"conditions\": {\n      \"hasStatisticalData\": true\n    },\n    \"priority\": 40\n  },\n  {\n    \"ruleId\": \"distribution_histogram\",\n    \"chartType\": \"histogram\",\n    \"conditions\": {\n      \"numericColumnCount\": 1,\n      \"categoricalColumnCount\": 0,\n      \"rowCount\": {\n        \"min\": 20\n      }\n    },\n    \"priority\": 42\n  },\n  {\n    \"ruleId\": \"multi_dimension_radar\",\n    \"chartType\": \"radar\",\n    \"conditions\": {\n      \"numericColumnCount\": {\n        \"min\": 3\n      },\n      \"categoricalColumnCount\": 1\n    },\n    \"priority\": 45\n  },\n  {\n    \"ruleId\": \"multi_dimension_parallel\",\n    \"chartType\": \"parallel\",\n    \"conditions\": {\n      \"numericColumnCount\": {\n        \"min\": 4\n      }\n    },\n    \"priority\": 48\n  },\n  {\n    \"ruleId\": \"single_value_gauge\",\n    \"chartType\": \"gauge\",\n    \"conditions\": {\n      \"numericColumnCount\": 1,\n      \"rowCount\": {\n        \"max\": 1\n      }\n    },\n    \"priority\": 50\n  },\n  {\n    \"ruleId\": \"funnel_stages\",\n    \"chartType\": \"funnel\",\n    \"conditions\": {\n      \"categoricalColumnCount\": 1,\n      \"numericColumnCount\": 1,\n      \"isOrdered\": true\n    },\n    \"priority\": 52\n  }\n]";

/**
 * Analyze columns and data to extract metadata for chart type suggestion.
 */
export const analyzeColumns = (columns, data) => {
  const hasDateColumn = columns.some(
    (col) => col.type === 'date' || col.type === 'datetime' || /date|time/i.test(col.name)
  );
  const numericColumns = columns.filter(
    (col) => col.type === 'number' || col.type === 'decimal' || col.type === 'integer'
  );
  const categoricalColumns = columns.filter(
    (col) => col.type === 'string' || col.type === 'enum'
  );

  return {
    hasDateColumn,
    numericColumnCount: numericColumns.length,
    categoricalColumnCount: categoricalColumns.length,
    rowCount: data ? data.length : 0,
    hasColumns: columns.length > 0,
    columns,
  };
};

/**
 * Suggest chart types based on column metadata and mapping rules.
 */
export const suggestChartType = (columns, data) => {
  const metadata = analyzeColumns(columns, data);
  const suggestions = [];

  for (const rule of mappingRules) {
    let matches = true;
    for (const [key, value] of Object.entries(rule.conditions)) {
      if (typeof value === 'boolean') {
        if (metadata[key] !== value) { matches = false; break; }
      } else if (typeof value === 'number') {
        if ((metadata[key] || 0) < value) { matches = false; break; }
      } else if (typeof value === 'string') {
        if (metadata[key] !== value) { matches = false; break; }
      }
    }
    if (matches) {
      suggestions.push({ chartType: rule.chartType, priority: rule.priority, ruleId: rule.ruleId });
    }
  }

  suggestions.sort((a, b) => b.priority - a.priority);
  return suggestions.length > 0 ? suggestions : [{ chartType: 'bar', priority: 0, ruleId: 'default' }];
};

/**
 * Build a complete ECharts option for a given chart type and data.
 */
export const buildChartOption = (chartType, columns, data) => {
  const numericCols = columns.filter(
    (col) => col.type === 'number' || col.type === 'decimal' || col.type === 'integer'
  );
  const categoryCols = columns.filter(
    (col) => col.type === 'string' || col.type === 'enum'
  );
  const categoryCol = categoryCols[0];
  const valueCol = numericCols[0];

  const categories = categoryCol ? data.map((row) => row[categoryCol.name]) : [];
  const values = valueCol ? data.map((row) => row[valueCol.name]) : [];

  const baseOption = {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: categories },
    yAxis: { type: 'value' },
    series: [{ type: chartType, data: values }],
  };

  return baseOption;
};