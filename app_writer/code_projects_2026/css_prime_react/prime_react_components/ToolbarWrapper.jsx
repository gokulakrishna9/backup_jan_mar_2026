/**
 * ToolbarWrapper - Enhanced wrapper for PrimeReact Toolbar
 * Category: Misc
 * 
 * Container for grouping buttons and other content
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Toolbar } from 'primereact/toolbar';

// Component metadata embedded for runtime access
export const ToolbarMetadata = {
  "name": "Toolbar",
  "import": "Toolbar",
  "category": "Misc",
  "metadata": {
    "description": "Container for grouping buttons and other content",
    "usageExamples": [
      "<ToolbarWrapper start={<Button label=\"New\" />} end={<Button label=\"Export\" />} />",
      "<ToolbarWrapper left={leftContent} right={rightContent} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "start",
        "type": "React.ReactNode",
        "optional": true,
        "description": "Start content",
        "helpText": "Content at start of toolbar (left side)",
        "dataTypes": [
          "React.ReactNode"
        ],
        "examples": [
          "<Button label=\"New\" />",
          "<div><Button /><Button /></div>"
        ]
      },
      {
        "name": "center",
        "type": "React.ReactNode",
        "optional": true,
        "description": "Center content",
        "helpText": "Content in center of toolbar",
        "dataTypes": [
          "React.ReactNode"
        ],
        "examples": [
          "<span>Title</span>",
          "<InputText />"
        ]
      },
      {
        "name": "end",
        "type": "React.ReactNode",
        "optional": true,
        "description": "End content",
        "helpText": "Content at end of toolbar (right side)",
        "dataTypes": [
          "React.ReactNode"
        ],
        "examples": [
          "<Button label=\"Save\" />",
          "<Avatar />"
        ]
      },
      {
        "name": "left",
        "type": "React.ReactNode",
        "optional": true,
        "description": "Left content (alias for start)",
        "helpText": "Same as start prop",
        "dataTypes": [
          "React.ReactNode"
        ],
        "examples": [
          "<Button label=\"New\" />"
        ]
      },
      {
        "name": "right",
        "type": "React.ReactNode",
        "optional": true,
        "description": "Right content (alias for end)",
        "helpText": "Same as end prop",
        "dataTypes": [
          "React.ReactNode"
        ],
        "examples": [
          "<Button label=\"Save\" />"
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
          "{ marginBottom: '1rem' }"
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
    "childrenDescription": "This component does not accept children - content defined via start/center/end props",
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
    "basic": "<ToolbarWrapper start={<Button label=\"New\" />} end={<Button label=\"Export\" />} />",
    "withStyling": "<ToolbarWrapper left={leftContent} right={rightContent} className=\"mb-3\" />",
    "withEvents": "N/A",
    "withRedux": "<ToolbarWrapper start={<Button label=\"Save\" onClick={() => dispatch(save())} />} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const ToolbarWrapper = (props) => {
  const {
    start, center, end, left, right, className, style, onMount, onUnmount,
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
    start,
    center,
    end,
    left,
    right,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <Toolbar {...primeReactProps} />
  );
};

ToolbarWrapper.displayName = 'ToolbarWrapper';

export default ToolbarWrapper;
