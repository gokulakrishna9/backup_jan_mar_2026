import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * ScatterChart Component
 * A React wrapper for Apache ECharts Scatter Chart
 * 
 * Scatter charts display data as points in a 2D coordinate system. Each point represents two variables, making them ideal for showing correlations, distributions, and clusters. Useful for analyzing relationships between variables, identifying outliers, and visualizing data density.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * xAxis: ['Category1', 'Category2', ...] (optional for value axis)
    series: [
      {
        name: 'Series Name',
        data: [[x1, y1], [x2, y2], ...] or [[x, y, size], ...],
        color: '#color' (optional)
      }
    ]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   series: [
 *     { 
 *       name: 'Dataset 1', 
 *       data: [[10, 20], [15, 25], [20, 30]], 
 *       color: '#ee6666' 
 *     }
 *   ]
 * };
 * const config = { title: 'Scatter Analysis', symbolSize: 15 };
 */
const ScatterChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Scatter Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        trigger: 'item',
        formatter: config.tooltipFormatter || '{a}<br/>{b}: ({c})'
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
        type: config.xAxisType || 'value',
        name: config.xAxisName || '',
        splitLine: {
          show: config.showXSplitLine !== undefined ? config.showXSplitLine : true
        }
      },
      yAxis: {
        type: config.yAxisType || 'value',
        name: config.yAxisName || '',
        splitLine: {
          show: config.showYSplitLine !== undefined ? config.showYSplitLine : true
        }
      },
      series: (data.series || []).map(series => ({
        name: series.name,
        type: 'scatter',
        data: series.data,
        symbolSize: config.symbolSize || function(data) {
          return data[2] || 10;
        },
        symbol: config.symbol || 'circle',
        itemStyle: {
          color: series.color || config.pointColor,
          opacity: config.pointOpacity || 0.8
        },
        emphasis: {
          focus: 'series',
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
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

ScatterChart.configOptions = {
  title: { type: 'string', default: 'Scatter Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  tooltipFormatter: { type: 'string', default: '{a}<br/>{b}: ({c})', help: 'Tooltip format' },
  legendData: { type: 'array', default: [], help: 'Legend items' },
  legendTop: { type: 'string', default: 'bottom', help: 'Legend position' },
  gridLeft: { type: 'string', default: '3%', help: 'Grid left margin' },
  gridRight: { type: 'string', default: '4%', help: 'Grid right margin' },
  gridBottom: { type: 'string', default: '10%', help: 'Grid bottom margin' },
  gridTop: { type: 'string', default: '15%', help: 'Grid top margin' },
  xAxisType: { type: 'string', default: 'value', options: ['value', 'category', 'time', 'log'], help: 'X-axis type' },
  xAxisName: { type: 'string', default: '', help: 'X-axis name' },
  showXSplitLine: { type: 'boolean', default: true, help: 'Show X-axis split lines' },
  yAxisType: { type: 'string', default: 'value', options: ['value', 'category', 'time', 'log'], help: 'Y-axis type' },
  yAxisName: { type: 'string', default: '', help: 'Y-axis name' },
  showYSplitLine: { type: 'boolean', default: true, help: 'Show Y-axis split lines' },
  symbolSize: { type: 'number|function', default: 10, help: 'Point size (can be function for dynamic sizing)' },
  symbol: { type: 'string', default: 'circle', options: ['circle', 'rect', 'roundRect', 'triangle', 'diamond', 'pin', 'arrow'], help: 'Point symbol type' },
  pointColor: { type: 'color', default: null, help: 'Point color' },
  pointOpacity: { type: 'number', default: 0.8, help: 'Point opacity (0-1)' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};


ScatterChart.dataFormat = {
  description: 'Scatter chart data structure',
  structure: `xAxis: ['Category1', 'Category2', ...] (optional for value axis)
    series: [
      {
        name: 'Series Name',
        data: [[x1, y1], [x2, y2], ...] or [[x, y, size], ...],
        color: '#color' (optional)
      }
    ]`,
  example: `const data = {
 *   series: [
 *     { 
 *       name: 'Dataset 1', 
 *       data: [[10, 20], [15, 25], [20, 30]], 
 *       color: '#ee6666' 
 *     }
 *   ]
 * };
 * const config = { title: 'Scatter Analysis', symbolSize: 15 };`
};


ScatterChart.dataFormat = {
  description: 'Scatter chart data structure',
  structure: `xAxis: ['Category1', 'Category2', ...] (optional for value axis)
    series: [
      {
        name: 'Series Name',
        data: [[x1, y1], [x2, y2], ...] or [[x, y, size], ...],
        color: '#color' (optional)
      }
    ]`,
  example: `const data = {
 *   series: [
 *     { 
 *       name: 'Dataset 1', 
 *       data: [[10, 20], [15, 25], [20, 30]], 
 *       color: '#ee6666' 
 *     }
 *   ]
 * };
 * const config = { title: 'Scatter Analysis', symbolSize: 15 };`
};

export default ScatterChart;
