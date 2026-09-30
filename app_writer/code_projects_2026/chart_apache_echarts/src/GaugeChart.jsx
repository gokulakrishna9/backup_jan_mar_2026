import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * GaugeChart Component
 * A React wrapper for Apache ECharts Gauge Chart
 * 
 * Gauge charts display a single value within a range, resembling a speedometer or meter. Perfect for showing KPIs, progress toward goals, performance metrics, or any measurement that needs context within min/max bounds.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * data: {
      value: number,
      name: 'Label' (optional)
    }
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = { value: 75, name: 'Progress' };
 * const config = { title: 'Project Progress', min: 0, max: 100 };
 */
const GaugeChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Gauge Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      series: [
        {
          type: 'gauge',
          center: config.center || ['50%', '60%'],
          radius: config.radius || '75%',
          startAngle: config.startAngle || 225,
          endAngle: config.endAngle || -45,
          min: config.min || 0,
          max: config.max || 100,
          splitNumber: config.splitNumber || 10,
          axisLine: {
            lineStyle: {
              width: config.axisLineWidth || 30,
              color: config.axisLineColor || [
                [0.3, '#67e0e3'],
                [0.7, '#37a2da'],
                [1, '#fd666d']
              ]
            }
          },
          pointer: {
            itemStyle: {
              color: config.pointerColor || 'auto'
            },
            width: config.pointerWidth || 8,
            length: config.pointerLength || '80%'
          },
          axisTick: {
            distance: config.axisTickDistance || -30,
            length: config.axisTickLength || 8,
            lineStyle: {
              color: config.axisTickColor || '#fff',
              width: 2
            }
          },
          splitLine: {
            distance: config.splitLineDistance || -30,
            length: config.splitLineLength || 30,
            lineStyle: {
              color: config.splitLineColor || '#fff',
              width: 4
            }
          },
          axisLabel: {
            color: config.axisLabelColor || 'inherit',
            distance: config.axisLabelDistance || 40,
            fontSize: config.axisLabelFontSize || 12
          },
          detail: {
            valueAnimation: config.valueAnimation !== undefined ? config.valueAnimation : true,
            formatter: config.detailFormatter || '{value}',
            color: config.detailColor || 'inherit',
            fontSize: config.detailFontSize || 30,
            offsetCenter: config.detailOffsetCenter || [0, '70%']
          },
          data: [
            {
              value: data.value || 0,
              name: data.name || ''
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

GaugeChart.configOptions = {
  title: { type: 'string', default: 'Gauge Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  center: { type: 'array', default: ['50%', '60%'], help: 'Gauge center [x, y]' },
  radius: { type: 'string', default: '75%', help: 'Gauge radius' },
  startAngle: { type: 'number', default: 225, help: 'Start angle (degrees)' },
  endAngle: { type: 'number', default: -45, help: 'End angle (degrees)' },
  min: { type: 'number', default: 0, help: 'Minimum value' },
  max: { type: 'number', default: 100, help: 'Maximum value' },
  splitNumber: { type: 'number', default: 10, help: 'Number of split segments' },
  axisLineWidth: { type: 'number', default: 30, help: 'Axis line width' },
  axisLineColor: { type: 'array', default: [[0.3, '#67e0e3'], [0.7, '#37a2da'], [1, '#fd666d']], help: 'Axis line color gradient [[position, color], ...]' },
  pointerColor: { type: 'string', default: 'auto', help: 'Pointer color' },
  pointerWidth: { type: 'number', default: 8, help: 'Pointer width' },
  pointerLength: { type: 'string', default: '80%', help: 'Pointer length' },
  axisTickDistance: { type: 'number', default: -30, help: 'Axis tick distance from axis line' },
  axisTickLength: { type: 'number', default: 8, help: 'Axis tick length' },
  axisTickColor: { type: 'color', default: '#fff', help: 'Axis tick color' },
  splitLineDistance: { type: 'number', default: -30, help: 'Split line distance from axis line' },
  splitLineLength: { type: 'number', default: 30, help: 'Split line length' },
  splitLineColor: { type: 'color', default: '#fff', help: 'Split line color' },
  axisLabelColor: { type: 'string', default: 'inherit', help: 'Axis label color' },
  axisLabelDistance: { type: 'number', default: 40, help: 'Axis label distance' },
  axisLabelFontSize: { type: 'number', default: 12, help: 'Axis label font size' },
  valueAnimation: { type: 'boolean', default: true, help: 'Enable value animation' },
  detailFormatter: { type: 'string', default: '{value}', help: 'Detail value format' },
  detailColor: { type: 'string', default: 'inherit', help: 'Detail text color' },
  detailFontSize: { type: 'number', default: 30, help: 'Detail font size' },
  detailOffsetCenter: { type: 'array', default: [0, '70%'], help: 'Detail offset from center [x, y]' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};


GaugeChart.dataFormat = {
  description: 'Gauge chart data structure',
  structure: `data: {
      value: number,
      name: 'Label' (optional)
    }`,
  example: `const data = { value: 75, name: 'Progress' };
 * const config = { title: 'Project Progress', min: 0, max: 100 };`
};


GaugeChart.dataFormat = {
  description: 'Gauge chart data structure',
  structure: `data: {
      value: number,
      name: 'Label' (optional)
    }`,
  example: `const data = { value: 75, name: 'Progress' };
 * const config = { title: 'Project Progress', min: 0, max: 100 };`
};

export default GaugeChart;
