import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * LinesChart Component
 * A React wrapper for Apache ECharts Lines Chart
 * 
 * Lines charts draw lines between coordinates, often with animation effects. Can work with geographic or Cartesian coordinates. Ideal for showing routes, connections, migrations, trade flows, or any directional relationships between points.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * data: [
      { coords: [[x1, y1], [x2, y2]] },
      ...
    ]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = [
 *   { coords: [[0, 0], [100, 100]] },
 *   { coords: [[50, 50], [150, 150]] }
 * ];
 */
const LinesChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Lines Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        trigger: 'item'
      },
      geo: config.useGeo ? {
        map: config.mapName || 'world',
        roam: config.roam !== undefined ? config.roam : true,
        itemStyle: {
          areaColor: config.areaColor || '#eee',
          borderColor: config.borderColor || '#444'
        }
      } : undefined,
      xAxis: !config.useGeo ? {
        type: config.xAxisType || 'value',
        name: config.xAxisName || ''
      } : undefined,
      yAxis: !config.useGeo ? {
        type: config.yAxisType || 'value',
        name: config.yAxisName || ''
      } : undefined,
      series: [
        {
          type: 'lines',
          coordinateSystem: config.useGeo ? 'geo' : 'cartesian2d',
          data: data || [],
          polyline: config.polyline || false,
          effect: {
            show: config.showEffect !== undefined ? config.showEffect : true,
            period: config.effectPeriod || 6,
            trailLength: config.trailLength || 0.7,
            color: config.effectColor || '#fff',
            symbolSize: config.effectSymbolSize || 3
          },
          lineStyle: {
            color: config.lineColor || '#c23531',
            width: config.lineWidth || 1,
            opacity: config.lineOpacity || 0.6,
            curveness: config.curveness || 0.2,
            type: config.lineType || 'solid'
          },
          emphasis: {
            lineStyle: {
              width: config.emphasisLineWidth || 3
            }
          },
          zlevel: 1
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

LinesChart.configOptions = {
  title: { type: 'string', default: 'Lines Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  useGeo: { type: 'boolean', default: false, help: 'Use geographic coordinate system' },
  mapName: { type: 'string', default: 'world', help: 'Map name (if useGeo=true)' },
  roam: { type: 'boolean', default: true, help: 'Enable pan and zoom (if useGeo=true)' },
  areaColor: { type: 'color', default: '#eee', help: 'Map area color (if useGeo=true)' },
  borderColor: { type: 'color', default: '#444', help: 'Map border color (if useGeo=true)' },
  xAxisType: { type: 'string', default: 'value', options: ['value', 'category'], help: 'X-axis type (if useGeo=false)' },
  xAxisName: { type: 'string', default: '', help: 'X-axis name (if useGeo=false)' },
  yAxisType: { type: 'string', default: 'value', options: ['value', 'category'], help: 'Y-axis type (if useGeo=false)' },
  yAxisName: { type: 'string', default: '', help: 'Y-axis name (if useGeo=false)' },
  polyline: { type: 'boolean', default: false, help: 'Enable polyline (multiple segments)' },
  showEffect: { type: 'boolean', default: true, help: 'Show animation effect' },
  effectPeriod: { type: 'number', default: 6, help: 'Effect animation period (seconds)' },
  trailLength: { type: 'number', default: 0.7, help: 'Trail length (0-1)' },
  effectColor: { type: 'color', default: '#fff', help: 'Effect color' },
  effectSymbolSize: { type: 'number', default: 3, help: 'Effect symbol size' },
  lineColor: { type: 'color', default: '#c23531', help: 'Line color' },
  lineWidth: { type: 'number', default: 1, help: 'Line width' },
  lineOpacity: { type: 'number', default: 0.6, help: 'Line opacity (0-1)' },
  curveness: { type: 'number', default: 0.2, help: 'Line curvature (0-1)' },
  lineType: { type: 'string', default: 'solid', options: ['solid', 'dashed', 'dotted'], help: 'Line type' },
  emphasisLineWidth: { type: 'number', default: 3, help: 'Line width on hover' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '600px', help: 'Chart height' }
};


LinesChart.dataFormat = {
  description: 'Lines chart data structure',
  structure: `data: [
      { coords: [[x1, y1], [x2, y2]] },
      ...
    ]`,
  example: `const data = [
 *   { coords: [[0, 0], [100, 100]] },
 *   { coords: [[50, 50], [150, 150]] }
 * ];`
};


LinesChart.dataFormat = {
  description: 'Lines chart data structure',
  structure: `data: [
      { coords: [[x1, y1], [x2, y2]] },
      ...
    ]`,
  example: `const data = [
 *   { coords: [[0, 0], [100, 100]] },
 *   { coords: [[50, 50], [150, 150]] }
 * ];`
};

export default LinesChart;
