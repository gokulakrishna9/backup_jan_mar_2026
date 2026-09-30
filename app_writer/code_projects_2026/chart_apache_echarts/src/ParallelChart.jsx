import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * ParallelChart Component
 * A React wrapper for Apache ECharts Parallel Chart
 * 
 * Parallel coordinates charts display multivariate data where each variable has its own vertical axis. Lines connect values across axes, making them ideal for comparing multiple dimensions, filtering data, and identifying patterns in high-dimensional datasets.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * parallelAxis: [{ dim: 0, name: 'Axis1' }, ...]
    data: [[value1, value2, value3, ...], ...]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   parallelAxis: [{ dim: 0, name: 'Price' }, { dim: 1, name: 'Size' }],
 *   data: [[12.99, 100], [19.99, 200]]
 * };
 */
const ParallelChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Parallel Coordinates',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        trigger: 'item'
      },
      parallelAxis: data.parallelAxis || [],
      parallel: {
        left: config.left || '5%',
        right: config.right || '13%',
        bottom: config.bottom || '10%',
        top: config.top || '15%',
        parallelAxisDefault: {
          type: config.axisType || 'value',
          nameLocation: config.nameLocation || 'end',
          nameGap: config.nameGap || 20,
          nameTextStyle: {
            fontSize: config.nameFontSize || 12,
            color: config.nameColor || '#333'
          },
          axisLine: {
            lineStyle: {
              color: config.axisLineColor || '#aaa'
            }
          },
          axisTick: {
            lineStyle: {
              color: config.axisTickColor || '#777'
            }
          },
          splitLine: {
            show: config.showSplitLine !== undefined ? config.showSplitLine : true,
            lineStyle: {
              color: config.splitLineColor || '#ddd'
            }
          },
          axisLabel: {
            fontSize: config.labelFontSize || 10,
            color: config.labelColor || '#333'
          }
        }
      },
      series: [
        {
          type: 'parallel',
          lineStyle: {
            width: config.lineWidth || 2,
            opacity: config.lineOpacity || 0.5
          },
          smooth: config.smooth !== undefined ? config.smooth : false,
          data: data.data || [],
          inactiveOpacity: config.inactiveOpacity || 0.05,
          activeOpacity: config.activeOpacity || 1,
          realtime: config.realtime !== undefined ? config.realtime : true
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
        height: config.height || '500px' 
      }} 
    />
  );
};

ParallelChart.configOptions = {
  title: { type: 'string', default: 'Parallel Coordinates', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  left: { type: 'string', default: '5%', help: 'Chart left position' },
  right: { type: 'string', default: '13%', help: 'Chart right position' },
  bottom: { type: 'string', default: '10%', help: 'Chart bottom position' },
  top: { type: 'string', default: '15%', help: 'Chart top position' },
  axisType: { type: 'string', default: 'value', options: ['value', 'category', 'time', 'log'], help: 'Default axis type' },
  nameLocation: { type: 'string', default: 'end', options: ['start', 'middle', 'end'], help: 'Axis name location' },
  nameGap: { type: 'number', default: 20, help: 'Gap between axis name and axis line' },
  nameFontSize: { type: 'number', default: 12, help: 'Axis name font size' },
  nameColor: { type: 'color', default: '#333', help: 'Axis name color' },
  axisLineColor: { type: 'color', default: '#aaa', help: 'Axis line color' },
  axisTickColor: { type: 'color', default: '#777', help: 'Axis tick color' },
  showSplitLine: { type: 'boolean', default: true, help: 'Show split lines' },
  splitLineColor: { type: 'color', default: '#ddd', help: 'Split line color' },
  labelFontSize: { type: 'number', default: 10, help: 'Axis label font size' },
  labelColor: { type: 'color', default: '#333', help: 'Axis label color' },
  lineWidth: { type: 'number', default: 2, help: 'Data line width' },
  lineOpacity: { type: 'number', default: 0.5, help: 'Data line opacity (0-1)' },
  smooth: { type: 'boolean', default: false, help: 'Enable smooth lines' },
  inactiveOpacity: { type: 'number', default: 0.05, help: 'Inactive line opacity (0-1)' },
  activeOpacity: { type: 'number', default: 1, help: 'Active line opacity (0-1)' },
  realtime: { type: 'boolean', default: true, help: 'Real-time brush update' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '500px', help: 'Chart height' }
};


ParallelChart.dataFormat = {
  description: 'Parallel chart data structure',
  structure: `parallelAxis: [{ dim: 0, name: 'Axis1' }, ...]
    data: [[value1, value2, value3, ...], ...]`,
  example: `const data = {
 *   parallelAxis: [{ dim: 0, name: 'Price' }, { dim: 1, name: 'Size' }],
 *   data: [[12.99, 100], [19.99, 200]]
 * };`
};


ParallelChart.dataFormat = {
  description: 'Parallel chart data structure',
  structure: `parallelAxis: [{ dim: 0, name: 'Axis1' }, ...]
    data: [[value1, value2, value3, ...], ...]`,
  example: `const data = {
 *   parallelAxis: [{ dim: 0, name: 'Price' }, { dim: 1, name: 'Size' }],
 *   data: [[12.99, 100], [19.99, 200]]
 * };`
};

export default ParallelChart;
