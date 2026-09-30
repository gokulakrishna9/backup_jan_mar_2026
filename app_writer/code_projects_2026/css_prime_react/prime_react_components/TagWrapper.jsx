/**
 * TagWrapper - Enhanced wrapper for PrimeReact Tag
 * Category: Misc
 * 
 * Label component for categorization
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Tag } from 'primereact/tag';

// Component metadata embedded for runtime access
export const TagMetadata = {
  "name": "Tag",
  "import": "Tag",
  "category": "Misc",
  "metadata": {
    "description": "Label component for categorization",
    "usageExamples": [
      "<TagWrapper value=\"New\" />",
      "<TagWrapper value=\"Primary\" severity=\"success\" icon=\"pi pi-check\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "string | React.ReactNode",
        "optional": true,
        "description": "Tag content",
        "helpText": "Text or custom content",
        "dataTypes": [
          "string",
          "React.ReactNode"
        ],
        "examples": [
          "'New'",
          "'Primary'",
          "<span>Custom</span>"
        ]
      },
      {
        "name": "severity",
        "type": "'success' | 'info' | 'warning' | 'danger'",
        "optional": true,
        "description": "Severity type",
        "helpText": "Predefined color schemes",
        "dataTypes": [
          "'success'",
          "'info'",
          "'warning'",
          "'danger'"
        ],
        "examples": [
          "'success'",
          "'danger'"
        ]
      },
      {
        "name": "icon",
        "type": "string",
        "optional": true,
        "description": "Icon class",
        "helpText": "PrimeIcons class name",
        "dataTypes": [
          "string (PrimeIcons class)"
        ],
        "examples": [
          "'pi pi-check'",
          "'pi pi-times'"
        ]
      },
      {
        "name": "rounded",
        "type": "boolean",
        "optional": true,
        "description": "Rounded style",
        "helpText": "Applies rounded corners",
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
          "'mr-2'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ marginRight: '0.5rem' }"
        ]
      }
    ],
    "children": {
      "type": "React.ReactNode",
      "description": "Tag content",
      "helpText": "Can use children instead of value prop"
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
    "internal": [],
    "patterns": []
  },
  "childComponentInfo": {
    "allowedChildren": [
      "Any React component",
      "Text"
    ],
    "childrenDescription": "Tag can accept children as alternative to value prop",
    "hasChildren": true,
    "examples": [
      "<TagWrapper severity=\"success\">New</TagWrapper>",
      "<TagWrapper><span>Custom</span></TagWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<TagWrapper value=\"New\" />",
    "withStyling": "<TagWrapper value=\"Primary\" severity=\"success\" icon=\"pi pi-check\" className=\"mr-2\" />",
    "withEvents": "N/A",
    "withRedux": "<TagWrapper value={status} severity={getSeverity(status)} />",
    "withValidation": "N/A",
    "withChildren": "<TagWrapper severity=\"info\" rounded><span>Custom Content</span></TagWrapper>"
  }
};

const TagWrapper = (props) => {
  const {
    value, severity, icon, rounded, className, style, children, onMount, onUnmount,
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
    value,
    severity,
    icon,
    rounded,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <Tag {...primeReactProps}>
      {children}
    </Tag>
  );
};

TagWrapper.displayName = 'TagWrapper';

export default TagWrapper;
