/**
 * SpeedDialWrapper - Enhanced wrapper for PrimeReact SpeedDial
 * Category: Button
 * 
 * Floating action button with menu
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { SpeedDial } from 'primereact/speeddial';

// Component metadata embedded for runtime access
export const SpeedDialMetadata = {
  "name": "SpeedDial",
  "import": "SpeedDial",
  "category": "Button",
  "metadata": {
    "description": "Floating action button with menu",
    "usageExamples": [
      "<SpeedDialWrapper model={items} />",
      "<SpeedDialWrapper model={actions} direction=\"up\" type=\"circle\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "model",
        "type": "MenuItem[]",
        "optional": false,
        "description": "Menu items",
        "helpText": "Array of action items",
        "dataTypes": [
          "MenuItem[] - {label, icon, command}"
        ],
        "examples": [
          "[{label: 'Add', icon: 'pi pi-plus', command: () => {}}]"
        ]
      },
      {
        "name": "direction",
        "type": "'up' | 'down' | 'left' | 'right' | 'up-left' | 'up-right' | 'down-left' | 'down-right'",
        "optional": true,
        "description": "Menu direction",
        "helpText": "Direction items expand",
        "dataTypes": [
          "'up' (default)",
          "'down'",
          "'left'",
          "'right'"
        ],
        "examples": [
          "'up'",
          "'right'"
        ]
      },
      {
        "name": "type",
        "type": "'linear' | 'circle' | 'semi-circle' | 'quarter-circle'",
        "optional": true,
        "description": "Menu type",
        "helpText": "Layout pattern",
        "dataTypes": [
          "'linear' (default)",
          "'circle'",
          "'semi-circle'"
        ],
        "examples": [
          "'linear'",
          "'circle'"
        ]
      },
      {
        "name": "radius",
        "type": "number",
        "optional": true,
        "description": "Radius",
        "helpText": "Radius for circle types (default: 0)",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "0",
          "80",
          "100"
        ]
      },
      {
        "name": "visible",
        "type": "boolean",
        "optional": true,
        "description": "Visibility",
        "helpText": "Controls visibility (controlled component)",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "showIcon",
        "type": "string",
        "optional": true,
        "description": "Show icon",
        "helpText": "Icon when menu is closed",
        "dataTypes": [
          "string (PrimeIcons class)"
        ],
        "examples": [
          "'pi pi-plus'",
          "'pi pi-bars'"
        ]
      },
      {
        "name": "hideIcon",
        "type": "string",
        "optional": true,
        "description": "Hide icon",
        "helpText": "Icon when menu is open",
        "dataTypes": [
          "string (PrimeIcons class)"
        ],
        "examples": [
          "'pi pi-times'"
        ]
      },
      {
        "name": "buttonClassName",
        "type": "string",
        "optional": true,
        "description": "Button CSS class",
        "helpText": "Class for main button",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'p-button-danger'"
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
          "'custom-speeddial'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ position: 'fixed', bottom: '20px', right: '20px' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onVisibleChange",
        "type": "(visible: boolean) => void",
        "description": "Callback when visibility changes"
      },
      {
        "name": "onShow",
        "type": "() => void",
        "description": "Callback when menu is shown"
      },
      {
        "name": "onHide",
        "type": "() => void",
        "description": "Callback when menu is hidden"
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
      "handleVisibleChange - Processes onVisibleChange event",
      "handleShow - Processes onShow event",
      "handleHide - Processes onHide event"
    ],
    "patterns": [
      "Check if event handler exists before calling",
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
    "basic": "<SpeedDialWrapper model={[{label: 'Add', icon: 'pi pi-plus', command: () => {}}]} />",
    "withStyling": "<SpeedDialWrapper model={items} direction=\"up\" type=\"circle\" style={{ position: 'fixed', bottom: '20px', right: '20px' }} />",
    "withEvents": "<SpeedDialWrapper model={actions} onShow={() => console.log('shown')} onHide={() => console.log('hidden')} />",
    "withRedux": "<SpeedDialWrapper model={[{label: 'Save', command: () => dispatch(save())}]} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const SpeedDialWrapper = (props) => {
  const {
    model, direction, type, radius, visible, showIcon, hideIcon, buttonClassName, className, style, onVisibleChange, onShow, onHide, onMount, onUnmount,
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
    direction,
    type,
    radius,
    visible,
    showIcon,
    hideIcon,
    buttonClassName,
    className,
    style,
    onVisibleChange,
    onShow,
    onHide,
    ref: componentRef,
    ...restProps
  };

  return (
    <SpeedDial {...primeReactProps} />
  );
};

SpeedDialWrapper.displayName = 'SpeedDialWrapper';

export default SpeedDialWrapper;
