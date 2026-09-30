/**
 * InputSwitchWrapper - Enhanced wrapper for PrimeReact InputSwitch
 * Category: Form
 * 
 * Toggle switch input
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { InputSwitch } from 'primereact/inputswitch';

// Component metadata embedded for runtime access
export const InputSwitchMetadata = {
  "name": "InputSwitch",
  "import": "InputSwitch",
  "category": "Form",
  "metadata": {
    "description": "Toggle switch input",
    "usageExamples": [
      "<InputSwitchWrapper checked={checked} onChange={(e) => setChecked(e.value)} />",
      "<InputSwitchWrapper checked={enabled} onChange={handleChange} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "checked",
        "type": "boolean",
        "optional": true,
        "description": "Checked state",
        "helpText": "Controls switch state (controlled component)",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false",
          "isEnabled"
        ]
      },
      {
        "name": "disabled",
        "type": "boolean",
        "optional": true,
        "description": "Disabled state",
        "helpText": "Disables the switch",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "inputId",
        "type": "string",
        "optional": true,
        "description": "Input element ID",
        "helpText": "For label association",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'switch-1'",
          "'toggle-enabled'"
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
          "'mr-2'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ marginRight: '0.5rem' }"
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
        "description": "Callback when switch state changes"
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
    "basic": "<InputSwitchWrapper checked={checked} onChange={(e) => setChecked(e.value)} />",
    "withStyling": "<InputSwitchWrapper checked={enabled} onChange={handleChange} className=\"mr-2\" />",
    "withEvents": "<InputSwitchWrapper checked={active} onChange={handleChange} />",
    "withRedux": "<InputSwitchWrapper checked={isEnabled} onCheckedChange={(val) => dispatch(setEnabled(val))} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const InputSwitchWrapper = (props) => {
  const {
    checked, disabled, inputId, className, style, onChange, onCheckedChange, onMount, onUnmount,
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
    disabled,
    inputId,
    className,
    style,
    onChange: handleChange,
    ref: componentRef,
    ...restProps
  };

  return (
    <InputSwitch {...primeReactProps} />
  );
};

InputSwitchWrapper.displayName = 'InputSwitchWrapper';

export default InputSwitchWrapper;
