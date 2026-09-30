/**
 * ProgressSpinnerWrapper - Enhanced wrapper for PrimeReact ProgressSpinner
 * Category: Misc
 * 
 * Animated loading spinner
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { ProgressSpinner } from 'primereact/progressspinner';

// Component metadata embedded for runtime access
export const ProgressSpinnerMetadata = {
  "name": "ProgressSpinner",
  "import": "ProgressSpinner",
  "category": "Misc",
  "metadata": {
    "description": "Animated loading spinner",
    "usageExamples": [
      "<ProgressSpinnerWrapper />",
      "<ProgressSpinnerWrapper strokeWidth=\"4\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "strokeWidth",
        "type": "string",
        "optional": true,
        "description": "Stroke width",
        "helpText": "Width of spinner stroke",
        "dataTypes": [
          "string (default: '2')"
        ],
        "examples": [
          "'2'",
          "'4'",
          "'8'"
        ]
      },
      {
        "name": "fill",
        "type": "string",
        "optional": true,
        "description": "Fill color",
        "helpText": "Background fill color",
        "dataTypes": [
          "string (CSS color)"
        ],
        "examples": [
          "'transparent'",
          "'#fff'"
        ]
      },
      {
        "name": "animationDuration",
        "type": "string",
        "optional": true,
        "description": "Animation duration",
        "helpText": "Speed of rotation",
        "dataTypes": [
          "string (CSS time)"
        ],
        "examples": [
          "'2s'",
          "'1s'"
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
          "'m-auto'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ width: '50px', height: '50px' }"
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
    "basic": "<ProgressSpinnerWrapper />",
    "withStyling": "<ProgressSpinnerWrapper strokeWidth=\"4\" className=\"m-auto\" style={{ width: '50px' }} />",
    "withEvents": "N/A",
    "withRedux": "N/A",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const ProgressSpinnerWrapper = (props) => {
  const {
    strokeWidth, fill, animationDuration, className, style, onMount, onUnmount,
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
    strokeWidth,
    fill,
    animationDuration,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <ProgressSpinner {...primeReactProps} />
  );
};

ProgressSpinnerWrapper.displayName = 'ProgressSpinnerWrapper';

export default ProgressSpinnerWrapper;
