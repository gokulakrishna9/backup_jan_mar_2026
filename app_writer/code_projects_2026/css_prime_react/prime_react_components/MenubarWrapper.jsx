/**
 * MenubarWrapper - Enhanced wrapper for PrimeReact Menubar
 * Category: Menu
 * 
 * Horizontal menu bar
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Menubar } from 'primereact/menubar';

// Component metadata embedded for runtime access
export const MenubarMetadata = {
  "name": "Menubar",
  "import": "Menubar",
  "category": "Menu",
  "metadata": {
    "description": "Horizontal menu bar",
    "usageExamples": [
      "<MenubarWrapper model={items} />",
      "<MenubarWrapper model={menuItems} start={logo} end={<Button label=\"Logout\" />} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "model",
        "type": "MenuItem[]",
        "optional": false,
        "description": "Menu items",
        "helpText": "Array of menu item objects with nested items",
        "dataTypes": [
          "MenuItem[] - {label, icon, command, url, items}"
        ],
        "examples": [
          "[{label: 'File', items: [{label: 'New'}]}]"
        ]
      },
      {
        "name": "start",
        "type": "React.ReactNode",
        "optional": true,
        "description": "Start content",
        "helpText": "Content at start of menubar (logo, etc.)",
        "dataTypes": [
          "React.ReactNode"
        ],
        "examples": [
          "<img src=\"logo.png\" />",
          "<span>Brand</span>"
        ]
      },
      {
        "name": "end",
        "type": "React.ReactNode",
        "optional": true,
        "description": "End content",
        "helpText": "Content at end of menubar (buttons, etc.)",
        "dataTypes": [
          "React.ReactNode"
        ],
        "examples": [
          "<Button label=\"Login\" />",
          "<Avatar />"
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
    "patterns": [
      "Menu items have their own command callbacks"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children - items defined via model prop, use start/end props for custom content",
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
    "basic": "<MenubarWrapper model={[{label: 'File', items: [{label: 'New'}]}]} />",
    "withStyling": "<MenubarWrapper model={items} className=\"mb-3\" />",
    "withEvents": "<MenubarWrapper model={[{label: 'Save', command: () => handleSave()}]} />",
    "withRedux": "<MenubarWrapper model={[{label: 'Logout', command: () => dispatch(logout())}]} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const MenubarWrapper = (props) => {
  const {
    model, start, end, className, style, onMount, onUnmount,
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
    model,
    start,
    end,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <Menubar {...primeReactProps} />
  );
};

MenubarWrapper.displayName = 'MenubarWrapper';

export default MenubarWrapper;
