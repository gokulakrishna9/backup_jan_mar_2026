import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * CalendarChart Component
 * A React wrapper for Apache ECharts Calendar Chart
 * 
 * Calendar charts display data in a calendar format where each day is a cell colored by value. Perfect for showing daily patterns, activity tracking, contribution graphs (like GitHub), or any time-series data with daily granularity.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * data: [
      ['YYYY-MM-DD', value],
      ...
    ]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = [
 *   ['2024-01-01', 100],
 *   ['2024-01-02', 150],
 *   ['2024-01-03', 80]
 * ];
 */
const CalendarChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Calendar Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        position: 'top',
        formatter: config.tooltipFormatter || function(p) {
          return p.data[0] + ': ' + p.data[1];
        }
      },
      visualMap: config.showVisualMap !== undefined && config.showVisualMap ? {
        min: config.visualMapMin || 0,
        max: config.visualMapMax || 1000,
        calculable: true,
        orient: config.visualMapOrient || 'horizontal',
        left: config.visualMapLeft || 'center',
        top: config.visualMapTop || 'top',
        inRange: {
          color: config.visualMapColors || ['#ebedf0', '#c6e48b', '#7bc96f', '#239a3b', '#196127']
        }
      } : undefined,
      calendar: {
        top: config.calendarTop || 120,
        left: config.calendarLeft || 30,
        right: config.calendarRight || 30,
        cellSize: config.cellSize || ['auto', 13],
        range: config.range || new Date().getFullYear(),
        itemStyle: {
          borderWidth: config.borderWidth || 0.5,
          borderColor: config.borderColor || '#fff'
        },
        yearLabel: {
          show: config.showYearLabel !== undefined ? config.showYearLabel : true,
          fontSize: config.yearLabelFontSize || 30
        },
        dayLabel: {
          firstDay: config.firstDay || 0,
          nameMap: config.dayNameMap || 'en',
          fontSize: config.dayLabelFontSize || 12
        },
        monthLabel: {
          show: config.showMonthLabel !== undefined ? config.showMonthLabel : true,
          nameMap: config.monthNameMap || 'en',
          fontSize: config.monthLabelFontSize || 12
        },
        splitLine: {
          show: config.showSplitLine !== undefined ? config.showSplitLine : true,
          lineStyle: {
            color: config.splitLineColor || '#000',
            width: config.splitLineWidth || 1,
            type: config.splitLineType || 'solid'
          }
        }
      },
      series: [
        {
          type: 'heatmap',
          coordinateSystem: 'calendar',
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
        height: config.height || '400px' 
      }} 
    />
  );
};

CalendarChart.configOptions = {
  title: { type: 'string', default: 'Calendar Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  tooltipFormatter: { type: 'function', default: null, help: 'Tooltip formatter function' },
  showVisualMap: { type: 'boolean', default: false, help: 'Show visual map' },
  visualMapMin: { type: 'number', default: 0, help: 'Visual map minimum' },
  visualMapMax: { type: 'number', default: 1000, help: 'Visual map maximum' },
  visualMapOrient: { type: 'string', default: 'horizontal', options: ['horizontal', 'vertical'], help: 'Visual map orientation' },
  visualMapLeft: { type: 'string', default: 'center', help: 'Visual map horizontal position' },
  visualMapTop: { type: 'string', default: 'top', help: 'Visual map vertical position' },
  visualMapColors: { type: 'array', default: ['#ebedf0', '#c6e48b', '#7bc96f', '#239a3b', '#196127'], help: 'Visual map color range' },
  calendarTop: { type: 'number', default: 120, help: 'Calendar top position' },
  calendarLeft: { type: 'number', default: 30, help: 'Calendar left position' },
  calendarRight: { type: 'number', default: 30, help: 'Calendar right position' },
  cellSize: { type: 'array', default: ['auto', 13], help: 'Cell size [width, height]' },
  range: { type: 'string|number|array', default: 'current year', help: 'Calendar range (year or [start, end])' },
  borderWidth: { type: 'number', default: 0.5, help: 'Cell border width' },
  borderColor: { type: 'color', default: '#fff', help: 'Cell border color' },
  showYearLabel: { type: 'boolean', default: true, help: 'Show year label' },
  yearLabelFontSize: { type: 'number', default: 30, help: 'Year label font size' },
  firstDay: { type: 'number', default: 0, options: [0, 1, 2, 3, 4, 5, 6], help: 'First day of week (0=Sunday)' },
  dayNameMap: { type: 'string|array', default: 'en', help: 'Day name mapping' },
  dayLabelFontSize: { type: 'number', default: 12, help: 'Day label font size' },
  showMonthLabel: { type: 'boolean', default: true, help: 'Show month labels' },
  monthNameMap: { type: 'string|array', default: 'en', help: 'Month name mapping' },
  monthLabelFontSize: { type: 'number', default: 12, help: 'Month label font size' },
  showSplitLine: { type: 'boolean', default: true, help: 'Show split lines' },
  splitLineColor: { type: 'color', default: '#000', help: 'Split line color' },
  splitLineWidth: { type: 'number', default: 1, help: 'Split line width' },
  splitLineType: { type: 'string', default: 'solid', options: ['solid', 'dashed', 'dotted'], help: 'Split line type' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};


CalendarChart.dataFormat = {
  description: 'Calendar chart data structure',
  structure: `data: [
      ['YYYY-MM-DD', value],
      ...
    ]`,
  example: `const data = [
 *   ['2024-01-01', 100],
 *   ['2024-01-02', 150],
 *   ['2024-01-03', 80]
 * ];`
};


CalendarChart.dataFormat = {
  description: 'Calendar chart data structure',
  structure: `data: [
      ['YYYY-MM-DD', value],
      ...
    ]`,
  example: `const data = [
 *   ['2024-01-01', 100],
 *   ['2024-01-02', 150],
 *   ['2024-01-03', 80]
 * ];`
};

export default CalendarChart;
