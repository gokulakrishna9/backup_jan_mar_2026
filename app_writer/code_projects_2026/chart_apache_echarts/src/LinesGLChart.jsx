import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import 'echarts-gl';

/**
 * LinesGLChart Component
 * A React wrapper for Apache ECharts LinesGL Chart
 * 
 * 3D lines charts on geographic maps display connections between locations on a 3D globe or map. Lines can be animated and styled. Perfect for flight routes, trade connections, migration patterns, or any geographic relationships. Requires echarts-gl.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * data: [
      { coords: [[lon1, lat1], [lon2, lat2]] },
      ...
    ]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = [
 *   { coords: [[-74, 40], [0, 51]] },
 *   { coords: [[139, 35], [-118, 34]] }
 * ];
 */
const LinesGLChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Lines GL Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      geo3D: {
        map: config.mapName || 'world',
        shading: config.shading || 'color',
        light: {
          main: {
            intensity: config.lightIntensity || 1
          },
          ambient: {
            intensity: config.ambientIntensity || 0.4
          }
        },
        viewControl: {
          autoRotate: config.autoRotate || false,
          distance: config.distance || 100
        },
        itemStyle: {
          color: config.mapColor || '#eee',
          opacity: config.mapOpacity || 1,
          borderWidth: config.borderWidth || 0.5,
          borderColor: config.borderColor || '#444'
        }
      },
      series: [
        {
          type: 'lines3D',
          coordinateSystem: 'geo3D',
          data: data || [],
          lineStyle: {
            width: config.lineWidth || 1,
            color: config.lineColor || '#c23531',
            opacity: config.lineOpacity || 0.6
          },
          blendMode: config.blendMode || 'source-over',
          effect: {
            show: config.showEffect !== undefined ? config.showEffect : true,
            period: config.effectPeriod || 4,
            trailWidth: config.trailWidth || 2,
            trailLength: config.trailLength || 0.2,
            trailOpacity: config.trailOpacity || 1
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

LinesGLChart.configOptions = {
  title: { type: 'string', default: 'Lines GL Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  mapName: { type: 'string', default: 'world', help: 'Map name (must be registered)' },
  shading: { type: 'string', default: 'color', options: ['color', 'lambert', 'realistic'], help: 'Shading mode' },
  lightIntensity: { type: 'number', default: 1, help: 'Main light intensity' },
  ambientIntensity: { type: 'number', default: 0.4, help: 'Ambient light intensity' },
  autoRotate: { type: 'boolean', default: false, help: 'Enable auto rotation' },
  distance: { type: 'number', default: 100, help: 'Camera distance' },
  mapColor: { type: 'color', default: '#eee', help: 'Map color' },
  mapOpacity: { type: 'number', default: 1, help: 'Map opacity (0-1)' },
  borderWidth: { type: 'number', default: 0.5, help: 'Map border width' },
  borderColor: { type: 'color', default: '#444', help: 'Map border color' },
  lineWidth: { type: 'number', default: 1, help: 'Line width' },
  lineColor: { type: 'color', default: '#c23531', help: 'Line color' },
  lineOpacity: { type: 'number', default: 0.6, help: 'Line opacity (0-1)' },
  blendMode: { type: 'string', default: 'source-over', help: 'Blend mode' },
  showEffect: { type: 'boolean', default: true, help: 'Show animation effect' },
  effectPeriod: { type: 'number', default: 4, help: 'Effect period (seconds)' },
  trailWidth: { type: 'number', default: 2, help: 'Trail width' },
  trailLength: { type: 'number', default: 0.2, help: 'Trail length (0-1)' },
  trailOpacity: { type: 'number', default: 1, help: 'Trail opacity (0-1)' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '600px', help: 'Chart height' }
};


LinesGLChart.dataFormat = {
  description: 'LinesGL chart data structure',
  structure: `data: [
      { coords: [[lon1, lat1], [lon2, lat2]] },
      ...
    ]`,
  example: `const data = [
 *   { coords: [[-74, 40], [0, 51]] },
 *   { coords: [[139, 35], [-118, 34]] }
 * ];`
};


LinesGLChart.dataFormat = {
  description: 'LinesGL chart data structure',
  structure: `data: [
      { coords: [[lon1, lat1], [lon2, lat2]] },
      ...
    ]`,
  example: `const data = [
 *   { coords: [[-74, 40], [0, 51]] },
 *   { coords: [[139, 35], [-118, 34]] }
 * ];`
};

export default LinesGLChart;
