import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * GraphChart Component
 * A React wrapper for Apache ECharts Graph Chart
 * 
 * Graph charts (network diagrams) visualize relationships between nodes using edges. Ideal for social networks, dependency graphs, organizational charts, knowledge graphs, or any connected data structure.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * nodes: [{ name: 'Node', value: number, category: index }, ...]
    links: [{ source: 'Node1', target: 'Node2', value: number }, ...]
    categories: [{ name: 'Category' }, ...]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   nodes: [{ name: 'A', value: 10 }, { name: 'B', value: 20 }],
 *   links: [{ source: 'A', target: 'B' }]
 * };
 */
const GraphChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Graph Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        formatter: config.tooltipFormatter || '{b}'
      },
      legend: {
        data: config.legendData || [],
        top: config.legendTop || 'bottom'
      },
      series: [
        {
          type: 'graph',
          layout: config.layout || 'force',
          data: data.nodes || [],
          links: data.links || [],
          categories: data.categories || [],
          roam: config.roam !== undefined ? config.roam : true,
          label: {
            show: config.showLabel !== undefined ? config.showLabel : true,
            position: config.labelPosition || 'right',
            formatter: config.labelFormatter || '{b}'
          },
          labelLayout: {
            hideOverlap: config.hideOverlap !== undefined ? config.hideOverlap : true
          },
          scaleLimit: {
            min: config.scaleMin || 0.4,
            max: config.scaleMax || 2
          },
          lineStyle: {
            color: config.lineColor || 'source',
            curveness: config.curveness || 0,
            width: config.lineWidth || 1
          },
          emphasis: {
            focus: config.emphasisFocus || 'adjacency',
            lineStyle: {
              width: config.emphasisLineWidth || 10
            }
          },
          force: config.layout === 'force' ? {
            repulsion: config.repulsion || 100,
            gravity: config.gravity || 0.1,
            edgeLength: config.edgeLength || 30,
            layoutAnimation: config.layoutAnimation !== undefined ? config.layoutAnimation : true
          } : undefined,
          circular: config.layout === 'circular' ? {
            rotateLabel: config.rotateLabel !== undefined ? config.rotateLabel : true
          } : undefined,
          symbolSize: config.symbolSize || 50,
          draggable: config.draggable !== undefined ? config.draggable : true,
          edgeSymbol: config.edgeSymbol || ['none', 'arrow'],
          edgeSymbolSize: config.edgeSymbolSize || [4, 10]
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

GraphChart.configOptions = {
  title: { type: 'string', default: 'Graph Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  tooltipFormatter: { type: 'string|function', default: '{b}', help: 'Tooltip formatter' },
  legendData: { type: 'array', default: [], help: 'Legend items' },
  legendTop: { type: 'string', default: 'bottom', help: 'Legend position' },
  layout: { type: 'string', default: 'force', options: ['none', 'circular', 'force'], help: 'Graph layout algorithm' },
  roam: { type: 'boolean', default: true, help: 'Enable pan and zoom' },
  showLabel: { type: 'boolean', default: true, help: 'Show node labels' },
  labelPosition: { type: 'string', default: 'right', options: ['left', 'right', 'top', 'bottom', 'inside'], help: 'Label position' },
  labelFormatter: { type: 'string', default: '{b}', help: 'Label format' },
  hideOverlap: { type: 'boolean', default: true, help: 'Hide overlapping labels' },
  scaleMin: { type: 'number', default: 0.4, help: 'Minimum zoom scale' },
  scaleMax: { type: 'number', default: 2, help: 'Maximum zoom scale' },
  lineColor: { type: 'color', default: 'source', help: 'Edge line color (source/target/color)' },
  curveness: { type: 'number', default: 0, help: 'Edge curvature (0-1)' },
  lineWidth: { type: 'number', default: 1, help: 'Edge line width' },
  emphasisFocus: { type: 'string', default: 'adjacency', options: ['none', 'self', 'series', 'adjacency'], help: 'Focus on hover' },
  emphasisLineWidth: { type: 'number', default: 10, help: 'Edge width on hover' },
  repulsion: { type: 'number', default: 100, help: 'Force layout: node repulsion' },
  gravity: { type: 'number', default: 0.1, help: 'Force layout: gravity to center' },
  edgeLength: { type: 'number', default: 30, help: 'Force layout: edge length' },
  layoutAnimation: { type: 'boolean', default: true, help: 'Force layout: enable animation' },
  rotateLabel: { type: 'boolean', default: true, help: 'Circular layout: rotate labels' },
  symbolSize: { type: 'number', default: 50, help: 'Node size' },
  draggable: { type: 'boolean', default: true, help: 'Enable node dragging' },
  edgeSymbol: { type: 'array', default: ['none', 'arrow'], help: 'Edge symbols [start, end]' },
  edgeSymbolSize: { type: 'array', default: [4, 10], help: 'Edge symbol sizes [start, end]' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '600px', help: 'Chart height' }
};


GraphChart.dataFormat = {
  description: 'Graph chart data structure',
  structure: `nodes: [{ name: 'Node', value: number, category: index }, ...]
    links: [{ source: 'Node1', target: 'Node2', value: number }, ...]
    categories: [{ name: 'Category' }, ...]`,
  example: `const data = {
 *   nodes: [{ name: 'A', value: 10 }, { name: 'B', value: 20 }],
 *   links: [{ source: 'A', target: 'B' }]
 * };`
};


GraphChart.dataFormat = {
  description: 'Graph chart data structure',
  structure: `nodes: [{ name: 'Node', value: number, category: index }, ...]
    links: [{ source: 'Node1', target: 'Node2', value: number }, ...]
    categories: [{ name: 'Category' }, ...]`,
  example: `const data = {
 *   nodes: [{ name: 'A', value: 10 }, { name: 'B', value: 20 }],
 *   links: [{ source: 'A', target: 'B' }]
 * };`
};

export default GraphChart;
