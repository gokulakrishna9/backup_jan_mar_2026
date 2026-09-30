import React from 'react';
import BaseChart from './BaseChart';

const defaultOption = "{\n  \"tooltip\": {},\n  \"series\": [\n    {\n      \"type\": \"gauge\"\n    }\n  ]\n}";

const GaugeChart = ({ data, option, theme, ...rest }) => {
  const mergedOption = { ...defaultOption, ...option };
  return <BaseChart option={mergedOption} data={data} theme={theme} {...rest} />;
};

export default GaugeChart;