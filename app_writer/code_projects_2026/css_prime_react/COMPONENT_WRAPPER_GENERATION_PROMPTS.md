# PrimeReact Component Wrapper Generation Prompts

This document contains prompts for generating React wrapper components for PrimeReact components. Components are organized by complexity level based on their child component acceptance.

## Organization Strategy

- **Level 1**: Components that accept NO children (self-contained)
- **Level 2**: Components that accept SIMPLE children (text, basic elements)
- **Level 3**: Components that accept COMPLEX children (specific component types, templates)

---

## EVENT HANDLING GUIDELINES FOR ALL WRAPPER COMPONENTS

**CRITICAL**: Every wrapper component MUST support comprehensive event handling for state management, Redux actions, and UI interactions.

### Required Event Handling Props

```typescript
interface BaseEventProps {
  // Component-specific events (e.g., onChange, onClick, onSelect)
  onChange?: (e: any) => void;
  onFocus?: (e: React.FocusEvent) => void;
  onBlur?: (e: React.FocusEvent) => void;
  
  // Custom event handlers for Redux/state management
  onValueChange?: (value: any) => void;  // Simplified value-only callback
  onStateChange?: (state: any) => void;  // For complex state updates
  
  // Lifecycle events
  onMount?: () => void;
  onUnmount?: () => void;
  
  // Validation events
  onValidate?: (value: any) => boolean | string;
  onError?: (error: string) => void;
}
```

### Event Handling Patterns

#### 1. Standard Event Handlers
Pass through native PrimeReact events:

```typescript
interface ButtonWrapperProps {
  onClick?: (e: React.MouseEvent) => void;
  onMouseEnter?: (e: React.MouseEvent) => void;
  onMouseLeave?: (e: React.MouseEvent) => void;
  onFocus?: (e: React.FocusEvent) => void;
  onBlur?: (e: React.FocusEvent) => void;
}

// Usage
<ButtonWrapper 
  onClick={(e) => console.log('Clicked', e)}
  onMouseEnter={() => setHovered(true)}
/>
```

#### 2. Redux Integration Pattern
Support Redux actions through event handlers:

```typescript
import { useDispatch } from 'react-redux';
import { updateUser, saveData } from './actions';

const MyComponent = () => {
  const dispatch = useDispatch();
  
  return (
    <InputTextWrapper
      value={username}
      onChange={(e) => dispatch(updateUser(e.target.value))}
      onBlur={() => dispatch(saveData())}
    />
  );
};
```

#### 3. Simplified Value Callbacks
Provide value-only callbacks for cleaner Redux integration:

```typescript
interface InputWrapperProps {
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onValueChange?: (value: string) => void;  // Simplified callback
}

const InputWrapper = ({ onChange, onValueChange, ...props }) => {
  const handleChange = (e) => {
    onChange?.(e);  // Call original handler
    onValueChange?.(e.target.value);  // Call simplified handler
  };
  
  return <InputText onChange={handleChange} {...props} />;
};

// Usage with Redux
<InputWrapper 
  value={name}
  onValueChange={(value) => dispatch(setName(value))}
/>
```

#### 4. Redux Selector Integration
Components can be triggered by Redux state changes:

```typescript
import { useSelector, useDispatch } from 'react-redux';

const MyComponent = () => {
  const isVisible = useSelector(state => state.ui.dialogVisible);
  const dispatch = useDispatch();
  
  return (
    <DialogWrapper
      visible={isVisible}
      onHide={() => dispatch(hideDialog())}
      onShow={() => dispatch(logDialogOpen())}
    />
  );
};
```

#### 5. Event Chaining Pattern
Support multiple event handlers:

```typescript
interface WrapperProps {
  onChange?: (e: any) => void;
  onChangeCapture?: (e: any) => void;  // Capture phase
  beforeChange?: (value: any) => boolean;  // Validation/prevention
  afterChange?: (value: any) => void;  // Side effects
}

const handleChange = (e) => {
  const newValue = e.target.value;
  
  // Before change hook (can prevent change)
  if (beforeChange && !beforeChange(newValue)) {
    return;
  }
  
  // Main change handler
  onChange?.(e);
  
  // After change hook (side effects)
  afterChange?.(newValue);
};
```

#### 6. Validation Events
Support validation with error handling:

```typescript
interface ValidatedInputProps {
  value?: string;
  onChange?: (e: any) => void;
  onValidate?: (value: string) => boolean | string;
  onError?: (error: string) => void;
  onValid?: () => void;
}

const handleChange = (e) => {
  const value = e.target.value;
  onChange?.(e);
  
  if (onValidate) {
    const result = onValidate(value);
    if (result === true) {
      onValid?.();
    } else if (typeof result === 'string') {
      onError?.(result);
    }
  }
};

// Usage
<InputWrapper
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  onValidate={(value) => {
    if (!value.includes('@')) return 'Invalid email';
    return true;
  }}
  onError={(error) => dispatch(setError(error))}
  onValid={() => dispatch(clearError())}
/>
```

### Event Handler Examples by Use Case

#### Form Submission with Redux
```typescript
<FormWrapper onSubmit={(data) => dispatch(submitForm(data))}>
  <InputTextWrapper 
    value={name}
    onValueChange={(value) => dispatch(updateField('name', value))}
  />
  <ButtonWrapper 
    type="submit"
    onClick={() => dispatch(validateForm())}
  />
</FormWrapper>
```

#### Real-time Search with Debouncing
```typescript
const [searchTerm, setSearchTerm] = useState('');
const dispatch = useDispatch();

const debouncedSearch = useMemo(
  () => debounce((value) => dispatch(searchProducts(value)), 300),
  [dispatch]
);

<InputTextWrapper
  value={searchTerm}
  onChange={(e) => setSearchTerm(e.target.value)}
  onValueChange={debouncedSearch}
/>
```

#### Conditional Actions Based on State
```typescript
const status = useSelector(state => state.user.status);

<ButtonWrapper
  onClick={() => {
    if (status === 'active') {
      dispatch(deactivateUser());
    } else {
      dispatch(activateUser());
    }
  }}
  label={status === 'active' ? 'Deactivate' : 'Activate'}
/>
```

#### Multi-step Form Navigation
```typescript
const currentStep = useSelector(state => state.form.currentStep);

<StepperWrapper activeStep={currentStep}>
  <StepperPanel 
    header="Step 1"
    onNext={() => dispatch(nextStep())}
  />
  <StepperPanel 
    header="Step 2"
    onNext={() => dispatch(nextStep())}
    onPrevious={() => dispatch(previousStep())}
  />
</StepperWrapper>
```

### Event Handling Best Practices

1. **Always Optional**: Make all event handlers optional with `?` operator
2. **Type Safety**: Use proper TypeScript types for event parameters
3. **Null Checks**: Always check if handler exists before calling: `onChange?.(e)`
4. **Event Bubbling**: Support both capture and bubble phase when needed
5. **Prevent Default**: Allow users to call `e.preventDefault()` when needed
6. **Redux Actions**: Support both direct Redux dispatch and callback patterns
7. **Error Boundaries**: Wrap event handlers in try-catch for production safety
8. **Performance**: Use `useCallback` for event handlers to prevent re-renders
9. **Cleanup**: Remove event listeners in cleanup functions
10. **Documentation**: Document all event parameters and return values

### Common Event Handler Props by Component Type

**Form Components:**
- `onChange`, `onValueChange`, `onBlur`, `onFocus`, `onValidate`, `onError`

**Button Components:**
- `onClick`, `onMouseEnter`, `onMouseLeave`, `onFocus`, `onBlur`

**Data Components:**
- `onSelectionChange`, `onRowSelect`, `onRowUnselect`, `onSort`, `onFilter`, `onPage`

**Dialog/Overlay Components:**
- `onShow`, `onHide`, `onMaximize`, `onMinimize`

**Menu Components:**
- `onSelect`, `onToggle`, `onShow`, `onHide`

---

## STYLING GUIDELINES FOR ALL WRAPPER COMPONENTS

**CRITICAL**: Every wrapper component MUST include the following styling props:

### Required Styling Props

```typescript
interface BaseWrapperProps {
  className?: string;           // Additional CSS classes for custom styling
  style?: React.CSSProperties;  // Inline styles object
}
```

### Styling Implementation Pattern

All wrapper components should:

1. **Accept Both Props**: Include both `className` and `style` in the props interface
2. **Pass Through**: Forward these props directly to the underlying PrimeReact component
3. **Merge Classes**: If wrapper adds default classes, merge with user-provided className
4. **Merge Styles**: If wrapper adds default styles, merge with user-provided style object

### Example Implementation

```typescript
interface BadgeWrapperProps {
  value?: string | number;
  severity?: 'success' | 'info' | 'warning' | 'danger' | null;
  className?: string;  // ✓ Always include
  style?: React.CSSProperties;  // ✓ Always include
}

const BadgeWrapper: React.FC<BadgeWrapperProps> = ({
  value,
  severity,
  className,
  style,
  ...rest
}) => {
  return (
    <Badge
      value={value}
      severity={severity}
      className={className}  // ✓ Pass through
      style={style}          // ✓ Pass through
      {...rest}
    />
  );
};
```

### Usage Examples with Styling

```jsx
// Using className with PrimeFlex utilities
<BadgeWrapper 
  value={5} 
  severity="danger"
  className="ml-2 shadow-2"
/>

// Using inline styles
<BadgeWrapper 
  value="NEW"
  severity="success"
  style={{ marginLeft: '1rem', fontSize: '0.875rem' }}
/>

// Combining both
<BadgeWrapper 
  value={10}
  className="border-round-lg"
  style={{ backgroundColor: '#custom-color' }}
/>

// With PrimeFlex responsive utilities
<CardWrapper 
  title="Product"
  className="col-12 md:col-6 lg:col-4 p-3"
  style={{ minHeight: '300px' }}
>
  Content
</CardWrapper>
```

### Styling Best Practices

1. **PrimeFlex Integration**: Wrappers should work seamlessly with PrimeFlex utility classes
2. **Responsive Design**: Support responsive className patterns (e.g., `col-12 md:col-6`)
3. **Theme Compatibility**: Don't override theme colors unless explicitly styled
4. **CSS Specificity**: User-provided styles should have higher specificity than defaults
5. **Style Merging**: When wrapper has default styles, use spread operator to merge:
   ```typescript
   style={{ ...defaultStyles, ...style }}
   ```

### Special Cases

Some components have additional style props for nested elements:

```typescript
// DataTable with multiple style props
interface DataTableWrapperProps {
  className?: string;           // Table container class
  style?: React.CSSProperties;  // Table container style
  tableStyle?: React.CSSProperties;  // Inner table element style
  // ... other props
}

// Dialog with content style
interface DialogWrapperProps {
  className?: string;           // Dialog container class
  style?: React.CSSProperties;  // Dialog container style
  contentStyle?: React.CSSProperties;  // Dialog content area style
  // ... other props
}
```

---

## LEVEL 1: NO CHILDREN COMPONENTS

These components are self-contained and do not accept child components.

### 1.1 Badge Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Badge with the following specifications:

Component Name: BadgeWrapper
Import: import { Badge } from 'primereact/badge';

Props Interface:
- value: string | number (optional) - Badge value to display
- severity: 'success' | 'info' | 'warning' | 'danger' | null (optional) - Severity type
- size: 'normal' | 'large' | 'xlarge' (optional) - Size of badge
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Can be numeric (count) or string (status text)
- severity: Predefined color schemes (success=green, info=blue, warning=orange, danger=red)

Child Components: NONE - This is a self-contained component

Usage Example:
<BadgeWrapper value={5} severity="danger" />
<BadgeWrapper value="NEW" severity="success" size="large" />
```

### 1.2 Avatar Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Avatar with the following specifications:

Component Name: AvatarWrapper
Import: import { Avatar } from 'primereact/avatar';

Props Interface:
- label: string (optional) - Text to display (initials)
- icon: string (optional) - PrimeIcon class name
- image: string (optional) - Image URL
- size: 'normal' | 'large' | 'xlarge' (optional) - Avatar size
- shape: 'square' | 'circle' (optional) - Avatar shape
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- label: String (typically 1-2 characters for initials)
- icon: String (PrimeIcon class like 'pi pi-user')
- image: String (URL or path to image)

Priority: image > label > icon (if multiple provided, image takes precedence)

Child Components: NONE

Usage Example:
<AvatarWrapper label="JD" size="large" shape="circle" />
<AvatarWrapper image="/avatar.jpg" />
<AvatarWrapper icon="pi pi-user" />
```

### 1.3 Chip Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Chip with the following specifications:

Component Name: ChipWrapper
Import: import { Chip } from 'primereact/chip';

Props Interface:
- label: string (optional) - Text to display
- icon: string (optional) - PrimeIcon class name
- image: string (optional) - Image URL
- removable: boolean (optional) - Show remove icon
- onRemove: (e: React.MouseEvent) => void (optional) - Remove callback
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- label: String (tag text, category name)
- icon: String (PrimeIcon class)
- image: String (URL for avatar-style chips)

Child Components: NONE

Usage Example:
<ChipWrapper label="Technology" />
<ChipWrapper label="React" icon="pi pi-check" removable onRemove={handleRemove} />
<ChipWrapper label="John Doe" image="/user.jpg" />
```

### 1.4 ProgressSpinner Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact ProgressSpinner with the following specifications:

Component Name: ProgressSpinnerWrapper
Import: import { ProgressSpinner } from 'primereact/progressspinner';

Props Interface:
- strokeWidth: string (optional) - Width of the circle stroke (default: '2')
- fill: string (optional) - Fill color of the background
- animationDuration: string (optional) - Duration of the rotate animation (default: '2s')
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- strokeWidth: String (pixel value like '2', '4')
- fill: String (color value, 'transparent' for no fill)
- animationDuration: String (CSS duration like '2s', '1.5s')

Child Components: NONE

Usage Example:
<ProgressSpinnerWrapper />
<ProgressSpinnerWrapper strokeWidth="4" animationDuration="1s" />
```

### 1.5 Skeleton Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Skeleton with the following specifications:

Component Name: SkeletonWrapper
Import: import { Skeleton } from 'primereact/skeleton';

Props Interface:
- shape: 'rectangle' | 'circle' (optional) - Shape of skeleton (default: 'rectangle')
- size: string (optional) - Size for circle shape (e.g., '4rem')
- width: string (optional) - Width of skeleton (e.g., '100%', '10rem')
- height: string (optional) - Height of skeleton (e.g., '2rem')
- borderRadius: string (optional) - Border radius
- animation: 'wave' | 'none' (optional) - Animation type (default: 'wave')
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- shape: Enum ('rectangle' | 'circle')
- size: String (CSS size value for circle)
- width/height: String (CSS size values)
- animation: Enum ('wave' | 'none')

Child Components: NONE

Usage Example:
<SkeletonWrapper width="100%" height="2rem" />
<SkeletonWrapper shape="circle" size="4rem" />
<SkeletonWrapper width="10rem" height="4rem" borderRadius="16px" />
```

### 1.6 Tag Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Tag with the following specifications:

Component Name: TagWrapper
Import: import { Tag } from 'primereact/tag';

Props Interface:
- value: string | number (optional) - Tag value to display
- severity: 'success' | 'info' | 'warning' | 'danger' | null (optional) - Severity type
- rounded: boolean (optional) - Rounded corners
- icon: string (optional) - PrimeIcon class name
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: String or number (status text, category)
- severity: Predefined color schemes
- icon: String (PrimeIcon class)

Child Components: NONE

Usage Example:
<TagWrapper value="Active" severity="success" />
<TagWrapper value="Pending" severity="warning" icon="pi pi-clock" />
<TagWrapper value="Premium" rounded />
```

### 1.7 Divider Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Divider with the following specifications:

Component Name: DividerWrapper
Import: import { Divider } from 'primereact/divider';

Props Interface:
- align: 'left' | 'center' | 'right' | 'top' | 'bottom' (optional) - Alignment of content
- layout: 'horizontal' | 'vertical' (optional) - Orientation (default: 'horizontal')
- type: 'solid' | 'dashed' | 'dotted' (optional) - Border style (default: 'solid')
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (optional) - Content to display in divider

Data Types:
- align: Enum (position of content within divider)
- layout: Enum (horizontal or vertical line)
- type: Enum (line style)

Child Components: Simple text or inline elements only

