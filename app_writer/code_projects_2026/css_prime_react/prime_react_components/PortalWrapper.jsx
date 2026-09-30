/**
 * PortalWrapper - Enhanced wrapper for PrimeReact Portal
 * Category: Utility
 * 
 * Renders content in a different DOM location for overlay positioning
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Portal } from 'primereact/portal';

// Component metadata embedded for runtime access
export const PortalMetadata = {
  "name": "Portal",
  "import": "Portal",
  "category": "Utility",
  "metadata": {
    "description": "Renders content in a different DOM location for overlay positioning",
    "usageExamples": [
      "<PortalWrapper><div>Content rendered at document.body</div></PortalWrapper>",
      "<PortalWrapper appendTo={document.getElementById('portal-root')}><Tooltip /></PortalWrapper>"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "appendTo",
        "type": "'body' | 'self' | HTMLElement",
        "optional": true,
        "description": "DOM element to append content",
        "helpText": "Where to render the portal content (default: document.body)",
        "dataTypes": [
          "'body'",
          "'self'",
          "HTMLElement"
        ],
        "examples": [
          "'body'",
          "document.getElementById('portal-root')"
        ]
      }
    ],
    "styling": [],
    "children": {
      "type": "React.ReactNode",
      "required": true,
      "description": "Content to be rendered in portal"
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
      "For overlays: Render tooltips, dialogs outside parent DOM hierarchy",
      "For z-index issues: Move content to body to avoid stacking context problems"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [
      "Any React component"
    ],
    "childrenDescription": "Can contain any content. Children are rendered at the specified DOM location instead of in the normal component tree.",
    "hasChildren": true,
    "examples": [
      "<PortalWrapper><Tooltip target=\".my-button\" /></PortalWrapper>",
      "<PortalWrapper appendTo={document.body}><Dialog visible={visible}>Content</Dialog></PortalWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": false,
    "responsive": false,
    "customCSS": false,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<PortalWrapper><div>Portal content</div></PortalWrapper>",
    "withStyling": "N/A",
    "withEvents": "N/A",
    "withRedux": "<PortalWrapper><Dialog visible={isOpen}>{content}</Dialog></PortalWrapper>",
    "withValidation": "N/A",
    "withChildren": "<PortalWrapper appendTo={document.getElementById('modals')}><Dialog visible={visible}><form>...</form></Dialog></PortalWrapper>"
  }
};

const PortalWrapper = (props) => {
  const {
    appendTo, children, onMount,
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
    appendTo,
    ref: componentRef,
    ...restProps
  };

  return (
    <Portal {...primeReactProps}>
      {children}
    </Portal>
  );
};

PortalWrapper.displayName = 'PortalWrapper';

export default PortalWrapper;
