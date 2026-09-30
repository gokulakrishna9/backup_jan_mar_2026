import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * HeatmapChart Component
 * A React wrapper for Apache ECharts Heatmap Chart
 * 
 * Heatmaps use color intensity to represent data values in a matrix format. Ideal for showing patterns, correlations, time-based activity, geographic data density, or any 2D data distribution where color indicates magnitude.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * xAxis: ['X1', 'X2', ...]
    yAxis: ['Y1', 'Y2', ...]
    data: [[xIndex, yIndex, value], ...]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   xAxis: ['Mon', 'Tue', 'Wed'],
 *   yAxis: ['Morning', 'Afternoon'],
 *   data: [[0, 0, 5], [0, 1, 1], [1, 0, 15]]
 * };
 */
const HeatmapChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Heatmap Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        position: 'top',
        formatter: config.tooltipFormatter || function(params) {
          return `${params.name}: ${params.value[2]}`;
        }
      },
      grid: {
        left: config.gridLeft || '3%',
        right: config.gridRight || '10%',
        bottom: config.gridBottom || '10%',
        top: config.gridTop || '15%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: data.xAxis || [],
        splitArea: {
          show: config.showXSplitArea !== undefined ? config.showXSplitArea : true
        },
        axisLabel: {
          rotate: config.xAxisLabelRotate || 0
        }
      },
      yAxis: {
        type: 'category',
        data: data.yAxis || [],
        splitArea: {
          show: config.showYSplitArea !== undefined ? config.showYSplitArea : true
        }
      },
      visualMap: {
        min: config.min || 0,
        max: config.max || 100,
        calculable: config.calculable !== undefined ? config.calculable : true,
        orient: config.visualMapOrient || 'vertical',
        left: config.visualMapLeft || 'right',
        top: config.visualMapTop || 'center',
        inRange: {
          color: config.colorRange || ['#50a3ba', '#eac736', '#d94e5d']
        }
      },
      series: [
        {
          name: config.seriesName || 'Heatmap',
          type: 'heatmap',
          data: data.data || [],
          label: {
            show: config.showLabel || false,
            fontSize: config.labelFontSize || 10
          },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
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

HeatmapChart.configOptions = {
  title: { type: 'string', default: 'Heatmap Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  tooltipFormatter: { type: 'function', default: null, help: 'Tooltip formatter function' },
  gridLeft: { type: 'string', default: '3%', help: 'Grid left margin' },
  gridRight: { type: 'string', default: '10%', help: 'Grid right margin' },
  gridBottom: { type: 'string', default: '10%', help: 'Grid bottom margin' },
  gridTop: { type: 'string', default: '15%', help: 'Grid top margin' },
  showXSplitArea: { type: 'boolean', default: true, help: 'Show X-axis split area' },
  xAxisLabelRotate: { type: 'number', default: 0, help: 'X-axis label rotation' },
  showYSplitArea: { type: 'boolean', default: true, help: 'Show Y-axis split area' },
  min: { type: 'number', default: 0, help: 'Visual map minimum value' },
  max: { type: 'number', default: 100, help: 'Visual map maximum value' },
  calculable: { type: 'boolean', default: true, help: 'Enable visual map dragging' },
  visualMapOrient: { type: 'string', default: 'vertical', options: ['vertical', 'horizontal'], help: 'Visual map orientation' },
  visualMapLeft: { type: 'string', default: 'right', help: 'Visual map horizontal position' },
  visualMapTop: { type: 'string', default: 'center', help: 'Visual map vertical position' },
  colorRange: { type: 'array', default: ['#50a3ba', '#eac736', '#d94e5d'], help: 'Color gradient range' },
  seriesName: { type: 'string', default: 'Heatmap', help: 'Series name' },
  showLabel: { type: 'boolean', default: false, help: 'Show cell labels' },
  labelFontSize: { type: 'number', default: 10, help: 'Label font size' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};


HeatmapChart.dataFormat = {
  description: 'Heatmap chart data structure',
  structure: `xAxis: ['X1', 'X2', ...]
    yAxis: ['Y1', 'Y2', ...]
    data: [[xIndex, yIndex, value], ...]`,
  example: `const data = {
 *   xAxis: ['Mon', 'Tue', 'Wed'],
 *   yAxis: ['Morning', 'Afternoon'],
 *   data: [[0, 0, 5], [0, 1, 1], [1, 0, 15]]
 * };`
};


HeatmapChart.dataFormat = {
  description: 'Heatmap chart data structure',
  structure: `xAxis: ['X1', 'X2', ...]
    yAxis: ['Y1', 'Y2', ...]
    data: [[xIndex, yIndex, value], ...]`,
  example: `const data = {
 *   xAxis: ['Mon', 'Tue', 'Wed'],
 *   yAxis: ['Morning', 'Afternoon'],
 *   data: [[0, 0, 5], [0, 1, 1], [1, 0, 15]]
 * };`
};

export default HeatmapChart;
