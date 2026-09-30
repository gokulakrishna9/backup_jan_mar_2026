/**
 * PickListWrapper - Enhanced wrapper for PrimeReact PickList
 * Category: Data
 * 
 * Dual list for transferring items
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { PickList } from 'primereact/picklist';

// Component metadata embedded for runtime access
export const PickListMetadata = {
  "name": "PickList",
  "import": "PickList",
  "category": "Data",
  "metadata": {
    "description": "Dual list for transferring items",
    "usageExamples": [
      "<PickListWrapper source={source} target={target} itemTemplate={itemTemplate} onChange={onChange} />",
      "<PickListWrapper source={available} target={selected} sourceHeader=\"Available\" targetHeader=\"Selected\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "source",
        "type": "any[]",
        "optional": false,
        "description": "Source items",
        "helpText": "Array of available items",
        "dataTypes": [
          "any[]"
        ],
        "examples": [
          "[{id: 1, name: 'Item 1'}]",
          "availableProducts"
        ]
      },
      {
        "name": "target",
        "type": "any[]",
        "optional": false,
        "description": "Target items",
        "helpText": "Array of selected items",
        "dataTypes": [
          "any[]"
        ],
        "examples": [
          "[{id: 2, name: 'Item 2'}]",
          "selectedProducts"
        ]
      },
      {
        "name": "itemTemplate",
        "type": "(item: any) => React.ReactNode",
        "optional": true,
        "description": "Item template",
        "helpText": "Function to render each item",
        "dataTypes": [
          "function"
        ],
        "examples": [
          "(item) => <div>{item.name}</div>"
        ]
      },
      {
        "name": "sourceHeader",
        "type": "string | React.ReactNode",
        "optional": true,
        "description": "Source list header",
        "helpText": "Header for source list",
        "dataTypes": [
          "string",
          "React.ReactNode"
        ],
        "examples": [
          "'Available'",
          "'Products'"
        ]
      },
      {
        "name": "targetHeader",
        "type": "string | React.ReactNode",
        "optional": true,
        "description": "Target list header",
        "helpText": "Header for target list",
        "dataTypes": [
          "string",
          "React.ReactNode"
        ],
        "examples": [
          "'Selected'",
          "'Chosen'"
        ]
      },
      {
        "name": "showSourceControls",
        "type": "boolean",
        "optional": true,
        "description": "Show source controls",
        "helpText": "Shows reorder buttons for source list (default: true)",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "showTargetControls",
        "type": "boolean",
        "optional": true,
        "description": "Show target controls",
        "helpText": "Shows reorder buttons for target list (default: true)",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "dataKey",
        "type": "string",
        "optional": true,
        "description": "Unique item identifier",
        "helpText": "Property name for unique ID",
        "dataTypes": [
          "string (property name)"
        ],
        "examples": [
          "'id'",
          "'code'"
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
          "'w-full'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ width: '100%' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onChange",
        "type": "(e: { source: any[], target: any[] }) => void",
        "description": "Callback when items are transferred"
      },
      {
        "name": "onMoveToSource",
        "type": "(e: { value: any[] }) => void",
        "description": "Callback when items move to source"
      },
      {
        "name": "onMoveToTarget",
        "type": "(e: { value: any[] }) => void",
        "description": "Callback when items move to target"
      },
      {
        "name": "onMoveAllToSource",
        "type": "() => void",
        "description": "Callback when all items move to source"
      },
      {
        "name": "onMoveAllToTarget",
        "type": "() => void",
        "description": "Callback when all items move to target"
      },
      {
        "name": "onSourceSelectionChange",
        "type": "(e: { value: any[] }) => void",
        "description": "Callback when source selection changes"
      },
      {
        "name": "onTargetSelectionChange",
        "type": "(e: { value: any[] }) => void",
        "description": "Callback when target selection changes"
      }
    ],
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
    "internal": [
      "handleChange - Processes onChange event",
      "handleMoveToSource - Processes onMoveToSource event",
      "handleMoveToTarget - Processes onMoveToTarget event"
    ],
    "patterns": [
      "Check if event handler exists before calling",
      "Extract source and target arrays from event object"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children - items defined via source/target props and itemTemplate",
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
    "basic": "<PickListWrapper source={source} target={target} itemTemplate={(item) => <div>{item.name}</div>} onChange={(e) => { setSource(e.source); setTarget(e.target); }} />",
    "withStyling": "<PickListWrapper source={available} target={selected} sourceHeader=\"Available\" targetHeader=\"Selected\" className=\"w-full\" />",
    "withEvents": "<PickListWrapper source={source} target={target} onChange={handleChange} onMoveToTarget={handleMoveToTarget} />",
    "withRedux": "<PickListWrapper source={availableItems} target={selectedItems} onChange={(e) => { dispatch(setAvailable(e.source)); dispatch(setSelected(e.target)); }} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const PickListWrapper = (props) => {
  const {
    source, target, itemTemplate, sourceHeader, targetHeader, showSourceControls, showTargetControls, dataKey, className, style, onChange, onMoveToSource, onMoveToTarget, onMoveAllToSource, onMoveAllToTarget, onSourceSelectionChange, onTargetSelectionChange, onMount, onUnmount,
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
    source,
    target,
    itemTemplate,
    sourceHeader,
    targetHeader,
    showSourceControls,
    showTargetControls,
    dataKey,
    className,
    style,
    onChange,
    onMoveToSource,
    onMoveToTarget,
    onMoveAllToSource,
    onMoveAllToTarget,
    onSourceSelectionChange,
    onTargetSelectionChange,
    ref: componentRef,
    ...restProps
  };

  return (
    <PickList {...primeReactProps} />
  );
};

PickListWrapper.displayName = 'PickListWrapper';

export default PickListWrapper;
