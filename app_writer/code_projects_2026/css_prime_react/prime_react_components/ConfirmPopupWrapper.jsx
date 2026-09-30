/**
 * ConfirmPopupWrapper - Enhanced wrapper for PrimeReact ConfirmPopup
 * Category: Overlay
 * 
 * Inline confirmation popup for quick user confirmations
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { ConfirmPopup } from 'primereact/confirmpopup';

// Component metadata embedded for runtime access
export const ConfirmPopupMetadata = {
  "name": "ConfirmPopup",
  "import": "ConfirmPopup",
  "category": "Overlay",
  "metadata": {
    "description": "Inline confirmation popup for quick user confirmations",
    "usageExamples": [
      "<ConfirmPopupWrapper />",
      "<ConfirmPopupWrapper target={buttonRef.current} visible={visible} onHide={() => setVisible(false)} message=\"Are you sure?\" accept={handleAccept} reject={handleReject} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "target",
        "type": "HTMLElement",
        "optional": true,
        "description": "Target element to attach popup",
        "helpText": "DOM element reference where popup should appear",
        "dataTypes": [
          "HTMLElement (ref.current)"
        ],
        "examples": [
          "buttonRef.current",
          "document.getElementById('btn')"
        ]
      },
      {
        "name": "visible",
        "type": "boolean",
        "optional": true,
        "description": "Whether popup is visible",
        "helpText": "Controls popup visibility",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "message",
        "type": "string | React.ReactNode",
        "optional": true,
        "description": "Confirmation message",
        "helpText": "Message to display in popup",
        "dataTypes": [
          "string",
          "React.ReactNode"
        ],
        "examples": [
          "'Are you sure you want to delete?'",
          "'Confirm action?'"
        ]
      },
      {
        "name": "icon",
        "type": "string",
        "optional": true,
        "description": "Icon to display",
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
        "description": "Label for accept button",
        "helpText": "Text for confirmation button (default: 'Yes')",
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
        "description": "Label for reject button",
        "helpText": "Text for cancel button (default: 'No')",
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
        "description": "CSS class for accept button",
        "helpText": "Custom styling for accept button",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'p-button-danger'",
          "'p-button-success'"
        ]
      },
      {
        "name": "rejectClassName",
        "type": "string",
        "optional": true,
        "description": "CSS class for reject button",
        "helpText": "Custom styling for reject button",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'p-button-text'",
          "'p-button-outlined'"
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
          "'custom-popup'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles object",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ width: '300px' }"
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
        "optional": true,
        "description": "Callback when popup is hidden"
      },
      {
        "name": "accept",
        "type": "() => void",
        "optional": true,
        "description": "Callback when user confirms"
      },
      {
        "name": "reject",
        "type": "() => void",
        "optional": true,
        "description": "Callback when user cancels"
      }
    ],
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
    "patterns": [
      "For delete actions: Use accept callback to perform deletion",
      "For Redux: Dispatch actions in accept/reject callbacks"
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
    "basic": "<ConfirmPopupWrapper />",
    "withStyling": "<ConfirmPopupWrapper className=\"custom-confirm\" style={{ width: '350px' }} />",
    "withEvents": "<ConfirmPopupWrapper target={buttonRef.current} visible={visible} onHide={() => setVisible(false)} message=\"Delete this item?\" accept={handleDelete} reject={() => setVisible(false)} />",
    "withRedux": "<ConfirmPopupWrapper target={target} visible={showConfirm} onHide={() => dispatch(hideConfirm())} message=\"Confirm action?\" accept={() => dispatch(confirmAction())} reject={() => dispatch(cancelAction())} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const ConfirmPopupWrapper = (props) => {
  const {
    target, visible, message, icon, acceptLabel, rejectLabel, acceptClassName, rejectClassName, className, style, onHide, accept, reject, onMount,
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
    target,
    visible,
    message,
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
    <ConfirmPopup {...primeReactProps} />
  );
};

ConfirmPopupWrapper.displayName = 'ConfirmPopupWrapper';

export default ConfirmPopupWrapper;
