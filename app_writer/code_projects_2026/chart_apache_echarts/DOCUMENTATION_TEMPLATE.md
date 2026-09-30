# Chart Documentation Template

This template shows the pattern for documenting each chart component.

## Pattern for JSDoc Comment
```javascript
/**
 * ChartName Component
 * A React wrapper for Apache ECharts [Chart Type]
 * 
 * [Description of what the chart does and when to use it]
 * 
 * @param {Object} data - Chart data
 * [Document data structure properties]
 * 
 * @param {Object} config - Chart configuration options
 * 
 * @example
 * const data = { ... };
 * const config = { ... };
 */
```

## Pattern for dataFormat Property
```javascript
ChartName.dataFormat = {
  description: 'Chart data structure',
  structure: {
    propertyName: {
      type: 'Type',
      required: true/false,
      description: 'What this property does',
      example: 'Example value'
    }
  }
};
```

## Color Properties
All color-related properties should use `type: 'color'` instead of `type: 'string'`

Examples:
- titleColor
- lineColor
- borderColor
- backgroundColor
- etc.
