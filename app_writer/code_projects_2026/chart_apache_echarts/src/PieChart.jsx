import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * PieChart Component
 * A React wrapper for Apache ECharts Pie Chart
 * 
 * Pie charts show proportions and percentages between categories by dividing a circle into
 * slices. Each slice represents a category's contribution to the total. Ideal for showing
 * composition, market share, budget allocation, or any part-to-whole relationships. Supports
 * donut charts (hollow center) and rose charts (nightingale/polar area).
 * 
 * @param {Array<Object>} data - Chart data array
 * @param {string} data[].name - Category name
 * @param {number} data[].value - Category value
 * @param {Object} [data[].itemStyle] - Optional item styling
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = [
 *   { value: 1048, name: 'Search Engine' },
 *   { value: 735, name: 'Direct' },
 *   { value: 580, name: 'Email' },
 *   { value: 484, name: 'Union Ads' }
 * ];
 * const config = { 
 *   title: 'Traffic Sources',
 *   radius: ['40%', '70%'], // Donut chart
 *   roseType: 'radius' // Rose chart
 * };
 */
const PieChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Pie Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        trigger: 'item',
        formatter: config.tooltipFormatter || '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: config.legendOrient || 'horizontal',
        left: config.legendLeft || 'center',
        top: config.legendTop || 'bottom',
        data: config.legendData || data.map(item => item.name)
      },
      series: [
        {
          name: config.seriesName || 'Data',
          type: 'pie',
          radius: config.radius || '50%',
          center: config.center || ['50%', '50%'],
          data: data,
          roseType: config.roseType || false,
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          },
          label: {
            show: config.showLabel !== undefined ? config.showLabel : true,
            position: config.labelPosition || 'outside',
            formatter: config.labelFormatter || '{b}: {d}%'
          },
          labelLine: {
            show: config.showLabelLine !== undefined ? config.showLabelLine : true,
            length: config.labelLineLength || 15,
            length2: config.labelLineLength2 || 10
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

PieChart.configOptions = {
  title: { type: 'string', default: 'Pie Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  tooltipFormatter: { type: 'string', default: '{a} <br/>{b}: {c} ({d}%)', help: 'Tooltip format string' },
  legendOrient: { type: 'string', default: 'horizontal', options: ['horizontal', 'vertical'], help: 'Legend orientation' },
  legendLeft: { type: 'string', default: 'center', help: 'Legend horizontal position' },
  legendTop: { type: 'string', default: 'bottom', help: 'Legend vertical position' },
  legendData: { type: 'array', default: [], help: 'Legend items (auto from data if empty)' },
  seriesName: { type: 'string', default: 'Data', help: 'Series name for tooltip' },
  radius: { type: 'string|array', default: '50%', help: 'Pie radius (e.g., "50%" or ["40%", "70%"] for donut)' },
  center: { type: 'array', default: ['50%', '50%'], help: 'Pie center position [x, y]' },
  roseType: { type: 'string|boolean', default: false, options: [false, 'radius', 'area'], help: 'Rose chart type' },
  showLabel: { type: 'boolean', default: true, help: 'Show labels' },
  labelPosition: { type: 'string', default: 'outside', options: ['outside', 'inside', 'center'], help: 'Label position' },
  labelFormatter: { type: 'string', default: '{b}: {d}%', help: 'Label format string' },
  showLabelLine: { type: 'boolean', default: true, help: 'Show label lines' },
  labelLineLength: { type: 'number', default: 15, help: 'First segment length of label line' },
  labelLineLength2: { type: 'number', default: 10, help: 'Second segment length of label line' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};

PieChart.dataFormat = {
  description: 'Pie chart data structure',
  structure: {
    data: {
      type: 'Array<Object>',
      required: true,
      description: 'Array of pie slices',
      properties: {
        name: { type: 'string', required: true, description: 'Category name' },
        value: { type: 'number', required: true, description: 'Category value' },
        itemStyle: { type: 'Object', required: false, description: 'Custom slice styling' }
      },
      example: "[{ name: 'Category A', value: 1048 }, { name: 'Category B', value: 735 }]"
    }
  }
};

export default PieChart;
