import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';
import 'echarts-gl';

/**
 * GraphGLChart Component
 * A React wrapper for Apache ECharts GraphGL Chart
 * 
 * 3D graph charts visualize large-scale network relationships in 3D space using WebGL for performance. Nodes and edges are rendered in 3D with force-directed layout. Ideal for large networks, complex relationships, or when 2D graphs become cluttered. Requires echarts-gl.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * nodes: [{ name: 'Node', value: number, category: index }, ...]
    edges: [{ source: 'Node1', target: 'Node2' }, ...]
    categories: [{ name: 'Category' }, ...]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   nodes: [{ name: 'A' }, { name: 'B' }],
 *   edges: [{ source: 'A', target: 'B' }]
 * };
 */
const GraphGLChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || '3D Graph Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {},
      legend: {
        data: config.legendData || [],
        top: config.legendTop || 'bottom'
      },
      series: [
        {
          type: 'graphGL',
          nodes: data.nodes || [],
          edges: data.edges || [],
          categories: data.categories || [],
          modularity: {
            resolution: config.modularityResolution || 2,
            sort: config.modularitySort !== undefined ? config.modularitySort : true
          },
          lineStyle: {
            color: config.lineColor || 'source',
            opacity: config.lineOpacity || 0.5,
            width: config.lineWidth || 1
          },
          itemStyle: {
            opacity: config.nodeOpacity || 0.9
          },
          forceAtlas2: {
            steps: config.forceSteps || 5,
            stopThreshold: config.stopThreshold || 1,
            jitterTolerence: config.jitterTolerence || 10,
            edgeWeight: config.edgeWeight || [1, 4],
            edgeWeightInfluence: config.edgeWeightInfluence || 1,
            nodeWeight: config.nodeWeight || [1, 4],
            nodeWeightInfluence: config.nodeWeightInfluence || 1,
            preventOverlap: config.preventOverlap !== undefined ? config.preventOverlap : false,
            gravity: config.gravity || 1
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

GraphGLChart.configOptions = {
  title: { type: 'string', default: '3D Graph Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  legendData: { type: 'array', default: [], help: 'Legend items' },
  legendTop: { type: 'string', default: 'bottom', help: 'Legend position' },
  modularityResolution: { type: 'number', default: 2, help: 'Modularity resolution' },
  modularitySort: { type: 'boolean', default: true, help: 'Sort by modularity' },
  lineColor: { type: 'color', default: 'source', help: 'Edge line color' },
  lineOpacity: { type: 'number', default: 0.5, help: 'Edge line opacity (0-1)' },
  lineWidth: { type: 'number', default: 1, help: 'Edge line width' },
  nodeOpacity: { type: 'number', default: 0.9, help: 'Node opacity (0-1)' },
  forceSteps: { type: 'number', default: 5, help: 'Force layout steps per frame' },
  stopThreshold: { type: 'number', default: 1, help: 'Stop threshold for layout' },
  jitterTolerence: { type: 'number', default: 10, help: 'Jitter tolerance' },
  edgeWeight: { type: 'array', default: [1, 4], help: 'Edge weight range [min, max]' },
  edgeWeightInfluence: { type: 'number', default: 1, help: 'Edge weight influence' },
  nodeWeight: { type: 'array', default: [1, 4], help: 'Node weight range [min, max]' },
  nodeWeightInfluence: { type: 'number', default: 1, help: 'Node weight influence' },
  preventOverlap: { type: 'boolean', default: false, help: 'Prevent node overlap' },
  gravity: { type: 'number', default: 1, help: 'Gravity strength' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '600px', help: 'Chart height' }
};


GraphGLChart.dataFormat = {
  description: 'GraphGL chart data structure',
  structure: `nodes: [{ name: 'Node', value: number, category: index }, ...]
    edges: [{ source: 'Node1', target: 'Node2' }, ...]
    categories: [{ name: 'Category' }, ...]`,
  example: `const data = {
 *   nodes: [{ name: 'A' }, { name: 'B' }],
 *   edges: [{ source: 'A', target: 'B' }]
 * };`
};


GraphGLChart.dataFormat = {
  description: 'GraphGL chart data structure',
  structure: `nodes: [{ name: 'Node', value: number, category: index }, ...]
    edges: [{ source: 'Node1', target: 'Node2' }, ...]
    categories: [{ name: 'Category' }, ...]`,
  example: `const data = {
 *   nodes: [{ name: 'A' }, { name: 'B' }],
 *   edges: [{ source: 'A', target: 'B' }]
 * };`
};

export default GraphGLChart;
