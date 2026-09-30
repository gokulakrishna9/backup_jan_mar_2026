import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import 'echarts-gl';

/**
 * FlowGLChart Component
 * A React wrapper for Apache ECharts FlowGL Chart
 * 
 * Flow GL charts visualize vector fields in 3D space using animated particles. Particles follow the flow direction, making them ideal for fluid dynamics, wind patterns, electromagnetic fields, or any vector field visualization. Requires echarts-gl.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * data: [[x, y, z, vx, vy, vz], ...]
    // vx, vy, vz are velocity components
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = [
 *   [0, 0, 0, 1, 0, 0],
 *   [1, 0, 0, 1, 1, 0]
 * ];
 */
const FlowGLChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Flow GL Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {},
      visualMap: config.showVisualMap ? {
        min: config.visualMapMin || 0,
        max: config.visualMapMax || 100,
        dimension: config.visualMapDimension || 2,
        inRange: {
          color: config.visualMapColors || ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8']
        }
      } : undefined,
      xAxis3D: {
        type: 'value',
        name: config.xAxisName || 'X'
      },
      yAxis3D: {
        type: 'value',
        name: config.yAxisName || 'Y'
      },
      zAxis3D: {
        type: 'value',
        name: config.zAxisName || 'Z'
      },
      grid3D: {
        viewControl: {
          projection: config.projection || 'perspective',
          autoRotate: config.autoRotate || false,
          autoRotateSpeed: config.autoRotateSpeed || 10,
          distance: config.distance || 100
        },
        boxWidth: config.boxWidth || 100,
        boxHeight: config.boxHeight || 100,
        boxDepth: config.boxDepth || 100
      },
      series: [
        {
          type: 'flowGL',
          data: data || [],
          particleDensity: config.particleDensity || 128,
          particleType: config.particleType || 'point',
          particleSize: config.particleSize || 1,
          particleSpeed: config.particleSpeed || 1,
          particleTrail: config.particleTrail || 2,
          supersampling: config.supersampling || 1,
          itemStyle: {
            opacity: config.particleOpacity || 0.7
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

FlowGLChart.configOptions = {
  title: { type: 'string', default: 'Flow GL Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  showVisualMap: { type: 'boolean', default: false, help: 'Show visual map' },
  visualMapMin: { type: 'number', default: 0, help: 'Visual map minimum' },
  visualMapMax: { type: 'number', default: 100, help: 'Visual map maximum' },
  visualMapDimension: { type: 'number', default: 2, help: 'Visual map dimension' },
  visualMapColors: { type: 'array', default: null, help: 'Visual map color range' },
  xAxisName: { type: 'string', default: 'X', help: 'X-axis name' },
  yAxisName: { type: 'string', default: 'Y', help: 'Y-axis name' },
  zAxisName: { type: 'string', default: 'Z', help: 'Z-axis name' },
  projection: { type: 'string', default: 'perspective', options: ['perspective', 'orthographic'], help: 'Projection type' },
  autoRotate: { type: 'boolean', default: false, help: 'Enable auto rotation' },
  autoRotateSpeed: { type: 'number', default: 10, help: 'Auto rotation speed' },
  distance: { type: 'number', default: 100, help: 'Camera distance' },
  boxWidth: { type: 'number', default: 100, help: '3D box width' },
  boxHeight: { type: 'number', default: 100, help: '3D box height' },
  boxDepth: { type: 'number', default: 100, help: '3D box depth' },
  particleDensity: { type: 'number', default: 128, help: 'Particle density' },
  particleType: { type: 'string', default: 'point', options: ['point', 'line'], help: 'Particle type' },
  particleSize: { type: 'number', default: 1, help: 'Particle size' },
  particleSpeed: { type: 'number', default: 1, help: 'Particle speed' },
  particleTrail: { type: 'number', default: 2, help: 'Particle trail length' },
  supersampling: { type: 'number', default: 1, help: 'Supersampling factor' },
  particleOpacity: { type: 'number', default: 0.7, help: 'Particle opacity (0-1)' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '600px', help: 'Chart height' }
};


FlowGLChart.dataFormat = {
  description: 'FlowGL chart data structure',
  structure: `data: [[x, y, z, vx, vy, vz], ...]
    // vx, vy, vz are velocity components`,
  example: `const data = [
 *   [0, 0, 0, 1, 0, 0],
 *   [1, 0, 0, 1, 1, 0]
 * ];`
};


FlowGLChart.dataFormat = {
  description: 'FlowGL chart data structure',
  structure: `data: [[x, y, z, vx, vy, vz], ...]
    // vx, vy, vz are velocity components`,
  example: `const data = [
 *   [0, 0, 0, 1, 0, 0],
 *   [1, 0, 0, 1, 1, 0]
 * ];`
};

export default FlowGLChart;
