# PrimeReact Wrapper Components

Enhanced React wrapper components for all 98 PrimeReact components with embedded metadata and simplified event handling.

## Features

- **Embedded Component Metadata**: Each wrapper includes the complete JSON definition for runtime introspection
- **Simplified Event Handlers**: Redux-friendly callbacks that pass only the value
- **Validation Hooks**: Built-in validation event handlers
- **Lifecycle Callbacks**: onMount and onUnmount support
- **Full PrimeReact Compatibility**: All original PrimeReact props are supported via spread operator

## Installation

```bash
npm install primereact primeicons
```

## Usage

### Basic Import

```javascript
import { ButtonWrapper } from './prime_react_components';

function App() {
  return (
    <ButtonWrapper 
      label="Click Me" 
      icon="pi pi-check" 
      severity="success"
      onClick={() => console.log('Clicked!')}
    />
  );
}
```

### With Redux Integration

```javascript
import { InputTextWrapper } from './prime_react_components';
import { useDispatch, useSelector } from 'react-redux';
import { setUsername } from './store/userSlice';

function LoginForm() {
  const dispatch = useDispatch();
  const username = useSelector(state => state.user.username);
  
  return (
    <InputTextWrapper
      value={username}
      // Simplified callback - receives just the value
      onValueChange={(value) => dispatch(setUsername(value))}
      placeholder="Enter username"
    />
  );
}
```

### Accessing Component Metadata

Each wrapper exports its metadata for runtime introspection:

```javascript
import { ButtonWrapper, ButtonMetadata } from './prime_react_components';

console.log(ButtonMetadata);
// {
//   name: "Button",
//   category: "Button",
//   metadata: { description: "...", usageExamples: [...] },
//   propsInterface: { componentSpecific: [...], styling: [...] },
//   eventHandlers: { standard: [...], simplified: [...] },
//   ...
// }

// Use metadata to build dynamic forms or documentation
const propsList = ButtonMetadata.propsInterface.componentSpecific;
propsList.forEach(prop => {
  console.log(`${prop.name}: ${prop.description}`);
});
```

### Lifecycle Hooks

```javascript
import { DialogWrapper } from './prime_react_components';

function MyDialog() {
  return (
    <DialogWrapper
      visible={true}
      onMount={() => console.log('Dialog mounted')}
      onUnmount={() => console.log('Dialog unmounted')}
      onHide={() => setVisible(false)}
    >
      <p>Dialog content</p>
    </DialogWrapper>
  );
}
```

### Validation

```javascript
import { InputNumberWrapper } from './prime_react_components';

function PriceInput() {
  return (
    <InputNumberWrapper
      value={price}
      onValueChange={(value) => setPrice(value)}
      onValidate={(value) => value > 0 && value < 1000}
      onError={(value) => console.error('Invalid price:', value)}
    />
  );
}
```

## Component Categories

### Form Components (27)
AutoComplete, Calendar, CascadeSelect, Checkbox, Chips, ColorPicker, Dropdown, Editor, FloatLabel, IconField, InputGroup, InputMask, InputNumber, InputOtp, InputSwitch, InputText, InputTextarea, Knob, Listbox, MultiSelect, Password, RadioButton, Rating, SelectButton, Slider, TreeSelect, TriStateCheckbox

### Button Components (5)
Button, ButtonGroup, SpeedDial, SplitButton, ToggleButton

### Data Components (11)
Column, DataTable, DataView, OrderList, OrganizationChart, Paginator, PickList, Timeline, Tree, TreeTable, VirtualScroller

### Panel Components (9)
Accordion, Card, DeferredContent, Fieldset, Panel, ScrollPanel, Splitter, Stepper, TabView

### Overlay Components (8)
ConfirmDialog, ConfirmPopup, Dialog, DynamicDialog, OverlayPanel, Popover, Sidebar, Tooltip

### Menu Components (11)
Breadcrumb, ContextMenu, Dock, MegaMenu, Menu, Menubar, PanelMenu, SlideMenu, Steps, TabMenu, TieredMenu

### Chart Components (1)
Chart

### Media Components (3)
Carousel, Galleria, Image

### Messages Components (3)
Message, Messages, Toast

### Misc Components (15)
Avatar, AvatarGroup, Badge, BlockUI, Chip, Divider, Inplace, MeterGroup, ProgressBar, ProgressSpinner, ScrollTop, Skeleton, Tag, Terminal, Toolbar

### File Components (1)
FileUpload

### Utility Components (4)
FocusTrap, Portal, Ripple, StyleClass

## Event Handler Types

### Standard Events
Original PrimeReact event handlers with full event object:
```javascript
onChange={(e) => console.log(e.value, e.originalEvent)}
```

### Simplified Events
Redux-friendly handlers that receive only the value:
```javascript
onValueChange={(value) => dispatch(setValue(value))}
```

### Validation Events
```javascript
onValidate={(value) => value.length > 0}
onError={(value) => console.error('Invalid:', value)}
onValid={(value) => console.log('Valid:', value)}
```

### Lifecycle Events
```javascript
onMount={() => console.log('Mounted')}
onUnmount={() => console.log('Unmounted')}
```

## Styling Support

All components support:
- **className**: PrimeFlex utility classes and custom CSS
- **style**: React inline styles
- **PrimeFlex Integration**: Full support for PrimeFlex utility classes

```javascript
<ButtonWrapper
  label="Styled Button"
  className="w-full mb-3 shadow-2"
  style={{ fontSize: '1.2rem' }}
/>
```

## Component Metadata Structure

Each component's metadata includes:

1. **Metadata**: Name, description, usage examples
2. **Props Interface**: Component-specific props, styling props, children info
3. **Event Handlers**: Standard, simplified, validation, lifecycle
4. **Event Handler Methods**: Internal methods and patterns
5. **Child Component Info**: Allowed children, descriptions, examples
6. **Styling Support**: PrimeFlex, responsive, custom CSS support
7. **Usage Examples**: Basic, with styling, events, Redux, validation, children

## Generation

These components were auto-generated from JSON definitions using:

```bash
# Build component definitions
python component_generator/build_all_definitions.py

# Generate wrapper components
python component_generator/generate_wrappers.py
```

## License

MIT - Same as PrimeReact

## Links

- [PrimeReact Documentation](https://primereact.org/)
- [PrimeFlex Documentation](https://primeflex.org/)
- [PrimeIcons](https://primereact.org/icons/)
