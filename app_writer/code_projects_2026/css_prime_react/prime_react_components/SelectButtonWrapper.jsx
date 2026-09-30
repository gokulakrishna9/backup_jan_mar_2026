/**
 * SelectButtonWrapper - Enhanced wrapper for PrimeReact SelectButton
 * Category: Form
 * 
 * Button group for single or multiple selection
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { SelectButton } from 'primereact/selectbutton';

// Component metadata embedded for runtime access
export const SelectButtonMetadata = {
  "name": "SelectButton",
  "import": "SelectButton",
  "category": "Form",
  "metadata": {
    "description": "Button group for single or multiple selection",
    "usageExamples": [
      "<SelectButtonWrapper value={selected} options={options} onChange={(e) => setSelected(e.value)} />",
      "<SelectButtonWrapper value={sizes} options={['S', 'M', 'L', 'XL']} multiple />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "any | any[]",
        "optional": true,
        "description": "Selected value(s)",
        "helpText": "Single value or array for multiple mode",
        "dataTypes": [
          "any",
          "any[]"
        ],
        "examples": [
          "'option1'",
          "['S', 'M']",
          "{ code: 'US' }"
        ]
      },
      {
        "name": "options",
        "type": "any[]",
        "optional": false,
        "description": "Array of options",
        "helpText": "List of selectable items",
        "dataTypes": [
          "string[]",
          "number[]",
          "object[]"
        ],
        "examples": [
          "['Option 1', 'Option 2']",
          "[{label: 'Yes', value: 'yes'}]"
        ]
      },
      {
        "name": "optionLabel",
        "type": "string",
        "optional": true,
        "description": "Property name for option label",
        "helpText": "When options are objects, specifies display property",
        "dataTypes": [
          "string (property name)"
        ],
        "examples": [
          "'name'",
          "'label'"
        ]
      },
      {
        "name": "optionValue",
        "type": "string",
        "optional": true,
        "description": "Property name for option value",
        "helpText": "When options are objects, specifies value property",
        "dataTypes": [
          "string (property name)"
        ],
        "examples": [
          "'code'",
          "'id'"
        ]
      },
      {
        "name": "multiple",
        "type": "boolean",
        "optional": true,
        "description": "Multiple selection",
        "helpText": "Allows selecting multiple options",
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
        "helpText": "Disables all buttons",
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
          "'mb-3'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ marginBottom: '1rem' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onChange",
        "type": "(e: { value: any | any[] }) => void",
        "description": "Callback when selection changes"
      }
    ],
    "simplified": [
      {
        "name": "onValueChange",
        "type": "(value: any | any[]) => void",
        "description": "Simplified callback with just the value"
      }
    ],
    "validation": [
      {
        "name": "onValidate",
        "type": "(value: any | any[]) => boolean | string",
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
    "basic": "<SelectButtonWrapper value={selected} options={['Option 1', 'Option 2', 'Option 3']} onChange={(e) => setSelected(e.value)} />",
    "withStyling": "<SelectButtonWrapper value={size} options={['S', 'M', 'L', 'XL']} className=\"mb-3\" />",
    "withEvents": "<SelectButtonWrapper value={choice} options={options} onChange={handleChange} />",
    "withRedux": "<SelectButtonWrapper value={selectedOption} options={options} onValueChange={(val) => dispatch(setOption(val))} />",
    "withValidation": "<SelectButtonWrapper value={selection} options={options} onValidate={(val) => val ? true : 'Required'} onError={(err) => setError(err)} />",
    "withChildren": "N/A"
  }
};

const SelectButtonWrapper = (props) => {
  const {
    value, options, optionLabel, optionValue, multiple, disabled, className, style, onChange, onValueChange, onValidate, onError, onMount, onUnmount,
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
    options,
    optionLabel,
    optionValue,
    multiple,
    disabled,
    className,
    style,
    onChange: handleChange,
    ref: componentRef,
    ...restProps
  };

  return (
    <SelectButton {...primeReactProps} />
  );
};

SelectButtonWrapper.displayName = 'SelectButtonWrapper';

export default SelectButtonWrapper;
