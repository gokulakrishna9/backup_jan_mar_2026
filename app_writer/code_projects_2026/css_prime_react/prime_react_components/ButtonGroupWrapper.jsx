/**
 * ButtonGroupWrapper - Enhanced wrapper for PrimeReact ButtonGroup
 * Category: Button
 * 
 * Groups multiple buttons together for related actions
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { ButtonGroup } from 'primereact/buttongroup';

// Component metadata embedded for runtime access
export const ButtonGroupMetadata = {
  "name": "ButtonGroup",
  "import": "ButtonGroup",
  "category": "Button",
  "metadata": {
    "description": "Groups multiple buttons together for related actions",
    "usageExamples": [
      "<ButtonGroupWrapper><Button label=\"Left\" /><Button label=\"Center\" /><Button label=\"Right\" /></ButtonGroupWrapper>",
      "<ButtonGroupWrapper><Button icon=\"pi pi-align-left\" /><Button icon=\"pi pi-align-center\" /><Button icon=\"pi pi-align-right\" /></ButtonGroupWrapper>"
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
          "'flex-wrap'"
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
      "description": "Button components to be grouped"
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
      "Button"
    ],
    "childrenDescription": "Contains multiple Button components that are visually grouped together. Buttons share borders and are rendered as a single unit.",
    "hasChildren": true,
    "examples": [
      "<ButtonGroupWrapper><Button label=\"Save\" icon=\"pi pi-check\" /><Button label=\"Cancel\" icon=\"pi pi-times\" /></ButtonGroupWrapper>",
      "<ButtonGroupWrapper><Button icon=\"pi pi-bold\" /><Button icon=\"pi pi-italic\" /><Button icon=\"pi pi-underline\" /></ButtonGroupWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<ButtonGroupWrapper><Button label=\"Yes\" /><Button label=\"No\" /><Button label=\"Maybe\" /></ButtonGroupWrapper>",
    "withStyling": "<ButtonGroupWrapper className=\"mb-3\"><Button label=\"Left\" className=\"p-button-outlined\" /><Button label=\"Center\" className=\"p-button-outlined\" /><Button label=\"Right\" className=\"p-button-outlined\" /></ButtonGroupWrapper>",
    "withEvents": "<ButtonGroupWrapper><Button label=\"Save\" onClick={handleSave} /><Button label=\"Cancel\" onClick={handleCancel} /></ButtonGroupWrapper>",
    "withRedux": "<ButtonGroupWrapper><Button label=\"Increment\" onClick={() => dispatch(increment())} /><Button label=\"Decrement\" onClick={() => dispatch(decrement())} /></ButtonGroupWrapper>",
    "withValidation": "N/A",
    "withChildren": "<ButtonGroupWrapper><Button icon=\"pi pi-align-left\" onClick={() => setAlign('left')} /><Button icon=\"pi pi-align-center\" onClick={() => setAlign('center')} /><Button icon=\"pi pi-align-right\" onClick={() => setAlign('right')} /></ButtonGroupWrapper>"
  }
};

const ButtonGroupWrapper = (props) => {
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
    <ButtonGroup {...primeReactProps}>
      {children}
    </ButtonGroup>
  );
};

ButtonGroupWrapper.displayName = 'ButtonGroupWrapper';

export default ButtonGroupWrapper;
