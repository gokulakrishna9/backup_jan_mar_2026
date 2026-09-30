import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * RadarChart Component
 * A React wrapper for Apache ECharts Radar Chart
 * 
 * Radar charts (spider/web charts) display multivariate data on axes starting from the same point. Each axis represents a different variable, making them perfect for comparing multiple characteristics across items, showing strengths/weaknesses, or displaying performance metrics.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * indicator: [{ name: 'Metric', max: maxValue }, ...]
    series: [
      {
        name: 'Series Name',
        value: [value1, value2, ...],
        color: '#color' (optional)
      }
    ]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   indicator: [
 *     { name: 'Sales', max: 100 },
 *     { name: 'Marketing', max: 100 }
 *   ],
 *   series: [{ name: 'Team A', value: [80, 90], color: '#5470c6' }]
 * };
 */
const RadarChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Radar Chart',
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
      radar: {
        indicator: data.indicator || [],
        shape: config.shape || 'polygon',
        radius: config.radius || '70%',
        center: config.center || ['50%', '50%'],
        splitNumber: config.splitNumber || 5,
        name: {
          textStyle: {
            color: config.indicatorColor || '#333',
            fontSize: config.indicatorFontSize || 12
          }
        },
        splitLine: {
          lineStyle: {
            color: config.splitLineColor || '#ccc'
          }
        },
        splitArea: {
          show: config.showSplitArea !== undefined ? config.showSplitArea : true,
          areaStyle: {
            color: config.splitAreaColors || ['rgba(114, 172, 209, 0.2)', 'rgba(114, 172, 209, 0.4)']
          }
        },
        axisLine: {
          lineStyle: {
            color: config.axisLineColor || '#ccc'
          }
        }
      },
      series: [
        {
          type: 'radar',
          data: (data.series || []).map(series => ({
            value: series.value,
            name: series.name,
            areaStyle: {
              opacity: config.areaOpacity || 0.3,
              color: series.color || config.areaColor
            },
            lineStyle: {
              width: config.lineWidth || 2,
              color: series.color || config.lineColor
            },
            symbol: config.symbol || 'circle',
            symbolSize: config.symbolSize || 4
          }))
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

RadarChart.configOptions = {
  title: { type: 'string', default: 'Radar Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  legendData: { type: 'array', default: [], help: 'Legend items' },
  legendTop: { type: 'string', default: 'bottom', help: 'Legend position' },
  shape: { type: 'string', default: 'polygon', options: ['polygon', 'circle'], help: 'Radar shape' },
  radius: { type: 'string', default: '70%', help: 'Radar radius' },
  center: { type: 'array', default: ['50%', '50%'], help: 'Radar center [x, y]' },
  splitNumber: { type: 'number', default: 5, help: 'Number of split segments' },
  indicatorColor: { type: 'color', default: '#333', help: 'Indicator label color' },
  indicatorFontSize: { type: 'number', default: 12, help: 'Indicator label font size' },
  splitLineColor: { type: 'color', default: '#ccc', help: 'Split line color' },
  showSplitArea: { type: 'boolean', default: true, help: 'Show split area' },
  splitAreaColors: { type: 'array', default: ['rgba(114, 172, 209, 0.2)', 'rgba(114, 172, 209, 0.4)'], help: 'Split area colors' },
  axisLineColor: { type: 'color', default: '#ccc', help: 'Axis line color' },
  areaOpacity: { type: 'number', default: 0.3, help: 'Area fill opacity (0-1)' },
  areaColor: { type: 'color', default: null, help: 'Area fill color' },
  lineWidth: { type: 'number', default: 2, help: 'Line width' },
  lineColor: { type: 'color', default: null, help: 'Line color' },
  symbol: { type: 'string', default: 'circle', options: ['circle', 'rect', 'roundRect', 'triangle', 'diamond', 'none'], help: 'Point symbol' },
  symbolSize: { type: 'number', default: 4, help: 'Point size' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};


RadarChart.dataFormat = {
  description: 'Radar chart data structure',
  structure: `indicator: [{ name: 'Metric', max: maxValue }, ...]
    series: [
      {
        name: 'Series Name',
        value: [value1, value2, ...],
        color: '#color' (optional)
      }
    ]`,
  example: `const data = {
 *   indicator: [
 *     { name: 'Sales', max: 100 },
 *     { name: 'Marketing', max: 100 }
 *   ],
 *   series: [{ name: 'Team A', value: [80, 90], color: '#5470c6' }]
 * };`
};


RadarChart.dataFormat = {
  description: 'Radar chart data structure',
  structure: `indicator: [{ name: 'Metric', max: maxValue }, ...]
    series: [
      {
        name: 'Series Name',
        value: [value1, value2, ...],
        color: '#color' (optional)
      }
    ]`,
  example: `const data = {
 *   indicator: [
 *     { name: 'Sales', max: 100 },
 *     { name: 'Marketing', max: 100 }
 *   ],
 *   series: [{ name: 'Team A', value: [80, 90], color: '#5470c6' }]
 * };`
};

export default RadarChart;
