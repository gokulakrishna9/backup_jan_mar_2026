/**
 * InplaceWrapper - Enhanced wrapper for PrimeReact Inplace
 * Category: Misc
 * 
 * Inline editing with display/edit modes
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Inplace } from 'primereact/inplace';

// Component metadata embedded for runtime access
export const InplaceMetadata = {
  "name": "Inplace",
  "import": "Inplace",
  "category": "Misc",
  "metadata": {
    "description": "Inline editing with display/edit modes",
    "usageExamples": [
      "<InplaceWrapper><InplaceDisplay>View Content</InplaceDisplay><InplaceContent><InputText /></InplaceContent></InplaceWrapper>",
      "<InplaceWrapper closable><InplaceDisplay>{text || 'Click to Edit'}</InplaceDisplay><InplaceContent><InputText value={text} onChange={(e) => setText(e.target.value)} /></InplaceContent></InplaceWrapper>"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "active",
        "type": "boolean",
        "optional": true,
        "description": "Active state",
        "helpText": "Controls edit mode (controlled component)",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false",
          "isEditing"
        ]
      },
      {
        "name": "closable",
        "type": "boolean",
        "optional": true,
        "description": "Show close button",
        "helpText": "Displays button to exit edit mode",
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
        "helpText": "Disables the inplace",
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
      "type": "InplaceDisplay and InplaceContent",
      "description": "Display and edit content",
      "helpText": "Must contain InplaceDisplay and InplaceContent children"
    }
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onToggle",
        "type": "(e: { value: boolean }) => void",
        "description": "Callback when mode toggles"
      },
      {
        "name": "onOpen",
        "type": "() => void",
        "description": "Callback when edit mode opens"
      },
      {
        "name": "onClose",
        "type": "() => void",
        "description": "Callback when edit mode closes"
      }
    ],
    "simplified": [
      {
        "name": "onActiveChange",
        "type": "(active: boolean) => void",
        "description": "Simplified callback with active state"
      }
    ],
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
      "handleToggle - Processes onToggle event, calls onToggle and onActiveChange",
      "handleOpen - Processes onOpen event",
      "handleClose - Processes onClose event"
    ],
    "patterns": [
      "Check if event handler exists before calling"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [
      "InplaceDisplay",
      "InplaceContent"
    ],
    "childrenDescription": "Inplace must contain InplaceDisplay (view mode) and InplaceContent (edit mode) as children",
    "hasChildren": true,
    "examples": [
      "<InplaceWrapper><InplaceDisplay>Click to edit</InplaceDisplay><InplaceContent><InputText /></InplaceContent></InplaceWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<InplaceWrapper><InplaceDisplay>View Content</InplaceDisplay><InplaceContent><InputText /></InplaceContent></InplaceWrapper>",
    "withStyling": "<InplaceWrapper closable className=\"mb-3\"><InplaceDisplay>{text}</InplaceDisplay><InplaceContent><InputText value={text} onChange={(e) => setText(e.target.value)} /></InplaceContent></InplaceWrapper>",
    "withEvents": "<InplaceWrapper onOpen={() => console.log('editing')} onClose={() => console.log('closed')}><InplaceDisplay>Edit</InplaceDisplay><InplaceContent><InputText /></InplaceContent></InplaceWrapper>",
    "withRedux": "<InplaceWrapper active={isEditing} onActiveChange={(val) => dispatch(setEditing(val))}><InplaceDisplay>{value}</InplaceDisplay><InplaceContent><InputText value={value} onChange={(e) => dispatch(setValue(e.target.value))} /></InplaceContent></InplaceWrapper>",
    "withValidation": "N/A",
    "withChildren": "<InplaceWrapper closable><InplaceDisplay><span>{name || 'Click to edit name'}</span></InplaceDisplay><InplaceContent><InputText value={name} onChange={(e) => setName(e.target.value)} /></InplaceContent></InplaceWrapper>"
  }
};

const InplaceWrapper = (props) => {
  const {
    active, closable, disabled, className, style, children, onToggle, onOpen, onClose, onActiveChange, onMount, onUnmount,
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
    active,
    closable,
    disabled,
    className,
    style,
    onToggle,
    onOpen,
    onClose,
    ref: componentRef,
    ...restProps
  };

  return (
    <Inplace {...primeReactProps}>
      {children}
    </Inplace>
  );
};

InplaceWrapper.displayName = 'InplaceWrapper';

export default InplaceWrapper;
