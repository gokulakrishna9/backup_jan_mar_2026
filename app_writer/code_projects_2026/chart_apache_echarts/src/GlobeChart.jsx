import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import 'echarts-gl';

/**
 * GlobeChart Component
 * A React wrapper for Apache ECharts Globe Chart
 * 
 * Globe charts display data on a 3D Earth globe. Can show points, lines, or other visualizations on geographic coordinates. Perfect for global data, international connections, worldwide distributions, or any planetary-scale visualization. Requires echarts-gl.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * series: [
      {
        type: 'scatter3D' or 'lines3D',
        data: [[lon, lat, value], ...] or lines data
      }
    ]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   series: [
 *     { type: 'scatter3D', data: [[-74, 40, 100], [0, 51, 200]] }
 *   ]
 * };
 */
const GlobeChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Globe Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      globe: {
        baseTexture: config.baseTexture || null,
        heightTexture: config.heightTexture || null,
        displacementScale: config.displacementScale || 0.1,
        shading: config.shading || 'realistic',
        environment: config.environment || null,
        light: {
          main: {
            intensity: config.lightIntensity || 1,
            shadow: config.showShadow !== undefined ? config.showShadow : false
          },
          ambient: {
            intensity: config.ambientIntensity || 0.1
          }
        },
        viewControl: {
          autoRotate: config.autoRotate || false,
          autoRotateSpeed: config.autoRotateSpeed || 10,
          rotateSensitivity: config.rotateSensitivity || 1,
          zoomSensitivity: config.zoomSensitivity || 1,
          distance: config.distance || 150,
          alpha: config.alpha || 40,
          beta: config.beta || 0
        },
        layers: config.layers || []
      },
      series: (data.series || []).map(series => ({
        type: series.type || 'scatter3D',
        coordinateSystem: 'globe',
        data: series.data,
        symbolSize: config.symbolSize || 5,
        itemStyle: {
          color: series.color || config.pointColor,
          opacity: config.pointOpacity || 0.8
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

GlobeChart.configOptions = {
  title: { type: 'string', default: 'Globe Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  baseTexture: { type: 'string', default: null, help: 'Base texture image URL' },
  heightTexture: { type: 'string', default: null, help: 'Height texture image URL' },
  displacementScale: { type: 'number', default: 0.1, help: 'Displacement scale for height texture' },
  shading: { type: 'string', default: 'realistic', options: ['color', 'lambert', 'realistic'], help: 'Shading mode' },
  environment: { type: 'string', default: null, help: 'Environment map URL' },
  lightIntensity: { type: 'number', default: 1, help: 'Main light intensity' },
  showShadow: { type: 'boolean', default: false, help: 'Show shadows' },
  ambientIntensity: { type: 'number', default: 0.1, help: 'Ambient light intensity' },
  autoRotate: { type: 'boolean', default: false, help: 'Enable auto rotation' },
  autoRotateSpeed: { type: 'number', default: 10, help: 'Auto rotation speed' },
  rotateSensitivity: { type: 'number', default: 1, help: 'Rotation sensitivity' },
  zoomSensitivity: { type: 'number', default: 1, help: 'Zoom sensitivity' },
  distance: { type: 'number', default: 150, help: 'Camera distance' },
  alpha: { type: 'number', default: 40, help: 'Rotation angle around X-axis' },
  beta: { type: 'number', default: 0, help: 'Rotation angle around Y-axis' },
  layers: { type: 'array', default: [], help: 'Globe layers configuration' },
  symbolSize: { type: 'number', default: 5, help: 'Point size' },
  pointColor: { type: 'color', default: null, help: 'Point color' },
  pointOpacity: { type: 'number', default: 0.8, help: 'Point opacity (0-1)' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '600px', help: 'Chart height' }
};


GlobeChart.dataFormat = {
  description: 'Globe chart data structure',
  structure: `series: [
      {
        type: 'scatter3D' or 'lines3D',
        data: [[lon, lat, value], ...] or lines data
      }
    ]`,
  example: `const data = {
 *   series: [
 *     { type: 'scatter3D', data: [[-74, 40, 100], [0, 51, 200]] }
 *   ]
 * };`
};


GlobeChart.dataFormat = {
  description: 'Globe chart data structure',
  structure: `series: [
      {
        type: 'scatter3D' or 'lines3D',
        data: [[lon, lat, value], ...] or lines data
      }
    ]`,
  example: `const data = {
 *   series: [
 *     { type: 'scatter3D', data: [[-74, 40, 100], [0, 51, 200]] }
 *   ]
 * };`
};

export default GlobeChart;
