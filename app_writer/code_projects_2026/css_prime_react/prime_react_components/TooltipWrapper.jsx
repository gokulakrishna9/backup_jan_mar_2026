/**
 * TooltipWrapper - Enhanced wrapper for PrimeReact Tooltip
 * Category: Overlay
 * 
 * Tooltip overlay for elements
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Tooltip } from 'primereact/tooltip';

// Component metadata embedded for runtime access
export const TooltipMetadata = {
  "name": "Tooltip",
  "import": "Tooltip",
  "category": "Overlay",
  "metadata": {
    "description": "Tooltip overlay for elements",
    "usageExamples": [
      "<TooltipWrapper target=\".custom-target\" />; <Button className=\"custom-target\" data-pr-tooltip=\"Tooltip text\" />",
      "<TooltipWrapper target=\".my-button\" position=\"top\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "target",
        "type": "string | HTMLElement",
        "optional": false,
        "description": "Target selector",
        "helpText": "CSS selector or element to attach tooltip",
        "dataTypes": [
          "string (CSS selector)",
          "HTMLElement"
        ],
        "examples": [
          "'.custom-target'",
          "'#myButton'",
          "buttonRef.current"
        ]
      },
      {
        "name": "position",
        "type": "'right' | 'left' | 'top' | 'bottom'",
        "optional": true,
        "description": "Tooltip position",
        "helpText": "Where tooltip appears relative to target",
        "dataTypes": [
          "'right' (default)",
          "'left'",
          "'top'",
          "'bottom'"
        ],
        "examples": [
          "'top'",
          "'right'"
        ]
      },
      {
        "name": "event",
        "type": "'hover' | 'focus' | 'both'",
        "optional": true,
        "description": "Trigger event",
        "helpText": "Event that shows tooltip",
        "dataTypes": [
          "'hover' (default)",
          "'focus'",
          "'both'"
        ],
        "examples": [
          "'hover'",
          "'focus'"
        ]
      },
      {
        "name": "mouseTrack",
        "type": "boolean",
        "optional": true,
        "description": "Follow mouse",
        "helpText": "Tooltip follows mouse cursor",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "showDelay",
        "type": "number",
        "optional": true,
        "description": "Show delay",
        "helpText": "Milliseconds before showing",
        "dataTypes": [
          "number (milliseconds)"
        ],
        "examples": [
          "0",
          "500",
          "1000"
        ]
      },
      {
        "name": "hideDelay",
        "type": "number",
        "optional": true,
        "description": "Hide delay",
        "helpText": "Milliseconds before hiding",
        "dataTypes": [
          "number (milliseconds)"
        ],
        "examples": [
          "0",
          "300"
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
          "'custom-tooltip'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ maxWidth: '300px' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [],
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
    "internal": [],
    "patterns": [
      "Target elements use data-pr-tooltip attribute for content",
      "Use data-pr-position to override position per element"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children - tooltip content defined via data-pr-tooltip attribute on target elements",
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
    "basic": "<TooltipWrapper target=\".custom-target\" />; <Button className=\"custom-target\" data-pr-tooltip=\"Tooltip text\" />",
    "withStyling": "<TooltipWrapper target=\".my-button\" position=\"top\" className=\"custom-tooltip\" />",
    "withEvents": "N/A",
    "withRedux": "N/A",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const TooltipWrapper = (props) => {
  const {
    target, position, event, mouseTrack, showDelay, hideDelay, className, style, onMount, onUnmount,
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
    target,
    position,
    event,
    mouseTrack,
    showDelay,
    hideDelay,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <Tooltip {...primeReactProps} />
  );
};

TooltipWrapper.displayName = 'TooltipWrapper';

export default TooltipWrapper;
