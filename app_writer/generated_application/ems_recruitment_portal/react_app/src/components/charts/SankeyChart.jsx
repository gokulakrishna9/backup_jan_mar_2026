import React from 'react';
import BaseChart from './BaseChart';

const defaultOption = "{\n  \"tooltip\": {},\n  \"series\": [\n    {\n      \"type\": \"sankey\",\n      \"layout\": \"none\"\n    }\n  ]\n}";

const SankeyChart = ({ data, option, theme, ...rest }) => {
  const mergedOption = { ...defaultOption, ...option };
  return <BaseChart option={mergedOption} data={data} theme={theme} {...rest} />;
};

export default SankeyChart;