const mappingRules = "[]";

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