Usage Example:
<DividerWrapper />
<DividerWrapper align="center">OR</DividerWrapper>
<DividerWrapper layout="vertical" />
<DividerWrapper type="dashed" align="left">Section</DividerWrapper>
```

### 1.8 Image Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Image with the following specifications:

Component Name: ImageWrapper
Import: import { Image } from 'primereact/image';

Props Interface:
- src: string (required) - Image source URL
- alt: string (optional) - Alternative text
- width: string (optional) - Image width
- height: string (optional) - Image height
- preview: boolean (optional) - Enable image preview/zoom
- imageClassName: string (optional) - CSS class for img element
- imageStyle: React.CSSProperties (optional) - Inline styles for img
- className: string (optional) - CSS class for container
- style: React.CSSProperties (optional) - Inline styles for container

Data Types:
- src: String (URL or path)
- alt: String (accessibility text)
- width/height: String (CSS size values)
- preview: Boolean (enables lightbox functionality)

Child Components: NONE

Usage Example:
<ImageWrapper src="/product.jpg" alt="Product" width="250" />
<ImageWrapper src="/gallery.jpg" preview />
```

### 1.9 ProgressBar Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact ProgressBar with the following specifications:

Component Name: ProgressBarWrapper
Import: import { ProgressBar } from 'primereact/progressbar';

Props Interface:
- value: number (optional) - Progress value (0-100)
- showValue: boolean (optional) - Display percentage text (default: true)
- mode: 'determinate' | 'indeterminate' (optional) - Progress mode (default: 'determinate')
- color: string (optional) - Custom color
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Number (0-100 for determinate mode)
- mode: Enum ('determinate' for known progress, 'indeterminate' for loading)
- color: String (CSS color value)

Child Components: NONE

Usage Example:
<ProgressBarWrapper value={75} />
<ProgressBarWrapper mode="indeterminate" />
<ProgressBarWrapper value={50} showValue={false} color="#4CAF50" />
```

### 1.10 ScrollTop Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact ScrollTop with the following specifications:

Component Name: ScrollTopWrapper
Import: import { ScrollTop } from 'primereact/scrolltop';

Props Interface:
- target: 'window' | 'parent' (optional) - Target element to scroll (default: 'window')
- threshold: number (optional) - Scroll position to show button (default: 400)
- icon: string (optional) - PrimeIcon class (default: 'pi pi-chevron-up')
- behavior: 'auto' | 'smooth' (optional) - Scroll behavior (default: 'smooth')
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- target: Enum (scroll window or parent container)
- threshold: Number (pixels from top)
- icon: String (PrimeIcon class)
- behavior: Enum (scroll animation type)

Child Components: NONE

Usage Example:
<ScrollTopWrapper />
<ScrollTopWrapper threshold={200} icon="pi pi-arrow-up" />
<ScrollTopWrapper target="parent" />
```

---

## LEVEL 2: SIMPLE CHILDREN COMPONENTS

These components accept simple children like text, basic HTML elements, or simple React nodes.

### 2.1 Button Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Button with the following specifications:

Component Name: ButtonWrapper
Import: import { Button } from 'primereact/button';

Props Interface:
- label: string (optional) - Button text
- icon: string (optional) - PrimeIcon class name
- iconPos: 'left' | 'right' | 'top' | 'bottom' (optional) - Icon position (default: 'left')
- badge: string (optional) - Badge value
- badgeClassName: string (optional) - Badge CSS class
- loading: boolean (optional) - Show loading spinner
- severity: 'success' | 'info' | 'warning' | 'danger' | 'help' | 'secondary' | null (optional)
- raised: boolean (optional) - Raised button style
- rounded: boolean (optional) - Rounded button style
- text: boolean (optional) - Text-only button style
- outlined: boolean (optional) - Outlined button style
- size: 'small' | 'large' | null (optional) - Button size
- disabled: boolean (optional) - Disabled state
- onClick: (e: React.MouseEvent) => void (optional) - Click handler
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (optional) - Button content

Data Types:
- label: String (button text)
- icon: String (PrimeIcon class like 'pi pi-check')
- severity: Predefined color schemes
- badge: String or number (notification count)

Child Components: Text, icons, or simple inline elements

Usage Example:
<ButtonWrapper label="Submit" icon="pi pi-check" severity="success" />
<ButtonWrapper icon="pi pi-search" rounded />
<ButtonWrapper label="Loading" loading />
<ButtonWrapper outlined>Custom Content</ButtonWrapper>
```

### 2.2 Card Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Card with the following specifications:

Component Name: CardWrapper
Import: import { Card } from 'primereact/card';

Props Interface:
- title: string | React.ReactNode (optional) - Card title
- subTitle: string | React.ReactNode (optional) - Card subtitle
- header: React.ReactNode (optional) - Header content (typically image)
- footer: React.ReactNode (optional) - Footer content (typically buttons)
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - Card body content

Data Types:
- title: String or React element
- subTitle: String or React element
- header: React element (commonly <img> or custom header)
- footer: React element (commonly buttons or actions)

Child Components: Any content for card body

Usage Example:
<CardWrapper title="Card Title" subTitle="Subtitle">
  <p>Card content goes here</p>
</CardWrapper>

<CardWrapper 
  header={<img src="/card-header.jpg" />}
  footer={<Button label="Save" />}
>
  Card body content
</CardWrapper>
```

### 2.3 Panel Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Panel with the following specifications:

Component Name: PanelWrapper
Import: import { Panel } from 'primereact/panel';

Props Interface:
- header: string | React.ReactNode (optional) - Panel header
- toggleable: boolean (optional) - Enable collapse/expand
- collapsed: boolean (optional) - Collapsed state (controlled)
- onToggle: (e: {originalEvent: Event, value: boolean}) => void (optional) - Toggle callback
- icons: React.ReactNode (optional) - Custom header icons
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - Panel content

Data Types:
- header: String or React element
- toggleable: Boolean (enables collapse functionality)
- collapsed: Boolean (controlled collapse state)

Child Components: Any content

Usage Example:
<PanelWrapper header="Panel Title">
  <p>Panel content</p>
</PanelWrapper>

<PanelWrapper header="Collapsible Panel" toggleable>
  <p>This panel can be collapsed</p>
</PanelWrapper>
```

### 2.4 Message Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Message with the following specifications:

Component Name: MessageWrapper
Import: import { Message } from 'primereact/message';

Props Interface:
- severity: 'success' | 'info' | 'warn' | 'error' (optional) - Message severity (default: 'info')
- text: string (optional) - Message text
- content: React.ReactNode (optional) - Custom message content
- icon: string (optional) - Custom icon class
- closable: boolean (optional) - Show close button
- onClose: (e: React.MouseEvent) => void (optional) - Close callback
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (optional) - Message content

Data Types:
- severity: Enum (determines color and default icon)
- text: String (simple message text)
- content: React element (for complex messages)

Child Components: Text or simple inline elements

Usage Example:
<MessageWrapper severity="success" text="Operation successful" />
<MessageWrapper severity="error" closable>
  <strong>Error:</strong> Something went wrong
</MessageWrapper>
```

### 2.5 Tooltip Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Tooltip with the following specifications:

Component Name: TooltipWrapper
Import: import { Tooltip } from 'primereact/tooltip';

Props Interface:
- target: string | HTMLElement (required) - CSS selector or element reference
- content: string | React.ReactNode (optional) - Tooltip content
- position: 'right' | 'left' | 'top' | 'bottom' (optional) - Tooltip position (default: 'right')
- event: 'hover' | 'focus' | 'both' (optional) - Trigger event (default: 'hover')
- disabled: boolean (optional) - Disable tooltip
- showDelay: number (optional) - Show delay in ms
- hideDelay: number (optional) - Hide delay in ms
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (optional) - Tooltip content

Data Types:
- target: String (CSS selector like '.my-button') or HTMLElement
- content: String or React element
- position: Enum (tooltip placement)
- event: Enum (trigger type)

Child Components: Text or simple inline elements for content

Usage Example:
<TooltipWrapper target=".my-button" content="Click to submit" position="top" />
<TooltipWrapper target="#save-btn">
  <strong>Save</strong> your changes
</TooltipWrapper>
```

### 2.6 Toolbar Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Toolbar with the following specifications:

Component Name: ToolbarWrapper
Import: import { Toolbar } from 'primereact/toolbar';

Props Interface:
- start: React.ReactNode (optional) - Left side content
- center: React.ReactNode (optional) - Center content
- end: React.ReactNode (optional) - Right side content
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (optional) - Default content

Data Types:
- start/center/end: React elements (typically buttons or button groups)

Child Components: Buttons, ButtonGroups, or any toolbar items

Usage Example:
<ToolbarWrapper 
  start={<Button label="New" icon="pi pi-plus" />}
  end={<Button label="Save" icon="pi pi-check" />}
/>

<ToolbarWrapper 
  start={<><Button label="New" /><Button label="Open" /></>}
  center={<span>Document Editor</span>}
  end={<Button label="Save" />}
/>
```

### 2.7 Dialog Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Dialog with the following specifications:

Component Name: DialogWrapper
Import: import { Dialog } from 'primereact/dialog';

Props Interface:
- visible: boolean (required) - Visibility state
- onHide: () => void (required) - Hide callback
- header: string | React.ReactNode (optional) - Dialog header
- footer: React.ReactNode (optional) - Dialog footer
- modal: boolean (optional) - Modal mode (default: true)
- closable: boolean (optional) - Show close button (default: true)
- dismissableMask: boolean (optional) - Close on mask click
- draggable: boolean (optional) - Enable dragging (default: true)
- resizable: boolean (optional) - Enable resizing (default: true)
- position: 'center' | 'top' | 'bottom' | 'left' | 'right' | 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right' (optional)
- maximizable: boolean (optional) - Show maximize button
- breakpoints: object (optional) - Responsive breakpoints
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - Dialog content

Data Types:
- visible: Boolean (controlled visibility)
- header: String or React element
- footer: React element (typically buttons)
- position: Enum (dialog placement)
- breakpoints: Object like {'960px': '75vw', '640px': '100vw'}

Child Components: Any content for dialog body

Usage Example:
<DialogWrapper 
  visible={showDialog} 
  onHide={() => setShowDialog(false)}
  header="Confirm"
  footer={<Button label="OK" onClick={handleOk} />}
>
  <p>Are you sure?</p>
</DialogWrapper>
```

### 2.8 Sidebar Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Sidebar with the following specifications:

Component Name: SidebarWrapper
Import: import { Sidebar } from 'primereact/sidebar';

Props Interface:
- visible: boolean (required) - Visibility state
- onHide: () => void (required) - Hide callback
- position: 'left' | 'right' | 'top' | 'bottom' (optional) - Sidebar position (default: 'left')
- fullScreen: boolean (optional) - Full screen mode
- modal: boolean (optional) - Modal mode (default: true)
- dismissable: boolean (optional) - Close on mask click (default: true)
- showCloseIcon: boolean (optional) - Show close button (default: true)
- closeOnEscape: boolean (optional) - Close on ESC key (default: true)
- icons: React.ReactNode (optional) - Custom header icons
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - Sidebar content

Data Types:
- visible: Boolean (controlled visibility)
- position: Enum (slide-in direction)
- fullScreen: Boolean (covers entire viewport)

Child Components: Any content (navigation, filters, etc.)

Usage Example:
<SidebarWrapper 
  visible={showSidebar} 
  onHide={() => setShowSidebar(false)}
  position="right"
>
  <h3>Filters</h3>
  <div>Filter content here</div>
</SidebarWrapper>
```

---

## LEVEL 3: COMPLEX CHILDREN COMPONENTS

These components accept specific child component types, templates, or have complex data structures.

### 3.1 DataTable Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact DataTable with the following specifications:

Component Name: DataTableWrapper
Import: import { DataTable } from 'primereact/datatable';
Import: import { Column } from 'primereact/column';

Props Interface:
- value: any[] (required) - Array of data objects
- dataKey: string (optional) - Unique identifier field (recommended)
- paginator: boolean (optional) - Enable pagination
- rows: number (optional) - Rows per page
- rowsPerPageOptions: number[] (optional) - Page size options
- sortMode: 'single' | 'multiple' (optional) - Sort mode
- sortField: string (optional) - Default sort field
- sortOrder: 1 | -1 (optional) - Sort direction (1=asc, -1=desc)
- filters: object (optional) - Filter configuration
- filterDisplay: 'menu' | 'row' (optional) - Filter UI type
- selection: any | any[] (optional) - Selected row(s)
- onSelectionChange: (e: {value: any}) => void (optional) - Selection callback
- selectionMode: 'single' | 'multiple' | 'checkbox' | 'radiobutton' (optional)
- loading: boolean (optional) - Loading state
- emptyMessage: string (optional) - Message when no data
- responsiveLayout: 'scroll' | 'stack' (optional) - Responsive behavior
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - Column components

Data Types:
- value: Array of objects (table data)
- dataKey: String (field name for unique identification)
- rows: Number (items per page)
- sortOrder: Number (1 or -1)
- filters: Object like {name: {value: 'John', matchMode: 'contains'}}

Child Components: MUST be Column components

Column Props:
- field: string - Data field name
- header: string | React.ReactNode - Column header
- sortable: boolean - Enable sorting
- filter: boolean - Enable filtering
- filterPlaceholder: string - Filter input placeholder
- body: (rowData: any) => React.ReactNode - Custom cell template
- style: React.CSSProperties - Column styles

Usage Example:
<DataTableWrapper 
  value={products} 
  dataKey="id"
  paginator 
  rows={10}
  sortMode="multiple"
  filterDisplay="row"
>
  <Column field="name" header="Name" sortable filter />
  <Column field="price" header="Price" sortable body={(data) => `$${data.price}`} />
  <Column field="category" header="Category" filter />
  <Column header="Actions" body={(data) => <Button icon="pi pi-pencil" />} />
</DataTableWrapper>
```

### 3.2 Accordion Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Accordion with the following specifications:

Component Name: AccordionWrapper
Import: import { Accordion, AccordionTab } from 'primereact/accordion';

Props Interface:
- activeIndex: number | number[] (optional) - Active tab index(es)
- onTabChange: (e: {index: number | number[]}) => void (optional) - Tab change callback
- multiple: boolean (optional) - Allow multiple tabs open
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - AccordionTab components

Data Types:
- activeIndex: Number (single mode) or Array of numbers (multiple mode)
- multiple: Boolean (enables multiple tabs open simultaneously)

Child Components: MUST be AccordionTab components

AccordionTab Props:
- header: string | React.ReactNode - Tab header
- disabled: boolean - Disable tab
- headerTemplate: React.ReactNode - Custom header template
- children: React.ReactNode - Tab content

Usage Example:
<AccordionWrapper activeIndex={0}>
  <AccordionTab header="Header 1">
    <p>Content 1</p>
  </AccordionTab>
  <AccordionTab header="Header 2">
    <p>Content 2</p>
  </AccordionTab>
  <AccordionTab header="Header 3" disabled>
    <p>Content 3</p>
  </AccordionTab>
</AccordionWrapper>

<AccordionWrapper multiple activeIndex={[0, 1]}>
  <AccordionTab header="FAQ 1">Answer 1</AccordionTab>
  <AccordionTab header="FAQ 2">Answer 2</AccordionTab>
</AccordionWrapper>
```

### 3.3 TabView Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact TabView with the following specifications:

Component Name: TabViewWrapper
Import: import { TabView, TabPanel } from 'primereact/tabview';

Props Interface:
- activeIndex: number (optional) - Active tab index (controlled)
- onTabChange: (e: {index: number}) => void (optional) - Tab change callback
- scrollable: boolean (optional) - Enable scrolling for many tabs
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - TabPanel components

Data Types:
- activeIndex: Number (0-based tab index)
- scrollable: Boolean (enables horizontal scrolling)

Child Components: MUST be TabPanel components

TabPanel Props:
- header: string | React.ReactNode - Tab header
- leftIcon: string - PrimeIcon class for left icon
- rightIcon: string - PrimeIcon class for right icon
- disabled: boolean - Disable tab
- closable: boolean - Show close button
- headerTemplate: React.ReactNode - Custom header template
- children: React.ReactNode - Tab content

Usage Example:
<TabViewWrapper activeIndex={0}>
  <TabPanel header="Tab 1" leftIcon="pi pi-calendar">
    <p>Tab 1 Content</p>
  </TabPanel>
  <TabPanel header="Tab 2" leftIcon="pi pi-user">
    <p>Tab 2 Content</p>
  </TabPanel>
  <TabPanel header="Tab 3" disabled>
    <p>Tab 3 Content</p>
  </TabPanel>
