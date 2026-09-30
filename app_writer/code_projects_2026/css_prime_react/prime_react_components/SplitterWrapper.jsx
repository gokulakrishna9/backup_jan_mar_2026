/**
 * SplitterWrapper - Enhanced wrapper for PrimeReact Splitter
 * Category: Panel
 * 
 * Resizable split panels
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Splitter } from 'primereact/splitter';

// Component metadata embedded for runtime access
export const SplitterMetadata = {
  "name": "Splitter",
  "import": "Splitter",
  "category": "Panel",
  "metadata": {
    "description": "Resizable split panels",
    "usageExamples": [
      "<SplitterWrapper><SplitterPanel><div>Panel 1</div></SplitterPanel><SplitterPanel><div>Panel 2</div></SplitterPanel></SplitterWrapper>",
      "<SplitterWrapper layout=\"vertical\"><SplitterPanel size={30}><div>Top</div></SplitterPanel><SplitterPanel size={70}><div>Bottom</div></SplitterPanel></SplitterWrapper>"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "layout",
        "type": "'horizontal' | 'vertical'",
        "optional": true,
        "description": "Split orientation",
        "helpText": "Direction of split",
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
        "name": "gutterSize",
        "type": "number",
        "optional": true,
        "description": "Gutter size",
        "helpText": "Width of resize handle in pixels (default: 4)",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "4",
          "8",
          "10"
        ]
      },
      {
        "name": "stateKey",
        "type": "string",
        "optional": true,
        "description": "State storage key",
        "helpText": "Key for localStorage to save panel sizes",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'splitter-state'",
          "'layout-state'"
        ]
      },
      {
        "name": "stateStorage",
        "type": "'session' | 'local'",
        "optional": true,
        "description": "State storage type",
        "helpText": "Where to save panel sizes",
        "dataTypes": [
          "'session'",
          "'local'"
        ],
        "examples": [
          "'session'",
          "'local'"
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
          "{ height: '300px' }"
        ]
      }
    ],
    "children": {
      "type": "SplitterPanel[]",
      "description": "SplitterPanel components",
      "helpText": "Must contain SplitterPanel children"
    }
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onResizeEnd",
        "type": "(e: { sizes: number[] }) => void",
        "description": "Callback when resize ends"
      }
    ],
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
    "internal": [
      "handleResizeEnd - Processes onResizeEnd event"
    ],
    "patterns": [
      "Check if event handler exists before calling"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [
      "SplitterPanel"
    ],
    "childrenDescription": "Splitter must contain SplitterPanel components as direct children",
    "hasChildren": true,
    "examples": [
      "<SplitterWrapper><SplitterPanel size={50}><div>Left</div></SplitterPanel><SplitterPanel size={50}><div>Right</div></SplitterPanel></SplitterWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<SplitterWrapper><SplitterPanel><div>Panel 1</div></SplitterPanel><SplitterPanel><div>Panel 2</div></SplitterPanel></SplitterWrapper>",
    "withStyling": "<SplitterWrapper layout=\"vertical\" style={{ height: '300px' }}><SplitterPanel><div>Top</div></SplitterPanel><SplitterPanel><div>Bottom</div></SplitterPanel></SplitterWrapper>",
    "withEvents": "<SplitterWrapper onResizeEnd={(e) => console.log('Sizes:', e.sizes)}><SplitterPanel>Panel 1</SplitterPanel><SplitterPanel>Panel 2</SplitterPanel></SplitterWrapper>",
    "withRedux": "<SplitterWrapper onResizeEnd={(e) => dispatch(saveSizes(e.sizes))}><SplitterPanel>Left</SplitterPanel><SplitterPanel>Right</SplitterPanel></SplitterWrapper>",
    "withValidation": "N/A",
    "withChildren": "<SplitterWrapper><SplitterPanel size={30}><Tree value={nodes} /></SplitterPanel><SplitterPanel size={70}><DataTable value={data} /></SplitterPanel></SplitterWrapper>"
  }
};

const SplitterWrapper = (props) => {
  const {
    layout, gutterSize, stateKey, stateStorage, className, style, children, onResizeEnd, onMount, onUnmount,
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
    layout,
    gutterSize,
    stateKey,
    stateStorage,
    className,
    style,
    onResizeEnd,
    ref: componentRef,
    ...restProps
  };

  return (
    <Splitter {...primeReactProps}>
      {children}
    </Splitter>
  );
};

SplitterWrapper.displayName = 'SplitterWrapper';

export default SplitterWrapper;
