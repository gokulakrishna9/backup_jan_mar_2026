"""
Script to add comprehensive documentation to all ECharts React wrapper components.
Adds JSDoc comments, data format descriptions, and changes color properties to type: 'color'.
"""

import os
import re
from pathlib import Path

# Chart descriptions and data formats
CHART_INFO = {
    'ScatterChart': {
        'description': 'Scatter charts display data as points in a 2D coordinate system. Each point represents two variables, making them ideal for showing correlations, distributions, and clusters. Useful for analyzing relationships between variables, identifying outliers, and visualizing data density.',
        'data_structure': '''xAxis: ['Category1', 'Category2', ...] (optional for value axis)
    series: [
      {
        name: 'Series Name',
        data: [[x1, y1], [x2, y2], ...] or [[x, y, size], ...],
        color: '#color' (optional)
      }
    ]''',
        'example': '''const data = {
 *   series: [
 *     { 
 *       name: 'Dataset 1', 
 *       data: [[10, 20], [15, 25], [20, 30]], 
 *       color: '#ee6666' 
 *     }
 *   ]
 * };
 * const config = { title: 'Scatter Analysis', symbolSize: 15 };'''
    },
    'RadarChart': {
        'description': 'Radar charts (spider/web charts) display multivariate data on axes starting from the same point. Each axis represents a different variable, making them perfect for comparing multiple characteristics across items, showing strengths/weaknesses, or displaying performance metrics.',
        'data_structure': '''indicator: [{ name: 'Metric', max: maxValue }, ...]
    series: [
      {
        name: 'Series Name',
        value: [value1, value2, ...],
        color: '#color' (optional)
      }
    ]''',
        'example': '''const data = {
 *   indicator: [
 *     { name: 'Sales', max: 100 },
 *     { name: 'Marketing', max: 100 }
 *   ],
 *   series: [{ name: 'Team A', value: [80, 90], color: '#5470c6' }]
 * };'''
    },
    'FunnelChart': {
        'description': 'Funnel charts visualize stages in a linear process where values decrease at each stage. Commonly used for sales pipelines, conversion funnels, recruitment processes, or any sequential workflow where quantities diminish through stages.',
        'data_structure': '''data: [
      { value: number, name: 'Stage Name' },
      ...
    ]''',
        'example': '''const data = [
 *   { value: 100, name: 'Visits' },
 *   { value: 80, name: 'Inquiries' },
 *   { value: 50, name: 'Orders' }
 * ];'''
    },
    'GaugeChart': {
        'description': 'Gauge charts display a single value within a range, resembling a speedometer or meter. Perfect for showing KPIs, progress toward goals, performance metrics, or any measurement that needs context within min/max bounds.',
        'data_structure': '''data: {
      value: number,
      name: 'Label' (optional)
    }''',
        'example': '''const data = { value: 75, name: 'Progress' };
 * const config = { title: 'Project Progress', min: 0, max: 100 };'''
    },
    'HeatmapChart': {
        'description': 'Heatmaps use color intensity to represent data values in a matrix format. Ideal for showing patterns, correlations, time-based activity, geographic data density, or any 2D data distribution where color indicates magnitude.',
        'data_structure': '''xAxis: ['X1', 'X2', ...]
    yAxis: ['Y1', 'Y2', ...]
    data: [[xIndex, yIndex, value], ...]''',
        'example': '''const data = {
 *   xAxis: ['Mon', 'Tue', 'Wed'],
 *   yAxis: ['Morning', 'Afternoon'],
 *   data: [[0, 0, 5], [0, 1, 1], [1, 0, 15]]
 * };'''
    },
    'CandlestickChart': {
        'description': 'Candlestick charts display financial data showing open, high, low, and close values for each time period. Essential for stock market analysis, forex trading, and any financial time series requiring OHLC data visualization.',
        'data_structure': '''xAxis: ['Date1', 'Date2', ...]
    data: [[open, close, low, high], ...]''',
        'example': '''const data = {
 *   xAxis: ['2024-01', '2024-02'],
 *   data: [[20, 34, 10, 38], [40, 35, 30, 50]]
 * };'''
    },
    'TreemapChart': {
        'description': 'Treemaps display hierarchical data as nested rectangles. Rectangle size represents quantitative values, making them ideal for showing proportions within hierarchies, disk space usage, portfolio composition, or organizational structures.',
        'data_structure': '''data: [
      {
        name: 'Parent',
        value: number,
        children: [{ name: 'Child', value: number }, ...]
      }
    ]''',
        'example': '''const data = [{
 *   name: 'Root',
 *   children: [
 *     { name: 'A', value: 100 },
 *     { name: 'B', value: 200 }
 *   ]
 * }];'''
    },
    'SunburstChart': {
        'description': 'Sunburst charts visualize hierarchical data in concentric circles. Each ring represents a level in the hierarchy, with segments sized by value. Perfect for showing multi-level categorizations, file systems, or organizational hierarchies.',
        'data_structure': '''data: {
      name: 'Root',
      children: [
        { name: 'Child', value: number, children: [...] }
      ]
    }''',
        'example': '''const data = {
 *   name: 'Root',
 *   children: [
 *     { name: 'A', value: 100 },
 *     { name: 'B', value: 200, children: [...] }
 *   ]
 * };'''
    },
    'BoxplotChart': {
        'description': 'Boxplot charts (box-and-whisker plots) display statistical distributions showing median, quartiles, and outliers. Essential for statistical analysis, comparing distributions across groups, and identifying data anomalies.',
        'data_structure': '''xAxis: ['Category1', 'Category2', ...]
    boxData: [[min, Q1, median, Q3, max], ...]
    outliers: [[categoryIndex, value], ...]''',
        'example': '''const data = {
 *   xAxis: ['Group A', 'Group B'],
 *   boxData: [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6]],
 *   outliers: [[0, 10], [1, 12]]
 * };'''
    },
    'GraphChart': {
        'description': 'Graph charts (network diagrams) visualize relationships between nodes using edges. Ideal for social networks, dependency graphs, organizational charts, knowledge graphs, or any connected data structure.',
        'data_structure': '''nodes: [{ name: 'Node', value: number, category: index }, ...]
    links: [{ source: 'Node1', target: 'Node2', value: number }, ...]
    categories: [{ name: 'Category' }, ...]''',
        'example': '''const data = {
 *   nodes: [{ name: 'A', value: 10 }, { name: 'B', value: 20 }],
 *   links: [{ source: 'A', target: 'B' }]
 * };'''
    },
    'SankeyChart': {
        'description': 'Sankey diagrams show flow quantities between nodes using proportional link widths. Perfect for visualizing energy flows, material transfers, budget allocations, or any process where quantities flow between stages.',
        'data_structure': '''nodes: [{ name: 'Node Name' }, ...]
    links: [{ source: 'Node1', target: 'Node2', value: number }, ...]''',
        'example': '''const data = {
 *   nodes: [{ name: 'A' }, { name: 'B' }],
 *   links: [{ source: 'A', target: 'B', value: 100 }]
 * };'''
    },
    'ParallelChart': {
        'description': 'Parallel coordinates charts display multivariate data where each variable has its own vertical axis. Lines connect values across axes, making them ideal for comparing multiple dimensions, filtering data, and identifying patterns in high-dimensional datasets.',
        'data_structure': '''parallelAxis: [{ dim: 0, name: 'Axis1' }, ...]
    data: [[value1, value2, value3, ...], ...]''',
        'example': '''const data = {
 *   parallelAxis: [{ dim: 0, name: 'Price' }, { dim: 1, name: 'Size' }],
 *   data: [[12.99, 100], [19.99, 200]]
 * };'''
    },
    'TreeChart': {
        'description': 'Tree diagrams display hierarchical data in a branching structure. Nodes can be expanded/collapsed, making them perfect for organizational charts, file systems, taxonomies, or any parent-child relationships.',
        'data_structure': '''data: {
      name: 'Root',
      children: [
        { name: 'Child', value: number, children: [...] }
      ]
    }''',
        'example': '''const data = {
 *   name: 'CEO',
 *   children: [
 *     { name: 'CTO', children: [{ name: 'Dev Lead' }] }
 *   ]
 * };'''
    },
    'MapChart': {
        'description': 'Map charts display geographic data on maps. Values can be shown through colors, symbols, or other visual encodings. Ideal for regional statistics, location-based data, geographic distributions, or spatial analysis. Requires GeoJSON data registration.',
        'data_structure': '''data: [
      { name: 'Region Name', value: number },
      ...
    ]''',
        'example': '''const data = [
 *   { name: 'California', value: 1000 },
 *   { name: 'Texas', value: 800 }
 * ];
 * // Note: Requires echarts.registerMap('mapName', geoJsonData)'''
    },
    'CalendarChart': {
        'description': 'Calendar charts display data in a calendar format where each day is a cell colored by value. Perfect for showing daily patterns, activity tracking, contribution graphs (like GitHub), or any time-series data with daily granularity.',
        'data_structure': '''data: [
      ['YYYY-MM-DD', value],
      ...
    ]''',
        'example': '''const data = [
 *   ['2024-01-01', 100],
 *   ['2024-01-02', 150],
 *   ['2024-01-03', 80]
 * ];'''
    },
    'ThemeRiverChart': {
        'description': 'ThemeRiver charts show temporal changes in multiple categories using flowing, organic shapes. Each stream represents a category, with width indicating value over time. Ideal for showing trends, topic evolution, or temporal distributions across categories.',
        'data_structure': '''data: [
      ['date', value, 'category'],
      ...
    ]''',
        'example': '''const data = [
 *   ['2024-01-01', 100, 'Category A'],
 *   ['2024-01-01', 80, 'Category B'],
 *   ['2024-01-02', 120, 'Category A']
 * ];'''
    },
    'PictorialBarChart': {
        'description': 'Pictorial bar charts use custom symbols or images instead of rectangular bars. Symbols can repeat to show quantity, making them ideal for infographics, presentations, or any visualization requiring visual metaphors and enhanced engagement.',
        'data_structure': '''xAxis: ['Category1', 'Category2', ...]
    series: [
      {
        name: 'Series Name',
        data: [value1, value2, ...],
        symbol: 'path:// or image:// or built-in',
        color: '#color' (optional)
      }
    ]''',
        'example': '''const data = {
 *   xAxis: ['Mon', 'Tue', 'Wed'],
 *   series: [{ name: 'Sales', data: [100, 200, 150], symbol: 'rect' }]
 * };'''
    },
    'EffectScatterChart': {
        'description': 'Effect scatter charts are scatter plots with animated ripple effects on points. The animation draws attention to specific data points, making them ideal for highlighting important values, showing real-time updates, or emphasizing key insights.',
        'data_structure': '''series: [
      {
        name: 'Series Name',
        data: [[x1, y1], [x2, y2], ...] or [[x, y, size], ...],
        color: '#color' (optional)
      }
    ]''',
        'example': '''const data = {
 *   series: [
 *     { name: 'Important Points', data: [[10, 20, 30], [15, 25, 40]] }
 *   ]
 * };'''
    },
    'LinesChart': {
        'description': 'Lines charts draw lines between coordinates, often with animation effects. Can work with geographic or Cartesian coordinates. Ideal for showing routes, connections, migrations, trade flows, or any directional relationships between points.',
        'data_structure': '''data: [
      { coords: [[x1, y1], [x2, y2]] },
      ...
    ]''',
        'example': '''const data = [
 *   { coords: [[0, 0], [100, 100]] },
 *   { coords: [[50, 50], [150, 150]] }
 * ];'''
    },
    'CustomChart': {
        'description': 'Custom charts allow complete control over rendering using a custom renderItem function. You define how each data item is drawn using graphic primitives. Perfect for unique visualizations, specialized charts, or when built-in chart types don\'t meet requirements.',
        'data_structure': '''data: [
      [value1, value2, ...],
      ...
    ]
    // Structure depends on your custom renderItem function''',
        'example': '''const data = {
 *   xAxis: ['A', 'B', 'C'],
 *   data: [[0, 10, 20], [1, 15, 25]]
 * };
 * const config = {
 *   renderItem: (params, api) => ({ type: 'rect', ... })
 * };'''
    },
    'Scatter3DChart': {
        'description': '3D scatter charts display data points in three-dimensional space. Each point has X, Y, and Z coordinates, making them ideal for visualizing 3D distributions, spatial data, scientific simulations, or any data with three continuous variables. Requires echarts-gl.',
        'data_structure': '''series: [
      {
        name: 'Series Name',
        data: [[x, y, z], ...],
        color: '#color' (optional)
      }
    ]''',
        'example': '''const data = {
 *   series: [
 *     { name: '3D Points', data: [[1, 2, 3], [4, 5, 6]] }
 *   ]
 * };'''
    },
    'Bar3DChart': {
        'description': '3D bar charts display bars in three-dimensional space with X, Y axes for categories and Z axis for values. Bars can be colored by value using visual mapping. Ideal for comparing values across two categorical dimensions. Requires echarts-gl.',
        'data_structure': '''xAxis: ['X1', 'X2', ...]
    yAxis: ['Y1', 'Y2', ...]
    data: [[xIndex, yIndex, value], ...]''',
        'example': '''const data = {
 *   xAxis: ['A', 'B'],
 *   yAxis: ['Q1', 'Q2'],
 *   data: [[0, 0, 100], [0, 1, 150], [1, 0, 200]]
 * };'''
    },
    'Line3DChart': {
        'description': '3D line charts draw lines in three-dimensional space connecting data points. Perfect for showing trajectories, paths in 3D space, time series with an additional dimension, or any continuous data in 3D. Requires echarts-gl.',
        'data_structure': '''series: [
      {
        name: 'Series Name',
        data: [[x, y, z], ...],
        color: '#color' (optional)
      }
    ]''',
        'example': '''const data = {
 *   series: [
 *     { name: 'Path', data: [[0, 0, 0], [1, 1, 1], [2, 1, 2]] }
 *   ]
 * };'''
    },
    'Surface3DChart': {
        'description': '3D surface charts display continuous data as a surface in 3D space. Height and color represent values, making them ideal for mathematical functions, terrain visualization, heat distributions, or any continuous 2D-to-1D mapping. Requires echarts-gl.',
        'data_structure': '''data: [[x, y, z], ...]
    // Or use parametric equations''',
        'example': '''const data = {
 *   data: [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 2]]
 * };'''
    },
    'GlobeChart': {
        'description': 'Globe charts display data on a 3D Earth globe. Can show points, lines, or other visualizations on geographic coordinates. Perfect for global data, international connections, worldwide distributions, or any planetary-scale visualization. Requires echarts-gl.',
        'data_structure': '''series: [
      {
        type: 'scatter3D' or 'lines3D',
        data: [[lon, lat, value], ...] or lines data
      }
    ]''',
        'example': '''const data = {
 *   series: [
 *     { type: 'scatter3D', data: [[-74, 40, 100], [0, 51, 200]] }
 *   ]
 * };'''
    },
    'GraphGLChart': {
        'description': '3D graph charts visualize large-scale network relationships in 3D space using WebGL for performance. Nodes and edges are rendered in 3D with force-directed layout. Ideal for large networks, complex relationships, or when 2D graphs become cluttered. Requires echarts-gl.',
        'data_structure': '''nodes: [{ name: 'Node', value: number, category: index }, ...]
    edges: [{ source: 'Node1', target: 'Node2' }, ...]
    categories: [{ name: 'Category' }, ...]''',
        'example': '''const data = {
 *   nodes: [{ name: 'A' }, { name: 'B' }],
 *   edges: [{ source: 'A', target: 'B' }]
 * };'''
    },
    'FlowGLChart': {
        'description': 'Flow GL charts visualize vector fields in 3D space using animated particles. Particles follow the flow direction, making them ideal for fluid dynamics, wind patterns, electromagnetic fields, or any vector field visualization. Requires echarts-gl.',
        'data_structure': '''data: [[x, y, z, vx, vy, vz], ...]
    // vx, vy, vz are velocity components''',
        'example': '''const data = [
 *   [0, 0, 0, 1, 0, 0],
 *   [1, 0, 0, 1, 1, 0]
 * ];'''
    },
    'LinesGLChart': {
        'description': '3D lines charts on geographic maps display connections between locations on a 3D globe or map. Lines can be animated and styled. Perfect for flight routes, trade connections, migration patterns, or any geographic relationships. Requires echarts-gl.',
        'data_structure': '''data: [
      { coords: [[lon1, lat1], [lon2, lat2]] },
      ...
    ]''',
        'example': '''const data = [
 *   { coords: [[-74, 40], [0, 51]] },
 *   { coords: [[139, 35], [-118, 34]] }
 * ];'''
    }
}

