/**
 * TreeWrapper - Enhanced wrapper for PrimeReact Tree
 * Category: Data
 * 
 * Hierarchical tree structure
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Tree } from 'primereact/tree';

// Component metadata embedded for runtime access
export const TreeMetadata = {
  "name": "Tree",
  "import": "Tree",
  "category": "Data",
  "metadata": {
    "description": "Hierarchical tree structure",
    "usageExamples": [
      "<TreeWrapper value={nodes} />",
      "<TreeWrapper value={treeData} selectionMode=\"single\" selection={selected} onSelectionChange={(e) => setSelected(e.value)} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "TreeNode[]",
        "optional": false,
        "description": "Tree nodes",
        "helpText": "Array of tree node objects with children",
        "dataTypes": [
          "TreeNode[] - {key, label, icon, children, data}"
        ],
        "examples": [
          "[{key: '0', label: 'Root', children: [{key: '0-0', label: 'Child'}]}]"
        ]
      },
      {
        "name": "selectionMode",
        "type": "'single' | 'multiple' | 'checkbox'",
        "optional": true,
        "description": "Selection mode",
        "helpText": "How nodes can be selected",
        "dataTypes": [
          "'single'",
          "'multiple'",
          "'checkbox'"
        ],
        "examples": [
          "'single'",
          "'checkbox'"
        ]
      },
      {
        "name": "selection",
        "type": "any | any[]",
        "optional": true,
        "description": "Selected node(s)",
        "helpText": "Selected node key(s)",
        "dataTypes": [
          "string",
          "string[]",
          "object"
        ],
        "examples": [
          "'0-0'",
          "['0-0', '0-1']",
          "{key: value}"
        ]
      },
      {
        "name": "expandedKeys",
        "type": "{ [key: string]: boolean }",
        "optional": true,
        "description": "Expanded nodes",
        "helpText": "Object with node keys as properties",
        "dataTypes": [
          "object - {[key]: true}"
        ],
        "examples": [
          "{'0': true, '0-0': true}"
        ]
      },
      {
        "name": "filter",
        "type": "boolean",
        "optional": true,
        "description": "Enable filtering",
        "helpText": "Shows search input",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "filterMode",
        "type": "'lenient' | 'strict'",
        "optional": true,
        "description": "Filter mode",
        "helpText": "lenient=shows parent if child matches",
        "dataTypes": [
          "'lenient' (default)",
          "'strict'"
        ],
        "examples": [
          "'lenient'",
          "'strict'"
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
        "name": "onSelectionChange",
        "type": "(e: { value: any }) => void",
        "description": "Callback when selection changes"
      },
      {
        "name": "onExpand",
        "type": "(e: { node: TreeNode }) => void",
        "description": "Callback when node expands"
      },
      {
        "name": "onCollapse",
        "type": "(e: { node: TreeNode }) => void",
        "description": "Callback when node collapses"
      },
      {
        "name": "onToggle",
        "type": "(e: { value: { [key: string]: boolean } }) => void",
        "description": "Callback when node is toggled"
      },
      {
        "name": "onNodeClick",
        "type": "(e: { node: TreeNode }) => void",
        "description": "Callback when node is clicked"
      }
    ],
    "simplified": [
      {
        "name": "onSelectionUpdate",
        "type": "(selection: any) => void",
        "description": "Simplified selection callback"
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
      "handleSelectionChange - Processes onSelectionChange event",
      "handleExpand - Processes onExpand event",
      "handleCollapse - Processes onCollapse event",
      "handleToggle - Processes onToggle event",
      "handleNodeClick - Processes onNodeClick event"
    ],
    "patterns": [
      "Check if event handler exists before calling",
      "Extract node/value from event objects"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children - nodes defined via value prop",
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
    "basic": "<TreeWrapper value={[{key: '0', label: 'Root', children: [{key: '0-0', label: 'Child'}]}]} />",
    "withStyling": "<TreeWrapper value={nodes} filter className=\"w-full\" />",
    "withEvents": "<TreeWrapper value={treeData} selectionMode=\"single\" selection={selected} onSelectionChange={(e) => setSelected(e.value)} />",
    "withRedux": "<TreeWrapper value={nodes} selection={selectedNode} onSelectionUpdate={(val) => dispatch(setNode(val))} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const TreeWrapper = (props) => {
  const {
    value, selectionMode, selection, expandedKeys, filter, filterMode, className, style, onSelectionChange, onExpand, onCollapse, onToggle, onNodeClick, onSelectionUpdate, onMount, onUnmount,
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

  // Simplified event handler: onSelectionUpdate
  const handleSelectionChange = (e) => {
    if (onSelectionChange) {
      onSelectionChange(e);
    }
    if (onSelectionUpdate) {
      onSelectionUpdate(e.value || e.data || e);
    }
  };

  // Build props for underlying PrimeReact component
  const primeReactProps = {
    value,
    selectionMode,
    selection,
    expandedKeys,
    filter,
    filterMode,
    className,
    style,
    onSelectionChange: handleSelectionChange,
    onExpand,
    onCollapse,
    onToggle,
    onNodeClick,
    ref: componentRef,
    ...restProps
  };

  return (
    <Tree {...primeReactProps} />
  );
};

TreeWrapper.displayName = 'TreeWrapper';

export default TreeWrapper;
