/**
 * PanelMenuWrapper - Enhanced wrapper for PrimeReact PanelMenu
 * Category: Menu
 * 
 * Vertical accordion menu
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { PanelMenu } from 'primereact/panelmenu';

// Component metadata embedded for runtime access
export const PanelMenuMetadata = {
  "name": "PanelMenu",
  "import": "PanelMenu",
  "category": "Menu",
  "metadata": {
    "description": "Vertical accordion menu",
    "usageExamples": [
      "<PanelMenuWrapper model={items} />",
      "<PanelMenuWrapper model={menuItems} multiple />"
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
          "MenuItem[] - {label, icon, command, url, items, expanded}"
        ],
        "examples": [
          "[{label: 'File', items: [{label: 'New'}]}]"
        ]
      },
      {
        "name": "multiple",
        "type": "boolean",
        "optional": true,
        "description": "Multiple panels open",
        "helpText": "Allows multiple panels to be expanded simultaneously",
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
          "'w-full'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ width: '15rem' }"
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
    "childrenDescription": "This component does not accept children - items defined via model prop",
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
    "basic": "<PanelMenuWrapper model={[{label: 'File', items: [{label: 'New', command: () => {}}]}]} />",
    "withStyling": "<PanelMenuWrapper model={items} multiple className=\"w-full\" style={{ width: '15rem' }} />",
    "withEvents": "<PanelMenuWrapper model={[{label: 'Save', command: () => handleSave()}]} />",
    "withRedux": "<PanelMenuWrapper model={[{label: 'Logout', command: () => dispatch(logout())}]} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const PanelMenuWrapper = (props) => {
  const {
    model, multiple, className, style, onMount, onUnmount,
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
    multiple,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <PanelMenu {...primeReactProps} />
  );
};

PanelMenuWrapper.displayName = 'PanelMenuWrapper';

export default PanelMenuWrapper;
