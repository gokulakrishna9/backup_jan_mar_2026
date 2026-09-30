/**
 * DockWrapper - Enhanced wrapper for PrimeReact Dock
 * Category: Menu
 * 
 * macOS-style dock menu for application launcher and quick access
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Dock } from 'primereact/dock';

// Component metadata embedded for runtime access
export const DockMetadata = {
  "name": "Dock",
  "import": "Dock",
  "category": "Menu",
  "metadata": {
    "description": "macOS-style dock menu for application launcher and quick access",
    "usageExamples": [
      "<DockWrapper model={dockItems} />",
      "<DockWrapper model={items} position=\"bottom\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "model",
        "type": "MenuItem[]",
        "optional": false,
        "description": "Array of menu items",
        "helpText": "Menu items with label, icon, command properties",
        "dataTypes": [
          "MenuItem[] - { label?: string, icon?: string, command?: () => void, url?: string }"
        ],
        "examples": [
          "[{ label: 'Home', icon: 'pi pi-home', command: () => navigate('/') }]"
        ]
      },
      {
        "name": "position",
        "type": "'bottom' | 'top' | 'left' | 'right'",
        "optional": true,
        "description": "Position of the dock",
        "helpText": "Where to display the dock (default: bottom)",
        "dataTypes": [
          "'bottom'",
          "'top'",
          "'left'",
          "'right'"
        ],
        "examples": [
          "'bottom'",
          "'left'"
        ]
      },
      {
        "name": "magnification",
        "type": "boolean",
        "optional": true,
        "description": "Whether to enable magnification effect",
        "helpText": "macOS-style zoom effect on hover",
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
        "description": "Additional CSS classes for custom styling",
        "helpText": "Supports PrimeFlex utility classes and custom CSS",
        "examples": [
          "'custom-dock'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles object",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ width: '100%' }"
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
        "optional": true,
        "description": "Callback when component mounts"
      }
    ]
  },
  "eventHandlerMethods": {
    "internal": [],
    "patterns": [
      "Use command property in menu items for click handlers",
      "For navigation: Use url property or command with router navigation"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children. Use model prop to define dock items.",
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
    "basic": "<DockWrapper model={dockItems} />",
    "withStyling": "<DockWrapper model={items} className=\"custom-dock\" position=\"bottom\" />",
    "withEvents": "<DockWrapper model={[{ label: 'Home', icon: 'pi pi-home', command: () => navigate('/') }]} />",
    "withRedux": "<DockWrapper model={[{ label: 'Profile', icon: 'pi pi-user', command: () => dispatch(openProfile()) }]} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const DockWrapper = (props) => {
  const {
    model, position, magnification, className, style, onMount,
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
    position,
    magnification,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <Dock {...primeReactProps} />
  );
};

DockWrapper.displayName = 'DockWrapper';

export default DockWrapper;
