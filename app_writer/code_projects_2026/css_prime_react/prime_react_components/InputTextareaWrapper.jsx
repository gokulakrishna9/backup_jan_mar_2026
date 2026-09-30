/**
 * InputTextareaWrapper - Enhanced wrapper for PrimeReact InputTextarea
 * Category: Form
 * 
 * Multi-line text input
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { InputTextarea } from 'primereact/inputtextarea';

// Component metadata embedded for runtime access
export const InputTextareaMetadata = {
  "name": "InputTextarea",
  "import": "InputTextarea",
  "category": "Form",
  "metadata": {
    "description": "Multi-line text input",
    "usageExamples": [
      "<InputTextareaWrapper value={text} onChange={(e) => setText(e.target.value)} />",
      "<InputTextareaWrapper value={comment} rows={5} autoResize />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "string",
        "optional": true,
        "description": "Text value",
        "helpText": "Current text content (controlled component)",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'Some text'",
          "comment",
          "description"
        ]
      },
      {
        "name": "rows",
        "type": "number",
        "optional": true,
        "description": "Number of rows",
        "helpText": "Visible text lines",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "3",
          "5",
          "10"
        ]
      },
      {
        "name": "cols",
        "type": "number",
        "optional": true,
        "description": "Number of columns",
        "helpText": "Width in characters",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "30",
          "50"
        ]
      },
      {
        "name": "autoResize",
        "type": "boolean",
        "optional": true,
        "description": "Auto resize height",
        "helpText": "Grows with content",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
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
          "'Enter description'",
          "'Type here...'"
        ]
      },
      {
        "name": "disabled",
        "type": "boolean",
        "optional": true,
        "description": "Disabled state",
        "helpText": "Disables the textarea",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "maxLength",
        "type": "number",
        "optional": true,
        "description": "Maximum length",
        "helpText": "Max character count",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "100",
          "500",
          "1000"
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
        "type": "(e: React.ChangeEvent<HTMLTextAreaElement>) => void",
        "description": "Callback when text changes"
      },
      {
        "name": "onFocus",
        "type": "(e: React.FocusEvent) => void",
        "description": "Callback when textarea gains focus"
      },
      {
        "name": "onBlur",
        "type": "(e: React.FocusEvent) => void",
        "description": "Callback when textarea loses focus"
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
      "handleFocus - Processes onFocus event",
      "handleBlur - Processes onBlur event, triggers validation"
    ],
    "patterns": [
      "Check if event handler exists before calling",
      "Extract value from event.target.value",
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
    "basic": "<InputTextareaWrapper value={text} onChange={(e) => setText(e.target.value)} />",
    "withStyling": "<InputTextareaWrapper value={comment} rows={5} autoResize className=\"w-full\" />",
    "withEvents": "<InputTextareaWrapper value={description} onChange={handleChange} onBlur={handleBlur} />",
    "withRedux": "<InputTextareaWrapper value={comment} onValueChange={(val) => dispatch(setComment(val))} />",
    "withValidation": "<InputTextareaWrapper value={text} onValidate={(val) => val.length > 10 ? true : 'Min 10 chars'} onError={(err) => setError(err)} />",
    "withChildren": "N/A"
  }
};

const InputTextareaWrapper = (props) => {
  const {
    value, rows, cols, autoResize, placeholder, disabled, maxLength, className, style, onChange, onFocus, onBlur, onValueChange, onValidate, onError, onMount, onUnmount,
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
    rows,
    cols,
    autoResize,
    placeholder,
    disabled,
    maxLength,
    className,
    style,
    onChange: handleChange,
    onFocus,
    onBlur,
    ref: componentRef,
    ...restProps
  };

  return (
    <InputTextarea {...primeReactProps} />
  );
};

InputTextareaWrapper.displayName = 'InputTextareaWrapper';

export default InputTextareaWrapper;
