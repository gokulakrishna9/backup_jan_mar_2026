import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * EffectScatterChart Component
 * A React wrapper for Apache ECharts EffectScatter Chart
 * 
 * Effect scatter charts are scatter plots with animated ripple effects on points. The animation draws attention to specific data points, making them ideal for highlighting important values, showing real-time updates, or emphasizing key insights.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * series: [
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
 *     { name: 'Important Points', data: [[10, 20, 30], [15, 25, 40]] }
 *   ]
 * };
 */
const EffectScatterChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Effect Scatter Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        trigger: 'item'
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
        type: 'effectScatter',
        data: series.data,
        symbolSize: config.symbolSize || function(val) {
          return val[2] || 10;
        },
        showEffectOn: config.showEffectOn || 'render',
        rippleEffect: {
          brushType: config.rippleBrushType || 'stroke',
          scale: config.rippleScale || 2.5,
          period: config.ripplePeriod || 4
        },
        itemStyle: {
          color: series.color || config.pointColor,
          shadowBlur: config.shadowBlur || 10,
          shadowColor: config.shadowColor || 'rgba(0, 0, 0, 0.5)'
        },
        zlevel: 1
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

EffectScatterChart.configOptions = {
  title: { type: 'string', default: 'Effect Scatter Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
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
  symbolSize: { type: 'number|function', default: 10, help: 'Point size (can be function)' },
  showEffectOn: { type: 'string', default: 'render', options: ['render', 'emphasis'], help: 'When to show effect' },
  rippleBrushType: { type: 'string', default: 'stroke', options: ['stroke', 'fill'], help: 'Ripple brush type' },
  rippleScale: { type: 'number', default: 2.5, help: 'Ripple scale factor' },
  ripplePeriod: { type: 'number', default: 4, help: 'Ripple animation period (seconds)' },
  pointColor: { type: 'color', default: null, help: 'Point color' },
  shadowBlur: { type: 'number', default: 10, help: 'Shadow blur size' },
  shadowColor: { type: 'color', default: 'rgba(0, 0, 0, 0.5)', help: 'Shadow color' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};


EffectScatterChart.dataFormat = {
  description: 'EffectScatter chart data structure',
  structure: `series: [
      {
        name: 'Series Name',
        data: [[x1, y1], [x2, y2], ...] or [[x, y, size], ...],
        color: '#color' (optional)
      }
    ]`,
  example: `const data = {
 *   series: [
 *     { name: 'Important Points', data: [[10, 20, 30], [15, 25, 40]] }
 *   ]
 * };`
};


EffectScatterChart.dataFormat = {
  description: 'EffectScatter chart data structure',
  structure: `series: [
      {
        name: 'Series Name',
        data: [[x1, y1], [x2, y2], ...] or [[x, y, size], ...],
        color: '#color' (optional)
      }
    ]`,
  example: `const data = {
 *   series: [
 *     { name: 'Important Points', data: [[10, 20, 30], [15, 25, 40]] }
 *   ]
 * };`
};

export default EffectScatterChart;
