/**
 * ButtonWrapper - Enhanced wrapper for PrimeReact Button
 * Category: Button
 * 
 * Button with various styles and states
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Button } from 'primereact/button';

// Component metadata embedded for runtime access
export const ButtonMetadata = {
  "name": "Button",
  "import": "Button",
  "category": "Button",
  "metadata": {
    "description": "Button with various styles and states",
    "usageExamples": [
      "<ButtonWrapper label=\"Submit\" icon=\"pi pi-check\" severity=\"success\" onClick={handleSubmit} />",
      "<ButtonWrapper loading={isLoading}>Save</ButtonWrapper>"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "label",
        "type": "string",
        "optional": true,
        "description": "Button text",
        "helpText": "Text displayed on the button",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'Submit'",
          "'Cancel'",
          "'Save'"
        ]
      },
      {
        "name": "icon",
        "type": "string",
        "optional": true,
        "description": "PrimeIcon class name",
        "helpText": "Icon to display on button",
        "dataTypes": [
          "string (PrimeIcon class)"
        ],
        "examples": [
          "'pi pi-check'",
          "'pi pi-times'"
        ]
      },
      {
        "name": "severity",
        "type": "'success' | 'info' | 'warning' | 'danger' | 'help' | 'secondary' | null",
        "optional": true,
        "description": "Button severity/color scheme",
        "helpText": "Predefined color schemes",
        "dataTypes": [
          "'success'",
          "'danger'",
          "'secondary'"
        ],
        "examples": [
          "'success'",
          "'danger'"
        ]
      },
      {
        "name": "loading",
        "type": "boolean",
        "optional": true,
        "description": "Show loading spinner",
        "helpText": "Displays spinner and disables button",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "isLoading"
        ]
      },
      {
        "name": "disabled",
        "type": "boolean",
        "optional": true,
        "description": "Disabled state",
        "helpText": "Disables button interaction",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "!isValid"
        ]
      }
    ],
    "styling": [
      {
        "name": "className",
        "type": "string",
        "optional": true,
        "description": "Additional CSS classes",
        "helpText": "Supports PrimeFlex",
        "examples": [
          "'w-full'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "React inline styles",
        "examples": [
          "{ width: '100%' }"
        ]
      }
    ],
    "children": {
      "type": "React.ReactNode",
      "optional": true,
      "description": "Button content",
      "helpText": "Can contain text, icons, or custom elements"
    }
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onClick",
        "type": "(e: React.MouseEvent) => void",
        "optional": true,
        "description": "Click handler",
        "helpText": "Called when button is clicked",
        "examples": [
          "(e) => handleClick()",
          "(e) => dispatch(action())"
        ]
      }
    ],
    "simplified": [],
    "validation": [],
    "lifecycle": []
  },
  "eventHandlerMethods": {
    "internal": [
      "handleClick"
    ],
    "patterns": [
      "Standard onClick",
      "Redux dispatch"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [
      "Text",
      "Icons",
      "React.ReactNode"
    ],
    "childrenDescription": "Can contain text, icons, or any React elements",
    "hasChildren": true,
    "examples": [
      "<ButtonWrapper>Custom Content</ButtonWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<ButtonWrapper label=\"Submit\" />",
    "withStyling": "<ButtonWrapper label=\"Submit\" className=\"w-full\" severity=\"success\" />",
    "withEvents": "<ButtonWrapper label=\"Save\" onClick={handleSave} loading={isSaving} />",
    "withRedux": "<ButtonWrapper label=\"Submit\" onClick={() => dispatch(submitForm())} />",
    "withValidation": "<ButtonWrapper label=\"Submit\" disabled={!isValid} />",
    "withChildren": "<ButtonWrapper severity=\"success\">Confirm</ButtonWrapper>"
  }
};

const ButtonWrapper = (props) => {
  const {
    label, icon, severity, loading, disabled, className, style, children, onClick,
    ...restProps
  } = props;

  const componentRef = useRef(null);

  // Build props for underlying PrimeReact component
  const primeReactProps = {
    label,
    icon,
    severity,
    loading,
    disabled,
    className,
    style,
    onClick,
    ref: componentRef,
    ...restProps
  };

  return (
    <Button {...primeReactProps}>
      {children}
    </Button>
  );
};

ButtonWrapper.displayName = 'ButtonWrapper';

export default ButtonWrapper;
