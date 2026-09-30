/**
 * ProgressBarWrapper - Enhanced wrapper for PrimeReact ProgressBar
 * Category: Misc
 * 
 * Progress indicator
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { ProgressBar } from 'primereact/progressbar';

// Component metadata embedded for runtime access
export const ProgressBarMetadata = {
  "name": "ProgressBar",
  "import": "ProgressBar",
  "category": "Misc",
  "metadata": {
    "description": "Progress indicator",
    "usageExamples": [
      "<ProgressBarWrapper value={50} />",
      "<ProgressBarWrapper mode=\"indeterminate\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "number",
        "optional": true,
        "description": "Progress value (0-100)",
        "helpText": "Percentage of completion",
        "dataTypes": [
          "number (0-100)"
        ],
        "examples": [
          "50",
          "75",
          "100"
        ]
      },
      {
        "name": "mode",
        "type": "'determinate' | 'indeterminate'",
        "optional": true,
        "description": "Progress mode",
        "helpText": "determinate=shows value, indeterminate=animated loading",
        "dataTypes": [
          "'determinate' (default)",
          "'indeterminate'"
        ],
        "examples": [
          "'determinate'",
          "'indeterminate'"
        ]
      },
      {
        "name": "showValue",
        "type": "boolean",
        "optional": true,
        "description": "Show percentage text",
        "helpText": "Displays value as text",
        "dataTypes": [
          "boolean (default: true)"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "unit",
        "type": "string",
        "optional": true,
        "description": "Unit suffix",
        "helpText": "Text after value (default: %)",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'%'",
          "' MB'",
          "' items'"
        ]
      }
    ],
    "styling": [
      {
        "name": "className",
        "type": "string",
        "optional": true,
        "description": "Additional CSS classes",
        "helpText": "Supports PrimeFlex utility classes",
        "examples": [
          "'mb-3'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ height: '20px' }"
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
        "description": "Called when component mounts"
      },
      {
        "name": "onUnmount",
        "type": "() => void",
        "description": "Called when component unmounts"
      }
    ]
  },
  "eventHandlerMethods": {
    "internal": [],
    "patterns": []
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children",
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
    "basic": "<ProgressBarWrapper value={50} />",
    "withStyling": "<ProgressBarWrapper value={75} className=\"mb-3\" style={{ height: '20px' }} />",
    "withEvents": "N/A",
    "withRedux": "<ProgressBarWrapper value={uploadProgress} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const ProgressBarWrapper = (props) => {
  const {
    value, mode, showValue, unit, className, style, onMount, onUnmount,
    ...restProps
  } = props;

  const componentRef = useRef(null);

  // Lifecycle: onMount
  useEffect(() => {
    if (onMount) {
      onMount();
    }
  }, []);

  // Lifecycle: onUnmount
  useEffect(() => {
    return () => {
      if (onUnmount) {
        onUnmount();
      }
    };
  }, []);

  // Build props for underlying PrimeReact component
  const primeReactProps = {
    value,
    mode,
    showValue,
    unit,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <ProgressBar {...primeReactProps} />
  );
};

ProgressBarWrapper.displayName = 'ProgressBarWrapper';

export default ProgressBarWrapper;
