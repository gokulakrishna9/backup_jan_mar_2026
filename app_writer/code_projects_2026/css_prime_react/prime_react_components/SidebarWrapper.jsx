/**
 * SidebarWrapper - Enhanced wrapper for PrimeReact Sidebar
 * Category: Overlay
 * 
 * Side panel overlay
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Sidebar } from 'primereact/sidebar';

// Component metadata embedded for runtime access
export const SidebarMetadata = {
  "name": "Sidebar",
  "import": "Sidebar",
  "category": "Overlay",
  "metadata": {
    "description": "Side panel overlay",
    "usageExamples": [
      "<SidebarWrapper visible={show} onHide={() => setShow(false)}><p>Content</p></SidebarWrapper>",
      "<SidebarWrapper visible={show} position=\"right\" onHide={handleClose}>Content</SidebarWrapper>"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "visible",
        "type": "boolean",
        "optional": false,
        "description": "Visibility state",
        "helpText": "Controls sidebar visibility (controlled component)",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "showSidebar",
          "isOpen",
          "visible"
        ]
      },
      {
        "name": "position",
        "type": "'left' | 'right' | 'top' | 'bottom'",
        "optional": true,
        "description": "Sidebar position",
        "helpText": "Which side of screen sidebar appears",
        "dataTypes": [
          "'left' (default)",
          "'right'",
          "'top'",
          "'bottom'"
        ],
        "examples": [
          "'left'",
          "'right'"
        ]
      },
      {
        "name": "fullScreen",
        "type": "boolean",
        "optional": true,
        "description": "Full screen mode",
        "helpText": "Sidebar covers entire screen",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "modal",
        "type": "boolean",
        "optional": true,
        "description": "Modal mode",
        "helpText": "Shows overlay behind sidebar",
        "dataTypes": [
          "boolean (default: true)"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "dismissable",
        "type": "boolean",
        "optional": true,
        "description": "Close on outside click",
        "helpText": "Clicking overlay closes sidebar",
        "dataTypes": [
          "boolean (default: true)"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "showCloseIcon",
        "type": "boolean",
        "optional": true,
        "description": "Show close button",
        "helpText": "Displays X button",
        "dataTypes": [
          "boolean (default: true)"
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
          "'w-20rem'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ width: '20rem' }"
        ]
      }
    ],
    "children": {
      "type": "React.ReactNode",
      "description": "Sidebar content",
      "helpText": "Any React content"
    }
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onHide",
        "type": "() => void",
        "description": "Callback when sidebar is hidden (required)"
      },
      {
        "name": "onShow",
        "type": "() => void",
        "description": "Callback when sidebar is shown"
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
      "handleHide - Processes onHide event",
      "handleShow - Processes onShow event"
    ],
    "patterns": [
      "Check if event handler exists before calling"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [
      "Any React component",
      "Text",
      "HTML elements"
    ],
    "childrenDescription": "Sidebar accepts any React content as children",
    "hasChildren": true,
    "examples": [
      "<SidebarWrapper visible={show} onHide={handleClose}><Menu model={items} /></SidebarWrapper>",
      "<SidebarWrapper visible={show} onHide={handleClose}><div><h3>Menu</h3><ul><li>Item</li></ul></div></SidebarWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<SidebarWrapper visible={show} onHide={() => setShow(false)}><p>Content</p></SidebarWrapper>",
    "withStyling": "<SidebarWrapper visible={show} position=\"right\" className=\"w-20rem\" onHide={handleClose}>Content</SidebarWrapper>",
    "withEvents": "<SidebarWrapper visible={show} onHide={handleClose} onShow={() => console.log('shown')}>Content</SidebarWrapper>",
    "withRedux": "<SidebarWrapper visible={sidebarVisible} onHide={() => dispatch(closeSidebar())}>Content</SidebarWrapper>",
    "withValidation": "N/A",
    "withChildren": "<SidebarWrapper visible={show} onHide={handleClose}><Menu model={menuItems} /><Button label=\"Close\" /></SidebarWrapper>"
  }
};

const SidebarWrapper = (props) => {
  const {
    visible, position, fullScreen, modal, dismissable, showCloseIcon, className, style, children, onHide, onShow, onMount, onUnmount,
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
    visible,
    position,
    fullScreen,
    modal,
    dismissable,
    showCloseIcon,
    className,
    style,
    onHide,
    onShow,
    ref: componentRef,
    ...restProps
  };

  return (
    <Sidebar {...primeReactProps}>
      {children}
    </Sidebar>
  );
};

SidebarWrapper.displayName = 'SidebarWrapper';

export default SidebarWrapper;
