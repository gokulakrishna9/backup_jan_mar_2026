import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import 'echarts-gl';

/**
 * Scatter3DChart Component
 * A React wrapper for Apache ECharts Scatter3D Chart
 * 
 * 3D scatter charts display data points in three-dimensional space. Each point has X, Y, and Z coordinates, making them ideal for visualizing 3D distributions, spatial data, scientific simulations, or any data with three continuous variables. Requires echarts-gl.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * series: [
      {
        name: 'Series Name',
        data: [[x, y, z], ...],
        color: '#color' (optional)
      }
    ]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   series: [
 *     { name: '3D Points', data: [[1, 2, 3], [4, 5, 6]] }
 *   ]
 * };
 */
const Scatter3DChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || '3D Scatter Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {},
      legend: {
        data: config.legendData || data.series?.map(s => s.name) || [],
        top: config.legendTop || 'bottom'
      },
      xAxis3D: {
        type: config.xAxisType || 'value',
        name: config.xAxisName || 'X'
      },
      yAxis3D: {
        type: config.yAxisType || 'value',
        name: config.yAxisName || 'Y'
      },
      zAxis3D: {
        type: config.zAxisType || 'value',
        name: config.zAxisName || 'Z'
      },
      grid3D: {
        viewControl: {
          projection: config.projection || 'perspective',
          autoRotate: config.autoRotate || false,
          autoRotateSpeed: config.autoRotateSpeed || 10,
          rotateSensitivity: config.rotateSensitivity || 1,
          zoomSensitivity: config.zoomSensitivity || 1,
          panSensitivity: config.panSensitivity || 1,
          distance: config.distance || 100,
          alpha: config.alpha || 40,
          beta: config.beta || 0
        },
        boxWidth: config.boxWidth || 100,
        boxHeight: config.boxHeight || 100,
        boxDepth: config.boxDepth || 100,
        light: {
          main: {
            intensity: config.lightIntensity || 1.2,
            shadow: config.showShadow !== undefined ? config.showShadow : true
          },
          ambient: {
            intensity: config.ambientIntensity || 0.3
          }
        }
      },
      series: (data.series || []).map(series => ({
        name: series.name,
        type: 'scatter3D',
        data: series.data,
        symbolSize: config.symbolSize || 5,
        itemStyle: {
          color: series.color || config.pointColor,
          opacity: config.pointOpacity || 0.8
        },
        emphasis: {
          itemStyle: {
            color: config.emphasisColor || '#fff'
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
        height: config.height || '600px' 
      }} 
    />
  );
};

Scatter3DChart.configOptions = {
  title: { type: 'string', default: '3D Scatter Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  legendData: { type: 'array', default: [], help: 'Legend items' },
  legendTop: { type: 'string', default: 'bottom', help: 'Legend position' },
  xAxisType: { type: 'string', default: 'value', options: ['value', 'category', 'time', 'log'], help: 'X-axis type' },
  xAxisName: { type: 'string', default: 'X', help: 'X-axis name' },
  yAxisType: { type: 'string', default: 'value', options: ['value', 'category', 'time', 'log'], help: 'Y-axis type' },
  yAxisName: { type: 'string', default: 'Y', help: 'Y-axis name' },
  zAxisType: { type: 'string', default: 'value', options: ['value', 'category', 'time', 'log'], help: 'Z-axis type' },
  zAxisName: { type: 'string', default: 'Z', help: 'Z-axis name' },
  projection: { type: 'string', default: 'perspective', options: ['perspective', 'orthographic'], help: 'Projection type' },
  autoRotate: { type: 'boolean', default: false, help: 'Enable auto rotation' },
  autoRotateSpeed: { type: 'number', default: 10, help: 'Auto rotation speed' },
  rotateSensitivity: { type: 'number', default: 1, help: 'Rotation sensitivity' },
  zoomSensitivity: { type: 'number', default: 1, help: 'Zoom sensitivity' },
  panSensitivity: { type: 'number', default: 1, help: 'Pan sensitivity' },
  distance: { type: 'number', default: 100, help: 'Camera distance' },
  alpha: { type: 'number', default: 40, help: 'Rotation angle around X-axis' },
  beta: { type: 'number', default: 0, help: 'Rotation angle around Y-axis' },
  boxWidth: { type: 'number', default: 100, help: '3D box width' },
  boxHeight: { type: 'number', default: 100, help: '3D box height' },
  boxDepth: { type: 'number', default: 100, help: '3D box depth' },
  lightIntensity: { type: 'number', default: 1.2, help: 'Main light intensity' },
  showShadow: { type: 'boolean', default: true, help: 'Show shadows' },
  ambientIntensity: { type: 'number', default: 0.3, help: 'Ambient light intensity' },
  symbolSize: { type: 'number', default: 5, help: 'Point size' },
  pointColor: { type: 'color', default: null, help: 'Point color' },
  pointOpacity: { type: 'number', default: 0.8, help: 'Point opacity (0-1)' },
  emphasisColor: { type: 'color', default: '#fff', help: 'Point color on hover' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '600px', help: 'Chart height' }
};


Scatter3DChart.dataFormat = {
  description: 'Scatter3D chart data structure',
  structure: `series: [
      {
        name: 'Series Name',
        data: [[x, y, z], ...],
        color: '#color' (optional)
      }
    ]`,
  example: `const data = {
 *   series: [
 *     { name: '3D Points', data: [[1, 2, 3], [4, 5, 6]] }
 *   ]
 * };`
};


Scatter3DChart.dataFormat = {
  description: 'Scatter3D chart data structure',
  structure: `series: [
      {
        name: 'Series Name',
        data: [[x, y, z], ...],
        color: '#color' (optional)
      }
    ]`,
  example: `const data = {
 *   series: [
 *     { name: '3D Points', data: [[1, 2, 3], [4, 5, 6]] }
 *   ]
 * };`
};

export default Scatter3DChart;
