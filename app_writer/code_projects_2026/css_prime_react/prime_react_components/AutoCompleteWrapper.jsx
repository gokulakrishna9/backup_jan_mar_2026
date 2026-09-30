/**
 * AutoCompleteWrapper - Enhanced wrapper for PrimeReact AutoComplete
 * Category: Form
 * 
 * Input with autocomplete suggestions
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { AutoComplete } from 'primereact/autocomplete';

// Component metadata embedded for runtime access
export const AutoCompleteMetadata = {
  "name": "AutoComplete",
  "import": "AutoComplete",
  "category": "Form",
  "metadata": {
    "description": "Input with autocomplete suggestions",
    "usageExamples": [
      "<AutoCompleteWrapper value={selected} suggestions={filtered} completeMethod={search} onChange={(e) => setSelected(e.value)} />",
      "<AutoCompleteWrapper value={country} suggestions={countries} field=\"name\" dropdown />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "any",
        "optional": true,
        "description": "Selected value",
        "helpText": "Current value (controlled component)",
        "dataTypes": [
          "string",
          "object",
          "any"
        ],
        "examples": [
          "'text'",
          "{ name: 'Item' }",
          "selectedItem"
        ]
      },
      {
        "name": "suggestions",
        "type": "any[]",
        "optional": true,
        "description": "Suggestion list",
        "helpText": "Array of suggestions to display",
        "dataTypes": [
          "string[]",
          "object[]"
        ],
        "examples": [
          "['Item 1', 'Item 2']",
          "[{name: 'USA'}]"
        ]
      },
      {
        "name": "completeMethod",
        "type": "(e: { query: string }) => void",
        "optional": false,
        "description": "Callback to fetch suggestions",
        "helpText": "Called when user types - update suggestions state",
        "dataTypes": [
          "function"
        ],
        "examples": [
          "(e) => setFiltered(items.filter(i => i.includes(e.query)))"
        ]
      },
      {
        "name": "field",
        "type": "string",
        "optional": true,
        "description": "Property name for display",
        "helpText": "When suggestions are objects, specifies display property",
        "dataTypes": [
          "string (property name)"
        ],
        "examples": [
          "'name'",
          "'label'",
          "'title'"
        ]
      },
      {
        "name": "dropdown",
        "type": "boolean",
        "optional": true,
        "description": "Show dropdown button",
        "helpText": "Displays button to show all suggestions",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "multiple",
        "type": "boolean",
        "optional": true,
        "description": "Multiple selection",
        "helpText": "Allows selecting multiple items",
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
          "'Search...'",
          "'Type to search'"
        ]
      },
      {
        "name": "disabled",
        "type": "boolean",
        "optional": true,
        "description": "Disabled state",
        "helpText": "Disables the autocomplete",
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
        "type": "(e: { value: any }) => void",
        "description": "Callback when selection changes"
      },
      {
        "name": "onSelect",
        "type": "(e: { value: any }) => void",
        "description": "Callback when item is selected"
      },
      {
        "name": "onUnselect",
        "type": "(e: { value: any }) => void",
        "description": "Callback when item is unselected (multiple mode)"
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
      },
      {
        "name": "onClear",
        "type": "() => void",
        "description": "Callback when input is cleared"
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
      "handleChange - Processes onChange event, calls onChange, onValueChange, onValidate",
      "handleSelect - Processes onSelect event",
      "handleUnselect - Processes onUnselect event",
      "handleFocus - Processes onFocus event",
      "handleBlur - Processes onBlur event, triggers validation",
      "handleClear - Processes onClear event"
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
    "basic": "<AutoCompleteWrapper value={selected} suggestions={filtered} completeMethod={(e) => setFiltered(items.filter(i => i.includes(e.query)))} onChange={(e) => setSelected(e.value)} />",
    "withStyling": "<AutoCompleteWrapper value={country} suggestions={countries} field=\"name\" dropdown className=\"w-full\" />",
    "withEvents": "<AutoCompleteWrapper value={item} suggestions={items} completeMethod={search} onChange={handleChange} onSelect={handleSelect} />",
    "withRedux": "<AutoCompleteWrapper value={selectedItem} suggestions={suggestions} completeMethod={search} onValueChange={(val) => dispatch(setItem(val))} />",
    "withValidation": "<AutoCompleteWrapper value={selection} suggestions={items} completeMethod={search} onValidate={(val) => val ? true : 'Required'} onError={(err) => setError(err)} />",
    "withChildren": "N/A"
  }
};

const AutoCompleteWrapper = (props) => {
  const {
    value, suggestions, completeMethod, field, dropdown, multiple, placeholder, disabled, className, style, onChange, onSelect, onUnselect, onFocus, onBlur, onClear, onValueChange, onValidate, onError, onMount, onUnmount,
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
    suggestions,
    completeMethod,
    field,
    dropdown,
    multiple,
    placeholder,
    disabled,
    className,
    style,
    onChange: handleChange,
    onSelect,
    onUnselect,
    onFocus,
    onBlur,
    onClear,
    ref: componentRef,
    ...restProps
  };

  return (
    <AutoComplete {...primeReactProps} />
  );
};

AutoCompleteWrapper.displayName = 'AutoCompleteWrapper';

export default AutoCompleteWrapper;
