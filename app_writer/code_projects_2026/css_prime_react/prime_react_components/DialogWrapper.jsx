/**
 * DialogWrapper - Enhanced wrapper for PrimeReact Dialog
 * Category: Overlay
 * 
 * Modal dialog window
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Dialog } from 'primereact/dialog';

// Component metadata embedded for runtime access
export const DialogMetadata = {
  "name": "Dialog",
  "import": "Dialog",
  "category": "Overlay",
  "metadata": {
    "description": "Modal dialog window",
    "usageExamples": [
      "<DialogWrapper visible={show} onHide={() => setShow(false)} header=\"Confirm\"><p>Are you sure?</p></DialogWrapper>",
      "<DialogWrapper visible={show} onHide={handleClose} footer={<Button label=\"OK\" />}>Content</DialogWrapper>"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "visible",
        "type": "boolean",
        "optional": false,
        "description": "Visibility state",
        "helpText": "Controls dialog visibility (controlled component)",
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
        "name": "header",
        "type": "string | React.ReactNode",
        "optional": true,
        "description": "Dialog header",
        "helpText": "Title or custom header content",
        "dataTypes": [
          "string",
          "React.ReactNode"
        ],
        "examples": [
          "'Confirm Action'",
          "'Edit User'",
          "<CustomHeader />"
        ]
      },
      {
        "name": "footer",
        "type": "React.ReactNode",
        "optional": true,
        "description": "Dialog footer",
        "helpText": "Typically contains action buttons",
        "dataTypes": [
          "React.ReactNode"
        ],
        "examples": [
          "<Button label=\"OK\" />",
          "<><Button label=\"Cancel\" /><Button label=\"Save\" /></>"
        ]
      },
      {
        "name": "modal",
        "type": "boolean",
        "optional": true,
        "description": "Modal mode",
        "helpText": "If true, shows overlay and prevents interaction with page",
        "dataTypes": [
          "boolean (default: true)"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "closable",
        "type": "boolean",
        "optional": true,
        "description": "Show close button",
        "helpText": "Shows X button in header",
        "dataTypes": [
          "boolean (default: true)"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "dismissableMask",
        "type": "boolean",
        "optional": true,
        "description": "Close on mask click",
        "helpText": "Clicking overlay closes dialog",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "draggable",
        "type": "boolean",
        "optional": true,
        "description": "Enable dragging",
        "helpText": "Dialog can be dragged",
        "dataTypes": [
          "boolean (default: true)"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "resizable",
        "type": "boolean",
        "optional": true,
        "description": "Enable resizing",
        "helpText": "Dialog can be resized",
        "dataTypes": [
          "boolean (default: true)"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "position",
        "type": "'center' | 'top' | 'bottom' | 'left' | 'right' | 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right'",
        "optional": true,
        "description": "Dialog position",
        "helpText": "Position on screen",
        "dataTypes": [
          "'center' (default)",
          "'top'",
          "'bottom'",
          "'left'",
          "'right'"
        ],
        "examples": [
          "'center'",
          "'top'"
        ]
      }
    ],
    "styling": [
      {
        "name": "className",
        "type": "string",
        "optional": true,
        "description": "Additional CSS classes",
        "helpText": "Applied to dialog container",
        "examples": [
          "'custom-dialog'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Applied to dialog container",
        "examples": [
          "{ width: '50vw' }"
        ]
      }
    ],
    "children": {
      "type": "React.ReactNode",
      "optional": false,
      "description": "Dialog content",
      "helpText": "Main content of the dialog"
    }
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onHide",
        "type": "() => void",
        "optional": false,
        "description": "Hide callback",
        "helpText": "Called when dialog should close (ESC, close button, mask click)",
        "examples": [
          "() => setVisible(false)",
          "() => dispatch(closeDialog())"
        ]
      },
      {
        "name": "onShow",
        "type": "() => void",
        "optional": true,
        "description": "Show callback",
        "helpText": "Called when dialog is shown",
        "examples": [
          "() => console.log('Dialog shown')"
        ]
      }
    ],
    "simplified": [],
    "validation": [],
    "lifecycle": [
      {
        "name": "onShow",
        "type": "() => void",
        "optional": true,
        "description": "Lifecycle: Dialog shown",
        "helpText": "Called after dialog is displayed",
        "examples": [
          "() => loadData()"
        ]
      },
      {
        "name": "onHide",
        "type": "() => void",
        "optional": false,
        "description": "Lifecycle: Dialog hidden",
        "helpText": "Called when dialog closes",
        "examples": [
          "() => cleanup()"
        ]
      }
    ]
  },
  "eventHandlerMethods": {
    "internal": [
      "handleHide",
      "handleShow"
    ],
    "patterns": [
      "Standard onHide",
      "Redux dispatch",
      "Lifecycle hooks"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [
      "Any React components"
    ],
    "childrenDescription": "Can contain any content - forms, text, images, other components",
    "hasChildren": true,
    "examples": [
      "<DialogWrapper visible={show} onHide={handleClose}><p>Content</p></DialogWrapper>",
      "<DialogWrapper visible={show} onHide={handleClose}><Form /></DialogWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<DialogWrapper visible={show} onHide={() => setShow(false)}><p>Content</p></DialogWrapper>",
    "withStyling": "<DialogWrapper visible={show} onHide={handleClose} style={{ width: '50vw' }}>Content</DialogWrapper>",
    "withEvents": "<DialogWrapper visible={show} onHide={handleClose} onShow={loadData}>Content</DialogWrapper>",
    "withRedux": "<DialogWrapper visible={isOpen} onHide={() => dispatch(closeDialog())}>Content</DialogWrapper>",
    "withValidation": "N/A",
    "withChildren": "<DialogWrapper visible={show} onHide={handleClose} header=\"Edit\" footer={<Button label=\"Save\" />}><Form /></DialogWrapper>"
  }
};

const DialogWrapper = (props) => {
  const {
    visible, header, footer, modal, closable, dismissableMask, draggable, resizable, position, className, style, children, onHide, onShow, onShow, onHide,
    ...restProps
  } = props;

  const componentRef = useRef(null);

  // Build props for underlying PrimeReact component
  const primeReactProps = {
    visible,
    header,
    footer,
    modal,
    closable,
    dismissableMask,
    draggable,
    resizable,
    position,
    className,
    style,
    onHide,
    onShow,
    ref: componentRef,
    ...restProps
  };

  return (
    <Dialog {...primeReactProps}>
      {children}
    </Dialog>
  );
};

DialogWrapper.displayName = 'DialogWrapper';

export default DialogWrapper;
