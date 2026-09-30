import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * CustomChart Component
 * A React wrapper for Apache ECharts Custom Chart
 * 
 * Custom charts allow complete control over rendering using a custom renderItem function. You define how each data item is drawn using graphic primitives. Perfect for unique visualizations, specialized charts, or when built-in chart types don't meet requirements.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * data: [
      [value1, value2, ...],
      ...
    ]
    // Structure depends on your custom renderItem function
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   xAxis: ['A', 'B', 'C'],
 *   data: [[0, 10, 20], [1, 15, 25]]
 * };
 * const config = {
 *   renderItem: (params, api) => ({ type: 'rect', ... })
 * };
 */
const CustomChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Custom Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        trigger: config.tooltipTrigger || 'item'
      },
      legend: {
        data: config.legendData || [],
        top: config.legendTop || 'bottom'
      },
      xAxis: config.xAxis || {
        type: 'category',
        data: data.xAxis || []
      },
      yAxis: config.yAxis || {
        type: 'value'
      },
      series: [
        {
          type: 'custom',
          renderItem: config.renderItem || function(params, api) {
            // Default render function - simple rectangle
            const categoryIndex = api.value(0);
            const start = api.coord([categoryIndex, api.value(1)]);
            const size = api.size([1, api.value(2)]);
            const style = api.style();
            
            return {
              type: 'rect',
              shape: {
                x: start[0] - size[0] / 2,
                y: start[1],
                width: size[0],
                height: size[1]
              },
              style: style
            };
          },
          encode: config.encode || {
            x: 0,
            y: [1, 2]
          },
          data: data.data || [],
          clip: config.clip !== undefined ? config.clip : true,
          z: config.z || 2
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

CustomChart.configOptions = {
  title: { type: 'string', default: 'Custom Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  tooltipTrigger: { type: 'string', default: 'item', options: ['item', 'axis', 'none'], help: 'Tooltip trigger' },
  legendData: { type: 'array', default: [], help: 'Legend items' },
  legendTop: { type: 'string', default: 'bottom', help: 'Legend position' },
  xAxis: { type: 'object', default: null, help: 'X-axis configuration object' },
  yAxis: { type: 'object', default: null, help: 'Y-axis configuration object' },
  renderItem: { type: 'function', default: null, help: 'Custom render function (params, api) => graphic element' },
  encode: { type: 'object', default: { x: 0, y: [1, 2] }, help: 'Data encoding configuration' },
  clip: { type: 'boolean', default: true, help: 'Clip graphics outside coordinate system' },
  z: { type: 'number', default: 2, help: 'Z-index level' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};


CustomChart.dataFormat = {
  description: 'Custom chart data structure',
  structure: `data: [
      [value1, value2, ...],
      ...
    ]
    // Structure depends on your custom renderItem function`,
  example: `const data = {
 *   xAxis: ['A', 'B', 'C'],
 *   data: [[0, 10, 20], [1, 15, 25]]
 * };
 * const config = {
 *   renderItem: (params, api) => ({ type: 'rect', ... })
 * };`
};


CustomChart.dataFormat = {
  description: 'Custom chart data structure',
  structure: `data: [
      [value1, value2, ...],
      ...
    ]
    // Structure depends on your custom renderItem function`,
  example: `const data = {
 *   xAxis: ['A', 'B', 'C'],
 *   data: [[0, 10, 20], [1, 15, 25]]
 * };
 * const config = {
 *   renderItem: (params, api) => ({ type: 'rect', ... })
 * };`
};

export default CustomChart;
