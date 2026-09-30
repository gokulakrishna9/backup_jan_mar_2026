/**
 * PopoverWrapper - Enhanced wrapper for PrimeReact Popover
 * Category: Overlay
 * 
 * Popover overlay for displaying rich content on demand
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Popover } from 'primereact/popover';

// Component metadata embedded for runtime access
export const PopoverMetadata = {
  "name": "Popover",
  "import": "Popover",
  "category": "Overlay",
  "metadata": {
    "description": "Popover overlay for displaying rich content on demand",
    "usageExamples": [
      "<PopoverWrapper ref={popoverRef}><div>Popover content</div></PopoverWrapper>",
      "<PopoverWrapper ref={op} dismissable><Card title=\"Details\"><p>Additional information</p></Card></PopoverWrapper>"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "dismissable",
        "type": "boolean",
        "optional": true,
        "description": "Whether clicking outside closes popover",
        "helpText": "Enables click-outside-to-close behavior",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "appendTo",
        "type": "'body' | 'self' | HTMLElement",
        "optional": true,
        "description": "DOM element to append popover",
        "helpText": "Where to mount the popover in DOM",
        "dataTypes": [
          "'body'",
          "'self'",
          "HTMLElement"
        ],
        "examples": [
          "'body'",
          "'self'"
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
          "'custom-popover'",
          "'shadow-4'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles object",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ width: '300px' }"
        ]
      }
    ],
    "children": {
      "type": "React.ReactNode",
      "required": true,
      "description": "Popover content"
    }
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onShow",
        "type": "() => void",
        "optional": true,
        "description": "Callback when popover is shown"
      },
      {
        "name": "onHide",
        "type": "() => void",
        "optional": true,
        "description": "Callback when popover is hidden"
      }
    ],
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
    "patterns": [
      "Use ref to control popover: popoverRef.current.toggle(event)",
      "For contextual help: Show popover on button click with rich content"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [
      "Any React component"
    ],
    "childrenDescription": "Can contain any content including text, images, forms, or complex components. Content is displayed in an overlay when popover is shown.",
    "hasChildren": true,
    "examples": [
      "<PopoverWrapper ref={op}><div className=\"p-3\"><h4>Title</h4><p>Content</p></div></PopoverWrapper>",
      "<PopoverWrapper ref={op}><Card title=\"Info\"><p>Details here</p></Card></PopoverWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<PopoverWrapper ref={popoverRef}><div>Popover content</div></PopoverWrapper>",
    "withStyling": "<PopoverWrapper ref={op} className=\"shadow-4\" style={{ width: '400px' }}><div className=\"p-3\">Rich content</div></PopoverWrapper>",
    "withEvents": "<PopoverWrapper ref={op} onShow={() => console.log('Shown')} onHide={() => console.log('Hidden')} dismissable><div>Content</div></PopoverWrapper>",
    "withRedux": "<PopoverWrapper ref={op} onShow={() => dispatch(loadPopoverData())}><div>{popoverContent}</div></PopoverWrapper>",
    "withValidation": "N/A",
    "withChildren": "<PopoverWrapper ref={op}><Card title=\"User Info\"><div className=\"grid\"><div className=\"col-12\"><Avatar /><p>Details</p></div></div></Card></PopoverWrapper>"
  }
};

const PopoverWrapper = (props) => {
  const {
    dismissable, appendTo, className, style, children, onShow, onHide, onMount,
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
    dismissable,
    appendTo,
    className,
    style,
    onShow,
    onHide,
    ref: componentRef,
    ...restProps
  };

  return (
    <Popover {...primeReactProps}>
      {children}
    </Popover>
  );
};

PopoverWrapper.displayName = 'PopoverWrapper';

export default PopoverWrapper;
