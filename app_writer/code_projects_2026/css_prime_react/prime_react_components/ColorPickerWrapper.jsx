/**
 * ColorPickerWrapper - Enhanced wrapper for PrimeReact ColorPicker
 * Category: Form
 * 
 * Color selection input
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { ColorPicker } from 'primereact/colorpicker';

// Component metadata embedded for runtime access
export const ColorPickerMetadata = {
  "name": "ColorPicker",
  "import": "ColorPicker",
  "category": "Form",
  "metadata": {
    "description": "Color selection input",
    "usageExamples": [
      "<ColorPickerWrapper value={color} onChange={(e) => setColor(e.value)} />",
      "<ColorPickerWrapper value={bgColor} format=\"hex\" inline />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "string",
        "optional": true,
        "description": "Color value",
        "helpText": "Current color (controlled component)",
        "dataTypes": [
          "string (hex without #)",
          "string (rgb/hsb object)"
        ],
        "examples": [
          "'1976D2'",
          "'FF5733'"
        ]
      },
      {
        "name": "format",
        "type": "'hex' | 'rgb' | 'hsb'",
        "optional": true,
        "description": "Color format",
        "helpText": "Format for color value",
        "dataTypes": [
          "'hex' (default)",
          "'rgb'",
          "'hsb'"
        ],
        "examples": [
          "'hex'",
          "'rgb'"
        ]
      },
      {
        "name": "inline",
        "type": "boolean",
        "optional": true,
        "description": "Inline mode",
        "helpText": "Always visible (not popup)",
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
        "helpText": "Disables the color picker",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "appendTo",
        "type": "'self' | HTMLElement | null",
        "optional": true,
        "description": "Append target",
        "helpText": "Element to append overlay to",
        "dataTypes": [
          "'self'",
          "HTMLElement",
          "null"
        ],
        "examples": [
          "'self'",
          "document.body"
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
        "type": "(e: { value: string, target: { value: string } }) => void",
        "description": "Callback when color changes"
      },
      {
        "name": "onShow",
        "type": "() => void",
        "description": "Callback when picker is shown"
      },
      {
        "name": "onHide",
        "type": "() => void",
        "description": "Callback when picker is hidden"
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
      "handleShow - Processes onShow event",
      "handleHide - Processes onHide event"
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
    "basic": "<ColorPickerWrapper value={color} onChange={(e) => setColor(e.value)} />",
    "withStyling": "<ColorPickerWrapper value={bgColor} format=\"hex\" inline className=\"mb-3\" />",
    "withEvents": "<ColorPickerWrapper value={color} onChange={handleChange} onShow={() => console.log('shown')} />",
    "withRedux": "<ColorPickerWrapper value={themeColor} onValueChange={(val) => dispatch(setColor(val))} />",
    "withValidation": "<ColorPickerWrapper value={color} onValidate={(val) => val ? true : 'Required'} onError={(err) => setError(err)} />",
    "withChildren": "N/A"
  }
};

const ColorPickerWrapper = (props) => {
  const {
    value, format, inline, disabled, appendTo, className, style, onChange, onShow, onHide, onValueChange, onValidate, onError, onMount, onUnmount,
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
    format,
    inline,
    disabled,
    appendTo,
    className,
    style,
    onChange: handleChange,
    onShow,
    onHide,
    ref: componentRef,
    ...restProps
  };

  return (
    <ColorPicker {...primeReactProps} />
  );
};

ColorPickerWrapper.displayName = 'ColorPickerWrapper';

export default ColorPickerWrapper;
