/**
 * ConfirmDialogWrapper - Enhanced wrapper for PrimeReact ConfirmDialog
 * Category: Overlay
 * 
 * Confirmation dialog
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { ConfirmDialog } from 'primereact/confirmdialog';

// Component metadata embedded for runtime access
export const ConfirmDialogMetadata = {
  "name": "ConfirmDialog",
  "import": "ConfirmDialog",
  "category": "Overlay",
  "metadata": {
    "description": "Confirmation dialog",
    "usageExamples": [
      "<ConfirmDialogWrapper />",
      "<ConfirmDialogWrapper visible={show} message=\"Are you sure?\" header=\"Confirmation\" onHide={() => setShow(false)} accept={handleAccept} reject={handleReject} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "visible",
        "type": "boolean",
        "optional": true,
        "description": "Visibility state",
        "helpText": "Controls dialog visibility",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "showDialog",
          "isOpen",
          "visible"
        ]
      },
      {
        "name": "message",
        "type": "string | React.ReactNode",
        "optional": true,
        "description": "Confirmation message",
        "helpText": "Message to display",
        "dataTypes": [
          "string",
          "React.ReactNode"
        ],
        "examples": [
          "'Are you sure?'",
          "'Delete this item?'"
        ]
      },
      {
        "name": "header",
        "type": "string",
        "optional": true,
        "description": "Dialog header",
        "helpText": "Title text",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'Confirmation'",
          "'Delete'",
          "'Warning'"
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
          "'pi pi-exclamation-triangle'",
          "'pi pi-question'"
        ]
      },
      {
        "name": "acceptLabel",
        "type": "string",
        "optional": true,
        "description": "Accept button label",
        "helpText": "Text for accept button (default: Yes)",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'Yes'",
          "'Confirm'",
          "'Delete'"
        ]
      },
      {
        "name": "rejectLabel",
        "type": "string",
        "optional": true,
        "description": "Reject button label",
        "helpText": "Text for reject button (default: No)",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'No'",
          "'Cancel'"
        ]
      },
      {
        "name": "acceptClassName",
        "type": "string",
        "optional": true,
        "description": "Accept button class",
        "helpText": "CSS class for accept button",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'p-button-danger'"
        ]
      },
      {
        "name": "rejectClassName",
        "type": "string",
        "optional": true,
        "description": "Reject button class",
        "helpText": "CSS class for reject button",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'p-button-text'"
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
          "'custom-dialog'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ width: '30rem' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onHide",
        "type": "() => void",
        "description": "Callback when dialog is hidden (required)"
      },
      {
        "name": "accept",
        "type": "() => void",
        "description": "Callback when accept button is clicked"
      },
      {
        "name": "reject",
        "type": "() => void",
        "description": "Callback when reject button is clicked"
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
      "handleHide - Processes onHide event",
      "handleAccept - Processes accept event",
      "handleReject - Processes reject event"
    ],
    "patterns": [
      "Check if event handler exists before calling"
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
    "basic": "<ConfirmDialogWrapper visible={show} message=\"Are you sure?\" onHide={() => setShow(false)} accept={handleAccept} />",
    "withStyling": "<ConfirmDialogWrapper visible={show} message=\"Delete?\" header=\"Confirmation\" icon=\"pi pi-exclamation-triangle\" acceptClassName=\"p-button-danger\" onHide={handleClose} accept={handleDelete} />",
    "withEvents": "<ConfirmDialogWrapper visible={show} message=\"Proceed?\" onHide={handleClose} accept={handleAccept} reject={handleReject} />",
    "withRedux": "<ConfirmDialogWrapper visible={showConfirm} message=\"Save changes?\" onHide={() => dispatch(hideConfirm())} accept={() => dispatch(saveChanges())} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const ConfirmDialogWrapper = (props) => {
  const {
    visible, message, header, icon, acceptLabel, rejectLabel, acceptClassName, rejectClassName, className, style, onHide, accept, reject, onMount, onUnmount,
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
    visible,
    message,
    header,
    icon,
    acceptLabel,
    rejectLabel,
    acceptClassName,
    rejectClassName,
    className,
    style,
    onHide,
    accept,
    reject,
    ref: componentRef,
    ...restProps
  };

  return (
    <ConfirmDialog {...primeReactProps} />
  );
};

ConfirmDialogWrapper.displayName = 'ConfirmDialogWrapper';

export default ConfirmDialogWrapper;
