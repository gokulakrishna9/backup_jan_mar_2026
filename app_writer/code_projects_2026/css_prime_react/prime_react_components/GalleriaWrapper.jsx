/**
 * GalleriaWrapper - Enhanced wrapper for PrimeReact Galleria
 * Category: Media
 * 
 * Advanced image gallery with thumbnails
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Galleria } from 'primereact/galleria';

// Component metadata embedded for runtime access
export const GalleriaMetadata = {
  "name": "Galleria",
  "import": "Galleria",
  "category": "Media",
  "metadata": {
    "description": "Advanced image gallery with thumbnails",
    "usageExamples": [
      "<GalleriaWrapper value={images} item={itemTemplate} thumbnail={thumbnailTemplate} />",
      "<GalleriaWrapper value={photos} numVisible={5} circular fullScreen />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "value",
        "type": "any[]",
        "optional": false,
        "description": "Images array",
        "helpText": "Array of image objects",
        "dataTypes": [
          "any[]"
        ],
        "examples": [
          "[{itemImageSrc: 'img1.jpg', thumbnailImageSrc: 'thumb1.jpg'}]"
        ]
      },
      {
        "name": "item",
        "type": "(item: any) => React.ReactNode",
        "optional": true,
        "description": "Item template",
        "helpText": "Function to render main image",
        "dataTypes": [
          "function"
        ],
        "examples": [
          "(item) => <img src={item.itemImageSrc} />"
        ]
      },
      {
        "name": "thumbnail",
        "type": "(item: any) => React.ReactNode",
        "optional": true,
        "description": "Thumbnail template",
        "helpText": "Function to render thumbnail",
        "dataTypes": [
          "function"
        ],
        "examples": [
          "(item) => <img src={item.thumbnailImageSrc} />"
        ]
      },
      {
        "name": "activeIndex",
        "type": "number",
        "optional": true,
        "description": "Active image index",
        "helpText": "Currently displayed image (controlled)",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "0",
          "1",
          "2"
        ]
      },
      {
        "name": "numVisible",
        "type": "number",
        "optional": true,
        "description": "Visible thumbnails",
        "helpText": "Number of thumbnails visible (default: 3)",
        "dataTypes": [
          "number"
        ],
        "examples": [
          "3",
          "5",
          "7"
        ]
      },
      {
        "name": "circular",
        "type": "boolean",
        "optional": true,
        "description": "Circular mode",
        "helpText": "Infinite loop",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "autoPlay",
        "type": "boolean",
        "optional": true,
        "description": "Auto play",
        "helpText": "Automatically cycles through images",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "transitionInterval",
        "type": "number",
        "optional": true,
        "description": "Transition interval",
        "helpText": "Milliseconds between auto-play transitions (default: 4000)",
        "dataTypes": [
          "number (milliseconds)"
        ],
        "examples": [
          "3000",
          "5000"
        ]
      },
      {
        "name": "fullScreen",
        "type": "boolean",
        "optional": true,
        "description": "Full screen mode",
        "helpText": "Opens in full screen overlay",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "visible",
        "type": "boolean",
        "optional": true,
        "description": "Visibility (fullScreen mode)",
        "helpText": "Controls visibility when fullScreen=true",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "showThumbnails",
        "type": "boolean",
        "optional": true,
        "description": "Show thumbnails",
        "helpText": "Displays thumbnail strip (default: true)",
        "dataTypes": [
          "boolean"
        ],
        "examples": [
          "true",
          "false"
        ]
      },
      {
        "name": "showIndicators",
        "type": "boolean",
        "optional": true,
        "description": "Show indicators",
        "helpText": "Displays position indicators",
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
          "'custom-galleria'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ maxWidth: '640px' }"
        ]
      }
    ],
    "children": null
  },
  "eventHandlers": {
    "standard": [
      {
        "name": "onItemChange",
        "type": "(e: { index: number }) => void",
        "description": "Callback when active item changes"
      },
      {
        "name": "onHide",
        "type": "() => void",
        "description": "Callback when fullScreen gallery is hidden"
      }
    ],
    "simplified": [
      {
        "name": "onActiveIndexChange",
        "type": "(index: number) => void",
        "description": "Simplified callback with just the index"
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
      "handleItemChange - Processes onItemChange event",
      "handleHide - Processes onHide event"
    ],
    "patterns": [
      "Check if event handler exists before calling"
    ]
  },
  "childComponentInfo": {
    "allowedChildren": [],
    "childrenDescription": "This component does not accept children - images defined via value prop and templates",
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
    "basic": "<GalleriaWrapper value={images} item={(item) => <img src={item.itemImageSrc} />} thumbnail={(item) => <img src={item.thumbnailImageSrc} />} />",
    "withStyling": "<GalleriaWrapper value={photos} numVisible={5} circular className=\"custom-galleria\" style={{ maxWidth: '640px' }} />",
    "withEvents": "<GalleriaWrapper value={images} activeIndex={activeIndex} onItemChange={(e) => setActiveIndex(e.index)} />",
    "withRedux": "<GalleriaWrapper value={galleryImages} activeIndex={currentIndex} onActiveIndexChange={(idx) => dispatch(setIndex(idx))} />",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const GalleriaWrapper = (props) => {
  const {
    value, item, thumbnail, activeIndex, numVisible, circular, autoPlay, transitionInterval, fullScreen, visible, showThumbnails, showIndicators, className, style, onItemChange, onHide, onActiveIndexChange, onMount, onUnmount,
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
    item,
    thumbnail,
    activeIndex,
    numVisible,
    circular,
    autoPlay,
    transitionInterval,
    fullScreen,
    visible,
    showThumbnails,
    showIndicators,
    className,
    style,
    onItemChange,
    onHide,
    ref: componentRef,
    ...restProps
  };

  return (
    <Galleria {...primeReactProps} />
  );
};

GalleriaWrapper.displayName = 'GalleriaWrapper';

export default GalleriaWrapper;