</TabViewWrapper>
```

### 3.4 Dropdown Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Dropdown with the following specifications:

Component Name: DropdownWrapper
Import: import { Dropdown } from 'primereact/dropdown';

Props Interface:
- value: any (optional) - Selected value
- options: any[] (required) - Array of options
- onChange: (e: {value: any}) => void (optional) - Change callback
- optionLabel: string (optional) - Field name for option label (default: 'label')
- optionValue: string (optional) - Field name for option value (default: 'value')
- placeholder: string (optional) - Placeholder text
- filter: boolean (optional) - Enable filtering
- filterBy: string (optional) - Fields to filter by
- filterPlaceholder: string (optional) - Filter input placeholder
- showClear: boolean (optional) - Show clear button
- disabled: boolean (optional) - Disabled state
- emptyMessage: string (optional) - Message when no options
- emptyFilterMessage: string (optional) - Message when filter returns no results
- itemTemplate: (option: any) => React.ReactNode (optional) - Custom option template
- valueTemplate: (option: any) => React.ReactNode (optional) - Custom selected value template
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Any (selected option value)
- options: Array of objects like [{label: 'Option 1', value: 1}] or simple array ['Option 1', 'Option 2']
- optionLabel: String (field name for display)
- optionValue: String (field name for value)

Child Components: NONE (uses options prop and templates)

Usage Example:
<DropdownWrapper 
  value={selectedCity}
  options={cities}
  onChange={(e) => setSelectedCity(e.value)}
  optionLabel="name"
  placeholder="Select a City"
  filter
/>

<DropdownWrapper 
  value={selectedCountry}
  options={countries}
  onChange={(e) => setSelectedCountry(e.value)}
  optionLabel="name"
  optionValue="code"
  itemTemplate={(option) => (
    <div><img src={option.flag} /> {option.name}</div>
  )}
/>
```

### 3.5 Tree Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Tree with the following specifications:

Component Name: TreeWrapper
Import: import { Tree } from 'primereact/tree';

Props Interface:
- value: TreeNode[] (required) - Array of tree nodes
- selectionMode: 'single' | 'multiple' | 'checkbox' (optional) - Selection mode
- selectionKeys: any (optional) - Selected node keys
- onSelectionChange: (e: {value: any}) => void (optional) - Selection callback
- expandedKeys: any (optional) - Expanded node keys
- onToggle: (e: {value: any}) => void (optional) - Toggle callback
- filter: boolean (optional) - Enable filtering
- filterMode: 'lenient' | 'strict' (optional) - Filter mode
- filterPlaceholder: string (optional) - Filter input placeholder
- loading: boolean (optional) - Loading state
- nodeTemplate: (node: TreeNode) => React.ReactNode (optional) - Custom node template
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Array of TreeNode objects with structure:
  {
    key: string | number (unique identifier)
    label: string (node label)
    data: any (custom data)
    icon: string (PrimeIcon class)
    children: TreeNode[] (child nodes)
    leaf: boolean (is leaf node)
    expanded: boolean (is expanded)
  }
- selectionKeys: Object like {'0': true, '0-0': true} for checkbox mode, or single key for single mode
- expandedKeys: Object like {'0': true, '1': true}

Child Components: NONE (uses value prop with TreeNode structure)

Usage Example:
const nodes = [
  {
    key: '0',
    label: 'Documents',
    icon: 'pi pi-folder',
    children: [
      {key: '0-0', label: 'Work', icon: 'pi pi-folder', leaf: true},
      {key: '0-1', label: 'Personal', icon: 'pi pi-folder', leaf: true}
    ]
  },
  {
    key: '1',
    label: 'Pictures',
    icon: 'pi pi-image',
    leaf: true
  }
];

<TreeWrapper 
  value={nodes}
  selectionMode="checkbox"
  selectionKeys={selectedKeys}
  onSelectionChange={(e) => setSelectedKeys(e.value)}
  filter
/>
```

### 3.6 Menu Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Menu with the following specifications:

Component Name: MenuWrapper
Import: import { Menu } from 'primereact/menu';

Props Interface:
- model: MenuItem[] (required) - Array of menu items
- popup: boolean (optional) - Popup mode
- onShow: () => void (optional) - Show callback (popup mode)
- onHide: () => void (optional) - Hide callback (popup mode)
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- model: Array of MenuItem objects with structure:
  {
    label: string (menu item label)
    icon: string (PrimeIcon class)
    command: (event: any) => void (click handler)
    url: string (navigation URL)
    items: MenuItem[] (submenu items)
    disabled: boolean (disabled state)
    separator: boolean (render as separator)
    template: (item: MenuItem) => React.ReactNode (custom template)
  }

Child Components: NONE (uses model prop)

Usage Example:
const items = [
  {
    label: 'File',
    items: [
      {label: 'New', icon: 'pi pi-plus', command: () => handleNew()},
      {label: 'Open', icon: 'pi pi-folder-open'},
      {separator: true},
      {label: 'Quit', icon: 'pi pi-times'}
    ]
  },
  {
    label: 'Edit',
    items: [
      {label: 'Copy', icon: 'pi pi-copy'},
      {label: 'Paste', icon: 'pi pi-clipboard'}
    ]
  }
];

<MenuWrapper model={items} />

// Popup mode
const menuRef = useRef(null);
<MenuWrapper model={items} popup ref={menuRef} />
<Button label="Show Menu" onClick={(e) => menuRef.current.toggle(e)} />
```

### 3.7 Calendar Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Calendar with the following specifications:

Component Name: CalendarWrapper
Import: import { Calendar } from 'primereact/calendar';

Props Interface:
- value: Date | Date[] (optional) - Selected date(s)
- onChange: (e: {value: Date | Date[]}) => void (optional) - Change callback
- selectionMode: 'single' | 'multiple' | 'range' (optional) - Selection mode (default: 'single')
- dateFormat: string (optional) - Date format (default: 'mm/dd/yy')
- showTime: boolean (optional) - Show time picker
- timeOnly: boolean (optional) - Time picker only
- hourFormat: '12' | '24' (optional) - Hour format (default: '24')
- showIcon: boolean (optional) - Show calendar icon
- icon: string (optional) - Custom icon class
- inline: boolean (optional) - Inline mode (always visible)
- minDate: Date (optional) - Minimum selectable date
- maxDate: Date (optional) - Maximum selectable date
- disabledDates: Date[] (optional) - Array of disabled dates
- disabledDays: number[] (optional) - Disabled days of week (0-6)
- monthNavigator: boolean (optional) - Month dropdown
- yearNavigator: boolean (optional) - Year dropdown
- yearRange: string (optional) - Year range (e.g., '2000:2030')
- placeholder: string (optional) - Placeholder text
- disabled: boolean (optional) - Disabled state
- readOnlyInput: boolean (optional) - Read-only input
- showButtonBar: boolean (optional) - Show today/clear buttons
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Date object (single), Array of Dates (multiple/range)
- selectionMode: Enum ('single' for one date, 'multiple' for many, 'range' for start-end)
- dateFormat: String (e.g., 'mm/dd/yy', 'dd/mm/yy', 'yy-mm-dd')
- disabledDays: Array of numbers (0=Sunday, 6=Saturday)

Child Components: NONE

Usage Example:
<CalendarWrapper 
  value={date}
  onChange={(e) => setDate(e.value)}
  showIcon
  placeholder="Select a date"
/>

<CalendarWrapper 
  value={dateTime}
  onChange={(e) => setDateTime(e.value)}
  showTime
  hourFormat="12"
/>

<CalendarWrapper 
  value={dateRange}
  onChange={(e) => setDateRange(e.value)}
  selectionMode="range"
  readOnlyInput
/>
```

### 3.8 FileUpload Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact FileUpload with the following specifications:

Component Name: FileUploadWrapper
Import: import { FileUpload } from 'primereact/fileupload';

Props Interface:
- name: string (optional) - Name for file input
- url: string (optional) - Upload URL
- mode: 'basic' | 'advanced' (optional) - Upload mode (default: 'advanced')
- multiple: boolean (optional) - Allow multiple files
- accept: string (optional) - Accepted file types (e.g., 'image/*')
- maxFileSize: number (optional) - Max file size in bytes
- auto: boolean (optional) - Auto upload on select
- customUpload: boolean (optional) - Use custom upload handler
- uploadHandler: (e: {files: File[]}) => void (optional) - Custom upload function
- onUpload: (e: {files: File[]}) => void (optional) - Upload success callback
- onSelect: (e: {files: File[]}) => void (optional) - File select callback
- onError: (e: {files: File[]}) => void (optional) - Upload error callback
- onClear: () => void (optional) - Clear callback
- onRemove: (e: {file: File}) => void (optional) - Remove file callback
- emptyTemplate: React.ReactNode (optional) - Custom empty state template
- itemTemplate: (file: object, props: object) => React.ReactNode (optional) - Custom file item template
- chooseLabel: string (optional) - Choose button label
- uploadLabel: string (optional) - Upload button label
- cancelLabel: string (optional) - Cancel button label
- disabled: boolean (optional) - Disabled state
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- mode: Enum ('basic' for simple button, 'advanced' for full UI)
- accept: String (MIME types like 'image/*', '.pdf,.doc', 'image/png,image/jpeg')
- maxFileSize: Number (bytes, e.g., 1000000 for 1MB)
- files: Array of File objects

Child Components: NONE (uses templates)

Usage Example:
<FileUploadWrapper 
  name="demo"
  url="/api/upload"
  accept="image/*"
  maxFileSize={1000000}
  onUpload={handleUpload}
/>

<FileUploadWrapper 
  mode="basic"
  name="file"
  accept=".pdf,.doc"
  customUpload
  uploadHandler={handleCustomUpload}
  chooseLabel="Select Document"
/>
```

### 3.9 AutoComplete Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact AutoComplete with the following specifications:

Component Name: AutoCompleteWrapper
Import: import { AutoComplete } from 'primereact/autocomplete';

Props Interface:
- value: any (optional) - Selected value
- suggestions: any[] (optional) - Array of suggestions to display
- completeMethod: (e: {query: string}) => void (required) - Method to load suggestions
- onChange: (e: {value: any}) => void (optional) - Change callback
- field: string (optional) - Field name for suggestion label (for object arrays)
- multiple: boolean (optional) - Allow multiple selections
- dropdown: boolean (optional) - Show dropdown button
- forceSelection: boolean (optional) - Force selection from suggestions
- placeholder: string (optional) - Placeholder text
- minLength: number (optional) - Minimum characters to trigger search (default: 1)
- delay: number (optional) - Delay before search in ms (default: 300)
- disabled: boolean (optional) - Disabled state
- itemTemplate: (item: any) => React.ReactNode (optional) - Custom suggestion template
- selectedItemTemplate: (value: any) => React.ReactNode (optional) - Custom selected item template
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Any (string for simple, object for complex)
- suggestions: Array of strings or objects
- field: String (property name to display from objects)
- multiple: Boolean (enables multi-select with chips)

Child Components: NONE (uses templates)

Usage Example:
const [filteredCountries, setFilteredCountries] = useState([]);

const searchCountry = (event) => {
  const filtered = countries.filter(country => 
    country.name.toLowerCase().includes(event.query.toLowerCase())
  );
  setFilteredCountries(filtered);
};

<AutoCompleteWrapper 
  value={selectedCountry}
  suggestions={filteredCountries}
  completeMethod={searchCountry}
  field="name"
  onChange={(e) => setSelectedCountry(e.value)}
  placeholder="Search countries"
  dropdown
/>

<AutoCompleteWrapper 
  value={selectedItems}
  suggestions={filteredItems}
  completeMethod={searchItems}
  multiple
  onChange={(e) => setSelectedItems(e.value)}
/>
```

### 3.10 Chart Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Chart with the following specifications:

Component Name: ChartWrapper
Import: import { Chart } from 'primereact/chart';

Props Interface:
- type: 'line' | 'bar' | 'pie' | 'doughnut' | 'polarArea' | 'radar' | 'bubble' | 'scatter' (required) - Chart type
- data: object (required) - Chart data
- options: object (optional) - Chart.js options
- width: string (optional) - Chart width
- height: string (optional) - Chart height
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- type: Enum (chart visualization type)
- data: Object with structure depending on chart type:
  
  Line/Bar Chart:
  {
    labels: string[] (x-axis labels)
    datasets: [{
      label: string (dataset label)
      data: number[] (data points)
      backgroundColor: string | string[] (fill color)
      borderColor: string (line/border color)
      borderWidth: number
    }]
  }
  
  Pie/Doughnut Chart:
  {
    labels: string[] (slice labels)
    datasets: [{
      data: number[] (slice values)
      backgroundColor: string[] (slice colors)
    }]
  }

- options: Chart.js configuration object (plugins, scales, etc.)

Child Components: NONE

Usage Example:
const lineData = {
  labels: ['January', 'February', 'March', 'April', 'May'],
  datasets: [{
    label: 'Sales',
    data: [65, 59, 80, 81, 56],
    borderColor: '#42A5F5',
    backgroundColor: 'rgba(66, 165, 245, 0.2)'
  }]
};

const lineOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'top' }
  }
};

<ChartWrapper type="line" data={lineData} options={lineOptions} />

const pieData = {
  labels: ['Red', 'Blue', 'Yellow'],
  datasets: [{
    data: [300, 50, 100],
    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
  }]
};

<ChartWrapper type="pie" data={pieData} />
```

---

## FORM INPUT COMPONENTS

These are specialized form components with specific data handling requirements.

### 4.1 InputText Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact InputText with the following specifications:

Component Name: InputTextWrapper
Import: import { InputText } from 'primereact/inputtext';

Props Interface:
- value: string (optional) - Input value
- onChange: (e: React.ChangeEvent<HTMLInputElement>) => void (optional) - Change callback
- placeholder: string (optional) - Placeholder text
- disabled: boolean (optional) - Disabled state
- readOnly: boolean (optional) - Read-only state
- type: string (optional) - Input type (default: 'text')
- maxLength: number (optional) - Maximum length
- keyfilter: string | RegExp (optional) - Key filter pattern
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: String
- type: String ('text', 'email', 'password', 'number', etc.)
- keyfilter: String ('int', 'num', 'alpha', 'alphanum') or RegExp

Child Components: NONE

Usage Example:
<InputTextWrapper 
  value={name}
  onChange={(e) => setName(e.target.value)}
  placeholder="Enter name"
/>

<InputTextWrapper 
  value={age}
  onChange={(e) => setAge(e.target.value)}
  keyfilter="int"
  placeholder="Age"
/>
```

### 4.2 InputNumber Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact InputNumber with the following specifications:

Component Name: InputNumberWrapper
Import: import { InputNumber } from 'primereact/inputnumber';

Props Interface:
- value: number (optional) - Input value
- onValueChange: (e: {value: number}) => void (optional) - Value change callback
- format: boolean (optional) - Enable number formatting (default: true)
- showButtons: boolean (optional) - Show increment/decrement buttons
- buttonLayout: 'stacked' | 'horizontal' | 'vertical' (optional) - Button layout
- incrementButtonIcon: string (optional) - Increment button icon
- decrementButtonIcon: string (optional) - Decrement button icon
- mode: 'decimal' | 'currency' (optional) - Input mode (default: 'decimal')
- currency: string (optional) - Currency code (e.g., 'USD')
- currencyDisplay: 'symbol' | 'code' | 'name' (optional) - Currency display
- locale: string (optional) - Locale for formatting (e.g., 'en-US')
- min: number (optional) - Minimum value
- max: number (optional) - Maximum value
- step: number (optional) - Step increment (default: 1)
- minFractionDigits: number (optional) - Minimum decimal places
- maxFractionDigits: number (optional) - Maximum decimal places
- prefix: string (optional) - Prefix text
- suffix: string (optional) - Suffix text
- placeholder: string (optional) - Placeholder text
- disabled: boolean (optional) - Disabled state
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Number
- mode: Enum ('decimal' for numbers, 'currency' for money)
- currency: String (ISO 4217 currency code)
- locale: String (BCP 47 language tag)

Child Components: NONE

Usage Example:
<InputNumberWrapper 
  value={quantity}
  onValueChange={(e) => setQuantity(e.value)}
  showButtons
  min={0}
  max={100}
/>

<InputNumberWrapper 
  value={price}
  onValueChange={(e) => setPrice(e.value)}
  mode="currency"
  currency="USD"
  locale="en-US"
/>

<InputNumberWrapper 
  value={percentage}
  onValueChange={(e) => setPercentage(e.value)}
  suffix="%"
  min={0}
  max={100}
/>
```

### 4.3 Checkbox Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Checkbox with the following specifications:

Component Name: CheckboxWrapper
Import: import { Checkbox } from 'primereact/checkbox';

Props Interface:
- checked: boolean (optional) - Checked state
- onChange: (e: {checked: boolean}) => void (optional) - Change callback
- inputId: string (optional) - ID for input element (for label association)
- value: any (optional) - Value for checkbox (used in groups)
- name: string (optional) - Name for input element
- disabled: boolean (optional) - Disabled state
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- checked: Boolean
- value: Any (used when multiple checkboxes share same name)

Child Components: NONE (typically used with label element)

Usage Example:
<div className="flex align-items-center">
  <CheckboxWrapper 
    inputId="accept"
    checked={accepted}
    onChange={(e) => setAccepted(e.checked)}
  />
  <label htmlFor="accept" className="ml-2">I accept the terms</label>
