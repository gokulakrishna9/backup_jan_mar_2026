import React from 'react';
import BaseChart from './BaseChart';

const defaultOption = "{\n  \"tooltip\": {},\n  \"series\": [\n    {\n      \"type\": \"sunburst\"\n    }\n  ]\n}";

const SunburstChart = ({ data, option, theme, ...rest }) => {
  const mergedOption = { ...defaultOption, ...option };
  return <BaseChart option={mergedOption} data={data} theme={theme} {...rest} />;
};

export default SunburstChart;