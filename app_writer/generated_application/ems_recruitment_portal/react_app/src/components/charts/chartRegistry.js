import BarChart from './BarChart';
import LineChart from './LineChart';
import AreaChart from './AreaChart';
import PieChart from './PieChart';
import DonutChart from './DonutChart';
import ScatterChart from './ScatterChart';
import BubbleChart from './BubbleChart';
import RadarChart from './RadarChart';
import HeatmapChart from './HeatmapChart';
import TreemapChart from './TreemapChart';
import FunnelChart from './FunnelChart';
import GaugeChart from './GaugeChart';
import CandlestickChart from './CandlestickChart';
import BoxplotChart from './BoxplotChart';
import SankeyChart from './SankeyChart';
import SunburstChart from './SunburstChart';
import HistogramChart from './HistogramChart';
import ParallelChart from './ParallelChart';
import PictorialBarChart from './PictorialBarChart';


const chartRegistry = {
  'bar': BarChart,
  'line': LineChart,
  'area': AreaChart,
  'pie': PieChart,
  'donut': DonutChart,
  'scatter': ScatterChart,
  'bubble': BubbleChart,
  'radar': RadarChart,
  'heatmap': HeatmapChart,
  'treemap': TreemapChart,
  'funnel': FunnelChart,
  'gauge': GaugeChart,
  'candlestick': CandlestickChart,
  'boxplot': BoxplotChart,
  'sankey': SankeyChart,
  'sunburst': SunburstChart,
  'histogram': HistogramChart,
  'parallel': ParallelChart,
  'pictorialBar': PictorialBarChart,
};

export default chartRegistry;