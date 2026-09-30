import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * BarChart Component
 * A React wrapper for Apache ECharts Bar Chart
 * 
 * Bar charts display categorical data with rectangular bars. Heights or lengths of bars are
 * proportional to the values they represent. Ideal for comparing quantities across categories,
 * showing rankings, or displaying distributions. Supports vertical/horizontal orientation,
 * stacking, and grouping.
 * 
 * @param {Object} data - Chart data
 * @param {Array<string>} data.xAxis - X-axis categories (e.g., ['Q1', 'Q2', 'Q3', 'Q4'])
 * @param {Array<Object>} data.series - Array of data series
 * @param {string} data.series[].name - Series name for legend
 * @param {Array<number>} data.series[].data - Bar heights for each category
 * @param {string} [data.series[].color] - Optional series color
 * @param {string} [data.series[].stack] - Stack group name (for stacked bars)
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   xAxis: ['Q1', 'Q2', 'Q3', 'Q4'],
 *   series: [
 *     { name: 'Revenue', data: [2000, 3000, 2500, 4000], color: '#5470c6' },
 *     { name: 'Profit', data: [500, 800, 600, 1000], color: '#91cc75' }
 *   ]
 * };
 * const config = { title: 'Quarterly Performance', stack: true, showLabel: true };
 */
const BarChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Bar Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        trigger: config.tooltipTrigger || 'axis',
        axisPointer: {
          type: config.axisPointerType || 'shadow'
        }
      },
      legend: {
        data: config.legendData || data.series?.map(s => s.name) || [],
        top: config.legendTop || 'bottom'
      },
      grid: {
        left: config.gridLeft || '3%',
        right: config.gridRight || '4%',
        bottom: config.gridBottom || '10%',
        top: config.gridTop || '15%',
        containLabel: true
      },
      xAxis: {
        type: config.xAxisType || 'category',
        data: data.xAxis || [],
        name: config.xAxisName || '',
        axisLabel: {
          rotate: config.xAxisLabelRotate || 0
        }
      },
      yAxis: {
        type: config.yAxisType || 'value',
        name: config.yAxisName || ''
      },
      series: (data.series || []).map(series => ({
        name: series.name,
        type: 'bar',
        data: series.data,
        barWidth: config.barWidth || 'auto',
        barGap: config.barGap || '30%',
        itemStyle: {
          color: series.color || config.barColor,
          borderRadius: config.barBorderRadius || 0
        },
        label: {
          show: config.showLabel || false,
          position: config.labelPosition || 'top'
        },
        stack: config.stack ? series.stack || 'total' : undefined
      }))
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

BarChart.configOptions = {
  title: { type: 'string', default: 'Bar Chart', help: 'Chart title text' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  tooltipTrigger: { type: 'string', default: 'axis', options: ['item', 'axis'], help: 'Tooltip trigger' },
  axisPointerType: { type: 'string', default: 'shadow', options: ['line', 'shadow', 'cross'], help: 'Axis pointer type' },
  legendData: { type: 'array', default: [], help: 'Legend items' },
  legendTop: { type: 'string', default: 'bottom', help: 'Legend position' },
  gridLeft: { type: 'string', default: '3%', help: 'Grid left margin' },
  gridRight: { type: 'string', default: '4%', help: 'Grid right margin' },
  gridBottom: { type: 'string', default: '10%', help: 'Grid bottom margin' },
  gridTop: { type: 'string', default: '15%', help: 'Grid top margin' },
  xAxisType: { type: 'string', default: 'category', options: ['value', 'category'], help: 'X-axis type' },
  xAxisName: { type: 'string', default: '', help: 'X-axis name' },
  xAxisLabelRotate: { type: 'number', default: 0, help: 'X-axis label rotation angle' },
  yAxisType: { type: 'string', default: 'value', options: ['value', 'category'], help: 'Y-axis type' },
  yAxisName: { type: 'string', default: '', help: 'Y-axis name' },
  barWidth: { type: 'string|number', default: 'auto', help: 'Bar width (px or %)' },
  barGap: { type: 'string', default: '30%', help: 'Gap between bars' },
  barColor: { type: 'color', default: null, help: 'Bar color' },
  barBorderRadius: { type: 'number', default: 0, help: 'Bar border radius' },
  showLabel: { type: 'boolean', default: false, help: 'Show value labels' },
  labelPosition: { type: 'string', default: 'top', options: ['top', 'inside', 'bottom'], help: 'Label position' },
  stack: { type: 'boolean', default: false, help: 'Enable stacked bars' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};

BarChart.dataFormat = {
  description: 'Bar chart data structure',
  structure: {
    xAxis: {
      type: 'Array<string|number>',
      required: true,
      description: 'X-axis categories',
      example: "['Q1', 'Q2', 'Q3', 'Q4']"
    },
    series: {
      type: 'Array<Object>',
      required: true,
      description: 'Array of bar series',
      properties: {
        name: { type: 'string', required: true, description: 'Series name' },
        data: { type: 'Array<number>', required: true, description: 'Bar values' },
        color: { type: 'string', required: false, description: 'Bar color' },
        stack: { type: 'string', required: false, description: 'Stack group name' }
      },
      example: "[{ name: 'Sales', data: [100, 200, 150], color: '#5470c6' }]"
    }
  }
};

export default BarChart;
