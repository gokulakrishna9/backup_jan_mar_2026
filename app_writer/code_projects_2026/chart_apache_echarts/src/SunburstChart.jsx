import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * SunburstChart Component
 * A React wrapper for Apache ECharts Sunburst Chart
 * 
 * Sunburst charts visualize hierarchical data in concentric circles. Each ring represents a level in the hierarchy, with segments sized by value. Perfect for showing multi-level categorizations, file systems, or organizational hierarchies.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * data: {
      name: 'Root',
      children: [
        { name: 'Child', value: number, children: [...] }
      ]
    }
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   name: 'Root',
 *   children: [
 *     { name: 'A', value: 100 },
 *     { name: 'B', value: 200, children: [...] }
 *   ]
 * };
 */
const SunburstChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Sunburst Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        trigger: 'item'
      },
      series: [
        {
          type: 'sunburst',
          data: data,
          radius: config.radius || [0, '90%'],
          center: config.center || ['50%', '50%'],
          sort: config.sort || 'desc',
          highlightPolicy: config.highlightPolicy || 'ancestor',
          itemStyle: {
            borderRadius: config.borderRadius || 7,
            borderWidth: config.borderWidth || 2,
            borderColor: config.borderColor || '#fff'
          },
          label: {
            show: config.showLabel !== undefined ? config.showLabel : true,
            rotate: config.labelRotate || 'radial',
            fontSize: config.labelFontSize || 12
          },
          levels: config.levels || [
            {},
            {
              r0: '15%',
              r: '35%',
              itemStyle: {
                borderWidth: 2
              },
              label: {
                rotate: 'tangential'
              }
            },
            {
              r0: '35%',
              r: '70%',
              label: {
                align: 'right'
              }
            },
            {
              r0: '70%',
              r: '72%',
              label: {
                position: 'outside',
                padding: 3,
                silent: false
              },
              itemStyle: {
                borderWidth: 3
              }
            }
          ]
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

SunburstChart.configOptions = {
  title: { type: 'string', default: 'Sunburst Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  radius: { type: 'array', default: [0, '90%'], help: 'Sunburst radius [inner, outer]' },
  center: { type: 'array', default: ['50%', '50%'], help: 'Sunburst center [x, y]' },
  sort: { type: 'string', default: 'desc', options: ['desc', 'asc', null], help: 'Sort order' },
  highlightPolicy: { type: 'string', default: 'ancestor', options: ['ancestor', 'descendant', 'self', 'none'], help: 'Highlight policy on hover' },
  borderRadius: { type: 'number', default: 7, help: 'Sector border radius' },
  borderWidth: { type: 'number', default: 2, help: 'Sector border width' },
  borderColor: { type: 'color', default: '#fff', help: 'Sector border color' },
  showLabel: { type: 'boolean', default: true, help: 'Show labels' },
  labelRotate: { type: 'string', default: 'radial', options: ['radial', 'tangential', 0], help: 'Label rotation' },
  labelFontSize: { type: 'number', default: 12, help: 'Label font size' },
  levels: { type: 'array', default: null, help: 'Level-specific configurations' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};


SunburstChart.dataFormat = {
  description: 'Sunburst chart data structure',
  structure: `data: {
      name: 'Root',
      children: [
        { name: 'Child', value: number, children: [...] }
      ]
    }`,
  example: `const data = {
 *   name: 'Root',
 *   children: [
 *     { name: 'A', value: 100 },
 *     { name: 'B', value: 200, children: [...] }
 *   ]
 * };`
};


SunburstChart.dataFormat = {
  description: 'Sunburst chart data structure',
  structure: `data: {
      name: 'Root',
      children: [
        { name: 'Child', value: number, children: [...] }
      ]
    }`,
  example: `const data = {
 *   name: 'Root',
 *   children: [
 *     { name: 'A', value: 100 },
 *     { name: 'B', value: 200, children: [...] }
 *   ]
 * };`
};

export default SunburstChart;
