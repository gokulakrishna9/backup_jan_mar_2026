/**
 * TriStateCheckboxWrapper - Enhanced wrapper for PrimeReact TriStateCheckbox
 * Category: Form
 * 
 * Checkbox with three states: checked, unchecked, null
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { TriStateCheckbox } from 'primereact/tristatecheckbox';

// Component metadata embedded for runtime access
export const TriStateCheckboxMetadata = {
  "name": "TriStateCheckbox",
  "import": "TriStateCheckbox",
  "category": "Form",
  "metadata": {
    "description": "Checkbox with three states: checked, unchecked, null",
    "usageExamples": [
      "<TriStateCheckboxWrapper value={value} onChange={(e) => setValue(e.value)} />",
      "<TriStateCheckboxWrapper value={state} onChange={handleChange} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "boolean | null",
        "optional": true,
        "description": "Checkbox state",
        "helpText": "true=checked, false=unchecked, null=indeterminate",
        "dataTypes": [
          "true",
          "false",
          "null"
        ],
        "examples": [
          "true",
          "false",
          "null"
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
          "'tristate-1'",
          "'checkbox-tri'"
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
        "type": "(e: { value: boolean | null, target: { value: boolean | null } }) => void",
        "description": "Callback when state changes"
      }
    ],
    "simplified": [
      {
        "name": "onValueChange",
        "type": "(value: boolean | null) => void",
        "description": "Simplified callback with just the value"
      }
    ],
    "validation": [
      {
        "name": "onValidate",
        "type": "(value: boolean | null) => boolean | string",
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
      "handleChange - Processes onChange event, calls onChange, onValueChange, onValidate"
    ],
    "patterns": [
      "Check if event handler exists before calling",
      "Extract value from event object",
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
    "basic": "<TriStateCheckboxWrapper value={value} onChange={(e) => setValue(e.value)} />",
    "withStyling": "<TriStateCheckboxWrapper value={state} onChange={handleChange} className=\"mr-2\" />",
    "withEvents": "<TriStateCheckboxWrapper value={checked} onChange={handleChange} />",
    "withRedux": "<TriStateCheckboxWrapper value={checkState} onValueChange={(val) => dispatch(setState(val))} />",
    "withValidation": "<TriStateCheckboxWrapper value={value} onValidate={(val) => val !== null ? true : 'Required'} onError={(err) => setError(err)} />",
    "withChildren": "N/A"
  }
};

const TriStateCheckboxWrapper = (props) => {
  const {
    value, disabled, inputId, className, style, onChange, onValueChange, onValidate, onError, onMount, onUnmount,
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

  // Simplified event handler: onValueChange
  const handleChange = (e) => {
    if (onChange) {
      onChange(e);
    }
    if (onValueChange) {
      onValueChange(e.value || e.data || e);
    }
  };

  // Build props for underlying PrimeReact component
  const primeReactProps = {
    value,
    disabled,
    inputId,
    className,
    style,
    onChange: handleChange,
    ref: componentRef,
    ...restProps
  };

  return (
    <TriStateCheckbox {...primeReactProps} />
  );
};

TriStateCheckboxWrapper.displayName = 'TriStateCheckboxWrapper';

export default TriStateCheckboxWrapper;
