/**
 * SlideMenuWrapper - Enhanced wrapper for PrimeReact SlideMenu
 * Category: Menu
 * 
 * Nested sliding menu for mobile navigation and hierarchical menus
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { SlideMenu } from 'primereact/slidemenu';

// Component metadata embedded for runtime access
export const SlideMenuMetadata = {
  "name": "SlideMenu",
  "import": "SlideMenu",
  "category": "Menu",
  "metadata": {
    "description": "Nested sliding menu for mobile navigation and hierarchical menus",
    "usageExamples": [
      "<SlideMenuWrapper model={menuItems} />",
      "<SlideMenuWrapper model={items} viewportHeight={250} menuWidth={200} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "model",
        "type": "MenuItem[]",
        "optional": false,
        "description": "Array of menu items",
        "helpText": "Hierarchical menu items with label, icon, items, command properties",
        "dataTypes": [
          "MenuItem[] - { label: string, icon?: string, items?: MenuItem[], command?: () => void }"
        ],
        "examples": [
          "[{ label: 'File', items: [{ label: 'New', command: () => {} }] }]"
        ]
      },
      {
        "name": "popup",
        "type": "boolean",
        "optional": true,
        "description": "Whether menu is displayed as popup",
        "helpText": "Enables popup mode (requires ref to toggle)",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "viewportHeight",
        "type": "number",
        "optional": true,
        "description": "Height of the viewport in pixels",
        "helpText": "Visible height of menu content (default: 175)",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "200",
          "300",
          "400"
        ]
      },
      {
        "name": "menuWidth",
        "type": "number",
        "optional": true,
        "description": "Width of the menu in pixels",
        "helpText": "Menu width (default: 190)",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "200",
          "250",
          "300"
        ]
      },
      {
        "name": "backLabel",
        "type": "string",
        "optional": true,
        "description": "Label for back button",
        "helpText": "Text for navigation back button (default: 'Back')",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'Back'",
          "'Return'",
          "'Previous'"
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
          "'custom-slide-menu'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles object",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ width: '250px' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onShow",
        "type": "() => void",
        "optional": true,
        "description": "Callback when menu is shown (popup mode)"
      },
      {
        "name": "onHide",
        "type": "() => void",
        "optional": true,
        "description": "Callback when menu is hidden (popup mode)"
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
      "Use command property in menu items for click handlers",
      "For popup mode: Use ref to control menu visibility with toggle(event)"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children. Use model prop to define menu structure.",
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
    "basic": "<SlideMenuWrapper model={menuItems} />",
    "withStyling": "<SlideMenuWrapper model={items} className=\"custom-menu\" style={{ width: '300px' }} viewportHeight={300} />",
    "withEvents": "<SlideMenuWrapper model={items} popup onShow={() => console.log('Shown')} onHide={() => console.log('Hidden')} />",
    "withRedux": "<SlideMenuWrapper model={menuItems.map(item => ({ ...item, command: () => dispatch(navigate(item.route)) }))} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const SlideMenuWrapper = (props) => {
  const {
    model, popup, viewportHeight, menuWidth, backLabel, className, style, onShow, onHide, onMount,
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
    model,
    popup,
    viewportHeight,
    menuWidth,
    backLabel,
    className,
    style,
    onShow,
    onHide,
    ref: componentRef,
    ...restProps
  };

  return (
    <SlideMenu {...primeReactProps} />
  );
};

SlideMenuWrapper.displayName = 'SlideMenuWrapper';

export default SlideMenuWrapper;
