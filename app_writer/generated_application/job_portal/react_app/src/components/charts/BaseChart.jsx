import React, { useRef, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';

/**
 * BaseChart — initializes ECharts instance, handles resize and lifecycle.
 */
const BaseChart = ({ option, data, theme, width, height, style, ...rest }) => {
  const chartRef = useRef(null);

  useEffect(() => {
    const handleResize = () => {
      chartRef.current?.getEchartsInstance()?.resize();
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const mergedOption = { ...option };
  if (data) {
    if (mergedOption.series && Array.isArray(mergedOption.series)) {
      mergedOption.series = mergedOption.series.map((s) => ({ ...s, data }));
    } else if (mergedOption.series) {
      mergedOption.series = { ...mergedOption.series, data };
    }
  }

  return (
    <ReactECharts
      ref={chartRef}
      option={mergedOption}
      theme={theme}
      style={ { width: width || '100%', height: height || '400px', ...style } }
      {...rest}
    />
  );
};

export default BaseChart;
