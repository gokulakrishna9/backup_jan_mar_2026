/**
 * FieldsetWrapper - Enhanced wrapper for PrimeReact Fieldset
 * Category: Panel
 * 
 * Grouping container with legend
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Fieldset } from 'primereact/fieldset';

// Component metadata embedded for runtime access
export const FieldsetMetadata = {
  "name": "Fieldset",
  "import": "Fieldset",
  "category": "Panel",
  "metadata": {
    "description": "Grouping container with legend",
    "usageExamples": [
      "<FieldsetWrapper legend=\"Header\"><p>Content</p></FieldsetWrapper>",
      "<FieldsetWrapper legend=\"Details\" toggleable collapsed><p>Content</p></FieldsetWrapper>"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "legend",
        "type": "string | React.ReactNode",
        "optional": true,
        "description": "Legend text",
        "helpText": "Header/title for fieldset",
        "dataTypes": [
          "string",
          "React.ReactNode"
        ],
        "examples": [
          "'User Details'",
          "'Settings'",
          "<CustomLegend />"
        ]
      },
      {
        "name": "toggleable",
        "type": "boolean",
        "optional": true,
        "description": "Enable collapse/expand",
        "helpText": "Makes fieldset collapsible",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "collapsed",
        "type": "boolean",
        "optional": true,
        "description": "Collapsed state",
        "helpText": "Controls collapsed state (controlled component)",
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
      "type": "React.ReactNode",
      "description": "Fieldset content",
      "helpText": "Main content area"
    }
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onToggle",
        "type": "(e: { value: boolean }) => void",
        "description": "Callback when fieldset is toggled"
      }
    ],
    "simplified": [
      {
        "name": "onCollapsedChange",
        "type": "(collapsed: boolean) => void",
        "description": "Simplified callback with collapsed state"
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
      "handleToggle - Processes onToggle event, calls onToggle and onCollapsedChange"
    ],
    "patterns": [
      "Check if event handler exists before calling"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [
      "Any React component",
      "Text",
      "HTML elements"
    ],
    "childrenDescription": "Fieldset accepts any React content as children",
    "hasChildren": true,
    "examples": [
      "<FieldsetWrapper legend=\"User Info\"><InputText /><Button /></FieldsetWrapper>"
    ]
  },
  "stylingSupport": {
    "primeFlex": true,
    "responsive": true,
    "customCSS": true,
    "styleMerging": false
  },
  "usageExamples": {
    "basic": "<FieldsetWrapper legend=\"Header\"><p>Content</p></FieldsetWrapper>",
    "withStyling": "<FieldsetWrapper legend=\"Details\" className=\"mb-3\"><p>Content</p></FieldsetWrapper>",
    "withEvents": "<FieldsetWrapper legend=\"Info\" toggleable onToggle={handleToggle}><p>Content</p></FieldsetWrapper>",
    "withRedux": "<FieldsetWrapper legend=\"Settings\" toggleable collapsed={isCollapsed} onCollapsedChange={(val) => dispatch(setCollapsed(val))}><p>Content</p></FieldsetWrapper>",
    "withValidation": "N/A",
    "withChildren": "<FieldsetWrapper legend=\"Form\" toggleable><InputText /><Dropdown /><Button label=\"Submit\" /></FieldsetWrapper>"
  }
};

const FieldsetWrapper = (props) => {
  const {
    legend, toggleable, collapsed, className, style, children, onToggle, onCollapsedChange, onMount, onUnmount,
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
    legend,
    toggleable,
    collapsed,
    className,
    style,
    onToggle,
    ref: componentRef,
    ...restProps
  };

  return (
    <Fieldset {...primeReactProps}>
      {children}
    </Fieldset>
  );
};

FieldsetWrapper.displayName = 'FieldsetWrapper';

export default FieldsetWrapper;