</div>

// Checkbox group
<CheckboxWrapper 
  inputId="category1"
  name="category"
  value="Technology"
  checked={categories.includes('Technology')}
  onChange={(e) => onCategoryChange(e)}
/>
```

### 4.4 RadioButton Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact RadioButton with the following specifications:

Component Name: RadioButtonWrapper
Import: import { RadioButton } from 'primereact/radiobutton';

Props Interface:
- value: any (required) - Value of radio button
- checked: boolean (optional) - Checked state
- onChange: (e: {value: any}) => void (optional) - Change callback
- inputId: string (optional) - ID for input element (for label association)
- name: string (optional) - Name for radio group
- disabled: boolean (optional) - Disabled state
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Any (the value this radio represents)
- checked: Boolean (typically checked={selectedValue === value})

Child Components: NONE (typically used with label element)

Usage Example:
<div className="flex flex-column gap-3">
  <div className="flex align-items-center">
    <RadioButtonWrapper 
      inputId="option1"
      name="option"
      value="Option 1"
      checked={selectedOption === 'Option 1'}
      onChange={(e) => setSelectedOption(e.value)}
    />
    <label htmlFor="option1" className="ml-2">Option 1</label>
  </div>
  <div className="flex align-items-center">
    <RadioButtonWrapper 
      inputId="option2"
      name="option"
      value="Option 2"
      checked={selectedOption === 'Option 2'}
      onChange={(e) => setSelectedOption(e.value)}
    />
    <label htmlFor="option2" className="ml-2">Option 2</label>
  </div>
</div>
```

### 4.5 MultiSelect Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact MultiSelect with the following specifications:

Component Name: MultiSelectWrapper
Import: import { MultiSelect } from 'primereact/multiselect';

Props Interface:
- value: any[] (optional) - Selected values array
- options: any[] (required) - Array of options
- onChange: (e: {value: any[]}) => void (optional) - Change callback
- optionLabel: string (optional) - Field name for option label (default: 'label')
- optionValue: string (optional) - Field name for option value (default: 'value')
- placeholder: string (optional) - Placeholder text
- filter: boolean (optional) - Enable filtering
- filterBy: string (optional) - Fields to filter by
- filterPlaceholder: string (optional) - Filter input placeholder
- showClear: boolean (optional) - Show clear button
- disabled: boolean (optional) - Disabled state
- maxSelectedLabels: number (optional) - Max labels to display (default: 3)
- selectedItemsLabel: string (optional) - Label when max exceeded (default: '{0} items selected')
- display: 'comma' | 'chip' (optional) - Display mode (default: 'comma')
- emptyFilterMessage: string (optional) - Message when filter returns no results
- itemTemplate: (option: any) => React.ReactNode (optional) - Custom option template
- selectedItemTemplate: (value: any) => React.ReactNode (optional) - Custom selected item template
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Array of selected values
- options: Array of objects like [{label: 'Option 1', value: 1}]
- display: Enum ('comma' for comma-separated, 'chip' for chip display)

Child Components: NONE (uses options prop and templates)

Usage Example:
<MultiSelectWrapper 
  value={selectedCities}
  options={cities}
  onChange={(e) => setSelectedCities(e.value)}
  optionLabel="name"
  placeholder="Select Cities"
  filter
  display="chip"
/>

<MultiSelectWrapper 
  value={selectedCountries}
  options={countries}
  onChange={(e) => setSelectedCountries(e.value)}
  optionLabel="name"
  optionValue="code"
  maxSelectedLabels={2}
  itemTemplate={(option) => (
    <div><img src={option.flag} /> {option.name}</div>
  )}
/>
```

---

## ADDITIONAL NOTES

### Wrapper Component Best Practices

1. **Type Safety**: Use TypeScript interfaces for all props
2. **Default Props**: Provide sensible defaults where applicable
3. **Error Handling**: Validate required props and provide helpful error messages
4. **Documentation**: Include JSDoc comments for all props
5. **Accessibility**: Ensure proper ARIA attributes and keyboard navigation
6. **Styling Support** (CRITICAL): 
   - ALWAYS include `className?: string` prop
   - ALWAYS include `style?: React.CSSProperties` prop
   - Pass both props through to underlying PrimeReact component
   - Support PrimeFlex utility classes
   - Enable responsive design patterns
7. **Event Handling** (CRITICAL):
   - Include all relevant event handler props (onChange, onClick, etc.)
   - Support simplified value callbacks (onValueChange)
   - Enable Redux integration patterns
   - Provide validation event hooks (onValidate, onError)
   - Support event chaining (before/after hooks)
   - Always make event handlers optional
   - Use proper TypeScript event types
8. **Ref Forwarding**: Use React.forwardRef when component needs ref access

### Implementation Checklist

Every wrapper component MUST:

**Styling:**
- ✓ Include `className` prop in interface
- ✓ Include `style` prop in interface
- ✓ Pass `className` to PrimeReact component
- ✓ Pass `style` to PrimeReact component
- ✓ Document both props in JSDoc comments
- ✓ Show usage examples with styling
- ✓ Support PrimeFlex utility classes
- ✓ Handle style merging if wrapper has defaults

**Event Handling:**
- ✓ Include all component-specific event handlers
- ✓ Add simplified value callbacks where applicable
- ✓ Support Redux dispatch patterns
- ✓ Provide validation hooks (onValidate, onError)
- ✓ Make all handlers optional with `?` operator
- ✓ Use proper TypeScript event types
- ✓ Document event parameters and return values
- ✓ Show Redux integration examples
- ✓ Include event chaining examples
- ✓ Handle errors gracefully in event handlers

### Common Patterns

**Controlled Components**: Most PrimeReact components are controlled, requiring value and onChange props.

**Template Props**: Many components support custom templates for rendering (itemTemplate, headerTemplate, etc.)

**Event Objects**: PrimeReact callbacks typically receive event objects with specific structures (e.g., {value, originalEvent})

**Responsive Design**: Use PrimeFlex utility classes for responsive layouts via className prop

**Style Composition**: Combine PrimeFlex classes with inline styles for maximum flexibility:
```jsx
<ComponentWrapper 
  className="col-12 md:col-6 p-3 shadow-2"
  style={{ minHeight: '200px', backgroundColor: '#f8f9fa' }}
/>
```

**Redux Integration**: Support both direct event handlers and simplified callbacks:
```jsx
// Direct event handler
<InputWrapper 
  value={name}
  onChange={(e) => dispatch(updateName(e.target.value))}
/>

// Simplified callback
<InputWrapper 
  value={name}
  onValueChange={(value) => dispatch(updateName(value))}
/>
```

**Event Chaining**: Support multiple event handlers for complex workflows:
```jsx
<InputWrapper
  value={email}
  beforeChange={(value) => validateEmail(value)}
  onChange={(e) => setEmail(e.target.value)}
  afterChange={(value) => dispatch(saveEmail(value))}
  onError={(error) => dispatch(showError(error))}
/>
```

### Testing Considerations

- Test with various data types and edge cases
- Verify accessibility with screen readers
- Test keyboard navigation
- Validate form submission and validation
- Test responsive behavior at different breakpoints
- Test custom className and style prop application
- Verify style merging when wrapper has defaults
- Test all event handlers fire correctly
- Verify Redux action dispatching
- Test event handler chaining
- Validate error handling in event callbacks
- Test event handler cleanup on unmount

---

**Document Version**: 2.0  
**Last Updated**: February 2026  
**Total Component Prompts**: 90+ (complete coverage)
**Styling**: All components support className and style props
**Events**: All components support comprehensive event handling and Redux integration




---

## ADDITIONAL FORM COMPONENTS

### 5.1 InputTextarea Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact InputTextarea with the following specifications:

Component Name: InputTextareaWrapper
Import: import { InputTextarea } from 'primereact/inputtextarea';

Props Interface:
- value: string (optional) - Textarea value
- onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void (optional) - Change callback
- rows: number (optional) - Number of rows
- cols: number (optional) - Number of columns
- autoResize: boolean (optional) - Auto resize based on content
- placeholder: string (optional) - Placeholder text
- disabled: boolean (optional) - Disabled state
- readOnly: boolean (optional) - Read-only state
- maxLength: number (optional) - Maximum length
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: String (multi-line text)
- rows/cols: Number (dimensions)
- autoResize: Boolean (dynamic height adjustment)

Child Components: NONE

Usage Example:
<InputTextareaWrapper 
  value={description}
  onChange={(e) => setDescription(e.target.value)}
  rows={5}
  cols={30}
  placeholder="Enter description"
/>

<InputTextareaWrapper 
  value={comment}
  onChange={(e) => setComment(e.target.value)}
  autoResize
  maxLength={500}
/>
```

### 5.2 Password Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Password with the following specifications:

Component Name: PasswordWrapper
Import: import { Password } from 'primereact/password';

Props Interface:
- value: string (optional) - Password value
- onChange: (e: React.ChangeEvent<HTMLInputElement>) => void (optional) - Change callback
- placeholder: string (optional) - Placeholder text
- toggleMask: boolean (optional) - Show/hide password toggle
- feedback: boolean (optional) - Show strength indicator (default: true)
- promptLabel: string (optional) - Prompt text
- weakLabel: string (optional) - Weak password text
- mediumLabel: string (optional) - Medium password text
- strongLabel: string (optional) - Strong password text
- mediumRegex: string (optional) - Regex for medium strength
- strongRegex: string (optional) - Regex for strong strength
- disabled: boolean (optional) - Disabled state
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: String (password text)
- feedback: Boolean (enables strength meter)
- toggleMask: Boolean (show/hide password icon)

Child Components: NONE

Usage Example:
<PasswordWrapper 
  value={password}
  onChange={(e) => setPassword(e.target.value)}
  toggleMask
  feedback
/>

<PasswordWrapper 
  value={password}
  onChange={(e) => setPassword(e.target.value)}
  promptLabel="Enter password"
  weakLabel="Too simple"
  mediumLabel="Average"
  strongLabel="Strong password"
/>
```

### 5.3 InputMask Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact InputMask with the following specifications:

Component Name: InputMaskWrapper
Import: import { InputMask } from 'primereact/inputmask';

Props Interface:
- value: string (optional) - Input value
- onChange: (e: React.ChangeEvent<HTMLInputElement>) => void (optional) - Change callback
- mask: string (required) - Input mask pattern
- slotChar: string (optional) - Placeholder character (default: '_')
- autoClear: boolean (optional) - Clear incomplete input on blur (default: true)
- unmask: boolean (optional) - Return unmasked value
- placeholder: string (optional) - Placeholder text
- disabled: boolean (optional) - Disabled state
- readOnly: boolean (optional) - Read-only state
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- mask: String (pattern like '99-999999', '(999) 999-9999', '99/99/9999')
  - 9: Numeric (0-9)
  - a: Alphabetic (a-z, A-Z)
  - *: Alphanumeric (a-z, A-Z, 0-9)
- slotChar: String (single character)
- unmask: Boolean (returns value without mask characters)

Child Components: NONE

Usage Example:
<InputMaskWrapper 
  value={phone}
  onChange={(e) => setPhone(e.target.value)}
  mask="(999) 999-9999"
  placeholder="(999) 999-9999"
/>

<InputMaskWrapper 
  value={ssn}
  onChange={(e) => setSsn(e.target.value)}
  mask="999-99-9999"
  unmask
/>

<InputMaskWrapper 
  value={date}
  onChange={(e) => setDate(e.target.value)}
  mask="99/99/9999"
  slotChar="mm/dd/yyyy"
/>
```

### 5.4 Slider Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Slider with the following specifications:

Component Name: SliderWrapper
Import: import { Slider } from 'primereact/slider';

Props Interface:
- value: number | number[] (optional) - Slider value(s)
- onChange: (e: {value: number | number[]}) => void (optional) - Change callback
- min: number (optional) - Minimum value (default: 0)
- max: number (optional) - Maximum value (default: 100)
- step: number (optional) - Step increment (default: 1)
- range: boolean (optional) - Enable range selection (two handles)
- orientation: 'horizontal' | 'vertical' (optional) - Slider orientation (default: 'horizontal')
- disabled: boolean (optional) - Disabled state
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Number (single value) or Array of two numbers (range)
- range: Boolean (enables two-handle range selection)
- orientation: Enum (horizontal or vertical slider)

Child Components: NONE

Usage Example:
<SliderWrapper 
  value={volume}
  onChange={(e) => setVolume(e.value)}
  min={0}
  max={100}
/>

<SliderWrapper 
  value={priceRange}
  onChange={(e) => setPriceRange(e.value)}
  range
  min={0}
  max={1000}
  step={10}
/>

<SliderWrapper 
  value={temperature}
  onChange={(e) => setTemperature(e.value)}
  orientation="vertical"
  min={-20}
  max={50}
/>
```

### 5.5 Rating Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Rating with the following specifications:

Component Name: RatingWrapper
Import: import { Rating } from 'primereact/rating';

Props Interface:
- value: number (optional) - Rating value
- onChange: (e: {value: number}) => void (optional) - Change callback
- stars: number (optional) - Number of stars (default: 5)
- cancel: boolean (optional) - Show cancel icon (default: true)
- disabled: boolean (optional) - Disabled state
- readOnly: boolean (optional) - Read-only state
- onIcon: string (optional) - Custom filled star icon
- offIcon: string (optional) - Custom empty star icon
- cancelIcon: string (optional) - Custom cancel icon
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Number (0 to stars count)
- stars: Number (total number of stars)
- cancel: Boolean (allows clearing rating)

Child Components: NONE

Usage Example:
<RatingWrapper 
  value={rating}
  onChange={(e) => setRating(e.value)}
/>

<RatingWrapper 
  value={productRating}
  onChange={(e) => setProductRating(e.value)}
  stars={10}
  cancel={false}
/>

<RatingWrapper 
  value={averageRating}
  readOnly
  cancel={false}
/>
```

### 5.6 Knob Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Knob with the following specifications:

Component Name: KnobWrapper
Import: import { Knob } from 'primereact/knob';

Props Interface:
- value: number (optional) - Knob value
- onChange: (e: {value: number}) => void (optional) - Change callback
- size: number (optional) - Diameter in pixels (default: 100)
- min: number (optional) - Minimum value (default: 0)
- max: number (optional) - Maximum value (default: 100)
- step: number (optional) - Step increment (default: 1)
- valueColor: string (optional) - Value arc color
- rangeColor: string (optional) - Range arc color
- textColor: string (optional) - Text color
- strokeWidth: number (optional) - Arc thickness (default: 14)
- showValue: boolean (optional) - Display value text (default: true)
- valueTemplate: string (optional) - Value display template (e.g., '{value}%')
- readOnly: boolean (optional) - Read-only state
- disabled: boolean (optional) - Disabled state
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Number (current value)
- size: Number (pixels)
- valueTemplate: String (template with {value} placeholder)

Child Components: NONE

Usage Example:
<KnobWrapper 
  value={volume}
  onChange={(e) => setVolume(e.value)}
  valueTemplate="{value}%"
/>

<KnobWrapper 
  value={temperature}
  onChange={(e) => setTemperature(e.value)}
  min={-20}
  max={50}
  size={150}
  valueColor="#FF6B6B"
/>
```

### 5.7 ColorPicker Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact ColorPicker with the following specifications:

Component Name: ColorPickerWrapper
Import: import { ColorPicker } from 'primereact/colorpicker';

Props Interface:
- value: string (optional) - Color value
- onChange: (e: {value: string}) => void (optional) - Change callback
- format: 'hex' | 'rgb' | 'hsb' (optional) - Color format (default: 'hex')
- inline: boolean (optional) - Inline mode (always visible)
- disabled: boolean (optional) - Disabled state
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: String (color in specified format)
- format: Enum ('hex' like '#FF0000', 'rgb' like 'rgb(255,0,0)', 'hsb')

Child Components: NONE

Usage Example:
<ColorPickerWrapper 
  value={color}
  onChange={(e) => setColor(e.value)}
/>

<ColorPickerWrapper 
  value={backgroundColor}
  onChange={(e) => setBackgroundColor(e.value)}
  format="rgb"
/>

<ColorPickerWrapper 
  value={themeColor}
  onChange={(e) => setThemeColor(e.value)}
  inline
/>
```

### 5.8 ToggleButton Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact ToggleButton with the following specifications:

Component Name: ToggleButtonWrapper
Import: import { ToggleButton } from 'primereact/togglebutton';

Props Interface:
- checked: boolean (optional) - Checked state
- onChange: (e: {value: boolean}) => void (optional) - Change callback
- onLabel: string (optional) - Label when checked (default: 'Yes')
- offLabel: string (optional) - Label when unchecked (default: 'No')
- onIcon: string (optional) - Icon when checked
- offIcon: string (optional) - Icon when unchecked
- disabled: boolean (optional) - Disabled state
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- checked: Boolean
- onLabel/offLabel: String (button text for each state)
- onIcon/offIcon: String (PrimeIcon classes)

