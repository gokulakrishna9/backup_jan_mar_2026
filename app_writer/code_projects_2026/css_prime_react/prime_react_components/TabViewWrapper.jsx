/**
 * TabViewWrapper - Enhanced wrapper for PrimeReact TabView
 * Category: Panel
 * 
 * Tabbed panel container
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { TabView } from 'primereact/tabview';

// Component metadata embedded for runtime access
export const TabViewMetadata = {
  "name": "TabView",
  "import": "TabView",
  "category": "Panel",
  "metadata": {
    "description": "Tabbed panel container",
    "usageExamples": [
      "<TabViewWrapper><TabPanel header=\"Tab 1\"><p>Content 1</p></TabPanel></TabViewWrapper>",
      "<TabViewWrapper activeIndex={activeTab} onTabChange={(e) => setActiveTab(e.index)}><TabPanel header=\"Tab 1\">Content</TabPanel></TabViewWrapper>"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "activeIndex",
        "type": "number",
        "optional": true,
        "description": "Active tab index",
        "helpText": "Controls which tab is active (controlled component)",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "0",
          "1",
          "2"
        ]
      },
      {
        "name": "scrollable",
        "type": "boolean",
        "optional": true,
        "description": "Enable scrolling",
        "helpText": "Tabs scroll horizontally when overflow",
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
          "{ marginBottom: '1rem' }"
        ]
      }
    ],
    "children": {
      "type": "TabPanel[]",
      "description": "TabPanel components",
      "helpText": "Must contain TabPanel children"
    }
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onTabChange",
        "type": "(e: { index: number }) => void",
        "description": "Callback when active tab changes"
      },
      {
        "name": "onTabClose",
        "type": "(e: { index: number }) => void",
        "description": "Callback when tab is closed (if closable)"
      }
    ],
    "simplified": [
      {
        "name": "onActiveIndexChange",
        "type": "(index: number) => void",
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
      "handleTabChange - Processes onTabChange event, calls onTabChange and onActiveIndexChange",
      "handleTabClose - Processes onTabClose event"
    ],
    "patterns": [
      "Check if event handler exists before calling",
      "Extract index from event object"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [
      "TabPanel"
    ],
    "childrenDescription": "TabView must contain TabPanel components as direct children",
    "hasChildren": true,
    "examples": [
      "<TabViewWrapper><TabPanel header=\"Tab 1\"><p>Content 1</p></TabPanel><TabPanel header=\"Tab 2\"><p>Content 2</p></TabPanel></TabViewWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<TabViewWrapper><TabPanel header=\"Tab 1\"><p>Content</p></TabPanel></TabViewWrapper>",
    "withStyling": "<TabViewWrapper scrollable className=\"mb-3\"><TabPanel header=\"Tab\">Content</TabPanel></TabViewWrapper>",
    "withEvents": "<TabViewWrapper onTabChange={handleChange}><TabPanel header=\"Tab\">Content</TabPanel></TabViewWrapper>",
    "withRedux": "<TabViewWrapper activeIndex={activeTab} onActiveIndexChange={(idx) => dispatch(setActiveTab(idx))}><TabPanel header=\"Tab\">Content</TabPanel></TabViewWrapper>",
    "withValidation": "N/A",
    "withChildren": "<TabViewWrapper><TabPanel header=\"Tab 1\">Content 1</TabPanel><TabPanel header=\"Tab 2\">Content 2</TabPanel></TabViewWrapper>"
  }
};

const TabViewWrapper = (props) => {
  const {
    activeIndex, scrollable, className, style, children, onTabChange, onTabClose, onActiveIndexChange, onMount, onUnmount,
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
    scrollable,
    className,
    style,
    onTabChange,
    onTabClose,
    ref: componentRef,
    ...restProps
  };

  return (
    <TabView {...primeReactProps}>
      {children}
    </TabView>
  );
};

TabViewWrapper.displayName = 'TabViewWrapper';

export default TabViewWrapper;
