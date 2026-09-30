/**
 * TerminalWrapper - Enhanced wrapper for PrimeReact Terminal
 * Category: Misc
 * 
 * Command line interface simulation for terminal-like interactions
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Terminal } from 'primereact/terminal';

// Component metadata embedded for runtime access
export const TerminalMetadata = {
  "name": "Terminal",
  "import": "Terminal",
  "category": "Misc",
  "metadata": {
    "description": "Command line interface simulation for terminal-like interactions",
    "usageExamples": [
      "<TerminalWrapper welcomeMessage=\"Welcome to Terminal\" prompt=\"$\" />",
      "<TerminalWrapper welcomeMessage=\"CLI v1.0\" prompt=\">\" commandHandler={handleCommand} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "welcomeMessage",
        "type": "string",
        "optional": true,
        "description": "Welcome message displayed on load",
        "helpText": "Initial message shown in terminal",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'Welcome to Terminal'",
          "'CLI v1.0.0'"
        ]
      },
      {
        "name": "prompt",
        "type": "string",
        "optional": true,
        "description": "Command prompt symbol",
        "helpText": "Symbol displayed before user input (default: '$')",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'$'",
          "'>'",
          "'#'",
          "'>>>'"
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
          "'h-full'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles object",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ height: '400px' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "commandHandler",
        "type": "(text: string) => string",
        "optional": true,
        "description": "Handler for processing commands"
      }
    ],
    "simplified": [
      {
        "name": "onCommand",
        "type": "(command: string) => string | Promise<string>",
        "optional": true,
        "description": "Simplified command handler"
      }
    ],
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
    "internal": [
      "handleCommand(text): Processes command and returns response"
    ],
    "patterns": [
      "For command processing: Implement commandHandler to parse and execute commands",
      "For async operations: Return promises from command handler"
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
    "basic": "<TerminalWrapper welcomeMessage=\"Welcome\" prompt=\"$\" />",
    "withStyling": "<TerminalWrapper welcomeMessage=\"CLI v1.0\" prompt=\">\" className=\"w-full\" style={{ height: '400px' }} />",
    "withEvents": "<TerminalWrapper welcomeMessage=\"Terminal\" prompt=\"$\" commandHandler={(text) => `Executed: ${text}`} />",
    "withRedux": "<TerminalWrapper welcomeMessage=\"CLI\" onCommand={(cmd) => dispatch(executeCommand(cmd))} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const TerminalWrapper = (props) => {
  const {
    welcomeMessage, prompt, className, style, commandHandler, onCommand, onMount,
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
    welcomeMessage,
    prompt,
    className,
    style,
    commandHandler,
    ref: componentRef,
    ...restProps
  };

  return (
    <Terminal {...primeReactProps} />
  );
};

TerminalWrapper.displayName = 'TerminalWrapper';

export default TerminalWrapper;