Child Components: NONE

Usage Example:
<ToggleButtonWrapper 
  checked={active}
  onChange={(e) => setActive(e.value)}
  onLabel="Active"
  offLabel="Inactive"
/>

<ToggleButtonWrapper 
  checked={notifications}
  onChange={(e) => setNotifications(e.value)}
  onIcon="pi pi-bell"
  offIcon="pi pi-bell-slash"
/>
```

### 5.9 InputSwitch Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact InputSwitch with the following specifications:

Component Name: InputSwitchWrapper
Import: import { InputSwitch } from 'primereact/inputswitch';

Props Interface:
- checked: boolean (optional) - Checked state
- onChange: (e: {value: boolean}) => void (optional) - Change callback
- inputId: string (optional) - ID for input element
- disabled: boolean (optional) - Disabled state
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- checked: Boolean (on/off state)

Child Components: NONE (typically used with label)

Usage Example:
<div className="flex align-items-center">
  <InputSwitchWrapper 
    inputId="switch1"
    checked={enabled}
    onChange={(e) => setEnabled(e.value)}
  />
  <label htmlFor="switch1" className="ml-2">Enable Feature</label>
</div>
```

### 5.10 SelectButton Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact SelectButton with the following specifications:

Component Name: SelectButtonWrapper
Import: import { SelectButton } from 'primereact/selectbutton';

Props Interface:
- value: any (optional) - Selected value
- options: any[] (required) - Array of options
- onChange: (e: {value: any}) => void (optional) - Change callback
- optionLabel: string (optional) - Field name for option label
- optionValue: string (optional) - Field name for option value
- optionDisabled: string (optional) - Field name for disabled state
- multiple: boolean (optional) - Allow multiple selections
- disabled: boolean (optional) - Disabled state
- itemTemplate: (option: any) => React.ReactNode (optional) - Custom option template
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Any (single value) or Array (multiple mode)
- options: Array of objects or simple values
- multiple: Boolean (enables multi-select)

Child Components: NONE (uses options prop)

Usage Example:
const options = ['Off', 'On'];

<SelectButtonWrapper 
  value={value}
  options={options}
  onChange={(e) => setValue(e.value)}
/>

const viewOptions = [
  {label: 'List', value: 'list', icon: 'pi pi-list'},
  {label: 'Grid', value: 'grid', icon: 'pi pi-th-large'}
];

<SelectButtonWrapper 
  value={viewMode}
  options={viewOptions}
  onChange={(e) => setViewMode(e.value)}
  optionLabel="label"
  itemTemplate={(option) => <i className={option.icon}></i>}
/>
```


### 5.11 Listbox Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Listbox with the following specifications:

Component Name: ListboxWrapper
Import: import { Listbox } from 'primereact/listbox';

Props Interface:
- value: any | any[] (optional) - Selected value(s)
- options: any[] (required) - Array of options
- onChange: (e: {value: any}) => void (optional) - Change callback
- optionLabel: string (optional) - Field name for option label
- optionValue: string (optional) - Field name for option value
- optionDisabled: string (optional) - Field name for disabled state
- optionGroupLabel: string (optional) - Field name for group label
- optionGroupChildren: string (optional) - Field name for group children
- multiple: boolean (optional) - Allow multiple selections
- filter: boolean (optional) - Enable filtering
- filterBy: string (optional) - Fields to filter by
- filterPlaceholder: string (optional) - Filter input placeholder
- emptyMessage: string (optional) - Message when no options
- emptyFilterMessage: string (optional) - Message when filter returns no results
- disabled: boolean (optional) - Disabled state
- itemTemplate: (option: any) => React.ReactNode (optional) - Custom option template
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- listStyle: React.CSSProperties (optional) - Inline styles for list

Data Types:
- value: Any (single) or Array (multiple mode)
- options: Array of objects or simple values, can include groups
- multiple: Boolean (enables multi-select with checkboxes)

Child Components: NONE (uses options prop)

Usage Example:
<ListboxWrapper 
  value={selectedCity}
  options={cities}
  onChange={(e) => setSelectedCity(e.value)}
  optionLabel="name"
  filter
/>

<ListboxWrapper 
  value={selectedCountries}
  options={countries}
  onChange={(e) => setSelectedCountries(e.value)}
  multiple
  optionLabel="name"
  listStyle={{maxHeight: '250px'}}
/>
```

### 5.12 CascadeSelect Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact CascadeSelect with the following specifications:

Component Name: CascadeSelectWrapper
Import: import { CascadeSelect } from 'primereact/cascadeselect';

Props Interface:
- value: any (optional) - Selected value
- options: any[] (required) - Array of hierarchical options
- onChange: (e: {value: any}) => void (optional) - Change callback
- optionLabel: string (optional) - Field name for option label
- optionValue: string (optional) - Field name for option value
- optionGroupLabel: string (optional) - Field name for group label
- optionGroupChildren: string (optional) - Field name for group children (default: 'items')
- placeholder: string (optional) - Placeholder text
- disabled: boolean (optional) - Disabled state
- itemTemplate: (option: any) => React.ReactNode (optional) - Custom option template
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Any (selected leaf value)
- options: Array of nested objects with structure:
  {
    label: string,
    value: any,
    items: [ /* child options */ ]
  }

Child Components: NONE (uses options prop)

Usage Example:
const countries = [
  {
    name: 'USA',
    code: 'US',
    states: [
      {name: 'California', cities: [{name: 'Los Angeles'}, {name: 'San Francisco'}]},
      {name: 'Texas', cities: [{name: 'Houston'}, {name: 'Dallas'}]}
    ]
  }
];

<CascadeSelectWrapper 
  value={selectedCity}
  options={countries}
  onChange={(e) => setSelectedCity(e.value)}
  optionLabel="name"
  optionGroupLabel="name"
  optionGroupChildren="states"
  placeholder="Select a City"
/>
```

### 5.13 TreeSelect Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact TreeSelect with the following specifications:

Component Name: TreeSelectWrapper
Import: import { TreeSelect } from 'primereact/treeselect';

Props Interface:
- value: any (optional) - Selected node key(s)
- options: TreeNode[] (required) - Array of tree nodes
- onChange: (e: {value: any}) => void (optional) - Change callback
- selectionMode: 'single' | 'multiple' | 'checkbox' (optional) - Selection mode (default: 'single')
- placeholder: string (optional) - Placeholder text
- filter: boolean (optional) - Enable filtering
- filterBy: string (optional) - Fields to filter by (default: 'label')
- filterPlaceholder: string (optional) - Filter input placeholder
- emptyMessage: string (optional) - Message when no options
- display: 'comma' | 'chip' (optional) - Display mode for multiple (default: 'comma')
- metaKeySelection: boolean (optional) - Require meta key for multi-select
- disabled: boolean (optional) - Disabled state
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: String/Number (single), Object (checkbox mode with keys)
- options: Array of TreeNode objects (same structure as Tree component)
- selectionMode: Enum (single value, multiple values, or checkbox tree)

Child Components: NONE (uses options prop)

Usage Example:
const nodes = [
  {
    key: '0',
    label: 'Documents',
    children: [
      {key: '0-0', label: 'Work'},
      {key: '0-1', label: 'Personal'}
    ]
  }
];

<TreeSelectWrapper 
  value={selectedNodeKey}
  options={nodes}
  onChange={(e) => setSelectedNodeKey(e.value)}
  placeholder="Select Item"
/>

<TreeSelectWrapper 
  value={selectedNodeKeys}
  options={nodes}
  onChange={(e) => setSelectedNodeKeys(e.value)}
  selectionMode="checkbox"
  display="chip"
/>
```

### 5.14 Chips Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Chips with the following specifications:

Component Name: ChipsWrapper
Import: import { Chips } from 'primereact/chips';

Props Interface:
- value: any[] (optional) - Array of chip values
- onChange: (e: {value: any[]}) => void (optional) - Change callback
- max: number (optional) - Maximum number of chips
- separator: string (optional) - Separator character for adding chips (default: ',')
- allowDuplicate: boolean (optional) - Allow duplicate values (default: true)
- addOnBlur: boolean (optional) - Add chip on blur
- placeholder: string (optional) - Placeholder text
- disabled: boolean (optional) - Disabled state
- removable: boolean (optional) - Show remove icon (default: true)
- itemTemplate: (item: any) => React.ReactNode (optional) - Custom chip template
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Array of strings or objects
- max: Number (maximum chips allowed)
- separator: String (character to split input, e.g., ',' or ';')

Child Components: NONE (uses value array)

Usage Example:
<ChipsWrapper 
  value={tags}
  onChange={(e) => setTags(e.value)}
  placeholder="Add tags"
/>

<ChipsWrapper 
  value={emails}
  onChange={(e) => setEmails(e.value)}
  max={5}
  separator=";"
  allowDuplicate={false}
/>
```

### 5.15 Editor Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Editor with the following specifications:

Component Name: EditorWrapper
Import: import { Editor } from 'primereact/editor';

Props Interface:
- value: string (optional) - HTML content
- onTextChange: (e: {htmlValue: string, textValue: string}) => void (optional) - Change callback
- placeholder: string (optional) - Placeholder text
- readOnly: boolean (optional) - Read-only state
- modules: object (optional) - Quill modules configuration
- formats: string[] (optional) - Allowed formats
- headerTemplate: React.ReactNode (optional) - Custom toolbar template
- style: React.CSSProperties (optional) - Inline styles for container
- className: string (optional) - Additional CSS classes

Data Types:
- value: String (HTML content)
- modules: Object (Quill configuration for toolbar, etc.)
- formats: Array of strings (allowed formatting options)

Child Components: NONE

Usage Example:
<EditorWrapper 
  value={text}
  onTextChange={(e) => setText(e.htmlValue)}
  style={{height: '320px'}}
/>

const header = (
  <span className="ql-formats">
    <button className="ql-bold"></button>
    <button className="ql-italic"></button>
    <button className="ql-underline"></button>
  </span>
);

<EditorWrapper 
  value={content}
  onTextChange={(e) => setContent(e.htmlValue)}
  headerTemplate={header}
/>
```

### 5.16 InputOtp Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact InputOtp with the following specifications:

Component Name: InputOtpWrapper
Import: import { InputOtp } from 'primereact/inputotp';

Props Interface:
- value: string | number (optional) - OTP value
- onChange: (e: {value: string | number}) => void (optional) - Change callback
- length: number (optional) - Number of OTP digits (default: 4)
- mask: boolean (optional) - Mask input characters
- integerOnly: boolean (optional) - Accept only integers (default: false)
- disabled: boolean (optional) - Disabled state
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: String or Number (OTP code)
- length: Number (number of input boxes)
- mask: Boolean (hide characters like password)

Child Components: NONE

Usage Example:
<InputOtpWrapper 
  value={otp}
  onChange={(e) => setOtp(e.value)}
  length={6}
  integerOnly
/>

<InputOtpWrapper 
  value={secureCode}
  onChange={(e) => setSecureCode(e.value)}
  mask
/>
```

### 5.17 TriStateCheckbox Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact TriStateCheckbox with the following specifications:

Component Name: TriStateCheckboxWrapper
Import: import { TriStateCheckbox } from 'primereact/tristatecheckbox';

Props Interface:
- value: boolean | null (optional) - Checkbox state (true/false/null)
- onChange: (e: {value: boolean | null}) => void (optional) - Change callback
- inputId: string (optional) - ID for input element
- disabled: boolean (optional) - Disabled state
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Boolean or null (true=checked, false=unchecked, null=indeterminate)

Child Components: NONE (typically used with label)

Usage Example:
<div className="flex align-items-center">
  <TriStateCheckboxWrapper 
    inputId="tristate"
    value={value}
    onChange={(e) => setValue(e.value)}
  />
  <label htmlFor="tristate" className="ml-2">
    {value === null ? 'Indeterminate' : value ? 'Checked' : 'Unchecked'}
  </label>
</div>
```

### 5.18 FloatLabel Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact FloatLabel with the following specifications:

Component Name: FloatLabelWrapper
Import: import { FloatLabel } from 'primereact/floatlabel';

Props Interface:
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - Input component and label

Data Types:
- children: Must contain an input component and a label element

Child Components: Input component (InputText, Dropdown, etc.) and label element

Usage Example:
<FloatLabelWrapper>
  <InputText id="username" value={value} onChange={(e) => setValue(e.target.value)} />
  <label htmlFor="username">Username</label>
</FloatLabelWrapper>

<FloatLabelWrapper>
  <Dropdown id="country" value={selectedCountry} options={countries} onChange={(e) => setSelectedCountry(e.value)} />
  <label htmlFor="country">Select a Country</label>
</FloatLabelWrapper>
```

### 5.19 IconField Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact IconField with the following specifications:

Component Name: IconFieldWrapper
Import: import { IconField } from 'primereact/iconfield';
Import: import { InputIcon } from 'primereact/inputicon';

Props Interface:
- iconPosition: 'left' | 'right' (optional) - Icon position (default: 'left')
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - InputIcon and input component

Data Types:
- iconPosition: Enum (icon placement)

Child Components: InputIcon component and input component (InputText, etc.)

Usage Example:
<IconFieldWrapper iconPosition="left">
  <InputIcon className="pi pi-search" />
  <InputText placeholder="Search" />
</IconFieldWrapper>

<IconFieldWrapper iconPosition="right">
  <InputText placeholder="Email" />
  <InputIcon className="pi pi-envelope" />
</IconFieldWrapper>
```

### 5.20 InputGroup Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact InputGroup with the following specifications:

Component Name: InputGroupWrapper
Import: import { InputGroup } from 'primereact/inputgroup';
Import: import { InputGroupAddon } from 'primereact/inputgroupaddon';

Props Interface:
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - InputGroupAddon and input components

Data Types:
- children: Combination of InputGroupAddon and input components

Child Components: InputGroupAddon (for text/icons/buttons) and input components

Usage Example:
<InputGroupWrapper>
  <InputGroupAddon>
    <i className="pi pi-user"></i>
  </InputGroupAddon>
  <InputText placeholder="Username" />
</InputGroupWrapper>

<InputGroupWrapper>
  <InputGroupAddon>$</InputGroupAddon>
  <InputNumber placeholder="Price" />
  <InputGroupAddon>.00</InputGroupAddon>
</InputGroupWrapper>

<InputGroupWrapper>
  <InputText placeholder="Search" />
  <InputGroupAddon>
    <Button icon="pi pi-search" />
  </InputGroupAddon>
</InputGroupWrapper>
```

---

## ADDITIONAL BUTTON COMPONENTS

### 6.1 ButtonGroup Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact ButtonGroup with the following specifications:

Component Name: ButtonGroupWrapper
Import: import { ButtonGroup } from 'primereact/buttongroup';

Props Interface:
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - Button components

Data Types:
- children: Multiple Button components

Child Components: Button components

Usage Example:
<ButtonGroupWrapper>
  <Button label="Save" icon="pi pi-check" />
  <Button label="Delete" icon="pi pi-trash" />
  <Button label="Cancel" icon="pi pi-times" />
</ButtonGroupWrapper>
```

### 6.2 SplitButton Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact SplitButton with the following specifications:

Component Name: SplitButtonWrapper
Import: import { SplitButton } from 'primereact/splitbutton';

Props Interface:
- label: string (optional) - Button label
- icon: string (optional) - Button icon
- model: MenuItem[] (required) - Array of menu items
- onClick: (e: React.MouseEvent) => void (optional) - Main button click handler
- severity: 'success' | 'info' | 'warning' | 'danger' | 'help' | 'secondary' | null (optional)
- raised: boolean (optional) - Raised button style
- rounded: boolean (optional) - Rounded button style
- text: boolean (optional) - Text-only button style
- outlined: boolean (optional) - Outlined button style
- size: 'small' | 'large' | null (optional) - Button size
- disabled: boolean (optional) - Disabled state
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- model: Array of MenuItem objects (same as Menu component)
- severity: Enum (color scheme)

Child Components: NONE (uses model prop)

Usage Example:
const items = [
  {label: 'Update', icon: 'pi pi-refresh', command: () => update()},
  {label: 'Delete', icon: 'pi pi-times', command: () => delete()}
];

<SplitButtonWrapper 
  label="Save"
  icon="pi pi-check"
  model={items}
  onClick={save}
