/**
 * IconFieldWrapper - Enhanced wrapper for PrimeReact IconField
 * Category: Form
 * 
 * Input field wrapper with icon support for visual indicators
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { IconField } from 'primereact/iconfield';

// Component metadata embedded for runtime access
export const IconFieldMetadata = {
  "name": "IconField",
  "import": "IconField",
  "category": "Form",
  "metadata": {
    "description": "Input field wrapper with icon support for visual indicators",
    "usageExamples": [
      "<IconFieldWrapper iconPosition=\"left\"><InputIcon className=\"pi pi-search\" /><InputText placeholder=\"Search\" /></IconFieldWrapper>",
      "<IconFieldWrapper iconPosition=\"right\"><InputText placeholder=\"Email\" /><InputIcon className=\"pi pi-envelope\" /></IconFieldWrapper>"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "iconPosition",
        "type": "'left' | 'right'",
        "optional": true,
        "description": "Position of the icon relative to input",
        "helpText": "Determines whether icon appears on left or right side of input",
        "dataTypes": [
          "'left' (default)",
          "'right'"
        ],
        "examples": [
          "'left'",
          "'right'"
        ]
      }
    ],
    "styling": [
      {
        "name": "className",
        "type": "string",
        "optional": true,
        "description": "Additional CSS classes for custom styling",
        "helpText": "Supports PrimeFlex utility classes and custom CSS",
        "examples": [
          "'w-full'",
          "'mb-2'"
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
      "description": "InputIcon and input component"
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
      "InputIcon",
      "InputText",
      "Dropdown",
      "AutoComplete",
      "Calendar"
    ],
    "childrenDescription": "Requires InputIcon component and an input component as children. Icon position is controlled by iconPosition prop.",
    "hasChildren": true,
    "examples": [
      "<IconFieldWrapper iconPosition=\"left\"><InputIcon className=\"pi pi-search\" /><InputText /></IconFieldWrapper>",
      "<IconFieldWrapper iconPosition=\"right\"><InputText /><InputIcon className=\"pi pi-calendar\" /></IconFieldWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<IconFieldWrapper iconPosition=\"left\"><InputIcon className=\"pi pi-search\" /><InputText placeholder=\"Search\" /></IconFieldWrapper>",
    "withStyling": "<IconFieldWrapper iconPosition=\"left\" className=\"w-full mb-3\"><InputIcon className=\"pi pi-user\" /><InputText placeholder=\"Username\" className=\"w-full\" /></IconFieldWrapper>",
    "withEvents": "N/A",
    "withRedux": "<IconFieldWrapper iconPosition=\"left\"><InputIcon className=\"pi pi-search\" /><InputText value={searchTerm} onChange={(e) => dispatch(setSearchTerm(e.target.value))} /></IconFieldWrapper>",
    "withValidation": "N/A",
    "withChildren": "<IconFieldWrapper iconPosition=\"right\"><Calendar /><InputIcon className=\"pi pi-calendar\" /></IconFieldWrapper>"
  }
};

const IconFieldWrapper = (props) => {
  const {
    iconPosition, className, style, children, onMount,
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
    iconPosition,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <IconField {...primeReactProps}>
      {children}
    </IconField>
  );
};

IconFieldWrapper.displayName = 'IconFieldWrapper';

export default IconFieldWrapper;
