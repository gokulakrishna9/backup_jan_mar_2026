import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import 'echarts-gl';

/**
 * Surface3DChart Component
 * A React wrapper for Apache ECharts Surface3D Chart
 * 
 * 3D surface charts display continuous data as a surface in 3D space. Height and color represent values, making them ideal for mathematical functions, terrain visualization, heat distributions, or any continuous 2D-to-1D mapping. Requires echarts-gl.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * data: [[x, y, z], ...]
    // Or use parametric equations
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   data: [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 2]]
 * };
 */
const Surface3DChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || '3D Surface Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {},
      visualMap: config.showVisualMap !== undefined && config.showVisualMap ? {
        show: true,
        dimension: 2,
        min: config.visualMapMin || 0,
        max: config.visualMapMax || 100,
        inRange: {
          color: config.visualMapColors || ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
        }
      } : undefined,
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
            shadow: config.showShadow !== undefined ? config.showShadow : true,
            shadowQuality: config.shadowQuality || 'high'
          },
          ambient: {
            intensity: config.ambientIntensity || 0.3
          }
        },
        postEffect: config.enablePostEffect ? {
          enable: true,
          bloom: {
            enable: config.enableBloom || false,
            intensity: config.bloomIntensity || 0.1
          },
          SSAO: {
            enable: config.enableSSAO || false,
            quality: config.ssaoQuality || 'medium',
            radius: config.ssaoRadius || 2
          }
        } : undefined
      },
      series: [
        {
          type: 'surface',
          data: data.data || [],
          wireframe: {
            show: config.showWireframe !== undefined ? config.showWireframe : false,
            lineStyle: {
              color: config.wireframeColor || 'rgba(0,0,0,0.5)',
              width: config.wireframeWidth || 1
            }
          },
          shading: config.shading || 'color',
          itemStyle: {
            opacity: config.surfaceOpacity || 1
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
        height: config.height || '600px' 
      }} 
    />
  );
};

Surface3DChart.configOptions = {
  title: { type: 'string', default: '3D Surface Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  showVisualMap: { type: 'boolean', default: false, help: 'Show visual map' },
  visualMapMin: { type: 'number', default: 0, help: 'Visual map minimum value' },
  visualMapMax: { type: 'number', default: 100, help: 'Visual map maximum value' },
  visualMapColors: { type: 'array', default: null, help: 'Visual map color gradient' },
  xAxisType: { type: 'string', default: 'value', options: ['value', 'category'], help: 'X-axis type' },
  xAxisName: { type: 'string', default: 'X', help: 'X-axis name' },
  yAxisType: { type: 'string', default: 'value', options: ['value', 'category'], help: 'Y-axis type' },
  yAxisName: { type: 'string', default: 'Y', help: 'Y-axis name' },
  zAxisType: { type: 'string', default: 'value', options: ['value', 'category'], help: 'Z-axis type' },
  zAxisName: { type: 'string', default: 'Z', help: 'Z-axis name' },
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
  shadowQuality: { type: 'string', default: 'high', options: ['low', 'medium', 'high', 'ultra'], help: 'Shadow quality' },
  ambientIntensity: { type: 'number', default: 0.3, help: 'Ambient light intensity' },
  enablePostEffect: { type: 'boolean', default: false, help: 'Enable post-processing effects' },
  enableBloom: { type: 'boolean', default: false, help: 'Enable bloom effect' },
  bloomIntensity: { type: 'number', default: 0.1, help: 'Bloom intensity' },
  enableSSAO: { type: 'boolean', default: false, help: 'Enable SSAO (ambient occlusion)' },
  ssaoQuality: { type: 'string', default: 'medium', options: ['low', 'medium', 'high', 'ultra'], help: 'SSAO quality' },
  ssaoRadius: { type: 'number', default: 2, help: 'SSAO radius' },
  showWireframe: { type: 'boolean', default: false, help: 'Show wireframe' },
  wireframeColor: { type: 'color', default: 'rgba(0,0,0,0.5)', help: 'Wireframe color' },
  wireframeWidth: { type: 'number', default: 1, help: 'Wireframe line width' },
  shading: { type: 'string', default: 'color', options: ['color', 'lambert', 'realistic'], help: 'Shading mode' },
  surfaceOpacity: { type: 'number', default: 1, help: 'Surface opacity (0-1)' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '600px', help: 'Chart height' }
};


Surface3DChart.dataFormat = {
  description: 'Surface3D chart data structure',
  structure: `data: [[x, y, z], ...]
    // Or use parametric equations`,
  example: `const data = {
 *   data: [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 2]]
 * };`
};


Surface3DChart.dataFormat = {
  description: 'Surface3D chart data structure',
  structure: `data: [[x, y, z], ...]
    // Or use parametric equations`,
  example: `const data = {
 *   data: [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 2]]
 * };`
};

export default Surface3DChart;