/>
```

### 6.3 SpeedDial Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact SpeedDial with the following specifications:

Component Name: SpeedDialWrapper
Import: import { SpeedDial } from 'primereact/speeddial';

Props Interface:
- model: MenuItem[] (required) - Array of menu items
- direction: 'up' | 'down' | 'left' | 'right' | 'up-left' | 'up-right' | 'down-left' | 'down-right' (optional) - Direction of items (default: 'up')
- transitionDelay: number (optional) - Transition delay in ms (default: 30)
- type: 'linear' | 'circle' | 'semi-circle' | 'quarter-circle' (optional) - Layout type (default: 'linear')
- radius: number (optional) - Radius for circle types (default: 0)
- mask: boolean (optional) - Show overlay mask
- disabled: boolean (optional) - Disabled state
- hideOnClickOutside: boolean (optional) - Hide on outside click (default: true)
- buttonClassName: string (optional) - CSS class for main button
- maskClassName: string (optional) - CSS class for mask
- showIcon: string (optional) - Icon when closed (default: 'pi pi-plus')
- hideIcon: string (optional) - Icon when open
- rotateAnimation: boolean (optional) - Rotate main button (default: true)
- onShow: () => void (optional) - Show callback
- onHide: () => void (optional) - Hide callback
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- model: Array of MenuItem objects with icon and command
- direction: Enum (expansion direction)
- type: Enum (layout pattern)

Child Components: NONE (uses model prop)

Usage Example:
const items = [
  {icon: 'pi pi-pencil', command: () => edit()},
  {icon: 'pi pi-trash', command: () => delete()},
  {icon: 'pi pi-upload', command: () => upload()},
  {icon: 'pi pi-external-link', command: () => open()}
];

<SpeedDialWrapper 
  model={items}
  direction="up"
  style={{position: 'fixed', bottom: '2rem', right: '2rem'}}
/>

<SpeedDialWrapper 
  model={items}
  type="circle"
  radius={80}
  mask
/>
```

---

## ADDITIONAL DATA COMPONENTS


### 7.1 DataView Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact DataView with the following specifications:

Component Name: DataViewWrapper
Import: import { DataView } from 'primereact/dataview';

Props Interface:
- value: any[] (required) - Array of data objects
- layout: 'list' | 'grid' (optional) - Display layout (default: 'list')
- paginator: boolean (optional) - Enable pagination
- rows: number (optional) - Rows per page
- first: number (optional) - Index of first record
- onPage: (e: {first: number, rows: number}) => void (optional) - Page change callback
- sortField: string (optional) - Sort field
- sortOrder: 1 | -1 (optional) - Sort direction
- emptyMessage: string (optional) - Message when no data
- header: React.ReactNode (optional) - Header content
- footer: React.ReactNode (optional) - Footer content
- itemTemplate: (data: any, layout: string) => React.ReactNode (required) - Item template
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Array of objects
- layout: Enum ('list' for vertical, 'grid' for grid layout)
- itemTemplate: Function that receives data and layout type

Child Components: NONE (uses itemTemplate)

Usage Example:
const itemTemplate = (product, layout) => {
  if (layout === 'list') {
    return (
      <div className="flex align-items-center p-3">
        <img src={product.image} alt={product.name} width="100" />
        <div className="ml-3">
          <h4>{product.name}</h4>
          <p>${product.price}</p>
        </div>
      </div>
    );
  }
  return (
    <div className="col-12 md:col-4">
      <Card title={product.name}>
        <img src={product.image} alt={product.name} />
        <p>${product.price}</p>
      </Card>
    </div>
  );
};

<DataViewWrapper 
  value={products}
  layout={layout}
  itemTemplate={itemTemplate}
  paginator
  rows={9}
/>
```

### 7.2 OrderList Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact OrderList with the following specifications:

Component Name: OrderListWrapper
Import: import { OrderList } from 'primereact/orderlist';

Props Interface:
- value: any[] (required) - Array of items
- onChange: (e: {value: any[]}) => void (optional) - Change callback
- dataKey: string (optional) - Unique identifier field
- header: string | React.ReactNode (optional) - Header content
- itemTemplate: (item: any) => React.ReactNode (optional) - Item template
- dragdrop: boolean (optional) - Enable drag and drop
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- listStyle: React.CSSProperties (optional) - List container styles

Data Types:
- value: Array of objects (ordered list)
- dragdrop: Boolean (enables drag-drop reordering)

Child Components: NONE (uses itemTemplate)

Usage Example:
const itemTemplate = (item) => {
  return (
    <div className="flex align-items-center">
      <img src={item.image} alt={item.name} width="50" />
      <span className="ml-2">{item.name}</span>
    </div>
  );
};

<OrderListWrapper 
  value={products}
  onChange={(e) => setProducts(e.value)}
  itemTemplate={itemTemplate}
  header="Products"
  dragdrop
/>
```

### 7.3 PickList Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact PickList with the following specifications:

Component Name: PickListWrapper
Import: import { PickList } from 'primereact/picklist';

Props Interface:
- source: any[] (required) - Source array
- target: any[] (required) - Target array
- onChange: (e: {source: any[], target: any[]}) => void (required) - Change callback
- dataKey: string (optional) - Unique identifier field
- sourceHeader: React.ReactNode (optional) - Source list header
- targetHeader: React.ReactNode (optional) - Target list header
- itemTemplate: (item: any) => React.ReactNode (optional) - Item template
- sourceItemTemplate: (item: any) => React.ReactNode (optional) - Source item template
- targetItemTemplate: (item: any) => React.ReactNode (optional) - Target item template
- showSourceControls: boolean (optional) - Show source reorder controls (default: true)
- showTargetControls: boolean (optional) - Show target reorder controls (default: true)
- sourceStyle: React.CSSProperties (optional) - Source list styles
- targetStyle: React.CSSProperties (optional) - Target list styles
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- source/target: Arrays of objects
- onChange: Returns both source and target arrays

Child Components: NONE (uses templates)

Usage Example:
<PickListWrapper 
  source={availableProducts}
  target={selectedProducts}
  onChange={(e) => {
    setAvailableProducts(e.source);
    setSelectedProducts(e.target);
  }}
  itemTemplate={(item) => <div>{item.name}</div>}
  sourceHeader="Available"
  targetHeader="Selected"
/>
```

### 7.4 OrganizationChart Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact OrganizationChart with the following specifications:

Component Name: OrganizationChartWrapper
Import: import { OrganizationChart } from 'primereact/organizationchart';

Props Interface:
- value: TreeNode[] (required) - Array of tree nodes
- selectionMode: 'single' | 'multiple' (optional) - Selection mode
- selection: any (optional) - Selected node(s)
- onSelectionChange: (e: {data: any}) => void (optional) - Selection callback
- nodeTemplate: (node: any) => React.ReactNode (optional) - Custom node template
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Array of TreeNode objects with structure:
  {
    label: string,
    expanded: boolean,
    data: any,
    children: TreeNode[]
  }
- selectionMode: Enum (single or multiple node selection)

Child Components: NONE (uses value prop and nodeTemplate)

Usage Example:
const data = [{
  label: 'CEO',
  expanded: true,
  data: {name: 'John Doe', title: 'CEO'},
  children: [
    {
      label: 'CTO',
      data: {name: 'Jane Smith', title: 'CTO'},
      children: [
        {label: 'Dev Manager', data: {name: 'Bob Johnson'}}
      ]
    }
  ]
}];

<OrganizationChartWrapper 
  value={data}
  nodeTemplate={(node) => (
    <div>
      <div>{node.data.name}</div>
      <div>{node.data.title}</div>
    </div>
  )}
/>
```

### 7.5 Timeline Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Timeline with the following specifications:

Component Name: TimelineWrapper
Import: import { Timeline } from 'primereact/timeline';

Props Interface:
- value: any[] (required) - Array of events
- align: 'left' | 'right' | 'alternate' | 'top' | 'bottom' (optional) - Content alignment (default: 'left')
- layout: 'vertical' | 'horizontal' (optional) - Timeline orientation (default: 'vertical')
- dataKey: string (optional) - Unique identifier field
- opposite: (item: any) => React.ReactNode (optional) - Opposite content template
- marker: (item: any) => React.ReactNode (optional) - Marker template
- content: (item: any) => React.ReactNode (optional) - Content template
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Array of event objects
- align: Enum (content position relative to timeline)
- layout: Enum (vertical or horizontal timeline)

Child Components: NONE (uses templates)

Usage Example:
const events = [
  {status: 'Ordered', date: '15/10/2020', icon: 'pi pi-shopping-cart'},
  {status: 'Processing', date: '15/10/2020', icon: 'pi pi-cog'},
  {status: 'Shipped', date: '16/10/2020', icon: 'pi pi-truck'},
  {status: 'Delivered', date: '17/10/2020', icon: 'pi pi-check'}
];

<TimelineWrapper 
  value={events}
  content={(item) => <div>{item.status}</div>}
  opposite={(item) => <small>{item.date}</small>}
  marker={(item) => <i className={item.icon}></i>}
/>
```

### 7.6 TreeTable Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact TreeTable with the following specifications:

Component Name: TreeTableWrapper
Import: import { TreeTable } from 'primereact/treetable';
Import: import { Column } from 'primereact/column';

Props Interface:
- value: TreeNode[] (required) - Array of tree nodes
- selectionMode: 'single' | 'multiple' | 'checkbox' (optional) - Selection mode
- selectionKeys: any (optional) - Selected node keys
- onSelectionChange: (e: {value: any}) => void (optional) - Selection callback
- expandedKeys: any (optional) - Expanded node keys
- onToggle: (e: {value: any}) => void (optional) - Toggle callback
- paginator: boolean (optional) - Enable pagination
- rows: number (optional) - Rows per page
- sortMode: 'single' | 'multiple' (optional) - Sort mode
- loading: boolean (optional) - Loading state
- emptyMessage: string (optional) - Message when no data
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - Column components

Data Types:
- value: Array of TreeNode objects with hierarchical structure
- selectionKeys: Object with node keys
- expandedKeys: Object with expanded node keys

Child Components: Column components

Usage Example:
const nodes = [
  {
    key: '0',
    data: {name: 'Applications', size: '200kb', type: 'Folder'},
    children: [
      {key: '0-0', data: {name: 'React', size: '25kb', type: 'Application'}}
    ]
  }
];

<TreeTableWrapper value={nodes}>
  <Column field="name" header="Name" expander />
  <Column field="size" header="Size" />
  <Column field="type" header="Type" />
</TreeTableWrapper>
```

### 7.7 VirtualScroller Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact VirtualScroller with the following specifications:

Component Name: VirtualScrollerWrapper
Import: import { VirtualScroller } from 'primereact/virtualscroller';

Props Interface:
- items: any[] (required) - Array of items
- itemSize: number | number[] (required) - Height of item(s) in pixels
- itemTemplate: (item: any, options: any) => React.ReactNode (required) - Item template
- orientation: 'vertical' | 'horizontal' | 'both' (optional) - Scroll orientation (default: 'vertical')
- numToleratedItems: number (optional) - Number of items to render outside viewport
- delay: number (optional) - Delay in ms before loading (default: 0)
- lazy: boolean (optional) - Enable lazy loading
- onLazyLoad: (e: {first: number, last: number}) => void (optional) - Lazy load callback
- showLoader: boolean (optional) - Show loading indicator
- loading: boolean (optional) - Loading state
- loadingTemplate: React.ReactNode (optional) - Custom loading template
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- items: Array of any objects
- itemSize: Number (fixed height) or Array (variable heights)
- orientation: Enum (scroll direction)

Child Components: NONE (uses itemTemplate)

Usage Example:
<VirtualScrollerWrapper 
  items={items}
  itemSize={50}
  itemTemplate={(item) => <div className="p-3">{item.name}</div>}
  style={{height: '400px'}}
/>

<VirtualScrollerWrapper 
  items={lazyItems}
  itemSize={100}
  itemTemplate={(item) => <Card>{item.content}</Card>}
  lazy
  onLazyLoad={loadLazyData}
  loading={loading}
/>
```

### 7.8 Paginator Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Paginator with the following specifications:

Component Name: PaginatorWrapper
Import: import { Paginator } from 'primereact/paginator';

Props Interface:
- first: number (required) - Index of first record
- rows: number (required) - Number of rows per page
- totalRecords: number (required) - Total number of records
- onPageChange: (e: {first: number, rows: number, page: number, pageCount: number}) => void (required) - Page change callback
- rowsPerPageOptions: number[] (optional) - Page size options
- template: string (optional) - Template string for layout
- leftContent: React.ReactNode (optional) - Left side content
- rightContent: React.ReactNode (optional) - Right side content
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- first: Number (0-based index)
- rows: Number (page size)
- totalRecords: Number (total items)
- template: String (e.g., 'FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink')

Child Components: NONE

Usage Example:
<PaginatorWrapper 
  first={first}
  rows={rows}
  totalRecords={totalRecords}
  onPageChange={(e) => {
    setFirst(e.first);
    setRows(e.rows);
  }}
  rowsPerPageOptions={[10, 20, 30]}
/>
```

---

## ADDITIONAL PANEL COMPONENTS

### 8.1 Fieldset Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Fieldset with the following specifications:

Component Name: FieldsetWrapper
Import: import { Fieldset } from 'primereact/fieldset';

Props Interface:
- legend: string | React.ReactNode (optional) - Fieldset legend
- toggleable: boolean (optional) - Enable collapse/expand
- collapsed: boolean (optional) - Collapsed state
- onToggle: (e: {value: boolean}) => void (optional) - Toggle callback
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - Fieldset content

Data Types:
- legend: String or React element (fieldset title)
- toggleable: Boolean (enables collapse functionality)
- collapsed: Boolean (controlled collapse state)

Child Components: Any content

Usage Example:
<FieldsetWrapper legend="User Information">
  <div className="field">
    <label>Name</label>
    <InputText />
  </div>
  <div className="field">
    <label>Email</label>
    <InputText />
  </div>
</FieldsetWrapper>

<FieldsetWrapper legend="Advanced Options" toggleable collapsed>
  <p>Advanced settings content</p>
</FieldsetWrapper>
```

### 8.2 ScrollPanel Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact ScrollPanel with the following specifications:

Component Name: ScrollPanelWrapper
Import: import { ScrollPanel } from 'primereact/scrollpanel';

Props Interface:
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - Scrollable content

Data Types:
- No specific data types (container component)

Child Components: Any content

Usage Example:
<ScrollPanelWrapper style={{width: '100%', height: '200px'}}>
  <div style={{padding: '1rem', lineHeight: '1.5'}}>
    <p>Long content that needs scrolling...</p>
    <p>More content...</p>
  </div>
</ScrollPanelWrapper>
```

### 8.3 Splitter Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Splitter with the following specifications:

Component Name: SplitterWrapper
Import: import { Splitter, SplitterPanel } from 'primereact/splitter';

Props Interface:
- layout: 'horizontal' | 'vertical' (optional) - Splitter orientation (default: 'horizontal')
- gutterSize: number (optional) - Size of gutter in pixels (default: 4)
- stateKey: string (optional) - Storage key for saving state
- stateStorage: 'session' | 'local' (optional) - Storage type (default: 'session')
- onResizeEnd: (e: {sizes: number[]}) => void (optional) - Resize end callback
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - SplitterPanel components

Data Types:
- layout: Enum (horizontal or vertical split)
- gutterSize: Number (pixels)
- stateKey: String (localStorage/sessionStorage key)

Child Components: SplitterPanel components

SplitterPanel Props:
- size: number (optional) - Panel size percentage
- minSize: number (optional) - Minimum size percentage
- className: string (optional)
- style: React.CSSProperties (optional)

Usage Example:
<SplitterWrapper style={{height: '300px'}}>
  <SplitterPanel size={30} minSize={10}>
    <div>Left Panel</div>
  </SplitterPanel>
  <SplitterPanel size={70}>
    <div>Right Panel</div>
  </SplitterPanel>
</SplitterWrapper>

<SplitterWrapper layout="vertical">
  <SplitterPanel>Top Panel</SplitterPanel>
  <SplitterPanel>Bottom Panel</SplitterPanel>
</SplitterWrapper>
```

### 8.4 Stepper Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Stepper with the following specifications:

Component Name: StepperWrapper
Import: import { Stepper, StepperPanel } from 'primereact/stepper';

Props Interface:
- activeStep: number (optional) - Active step index (controlled)
- linear: boolean (optional) - Linear navigation mode
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - StepperPanel components

Data Types:
- activeStep: Number (0-based step index)
- linear: Boolean (enforces sequential navigation)

Child Components: StepperPanel components

StepperPanel Props:
- header: string | React.ReactNode - Step header

Usage Example:
<StepperWrapper activeStep={activeStep}>
  <StepperPanel header="Personal Info">
    <div className="field">
      <label>Name</label>
      <InputText />
    </div>
    <Button label="Next" onClick={() => setActiveStep(1)} />
  </StepperPanel>
  <StepperPanel header="Address">
    <div className="field">
      <label>Street</label>
      <InputText />
    </div>
    <Button label="Back" onClick={() => setActiveStep(0)} />
    <Button label="Next" onClick={() => setActiveStep(2)} />
  </StepperPanel>
  <StepperPanel header="Confirmation">
    <p>Review your information</p>
    <Button label="Submit" />
  </StepperPanel>
</StepperWrapper>
```

