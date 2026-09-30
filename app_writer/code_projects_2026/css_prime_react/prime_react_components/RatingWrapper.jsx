/**
 * RatingWrapper - Enhanced wrapper for PrimeReact Rating
 * Category: Form
 * 
 * Star rating input
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Rating } from 'primereact/rating';

// Component metadata embedded for runtime access
export const RatingMetadata = {
  "name": "Rating",
  "import": "Rating",
  "category": "Form",
  "metadata": {
    "description": "Star rating input",
    "usageExamples": [
      "<RatingWrapper value={rating} onChange={(e) => setRating(e.value)} />",
      "<RatingWrapper value={stars} stars={10} cancel={false} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "number | null",
        "optional": true,
        "description": "Rating value",
        "helpText": "Current rating (controlled component)",
        "dataTypes": [
          "number",
          "null"
        ],
        "examples": [
          "3",
          "5",
          "null"
        ]
      },
      {
        "name": "stars",
        "type": "number",
        "optional": true,
        "description": "Number of stars",
        "helpText": "Total stars to display (default: 5)",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "5",
          "10"
        ]
      },
      {
        "name": "cancel",
        "type": "boolean",
        "optional": true,
        "description": "Show cancel icon",
        "helpText": "Displays icon to clear rating (default: true)",
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
        "helpText": "Disables the rating",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "readOnly",
        "type": "boolean",
        "optional": true,
        "description": "Read-only mode",
        "helpText": "Display only, no interaction",
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
          "{ fontSize: '2rem' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onChange",
        "type": "(e: { value: number | null }) => void",
        "description": "Callback when rating changes"
      }
    ],
    "simplified": [
      {
        "name": "onValueChange",
        "type": "(value: number | null) => void",
        "description": "Simplified callback with just the value"
      }
    ],
    "validation": [
      {
        "name": "onValidate",
        "type": "(value: number | null) => boolean | string",
        "description": "Validation callback"
      },
      {
        "name": "onError",
        "type": "(error: string) => void",
        "description": "Called when validation fails"
      }
    ],
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
      "handleChange - Processes onChange event, calls onChange, onValueChange, onValidate"
    ],
    "patterns": [
      "Check if event handler exists before calling",
      "Extract value from event object",
      "Run validation on change"
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
    "basic": "<RatingWrapper value={rating} onChange={(e) => setRating(e.value)} />",
    "withStyling": "<RatingWrapper value={stars} stars={10} cancel={false} className=\"mb-3\" />",
    "withEvents": "<RatingWrapper value={userRating} onChange={handleChange} />",
    "withRedux": "<RatingWrapper value={productRating} onValueChange={(val) => dispatch(setRating(val))} />",
    "withValidation": "<RatingWrapper value={rating} onValidate={(val) => val && val > 0 ? true : 'Rating required'} onError={(err) => setError(err)} />",
    "withChildren": "N/A"
  }
};

const RatingWrapper = (props) => {
  const {
    value, stars, cancel, disabled, readOnly, className, style, onChange, onValueChange, onValidate, onError, onMount, onUnmount,
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

  // Simplified event handler: onValueChange
  const handleChange = (e) => {
    if (onChange) {
      onChange(e);
    }
    if (onValueChange) {
      onValueChange(e.value || e.data || e);
    }
  };

  // Build props for underlying PrimeReact component
  const primeReactProps = {
    value,
    stars,
    cancel,
    disabled,
    readOnly,
    className,
    style,
    onChange: handleChange,
    ref: componentRef,
    ...restProps
  };

  return (
    <Rating {...primeReactProps} />
  );
};

RatingWrapper.displayName = 'RatingWrapper';

export default RatingWrapper;
