/**
 * InputNumberWrapper - Enhanced wrapper for PrimeReact InputNumber
 * Category: Form
 * 
 * Numeric input with increment/decrement buttons
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { InputNumber } from 'primereact/inputnumber';

// Component metadata embedded for runtime access
export const InputNumberMetadata = {
  "name": "InputNumber",
  "import": "InputNumber",
  "category": "Form",
  "metadata": {
    "description": "Numeric input with increment/decrement buttons",
    "usageExamples": [
      "<InputNumberWrapper value={quantity} onValueChange={(e) => setQuantity(e.value)} />",
      "<InputNumberWrapper value={price} mode=\"currency\" currency=\"USD\" locale=\"en-US\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "number | null",
        "optional": true,
        "description": "Numeric value",
        "helpText": "Current number (controlled component)",
        "dataTypes": [
          "number",
          "null"
        ],
        "examples": [
          "10",
          "99.99",
          "null"
        ]
      },
      {
        "name": "mode",
        "type": "'decimal' | 'currency'",
        "optional": true,
        "description": "Input mode",
        "helpText": "decimal=plain number, currency=formatted money",
        "dataTypes": [
          "'decimal' (default)",
          "'currency'"
        ],
        "examples": [
          "'decimal'",
          "'currency'"
        ]
      },
      {
        "name": "currency",
        "type": "string",
        "optional": true,
        "description": "Currency code",
        "helpText": "ISO currency code (for currency mode)",
        "dataTypes": [
          "string (ISO code)"
        ],
        "examples": [
          "'USD'",
          "'EUR'",
          "'GBP'"
        ]
      },
      {
        "name": "locale",
        "type": "string",
        "optional": true,
        "description": "Locale",
        "helpText": "Locale for formatting",
        "dataTypes": [
          "string (locale code)"
        ],
        "examples": [
          "'en-US'",
          "'de-DE'",
          "'fr-FR'"
        ]
      },
      {
        "name": "min",
        "type": "number",
        "optional": true,
        "description": "Minimum value",
        "helpText": "Lowest allowed value",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "0",
          "1",
          "-100"
        ]
      },
      {
        "name": "max",
        "type": "number",
        "optional": true,
        "description": "Maximum value",
        "helpText": "Highest allowed value",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "100",
          "999",
          "1000"
        ]
      },
      {
        "name": "step",
        "type": "number",
        "optional": true,
        "description": "Step increment",
        "helpText": "Amount to increment/decrement",
        "dataTypes": [
          "number (default: 1)"
        ],
        "examples": [
          "1",
          "0.1",
          "5"
        ]
      },
      {
        "name": "showButtons",
        "type": "boolean",
        "optional": true,
        "description": "Show +/- buttons",
        "helpText": "Displays increment/decrement buttons",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "buttonLayout",
        "type": "'stacked' | 'horizontal' | 'vertical'",
        "optional": true,
        "description": "Button layout",
        "helpText": "Position of +/- buttons",
        "dataTypes": [
          "'stacked'",
          "'horizontal'",
          "'vertical'"
        ],
        "examples": [
          "'stacked'",
          "'horizontal'"
        ]
      },
      {
        "name": "prefix",
        "type": "string",
        "optional": true,
        "description": "Prefix text",
        "helpText": "Text before value",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'$'",
          "'#'"
        ]
      },
      {
        "name": "suffix",
        "type": "string",
        "optional": true,
        "description": "Suffix text",
        "helpText": "Text after value",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "' kg'",
          "'%'"
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
          "'Enter amount'",
          "'0'"
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
        "name": "onValueChange",
        "type": "(e: { value: number | null }) => void",
        "description": "Callback when value changes"
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
        "name": "onNumberChange",
        "type": "(value: number | null) => void",
        "description": "Simplified callback with just the number"
      }
    ],
    "validation": [
      {
        "name": "onValidate",
        "type": "(value: number | null) => boolean | string",
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
      "handleValueChange - Processes onValueChange event, calls onValueChange, onNumberChange, onValidate",
      "handleFocus - Processes onFocus event",
      "handleBlur - Processes onBlur event, triggers validation"
    ],
    "patterns": [
      "Check if event handler exists before calling",
      "Extract value from event object",
      "Run validation on blur and change events"
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
    "basic": "<InputNumberWrapper value={quantity} onValueChange={(e) => setQuantity(e.value)} />",
    "withStyling": "<InputNumberWrapper value={price} mode=\"currency\" currency=\"USD\" locale=\"en-US\" className=\"w-full\" />",
    "withEvents": "<InputNumberWrapper value={amount} onValueChange={handleChange} onBlur={handleBlur} />",
    "withRedux": "<InputNumberWrapper value={count} onNumberChange={(val) => dispatch(setCount(val))} />",
    "withValidation": "<InputNumberWrapper value={age} min={0} max={120} onValidate={(val) => val && val > 0 ? true : 'Must be positive'} onError={(err) => setError(err)} />",
    "withChildren": "N/A"
  }
};

const InputNumberWrapper = (props) => {
  const {
    value, mode, currency, locale, min, max, step, showButtons, buttonLayout, prefix, suffix, placeholder, disabled, className, style, onValueChange, onFocus, onBlur, onNumberChange, onValidate, onError, onMount, onUnmount,
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
    value,
    mode,
    currency,
    locale,
    min,
    max,
    step,
    showButtons,
    buttonLayout,
    prefix,
    suffix,
    placeholder,
    disabled,
    className,
    style,
    onValueChange,
    onFocus,
    onBlur,
    ref: componentRef,
    ...restProps
  };

  return (
    <InputNumber {...primeReactProps} />
  );
};

InputNumberWrapper.displayName = 'InputNumberWrapper';

export default InputNumberWrapper;
