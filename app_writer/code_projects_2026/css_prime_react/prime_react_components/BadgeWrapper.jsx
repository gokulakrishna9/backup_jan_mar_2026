/**
 * BadgeWrapper - Enhanced wrapper for PrimeReact Badge
 * Category: Misc
 * 
 * Displays a badge with value and severity styling
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Badge } from 'primereact/badge';

// Component metadata embedded for runtime access
export const BadgeMetadata = {
  "name": "Badge",
  "import": "Badge",
  "category": "Misc",
  "metadata": {
    "description": "Displays a badge with value and severity styling",
    "usageExamples": [
      "<BadgeWrapper value={5} severity=\"danger\" />",
      "<BadgeWrapper value=\"NEW\" severity=\"success\" size=\"large\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "string | number",
        "optional": true,
        "description": "Badge value to display",
        "helpText": "Can be numeric (count) or string (status text)",
        "dataTypes": [
          "number (e.g., 5, 10, 99)",
          "string (e.g., 'NEW', 'SALE', 'HOT')"
        ],
        "examples": [
          "5",
          "10",
          "'NEW'",
          "'BETA'"
        ]
      },
      {
        "name": "severity",
        "type": "'success' | 'info' | 'warning' | 'danger' | null",
        "optional": true,
        "description": "Severity type - determines color scheme",
        "helpText": "Predefined color schemes: success=green, info=blue, warning=orange, danger=red",
        "dataTypes": [
          "'success'",
          "'info'",
          "'warning'",
          "'danger'",
          "null"
        ],
        "examples": [
          "'success'",
          "'danger'",
          "'warning'"
        ]
      },
      {
        "name": "size",
        "type": "'normal' | 'large' | 'xlarge'",
        "optional": true,
        "description": "Size of badge",
        "helpText": "Controls the badge dimensions",
        "dataTypes": [
          "'normal' (default)",
          "'large'",
          "'xlarge'"
        ],
        "examples": [
          "'large'",
          "'xlarge'"
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
          "'ml-2 shadow-2'",
          "'border-round'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles object",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ marginLeft: '1rem' }",
          "{ fontSize: '0.875rem' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [],
    "simplified": [],
    "validation": [],
    "lifecycle": []
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
    "basic": "<BadgeWrapper value={5} />",
    "withStyling": "<BadgeWrapper value=\"NEW\" className=\"ml-2\" style={{ fontSize: '0.875rem' }} />",
    "withEvents": "N/A",
    "withRedux": "N/A",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const BadgeWrapper = (props) => {
  const {
    value, severity, size, className, style,
    ...restProps
  } = props;

  const componentRef = useRef(null);

  // Build props for underlying PrimeReact component
  const primeReactProps = {
    value,
    severity,
    size,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <Badge {...primeReactProps} />
  );
};

BadgeWrapper.displayName = 'BadgeWrapper';

export default BadgeWrapper;
