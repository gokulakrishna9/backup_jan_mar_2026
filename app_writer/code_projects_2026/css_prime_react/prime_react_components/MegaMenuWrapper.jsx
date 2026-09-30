/**
 * MegaMenuWrapper - Enhanced wrapper for PrimeReact MegaMenu
 * Category: Menu
 * 
 * Large menu with grouped items
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { MegaMenu } from 'primereact/megamenu';

// Component metadata embedded for runtime access
export const MegaMenuMetadata = {
  "name": "MegaMenu",
  "import": "MegaMenu",
  "category": "Menu",
  "metadata": {
    "description": "Large menu with grouped items",
    "usageExamples": [
      "<MegaMenuWrapper model={items} />",
      "<MegaMenuWrapper model={menuItems} orientation=\"vertical\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "model",
        "type": "MenuItem[]",
        "optional": false,
        "description": "Menu items",
        "helpText": "Array of menu item objects with nested items in columns",
        "dataTypes": [
          "MenuItem[] - {label, icon, items (array of columns)}"
        ],
        "examples": [
          "[{label: 'Products', items: [[{label: 'Electronics'}], [{label: 'Clothing'}]]}]"
        ]
      },
      {
        "name": "orientation",
        "type": "'horizontal' | 'vertical'",
        "optional": true,
        "description": "Menu orientation",
        "helpText": "Direction of menu",
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
        "name": "start",
        "type": "React.ReactNode",
        "optional": true,
        "description": "Start content",
        "helpText": "Content at start of menu",
        "dataTypes": [
          "React.ReactNode"
        ],
        "examples": [
          "<img src=\"logo.png\" />"
        ]
      },
      {
        "name": "end",
        "type": "React.ReactNode",
        "optional": true,
        "description": "End content",
        "helpText": "Content at end of menu",
        "dataTypes": [
          "React.ReactNode"
        ],
        "examples": [
          "<Button label=\"Login\" />"
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
      "Menu items have their own command callbacks",
      "Items array contains arrays of columns for mega menu layout"
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
    "basic": "<MegaMenuWrapper model={[{label: 'Products', items: [[{label: 'Electronics'}], [{label: 'Clothing'}]]}]} />",
    "withStyling": "<MegaMenuWrapper model={items} orientation=\"vertical\" className=\"mb-3\" />",
    "withEvents": "<MegaMenuWrapper model={[{label: 'Save', command: () => handleSave()}]} />",
    "withRedux": "<MegaMenuWrapper model={menuItems} start={<img src=\"logo.png\" />} end={<Button label=\"Logout\" onClick={() => dispatch(logout())} />} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const MegaMenuWrapper = (props) => {
  const {
    model, orientation, start, end, className, style, onMount, onUnmount,
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
    orientation,
    start,
    end,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <MegaMenu {...primeReactProps} />
  );
};

MegaMenuWrapper.displayName = 'MegaMenuWrapper';

export default MegaMenuWrapper;
