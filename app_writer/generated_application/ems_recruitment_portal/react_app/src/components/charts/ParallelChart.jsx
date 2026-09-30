import React from 'react';
import BaseChart from './BaseChart';

const defaultOption = "{\n  \"parallelAxis\": [],\n  \"series\": [\n    {\n      \"type\": \"parallel\"\n    }\n  ]\n}";

const ParallelChart = ({ data, option, theme, ...rest }) => {
  const mergedOption = { ...defaultOption, ...option };
  return <BaseChart option={mergedOption} data={data} theme={theme} {...rest} />;
};

export default ParallelChart;