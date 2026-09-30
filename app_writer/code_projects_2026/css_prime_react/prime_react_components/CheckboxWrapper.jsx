/**
 * CheckboxWrapper - Enhanced wrapper for PrimeReact Checkbox
 * Category: Form
 * 
 * Checkbox input component
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Checkbox } from 'primereact/checkbox';

// Component metadata embedded for runtime access
export const CheckboxMetadata = {
  "name": "Checkbox",
  "import": "Checkbox",
  "category": "Form",
  "metadata": {
    "description": "Checkbox input component",
    "usageExamples": [
      "<CheckboxWrapper checked={checked} onChange={(e) => setChecked(e.checked)} />",
      "<CheckboxWrapper checked={accepted} onChange={handleChange} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "checked",
        "type": "boolean",
        "optional": true,
        "description": "Checked state",
        "helpText": "Controls checkbox state (controlled component)",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false",
          "isChecked"
        ]
      },
      {
        "name": "disabled",
        "type": "boolean",
        "optional": true,
        "description": "Disabled state",
        "helpText": "Disables the checkbox",
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
          "'accept-terms'",
          "'checkbox-1'"
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
        "type": "(e: { checked: boolean, target: { checked: boolean } }) => void",
        "description": "Callback when checkbox state changes"
      }
    ],
    "simplified": [
      {
        "name": "onCheckedChange",
        "type": "(checked: boolean) => void",
        "description": "Simplified callback with just the checked state"
      }
    ],
    "validation": [
      {
        "name": "onValidate",
        "type": "(checked: boolean) => boolean | string",
        "description": "Validation callback"
      },
      {
        "name": "onError",
        "type": "(error: string) => void",
        "description": "Called when validation fails"
      }
    ],
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
      "handleChange - Processes onChange event, calls onChange, onCheckedChange, onValidate"
    ],
    "patterns": [
      "Check if event handler exists before calling",
      "Extract checked value from event object",
      "Run validation on change"
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
    "basic": "<CheckboxWrapper checked={checked} onChange={(e) => setChecked(e.checked)} />",
    "withStyling": "<CheckboxWrapper checked={accepted} onChange={handleChange} className=\"mr-2\" />",
    "withEvents": "<CheckboxWrapper checked={terms} onChange={handleChange} />",
    "withRedux": "<CheckboxWrapper checked={isAccepted} onCheckedChange={(val) => dispatch(setAccepted(val))} />",
    "withValidation": "<CheckboxWrapper checked={terms} onValidate={(val) => val ? true : 'Must accept terms'} onError={(err) => setError(err)} />",
    "withChildren": "N/A"
  }
};

const CheckboxWrapper = (props) => {
  const {
    checked, disabled, inputId, className, style, onChange, onCheckedChange, onValidate, onError, onMount, onUnmount,
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
    <Checkbox {...primeReactProps} />
  );
};

CheckboxWrapper.displayName = 'CheckboxWrapper';

export default CheckboxWrapper;
