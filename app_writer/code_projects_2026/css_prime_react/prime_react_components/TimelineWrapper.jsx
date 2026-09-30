/**
 * TimelineWrapper - Enhanced wrapper for PrimeReact Timeline
 * Category: Data
 * 
 * Chronological event display
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Timeline } from 'primereact/timeline';

// Component metadata embedded for runtime access
export const TimelineMetadata = {
  "name": "Timeline",
  "import": "Timeline",
  "category": "Data",
  "metadata": {
    "description": "Chronological event display",
    "usageExamples": [
      "<TimelineWrapper value={events} content={(item) => item.status} />",
      "<TimelineWrapper value={timeline} align=\"alternate\" layout=\"vertical\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "any[]",
        "optional": false,
        "description": "Events array",
        "helpText": "Array of timeline event objects",
        "dataTypes": [
          "any[]"
        ],
        "examples": [
          "[{status: 'Ordered', date: '15/10/2020'}]"
        ]
      },
      {
        "name": "align",
        "type": "'left' | 'right' | 'alternate' | 'top' | 'bottom'",
        "optional": true,
        "description": "Content alignment",
        "helpText": "Position of content relative to timeline",
        "dataTypes": [
          "'left' (default)",
          "'right'",
          "'alternate'",
          "'top'",
          "'bottom'"
        ],
        "examples": [
          "'left'",
          "'alternate'"
        ]
      },
      {
        "name": "layout",
        "type": "'vertical' | 'horizontal'",
        "optional": true,
        "description": "Timeline orientation",
        "helpText": "Direction of timeline",
        "dataTypes": [
          "'vertical' (default)",
          "'horizontal'"
        ],
        "examples": [
          "'vertical'",
          "'horizontal'"
        ]
      },
      {
        "name": "content",
        "type": "(item: any, index: number) => React.ReactNode",
        "optional": true,
        "description": "Content template",
        "helpText": "Function to render event content",
        "dataTypes": [
          "function"
        ],
        "examples": [
          "(item) => <div>{item.status}</div>"
        ]
      },
      {
        "name": "opposite",
        "type": "(item: any, index: number) => React.ReactNode",
        "optional": true,
        "description": "Opposite content template",
        "helpText": "Function to render opposite side content",
        "dataTypes": [
          "function"
        ],
        "examples": [
          "(item) => <small>{item.date}</small>"
        ]
      },
      {
        "name": "marker",
        "type": "(item: any, index: number) => React.ReactNode",
        "optional": true,
        "description": "Marker template",
        "helpText": "Function to render custom marker",
        "dataTypes": [
          "function"
        ],
        "examples": [
          "(item) => <i className=\"pi pi-check\" />"
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
          "'custom-timeline'"
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
    "patterns": []
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children - events defined via value prop and templates",
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
    "basic": "<TimelineWrapper value={events} content={(item) => item.status} />",
    "withStyling": "<TimelineWrapper value={timeline} align=\"alternate\" layout=\"vertical\" className=\"custom-timeline\" />",
    "withEvents": "N/A",
    "withRedux": "<TimelineWrapper value={historyEvents} content={(item) => <div>{item.action}</div>} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const TimelineWrapper = (props) => {
  const {
    value, align, layout, content, opposite, marker, className, style, onMount, onUnmount,
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
    value,
    align,
    layout,
    content,
    opposite,
    marker,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <Timeline {...primeReactProps} />
  );
};

TimelineWrapper.displayName = 'TimelineWrapper';

export default TimelineWrapper;
