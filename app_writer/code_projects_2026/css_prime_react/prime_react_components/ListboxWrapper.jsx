/**
 * ListboxWrapper - Enhanced wrapper for PrimeReact Listbox
 * Category: Form
 * 
 * List of selectable items
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Listbox } from 'primereact/listbox';

// Component metadata embedded for runtime access
export const ListboxMetadata = {
  "name": "Listbox",
  "import": "Listbox",
  "category": "Form",
  "metadata": {
    "description": "List of selectable items",
    "usageExamples": [
      "<ListboxWrapper value={selected} options={cities} onChange={(e) => setSelected(e.value)} />",
      "<ListboxWrapper value={items} options={allItems} multiple filter />"
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
          "'item1'",
          "['item1', 'item2']"
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
          "object[]"
        ],
        "examples": [
          "['Option 1', 'Option 2']",
          "[{label: 'USA', value: 'us'}]"
        ]
      },
      {
        "name": "optionLabel",
        "type": "string",
        "optional": true,
        "description": "Property name for option label",
        "helpText": "When options are objects",
        "dataTypes": [
          "string"
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
        "helpText": "When options are objects",
        "dataTypes": [
          "string"
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
        "name": "filter",
        "type": "boolean",
        "optional": true,
        "description": "Enable filtering",
        "helpText": "Shows search input",
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
        "helpText": "Disables the listbox",
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
          "{ width: '15rem' }"
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
    "basic": "<ListboxWrapper value={selected} options={['Option 1', 'Option 2']} onChange={(e) => setSelected(e.value)} />",
    "withStyling": "<ListboxWrapper value={city} options={cities} filter className=\"w-full\" />",
    "withEvents": "<ListboxWrapper value={item} options={items} onChange={handleChange} />",
    "withRedux": "<ListboxWrapper value={selectedItem} options={items} onValueChange={(val) => dispatch(setItem(val))} />",
    "withValidation": "<ListboxWrapper value={selection} options={options} onValidate={(val) => val ? true : 'Required'} onError={(err) => setError(err)} />",
    "withChildren": "N/A"
  }
};

const ListboxWrapper = (props) => {
  const {
    value, options, optionLabel, optionValue, multiple, filter, disabled, className, style, onChange, onValueChange, onValidate, onError, onMount, onUnmount,
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
    filter,
    disabled,
    className,
    style,
    onChange: handleChange,
    ref: componentRef,
    ...restProps
  };

  return (
    <Listbox {...primeReactProps} />
  );
};

ListboxWrapper.displayName = 'ListboxWrapper';

export default ListboxWrapper;
