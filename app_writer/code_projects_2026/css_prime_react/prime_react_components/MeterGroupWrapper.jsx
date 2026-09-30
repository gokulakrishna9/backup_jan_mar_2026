/**
 * MeterGroupWrapper - Enhanced wrapper for PrimeReact MeterGroup
 * Category: Misc
 * 
 * Multiple progress meters for displaying resource allocation and usage
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { MeterGroup } from 'primereact/metergroup';

// Component metadata embedded for runtime access
export const MeterGroupMetadata = {
  "name": "MeterGroup",
  "import": "MeterGroup",
  "category": "Misc",
  "metadata": {
    "description": "Multiple progress meters for displaying resource allocation and usage",
    "usageExamples": [
      "<MeterGroupWrapper value={meterData} />",
      "<MeterGroupWrapper value={storageData} labelPosition=\"end\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "MeterItem[]",
        "optional": false,
        "description": "Array of meter items",
        "helpText": "Meter data with label, value, color properties",
        "dataTypes": [
          "MeterItem[] - { label: string, value: number, color?: string, icon?: string }"
        ],
        "examples": [
          "[{ label: 'Apps', value: 24, color: '#34d399' }, { label: 'Messages', value: 16, color: '#fbbf24' }]"
        ]
      },
      {
        "name": "min",
        "type": "number",
        "optional": true,
        "description": "Minimum value",
        "helpText": "Minimum boundary value (default: 0)",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "0",
          "10"
        ]
      },
      {
        "name": "max",
        "type": "number",
        "optional": true,
        "description": "Maximum value",
        "helpText": "Maximum boundary value (default: 100)",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "100",
          "1000"
        ]
      },
      {
        "name": "orientation",
        "type": "'horizontal' | 'vertical'",
        "optional": true,
        "description": "Orientation of meters",
        "helpText": "Layout direction (default: horizontal)",
        "dataTypes": [
          "'horizontal'",
          "'vertical'"
        ],
        "examples": [
          "'horizontal'",
          "'vertical'"
        ]
      },
      {
        "name": "labelPosition",
        "type": "'start' | 'end'",
        "optional": true,
        "description": "Position of labels",
        "helpText": "Where to display labels relative to meters (default: end)",
        "dataTypes": [
          "'start'",
          "'end'"
        ],
        "examples": [
          "'start'",
          "'end'"
        ]
      }
    ],
    "styling": [
      {
        "name": "className",
        "type": "string",
        "optional": true,
        "description": "Additional CSS classes for custom styling",
        "helpText": "Supports PrimeFlex utility classes and custom CSS",
        "examples": [
          "'w-full'",
          "'mb-3'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles object",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ width: '100%' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [],
    "simplified": [],
    "validation": [],
    "lifecycle": [
      {
        "name": "onMount",
        "type": "() => void",
        "optional": true,
        "description": "Callback when component mounts"
      }
    ]
  },
  "eventHandlerMethods": {
    "internal": [],
    "patterns": []
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children. Use value prop to define meters.",
    "hasChildren": false,
    "examples": []
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<MeterGroupWrapper value={meterData} />",
    "withStyling": "<MeterGroupWrapper value={storageData} className=\"w-full mb-3\" />",
    "withEvents": "N/A",
    "withRedux": "<MeterGroupWrapper value={storageMetrics} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const MeterGroupWrapper = (props) => {
  const {
    value, min, max, orientation, labelPosition, className, style, onMount,
    ...restProps
  } = props;

  const componentRef = useRef(null);

  // Lifecycle: onMount
  useEffect(() => {
    if (onMount) {
      onMount();
    }
  }, []);

  // Build props for underlying PrimeReact component
  const primeReactProps = {
    value,
    min,
    max,
    orientation,
    labelPosition,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <MeterGroup {...primeReactProps} />
  );
};

MeterGroupWrapper.displayName = 'MeterGroupWrapper';

export default MeterGroupWrapper;
