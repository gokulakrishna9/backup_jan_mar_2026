import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * PictorialBarChart Component
 * A React wrapper for Apache ECharts PictorialBar Chart
 * 
 * Pictorial bar charts use custom symbols or images instead of rectangular bars. Symbols can repeat to show quantity, making them ideal for infographics, presentations, or any visualization requiring visual metaphors and enhanced engagement.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * xAxis: ['Category1', 'Category2', ...]
    series: [
      {
        name: 'Series Name',
        data: [value1, value2, ...],
        symbol: 'path:// or image:// or built-in',
        color: '#color' (optional)
      }
    ]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   xAxis: ['Mon', 'Tue', 'Wed'],
 *   series: [{ name: 'Sales', data: [100, 200, 150], symbol: 'rect' }]
 * };
 */
const PictorialBarChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Pictorial Bar Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
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
        axisTick: { show: false },
        axisLine: { show: false },
        axisLabel: {
          margin: config.xAxisLabelMargin || 10
        }
      },
      yAxis: {
        type: config.yAxisType || 'value',
        axisLabel: { show: config.showYAxisLabel !== undefined ? config.showYAxisLabel : true },
        axisTick: { show: false },
        axisLine: { show: false },
        splitLine: {
          lineStyle: {
            type: 'dashed'
          }
        }
      },
      series: (data.series || []).map(series => ({
        name: series.name,
        type: 'pictorialBar',
        data: series.data,
        symbol: config.symbol || series.symbol || 'rect',
        symbolRepeat: config.symbolRepeat || false,
        symbolSize: config.symbolSize || ['80%', '60%'],
        symbolMargin: config.symbolMargin || 1,
        symbolClip: config.symbolClip !== undefined ? config.symbolClip : true,
        symbolPosition: config.symbolPosition || 'start',
        symbolOffset: config.symbolOffset || [0, 0],
        symbolBoundingData: config.symbolBoundingData || null,
        itemStyle: {
          color: series.color || config.barColor,
          opacity: config.barOpacity || 1
        },
        label: {
          show: config.showLabel || false,
          position: config.labelPosition || 'top',
          fontSize: config.labelFontSize || 12
        },
        z: 10
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

PictorialBarChart.configOptions = {
  title: { type: 'string', default: 'Pictorial Bar Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  legendData: { type: 'array', default: [], help: 'Legend items' },
  legendTop: { type: 'string', default: 'bottom', help: 'Legend position' },
  gridLeft: { type: 'string', default: '3%', help: 'Grid left margin' },
  gridRight: { type: 'string', default: '4%', help: 'Grid right margin' },
  gridBottom: { type: 'string', default: '10%', help: 'Grid bottom margin' },
  gridTop: { type: 'string', default: '15%', help: 'Grid top margin' },
  xAxisType: { type: 'string', default: 'category', options: ['value', 'category'], help: 'X-axis type' },
  xAxisLabelMargin: { type: 'number', default: 10, help: 'X-axis label margin' },
  yAxisType: { type: 'string', default: 'value', options: ['value', 'category'], help: 'Y-axis type' },
  showYAxisLabel: { type: 'boolean', default: true, help: 'Show Y-axis labels' },
  symbol: { type: 'string', default: 'rect', help: 'Symbol type (path://, image://, or built-in)' },
  symbolRepeat: { type: 'boolean|string', default: false, help: 'Repeat symbol (true/false/fixed)' },
  symbolSize: { type: 'array', default: ['80%', '60%'], help: 'Symbol size [width, height]' },
  symbolMargin: { type: 'number', default: 1, help: 'Margin between repeated symbols' },
  symbolClip: { type: 'boolean', default: true, help: 'Clip symbol by data value' },
  symbolPosition: { type: 'string', default: 'start', options: ['start', 'end', 'center'], help: 'Symbol position' },
  symbolOffset: { type: 'array', default: [0, 0], help: 'Symbol offset [x, y]' },
  symbolBoundingData: { type: 'number', default: null, help: 'Bounding data for symbol clipping' },
  barColor: { type: 'color', default: null, help: 'Bar color' },
  barOpacity: { type: 'number', default: 1, help: 'Bar opacity (0-1)' },
  showLabel: { type: 'boolean', default: false, help: 'Show labels' },
  labelPosition: { type: 'string', default: 'top', options: ['top', 'inside', 'bottom'], help: 'Label position' },
  labelFontSize: { type: 'number', default: 12, help: 'Label font size' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};


PictorialBarChart.dataFormat = {
  description: 'PictorialBar chart data structure',
  structure: `xAxis: ['Category1', 'Category2', ...]
    series: [
      {
        name: 'Series Name',
        data: [value1, value2, ...],
        symbol: 'path:// or image:// or built-in',
        color: '#color' (optional)
      }
    ]`,
  example: `const data = {
 *   xAxis: ['Mon', 'Tue', 'Wed'],
 *   series: [{ name: 'Sales', data: [100, 200, 150], symbol: 'rect' }]
 * };`
};


PictorialBarChart.dataFormat = {
  description: 'PictorialBar chart data structure',
  structure: `xAxis: ['Category1', 'Category2', ...]
    series: [
      {
        name: 'Series Name',
        data: [value1, value2, ...],
        symbol: 'path:// or image:// or built-in',
        color: '#color' (optional)
      }
    ]`,
  example: `const data = {
 *   xAxis: ['Mon', 'Tue', 'Wed'],
 *   series: [{ name: 'Sales', data: [100, 200, 150], symbol: 'rect' }]
 * };`
};

export default PictorialBarChart;
