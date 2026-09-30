/**
 * InputMaskWrapper - Enhanced wrapper for PrimeReact InputMask
 * Category: Form
 * 
 * Masked input for formatted data
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { InputMask } from 'primereact/inputmask';

// Component metadata embedded for runtime access
export const InputMaskMetadata = {
  "name": "InputMask",
  "import": "InputMask",
  "category": "Form",
  "metadata": {
    "description": "Masked input for formatted data",
    "usageExamples": [
      "<InputMaskWrapper value={phone} mask=\"(999) 999-9999\" onChange={(e) => setPhone(e.value)} />",
      "<InputMaskWrapper value={ssn} mask=\"999-99-9999\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "string",
        "optional": true,
        "description": "Input value",
        "helpText": "Current value (controlled component)",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'(555) 123-4567'",
          "'123-45-6789'"
        ]
      },
      {
        "name": "mask",
        "type": "string",
        "optional": false,
        "description": "Input mask pattern",
        "helpText": "9=digit, a=letter, *=alphanumeric",
        "dataTypes": [
          "string (mask pattern)"
        ],
        "examples": [
          "'(999) 999-9999'",
          "'99/99/9999'",
          "'aa-999999'"
        ]
      },
      {
        "name": "placeholder",
        "type": "string",
        "optional": true,
        "description": "Placeholder text",
        "helpText": "Text shown when empty",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'(___) ___-____'",
          "'Enter phone'"
        ]
      },
      {
        "name": "slotChar",
        "type": "string",
        "optional": true,
        "description": "Slot character",
        "helpText": "Character for empty positions (default: _)",
        "dataTypes": [
          "string (single char)"
        ],
        "examples": [
          "'_'",
          "' '"
        ]
      },
      {
        "name": "autoClear",
        "type": "boolean",
        "optional": true,
        "description": "Auto clear incomplete",
        "helpText": "Clears incomplete input on blur",
        "dataTypes": [
          "boolean (default: true)"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "unmask",
        "type": "boolean",
        "optional": true,
        "description": "Return unmasked value",
        "helpText": "Returns value without mask characters",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "disabled",
        "type": "boolean",
        "optional": true,
        "description": "Disabled state",
        "helpText": "Disables the input",
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
          "'w-full'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ width: '100%' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onChange",
        "type": "(e: { value: string, target: { value: string } }) => void",
        "description": "Callback when value changes"
      },
      {
        "name": "onComplete",
        "type": "(e: { value: string }) => void",
        "description": "Callback when mask is fully filled"
      },
      {
        "name": "onFocus",
        "type": "(e: React.FocusEvent) => void",
        "description": "Callback when input gains focus"
      },
      {
        "name": "onBlur",
        "type": "(e: React.FocusEvent) => void",
        "description": "Callback when input loses focus"
      }
    ],
    "simplified": [
      {
        "name": "onValueChange",
        "type": "(value: string) => void",
        "description": "Simplified callback with just the value"
      }
    ],
    "validation": [
      {
        "name": "onValidate",
        "type": "(value: string) => boolean | string",
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
      "handleChange - Processes onChange event, calls onChange, onValueChange, onValidate",
      "handleComplete - Processes onComplete event",
      "handleFocus - Processes onFocus event",
      "handleBlur - Processes onBlur event, triggers validation"
    ],
    "patterns": [
      "Check if event handler exists before calling",
      "Extract value from event object",
      "Run validation on blur and complete events"
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
    "basic": "<InputMaskWrapper value={phone} mask=\"(999) 999-9999\" onChange={(e) => setPhone(e.value)} />",
    "withStyling": "<InputMaskWrapper value={ssn} mask=\"999-99-9999\" className=\"w-full\" />",
    "withEvents": "<InputMaskWrapper value={phone} mask=\"(999) 999-9999\" onChange={handleChange} onComplete={handleComplete} />",
    "withRedux": "<InputMaskWrapper value={phoneNumber} mask=\"(999) 999-9999\" onValueChange={(val) => dispatch(setPhone(val))} />",
    "withValidation": "<InputMaskWrapper value={phone} mask=\"(999) 999-9999\" onValidate={(val) => val.length > 0 ? true : 'Required'} onError={(err) => setError(err)} />",
    "withChildren": "N/A"
  }
};

const InputMaskWrapper = (props) => {
  const {
    value, mask, placeholder, slotChar, autoClear, unmask, disabled, className, style, onChange, onComplete, onFocus, onBlur, onValueChange, onValidate, onError, onMount, onUnmount,
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
    mask,
    placeholder,
    slotChar,
    autoClear,
    unmask,
    disabled,
    className,
    style,
    onChange: handleChange,
    onComplete,
    onFocus,
    onBlur,
    ref: componentRef,
    ...restProps
  };

  return (
    <InputMask {...primeReactProps} />
  );
};

InputMaskWrapper.displayName = 'InputMaskWrapper';

export default InputMaskWrapper;
