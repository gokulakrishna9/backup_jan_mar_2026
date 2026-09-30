/**
 * MessageWrapper - Enhanced wrapper for PrimeReact Message
 * Category: Messages
 * 
 * Inline message component
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Message } from 'primereact/message';

// Component metadata embedded for runtime access
export const MessageMetadata = {
  "name": "Message",
  "import": "Message",
  "category": "Messages",
  "metadata": {
    "description": "Inline message component",
    "usageExamples": [
      "<MessageWrapper severity=\"success\" text=\"Success Message\" />",
      "<MessageWrapper severity=\"error\" text=\"Error occurred\" closable />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "severity",
        "type": "'success' | 'info' | 'warn' | 'error'",
        "optional": true,
        "description": "Message severity",
        "helpText": "Determines color and icon",
        "dataTypes": [
          "'success'",
          "'info'",
          "'warn'",
          "'error'"
        ],
        "examples": [
          "'success'",
          "'error'"
        ]
      },
      {
        "name": "text",
        "type": "string",
        "optional": true,
        "description": "Message text",
        "helpText": "Content of the message",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'Operation successful'",
          "'Error occurred'"
        ]
      },
      {
        "name": "closable",
        "type": "boolean",
        "optional": true,
        "description": "Show close button",
        "helpText": "Displays X button to dismiss message",
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
    "children": {
      "type": "React.ReactNode",
      "description": "Message content",
      "helpText": "Can use children instead of text prop"
    }
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onClose",
        "type": "() => void",
        "description": "Callback when message is closed"
      }
    ],
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
    "internal": [
      "handleClose - Processes onClose event"
    ],
    "patterns": [
      "Check if event handler exists before calling"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [
      "Any React component",
      "Text",
      "HTML elements"
    ],
    "childrenDescription": "Message can accept children as alternative to text prop",
    "hasChildren": true,
    "examples": [
      "<MessageWrapper severity=\"success\"><p>Custom content</p></MessageWrapper>",
      "<MessageWrapper severity=\"error\"><div><strong>Error:</strong> Details</div></MessageWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<MessageWrapper severity=\"success\" text=\"Success Message\" />",
    "withStyling": "<MessageWrapper severity=\"error\" text=\"Error\" className=\"mb-3\" />",
    "withEvents": "<MessageWrapper severity=\"warn\" text=\"Warning\" closable onClose={handleClose} />",
    "withRedux": "<MessageWrapper severity=\"info\" text={errorMessage} closable onClose={() => dispatch(clearError())} />",
    "withValidation": "N/A",
    "withChildren": "<MessageWrapper severity=\"error\" closable><strong>Error:</strong> Operation failed</MessageWrapper>"
  }
};

const MessageWrapper = (props) => {
  const {
    severity, text, closable, className, style, children, onClose, onMount, onUnmount,
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
    severity,
    text,
    closable,
    className,
    style,
    onClose,
    ref: componentRef,
    ...restProps
  };

  return (
    <Message {...primeReactProps}>
      {children}
    </Message>
  );
};

MessageWrapper.displayName = 'MessageWrapper';

export default MessageWrapper;
