/**
 * FocusTrapWrapper - Enhanced wrapper for PrimeReact FocusTrap
 * Category: Utility
 * 
 * Traps focus within an element for modal accessibility and keyboard navigation
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { FocusTrap } from 'primereact/focustrap';

// Component metadata embedded for runtime access
export const FocusTrapMetadata = {
  "name": "FocusTrap",
  "import": "FocusTrap",
  "category": "Utility",
  "metadata": {
    "description": "Traps focus within an element for modal accessibility and keyboard navigation",
    "usageExamples": [
      "<FocusTrapWrapper><Dialog visible={visible}>Content</Dialog></FocusTrapWrapper>",
      "<FocusTrapWrapper><div className=\"modal\">Modal content</div></FocusTrapWrapper>"
    ]
  },
  "propsInterface": {
    "componentSpecific": [],
    "styling": [
      {
        "name": "className",
        "type": "string",
        "optional": true,
        "description": "Additional CSS classes for custom styling",
        "helpText": "Supports PrimeFlex utility classes and custom CSS",
        "examples": [
          "'focus-trap-container'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles object",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ position: 'relative' }"
        ]
      }
    ],
    "children": {
      "type": "React.ReactNode",
      "required": true,
      "description": "Content where focus should be trapped"
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
        "optional": true,
        "description": "Callback when component mounts"
      }
    ]
  },
  "eventHandlerMethods": {
    "internal": [],
    "patterns": [
      "For modals: Wrap modal content to trap focus within dialog",
      "For accessibility: Ensures keyboard navigation stays within component"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [
      "Any React component"
    ],
    "childrenDescription": "Can contain any content. Focus will be trapped within the children when active.",
    "hasChildren": true,
    "examples": [
      "<FocusTrapWrapper><Dialog visible={visible}><form>...</form></Dialog></FocusTrapWrapper>",
      "<FocusTrapWrapper><div className=\"modal\"><Button /><InputText /></div></FocusTrapWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<FocusTrapWrapper><Dialog visible={visible}>Content</Dialog></FocusTrapWrapper>",
    "withStyling": "<FocusTrapWrapper className=\"focus-container\"><div className=\"modal p-4\">Modal content</div></FocusTrapWrapper>",
    "withEvents": "N/A",
    "withRedux": "<FocusTrapWrapper><Dialog visible={isModalOpen}>{modalContent}</Dialog></FocusTrapWrapper>",
    "withValidation": "N/A",
    "withChildren": "<FocusTrapWrapper><div className=\"custom-modal\"><InputText /><Button label=\"Submit\" /><Button label=\"Cancel\" /></div></FocusTrapWrapper>"
  }
};

const FocusTrapWrapper = (props) => {
  const {
    className, style, children, onMount,
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
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <FocusTrap {...primeReactProps}>
      {children}
    </FocusTrap>
  );
};

FocusTrapWrapper.displayName = 'FocusTrapWrapper';

export default FocusTrapWrapper;
