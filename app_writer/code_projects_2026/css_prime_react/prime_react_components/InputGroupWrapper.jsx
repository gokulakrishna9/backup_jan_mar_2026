/**
 * InputGroupWrapper - Enhanced wrapper for PrimeReact InputGroup
 * Category: Form
 * 
 * Groups multiple inputs together with addons and buttons
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { InputGroup } from 'primereact/inputgroup';

// Component metadata embedded for runtime access
export const InputGroupMetadata = {
  "name": "InputGroup",
  "import": "InputGroup",
  "category": "Form",
  "metadata": {
    "description": "Groups multiple inputs together with addons and buttons",
    "usageExamples": [
      "<InputGroupWrapper><InputGroupAddon>@</InputGroupAddon><InputText placeholder=\"Username\" /></InputGroupWrapper>",
      "<InputGroupWrapper><InputText placeholder=\"Search\" /><Button icon=\"pi pi-search\" /></InputGroupWrapper>"
    ]
  },
  "propsInterface": {
    "componentSpecific": [],
    "styling": [
      {
        "name": "className",
        "type": "string",
        "optional": true,
        "description": "Additional CSS classes for custom styling",
        "helpText": "Supports PrimeFlex utility classes and custom CSS",
        "examples": [
          "'w-full'",
          "'mb-3'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles object",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ width: '100%' }"
        ]
      }
    ],
    "children": {
      "type": "React.ReactNode",
      "required": true,
      "description": "Input components, InputGroupAddon, and Button components"
    }
  },
  "eventHandlers": {
    "standard": [],
    "simplified": [],
    "validation": [],
    "lifecycle": [
      {
        "name": "onMount",
        "type": "() => void",
        "optional": true,
        "description": "Callback when component mounts"
      }
    ]
  },
  "eventHandlerMethods": {
    "internal": [],
    "patterns": []
  },
  "childComponentInfo": {
    "allowedChildren": [
      "InputText",
      "InputNumber",
      "Dropdown",
      "Button",
      "InputGroupAddon"
    ],
    "childrenDescription": "Can contain input components, InputGroupAddon for text/icons, and Button components. Children are rendered in sequence.",
    "hasChildren": true,
    "examples": [
      "<InputGroupWrapper><InputGroupAddon>$</InputGroupAddon><InputNumber placeholder=\"Price\" /></InputGroupWrapper>",
      "<InputGroupWrapper><InputText placeholder=\"Email\" /><InputGroupAddon>@example.com</InputGroupAddon></InputGroupWrapper>",
      "<InputGroupWrapper><Button icon=\"pi pi-search\" /><InputText placeholder=\"Search\" /><Button icon=\"pi pi-times\" /></InputGroupWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<InputGroupWrapper><InputGroupAddon>@</InputGroupAddon><InputText placeholder=\"Username\" /></InputGroupWrapper>",
    "withStyling": "<InputGroupWrapper className=\"w-full mb-3\"><InputGroupAddon><i className=\"pi pi-user\" /></InputGroupAddon><InputText placeholder=\"Username\" className=\"w-full\" /></InputGroupWrapper>",
    "withEvents": "N/A",
    "withRedux": "<InputGroupWrapper><InputGroupAddon>$</InputGroupAddon><InputNumber value={price} onValueChange={(e) => dispatch(setPrice(e.value))} /></InputGroupWrapper>",
    "withValidation": "N/A",
    "withChildren": "<InputGroupWrapper><Button icon=\"pi pi-plus\" onClick={handleAdd} /><InputText value={item} onChange={(e) => setItem(e.target.value)} /><Button icon=\"pi pi-check\" onClick={handleSave} /></InputGroupWrapper>"
  }
};

const InputGroupWrapper = (props) => {
  const {
    className, style, children, onMount,
    ...restProps
  } = props;

  const componentRef = useRef(null);

  // Lifecycle: onMount
  useEffect(() => {
    if (onMount) {
      onMount();
    }
  }, []);

  // Build props for underlying PrimeReact component
  const primeReactProps = {
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <InputGroup {...primeReactProps}>
      {children}
    </InputGroup>
  );
};

InputGroupWrapper.displayName = 'InputGroupWrapper';

export default InputGroupWrapper;
