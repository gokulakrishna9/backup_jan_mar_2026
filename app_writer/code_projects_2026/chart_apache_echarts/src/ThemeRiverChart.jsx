import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * ThemeRiverChart Component
 * A React wrapper for Apache ECharts ThemeRiver Chart
 * 
 * ThemeRiver charts show temporal changes in multiple categories using flowing, organic shapes. Each stream represents a category, with width indicating value over time. Ideal for showing trends, topic evolution, or temporal distributions across categories.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * data: [
      ['date', value, 'category'],
      ...
    ]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = [
 *   ['2024-01-01', 100, 'Category A'],
 *   ['2024-01-01', 80, 'Category B'],
 *   ['2024-01-02', 120, 'Category A']
 * ];
 */
const ThemeRiverChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'ThemeRiver Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'line',
          lineStyle: {
            color: 'rgba(0,0,0,0.2)',
            width: 1,
            type: 'solid'
          }
        }
      },
      legend: {
        data: config.legendData || [],
        top: config.legendTop || 'bottom'
      },
      singleAxis: {
        top: config.axisTop || 50,
        bottom: config.axisBottom || 50,
        axisTick: {},
        axisLabel: {},
        type: config.axisType || 'time',
        axisPointer: {
          animation: true,
          label: {
            show: true
          }
        },
        splitLine: {
          show: config.showSplitLine !== undefined ? config.showSplitLine : true,
          lineStyle: {
            type: config.splitLineType || 'dashed',
            opacity: config.splitLineOpacity || 0.2
          }
        }
      },
      series: [
        {
          type: 'themeRiver',
          emphasis: {
            itemStyle: {
              shadowBlur: 20,
              shadowColor: 'rgba(0, 0, 0, 0.8)'
            }
          },
          data: data || [],
          label: {
            show: config.showLabel !== undefined ? config.showLabel : true,
            position: config.labelPosition || 'left',
            fontSize: config.labelFontSize || 11
          }
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

ThemeRiverChart.configOptions = {
  title: { type: 'string', default: 'ThemeRiver Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  legendData: { type: 'array', default: [], help: 'Legend items' },
  legendTop: { type: 'string', default: 'bottom', help: 'Legend position' },
  axisTop: { type: 'number', default: 50, help: 'Axis top margin' },
  axisBottom: { type: 'number', default: 50, help: 'Axis bottom margin' },
  axisType: { type: 'string', default: 'time', options: ['value', 'category', 'time'], help: 'Axis type' },
  showSplitLine: { type: 'boolean', default: true, help: 'Show split lines' },
  splitLineType: { type: 'string', default: 'dashed', options: ['solid', 'dashed', 'dotted'], help: 'Split line type' },
  splitLineOpacity: { type: 'number', default: 0.2, help: 'Split line opacity (0-1)' },
  showLabel: { type: 'boolean', default: true, help: 'Show labels' },
  labelPosition: { type: 'string', default: 'left', options: ['left', 'right', 'top', 'bottom', 'inside'], help: 'Label position' },
  labelFontSize: { type: 'number', default: 11, help: 'Label font size' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};


ThemeRiverChart.dataFormat = {
  description: 'ThemeRiver chart data structure',
  structure: `data: [
      ['date', value, 'category'],
      ...
    ]`,
  example: `const data = [
 *   ['2024-01-01', 100, 'Category A'],
 *   ['2024-01-01', 80, 'Category B'],
 *   ['2024-01-02', 120, 'Category A']
 * ];`
};


ThemeRiverChart.dataFormat = {
  description: 'ThemeRiver chart data structure',
  structure: `data: [
      ['date', value, 'category'],
      ...
    ]`,
  example: `const data = [
 *   ['2024-01-01', 100, 'Category A'],
 *   ['2024-01-01', 80, 'Category B'],
 *   ['2024-01-02', 120, 'Category A']
 * ];`
};

export default ThemeRiverChart;
