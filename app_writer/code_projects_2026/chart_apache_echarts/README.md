# Apache ECharts React Wrappers

React wrapper components for Apache ECharts with simplified data and configuration props.

## Installation

```bash
npm install echarts react
```

## Components

All components accept two props:
- `data`: Chart data
- `config`: Chart configuration (styles, size, transformations, etc.)

### Available Charts

1. **LineChart** - Line series visualization
2. **BarChart** - Bar series visualization
3. **PieChart** - Pie/Donut charts
4. **ScatterChart** - Scatter plot visualization
5. **RadarChart** - Radar/Spider charts
6. **FunnelChart** - Funnel visualization
7. **GaugeChart** - Gauge/Meter charts
8. **HeatmapChart** - Heatmap visualization
9. **CandlestickChart** - Financial candlestick charts
10. **TreemapChart** - Hierarchical treemap
11. **SunburstChart** - Hierarchical sunburst
12. **BoxplotChart** - Statistical boxplot

## Usage Examples

### LineChart

```jsx
import { LineChart } from 'apache-echarts-react-wrappers';

const data = {
  xAxis: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
  series: [
    {
      name: 'Sales',
      data: [120, 200, 150, 80, 70],
      color: '#5470c6'
    }
  ]
};

const config = {
  title: 'Weekly Sales',
  smooth: true,
  showArea: true,
  height: '500px'
};

<LineChart data={data} config={config} />
```

### BarChart

```jsx
import { BarChart } from 'apache-echarts-react-wrappers';

const data = {
  xAxis: ['Q1', 'Q2', 'Q3', 'Q4'],
  series: [
    {
      name: 'Revenue',
      data: [2000, 3000, 2500, 4000]
    }
  ]
};

const config = {
  title: 'Quarterly Revenue',
  barColor: '#91cc75',
  showLabel: true
};

<BarChart data={data} config={config} />
```

### PieChart

```jsx
import { PieChart } from 'apache-echarts-react-wrappers';

const data = [
  { value: 1048, name: 'Search Engine' },
  { value: 735, name: 'Direct' },
  { value: 580, name: 'Email' },
  { value: 484, name: 'Union Ads' }
];

const config = {
  title: 'Traffic Sources',
  radius: ['40%', '70%'], // Donut chart
  roseType: 'radius'
};

<PieChart data={data} config={config} />
```

### ScatterChart

```jsx
import { ScatterChart } from 'apache-echarts-react-wrappers';

const data = {
  series: [
    {
      name: 'Dataset 1',
      data: [[10, 20], [15, 25], [20, 30]],
      color: '#ee6666'
    }
  ]
};

const config = {
  title: 'Scatter Analysis',
  xAxisName: 'X Value',
  yAxisName: 'Y Value',
  symbolSize: 15
};

<ScatterChart data={data} config={config} />
```

### RadarChart

```jsx
import { RadarChart } from 'apache-echarts-react-wrappers';

const data = {
  indicator: [
    { name: 'Sales', max: 100 },
    { name: 'Marketing', max: 100 },
    { name: 'Development', max: 100 },
    { name: 'Support', max: 100 }
  ],
  series: [
    {
      name: 'Team A',
      value: [80, 90, 70, 85],
      color: '#5470c6'
    }
  ]
};

const config = {
  title: 'Team Performance',
  shape: 'polygon'
};

<RadarChart data={data} config={config} />
```

### GaugeChart

```jsx
import { GaugeChart } from 'apache-echarts-react-wrappers';

const data = {
  value: 75,
  name: 'Progress'
};

const config = {
  title: 'Project Progress',
  min: 0,
  max: 100
};

<GaugeChart data={data} config={config} />
```

### HeatmapChart

```jsx
import { HeatmapChart } from 'apache-echarts-react-wrappers';

const data = {
  xAxis: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
  yAxis: ['Morning', 'Afternoon', 'Evening'],
  data: [
    [0, 0, 5], [0, 1, 1], [0, 2, 0],
    [1, 0, 1], [1, 1, 15], [1, 2, 0]
  ]
};

const config = {
  title: 'Activity Heatmap',
  colorRange: ['#313695', '#fee090', '#a50026']
};

<HeatmapChart data={data} config={config} />
```

## Configuration Options

Each component has a `configOptions` static property that documents all available configuration options with:
- Type
- Default value
- Available options (for enums)
- Help text

Access it like:

```javascript
console.log(LineChart.configOptions);
```

## Common Configuration Properties

Most charts support these common config properties:

- `title`: Chart title
- `titleAlign`: Title alignment ('left', 'center', 'right')
- `titleFontSize`: Title font size
- `titleColor`: Title color
- `width`: Chart width (default: '100%')
- `height`: Chart height (default: '400px')
- `legendTop`: Legend position
- `gridLeft`, `gridRight`, `gridTop`, `gridBottom`: Grid margins

## Data Formats

### Line/Bar Charts
```javascript
{
  xAxis: ['Category1', 'Category2', ...],
  series: [
    {
      name: 'Series Name',
      data: [value1, value2, ...],
      color: '#color' // optional
    }
  ]
}
```

### Pie Chart
```javascript
[
  { value: number, name: 'Label' },
  ...
]
```

### Scatter Chart
```javascript
{
  series: [
    {
      name: 'Series Name',
      data: [[x1, y1], [x2, y2], ...] // or [[x, y, size], ...]
    }
  ]
}
```

### Radar Chart
```javascript
{
  indicator: [
    { name: 'Metric', max: maxValue },
    ...
  ],
  series: [
    {
      name: 'Series Name',
      value: [value1, value2, ...]
    }
  ]
}
```

### Heatmap
```javascript
{
  xAxis: ['X1', 'X2', ...],
  yAxis: ['Y1', 'Y2', ...],
  data: [[xIndex, yIndex, value], ...]
}
```

## License

MIT

## Credits

Built on top of [Apache ECharts](https://echarts.apache.org/)