### 8.5 DeferredContent Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact DeferredContent with the following specifications:

Component Name: DeferredContentWrapper
Import: import { DeferredContent } from 'primereact/deferredcontent';

Props Interface:
- onLoad: (e: Event) => void (optional) - Load callback when content becomes visible
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - Deferred content

Data Types:
- onLoad: Function (called when content enters viewport)

Child Components: Any content (loaded lazily)

Usage Example:
<DeferredContentWrapper onLoad={() => console.log('Content loaded')}>
  <DataTable value={largeDataset} />
</DeferredContentWrapper>

<DeferredContentWrapper>
  <img src="large-image.jpg" alt="Lazy loaded" />
</DeferredContentWrapper>
```

---

## ADDITIONAL OVERLAY COMPONENTS


### 9.1 ConfirmDialog Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact ConfirmDialog with the following specifications:

Component Name: ConfirmDialogWrapper
Import: import { ConfirmDialog, confirmDialog } from 'primereact/confirmdialog';

Props Interface:
- visible: boolean (optional) - Visibility state
- onHide: () => void (optional) - Hide callback
- message: string | React.ReactNode (optional) - Confirmation message
- header: string (optional) - Dialog header
- icon: string (optional) - Icon class
- accept: () => void (optional) - Accept callback
- reject: () => void (optional) - Reject callback
- acceptLabel: string (optional) - Accept button label (default: 'Yes')
- rejectLabel: string (optional) - Reject button label (default: 'No')
- acceptIcon: string (optional) - Accept button icon
- rejectIcon: string (optional) - Reject button icon
- acceptClassName: string (optional) - Accept button CSS class
- rejectClassName: string (optional) - Reject button CSS class
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- message: String or React element
- accept/reject: Functions (callbacks for user choice)

Child Components: NONE

Usage Example:
// Declarative usage
<ConfirmDialogWrapper 
  visible={visible}
  onHide={() => setVisible(false)}
  message="Are you sure you want to proceed?"
  header="Confirmation"
  icon="pi pi-exclamation-triangle"
  accept={handleAccept}
  reject={handleReject}
/>

// Imperative usage
const confirm = () => {
  confirmDialog({
    message: 'Do you want to delete this record?',
    header: 'Delete Confirmation',
    icon: 'pi pi-info-circle',
    acceptClassName: 'p-button-danger',
    accept: () => deleteRecord(),
    reject: () => console.log('Rejected')
  });
};
```

### 9.2 ConfirmPopup Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact ConfirmPopup with the following specifications:

Component Name: ConfirmPopupWrapper
Import: import { ConfirmPopup, confirmPopup } from 'primereact/confirmpopup';

Props Interface:
- target: HTMLElement (optional) - Target element
- visible: boolean (optional) - Visibility state
- onHide: () => void (optional) - Hide callback
- message: string | React.ReactNode (optional) - Confirmation message
- icon: string (optional) - Icon class
- accept: () => void (optional) - Accept callback
- reject: () => void (optional) - Reject callback
- acceptLabel: string (optional) - Accept button label (default: 'Yes')
- rejectLabel: string (optional) - Reject button label (default: 'No')
- acceptIcon: string (optional) - Accept button icon
- rejectIcon: string (optional) - Reject button icon
- acceptClassName: string (optional) - Accept button CSS class
- rejectClassName: string (optional) - Reject button CSS class
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- target: HTMLElement (element to attach popup to)
- message: String or React element

Child Components: NONE

Usage Example:
const confirm = (event) => {
  confirmPopup({
    target: event.currentTarget,
    message: 'Are you sure you want to proceed?',
    icon: 'pi pi-exclamation-triangle',
    accept: () => handleAccept(),
    reject: () => handleReject()
  });
};

<Button onClick={confirm} label="Delete" />
<ConfirmPopupWrapper />
```

### 9.3 OverlayPanel Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact OverlayPanel with the following specifications:

Component Name: OverlayPanelWrapper
Import: import { OverlayPanel } from 'primereact/overlaypanel';

Props Interface:
- dismissable: boolean (optional) - Close on outside click (default: true)
- showCloseIcon: boolean (optional) - Show close icon
- appendTo: 'body' | HTMLElement (optional) - Append target
- breakpoints: object (optional) - Responsive breakpoints
- onShow: () => void (optional) - Show callback
- onHide: () => void (optional) - Hide callback
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - Panel content

Data Types:
- dismissable: Boolean (click outside to close)
- breakpoints: Object like {'960px': '75vw'}

Child Components: Any content

Usage Example:
const op = useRef(null);

<Button 
  label="Show" 
  onClick={(e) => op.current.toggle(e)} 
/>
<OverlayPanelWrapper ref={op}>
  <div className="p-3">
    <h5>Overlay Content</h5>
    <p>Additional information here</p>
  </div>
</OverlayPanelWrapper>
```

### 9.4 Popover Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Popover with the following specifications:

Component Name: PopoverWrapper
Import: import { Popover } from 'primereact/popover';

Props Interface:
- dismissable: boolean (optional) - Close on outside click (default: true)
- appendTo: 'body' | HTMLElement (optional) - Append target
- breakpoints: object (optional) - Responsive breakpoints
- onShow: () => void (optional) - Show callback
- onHide: () => void (optional) - Hide callback
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - Popover content

Data Types:
- Similar to OverlayPanel but with different styling

Child Components: Any content

Usage Example:
const popover = useRef(null);

<Button 
  label="Info" 
  icon="pi pi-info-circle"
  onClick={(e) => popover.current.toggle(e)} 
/>
<PopoverWrapper ref={popover}>
  <div className="p-3">
    <p>Helpful information</p>
  </div>
</PopoverWrapper>
```

### 9.5 DynamicDialog Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact DynamicDialog with the following specifications:

Component Name: DynamicDialogWrapper
Import: import { DynamicDialog } from 'primereact/dynamicdialog';
Import: import { DialogService } from 'primereact/dialogservice';

Props Interface:
- This component is used via DialogService, not directly instantiated

Usage Pattern:
- Wrap app with DialogService provider
- Use dialogService.show() to open dialogs programmatically

Data Types:
- DialogService.show() accepts:
  - component: React component to render
  - config: Dialog configuration object

Child Components: Any React component passed to show()

Usage Example:
// App.js
import { DialogService } from 'primereact/dialogservice';

<DialogService>
  <App />
</DialogService>

// Component.js
import { useDialog } from 'primereact/dynamicdialog';

const MyComponent = () => {
  const dialogService = useDialog();
  
  const show = () => {
    dialogService.show(ProductDetail, {
      header: 'Product Details',
      width: '50vw',
      modal: true,
      data: { productId: 123 }
    });
  };
  
  return <Button label="Show" onClick={show} />;
};
```

---

## ADDITIONAL MENU COMPONENTS

### 10.1 Breadcrumb Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Breadcrumb with the following specifications:

Component Name: BreadcrumbWrapper
Import: import { Breadcrumb } from 'primereact/breadcrumb';

Props Interface:
- model: MenuItem[] (required) - Array of menu items
- home: MenuItem (optional) - Home item
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- model: Array of MenuItem objects with label, url, icon, command
- home: MenuItem object for home link

Child Components: NONE (uses model prop)

Usage Example:
const items = [
  {label: 'Electronics'},
  {label: 'Computer'},
  {label: 'Accessories'},
  {label: 'Keyboard'}
];

const home = {icon: 'pi pi-home', url: '/'};

<BreadcrumbWrapper model={items} home={home} />
```

### 10.2 ContextMenu Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact ContextMenu with the following specifications:

Component Name: ContextMenuWrapper
Import: import { ContextMenu } from 'primereact/contextmenu';

Props Interface:
- model: MenuItem[] (required) - Array of menu items
- global: boolean (optional) - Attach to document (default: false)
- appendTo: 'body' | HTMLElement (optional) - Append target
- onShow: (e: Event) => void (optional) - Show callback
- onHide: (e: Event) => void (optional) - Hide callback
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- model: Array of MenuItem objects
- global: Boolean (document-level context menu)

Child Components: NONE (uses model prop)

Usage Example:
const cm = useRef(null);

const items = [
  {label: 'View', icon: 'pi pi-eye'},
  {label: 'Delete', icon: 'pi pi-trash'}
];

<ContextMenuWrapper model={items} ref={cm} />
<div onContextMenu={(e) => cm.current.show(e)}>
  Right click here
</div>
```

### 10.3 Menubar Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Menubar with the following specifications:

Component Name: MenubarWrapper
Import: import { Menubar } from 'primereact/menubar';

Props Interface:
- model: MenuItem[] (required) - Array of menu items
- start: React.ReactNode (optional) - Left side content
- end: React.ReactNode (optional) - Right side content
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- model: Array of MenuItem objects with nested items for submenus

Child Components: NONE (uses model prop, start/end for custom content)

Usage Example:
const items = [
  {
    label: 'File',
    icon: 'pi pi-file',
    items: [
      {label: 'New', icon: 'pi pi-plus'},
      {label: 'Open', icon: 'pi pi-folder-open'}
    ]
  },
  {
    label: 'Edit',
    icon: 'pi pi-pencil',
    items: [
      {label: 'Copy', icon: 'pi pi-copy'},
      {label: 'Paste', icon: 'pi pi-clipboard'}
    ]
  }
];

<MenubarWrapper 
  model={items}
  start={<img src="logo.png" height="40" />}
  end={<Button label="Logout" />}
/>
```

### 10.4 MegaMenu Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact MegaMenu with the following specifications:

Component Name: MegaMenuWrapper
Import: import { MegaMenu } from 'primereact/megamenu';

Props Interface:
- model: MenuItem[] (required) - Array of menu items
- orientation: 'horizontal' | 'vertical' (optional) - Menu orientation (default: 'horizontal')
- start: React.ReactNode (optional) - Left/top content
- end: React.ReactNode (optional) - Right/bottom content
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- model: Array of MenuItem objects with nested items in 2D array structure
- orientation: Enum (horizontal or vertical menu)

Child Components: NONE (uses model prop)

Usage Example:
const items = [
  {
    label: 'Products',
    icon: 'pi pi-box',
    items: [
      [
        {label: 'Electronics', items: [{label: 'TV'}, {label: 'Phone'}]},
        {label: 'Clothing', items: [{label: 'Shirts'}, {label: 'Pants'}]}
      ]
    ]
  }
];

<MegaMenuWrapper model={items} />
```

### 10.5 PanelMenu Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact PanelMenu with the following specifications:

Component Name: PanelMenuWrapper
Import: import { PanelMenu } from 'primereact/panelmenu';

Props Interface:
- model: MenuItem[] (required) - Array of menu items
- multiple: boolean (optional) - Allow multiple panels open (default: false)
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- model: Array of MenuItem objects with nested items
- multiple: Boolean (multiple panels expanded simultaneously)

Child Components: NONE (uses model prop)

Usage Example:
const items = [
  {
    label: 'File',
    icon: 'pi pi-file',
    items: [
      {label: 'New', icon: 'pi pi-plus'},
      {label: 'Open', icon: 'pi pi-folder-open'}
    ]
  },
  {
    label: 'Edit',
    icon: 'pi pi-pencil',
    items: [
      {label: 'Copy', icon: 'pi pi-copy'},
      {label: 'Paste', icon: 'pi pi-clipboard'}
    ]
  }
];

<PanelMenuWrapper model={items} />
```

### 10.6 SlideMenu Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact SlideMenu with the following specifications:

Component Name: SlideMenuWrapper
Import: import { SlideMenu } from 'primereact/slidemenu';

Props Interface:
- model: MenuItem[] (required) - Array of menu items
- popup: boolean (optional) - Popup mode
- viewportHeight: number (optional) - Height of scrollable area (default: 180)
- menuWidth: number (optional) - Width of menu (default: 190)
- effectDuration: number (optional) - Slide animation duration in ms
- backLabel: string (optional) - Back button label (default: 'Back')
- onShow: () => void (optional) - Show callback (popup mode)
- onHide: () => void (optional) - Hide callback (popup mode)
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- model: Array of MenuItem objects with nested items
- popup: Boolean (overlay mode)

Child Components: NONE (uses model prop)

Usage Example:
const items = [
  {
    label: 'File',
    items: [
      {label: 'New', icon: 'pi pi-plus'},
      {
        label: 'Open',
        items: [
          {label: 'Recent'},
          {label: 'Browse'}
        ]
      }
    ]
  }
];

<SlideMenuWrapper model={items} />

// Popup mode
const menu = useRef(null);
<Button label="Menu" onClick={(e) => menu.current.toggle(e)} />
<SlideMenuWrapper model={items} popup ref={menu} />
```

### 10.7 Steps Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Steps with the following specifications:

Component Name: StepsWrapper
Import: import { Steps } from 'primereact/steps';

Props Interface:
- model: MenuItem[] (required) - Array of step items
- activeIndex: number (optional) - Active step index (default: 0)
- onSelect: (e: {index: number}) => void (optional) - Step select callback
- readOnly: boolean (optional) - Read-only mode (default: true)
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- model: Array of MenuItem objects (typically with label only)
- activeIndex: Number (0-based step index)
- readOnly: Boolean (prevents clicking steps)

Child Components: NONE (uses model prop)

Usage Example:
const items = [
  {label: 'Personal'},
  {label: 'Address'},
  {label: 'Payment'},
  {label: 'Confirmation'}
];

<StepsWrapper 
  model={items}
  activeIndex={activeIndex}
  onSelect={(e) => setActiveIndex(e.index)}
  readOnly={false}
/>
```

### 10.8 TabMenu Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact TabMenu with the following specifications:

Component Name: TabMenuWrapper
Import: import { TabMenu } from 'primereact/tabmenu';

Props Interface:
- model: MenuItem[] (required) - Array of tab items
- activeIndex: number (optional) - Active tab index
- onTabChange: (e: {index: number}) => void (optional) - Tab change callback
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- model: Array of MenuItem objects with label, icon
- activeIndex: Number (0-based tab index)

Child Components: NONE (uses model prop)

Usage Example:
const items = [
  {label: 'Home', icon: 'pi pi-home'},
  {label: 'Calendar', icon: 'pi pi-calendar'},
  {label: 'Settings', icon: 'pi pi-cog'}
];

<TabMenuWrapper 
  model={items}
  activeIndex={activeIndex}
  onTabChange={(e) => setActiveIndex(e.index)}
/>
```

### 10.9 TieredMenu Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact TieredMenu with the following specifications:

Component Name: TieredMenuWrapper
Import: import { TieredMenu } from 'primereact/tieredmenu';

Props Interface:
- model: MenuItem[] (required) - Array of menu items
- popup: boolean (optional) - Popup mode
- appendTo: 'body' | HTMLElement (optional) - Append target
- onShow: () => void (optional) - Show callback (popup mode)
- onHide: () => void (optional) - Hide callback (popup mode)
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- model: Array of MenuItem objects with nested items
- popup: Boolean (overlay mode)

Child Components: NONE (uses model prop)

Usage Example:
const items = [
  {
    label: 'File',
    icon: 'pi pi-file',
    items: [
      {label: 'New', icon: 'pi pi-plus'},
      {
        label: 'Open',
        icon: 'pi pi-folder-open',
        items: [
          {label: 'Recent'},
          {label: 'Browse'}
        ]
      }
    ]
  }
];

<TieredMenuWrapper model={items} />

// Popup mode
const menu = useRef(null);
<Button label="Menu" onClick={(e) => menu.current.toggle(e)} />
<TieredMenuWrapper model={items} popup ref={menu} />
```

### 10.10 Dock Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Dock with the following specifications:

Component Name: DockWrapper
Import: import { Dock } from 'primereact/dock';

Props Interface:
- model: MenuItem[] (required) - Array of dock items
- position: 'bottom' | 'top' | 'left' | 'right' (optional) - Dock position (default: 'bottom')
- magnification: boolean (optional) - Enable magnification effect (default: true)
- header: React.ReactNode (optional) - Header content
- footer: React.ReactNode (optional) - Footer content
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- model: Array of MenuItem objects with icon, label, command
- position: Enum (dock placement)
- magnification: Boolean (macOS-style zoom effect)

Child Components: NONE (uses model prop)

Usage Example:
const items = [
  {
    label: 'Finder',
    icon: () => <img src="finder.svg" alt="Finder" width="100%" />,
    command: () => console.log('Finder')
  },
  {
    label: 'App Store',
    icon: () => <img src="appstore.svg" alt="App Store" width="100%" />,
    command: () => console.log('App Store')
  }
];

<DockWrapper 
  model={items}
  position="bottom"
/>
```

---

