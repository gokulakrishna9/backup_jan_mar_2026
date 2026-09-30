import React from 'react';
import BaseChart from './BaseChart';

const defaultOption = "{\n  \"tooltip\": {\n    \"trigger\": \"axis\"\n  },\n  \"xAxis\": {\n    \"type\": \"category\"\n  },\n  \"yAxis\": {\n    \"type\": \"value\"\n  },\n  \"series\": [\n    {\n      \"type\": \"bar\"\n    }\n  ]\n}";

const BarChart = ({ data, option, theme, ...rest }) => {
  const mergedOption = { ...defaultOption, ...option };
  return <BaseChart option={mergedOption} data={data} theme={theme} {...rest} />;
};

export default BarChart;