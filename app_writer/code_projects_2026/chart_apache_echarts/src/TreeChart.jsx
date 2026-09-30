import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * TreeChart Component
 * A React wrapper for Apache ECharts Tree Chart
 * 
 * Tree diagrams display hierarchical data in a branching structure. Nodes can be expanded/collapsed, making them perfect for organizational charts, file systems, taxonomies, or any parent-child relationships.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * data: {
      name: 'Root',
      children: [
        { name: 'Child', value: number, children: [...] }
      ]
    }
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   name: 'CEO',
 *   children: [
 *     { name: 'CTO', children: [{ name: 'Dev Lead' }] }
 *   ]
 * };
 */
const TreeChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Tree Diagram',
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
          type: 'tree',
          data: [data],
          left: config.left || '2%',
          right: config.right || '2%',
          top: config.top || '15%',
          bottom: config.bottom || '2%',
          symbol: config.symbol || 'emptyCircle',
          symbolSize: config.symbolSize || 7,
          orient: config.orient || 'LR',
          expandAndCollapse: config.expandAndCollapse !== undefined ? config.expandAndCollapse : true,
          initialTreeDepth: config.initialTreeDepth || -1,
          animationDuration: config.animationDuration || 550,
          animationDurationUpdate: config.animationDurationUpdate || 750,
          label: {
            show: config.showLabel !== undefined ? config.showLabel : true,
            position: config.labelPosition || 'left',
            verticalAlign: config.labelVerticalAlign || 'middle',
            align: config.labelAlign || 'right',
            fontSize: config.labelFontSize || 12,
            color: config.labelColor || '#000'
          },
          leaves: {
            label: {
              position: config.leavesLabelPosition || 'right',
              verticalAlign: config.leavesLabelVerticalAlign || 'middle',
              align: config.leavesLabelAlign || 'left'
            }
          },
          emphasis: {
            focus: 'descendant'
          },
          lineStyle: {
            color: config.lineColor || '#ccc',
            width: config.lineWidth || 1.5,
            curveness: config.curveness || 0.5
          },
          itemStyle: {
            color: config.nodeColor || '#5470c6',
            borderColor: config.nodeBorderColor || '#fff',
            borderWidth: config.nodeBorderWidth || 2
          },
          roam: config.roam !== undefined ? config.roam : true,
          layout: config.layout || 'orthogonal'
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

TreeChart.configOptions = {
  title: { type: 'string', default: 'Tree Diagram', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  left: { type: 'string', default: '2%', help: 'Tree left position' },
  right: { type: 'string', default: '2%', help: 'Tree right position' },
  top: { type: 'string', default: '15%', help: 'Tree top position' },
  bottom: { type: 'string', default: '2%', help: 'Tree bottom position' },
  symbol: { type: 'string', default: 'emptyCircle', options: ['circle', 'emptyCircle', 'rect', 'roundRect', 'triangle', 'diamond'], help: 'Node symbol' },
  symbolSize: { type: 'number', default: 7, help: 'Node size' },
  orient: { type: 'string', default: 'LR', options: ['LR', 'RL', 'TB', 'BT'], help: 'Tree orientation (LR=left-right, TB=top-bottom)' },
  expandAndCollapse: { type: 'boolean', default: true, help: 'Enable expand/collapse' },
  initialTreeDepth: { type: 'number', default: -1, help: 'Initial tree depth (-1 = all)' },
  animationDuration: { type: 'number', default: 550, help: 'Animation duration (ms)' },
  animationDurationUpdate: { type: 'number', default: 750, help: 'Update animation duration (ms)' },
  showLabel: { type: 'boolean', default: true, help: 'Show node labels' },
  labelPosition: { type: 'string', default: 'left', options: ['left', 'right', 'top', 'bottom'], help: 'Label position' },
  labelVerticalAlign: { type: 'string', default: 'middle', options: ['top', 'middle', 'bottom'], help: 'Label vertical alignment' },
  labelAlign: { type: 'string', default: 'right', options: ['left', 'center', 'right'], help: 'Label horizontal alignment' },
  labelFontSize: { type: 'number', default: 12, help: 'Label font size' },
  labelColor: { type: 'color', default: '#000', help: 'Label color' },
  leavesLabelPosition: { type: 'string', default: 'right', options: ['left', 'right', 'top', 'bottom'], help: 'Leaf label position' },
  leavesLabelVerticalAlign: { type: 'string', default: 'middle', options: ['top', 'middle', 'bottom'], help: 'Leaf label vertical alignment' },
  leavesLabelAlign: { type: 'string', default: 'left', options: ['left', 'center', 'right'], help: 'Leaf label horizontal alignment' },
  lineColor: { type: 'color', default: '#ccc', help: 'Edge line color' },
  lineWidth: { type: 'number', default: 1.5, help: 'Edge line width' },
  curveness: { type: 'number', default: 0.5, help: 'Edge line curvature (0-1)' },
  nodeColor: { type: 'color', default: '#5470c6', help: 'Node color' },
  nodeBorderColor: { type: 'color', default: '#fff', help: 'Node border color' },
  nodeBorderWidth: { type: 'number', default: 2, help: 'Node border width' },
  roam: { type: 'boolean', default: true, help: 'Enable pan and zoom' },
  layout: { type: 'string', default: 'orthogonal', options: ['orthogonal', 'radial'], help: 'Tree layout type' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '600px', help: 'Chart height' }
};


TreeChart.dataFormat = {
  description: 'Tree chart data structure',
  structure: `data: {
      name: 'Root',
      children: [
        { name: 'Child', value: number, children: [...] }
      ]
    }`,
  example: `const data = {
 *   name: 'CEO',
 *   children: [
 *     { name: 'CTO', children: [{ name: 'Dev Lead' }] }
 *   ]
 * };`
};


TreeChart.dataFormat = {
  description: 'Tree chart data structure',
  structure: `data: {
      name: 'Root',
      children: [
        { name: 'Child', value: number, children: [...] }
      ]
    }`,
  example: `const data = {
 *   name: 'CEO',
 *   children: [
 *     { name: 'CTO', children: [{ name: 'Dev Lead' }] }
 *   ]
 * };`
};

export default TreeChart;
