/**
 * ColumnWrapper - Enhanced wrapper for PrimeReact Column
 * Category: Data
 * 
 * Column definition component for DataTable and TreeTable with sorting, filtering, and custom rendering
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Column } from 'primereact/column';

// Component metadata embedded for runtime access
export const ColumnMetadata = {
  "name": "Column",
  "import": "Column",
  "category": "Data",
  "metadata": {
    "description": "Column definition component for DataTable and TreeTable with sorting, filtering, and custom rendering",
    "usageExamples": [
      "<Column field=\"name\" header=\"Name\" sortable />",
      "<Column field=\"price\" header=\"Price\" body={(rowData) => `$${rowData.price}`} sortable filter />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "field",
        "type": "string",
        "optional": true,
        "description": "Property name of the data field",
        "helpText": "Field name to display from row data object",
        "dataTypes": [
          "string (property name)"
        ],
        "examples": [
          "'name'",
          "'email'",
          "'price'"
        ]
      },
      {
        "name": "header",
        "type": "string | React.ReactNode",
        "optional": true,
        "description": "Header text or element",
        "helpText": "Column header content",
        "dataTypes": [
          "string",
          "React.ReactNode"
        ],
        "examples": [
          "'Name'",
          "'Email Address'",
          "<div>Custom Header</div>"
        ]
      },
      {
        "name": "body",
        "type": "(rowData: any, options: any) => React.ReactNode",
        "optional": true,
        "description": "Custom body template",
        "helpText": "Function to customize cell rendering",
        "dataTypes": [
          "(rowData, options) => JSX.Element"
        ],
        "examples": [
          "(data) => <span>{data.name}</span>"
        ]
      },
      {
        "name": "sortable",
        "type": "boolean",
        "optional": true,
        "description": "Whether column is sortable",
        "helpText": "Enables sorting for this column",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "filter",
        "type": "boolean",
        "optional": true,
        "description": "Whether column is filterable",
        "helpText": "Enables filtering for this column",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "filterPlaceholder",
        "type": "string",
        "optional": true,
        "description": "Placeholder for filter input",
        "helpText": "Placeholder text for filter field",
        "dataTypes": [
          "string"
        ],
        "examples": [
          "'Search by name'",
          "'Filter'"
        ]
      },
      {
        "name": "filterMatchMode",
        "type": "string",
        "optional": true,
        "description": "Filter match mode",
        "helpText": "How to match filter values (contains, startsWith, endsWith, equals, etc.)",
        "dataTypes": [
          "'contains'",
          "'startsWith'",
          "'endsWith'",
          "'equals'",
          "'notEquals'",
          "'in'"
        ],
        "examples": [
          "'contains'",
          "'startsWith'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles for column cells",
        "helpText": "CSS styles applied to column cells",
        "dataTypes": [
          "React.CSSProperties"
        ],
        "examples": [
          "{ width: '200px' }",
          "{ textAlign: 'center' }"
        ]
      },
      {
        "name": "headerStyle",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles for column header",
        "helpText": "CSS styles applied to column header",
        "dataTypes": [
          "React.CSSProperties"
        ],
        "examples": [
          "{ width: '200px' }"
        ]
      },
      {
        "name": "bodyStyle",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles for column body cells",
        "helpText": "CSS styles applied to body cells",
        "dataTypes": [
          "React.CSSProperties"
        ],
        "examples": [
          "{ textAlign: 'right' }"
        ]
      },
      {
        "name": "frozen",
        "type": "boolean",
        "optional": true,
        "description": "Whether column is frozen",
        "helpText": "Freezes column during horizontal scroll",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "alignFrozen",
        "type": "'left' | 'right'",
        "optional": true,
        "description": "Alignment of frozen column",
        "helpText": "Which side to freeze the column",
        "dataTypes": [
          "'left'",
          "'right'"
        ],
        "examples": [
          "'left'",
          "'right'"
        ]
      }
    ],
    "styling": [
      {
        "name": "className",
        "type": "string",
        "optional": true,
        "description": "Additional CSS classes for column cells",
        "helpText": "Supports PrimeFlex utility classes and custom CSS",
        "examples": [
          "'text-center'",
          "'font-bold'"
        ]
      },
      {
        "name": "headerClassName",
        "type": "string",
        "optional": true,
        "description": "CSS classes for column header",
        "helpText": "Classes applied to header cell",
        "examples": [
          "'text-center'",
          "'bg-primary'"
        ]
      },
      {
        "name": "bodyClassName",
        "type": "string",
        "optional": true,
        "description": "CSS classes for column body cells",
        "helpText": "Classes applied to body cells",
        "examples": [
          "'text-right'",
          "'font-bold'"
        ]
      }
    ],
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
    "patterns": []
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component is used as a child of DataTable or TreeTable and does not accept children itself.",
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
    "basic": "<Column field=\"name\" header=\"Name\" />",
    "withStyling": "<Column field=\"price\" header=\"Price\" className=\"text-right\" headerClassName=\"text-center\" style={{ width: '150px' }} />",
    "withEvents": "N/A",
    "withRedux": "N/A",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const ColumnWrapper = (props) => {
  const {
    field, header, body, sortable, filter, filterPlaceholder, filterMatchMode, style, headerStyle, bodyStyle, frozen, alignFrozen, className, headerClassName, bodyClassName,
    ...restProps
  } = props;

  const componentRef = useRef(null);

  // Build props for underlying PrimeReact component
  const primeReactProps = {
    field,
    header,
    body,
    sortable,
    filter,
    filterPlaceholder,
    filterMatchMode,
    style,
    headerStyle,
    bodyStyle,
    frozen,
    alignFrozen,
    className,
    headerClassName,
    bodyClassName,
    ref: componentRef,
    ...restProps
  };

  return (
    <Column {...primeReactProps} />
  );
};

ColumnWrapper.displayName = 'ColumnWrapper';

export default ColumnWrapper;
