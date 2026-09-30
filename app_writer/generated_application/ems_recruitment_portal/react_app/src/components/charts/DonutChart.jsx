import React from 'react';
import BaseChart from './BaseChart';

const defaultOption = "{\n  \"tooltip\": {\n    \"trigger\": \"item\"\n  },\n  \"series\": [\n    {\n      \"type\": \"pie\",\n      \"radius\": [\n        \"40%\",\n        \"70%\"\n      ]\n    }\n  ]\n}";

const DonutChart = ({ data, option, theme, ...rest }) => {
  const mergedOption = { ...defaultOption, ...option };
  return <BaseChart option={mergedOption} data={data} theme={theme} {...rest} />;
};

export default DonutChart;