def update_chart_file(filepath):
    """Update a single chart file with documentation."""
    chart_name = Path(filepath).stem
    
    if chart_name not in CHART_INFO:
        print(f"⚠️  No info for {chart_name}, skipping...")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    info = CHART_INFO[chart_name]
    
    # Add JSDoc comment
    jsdoc = f'''/**
 * {chart_name} Component
 * A React wrapper for Apache ECharts {chart_name.replace('Chart', ' Chart')}
 * 
 * {info['description']}
 * 
 * @param {{Object}} data - Chart data
 * Data structure:
 * {info['data_structure']}
 * 
 * @param {{Object}} config - Chart configuration options
 * 
 * @example
 * {info['example']}
 */'''
    
    # Replace the component declaration
    pattern = rf'(import.*?;\s*)(const {chart_name} = )'
    replacement = rf'\1{jsdoc}\nconst {chart_name} = '
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Change color properties from type: 'string' to type: 'color'
    color_properties = [
        'titleColor', 'lineColor', 'borderColor', 'backgroundColor', 'areaColor',
        'pointColor', 'barColor', 'nodeColor', 'edgeColor', 'shadowColor',
        'emphasisColor', 'selectColor', 'labelColor', 'axisLineColor', 'axisTickColor',
        'splitLineColor', 'nameColor', 'indicatorColor', 'wireframeColor', 'effectColor',
        'mapColor', 'upColor', 'downColor', 'upBorderColor', 'downBorderColor',
        'boxColor', 'boxBorderColor', 'outlierColor', 'nodeBorderColor',
        'emphasisLabelColor', 'selectLabelColor', 'emphasisAreaColor', 'selectAreaColor',
        'emphasisBorderColor', 'selectBorderColor'
    ]
    
    for prop in color_properties:
        content = re.sub(
            rf"({prop}:.*?type: )'string'",
            r"\1'color'",
            content
        )
    
    # Add dataFormat property before export
    data_format = f'''
{chart_name}.dataFormat = {{
  description: '{chart_name.replace('Chart', ' chart')} data structure',
  structure: `{info['data_structure']}`,
  example: `{info['example']}`
}};

export default {chart_name};'''
    
    # Replace export statement
    content = re.sub(
        rf'export default {chart_name};',
        data_format,
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """Update all chart files."""
    src_dir = Path(__file__).parent / 'src'
    chart_files = list(src_dir.glob('*Chart.jsx'))
    
    print(f"Found {len(chart_files)} chart files to update\n")
    
    updated = 0
    skipped = 0
    
    for filepath in sorted(chart_files):
        chart_name = filepath.stem
        print(f"Processing {chart_name}...", end=' ')
        
        if update_chart_file(filepath):
            print("✅")
            updated += 1
        else:
            print("⏭️")
            skipped += 1
    
    print(f"\n{'='*50}")
    print(f"Updated: {updated} files")
    print(f"Skipped: {skipped} files")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
