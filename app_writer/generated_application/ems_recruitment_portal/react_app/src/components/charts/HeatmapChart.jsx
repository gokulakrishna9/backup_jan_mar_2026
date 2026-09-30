import React from 'react';
import BaseChart from './BaseChart';

const defaultOption = "{\n  \"tooltip\": {\n    \"position\": \"top\"\n  },\n  \"xAxis\": {\n    \"type\": \"category\"\n  },\n  \"yAxis\": {\n    \"type\": \"category\"\n  },\n  \"visualMap\": {\n    \"min\": 0,\n    \"max\": 100\n  },\n  \"series\": [\n    {\n      \"type\": \"heatmap\"\n    }\n  ]\n}";

const HeatmapChart = ({ data, option, theme, ...rest }) => {
  const mergedOption = { ...defaultOption, ...option };
  return <BaseChart option={mergedOption} data={data} theme={theme} {...rest} />;
};

export default HeatmapChart;