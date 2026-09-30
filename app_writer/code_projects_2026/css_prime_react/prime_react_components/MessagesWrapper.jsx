/**
 * MessagesWrapper - Enhanced wrapper for PrimeReact Messages
 * Category: Messages
 * 
 * Multiple inline messages
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Messages } from 'primereact/messages';

// Component metadata embedded for runtime access
export const MessagesMetadata = {
  "name": "Messages",
  "import": "Messages",
  "category": "Messages",
  "metadata": {
    "description": "Multiple inline messages",
    "usageExamples": [
      "const msgs = useRef(null); <MessagesWrapper ref={msgs} />; msgs.current.show([{severity: 'success', summary: 'Success', detail: 'Message'}]);",
      "<MessagesWrapper ref={messagesRef} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [],
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
    "children": null
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onRemove",
        "type": "(message: any) => void",
        "description": "Callback when message is removed"
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
      "show - Method to display messages array",
      "clear - Method to clear all messages",
      "replace - Method to replace messages"
    ],
    "patterns": [
      "Use ref to access messages methods",
      "Call show() with array of message objects { severity, summary, detail, sticky, closable }"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children - messages are shown via ref methods",
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
    "basic": "const msgs = useRef(null); <MessagesWrapper ref={msgs} />; msgs.current.show([{severity: 'success', summary: 'Success', detail: 'Message'}]);",
    "withStyling": "<MessagesWrapper ref={msgs} className=\"mb-3\" />",
    "withEvents": "<MessagesWrapper ref={msgs} onRemove={(msg) => console.log('removed', msg)} />",
    "withRedux": "msgs.current.show([{severity: 'info', summary: 'Info', detail: 'Data loaded from Redux'}]);",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const MessagesWrapper = (props) => {
  const {
    className, style, onRemove, onMount, onUnmount,
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
    onRemove,
    ref: componentRef,
    ...restProps
  };

  return (
    <Messages {...primeReactProps} />
  );
};

MessagesWrapper.displayName = 'MessagesWrapper';

export default MessagesWrapper;
