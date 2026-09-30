/**
 * DividerWrapper - Enhanced wrapper for PrimeReact Divider
 * Category: Misc
 * 
 * Separator line with optional content
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Divider } from 'primereact/divider';

// Component metadata embedded for runtime access
export const DividerMetadata = {
  "name": "Divider",
  "import": "Divider",
  "category": "Misc",
  "metadata": {
    "description": "Separator line with optional content",
    "usageExamples": [
      "<DividerWrapper />",
      "<DividerWrapper align=\"center\" type=\"dashed\">OR</DividerWrapper>"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "align",
        "type": "'left' | 'center' | 'right' | 'top' | 'bottom'",
        "optional": true,
        "description": "Content alignment",
        "helpText": "Position of content within divider",
        "dataTypes": [
          "'center' (default)",
          "'left'",
          "'right'",
          "'top'",
          "'bottom'"
        ],
        "examples": [
          "'center'",
          "'left'"
        ]
      },
      {
        "name": "layout",
        "type": "'horizontal' | 'vertical'",
        "optional": true,
        "description": "Divider orientation",
        "helpText": "Horizontal or vertical line",
        "dataTypes": [
          "'horizontal' (default)",
          "'vertical'"
        ],
        "examples": [
          "'horizontal'",
          "'vertical'"
        ]
      },
      {
        "name": "type",
        "type": "'solid' | 'dashed' | 'dotted'",
        "optional": true,
        "description": "Line style",
        "helpText": "Border style",
        "dataTypes": [
          "'solid' (default)",
          "'dashed'",
          "'dotted'"
        ],
        "examples": [
          "'solid'",
          "'dashed'"
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
          "'my-3'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ margin: '1rem 0' }"
        ]
      }
    ],
    "children": {
      "type": "React.ReactNode",
      "description": "Divider content",
      "helpText": "Optional content displayed within divider"
    }
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
    "allowedChildren": [
      "Any React component",
      "Text"
    ],
    "childrenDescription": "Divider can accept children to display content within the divider line",
    "hasChildren": true,
    "examples": [
      "<DividerWrapper>OR</DividerWrapper>",
      "<DividerWrapper align=\"center\"><span>Section</span></DividerWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<DividerWrapper />",
    "withStyling": "<DividerWrapper type=\"dashed\" className=\"my-3\" />",
    "withEvents": "N/A",
    "withRedux": "N/A",
    "withValidation": "N/A",
    "withChildren": "<DividerWrapper align=\"center\" type=\"dashed\">OR</DividerWrapper>"
  }
};

const DividerWrapper = (props) => {
  const {
    align, layout, type, className, style, children, onMount, onUnmount,
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
    align,
    layout,
    type,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <Divider {...primeReactProps}>
      {children}
    </Divider>
  );
};

DividerWrapper.displayName = 'DividerWrapper';

export default DividerWrapper;
