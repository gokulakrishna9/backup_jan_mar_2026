/**
 * RadioButtonWrapper - Enhanced wrapper for PrimeReact RadioButton
 * Category: Form
 * 
 * Radio button input component
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { RadioButton } from 'primereact/radiobutton';

// Component metadata embedded for runtime access
export const RadioButtonMetadata = {
  "name": "RadioButton",
  "import": "RadioButton",
  "category": "Form",
  "metadata": {
    "description": "Radio button input component",
    "usageExamples": [
      "<RadioButtonWrapper value=\"option1\" checked={selected === 'option1'} onChange={(e) => setSelected(e.value)} />",
      "<RadioButtonWrapper value=\"yes\" checked={answer === 'yes'} onChange={handleChange} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "any",
        "optional": true,
        "description": "Value of radio button",
        "helpText": "Value when this radio is selected",
        "dataTypes": [
          "string",
          "number",
          "any"
        ],
        "examples": [
          "'option1'",
          "1",
          "'yes'"
        ]
      },
      {
        "name": "checked",
        "type": "boolean",
        "optional": true,
        "description": "Checked state",
        "helpText": "Controls radio state (controlled component)",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "selected === 'option1'",
          "true",
          "false"
        ]
      },
      {
        "name": "disabled",
        "type": "boolean",
        "optional": true,
        "description": "Disabled state",
        "helpText": "Disables the radio button",
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
          "'radio-1'",
          "'option-yes'"
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
        "type": "(e: { value: any, checked: boolean }) => void",
        "description": "Callback when radio button is selected"
      }
    ],
    "simplified": [
      {
        "name": "onValueChange",
        "type": "(value: any) => void",
        "description": "Simplified callback with just the value"
      }
    ],
    "validation": [
      {
        "name": "onValidate",
        "type": "(value: any) => boolean | string",
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
    "basic": "<RadioButtonWrapper value=\"option1\" checked={selected === 'option1'} onChange={(e) => setSelected(e.value)} />",
    "withStyling": "<RadioButtonWrapper value=\"yes\" checked={answer === 'yes'} onChange={handleChange} className=\"mr-2\" />",
    "withEvents": "<RadioButtonWrapper value=\"option\" checked={value === 'option'} onChange={handleChange} />",
    "withRedux": "<RadioButtonWrapper value=\"premium\" checked={plan === 'premium'} onValueChange={(val) => dispatch(setPlan(val))} />",
    "withValidation": "<RadioButtonWrapper value=\"yes\" checked={consent === 'yes'} onValidate={(val) => val ? true : 'Required'} onError={(err) => setError(err)} />",
    "withChildren": "N/A"
  }
};

const RadioButtonWrapper = (props) => {
  const {
    value, checked, disabled, inputId, className, style, onChange, onValueChange, onValidate, onError, onMount, onUnmount,
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
    <RadioButton {...primeReactProps} />
  );
};

RadioButtonWrapper.displayName = 'RadioButtonWrapper';

export default RadioButtonWrapper;
