/**
 * AccordionWrapper - Enhanced wrapper for PrimeReact Accordion
 * Category: Panel
 * 
 * Container with collapsible tabs
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Accordion } from 'primereact/accordion';

// Component metadata embedded for runtime access
export const AccordionMetadata = {
  "name": "Accordion",
  "import": "Accordion",
  "category": "Panel",
  "metadata": {
    "description": "Container with collapsible tabs",
    "usageExamples": [
      "<AccordionWrapper><AccordionTab header=\"Tab 1\"><p>Content 1</p></AccordionTab></AccordionWrapper>",
      "<AccordionWrapper multiple activeIndex={[0, 1]}><AccordionTab header=\"Tab 1\">Content</AccordionTab></AccordionWrapper>"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "activeIndex",
        "type": "number | number[]",
        "optional": true,
        "description": "Active tab index(es)",
        "helpText": "Controls which tabs are expanded (controlled component)",
        "dataTypes": [
          "number (single)",
          "number[] (multiple)"
        ],
        "examples": [
          "0",
          "[0, 1]",
          "2"
        ]
      },
      {
        "name": "multiple",
        "type": "boolean",
        "optional": true,
        "description": "Allow multiple tabs open",
        "helpText": "Enables multiple tabs to be expanded simultaneously",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
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
          "{ width: '100%' }"
        ]
      }
    ],
    "children": {
      "type": "AccordionTab[]",
      "description": "AccordionTab components",
      "helpText": "Must contain AccordionTab children"
    }
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onTabChange",
        "type": "(e: { index: number | number[] }) => void",
        "description": "Callback when active tab changes"
      },
      {
        "name": "onTabOpen",
        "type": "(e: { index: number }) => void",
        "description": "Callback when tab opens"
      },
      {
        "name": "onTabClose",
        "type": "(e: { index: number }) => void",
        "description": "Callback when tab closes"
      }
    ],
    "simplified": [
      {
        "name": "onActiveIndexChange",
        "type": "(index: number | number[]) => void",
        "description": "Simplified callback with just the index"
      }
    ],
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
      "handleTabChange - Processes onTabChange event, calls onTabChange and onActiveIndexChange"
    ],
    "patterns": [
      "Check if event handler exists before calling",
      "Extract index from event object"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [
      "AccordionTab"
    ],
    "childrenDescription": "Accordion must contain AccordionTab components as direct children",
    "hasChildren": true,
    "examples": [
      "<AccordionWrapper><AccordionTab header=\"Tab 1\"><p>Content 1</p></AccordionTab><AccordionTab header=\"Tab 2\"><p>Content 2</p></AccordionTab></AccordionWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<AccordionWrapper><AccordionTab header=\"Tab 1\"><p>Content</p></AccordionTab></AccordionWrapper>",
    "withStyling": "<AccordionWrapper className=\"mb-3\"><AccordionTab header=\"Tab\">Content</AccordionTab></AccordionWrapper>",
    "withEvents": "<AccordionWrapper onTabChange={handleChange}><AccordionTab header=\"Tab\">Content</AccordionTab></AccordionWrapper>",
    "withRedux": "<AccordionWrapper activeIndex={activeTab} onActiveIndexChange={(idx) => dispatch(setActiveTab(idx))}><AccordionTab header=\"Tab\">Content</AccordionTab></AccordionWrapper>",
    "withValidation": "N/A",
    "withChildren": "<AccordionWrapper multiple><AccordionTab header=\"Tab 1\">Content 1</AccordionTab><AccordionTab header=\"Tab 2\">Content 2</AccordionTab></AccordionWrapper>"
  }
};

const AccordionWrapper = (props) => {
  const {
    activeIndex, multiple, className, style, children, onTabChange, onTabOpen, onTabClose, onActiveIndexChange, onMount, onUnmount,
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
    activeIndex,
    multiple,
    className,
    style,
    onTabChange,
    onTabOpen,
    onTabClose,
    ref: componentRef,
    ...restProps
  };

  return (
    <Accordion {...primeReactProps}>
      {children}
    </Accordion>
  );
};

AccordionWrapper.displayName = 'AccordionWrapper';

export default AccordionWrapper;
