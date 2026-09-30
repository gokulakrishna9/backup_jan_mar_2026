/**
 * CascadeSelectWrapper - Enhanced wrapper for PrimeReact CascadeSelect
 * Category: Form
 * 
 * Nested dropdown selection
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { CascadeSelect } from 'primereact/cascadeselect';

// Component metadata embedded for runtime access
export const CascadeSelectMetadata = {
  "name": "CascadeSelect",
  "import": "CascadeSelect",
  "category": "Form",
  "metadata": {
    "description": "Nested dropdown selection",
    "usageExamples": [
      "<CascadeSelectWrapper value={selected} options={countries} optionLabel=\"cname\" optionGroupLabel=\"name\" optionGroupChildren=\"states\" onChange={(e) => setSelected(e.value)} />",
      "<CascadeSelectWrapper value={location} options={locations} placeholder=\"Select location\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "any",
        "optional": true,
        "description": "Selected value",
        "helpText": "Currently selected option",
        "dataTypes": [
          "object",
          "any"
        ],
        "examples": [
          "selectedItem",
          "{ name: 'Item' }"
        ]
      },
      {
        "name": "options",
        "type": "any[]",
        "optional": false,
        "description": "Options array",
        "helpText": "Hierarchical options with nested children",
        "dataTypes": [
          "object[] with nested children"
        ],
        "examples": [
          "[{name: 'USA', states: [{name: 'NY'}]}]"
        ]
      },
      {
        "name": "optionLabel",
        "type": "string",
        "optional": true,
        "description": "Option label property",
        "helpText": "Property name for option display",
        "dataTypes": [
          "string (property name)"
        ],
        "examples": [
          "'name'",
          "'label'",
          "'cname'"
        ]
      },
      {
        "name": "optionValue",
        "type": "string",
        "optional": true,
        "description": "Option value property",
        "helpText": "Property name for option value",
        "dataTypes": [
          "string (property name)"
        ],
        "examples": [
          "'code'",
          "'id'",
          "'value'"
        ]
      },
      {
        "name": "optionGroupLabel",
        "type": "string",
        "optional": true,
        "description": "Group label property",
        "helpText": "Property name for group display",
        "dataTypes": [
          "string (property name)"
        ],
        "examples": [
          "'name'",
          "'label'"
        ]
      },
      {
        "name": "optionGroupChildren",
        "type": "string",
        "optional": true,
        "description": "Group children property",
        "helpText": "Property name for nested children array",
        "dataTypes": [
          "string (property name)"
        ],
        "examples": [
          "'states'",
          "'cities'",
          "'children'"
        ]
      },
      {
        "name": "placeholder",
        "type": "string",
        "optional": true,
        "description": "Placeholder text",
        "helpText": "Text shown when no selection",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'Select location'",
          "'Choose...'"
        ]
      },
      {
        "name": "disabled",
        "type": "boolean",
        "optional": true,
        "description": "Disabled state",
        "helpText": "Disables the cascade select",
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
        "name": "onGroupChange",
        "type": "(e: { value: any }) => void",
        "description": "Callback when group changes"
      },
      {
        "name": "onBeforeShow",
        "type": "() => void",
        "description": "Callback before panel shows"
      },
      {
        "name": "onBeforeHide",
        "type": "() => void",
        "description": "Callback before panel hides"
      },
      {
        "name": "onShow",
        "type": "() => void",
        "description": "Callback when panel shows"
      },
      {
        "name": "onHide",
        "type": "() => void",
        "description": "Callback when panel hides"
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
      "handleGroupChange - Processes onGroupChange event",
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
    "basic": "<CascadeSelectWrapper value={selected} options={countries} optionLabel=\"cname\" optionGroupLabel=\"name\" optionGroupChildren=\"states\" onChange={(e) => setSelected(e.value)} />",
    "withStyling": "<CascadeSelectWrapper value={location} options={locations} placeholder=\"Select location\" className=\"w-full\" />",
    "withEvents": "<CascadeSelectWrapper value={item} options={items} onChange={handleChange} onGroupChange={handleGroupChange} />",
    "withRedux": "<CascadeSelectWrapper value={selectedLocation} options={locations} onValueChange={(val) => dispatch(setLocation(val))} />",
    "withValidation": "<CascadeSelectWrapper value={selection} options={options} onValidate={(val) => val ? true : 'Required'} onError={(err) => setError(err)} />",
    "withChildren": "N/A"
  }
};

const CascadeSelectWrapper = (props) => {
  const {
    value, options, optionLabel, optionValue, optionGroupLabel, optionGroupChildren, placeholder, disabled, className, style, onChange, onGroupChange, onBeforeShow, onBeforeHide, onShow, onHide, onValueChange, onValidate, onError, onMount, onUnmount,
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
    optionGroupLabel,
    optionGroupChildren,
    placeholder,
    disabled,
    className,
    style,
    onChange: handleChange,
    onGroupChange,
    onBeforeShow,
    onBeforeHide,
    onShow,
    onHide,
    ref: componentRef,
    ...restProps
  };

  return (
    <CascadeSelect {...primeReactProps} />
  );
};

CascadeSelectWrapper.displayName = 'CascadeSelectWrapper';

export default CascadeSelectWrapper;
