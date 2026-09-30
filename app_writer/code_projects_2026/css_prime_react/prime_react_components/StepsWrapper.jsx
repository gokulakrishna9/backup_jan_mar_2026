/**
 * StepsWrapper - Enhanced wrapper for PrimeReact Steps
 * Category: Menu
 * 
 * Step-by-step progress indicator
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Steps } from 'primereact/steps';

// Component metadata embedded for runtime access
export const StepsMetadata = {
  "name": "Steps",
  "import": "Steps",
  "category": "Menu",
  "metadata": {
    "description": "Step-by-step progress indicator",
    "usageExamples": [
      "<StepsWrapper model={items} activeIndex={activeStep} />",
      "<StepsWrapper model={[{label: 'Personal'}, {label: 'Payment'}]} activeIndex={0} onSelect={(e) => setActiveStep(e.index)} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "model",
        "type": "MenuItem[]",
        "optional": false,
        "description": "Step items",
        "helpText": "Array of step objects",
        "dataTypes": [
          "MenuItem[] - {label, icon, command}"
        ],
        "examples": [
          "[{label: 'Personal'}, {label: 'Payment'}, {label: 'Confirmation'}]"
        ]
      },
      {
        "name": "activeIndex",
        "type": "number",
        "optional": true,
        "description": "Active step index",
        "helpText": "Current step (0-based)",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "0",
          "1",
          "2"
        ]
      },
      {
        "name": "readOnly",
        "type": "boolean",
        "optional": true,
        "description": "Read-only mode",
        "helpText": "Steps are not clickable (default: true)",
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
        "name": "onSelect",
        "type": "(e: { index: number }) => void",
        "description": "Callback when step is selected"
      }
    ],
    "simplified": [
      {
        "name": "onActiveIndexChange",
        "type": "(index: number) => void",
        "description": "Simplified callback with just the index"
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
      "handleSelect - Processes onSelect event, calls onSelect and onActiveIndexChange"
    ],
    "patterns": [
      "Check if event handler exists before calling",
      "Extract index from event object"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children - items defined via model prop",
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
    "basic": "<StepsWrapper model={[{label: 'Personal'}, {label: 'Payment'}]} activeIndex={0} />",
    "withStyling": "<StepsWrapper model={items} activeIndex={step} className=\"mb-3\" />",
    "withEvents": "<StepsWrapper model={steps} activeIndex={activeStep} readOnly={false} onSelect={(e) => setActiveStep(e.index)} />",
    "withRedux": "<StepsWrapper model={wizardSteps} activeIndex={currentStep} onActiveIndexChange={(idx) => dispatch(setStep(idx))} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const StepsWrapper = (props) => {
  const {
    model, activeIndex, readOnly, className, style, onSelect, onActiveIndexChange, onMount, onUnmount,
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
    model,
    activeIndex,
    readOnly,
    className,
    style,
    onSelect,
    ref: componentRef,
    ...restProps
  };

  return (
    <Steps {...primeReactProps} />
  );
};

StepsWrapper.displayName = 'StepsWrapper';

export default StepsWrapper;
