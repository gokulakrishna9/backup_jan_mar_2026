/**
 * SplitButtonWrapper - Enhanced wrapper for PrimeReact SplitButton
 * Category: Button
 * 
 * Button with dropdown menu
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { SplitButton } from 'primereact/splitbutton';

// Component metadata embedded for runtime access
export const SplitButtonMetadata = {
  "name": "SplitButton",
  "import": "SplitButton",
  "category": "Button",
  "metadata": {
    "description": "Button with dropdown menu",
    "usageExamples": [
      "<SplitButtonWrapper label=\"Save\" model={items} onClick={handleSave} />",
      "<SplitButtonWrapper label=\"Actions\" icon=\"pi pi-plus\" model={menuItems} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "label",
        "type": "string",
        "optional": true,
        "description": "Button label",
        "helpText": "Text on main button",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'Save'",
          "'Actions'",
          "'Submit'"
        ]
      },
      {
        "name": "icon",
        "type": "string",
        "optional": true,
        "description": "Button icon",
        "helpText": "PrimeIcons class name",
        "dataTypes": [
          "string (PrimeIcons class)"
        ],
        "examples": [
          "'pi pi-check'",
          "'pi pi-plus'"
        ]
      },
      {
        "name": "model",
        "type": "MenuItem[]",
        "optional": false,
        "description": "Menu items",
        "helpText": "Array of menu item objects",
        "dataTypes": [
          "MenuItem[] - {label, icon, command, url, items}"
        ],
        "examples": [
          "[{label: 'Update', icon: 'pi pi-refresh', command: () => {}}]"
        ]
      },
      {
        "name": "disabled",
        "type": "boolean",
        "optional": true,
        "description": "Disabled state",
        "helpText": "Disables the button",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "severity",
        "type": "'success' | 'info' | 'warning' | 'danger' | 'help' | 'secondary' | 'contrast' | null",
        "optional": true,
        "description": "Button severity",
        "helpText": "Color scheme",
        "dataTypes": [
          "'success'",
          "'info'",
          "'warning'",
          "'danger'"
        ],
        "examples": [
          "'success'",
          "'danger'"
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
          "'mb-2'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ marginBottom: '0.5rem' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onClick",
        "type": "(e: React.MouseEvent) => void",
        "description": "Callback when main button is clicked"
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
      "Check if event handler exists before calling",
      "Menu items have their own command callbacks"
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
    "basic": "<SplitButtonWrapper label=\"Save\" model={[{label: 'Update', command: () => {}}]} onClick={handleSave} />",
    "withStyling": "<SplitButtonWrapper label=\"Actions\" icon=\"pi pi-plus\" model={items} severity=\"success\" className=\"mb-2\" />",
    "withEvents": "<SplitButtonWrapper label=\"Submit\" model={menuItems} onClick={handleSubmit} />",
    "withRedux": "<SplitButtonWrapper label=\"Save\" model={items} onClick={() => dispatch(saveData())} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const SplitButtonWrapper = (props) => {
  const {
    label, icon, model, disabled, severity, className, style, onClick, onMount, onUnmount,
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
    label,
    icon,
    model,
    disabled,
    severity,
    className,
    style,
    onClick,
    ref: componentRef,
    ...restProps
  };

  return (
    <SplitButton {...primeReactProps} />
  );
};

SplitButtonWrapper.displayName = 'SplitButtonWrapper';

export default SplitButtonWrapper;
