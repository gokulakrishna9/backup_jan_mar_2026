/**
 * DynamicDialogWrapper - Enhanced wrapper for PrimeReact DynamicDialog
 * Category: Overlay
 * 
 * Programmatically controlled dialog service for dynamic content
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { DynamicDialog } from 'primereact/dynamicdialog';

// Component metadata embedded for runtime access
export const DynamicDialogMetadata = {
  "name": "DynamicDialog",
  "import": "DynamicDialog",
  "category": "Overlay",
  "metadata": {
    "description": "Programmatically controlled dialog service for dynamic content",
    "usageExamples": [
      "<DynamicDialogWrapper />",
      "// Used with DialogService: dialogService.open(MyComponent, { header: 'Title', data: { id: 1 } })"
    ]
  },
  "propsInterface": {
    "componentSpecific": [],
    "styling": [
      {
        "name": "className",
        "type": "string",
        "optional": true,
        "description": "Additional CSS classes for custom styling",
        "helpText": "Supports PrimeFlex utility classes and custom CSS",
        "examples": [
          "'custom-dialog'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles object",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ width: '50vw' }"
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
        "optional": true,
        "description": "Callback when component mounts"
      }
    ]
  },
  "eventHandlerMethods": {
    "internal": [],
    "patterns": [
      "Use DialogService to open dialogs programmatically",
      "Pass data to dialog components through DialogService options",
      "Close dialogs using dialogRef.close()"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component is controlled by DialogService and does not accept children directly. Content is provided through DialogService.open().",
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
    "basic": "<DynamicDialogWrapper />",
    "withStyling": "<DynamicDialogWrapper className=\"custom-dynamic-dialog\" />",
    "withEvents": "// In component: const dialogRef = dialogService.open(ProductForm, { header: 'Add Product', onHide: () => console.log('closed') })",
    "withRedux": "// dialogService.open(EditForm, { data: { id: productId }, onHide: () => dispatch(refreshProducts()) })",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const DynamicDialogWrapper = (props) => {
  const {
    className, style, onMount,
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
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <DynamicDialog {...primeReactProps} />
  );
};

DynamicDialogWrapper.displayName = 'DynamicDialogWrapper';

export default DynamicDialogWrapper;
