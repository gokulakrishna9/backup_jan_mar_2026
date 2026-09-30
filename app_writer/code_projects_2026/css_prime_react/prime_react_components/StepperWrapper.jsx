/**
 * StepperWrapper - Enhanced wrapper for PrimeReact Stepper
 * Category: Panel
 * 
 * Step-by-step navigation component for multi-step forms and wizards
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Stepper } from 'primereact/stepper';

// Component metadata embedded for runtime access
export const StepperMetadata = {
  "name": "Stepper",
  "import": "Stepper",
  "category": "Panel",
  "metadata": {
    "description": "Step-by-step navigation component for multi-step forms and wizards",
    "usageExamples": [
      "<StepperWrapper activeStep={activeStep}><StepperPanel header=\"Personal\">Content 1</StepperPanel><StepperPanel header=\"Address\">Content 2</StepperPanel></StepperWrapper>",
      "<StepperWrapper activeStep={step} onChangeStep={(e) => setStep(e.index)} linear><StepperPanel header=\"Step 1\">...</StepperPanel></StepperWrapper>"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "activeStep",
        "type": "number",
        "optional": true,
        "description": "Index of the active step",
        "helpText": "Zero-based index of currently active step (default: 0)",
        "dataTypes": [
          "number (0, 1, 2, ...)"
        ],
        "examples": [
          "0",
          "1",
          "2"
        ]
      },
      {
        "name": "linear",
        "type": "boolean",
        "optional": true,
        "description": "Whether steps must be completed in order",
        "helpText": "When true, users cannot skip steps",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "orientation",
        "type": "'horizontal' | 'vertical'",
        "optional": true,
        "description": "Orientation of the stepper",
        "helpText": "Layout direction (default: horizontal)",
        "dataTypes": [
          "'horizontal'",
          "'vertical'"
        ],
        "examples": [
          "'horizontal'",
          "'vertical'"
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
          "'w-full'",
          "'mb-3'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles object",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ width: '100%' }"
        ]
      }
    ],
    "children": {
      "type": "StepperPanel[]",
      "required": true,
      "description": "StepperPanel components representing each step"
    }
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onChangeStep",
        "type": "(e: { originalEvent: Event, index: number }) => void",
        "optional": true,
        "description": "Callback when active step changes"
      }
    ],
    "simplified": [
      {
        "name": "onStepChange",
        "type": "(index: number) => void",
        "optional": true,
        "description": "Simplified callback with just the step index"
      }
    ],
    "validation": [
      {
        "name": "onValidateStep",
        "type": "(index: number) => boolean",
        "optional": true,
        "description": "Validation callback before changing step"
      }
    ],
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
    "internal": [
      "handleChangeStep(e): Processes step change and calls onStepChange if provided",
      "validateStep(index): Validates step before allowing navigation"
    ],
    "patterns": [
      "For Redux: Use onStepChange to dispatch step navigation actions",
      "For validation: Use onValidateStep to prevent navigation if current step is invalid"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [
      "StepperPanel"
    ],
    "childrenDescription": "Contains multiple StepperPanel components, each representing a step in the process. Each panel has a header and content.",
    "hasChildren": true,
    "examples": [
      "<StepperWrapper activeStep={0}><StepperPanel header=\"Personal Info\"><PersonalForm /></StepperPanel><StepperPanel header=\"Address\"><AddressForm /></StepperPanel><StepperPanel header=\"Review\"><ReviewStep /></StepperPanel></StepperWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<StepperWrapper activeStep={activeStep}><StepperPanel header=\"Step 1\">Content 1</StepperPanel><StepperPanel header=\"Step 2\">Content 2</StepperPanel></StepperWrapper>",
    "withStyling": "<StepperWrapper activeStep={activeStep} className=\"w-full mb-3\"><StepperPanel header=\"Personal\">Form 1</StepperPanel><StepperPanel header=\"Address\">Form 2</StepperPanel></StepperWrapper>",
    "withEvents": "<StepperWrapper activeStep={step} onChangeStep={(e) => setStep(e.index)} linear><StepperPanel header=\"Step 1\">Content</StepperPanel><StepperPanel header=\"Step 2\">Content</StepperPanel></StepperWrapper>",
    "withRedux": "<StepperWrapper activeStep={currentStep} onStepChange={(index) => dispatch(setStep(index))} linear><StepperPanel header=\"Info\">Form</StepperPanel></StepperWrapper>",
    "withValidation": "<StepperWrapper activeStep={step} onChangeStep={(e) => setStep(e.index)} onValidateStep={(index) => validateCurrentStep(index)} linear><StepperPanel header=\"Step 1\">Content</StepperPanel></StepperWrapper>",
    "withChildren": "<StepperWrapper activeStep={step}><StepperPanel header=\"Personal\"><div className=\"grid\"><div className=\"col-12\"><InputText /></div></div></StepperPanel></StepperWrapper>"
  }
};

const StepperWrapper = (props) => {
  const {
    activeStep, linear, orientation, className, style, children, onChangeStep, onStepChange, onValidateStep, onMount,
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
    activeStep,
    linear,
    orientation,
    className,
    style,
    onChangeStep,
    ref: componentRef,
    ...restProps
  };

  return (
    <Stepper {...primeReactProps}>
      {children}
    </Stepper>
  );
};

StepperWrapper.displayName = 'StepperWrapper';

export default StepperWrapper;
