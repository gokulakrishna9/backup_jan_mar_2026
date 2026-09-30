import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * FunnelChart Component
 * A React wrapper for Apache ECharts Funnel Chart
 * 
 * Funnel charts visualize stages in a linear process where values decrease at each stage. Commonly used for sales pipelines, conversion funnels, recruitment processes, or any sequential workflow where quantities diminish through stages.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * data: [
      { value: number, name: 'Stage Name' },
      ...
    ]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = [
 *   { value: 100, name: 'Visits' },
 *   { value: 80, name: 'Inquiries' },
 *   { value: 50, name: 'Orders' }
 * ];
 */
const FunnelChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Funnel Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        trigger: 'item',
        formatter: config.tooltipFormatter || '{a} <br/>{b}: {c}'
      },
      legend: {
        data: config.legendData || data.map(item => item.name),
        top: config.legendTop || 'bottom'
      },
      series: [
        {
          name: config.seriesName || 'Funnel',
          type: 'funnel',
          left: config.left || '10%',
          top: config.top || '15%',
          bottom: config.bottom || '10%',
          width: config.funnelWidth || '80%',
          min: config.min || 0,
          max: config.max || 100,
          minSize: config.minSize || '0%',
          maxSize: config.maxSize || '100%',
          sort: config.sort || 'descending',
          gap: config.gap || 2,
          label: {
            show: config.showLabel !== undefined ? config.showLabel : true,
            position: config.labelPosition || 'inside',
            formatter: config.labelFormatter || '{b}: {c}'
          },
          labelLine: {
            length: config.labelLineLength || 10,
            lineStyle: {
              width: 1,
              type: 'solid'
            }
          },
          itemStyle: {
            borderColor: config.borderColor || '#fff',
            borderWidth: config.borderWidth || 1
          },
          emphasis: {
            label: {
              fontSize: config.emphasisFontSize || 20
            }
          },
          data: data
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

FunnelChart.configOptions = {
  title: { type: 'string', default: 'Funnel Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  tooltipFormatter: { type: 'string', default: '{a} <br/>{b}: {c}', help: 'Tooltip format' },
  legendData: { type: 'array', default: [], help: 'Legend items' },
  legendTop: { type: 'string', default: 'bottom', help: 'Legend position' },
  seriesName: { type: 'string', default: 'Funnel', help: 'Series name' },
  left: { type: 'string', default: '10%', help: 'Funnel left position' },
  top: { type: 'string', default: '15%', help: 'Funnel top position' },
  bottom: { type: 'string', default: '10%', help: 'Funnel bottom position' },
  funnelWidth: { type: 'string', default: '80%', help: 'Funnel width' },
  min: { type: 'number', default: 0, help: 'Minimum data value' },
  max: { type: 'number', default: 100, help: 'Maximum data value' },
  minSize: { type: 'string', default: '0%', help: 'Minimum funnel size' },
  maxSize: { type: 'string', default: '100%', help: 'Maximum funnel size' },
  sort: { type: 'string', default: 'descending', options: ['descending', 'ascending', 'none'], help: 'Sort order' },
  gap: { type: 'number', default: 2, help: 'Gap between funnel sections' },
  showLabel: { type: 'boolean', default: true, help: 'Show labels' },
  labelPosition: { type: 'string', default: 'inside', options: ['inside', 'outside', 'left', 'right'], help: 'Label position' },
  labelFormatter: { type: 'string', default: '{b}: {c}', help: 'Label format' },
  labelLineLength: { type: 'number', default: 10, help: 'Label line length' },
  borderColor: { type: 'color', default: '#fff', help: 'Border color' },
  borderWidth: { type: 'number', default: 1, help: 'Border width' },
  emphasisFontSize: { type: 'number', default: 20, help: 'Font size on hover' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};


FunnelChart.dataFormat = {
  description: 'Funnel chart data structure',
  structure: `data: [
      { value: number, name: 'Stage Name' },
      ...
    ]`,
  example: `const data = [
 *   { value: 100, name: 'Visits' },
 *   { value: 80, name: 'Inquiries' },
 *   { value: 50, name: 'Orders' }
 * ];`
};


FunnelChart.dataFormat = {
  description: 'Funnel chart data structure',
  structure: `data: [
      { value: number, name: 'Stage Name' },
      ...
    ]`,
  example: `const data = [
 *   { value: 100, name: 'Visits' },
 *   { value: 80, name: 'Inquiries' },
 *   { value: 50, name: 'Orders' }
 * ];`
};

export default FunnelChart;
