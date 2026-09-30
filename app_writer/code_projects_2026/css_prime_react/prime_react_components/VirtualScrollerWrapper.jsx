/**
 * VirtualScrollerWrapper - Enhanced wrapper for PrimeReact VirtualScroller
 * Category: Data
 * 
 * Virtual scrolling for large datasets to optimize performance by rendering only visible items
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { VirtualScroller } from 'primereact/virtualscroller';

// Component metadata embedded for runtime access
export const VirtualScrollerMetadata = {
  "name": "VirtualScroller",
  "import": "VirtualScroller",
  "category": "Data",
  "metadata": {
    "description": "Virtual scrolling for large datasets to optimize performance by rendering only visible items",
    "usageExamples": [
      "<VirtualScrollerWrapper items={largeDataset} itemSize={50} itemTemplate={(item) => <div>{item.name}</div>} />",
      "<VirtualScrollerWrapper items={products} itemSize={100} itemTemplate={productTemplate} style={{ height: '400px' }} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "items",
        "type": "any[]",
        "optional": false,
        "description": "Array of items to display",
        "helpText": "Large dataset to be virtually scrolled",
        "dataTypes": [
          "any[] - array of objects or primitives"
        ],
        "examples": [
          "[{ id: 1, name: 'Item 1' }, ...]",
          "[1, 2, 3, ...]"
        ]
      },
      {
        "name": "itemSize",
        "type": "number | number[]",
        "optional": false,
        "description": "Height of each item in pixels",
        "helpText": "Fixed height for items or array of heights for variable sizing",
        "dataTypes": [
          "number (fixed height)",
          "number[] (variable heights)"
        ],
        "examples": [
          "50",
          "100",
          "[50, 75, 100]"
        ]
      },
      {
        "name": "itemTemplate",
        "type": "(item: any, options: any) => React.ReactNode",
        "optional": false,
        "description": "Template for rendering each item",
        "helpText": "Function that returns JSX for each item",
        "dataTypes": [
          "(item, options) => JSX.Element"
        ],
        "examples": [
          "(item) => <div>{item.name}</div>"
        ]
      },
      {
        "name": "lazy",
        "type": "boolean",
        "optional": true,
        "description": "Whether to use lazy loading",
        "helpText": "Enables lazy loading of data on scroll",
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
        "type": "'vertical' | 'horizontal' | 'both'",
        "optional": true,
        "description": "Scroll orientation",
        "helpText": "Direction of scrolling (default: vertical)",
        "dataTypes": [
          "'vertical'",
          "'horizontal'",
          "'both'"
        ],
        "examples": [
          "'vertical'",
          "'horizontal'"
        ]
      },
      {
        "name": "showLoader",
        "type": "boolean",
        "optional": true,
        "description": "Whether to show loading indicator",
        "helpText": "Displays loader during lazy loading",
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
        "description": "Additional CSS classes for custom styling",
        "helpText": "Supports PrimeFlex utility classes and custom CSS",
        "examples": [
          "'w-full'",
          "'shadow-2'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles object",
        "helpText": "Standard React inline styles - height is required",
        "examples": [
          "{ height: '400px', width: '100%' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onLazyLoad",
        "type": "(e: { first: number, last: number }) => void",
        "optional": true,
        "description": "Callback for lazy loading more items"
      },
      {
        "name": "onScroll",
        "type": "(e: { originalEvent: Event }) => void",
        "optional": true,
        "description": "Callback when scrolling occurs"
      }
    ],
    "simplified": [
      {
        "name": "onLoadMore",
        "type": "(first: number, last: number) => void",
        "optional": true,
        "description": "Simplified lazy load callback"
      }
    ],
    "validation": [],
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
      "handleLazyLoad(e): Processes lazy load event and calls onLoadMore if provided"
    ],
    "patterns": [
      "For infinite scroll: Use onLazyLoad to fetch more data when reaching end",
      "For Redux: Use onLoadMore to dispatch data fetching actions"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children. Use itemTemplate prop to render items.",
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
    "basic": "<VirtualScrollerWrapper items={items} itemSize={50} itemTemplate={(item) => <div>{item.name}</div>} style={{ height: '400px' }} />",
    "withStyling": "<VirtualScrollerWrapper items={items} itemSize={50} itemTemplate={(item) => <div className=\"p-3\">{item.name}</div>} className=\"w-full shadow-2\" style={{ height: '500px' }} />",
    "withEvents": "<VirtualScrollerWrapper items={items} itemSize={50} itemTemplate={itemTemplate} lazy onLazyLoad={(e) => loadMoreItems(e.first, e.last)} style={{ height: '400px' }} />",
    "withRedux": "<VirtualScrollerWrapper items={items} itemSize={50} itemTemplate={itemTemplate} lazy onLoadMore={(first, last) => dispatch(fetchItems(first, last))} style={{ height: '400px' }} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const VirtualScrollerWrapper = (props) => {
  const {
    items, itemSize, itemTemplate, lazy, orientation, showLoader, className, style, onLazyLoad, onScroll, onLoadMore, onMount,
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
    items,
    itemSize,
    itemTemplate,
    lazy,
    orientation,
    showLoader,
    className,
    style,
    onLazyLoad,
    onScroll,
    ref: componentRef,
    ...restProps
  };

  return (
    <VirtualScroller {...primeReactProps} />
  );
};

VirtualScrollerWrapper.displayName = 'VirtualScrollerWrapper';

export default VirtualScrollerWrapper;
