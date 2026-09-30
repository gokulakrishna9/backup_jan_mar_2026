/**
 * AvatarWrapper - Enhanced wrapper for PrimeReact Avatar
 * Category: Misc
 * 
 * Displays user avatars with images, text labels, or icons. Priority: image > label > icon
 * 
 * This wrapper provides:
 * - Simplified event handlers for Redux integration
 * - Validation hooks
 * - Lifecycle callbacks
 * - Embedded component metadata for runtime introspection
 */

import React, { useEffect, useRef } from 'react';
import { Avatar } from 'primereact/avatar';

// Component metadata embedded for runtime access
export const AvatarMetadata = {
  "name": "Avatar",
  "import": "Avatar",
  "category": "Misc",
  "metadata": {
    "description": "Displays user avatars with images, text labels, or icons. Priority: image > label > icon",
    "usageExamples": [
      "<AvatarWrapper label=\"JD\" size=\"large\" shape=\"circle\" />",
      "<AvatarWrapper image=\"/avatar.jpg\" />",
      "<AvatarWrapper icon=\"pi pi-user\" />"
    ]
  },
  "propsInterface": {
    "componentSpecific": [
      {
        "name": "label",
        "type": "string",
        "optional": true,
        "description": "Text to display (typically 1-2 characters for initials)",
        "helpText": "Use for displaying user initials",
        "dataTypes": [
          "string (1-2 characters)"
        ],
        "examples": [
          "'JD'",
          "'AB'",
          "'XY'"
        ]
      },
      {
        "name": "icon",
        "type": "string",
        "optional": true,
        "description": "PrimeIcon class name",
        "helpText": "Use PrimeIcons for generic avatars",
        "dataTypes": [
          "string (PrimeIcon class)"
        ],
        "examples": [
          "'pi pi-user'",
          "'pi pi-users'"
        ]
      },
      {
        "name": "image",
        "type": "string",
        "optional": true,
        "description": "Image URL or path",
        "helpText": "URL or path to avatar image. Takes priority over label and icon",
        "dataTypes": [
          "string (URL or file path)"
        ],
        "examples": [
          "'/avatar.jpg'",
          "'https://example.com/user.png'"
        ]
      },
      {
        "name": "size",
        "type": "'normal' | 'large' | 'xlarge'",
        "optional": true,
        "description": "Avatar size",
        "helpText": "Controls avatar dimensions",
        "dataTypes": [
          "'normal' (default)",
          "'large'",
          "'xlarge'"
        ],
        "examples": [
          "'large'",
          "'xlarge'"
        ]
      },
      {
        "name": "shape",
        "type": "'square' | 'circle'",
        "optional": true,
        "description": "Avatar shape",
        "helpText": "Square or circular avatar",
        "dataTypes": [
          "'square'",
          "'circle' (default)"
        ],
        "examples": [
          "'circle'",
          "'square'"
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
          "'mr-2'"
        ]
      },
      {
        "name": "style",
        "type": "React.CSSProperties",
        "optional": true,
        "description": "Inline styles",
        "helpText": "Standard React inline styles",
        "examples": [
          "{ border: '2px solid #ccc' }"
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
    "childrenDescription": "This component does not accept children",
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
    "basic": "<AvatarWrapper label=\"JD\" />",
    "withStyling": "<AvatarWrapper label=\"JD\" className=\"mr-2\" shape=\"circle\" />",
    "withEvents": "N/A",
    "withRedux": "N/A",
    "withValidation": "N/A",
    "withChildren": "N/A"
  }
};

const AvatarWrapper = (props) => {
  const {
    label, icon, image, size, shape, className, style,
    ...restProps
  } = props;

  const componentRef = useRef(null);

  // Build props for underlying PrimeReact component
  const primeReactProps = {
    label,
    icon,
    image,
    size,
    shape,
    className,
    style,
    ref: componentRef,
    ...restProps
  };

  return (
    <Avatar {...primeReactProps} />
  );
};

AvatarWrapper.displayName = 'AvatarWrapper';

export default AvatarWrapper;
