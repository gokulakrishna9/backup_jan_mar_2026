/**
 * ToggleButtonWrapper - Enhanced wrapper for PrimeReact ToggleButton
 * Category: Button
 * 
 * Two-state button
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { ToggleButton } from 'primereact/togglebutton';

// Component metadata embedded for runtime access
export const ToggleButtonMetadata = {
  "name": "ToggleButton",
  "import": "ToggleButton",
  "category": "Button",
  "metadata": {
    "description": "Two-state button",
    "usageExamples": [
      "<ToggleButtonWrapper checked={checked} onChange={(e) => setChecked(e.value)} />",
      "<ToggleButtonWrapper checked={active} onLabel=\"Yes\" offLabel=\"No\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "checked",
        "type": "boolean",
        "optional": true,
        "description": "Checked state",
        "helpText": "Controls toggle state (controlled component)",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false",
          "isActive"
        ]
      },
      {
        "name": "onLabel",
        "type": "string",
        "optional": true,
        "description": "Label when checked",
        "helpText": "Text shown when toggle is on",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'Yes'",
          "'On'",
          "'Active'"
        ]
      },
      {
        "name": "offLabel",
        "type": "string",
        "optional": true,
        "description": "Label when unchecked",
        "helpText": "Text shown when toggle is off",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'No'",
          "'Off'",
          "'Inactive'"
        ]
      },
      {
        "name": "onIcon",
        "type": "string",
        "optional": true,
        "description": "Icon when checked",
        "helpText": "PrimeIcons class for on state",
        "dataTypes": [
          "string (PrimeIcons class)"
        ],
        "examples": [
          "'pi pi-check'",
          "'pi pi-thumbs-up'"
        ]
      },
      {
        "name": "offIcon",
        "type": "string",
        "optional": true,
        "description": "Icon when unchecked",
        "helpText": "PrimeIcons class for off state",
        "dataTypes": [
          "string (PrimeIcons class)"
        ],
        "examples": [
          "'pi pi-times'",
          "'pi pi-thumbs-down'"
        ]
      },
      {
        "name": "disabled",
        "type": "boolean",
        "optional": true,
        "description": "Disabled state",
        "helpText": "Disables the toggle button",
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
          "'w-8rem'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ width: '8rem' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onChange",
        "type": "(e: { value: boolean, target: { value: boolean } }) => void",
        "description": "Callback when toggle state changes"
      }
    ],
    "simplified": [
      {
        "name": "onCheckedChange",
        "type": "(checked: boolean) => void",
        "description": "Simplified callback with just the checked state"
      }
    ],
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
      "handleChange - Processes onChange event, calls onChange and onCheckedChange"
    ],
    "patterns": [
      "Check if event handler exists before calling",
      "Extract checked value from event object"
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
    "basic": "<ToggleButtonWrapper checked={checked} onChange={(e) => setChecked(e.value)} />",
    "withStyling": "<ToggleButtonWrapper checked={active} onLabel=\"Yes\" offLabel=\"No\" className=\"w-8rem\" />",
    "withEvents": "<ToggleButtonWrapper checked={enabled} onChange={handleChange} />",
    "withRedux": "<ToggleButtonWrapper checked={isActive} onCheckedChange={(val) => dispatch(setActive(val))} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const ToggleButtonWrapper = (props) => {
  const {
    checked, onLabel, offLabel, onIcon, offIcon, disabled, className, style, onChange, onCheckedChange, onMount, onUnmount,
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

  // Simplified event handler: onCheckedChange
  const handleChange = (e) => {
    if (onChange) {
      onChange(e);
    }
    if (onCheckedChange) {
      onCheckedChange(e.value || e.data || e);
    }
  };

  // Build props for underlying PrimeReact component
  const primeReactProps = {
    checked,
    onLabel,
    offLabel,
    onIcon,
    offIcon,
    disabled,
    className,
    style,
    onChange: handleChange,
    ref: componentRef,
    ...restProps
  };

  return (
    <ToggleButton {...primeReactProps} />
  );
};

ToggleButtonWrapper.displayName = 'ToggleButtonWrapper';

export default ToggleButtonWrapper;
