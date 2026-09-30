import React, { useEffect, useRef } from 'react';
import * as echarts from 'echarts';

/**
 * CandlestickChart Component
 * A React wrapper for Apache ECharts Candlestick Chart
 * 
 * Candlestick charts display financial data showing open, high, low, and close values for each time period. Essential for stock market analysis, forex trading, and any financial time series requiring OHLC data visualization.
 * 
 * @param {Object} data - Chart data
 * Data structure:
 * xAxis: ['Date1', 'Date2', ...]
    data: [[open, close, low, high], ...]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = {
 *   xAxis: ['2024-01', '2024-02'],
 *   data: [[20, 34, 10, 38], [40, 35, 30, 50]]
 * };
 */
const CandlestickChart = ({ data, config = {} }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (!chartRef.current) return;

    chartInstance.current = echarts.init(chartRef.current);

    const option = {
      title: {
        text: config.title || 'Candlestick Chart',
        left: config.titleAlign || 'center',
        textStyle: {
          fontSize: config.titleFontSize || 18,
          color: config.titleColor || '#333'
        }
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross'
        }
      },
      legend: {
        data: config.legendData || ['Candlestick'],
        top: config.legendTop || 'bottom'
      },
      grid: {
        left: config.gridLeft || '10%',
        right: config.gridRight || '10%',
        bottom: config.gridBottom || '15%',
        top: config.gridTop || '15%'
      },
      xAxis: {
        type: 'category',
        data: data.xAxis || [],
        boundaryGap: true,
        axisLine: { onZero: false },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax'
      },
      yAxis: {
        scale: true,
        splitArea: {
          show: config.showSplitArea !== undefined ? config.showSplitArea : true
        }
      },
      dataZoom: [
        {
          type: config.dataZoomType || 'inside',
          start: config.dataZoomStart || 50,
          end: config.dataZoomEnd || 100
        },
        {
          show: config.showDataZoomSlider !== undefined ? config.showDataZoomSlider : true,
          type: 'slider',
          top: '90%',
          start: config.dataZoomStart || 50,
          end: config.dataZoomEnd || 100
        }
      ],
      series: [
        {
          name: config.seriesName || 'Candlestick',
          type: 'candlestick',
          data: data.data || [],
          itemStyle: {
            color: config.upColor || '#ec0000',
            color0: config.downColor || '#00da3c',
            borderColor: config.upBorderColor || '#8A0000',
            borderColor0: config.downBorderColor || '#008F28'
          },
          barWidth: config.barWidth || 'auto',
          barMaxWidth: config.barMaxWidth || 10
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

CandlestickChart.configOptions = {
  title: { type: 'string', default: 'Candlestick Chart', help: 'Chart title' },
  titleAlign: { type: 'string', default: 'center', options: ['left', 'center', 'right'], help: 'Title alignment' },
  titleFontSize: { type: 'number', default: 18, help: 'Title font size' },
  titleColor: { type: 'color', default: '#333', help: 'Title color' },
  legendData: { type: 'array', default: ['Candlestick'], help: 'Legend items' },
  legendTop: { type: 'string', default: 'bottom', help: 'Legend position' },
  gridLeft: { type: 'string', default: '10%', help: 'Grid left margin' },
  gridRight: { type: 'string', default: '10%', help: 'Grid right margin' },
  gridBottom: { type: 'string', default: '15%', help: 'Grid bottom margin' },
  gridTop: { type: 'string', default: '15%', help: 'Grid top margin' },
  showSplitArea: { type: 'boolean', default: true, help: 'Show Y-axis split area' },
  dataZoomType: { type: 'string', default: 'inside', options: ['inside', 'slider'], help: 'Data zoom type' },
  dataZoomStart: { type: 'number', default: 50, help: 'Data zoom start percentage' },
  dataZoomEnd: { type: 'number', default: 100, help: 'Data zoom end percentage' },
  showDataZoomSlider: { type: 'boolean', default: true, help: 'Show data zoom slider' },
  seriesName: { type: 'string', default: 'Candlestick', help: 'Series name' },
  upColor: { type: 'color', default: '#ec0000', help: 'Up candle color' },
  downColor: { type: 'color', default: '#00da3c', help: 'Down candle color' },
  upBorderColor: { type: 'color', default: '#8A0000', help: 'Up candle border color' },
  downBorderColor: { type: 'color', default: '#008F28', help: 'Down candle border color' },
  barWidth: { type: 'string', default: 'auto', help: 'Candle width' },
  barMaxWidth: { type: 'number', default: 10, help: 'Maximum candle width' },
  width: { type: 'string', default: '100%', help: 'Chart width' },
  height: { type: 'string', default: '400px', help: 'Chart height' }
};


CandlestickChart.dataFormat = {
  description: 'Candlestick chart data structure',
  structure: `xAxis: ['Date1', 'Date2', ...]
    data: [[open, close, low, high], ...]`,
  example: `const data = {
 *   xAxis: ['2024-01', '2024-02'],
 *   data: [[20, 34, 10, 38], [40, 35, 30, 50]]
 * };`
};


CandlestickChart.dataFormat = {
  description: 'Candlestick chart data structure',
  structure: `xAxis: ['Date1', 'Date2', ...]
    data: [[open, close, low, high], ...]`,
  example: `const data = {
 *   xAxis: ['2024-01', '2024-02'],
 *   data: [[20, 34, 10, 38], [40, 35, 30, 50]]
 * };`
};

export default CandlestickChart;
