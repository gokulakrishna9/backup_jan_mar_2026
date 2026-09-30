/**
 * TieredMenuWrapper - Enhanced wrapper for PrimeReact TieredMenu
 * Category: Menu
 * 
 * Nested overlay menu
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { TieredMenu } from 'primereact/tieredmenu';

// Component metadata embedded for runtime access
export const TieredMenuMetadata = {
  "name": "TieredMenu",
  "import": "TieredMenu",
  "category": "Menu",
  "metadata": {
    "description": "Nested overlay menu",
    "usageExamples": [
      "<TieredMenuWrapper model={items} />",
      "<TieredMenuWrapper model={menuItems} popup ref={menuRef} />"
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
          "MenuItem[] - {label, icon, command, url, items, separator}"
        ],
        "examples": [
          "[{label: 'File', items: [{label: 'New'}]}]"
        ]
      },
      {
        "name": "popup",
        "type": "boolean",
        "optional": true,
        "description": "Popup mode",
        "helpText": "Menu appears as overlay (use with ref)",
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
        "type": "'self' | HTMLElement | null",
        "optional": true,
        "description": "Append target",
        "helpText": "Element to append menu to",
        "dataTypes": [
          "'self'",
          "HTMLElement",
          "null"
        ],
        "examples": [
          "'self'",
          "document.body"
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
    "internal": [
      "show - Method to display popup menu (when popup=true)",
      "hide - Method to hide popup menu",
      "toggle - Method to toggle popup menu"
    ],
    "patterns": [
      "Use ref to access menu methods",
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
    "basic": "<TieredMenuWrapper model={[{label: 'File', items: [{label: 'New'}]}]} />",
    "withStyling": "<TieredMenuWrapper model={items} className=\"w-full\" style={{ width: '15rem' }} />",
    "withEvents": "const menu = useRef(null); <TieredMenuWrapper model={items} popup ref={menu} />; menu.current.toggle(event);",
    "withRedux": "<TieredMenuWrapper model={[{label: 'Save', command: () => dispatch(save())}]} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const TieredMenuWrapper = (props) => {
  const {
    model, popup, appendTo, className, style, onMount, onUnmount,
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
    popup,
    appendTo,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <TieredMenu {...primeReactProps} />
  );
};

TieredMenuWrapper.displayName = 'TieredMenuWrapper';

export default TieredMenuWrapper;
