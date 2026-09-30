import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import 'echarts-gl';

/**
 * Bar3DChart Component
 * A React wrapper for Apache ECharts Bar3D Chart
 * 
 * 3D bar charts display bars in three-dimensional space with X, Y axes for categories and Z axis for values. Bars can be colored by value using visual mapping. Ideal for comparing values across two categorical dimensions. Requires echarts-gl.
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
 *   xAxis: ['A', 'B'],
 *   yAxis: ['Q1', 'Q2'],
 *   data: [[0, 0, 100], [0, 1, 150], [1, 0, 200]]
 * };
 */
const Bar3DChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || '3D Bar Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {},
      visualMap: config.showVisualMap ? {
        max: config.visualMapMax || 100,
        inRange: {
          color: config.visualMapColors || ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
        }
      } : undefined,
      xAxis3D: {
        type: 'category',
        data: data.xAxis || [],
        name: config.xAxisName || ''
      },
      yAxis3D: {
        type: 'category',
        data: data.yAxis || [],
        name: config.yAxisName || ''
      },
      zAxis3D: {
        type: 'value',
        name: config.zAxisName || ''
      },
      grid3D: {
        viewControl: {
          projection: config.projection || 'perspective',
          autoRotate: config.autoRotate || false,
          autoRotateSpeed: config.autoRotateSpeed || 10,
          rotateSensitivity: config.rotateSensitivity || 1,
          zoomSensitivity: config.zoomSensitivity || 1,
          panSensitivity: config.panSensitivity || 1,
          distance: config.distance || 150,
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
      series: [
        {
          type: 'bar3D',
          data: data.data || [],
          shading: config.shading || 'color',
          label: {
            show: config.showLabel || false,
            fontSize: config.labelFontSize || 16,
            borderWidth: 1
          },
          itemStyle: {
            opacity: config.barOpacity || 0.8
          },
          emphasis: {
            label: {
              fontSize: config.emphasisLabelFontSize || 20,
              color: config.emphasisLabelColor || '#900'
            },
            itemStyle: {
              color: config.emphasisColor || '#900'
            }
          },
          bevelSize: config.bevelSize || 0.5,
          bevelSmoothness: config.bevelSmoothness || 2
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
        height: config.height || '600px' 
      }} 
    />
  );
};

Bar3DChart.configOptions = {
  title: { type: 'string', default: '3D Bar Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  showVisualMap: { type: 'boolean', default: false, help: 'Show visual map' },
  visualMapMax: { type: 'number', default: 100, help: 'Visual map maximum value' },
  visualMapColors: { type: 'array', default: null, help: 'Visual map color gradient' },
  xAxisName: { type: 'string', default: '', help: 'X-axis name' },
  yAxisName: { type: 'string', default: '', help: 'Y-axis name' },
  zAxisName: { type: 'string', default: '', help: 'Z-axis name' },
  projection: { type: 'string', default: 'perspective', options: ['perspective', 'orthographic'], help: 'Projection type' },
  autoRotate: { type: 'boolean', default: false, help: 'Enable auto rotation' },
  autoRotateSpeed: { type: 'number', default: 10, help: 'Auto rotation speed' },
  rotateSensitivity: { type: 'number', default: 1, help: 'Rotation sensitivity' },
  zoomSensitivity: { type: 'number', default: 1, help: 'Zoom sensitivity' },
  panSensitivity: { type: 'number', default: 1, help: 'Pan sensitivity' },
  distance: { type: 'number', default: 150, help: 'Camera distance' },
  alpha: { type: 'number', default: 40, help: 'Rotation angle around X-axis' },
  beta: { type: 'number', default: 0, help: 'Rotation angle around Y-axis' },
  boxWidth: { type: 'number', default: 100, help: '3D box width' },
  boxHeight: { type: 'number', default: 100, help: '3D box height' },
  boxDepth: { type: 'number', default: 100, help: '3D box depth' },
  lightIntensity: { type: 'number', default: 1.2, help: 'Main light intensity' },
  showShadow: { type: 'boolean', default: true, help: 'Show shadows' },
  ambientIntensity: { type: 'number', default: 0.3, help: 'Ambient light intensity' },
  shading: { type: 'string', default: 'color', options: ['color', 'lambert', 'realistic'], help: 'Shading mode' },
  showLabel: { type: 'boolean', default: false, help: 'Show bar labels' },
  labelFontSize: { type: 'number', default: 16, help: 'Label font size' },
  emphasisLabelFontSize: { type: 'number', default: 20, help: 'Label font size on hover' },
  emphasisLabelColor: { type: 'color', default: '#900', help: 'Label color on hover' },
  emphasisColor: { type: 'color', default: '#900', help: 'Bar color on hover' },
  barOpacity: { type: 'number', default: 0.8, help: 'Bar opacity (0-1)' },
  bevelSize: { type: 'number', default: 0.5, help: 'Bar bevel size' },
  bevelSmoothness: { type: 'number', default: 2, help: 'Bar bevel smoothness' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '600px', help: 'Chart height' }
};


Bar3DChart.dataFormat = {
  description: 'Bar3D chart data structure',
  structure: `xAxis: ['X1', 'X2', ...]
    yAxis: ['Y1', 'Y2', ...]
    data: [[xIndex, yIndex, value], ...]`,
  example: `const data = {
 *   xAxis: ['A', 'B'],
 *   yAxis: ['Q1', 'Q2'],
 *   data: [[0, 0, 100], [0, 1, 150], [1, 0, 200]]
 * };`
};


Bar3DChart.dataFormat = {
  description: 'Bar3D chart data structure',
  structure: `xAxis: ['X1', 'X2', ...]
    yAxis: ['Y1', 'Y2', ...]
    data: [[xIndex, yIndex, value], ...]`,
  example: `const data = {
 *   xAxis: ['A', 'B'],
 *   yAxis: ['Q1', 'Q2'],
 *   data: [[0, 0, 100], [0, 1, 150], [1, 0, 200]]
 * };`
};

export default Bar3DChart;
