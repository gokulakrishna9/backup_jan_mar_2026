/**
 * DataViewWrapper - Enhanced wrapper for PrimeReact DataView
 * Category: Data
 * 
 * Display data in grid or list layout
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { DataView } from 'primereact/dataview';

// Component metadata embedded for runtime access
export const DataViewMetadata = {
  "name": "DataView",
  "import": "DataView",
  "category": "Data",
  "metadata": {
    "description": "Display data in grid or list layout",
    "usageExamples": [
      "<DataViewWrapper value={products} itemTemplate={itemTemplate} layout=\"grid\" />",
      "<DataViewWrapper value={data} itemTemplate={template} paginator rows={9} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "any[]",
        "optional": false,
        "description": "Data array",
        "helpText": "Array of objects to display",
        "dataTypes": [
          "any[]"
        ],
        "examples": [
          "[{id: 1, name: 'Item'}]",
          "products"
        ]
      },
      {
        "name": "layout",
        "type": "'list' | 'grid'",
        "optional": true,
        "description": "Display layout",
        "helpText": "List or grid view",
        "dataTypes": [
          "'list' (default)",
          "'grid'"
        ],
        "examples": [
          "'list'",
          "'grid'"
        ]
      },
      {
        "name": "itemTemplate",
        "type": "(item: any, layout: string) => React.ReactNode",
        "optional": true,
        "description": "Item template",
        "helpText": "Function to render each item",
        "dataTypes": [
          "function"
        ],
        "examples": [
          "(item, layout) => <div>{item.name}</div>"
        ]
      },
      {
        "name": "header",
        "type": "React.ReactNode",
        "optional": true,
        "description": "Header content",
        "helpText": "Content for header section",
        "dataTypes": [
          "React.ReactNode"
        ],
        "examples": [
          "<h2>Products</h2>"
        ]
      },
      {
        "name": "footer",
        "type": "React.ReactNode",
        "optional": true,
        "description": "Footer content",
        "helpText": "Content for footer section",
        "dataTypes": [
          "React.ReactNode"
        ],
        "examples": [
          "<div>Total: {products.length}</div>"
        ]
      },
      {
        "name": "paginator",
        "type": "boolean",
        "optional": true,
        "description": "Enable pagination",
        "helpText": "Shows pagination controls",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "rows",
        "type": "number",
        "optional": true,
        "description": "Rows per page",
        "helpText": "Number of items per page",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "9",
          "12",
          "20"
        ]
      },
      {
        "name": "first",
        "type": "number",
        "optional": true,
        "description": "First item index",
        "helpText": "Index of first item (for controlled pagination)",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "0",
          "9",
          "18"
        ]
      },
      {
        "name": "sortField",
        "type": "string",
        "optional": true,
        "description": "Sort field",
        "helpText": "Field name to sort by",
        "dataTypes": [
          "string (field name)"
        ],
        "examples": [
          "'name'",
          "'price'",
          "'date'"
        ]
      },
      {
        "name": "sortOrder",
        "type": "1 | -1",
        "optional": true,
        "description": "Sort order",
        "helpText": "1=ascending, -1=descending",
        "dataTypes": [
          "1",
          "-1"
        ],
        "examples": [
          "1",
          "-1"
        ]
      },
      {
        "name": "emptyMessage",
        "type": "string",
        "optional": true,
        "description": "Empty message",
        "helpText": "Text shown when no data",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'No records found'",
          "'No data'"
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
        "name": "onPage",
        "type": "(e: { first: number, rows: number }) => void",
        "description": "Callback when page changes"
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
      "handlePage - Processes onPage event"
    ],
    "patterns": [
      "Check if event handler exists before calling"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children - items defined via value prop and itemTemplate",
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
    "basic": "<DataViewWrapper value={products} itemTemplate={(item) => <div>{item.name}</div>} layout=\"grid\" />",
    "withStyling": "<DataViewWrapper value={data} itemTemplate={template} layout=\"list\" paginator rows={9} className=\"mb-3\" />",
    "withEvents": "<DataViewWrapper value={items} itemTemplate={template} paginator rows={12} onPage={handlePage} />",
    "withRedux": "<DataViewWrapper value={productList} itemTemplate={template} first={pageFirst} rows={pageRows} onPage={(e) => dispatch(setPage(e))} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const DataViewWrapper = (props) => {
  const {
    value, layout, itemTemplate, header, footer, paginator, rows, first, sortField, sortOrder, emptyMessage, className, style, onPage, onMount, onUnmount,
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
    layout,
    itemTemplate,
    header,
    footer,
    paginator,
    rows,
    first,
    sortField,
    sortOrder,
    emptyMessage,
    className,
    style,
    onPage,
    ref: componentRef,
    ...restProps
  };

  return (
    <DataView {...primeReactProps} />
  );
};

DataViewWrapper.displayName = 'DataViewWrapper';

export default DataViewWrapper;
