/**
 * RippleWrapper - Enhanced wrapper for PrimeReact Ripple
 * Category: Utility
 * 
 * Material Design ripple effect for interactive elements
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Ripple } from 'primereact/ripple';

// Component metadata embedded for runtime access
export const RippleMetadata = {
  "name": "Ripple",
  "import": "Ripple",
  "category": "Utility",
  "metadata": {
    "description": "Material Design ripple effect for interactive elements",
    "usageExamples": [
      "<div className=\"p-ripple\"><Button label=\"Click\" /><RippleWrapper /></div>",
      "<div className=\"p-ripple\" style={{ position: 'relative' }}><span>Clickable</span><RippleWrapper /></div>"
    ]
  },
  "propsInterface": {
    "componentSpecific": [],
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
      "Add 'p-ripple' class to parent element",
      "Parent must have position: relative",
      "Place Ripple component as child of interactive element"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children. It must be placed inside an element with 'p-ripple' class.",
    "hasChildren": false,
    "examples": []
  },
  "stylingSupport": {
    "primeFlex": false,
    "responsive": false,
    "customCSS": false,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<div className=\"p-ripple\"><Button label=\"Click\" /><RippleWrapper /></div>",
    "withStyling": "<div className=\"p-ripple\" style={{ position: 'relative', padding: '1rem' }}><span>Click me</span><RippleWrapper /></div>",
    "withEvents": "N/A",
    "withRedux": "N/A",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const RippleWrapper = (props) => {
  const {
    ,
    ...restProps
  } = props;

  const componentRef = useRef(null);

  // Build props for underlying PrimeReact component
  const primeReactProps = {
    ref: componentRef,
    ...restProps
  };

  return (
    <Ripple {...primeReactProps} />
  );
};

RippleWrapper.displayName = 'RippleWrapper';

export default RippleWrapper;
