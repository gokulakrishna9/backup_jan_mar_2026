/**
 * EditorWrapper - Enhanced wrapper for PrimeReact Editor
 * Category: Form
 * 
 * Rich text editor (Quill-based)
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Editor } from 'primereact/editor';

// Component metadata embedded for runtime access
export const EditorMetadata = {
  "name": "Editor",
  "import": "Editor",
  "category": "Form",
  "metadata": {
    "description": "Rich text editor (Quill-based)",
    "usageExamples": [
      "<EditorWrapper value={text} onTextChange={(e) => setText(e.htmlValue)} />",
      "<EditorWrapper value={content} style={{ height: '320px' }} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "string",
        "optional": true,
        "description": "HTML content",
        "helpText": "Current HTML content (controlled component)",
        "dataTypes": [
          "string (HTML)"
        ],
        "examples": [
          "'<p>Hello</p>'",
          "htmlContent"
        ]
      },
      {
        "name": "placeholder",
        "type": "string",
        "optional": true,
        "description": "Placeholder text",
        "helpText": "Text shown when empty",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'Enter text...'",
          "'Type here'"
        ]
      },
      {
        "name": "readOnly",
        "type": "boolean",
        "optional": true,
        "description": "Read-only mode",
        "helpText": "Disables editing",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "formats",
        "type": "string[]",
        "optional": true,
        "description": "Enabled formats",
        "helpText": "Array of allowed formatting options",
        "dataTypes": [
          "string[]"
        ],
        "examples": [
          "['bold', 'italic', 'underline']"
        ]
      },
      {
        "name": "headerTemplate",
        "type": "React.ReactNode",
        "optional": true,
        "description": "Custom toolbar",
        "helpText": "Custom toolbar content",
        "dataTypes": [
          "React.ReactNode"
        ],
        "examples": [
          "<span className=\"ql-formats\"><button className=\"ql-bold\" /></span>"
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
          "{ height: '320px' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onTextChange",
        "type": "(e: { htmlValue: string, textValue: string, delta: any, source: string }) => void",
        "description": "Callback when text changes"
      },
      {
        "name": "onSelectionChange",
        "type": "(e: { range: any, oldRange: any, source: string }) => void",
        "description": "Callback when selection changes"
      }
    ],
    "simplified": [
      {
        "name": "onValueChange",
        "type": "(value: string) => void",
        "description": "Simplified callback with just the HTML value"
      }
    ],
    "validation": [
      {
        "name": "onValidate",
        "type": "(value: string) => boolean | string",
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
      "handleTextChange - Processes onTextChange event, calls onTextChange, onValueChange, onValidate",
      "handleSelectionChange - Processes onSelectionChange event"
    ],
    "patterns": [
      "Check if event handler exists before calling",
      "Extract htmlValue from event object",
      "Run validation on text change"
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
    "basic": "<EditorWrapper value={text} onTextChange={(e) => setText(e.htmlValue)} />",
    "withStyling": "<EditorWrapper value={content} style={{ height: '320px' }} className=\"mb-3\" />",
    "withEvents": "<EditorWrapper value={text} onTextChange={handleChange} onSelectionChange={handleSelection} />",
    "withRedux": "<EditorWrapper value={editorContent} onValueChange={(val) => dispatch(setContent(val))} />",
    "withValidation": "<EditorWrapper value={text} onValidate={(val) => val.length > 10 ? true : 'Min 10 chars'} onError={(err) => setError(err)} />",
    "withChildren": "N/A"
  }
};

const EditorWrapper = (props) => {
  const {
    value, placeholder, readOnly, formats, headerTemplate, className, style, onTextChange, onSelectionChange, onValueChange, onValidate, onError, onMount, onUnmount,
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
  const handleSelectionChange = (e) => {
    if (onSelectionChange) {
      onSelectionChange(e);
    }
    if (onValueChange) {
      onValueChange(e.value || e.data || e);
    }
  };

  // Build props for underlying PrimeReact component
  const primeReactProps = {
    value,
    placeholder,
    readOnly,
    formats,
    headerTemplate,
    className,
    style,
    onTextChange,
    onSelectionChange: handleSelectionChange,
    ref: componentRef,
    ...restProps
  };

  return (
    <Editor {...primeReactProps} />
  );
};

EditorWrapper.displayName = 'EditorWrapper';

export default EditorWrapper;
