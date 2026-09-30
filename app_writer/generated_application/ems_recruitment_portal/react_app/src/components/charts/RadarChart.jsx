import React from 'react';
import BaseChart from './BaseChart';

const defaultOption = "{\n  \"tooltip\": {},\n  \"radar\": {\n    \"indicator\": []\n  },\n  \"series\": [\n    {\n      \"type\": \"radar\"\n    }\n  ]\n}";

const RadarChart = ({ data, option, theme, ...rest }) => {
  const mergedOption = { ...defaultOption, ...option };
  return <BaseChart option={mergedOption} data={data} theme={theme} {...rest} />;
};

export default RadarChart;