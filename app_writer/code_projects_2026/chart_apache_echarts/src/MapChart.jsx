import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * MapChart Component
 * A React wrapper for Apache ECharts Map Chart
 * 
 * Map charts display geographic data on maps. Values can be shown through colors, symbols, or other visual encodings. Ideal for regional statistics, location-based data, geographic distributions, or spatial analysis. Requires GeoJSON data registration.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * data: [
      { name: 'Region Name', value: number },
      ...
    ]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = [
 *   { name: 'California', value: 1000 },
 *   { name: 'Texas', value: 800 }
 * ];
 * // Note: Requires echarts.registerMap('mapName', geoJsonData)
 */
const MapChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    // Note: Map requires GeoJSON data to be registered
    // echarts.registerMap('mapName', geoJsonData);
    
    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Map Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        trigger: 'item',
        formatter: config.tooltipFormatter || '{b}<br/>{c}'
      },
      visualMap: config.showVisualMap !== undefined && config.showVisualMap ? {
        min: config.visualMapMin || 0,
        max: config.visualMapMax || 1000,
        text: config.visualMapText || ['High', 'Low'],
        realtime: false,
        calculable: true,
        inRange: {
          color: config.visualMapColors || ['lightskyblue', 'yellow', 'orangered']
        }
      } : undefined,
      series: [
        {
          name: config.seriesName || 'Data',
          type: 'map',
          map: config.mapName || 'world',
          roam: config.roam !== undefined ? config.roam : true,
          scaleLimit: {
            min: config.scaleMin || 1,
            max: config.scaleMax || 5
          },
          itemStyle: {
            areaColor: config.areaColor || '#eee',
            borderColor: config.borderColor || '#444',
            borderWidth: config.borderWidth || 0.5
          },
          emphasis: {
            label: {
              show: config.showEmphasisLabel !== undefined ? config.showEmphasisLabel : true,
              color: config.emphasisLabelColor || '#000'
            },
            itemStyle: {
              areaColor: config.emphasisAreaColor || '#ffd700',
              borderColor: config.emphasisBorderColor || '#444',
              borderWidth: config.emphasisBorderWidth || 1
            }
          },
          select: {
            label: {
              show: config.showSelectLabel !== undefined ? config.showSelectLabel : true,
              color: config.selectLabelColor || '#fff'
            },
            itemStyle: {
              areaColor: config.selectAreaColor || '#b1d1fc',
              borderColor: config.selectBorderColor || '#444',
              borderWidth: config.selectBorderWidth || 1
            }
          },
          label: {
            show: config.showLabel !== undefined ? config.showLabel : false,
            fontSize: config.labelFontSize || 10,
            color: config.labelColor || '#000'
          },
          data: data || []
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

MapChart.configOptions = {
  title: { type: 'string', default: 'Map Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  tooltipFormatter: { type: 'string|function', default: '{b}<br/>{c}', help: 'Tooltip formatter' },
  showVisualMap: { type: 'boolean', default: false, help: 'Show visual map component' },
  visualMapMin: { type: 'number', default: 0, help: 'Visual map minimum value' },
  visualMapMax: { type: 'number', default: 1000, help: 'Visual map maximum value' },
  visualMapText: { type: 'array', default: ['High', 'Low'], help: 'Visual map text labels' },
  visualMapColors: { type: 'array', default: ['lightskyblue', 'yellow', 'orangered'], help: 'Visual map color range' },
  seriesName: { type: 'string', default: 'Data', help: 'Series name' },
  mapName: { type: 'string', default: 'world', help: 'Map name (must be registered with echarts.registerMap)' },
  roam: { type: 'boolean', default: true, help: 'Enable pan and zoom' },
  scaleMin: { type: 'number', default: 1, help: 'Minimum zoom scale' },
  scaleMax: { type: 'number', default: 5, help: 'Maximum zoom scale' },
  areaColor: { type: 'color', default: '#eee', help: 'Default area color' },
  borderColor: { type: 'color', default: '#444', help: 'Border color' },
  borderWidth: { type: 'number', default: 0.5, help: 'Border width' },
  showEmphasisLabel: { type: 'boolean', default: true, help: 'Show label on hover' },
  emphasisLabelColor: { type: 'color', default: '#000', help: 'Label color on hover' },
  emphasisAreaColor: { type: 'color', default: '#ffd700', help: 'Area color on hover' },
  emphasisBorderColor: { type: 'color', default: '#444', help: 'Border color on hover' },
  emphasisBorderWidth: { type: 'number', default: 1, help: 'Border width on hover' },
  showSelectLabel: { type: 'boolean', default: true, help: 'Show label when selected' },
  selectLabelColor: { type: 'color', default: '#fff', help: 'Label color when selected' },
  selectAreaColor: { type: 'color', default: '#b1d1fc', help: 'Area color when selected' },
  selectBorderColor: { type: 'color', default: '#444', help: 'Border color when selected' },
  selectBorderWidth: { type: 'number', default: 1, help: 'Border width when selected' },
  showLabel: { type: 'boolean', default: false, help: 'Show region labels' },
  labelFontSize: { type: 'number', default: 10, help: 'Label font size' },
  labelColor: { type: 'color', default: '#000', help: 'Label color' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '600px', help: 'Chart height' }
};


MapChart.dataFormat = {
  description: 'Map chart data structure',
  structure: `data: [
      { name: 'Region Name', value: number },
      ...
    ]`,
  example: `const data = [
 *   { name: 'California', value: 1000 },
 *   { name: 'Texas', value: 800 }
 * ];
 * // Note: Requires echarts.registerMap('mapName', geoJsonData)`
};


MapChart.dataFormat = {
  description: 'Map chart data structure',
  structure: `data: [
      { name: 'Region Name', value: number },
      ...
    ]`,
  example: `const data = [
 *   { name: 'California', value: 1000 },
 *   { name: 'Texas', value: 800 }
 * ];
 * // Note: Requires echarts.registerMap('mapName', geoJsonData)`
};

export default MapChart;
