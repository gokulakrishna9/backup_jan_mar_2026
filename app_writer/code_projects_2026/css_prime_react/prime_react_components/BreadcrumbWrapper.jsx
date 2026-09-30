/**
 * BreadcrumbWrapper - Enhanced wrapper for PrimeReact Breadcrumb
 * Category: Menu
 * 
 * Navigation breadcrumb trail
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Breadcrumb } from 'primereact/breadcrumb';

// Component metadata embedded for runtime access
export const BreadcrumbMetadata = {
  "name": "Breadcrumb",
  "import": "Breadcrumb",
  "category": "Menu",
  "metadata": {
    "description": "Navigation breadcrumb trail",
    "usageExamples": [
      "<BreadcrumbWrapper model={items} home={{icon: 'pi pi-home', url: '/'}} />",
      "<BreadcrumbWrapper model={[{label: 'Products'}, {label: 'Electronics'}]} />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "model",
        "type": "MenuItem[]",
        "optional": false,
        "description": "Breadcrumb items",
        "helpText": "Array of menu item objects",
        "dataTypes": [
          "MenuItem[] - {label, icon, url, command}"
        ],
        "examples": [
          "[{label: 'Home'}, {label: 'Products'}]"
        ]
      },
      {
        "name": "home",
        "type": "MenuItem",
        "optional": true,
        "description": "Home item",
        "helpText": "First item in breadcrumb",
        "dataTypes": [
          "MenuItem - {icon, url, command}"
        ],
        "examples": [
          "{icon: 'pi pi-home', url: '/'}"
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
    "patterns": [
      "Menu items have their own command callbacks"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children - items defined via model prop",
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
    "basic": "<BreadcrumbWrapper model={[{label: 'Home'}, {label: 'Products'}]} />",
    "withStyling": "<BreadcrumbWrapper model={items} home={{icon: 'pi pi-home', url: '/'}} className=\"mb-3\" />",
    "withEvents": "<BreadcrumbWrapper model={[{label: 'Products', command: () => navigate('/products')}]} />",
    "withRedux": "<BreadcrumbWrapper model={breadcrumbItems} home={{icon: 'pi pi-home', command: () => dispatch(goHome())}} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const BreadcrumbWrapper = (props) => {
  const {
    model, home, className, style, onMount, onUnmount,
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
    model,
    home,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <Breadcrumb {...primeReactProps} />
  );
};

BreadcrumbWrapper.displayName = 'BreadcrumbWrapper';

export default BreadcrumbWrapper;
