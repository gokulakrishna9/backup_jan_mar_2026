import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * BoxplotChart Component
 * A React wrapper for Apache ECharts Boxplot Chart
 * 
 * Boxplot charts (box-and-whisker plots) display statistical distributions showing median, quartiles, and outliers. Essential for statistical analysis, comparing distributions across groups, and identifying data anomalies.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * xAxis: ['Category1', 'Category2', ...]
    boxData: [[min, Q1, median, Q3, max], ...]
    outliers: [[categoryIndex, value], ...]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   xAxis: ['Group A', 'Group B'],
 *   boxData: [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]],
 *   outliers: [[0, 10], [1, 12]]
 * };
 */
const BoxplotChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Boxplot Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        trigger: 'item',
        axisPointer: {
          type: 'shadow'
        }
      },
      legend: {
        data: config.legendData || ['boxplot', 'outlier'],
        top: config.legendTop || 'bottom'
      },
      grid: {
        left: config.gridLeft || '10%',
        right: config.gridRight || '10%',
        bottom: config.gridBottom || '15%',
        top: config.gridTop || '15%'
      },
      xAxis: {
        type: 'category',
        data: data.xAxis || [],
        boundaryGap: true,
        nameGap: 30,
        splitArea: {
          show: config.showXSplitArea !== undefined ? config.showXSplitArea : false
        },
        splitLine: {
          show: false
        }
      },
      yAxis: {
        type: 'value',
        name: config.yAxisName || '',
        splitArea: {
          show: config.showYSplitArea !== undefined ? config.showYSplitArea : true
        }
      },
      series: [
        {
          name: 'boxplot',
          type: 'boxplot',
          data: data.boxData || [],
          itemStyle: {
            color: config.boxColor || '#b8c5f2',
            borderColor: config.boxBorderColor || '#8a9fd5'
          },
          boxWidth: config.boxWidth || [7, 50]
        },
        {
          name: 'outlier',
          type: 'scatter',
          data: data.outliers || [],
          itemStyle: {
            color: config.outlierColor || '#d94e5d'
          },
          symbolSize: config.outlierSize || 6
        }
      ]
    };

    chartInstance.current.setOption(option);

    const handleResize = () => chartInstance.current?.resize();
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chartInstance.current?.dispose();
    };
  }, [data, config]);

  return (
    <div 
      ref={chartRef} 
      style={{ 
        width: config.width || '100%', 
        height: config.height || '400px' 
      }} 
    />
  );
};

BoxplotChart.configOptions = {
  title: { type: 'string', default: 'Boxplot Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  legendData: { type: 'array', default: ['boxplot', 'outlier'], help: 'Legend items' },
  legendTop: { type: 'string', default: 'bottom', help: 'Legend position' },
  gridLeft: { type: 'string', default: '10%', help: 'Grid left margin' },
  gridRight: { type: 'string', default: '10%', help: 'Grid right margin' },
  gridBottom: { type: 'string', default: '15%', help: 'Grid bottom margin' },
  gridTop: { type: 'string', default: '15%', help: 'Grid top margin' },
  showXSplitArea: { type: 'boolean', default: false, help: 'Show X-axis split area' },
  yAxisName: { type: 'string', default: '', help: 'Y-axis name' },
  showYSplitArea: { type: 'boolean', default: true, help: 'Show Y-axis split area' },
  boxColor: { type: 'color', default: '#b8c5f2', help: 'Box fill color' },
  boxBorderColor: { type: 'color', default: '#8a9fd5', help: 'Box border color' },
  boxWidth: { type: 'array', default: [7, 50], help: 'Box width range [min, max]' },
  outlierColor: { type: 'color', default: '#d94e5d', help: 'Outlier point color' },
  outlierSize: { type: 'number', default: 6, help: 'Outlier point size' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};


BoxplotChart.dataFormat = {
  description: 'Boxplot chart data structure',
  structure: `xAxis: ['Category1', 'Category2', ...]
    boxData: [[min, Q1, median, Q3, max], ...]
    outliers: [[categoryIndex, value], ...]`,
  example: `const data = {
 *   xAxis: ['Group A', 'Group B'],
 *   boxData: [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]],
 *   outliers: [[0, 10], [1, 12]]
 * };`
};


BoxplotChart.dataFormat = {
  description: 'Boxplot chart data structure',
  structure: `xAxis: ['Category1', 'Category2', ...]
    boxData: [[min, Q1, median, Q3, max], ...]
    outliers: [[categoryIndex, value], ...]`,
  example: `const data = {
 *   xAxis: ['Group A', 'Group B'],
 *   boxData: [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]],
 *   outliers: [[0, 10], [1, 12]]
 * };`
};

export default BoxplotChart;