## ADDITIONAL MEDIA COMPONENTS


### 11.1 Carousel Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Carousel with the following specifications:

Component Name: CarouselWrapper
Import: import { Carousel } from 'primereact/carousel';

Props Interface:
- value: any[] (required) - Array of items
- page: number (optional) - Active page index
- header: React.ReactNode (optional) - Header content
- footer: React.ReactNode (optional) - Footer content
- itemTemplate: (item: any) => React.ReactNode (required) - Item template
- numVisible: number (optional) - Number of visible items (default: 1)
- numScroll: number (optional) - Number of items to scroll (default: 1)
- responsiveOptions: object[] (optional) - Responsive breakpoint options
- orientation: 'horizontal' | 'vertical' (optional) - Carousel orientation (default: 'horizontal')
- verticalViewPortHeight: string (optional) - Height for vertical mode (default: '300px')
- autoplayInterval: number (optional) - Autoplay interval in ms (0 = disabled)
- circular: boolean (optional) - Infinite loop (default: false)
- showNavigators: boolean (optional) - Show prev/next buttons (default: true)
- showIndicators: boolean (optional) - Show page indicators (default: true)
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Array of any objects
- responsiveOptions: Array like [{breakpoint: '1024px', numVisible: 3, numScroll: 3}]
- autoplayInterval: Number (milliseconds, 0 to disable)

Child Components: NONE (uses itemTemplate)

Usage Example:
const products = [{name: 'Product 1', image: 'p1.jpg'}, ...];

const itemTemplate = (product) => {
  return (
    <div className="p-4">
      <img src={product.image} alt={product.name} />
      <h4>{product.name}</h4>
    </div>
  );
};

const responsiveOptions = [
  {breakpoint: '1024px', numVisible: 3, numScroll: 3},
  {breakpoint: '768px', numVisible: 2, numScroll: 2},
  {breakpoint: '560px', numVisible: 1, numScroll: 1}
];

<CarouselWrapper 
  value={products}
  itemTemplate={itemTemplate}
  numVisible={3}
  numScroll={1}
  responsiveOptions={responsiveOptions}
  circular
  autoplayInterval={3000}
/>
```

### 11.2 Galleria Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Galleria with the following specifications:

Component Name: GalleriaWrapper
Import: import { Galleria } from 'primereact/galleria';

Props Interface:
- value: any[] (required) - Array of images
- activeIndex: number (optional) - Active image index
- onItemChange: (e: {index: number}) => void (optional) - Item change callback
- fullScreen: boolean (optional) - Full screen mode
- visible: boolean (optional) - Visibility (fullScreen mode)
- onHide: () => void (optional) - Hide callback (fullScreen mode)
- numVisible: number (optional) - Number of visible thumbnails (default: 3)
- responsiveOptions: object[] (optional) - Responsive options
- showItemNavigators: boolean (optional) - Show prev/next buttons (default: false)
- showThumbnailNavigators: boolean (optional) - Show thumbnail nav (default: true)
- showItemNavigatorsOnHover: boolean (optional) - Show nav on hover (default: false)
- changeItemOnIndicatorHover: boolean (optional) - Change on indicator hover (default: false)
- circular: boolean (optional) - Infinite loop (default: false)
- autoPlay: boolean (optional) - Auto play (default: false)
- transitionInterval: number (optional) - Transition interval in ms (default: 4000)
- showThumbnails: boolean (optional) - Show thumbnails (default: true)
- thumbnailsPosition: 'bottom' | 'top' | 'left' | 'right' (optional) - Thumbnail position (default: 'bottom')
- showIndicators: boolean (optional) - Show indicators (default: false)
- indicatorsPosition: 'bottom' | 'top' | 'left' | 'right' (optional) - Indicator position
- item: (item: any) => React.ReactNode (optional) - Item template
- thumbnail: (item: any) => React.ReactNode (optional) - Thumbnail template
- caption: (item: any) => React.ReactNode (optional) - Caption template
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Array of objects with image data
- responsiveOptions: Array of breakpoint configurations
- transitionInterval: Number (milliseconds)

Child Components: NONE (uses templates)

Usage Example:
const images = [
  {itemImageSrc: 'photo1.jpg', thumbnailImageSrc: 'photo1-small.jpg', alt: 'Photo 1'},
  {itemImageSrc: 'photo2.jpg', thumbnailImageSrc: 'photo2-small.jpg', alt: 'Photo 2'}
];

const itemTemplate = (item) => {
  return <img src={item.itemImageSrc} alt={item.alt} style={{width: '100%'}} />;
};

const thumbnailTemplate = (item) => {
  return <img src={item.thumbnailImageSrc} alt={item.alt} />;
};

<GalleriaWrapper 
  value={images}
  item={itemTemplate}
  thumbnail={thumbnailTemplate}
  numVisible={5}
  circular
  autoPlay
  transitionInterval={3000}
/>

// Full screen mode
<GalleriaWrapper 
  value={images}
  item={itemTemplate}
  thumbnail={thumbnailTemplate}
  fullScreen
  visible={visible}
  onHide={() => setVisible(false)}
/>
```

---

## ADDITIONAL MISC COMPONENTS

### 12.1 AvatarGroup Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact AvatarGroup with the following specifications:

Component Name: AvatarGroupWrapper
Import: import { AvatarGroup } from 'primereact/avatargroup';
Import: import { Avatar } from 'primereact/avatar';

Props Interface:
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - Avatar components

Data Types:
- children: Multiple Avatar components

Child Components: Avatar components

Usage Example:
<AvatarGroupWrapper>
  <Avatar image="user1.jpg" size="large" shape="circle" />
  <Avatar image="user2.jpg" size="large" shape="circle" />
  <Avatar image="user3.jpg" size="large" shape="circle" />
  <Avatar label="+2" size="large" shape="circle" />
</AvatarGroupWrapper>
```

### 12.2 BlockUI Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact BlockUI with the following specifications:

Component Name: BlockUIWrapper
Import: import { BlockUI } from 'primereact/blockui';

Props Interface:
- blocked: boolean (required) - Blocked state
- fullScreen: boolean (optional) - Block entire screen
- template: React.ReactNode (optional) - Custom blocked content template
- onBlocked: () => void (optional) - Blocked callback
- onUnblocked: () => void (optional) - Unblocked callback
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - Content to block

Data Types:
- blocked: Boolean (controls blocking state)
- fullScreen: Boolean (blocks entire viewport)
- template: React element (custom blocking overlay)

Child Components: Any content to be blocked

Usage Example:
<BlockUIWrapper blocked={loading}>
  <Panel header="Content">
    <p>This content will be blocked when loading</p>
  </Panel>
</BlockUIWrapper>

<BlockUIWrapper 
  blocked={processing}
  template={<ProgressSpinner />}
>
  <DataTable value={data} />
</BlockUIWrapper>

<BlockUIWrapper blocked={fullScreenLoading} fullScreen>
  <div>App content</div>
</BlockUIWrapper>
```

### 12.3 Inplace Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Inplace with the following specifications:

Component Name: InplaceWrapper
Import: import { Inplace, InplaceDisplay, InplaceContent } from 'primereact/inplace';

Props Interface:
- active: boolean (optional) - Active state (controlled)
- onToggle: (e: {value: boolean}) => void (optional) - Toggle callback
- closable: boolean (optional) - Show close button
- disabled: boolean (optional) - Disabled state
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - InplaceDisplay and InplaceContent

Data Types:
- active: Boolean (edit mode state)
- closable: Boolean (allows closing edit mode)

Child Components: InplaceDisplay and InplaceContent components

Usage Example:
<InplaceWrapper closable>
  <InplaceDisplay>
    {text || 'Click to Edit'}
  </InplaceDisplay>
  <InplaceContent>
    <InputText 
      value={text}
      onChange={(e) => setText(e.target.value)}
      autoFocus
    />
  </InplaceContent>
</InplaceWrapper>
```

### 12.4 MeterGroup Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact MeterGroup with the following specifications:

Component Name: MeterGroupWrapper
Import: import { MeterGroup } from 'primereact/metergroup';

Props Interface:
- value: object[] (required) - Array of meter values
- min: number (optional) - Minimum value (default: 0)
- max: number (optional) - Maximum value (default: 100)
- orientation: 'horizontal' | 'vertical' (optional) - Orientation (default: 'horizontal')
- labelPosition: 'start' | 'end' (optional) - Label position (default: 'end')
- start: React.ReactNode (optional) - Start content
- end: React.ReactNode (optional) - End content
- meter: (value: any) => React.ReactNode (optional) - Custom meter template
- labelList: (value: any[]) => React.ReactNode (optional) - Custom label list template
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- value: Array of objects like [{label: 'Apps', value: 24, color: '#34d399'}]
- orientation: Enum (horizontal or vertical meters)

Child Components: NONE (uses value prop and templates)

Usage Example:
const values = [
  {label: 'Apps', value: 24, color: '#34d399'},
  {label: 'Messages', value: 16, color: '#fbbf24'},
  {label: 'Media', value: 24, color: '#60a5fa'},
  {label: 'System', value: 12, color: '#c084fc'}
];

<MeterGroupWrapper value={values} />

<MeterGroupWrapper 
  value={values}
  orientation="vertical"
  labelPosition="start"
/>
```

### 12.5 Terminal Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Terminal with the following specifications:

Component Name: TerminalWrapper
Import: import { Terminal } from 'primereact/terminal';
Import: import { TerminalService } from 'primereact/terminalservice';

Props Interface:
- welcomeMessage: string (optional) - Welcome message
- prompt: string (optional) - Command prompt (default: '$')
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Data Types:
- welcomeMessage: String (initial message)
- prompt: String (command line prompt)

Usage Pattern:
- Use TerminalService to handle commands

Child Components: NONE

Usage Example:
useEffect(() => {
  TerminalService.on('command', (command) => {
    let response;
    switch(command) {
      case 'date':
        response = new Date().toDateString();
        break;
      case 'greet':
        response = 'Hello World!';
        break;
      default:
        response = 'Unknown command: ' + command;
    }
    TerminalService.emit('response', response);
  });
  
  return () => TerminalService.off('command');
}, []);

<TerminalWrapper 
  welcomeMessage="Welcome to PrimeReact Terminal"
  prompt="primereact $"
/>
```

---

## ADDITIONAL MESSAGES COMPONENTS

### 13.1 Messages Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Messages with the following specifications:

Component Name: MessagesWrapper
Import: import { Messages } from 'primereact/messages';

Props Interface:
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Usage Pattern:
- Use ref to call show() method programmatically

Data Types:
- show() accepts: {severity, summary, detail, life, sticky, closable}

Child Components: NONE

Usage Example:
const msgs = useRef(null);

const showSuccess = () => {
  msgs.current.show({
    severity: 'success',
    summary: 'Success',
    detail: 'Message sent successfully',
    life: 3000
  });
};

const showMultiple = () => {
  msgs.current.show([
    {severity: 'info', summary: 'Info', detail: 'Info message'},
    {severity: 'warn', summary: 'Warning', detail: 'Warning message'}
  ]);
};

<MessagesWrapper ref={msgs} />
<Button label="Show" onClick={showSuccess} />
```

### 13.2 Toast Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Toast with the following specifications:

Component Name: ToastWrapper
Import: import { Toast } from 'primereact/toast';

Props Interface:
- position: 'top-left' | 'top-center' | 'top-right' | 'bottom-left' | 'bottom-center' | 'bottom-right' | 'center' (optional) - Toast position (default: 'top-right')
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles

Usage Pattern:
- Use ref to call show() method programmatically

Data Types:
- show() accepts: {severity, summary, detail, life, sticky, closable}
- severity: 'success' | 'info' | 'warn' | 'error'

Child Components: NONE

Usage Example:
const toast = useRef(null);

const showSuccess = () => {
  toast.current.show({
    severity: 'success',
    summary: 'Success',
    detail: 'Operation completed',
    life: 3000
  });
};

const showMultiple = () => {
  toast.current.show([
    {severity: 'info', summary: 'Info', detail: 'Info message'},
    {severity: 'warn', summary: 'Warning', detail: 'Warning message'},
    {severity: 'error', summary: 'Error', detail: 'Error message'}
  ]);
};

<ToastWrapper ref={toast} position="top-right" />
<Button label="Show" onClick={showSuccess} />
```

---

## UTILITY COMPONENTS

### 14.1 FocusTrap Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact FocusTrap with the following specifications:

Component Name: FocusTrapWrapper
Import: import { FocusTrap } from 'primereact/focustrap';

Props Interface:
- disabled: boolean (optional) - Disable focus trap
- className: string (optional) - Additional CSS classes
- style: React.CSSProperties (optional) - Inline styles
- children: React.ReactNode (required) - Content to trap focus within

Data Types:
- disabled: Boolean (enables/disables trap)

Child Components: Any content (typically modal dialogs)

Usage Example:
<FocusTrapWrapper>
  <Dialog visible={visible} onHide={() => setVisible(false)}>
    <InputText />
    <Button label="Submit" />
  </Dialog>
</FocusTrapWrapper>
```

### 14.2 Portal Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Portal with the following specifications:

Component Name: PortalWrapper
Import: import { Portal } from 'primereact/portal';

Props Interface:
- element: HTMLElement (optional) - Target element (default: document.body)
- appendTo: 'self' | HTMLElement (optional) - Append target
- visible: boolean (optional) - Visibility state
- onMounted: (el: HTMLElement) => void (optional) - Mounted callback
- onUnmounted: (el: HTMLElement) => void (optional) - Unmounted callback
- children: React.ReactNode (required) - Content to portal

Data Types:
- element: HTMLElement (DOM element to render into)
- appendTo: String or HTMLElement

Child Components: Any content

Usage Example:
<PortalWrapper>
  <div className="custom-overlay">
    <p>This content is rendered in document.body</p>
  </div>
</PortalWrapper>

<PortalWrapper element={document.getElementById('portal-target')}>
  <div>Content rendered in specific element</div>
</PortalWrapper>
```

### 14.3 Ripple Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact Ripple with the following specifications:

Component Name: RippleWrapper
Import: import { Ripple } from 'primereact/ripple';

Props Interface:
- No props (self-contained effect)

Usage Pattern:
- Add Ripple component inside clickable elements
- Requires PrimeReact CSS

Data Types:
- No data types (visual effect only)

Child Components: NONE

Usage Example:
<div className="p-ripple" style={{position: 'relative'}}>
  <Button label="Click Me" />
  <RippleWrapper />
</div>

// Or use with custom elements
<div className="custom-button p-ripple" style={{position: 'relative'}}>
  Click Me
  <RippleWrapper />
</div>
```

### 14.4 StyleClass Component

**Prompt:**
```
Generate a React wrapper component for PrimeReact StyleClass with the following specifications:

Component Name: StyleClassWrapper
Import: import { StyleClass } from 'primereact/styleclass';

Props Interface:
- nodeRef: React.RefObject (required) - Reference to trigger element
- selector: string (required) - Target element selector
- enterClassName: string (optional) - Class to add on enter
- enterActiveClassName: string (optional) - Active class during enter
- leaveClassName: string (optional) - Class to add on leave
- leaveActiveClassName: string (optional) - Active class during leave
- hideOnOutsideClick: boolean (optional) - Hide on outside click
- toggleClassName: string (optional) - Class to toggle

Data Types:
- selector: String (CSS selector for target)
- enterClassName/leaveClassName: String (animation classes)

Child Components: NONE

Usage Example:
const btnRef = useRef(null);

<Button 
  ref={btnRef}
  label="Toggle"
  className="p-button-text"
/>
<StyleClassWrapper 
  nodeRef={btnRef}
  selector="#menu"
  enterClassName="hidden"
  leaveToClassName="hidden"
  hideOnOutsideClick
/>
<div id="menu" className="hidden">
  <ul>
    <li>Item 1</li>
    <li>Item 2</li>
  </ul>
</div>
```

---

## SUMMARY

**Total Component Prompts: 90+**

This comprehensive document now includes wrapper generation prompts for all major PrimeReact components organized by:

1. **Level 1 (No Children)**: 10 components
2. **Level 2 (Simple Children)**: 8 components
3. **Level 3 (Complex Children)**: 10 components
4. **Form Components**: 20 components
5. **Button Components**: 3 components
6. **Data Components**: 8 components
7. **Panel Components**: 5 components
8. **Overlay Components**: 5 components
9. **Menu Components**: 10 components
10. **Media Components**: 2 components
11. **Misc Components**: 5 components
12. **Messages Components**: 2 components
13. **Utility Components**: 4 components

Each prompt includes:
- Complete props interface with TypeScript types
- Data type specifications
- Child component requirements
- Practical usage examples
- Multiple usage patterns where applicable

**Document Version**: 2.0  
**Last Updated**: February 2026  
**Coverage**: 90+ PrimeReact components
