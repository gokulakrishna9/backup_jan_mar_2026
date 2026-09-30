import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * TreemapChart Component
 * A React wrapper for Apache ECharts Treemap Chart
 * 
 * Treemaps display hierarchical data as nested rectangles. Rectangle size represents quantitative values, making them ideal for showing proportions within hierarchies, disk space usage, portfolio composition, or organizational structures.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * data: [
      {
        name: 'Parent',
        value: number,
        children: [{ name: 'Child', value: number }, ...]
      }
    ]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = [{
 *   name: 'Root',
 *   children: [
 *     { name: 'A', value: 100 },
 *     { name: 'B', value: 200 }
 *   ]
 * }];
 */
const TreemapChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Treemap Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        formatter: config.tooltipFormatter || function(info) {
          return `${info.name}: ${info.value}`;
        }
      },
      series: [
        {
          type: 'treemap',
          data: data,
          left: config.left || '2%',
          right: config.right || '2%',
          top: config.top || '15%',
          bottom: config.bottom || '2%',
          roam: config.roam !== undefined ? config.roam : true,
          nodeClick: config.nodeClick || 'zoomToNode',
          breadcrumb: {
            show: config.showBreadcrumb !== undefined ? config.showBreadcrumb : true,
            top: config.breadcrumbTop || 'bottom',
            height: config.breadcrumbHeight || 22
          },
          label: {
            show: config.showLabel !== undefined ? config.showLabel : true,
            formatter: config.labelFormatter || '{b}',
            fontSize: config.labelFontSize || 12
          },
          upperLabel: {
            show: config.showUpperLabel !== undefined ? config.showUpperLabel : true,
            height: config.upperLabelHeight || 30,
            fontSize: config.upperLabelFontSize || 14
          },
          itemStyle: {
            borderColor: config.borderColor || '#fff',
            borderWidth: config.borderWidth || 2,
            gapWidth: config.gapWidth || 2
          },
          levels: config.levels || [
            {
              itemStyle: {
                borderColor: '#777',
                borderWidth: 0,
                gapWidth: 1
              },
              upperLabel: {
                show: false
              }
            },
            {
              itemStyle: {
                borderColor: '#555',
                borderWidth: 5,
                gapWidth: 1
              },
              emphasis: {
                itemStyle: {
                  borderColor: '#ddd'
                }
              }
            },
            {
              colorSaturation: [0.35, 0.5],
              itemStyle: {
                borderWidth: 5,
                gapWidth: 1,
                borderColorSaturation: 0.6
              }
            }
          ]
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

TreemapChart.configOptions = {
  title: { type: 'string', default: 'Treemap Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  tooltipFormatter: { type: 'function', default: null, help: 'Tooltip formatter function' },
  left: { type: 'string', default: '2%', help: 'Treemap left position' },
  right: { type: 'string', default: '2%', help: 'Treemap right position' },
  top: { type: 'string', default: '15%', help: 'Treemap top position' },
  bottom: { type: 'string', default: '2%', help: 'Treemap bottom position' },
  roam: { type: 'boolean', default: true, help: 'Enable roaming (pan and zoom)' },
  nodeClick: { type: 'string', default: 'zoomToNode', options: ['zoomToNode', 'link', false], help: 'Node click behavior' },
  showBreadcrumb: { type: 'boolean', default: true, help: 'Show breadcrumb navigation' },
  breadcrumbTop: { type: 'string', default: 'bottom', help: 'Breadcrumb position' },
  breadcrumbHeight: { type: 'number', default: 22, help: 'Breadcrumb height' },
  showLabel: { type: 'boolean', default: true, help: 'Show node labels' },
  labelFormatter: { type: 'string', default: '{b}', help: 'Label format' },
  labelFontSize: { type: 'number', default: 12, help: 'Label font size' },
  showUpperLabel: { type: 'boolean', default: true, help: 'Show upper level labels' },
  upperLabelHeight: { type: 'number', default: 30, help: 'Upper label height' },
  upperLabelFontSize: { type: 'number', default: 14, help: 'Upper label font size' },
  borderColor: { type: 'color', default: '#fff', help: 'Node border color' },
  borderWidth: { type: 'number', default: 2, help: 'Node border width' },
  gapWidth: { type: 'number', default: 2, help: 'Gap between nodes' },
  levels: { type: 'array', default: null, help: 'Level-specific configurations' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};


TreemapChart.dataFormat = {
  description: 'Treemap chart data structure',
  structure: `data: [
      {
        name: 'Parent',
        value: number,
        children: [{ name: 'Child', value: number }, ...]
      }
    ]`,
  example: `const data = [{
 *   name: 'Root',
 *   children: [
 *     { name: 'A', value: 100 },
 *     { name: 'B', value: 200 }
 *   ]
 * }];`
};


TreemapChart.dataFormat = {
  description: 'Treemap chart data structure',
  structure: `data: [
      {
        name: 'Parent',
        value: number,
        children: [{ name: 'Child', value: number }, ...]
      }
    ]`,
  example: `const data = [{
 *   name: 'Root',
 *   children: [
 *     { name: 'A', value: 100 },
 *     { name: 'B', value: 200 }
 *   ]
 * }];`
};

export default TreemapChart;
