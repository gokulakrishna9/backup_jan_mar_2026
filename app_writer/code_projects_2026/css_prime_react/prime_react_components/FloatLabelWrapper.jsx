/**
 * FloatLabelWrapper - Enhanced wrapper for PrimeReact FloatLabel
 * Category: Form
 * 
 * Floating label wrapper for input fields with animated label behavior
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { FloatLabel } from 'primereact/floatlabel';

// Component metadata embedded for runtime access
export const FloatLabelMetadata = {
  "name": "FloatLabel",
  "import": "FloatLabel",
  "category": "Form",
  "metadata": {
    "description": "Floating label wrapper for input fields with animated label behavior",
    "usageExamples": [
      "<FloatLabelWrapper><InputText id=\"username\" /><label htmlFor=\"username\">Username</label></FloatLabelWrapper>",
      "<FloatLabelWrapper><Dropdown id=\"country\" options={countries} /><label htmlFor=\"country\">Country</label></FloatLabelWrapper>"
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
          "'mb-3'",
          "'field'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles object",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ marginBottom: '1rem' }"
        ]
      }
    ],
    "children": {
      "type": "React.ReactNode",
      "required": true,
      "description": "Input component and label element"
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
      },
      {
        "name": "onUnmount",
        "type": "() => void",
        "optional": true,
        "description": "Callback when component unmounts"
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
      "Dropdown",
      "Calendar",
      "InputNumber",
      "InputMask",
      "Password",
      "Textarea",
      "AutoComplete",
      "MultiSelect",
      "label"
    ],
    "childrenDescription": "Requires an input component and a label element as children. The label should have htmlFor attribute matching the input's id.",
    "hasChildren": true,
    "examples": [
      "<FloatLabelWrapper><InputText id=\"email\" /><label htmlFor=\"email\">Email</label></FloatLabelWrapper>",
      "<FloatLabelWrapper><Calendar id=\"date\" /><label htmlFor=\"date\">Date</label></FloatLabelWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<FloatLabelWrapper><InputText id=\"username\" /><label htmlFor=\"username\">Username</label></FloatLabelWrapper>",
    "withStyling": "<FloatLabelWrapper className=\"mb-3\"><InputText id=\"email\" className=\"w-full\" /><label htmlFor=\"email\">Email</label></FloatLabelWrapper>",
    "withEvents": "<FloatLabelWrapper onMount={() => console.log('Mounted')}><InputText id=\"name\" /><label htmlFor=\"name\">Name</label></FloatLabelWrapper>",
    "withRedux": "<FloatLabelWrapper><InputText id=\"username\" value={username} onChange={(e) => dispatch(setUsername(e.target.value))} /><label htmlFor=\"username\">Username</label></FloatLabelWrapper>",
    "withValidation": "N/A",
    "withChildren": "<FloatLabelWrapper><Dropdown id=\"country\" options={countries} value={selectedCountry} onChange={(e) => setSelectedCountry(e.value)} /><label htmlFor=\"country\">Select Country</label></FloatLabelWrapper>"
  }
};

const FloatLabelWrapper = (props) => {
  const {
    className, style, children, onMount, onUnmount,
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
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <FloatLabel {...primeReactProps}>
      {children}
    </FloatLabel>
  );
};

FloatLabelWrapper.displayName = 'FloatLabelWrapper';

export default FloatLabelWrapper;
