import React from 'react';
import BaseChart from './BaseChart';

const defaultOption = "{\n  \"tooltip\": {\n    \"trigger\": \"item\"\n  },\n  \"series\": [\n    {\n      \"type\": \"funnel\",\n      \"left\": \"10%\",\n      \"width\": \"80%\"\n    }\n  ]\n}";

const FunnelChart = ({ data, option, theme, ...rest }) => {
  const mergedOption = { ...defaultOption, ...option };
  return <BaseChart option={mergedOption} data={data} theme={theme} {...rest} />;
};

export default FunnelChart;