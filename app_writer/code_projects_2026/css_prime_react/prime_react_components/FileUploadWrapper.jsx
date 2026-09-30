/**
 * FileUploadWrapper - Enhanced wrapper for PrimeReact FileUpload
 * Category: File
 * 
 * File upload with drag and drop
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { FileUpload } from 'primereact/fileupload';

// Component metadata embedded for runtime access
export const FileUploadMetadata = {
  "name": "FileUpload",
  "import": "FileUpload",
  "category": "File",
  "metadata": {
    "description": "File upload with drag and drop",
    "usageExamples": [
      "<FileUploadWrapper name=\"file\" url=\"/api/upload\" onUpload={handleUpload} />",
      "<FileUploadWrapper mode=\"basic\" name=\"file\" accept=\"image/*\" maxFileSize={1000000} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "name",
        "type": "string",
        "optional": false,
        "description": "Form field name",
        "helpText": "Name attribute for file input",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'file'",
          "'upload'",
          "'document'"
        ]
      },
      {
        "name": "url",
        "type": "string",
        "optional": true,
        "description": "Upload URL",
        "helpText": "Server endpoint for upload",
        "dataTypes": [
          "string (URL)"
        ],
        "examples": [
          "'/api/upload'",
          "'https://example.com/upload'"
        ]
      },
      {
        "name": "mode",
        "type": "'advanced' | 'basic'",
        "optional": true,
        "description": "Upload mode",
        "helpText": "advanced=full UI, basic=simple button",
        "dataTypes": [
          "'advanced' (default)",
          "'basic'"
        ],
        "examples": [
          "'advanced'",
          "'basic'"
        ]
      },
      {
        "name": "multiple",
        "type": "boolean",
        "optional": true,
        "description": "Multiple files",
        "helpText": "Allow selecting multiple files",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "accept",
        "type": "string",
        "optional": true,
        "description": "Accepted file types",
        "helpText": "MIME types or extensions",
        "dataTypes": [
          "string (MIME types)"
        ],
        "examples": [
          "'image/*'",
          "'.pdf,.doc'",
          "'application/pdf'"
        ]
      },
      {
        "name": "maxFileSize",
        "type": "number",
        "optional": true,
        "description": "Max file size",
        "helpText": "Maximum size in bytes",
        "dataTypes": [
          "number (bytes)"
        ],
        "examples": [
          "1000000",
          "5000000"
        ]
      },
      {
        "name": "auto",
        "type": "boolean",
        "optional": true,
        "description": "Auto upload",
        "helpText": "Upload immediately after selection",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "customUpload",
        "type": "boolean",
        "optional": true,
        "description": "Custom upload",
        "helpText": "Use custom upload handler",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "disabled",
        "type": "boolean",
        "optional": true,
        "description": "Disabled state",
        "helpText": "Disables the upload",
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
    "children": null
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onUpload",
        "type": "(e: { files: File[] }) => void",
        "description": "Callback when upload completes"
      },
      {
        "name": "onSelect",
        "type": "(e: { files: File[] }) => void",
        "description": "Callback when files are selected"
      },
      {
        "name": "onError",
        "type": "(e: { files: File[] }) => void",
        "description": "Callback when upload fails"
      },
      {
        "name": "onClear",
        "type": "() => void",
        "description": "Callback when files are cleared"
      },
      {
        "name": "onRemove",
        "type": "(e: { file: File }) => void",
        "description": "Callback when file is removed"
      },
      {
        "name": "onBeforeUpload",
        "type": "(e: { xhr: XMLHttpRequest, formData: FormData }) => void",
        "description": "Callback before upload starts"
      },
      {
        "name": "onBeforeSend",
        "type": "(e: { xhr: XMLHttpRequest, formData: FormData }) => void",
        "description": "Callback before request is sent"
      },
      {
        "name": "uploadHandler",
        "type": "(e: { files: File[] }) => void",
        "description": "Custom upload handler (when customUpload=true)"
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
      "handleUpload - Processes onUpload event",
      "handleSelect - Processes onSelect event",
      "handleError - Processes onError event",
      "handleClear - Processes onClear event",
      "handleRemove - Processes onRemove event",
      "handleBeforeUpload - Processes onBeforeUpload event",
      "handleBeforeSend - Processes onBeforeSend event"
    ],
    "patterns": [
      "Check if event handler exists before calling",
      "Extract files from event objects"
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
    "basic": "<FileUploadWrapper name=\"file\" url=\"/api/upload\" onUpload={handleUpload} />",
    "withStyling": "<FileUploadWrapper mode=\"basic\" name=\"file\" accept=\"image/*\" className=\"mb-3\" />",
    "withEvents": "<FileUploadWrapper name=\"file\" onSelect={handleSelect} onError={handleError} />",
    "withRedux": "<FileUploadWrapper name=\"file\" customUpload uploadHandler={(e) => dispatch(uploadFiles(e.files))} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const FileUploadWrapper = (props) => {
  const {
    name, url, mode, multiple, accept, maxFileSize, auto, customUpload, disabled, className, style, onUpload, onSelect, onError, onClear, onRemove, onBeforeUpload, onBeforeSend, uploadHandler, onMount, onUnmount,
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
    name,
    url,
    mode,
    multiple,
    accept,
    maxFileSize,
    auto,
    customUpload,
    disabled,
    className,
    style,
    onUpload,
    onSelect,
    onError,
    onClear,
    onRemove,
    onBeforeUpload,
    onBeforeSend,
    uploadHandler,
    ref: componentRef,
    ...restProps
  };

  return (
    <FileUpload {...primeReactProps} />
  );
};

FileUploadWrapper.displayName = 'FileUploadWrapper';

export default FileUploadWrapper;
