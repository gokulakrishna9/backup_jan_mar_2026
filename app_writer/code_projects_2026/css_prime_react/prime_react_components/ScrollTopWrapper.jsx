/**
 * ScrollTopWrapper - Enhanced wrapper for PrimeReact ScrollTop
 * Category: Misc
 * 
 * Button to scroll to top of page
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { ScrollTop } from 'primereact/scrolltop';

// Component metadata embedded for runtime access
export const ScrollTopMetadata = {
  "name": "ScrollTop",
  "import": "ScrollTop",
  "category": "Misc",
  "metadata": {
    "description": "Button to scroll to top of page",
    "usageExamples": [
      "<ScrollTopWrapper />",
      "<ScrollTopWrapper threshold={500} icon=\"pi pi-arrow-up\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "threshold",
        "type": "number",
        "optional": true,
        "description": "Scroll threshold",
        "helpText": "Pixels scrolled before button appears",
        "dataTypes": [
          "number (default: 400)"
        ],
        "examples": [
          "400",
          "500",
          "1000"
        ]
      },
      {
        "name": "icon",
        "type": "string",
        "optional": true,
        "description": "Icon class",
        "helpText": "PrimeIcons class name",
        "dataTypes": [
          "string (PrimeIcons class)"
        ],
        "examples": [
          "'pi pi-chevron-up'",
          "'pi pi-arrow-up'"
        ]
      },
      {
        "name": "target",
        "type": "'window' | 'parent'",
        "optional": true,
        "description": "Scroll target",
        "helpText": "Element to scroll",
        "dataTypes": [
          "'window' (default)",
          "'parent'"
        ],
        "examples": [
          "'window'",
          "'parent'"
        ]
      },
      {
        "name": "behavior",
        "type": "'auto' | 'smooth'",
        "optional": true,
        "description": "Scroll behavior",
        "helpText": "Animation style",
        "dataTypes": [
          "'smooth' (default)",
          "'auto'"
        ],
        "examples": [
          "'smooth'",
          "'auto'"
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
          "'custom-scroll-top'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ bottom: '20px', right: '20px' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onClick",
        "type": "() => void",
        "description": "Callback when button is clicked"
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
      "handleClick - Processes onClick event"
    ],
    "patterns": [
      "Check if event handler exists before calling"
    ]
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
    "basic": "<ScrollTopWrapper />",
    "withStyling": "<ScrollTopWrapper threshold={500} icon=\"pi pi-arrow-up\" className=\"custom-scroll-top\" />",
    "withEvents": "<ScrollTopWrapper onClick={() => console.log('scrolling to top')} />",
    "withRedux": "<ScrollTopWrapper onClick={() => dispatch(trackScrollTop())} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const ScrollTopWrapper = (props) => {
  const {
    threshold, icon, target, behavior, className, style, onClick, onMount, onUnmount,
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
    threshold,
    icon,
    target,
    behavior,
    className,
    style,
    onClick,
    ref: componentRef,
    ...restProps
  };

  return (
    <ScrollTop {...primeReactProps} />
  );
};

ScrollTopWrapper.displayName = 'ScrollTopWrapper';

export default ScrollTopWrapper;
