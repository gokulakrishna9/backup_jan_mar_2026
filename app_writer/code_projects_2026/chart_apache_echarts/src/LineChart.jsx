import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * LineChart Component
 * A React wrapper for Apache ECharts Line Chart
 * 
 * Line charts are used to show trends over time or continuous data. They connect data points
 * with lines to visualize changes and patterns. Ideal for time series data, stock prices,
 * temperature changes, or any data that shows progression.
 * 
 * @param {Object} data - Chart data
 * @param {Array<string>} data.xAxis - X-axis categories/labels (e.g., ['Mon', 'Tue', 'Wed'])
 * @param {Array<Object>} data.series - Array of data series
 * @param {string} data.series[].name - Series name for legend
 * @param {Array<number>} data.series[].data - Y-axis values for each x-axis point
 * @param {string} [data.series[].color] - Optional series color
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   xAxis: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
 *   series: [
 *     { name: 'Sales', data: [120, 200, 150, 80, 70], color: '#5470c6' },
 *     { name: 'Revenue', data: [100, 180, 130, 90, 85], color: '#91cc75' }
 *   ]
 * };
 * const config = { title: 'Weekly Sales', smooth: true, showArea: true };
 */
const LineChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    // Initialize chart
    chartInstance.current = echarts.init(chartRef.current);

    // Build chart option
    const option = {
      title: {
        text: config.title || 'Line Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        trigger: config.tooltipTrigger || 'axis',
        axisPointer: {
          type: config.axisPointerType || 'cross'
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
        boundaryGap: config.xAxisBoundaryGap !== undefined ? config.xAxisBoundaryGap : false,
        data: data.xAxis || [],
        name: config.xAxisName || '',
        nameLocation: config.xAxisNameLocation || 'end'
      },
      yAxis: {
        type: config.yAxisType || 'value',
        name: config.yAxisName || '',
        nameLocation: config.yAxisNameLocation || 'end'
      },
      series: (data.series || []).map(series => ({
        name: series.name,
        type: 'line',
        data: series.data,
        smooth: config.smooth !== undefined ? config.smooth : false,
        lineStyle: {
          width: config.lineWidth || 2,
          color: series.color || config.lineColor
        },
        areaStyle: config.showArea ? {} : undefined,
        symbol: config.symbol || 'circle',
        symbolSize: config.symbolSize || 4
      }))
    };

    chartInstance.current.setOption(option);

    // Handle resize
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

// Configuration properties with help text
LineChart.configOptions = {
  title: { type: 'string', default: 'Line Chart', help: 'Chart title text' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size in pixels' },
  titleColor: { type: 'string', default: '#333', help: 'Title text color' },
  tooltipTrigger: { type: 'string', default: 'axis', options: ['item', 'axis', 'none'], help: 'Tooltip trigger type' },
  axisPointerType: { type: 'string', default: 'cross', options: ['line', 'shadow', 'cross'], help: 'Axis pointer type' },
  legendData: { type: 'array', default: [], help: 'Legend items (auto-generated from series if not provided)' },
  legendTop: { type: 'string', default: 'bottom', help: 'Legend vertical position' },
  gridLeft: { type: 'string', default: '3%', help: 'Grid left margin' },
  gridRight: { type: 'string', default: '4%', help: 'Grid right margin' },
  gridBottom: { type: 'string', default: '10%', help: 'Grid bottom margin' },
  gridTop: { type: 'string', default: '15%', help: 'Grid top margin' },
  xAxisType: { type: 'string', default: 'category', options: ['value', 'category', 'time', 'log'], help: 'X-axis type' },
  xAxisBoundaryGap: { type: 'boolean', default: false, help: 'Leave blank space on both sides of axis' },
  xAxisName: { type: 'string', default: '', help: 'X-axis name' },
  xAxisNameLocation: { type: 'string', default: 'end', options: ['start', 'middle', 'end'], help: 'X-axis name location' },
  yAxisType: { type: 'string', default: 'value', options: ['value', 'category', 'time', 'log'], help: 'Y-axis type' },
  yAxisName: { type: 'string', default: '', help: 'Y-axis name' },
  yAxisNameLocation: { type: 'string', default: 'end', options: ['start', 'middle', 'end'], help: 'Y-axis name location' },
  smooth: { type: 'boolean', default: false, help: 'Enable smooth curve' },
  lineWidth: { type: 'number', default: 2, help: 'Line width in pixels' },
  lineColor: { type: 'string', default: null, help: 'Line color (overrides series color)' },
  showArea: { type: 'boolean', default: false, help: 'Show area under line' },
  symbol: { type: 'string', default: 'circle', options: ['circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow', 'none'], help: 'Symbol type for data points' },
  symbolSize: { type: 'number', default: 4, help: 'Symbol size in pixels' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};

// Data format description
LineChart.dataFormat = {
  description: 'Line chart data structure',
  structure: {
    xAxis: {
      type: 'Array<string|number>',
      required: true,
      description: 'X-axis categories or values',
      example: "['Mon', 'Tue', 'Wed', 'Thu', 'Fri']"
    },
    series: {
      type: 'Array<Object>',
      required: true,
      description: 'Array of data series to plot',
      properties: {
        name: { type: 'string', required: true, description: 'Series name for legend' },
        data: { type: 'Array<number>', required: true, description: 'Y-axis values' },
        color: { type: 'string', required: false, description: 'Series color (hex/rgb)' }
      },
      example: "[{ name: 'Sales', data: [120, 200, 150], color: '#5470c6' }]"
    }
  }
};

export default LineChart;
