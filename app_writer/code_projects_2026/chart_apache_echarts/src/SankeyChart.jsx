import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * SankeyChart Component
 * A React wrapper for Apache ECharts Sankey Chart
 * 
 * Sankey diagrams show flow quantities between nodes using proportional link widths. Perfect for visualizing energy flows, material transfers, budget allocations, or any process where quantities flow between stages.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * nodes: [{ name: 'Node Name' }, ...]
    links: [{ source: 'Node1', target: 'Node2', value: number }, ...]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   nodes: [{ name: 'A' }, { name: 'B' }],
 *   links: [{ source: 'A', target: 'B', value: 100 }]
 * };
 */
const SankeyChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Sankey Diagram',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        trigger: 'item',
        triggerOn: 'mousemove'
      },
      series: [
        {
          type: 'sankey',
          data: data.nodes || [],
          links: data.links || [],
          emphasis: {
            focus: 'adjacency'
          },
          left: config.left || '5%',
          right: config.right || '20%',
          top: config.top || '15%',
          bottom: config.bottom || '5%',
          nodeWidth: config.nodeWidth || 20,
          nodeGap: config.nodeGap || 8,
          nodeAlign: config.nodeAlign || 'justify',
          layoutIterations: config.layoutIterations || 32,
          orient: config.orient || 'horizontal',
          draggable: config.draggable !== undefined ? config.draggable : true,
          label: {
            show: config.showLabel !== undefined ? config.showLabel : true,
            position: config.labelPosition || 'right',
            fontSize: config.labelFontSize || 12,
            color: config.labelColor || '#000'
          },
          itemStyle: {
            borderWidth: config.borderWidth || 1,
            borderColor: config.borderColor || '#aaa'
          },
          lineStyle: {
            color: config.lineColor || 'gradient',
            opacity: config.lineOpacity || 0.2,
            curveness: config.curveness || 0.5
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

SankeyChart.configOptions = {
  title: { type: 'string', default: 'Sankey Diagram', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  left: { type: 'string', default: '5%', help: 'Diagram left position' },
  right: { type: 'string', default: '20%', help: 'Diagram right position' },
  top: { type: 'string', default: '15%', help: 'Diagram top position' },
  bottom: { type: 'string', default: '5%', help: 'Diagram bottom position' },
  nodeWidth: { type: 'number', default: 20, help: 'Node width' },
  nodeGap: { type: 'number', default: 8, help: 'Gap between nodes' },
  nodeAlign: { type: 'string', default: 'justify', options: ['justify', 'left', 'right'], help: 'Node alignment' },
  layoutIterations: { type: 'number', default: 32, help: 'Layout calculation iterations' },
  orient: { type: 'string', default: 'horizontal', options: ['horizontal', 'vertical'], help: 'Diagram orientation' },
  draggable: { type: 'boolean', default: true, help: 'Enable node dragging' },
  showLabel: { type: 'boolean', default: true, help: 'Show node labels' },
  labelPosition: { type: 'string', default: 'right', options: ['left', 'right', 'top', 'bottom'], help: 'Label position' },
  labelFontSize: { type: 'number', default: 12, help: 'Label font size' },
  labelColor: { type: 'color', default: '#000', help: 'Label color' },
  borderWidth: { type: 'number', default: 1, help: 'Node border width' },
  borderColor: { type: 'color', default: '#aaa', help: 'Node border color' },
  lineColor: { type: 'color', default: 'gradient', help: 'Link line color (gradient/source/target/color)' },
  lineOpacity: { type: 'number', default: 0.2, help: 'Link line opacity (0-1)' },
  curveness: { type: 'number', default: 0.5, help: 'Link line curvature (0-1)' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '600px', help: 'Chart height' }
};


SankeyChart.dataFormat = {
  description: 'Sankey chart data structure',
  structure: `nodes: [{ name: 'Node Name' }, ...]
    links: [{ source: 'Node1', target: 'Node2', value: number }, ...]`,
  example: `const data = {
 *   nodes: [{ name: 'A' }, { name: 'B' }],
 *   links: [{ source: 'A', target: 'B', value: 100 }]
 * };`
};


SankeyChart.dataFormat = {
  description: 'Sankey chart data structure',
  structure: `nodes: [{ name: 'Node Name' }, ...]
    links: [{ source: 'Node1', target: 'Node2', value: number }, ...]`,
  example: `const data = {
 *   nodes: [{ name: 'A' }, { name: 'B' }],
 *   links: [{ source: 'A', target: 'B', value: 100 }]
 * };`
};

export default SankeyChart;
