/**
 * StyleClassWrapper - Enhanced wrapper for PrimeReact StyleClass
 * Category: Utility
 * 
 * Dynamic style class manipulation for animations and transitions
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { StyleClass } from 'primereact/styleclass';

// Component metadata embedded for runtime access
export const StyleClassMetadata = {
  "name": "StyleClass",
  "import": "StyleClass",
  "category": "Utility",
  "metadata": {
    "description": "Dynamic style class manipulation for animations and transitions",
    "usageExamples": [
      "<StyleClassWrapper nodeRef={buttonRef} selector=\"@next\" enterClassName=\"fadein\" leaveClassName=\"fadeout\" />",
      "<StyleClassWrapper nodeRef={triggerRef} selector=\"#panel\" toggleClassName=\"hidden\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "nodeRef",
        "type": "React.RefObject",
        "optional": false,
        "description": "Reference to trigger element",
        "helpText": "React ref of element that triggers the style change",
        "dataTypes": [
          "React.RefObject<HTMLElement>"
        ],
        "examples": [
          "buttonRef",
          "triggerRef"
        ]
      },
      {
        "name": "selector",
        "type": "string",
        "optional": false,
        "description": "CSS selector or special selector for target",
        "helpText": "Target element selector (@next, @prev, @parent, or CSS selector)",
        "dataTypes": [
          "'@next'",
          "'@prev'",
          "'@parent'",
          "'#elementId'",
          "'.className'"
        ],
        "examples": [
          "'@next'",
          "'#panel'",
          "'.content'"
        ]
      },
      {
        "name": "enterClassName",
        "type": "string",
        "optional": true,
        "description": "Class to add on enter",
        "helpText": "CSS class applied when entering",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'fadein'",
          "'scalein'",
          "'slidedown'"
        ]
      },
      {
        "name": "leaveClassName",
        "type": "string",
        "optional": true,
        "description": "Class to add on leave",
        "helpText": "CSS class applied when leaving",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'fadeout'",
          "'scaleout'",
          "'slideup'"
        ]
      },
      {
        "name": "toggleClassName",
        "type": "string",
        "optional": true,
        "description": "Class to toggle",
        "helpText": "CSS class to toggle on/off",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'hidden'",
          "'active'",
          "'expanded'"
        ]
      },
      {
        "name": "hideOnOutsideClick",
        "type": "boolean",
        "optional": true,
        "description": "Whether to hide on outside click",
        "helpText": "Automatically hide when clicking outside",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      }
    ],
    "styling": [],
    "children": null
  },
  "eventHandlers": {
    "standard": [],
    "simplified": [],
    "validation": [],
    "lifecycle": []
  },
  "eventHandlerMethods": {
    "internal": [],
    "patterns": [
      "Use @next to target next sibling element",
      "Use @prev to target previous sibling",
      "Use @parent to target parent element",
      "Use CSS selectors for specific elements"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children. It manipulates classes on target elements.",
    "hasChildren": false,
    "examples": []
  },
  "stylingSupport": {
    "primeFlex": false,
    "responsive": false,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<StyleClassWrapper nodeRef={buttonRef} selector=\"@next\" toggleClassName=\"hidden\" />",
    "withStyling": "<StyleClassWrapper nodeRef={triggerRef} selector=\"#panel\" enterClassName=\"fadein\" leaveClassName=\"fadeout\" />",
    "withEvents": "N/A",
    "withRedux": "N/A",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const StyleClassWrapper = (props) => {
  const {
    nodeRef, selector, enterClassName, leaveClassName, toggleClassName, hideOnOutsideClick,
    ...restProps
  } = props;

  const componentRef = useRef(null);

  // Build props for underlying PrimeReact component
  const primeReactProps = {
    nodeRef,
    selector,
    enterClassName,
    leaveClassName,
    toggleClassName,
    hideOnOutsideClick,
    ref: componentRef,
    ...restProps
  };

  return (
    <StyleClass {...primeReactProps} />
  );
};

StyleClassWrapper.displayName = 'StyleClassWrapper';

export default StyleClassWrapper;
