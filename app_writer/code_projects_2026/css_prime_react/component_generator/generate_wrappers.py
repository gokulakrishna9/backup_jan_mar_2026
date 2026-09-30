#!/usr/bin/env python3
"""
Generate JavaScript React wrapper components from JSON definitions.
Each wrapper includes the component properties JSON embedded for runtime access.
"""

import json
import os
from pathlib import Path

def generate_wrapper_component(component_data, output_dir):
    """Generate a JavaScript wrapper component from JSON definition"""
    
    name = component_data.get('name')
    import_name = component_data.get('import')
    category = component_data.get('category', 'Unknown')
    
    # Get props interface
    props_interface = component_data.get('propsInterface', {})
    component_specific = props_interface.get('componentSpecific', [])
    styling = props_interface.get('styling', [])
    children_info = props_interface.get('children')
    
    # Get event handlers
    event_handlers = component_data.get('eventHandlers', {})
    standard_events = event_handlers.get('standard', [])
    simplified_events = event_handlers.get('simplified', [])
    validation_events = event_handlers.get('validation', [])
    lifecycle_events = event_handlers.get('lifecycle', [])
    
    # Check if component has children
    child_component_info = component_data.get('childComponentInfo', {})
    has_children = child_component_info.get('hasChildren', False)
    
    # Start building the component file
    lines = []
    
    # File header
    lines.append("/**")
    lines.append(f" * {name}Wrapper - Enhanced wrapper for PrimeReact {name}")
    lines.append(f" * Category: {category}")
    lines.append(f" * ")
    lines.append(f" * {component_data.get('metadata', {}).get('description', '')}")
    lines.append(f" * ")
    lines.append(f" * This wrapper provides:")
    lines.append(f" * - Simplified event handlers for Redux integration")
    lines.append(f" * - Validation hooks")
    lines.append(f" * - Lifecycle callbacks")
    lines.append(f" * - Embedded component metadata for runtime introspection")
    lines.append(f" */")
    lines.append("")
    lines.append("import React, { useEffect, useRef } from 'react';")
    lines.append(f"import {{ {import_name} }} from 'primereact/{import_name.lower()}';")
    lines.append("")
    
    # Embed the component definition as a constant
    lines.append(f"// Component metadata embedded for runtime access")
    lines.append(f"export const {name}Metadata = {json.dumps(component_data, indent=2)};")
    lines.append("")
    
    # Component function
    lines.append(f"const {name}Wrapper = (props) => {{")
    lines.append(f"  const {{")
    
    # List all possible props
    all_props = []
    
    # Add component-specific props
    for prop in component_specific:
        all_props.append(prop['name'])
    
    # Add styling props
    for prop in styling:
        all_props.append(prop['name'])
    
    # Add children if applicable
    if has_children:
        all_props.append('children')
    
    # Add all event handler types
    for event in standard_events:
        all_props.append(event['name'])
    for event in simplified_events:
        all_props.append(event['name'])
    for event in validation_events:
        all_props.append(event['name'])
    for event in lifecycle_events:
        all_props.append(event['name'])
    
    # Add rest props
    lines.append(f"    {', '.join(all_props)},")
    lines.append(f"    ...restProps")
    lines.append(f"  }} = props;")
    lines.append("")
    
    # Add ref if needed
    lines.append(f"  const componentRef = useRef(null);")
    lines.append("")
    
    # Lifecycle: onMount
    if any(e['name'] == 'onMount' for e in lifecycle_events):
        lines.append(f"  // Lifecycle: onMount")
        lines.append(f"  useEffect(() => {{")
        lines.append(f"    if (onMount) {{")
        lines.append(f"      onMount();")
        lines.append(f"    }}")
        lines.append(f"  }}, []);")
        lines.append("")
    
    # Lifecycle: onUnmount
    if any(e['name'] == 'onUnmount' for e in lifecycle_events):
        lines.append(f"  // Lifecycle: onUnmount")
        lines.append(f"  useEffect(() => {{")
        lines.append(f"    return () => {{")
        lines.append(f"      if (onUnmount) {{")
        lines.append(f"        onUnmount();")
        lines.append(f"      }}")
        lines.append(f"    }};")
        lines.append(f"  }}, []);")
        lines.append("")
    
    # Event handler wrappers for simplified callbacks
    for simplified in simplified_events:
        simplified_name = simplified['name']
        # Find corresponding standard event
        standard_name = None
        if 'onChange' in [e['name'] for e in standard_events]:
            standard_name = 'onChange'
        elif 'onSelectionChange' in [e['name'] for e in standard_events]:
            standard_name = 'onSelectionChange'
        
        if standard_name:
            lines.append(f"  // Simplified event handler: {simplified_name}")
            lines.append(f"  const handle{standard_name[2:]} = (e) => {{")
            lines.append(f"    if ({standard_name}) {{")
            lines.append(f"      {standard_name}(e);")
            lines.append(f"    }}")
            lines.append(f"    if ({simplified_name}) {{")
            lines.append(f"      {simplified_name}(e.value || e.data || e);")
            lines.append(f"    }}")
            lines.append(f"  }};")
            lines.append("")
    
    # Build props object for underlying component
    lines.append(f"  // Build props for underlying PrimeReact component")
    lines.append(f"  const primeReactProps = {{")
    
    # Add component-specific props
    for prop in component_specific:
        prop_name = prop['name']
        lines.append(f"    {prop_name},")
    
    # Add styling props
    for prop in styling:
        prop_name = prop['name']
        lines.append(f"    {prop_name},")
    
    # Add standard event handlers (use wrapped versions if simplified exists)
    for event in standard_events:
        event_name = event['name']
        # Check if there's a simplified version
        has_simplified = any(s['name'] for s in simplified_events if 'Change' in event_name)
        if has_simplified and event_name in ['onChange', 'onSelectionChange']:
            lines.append(f"    {event_name}: handle{event_name[2:]},")
        else:
            lines.append(f"    {event_name},")
    
    lines.append(f"    ref: componentRef,")
    lines.append(f"    ...restProps")
    lines.append(f"  }};")
    lines.append("")
    
    # Render component
    lines.append(f"  return (")
    if has_children:
        lines.append(f"    <{import_name} {{...primeReactProps}}>")
        lines.append(f"      {{children}}")
        lines.append(f"    </{import_name}>")
    else:
        lines.append(f"    <{import_name} {{...primeReactProps}} />")
    lines.append(f"  );")
    lines.append(f"}};")
    lines.append("")
    
    # Add display name
    lines.append(f"{name}Wrapper.displayName = '{name}Wrapper';")
    lines.append("")
    
    # Export
    lines.append(f"export default {name}Wrapper;")
    lines.append("")
    
    # Write to file
    output_file = output_dir / f"{name}Wrapper.jsx"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return output_file

def generate_all_wrappers():
    """Generate all wrapper components from JSON definitions"""
    
    # Get directories
    script_dir = Path(__file__).parent
    output_dir = script_dir.parent / "prime_react_components"
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    print(f"Generating wrapper components in: {output_dir}")
    print()
    
    # Get all JSON files except component_definitions.json
    json_files = [f for f in script_dir.glob("*.json") 
                  if f.name != "component_definitions.json"]
    
    print(f"Found {len(json_files)} component JSON files")
    print()
    
    generated_files = []
    
    # Generate wrapper for each component
    for json_file in sorted(json_files):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                component_data = json.load(f)
                component_name = component_data.get('name')
                
                if component_name:
                    output_file = generate_wrapper_component(component_data, output_dir)
                    generated_files.append(output_file)
                    print(f"  ✓ Generated {component_name}Wrapper.jsx")
                else:
                    print(f"  ✗ Warning: {json_file.name} has no 'name' field")
                    
        except json.JSONDecodeError as e:
            print(f"  ✗ Error parsing {json_file.name}: {e}")
        except Exception as e:
            print(f"  ✗ Error processing {json_file.name}: {e}")
    
    print()
    print(f"✓ Successfully generated {len(generated_files)} wrapper components")
    
    # Generate index.js for easy imports
    generate_index_file(generated_files, output_dir)

def generate_index_file(generated_files, output_dir):
    """Generate index.js file that exports all wrappers"""
    
    lines = []
    lines.append("/**")
    lines.append(" * PrimeReact Wrapper Components")
    lines.append(" * Auto-generated index file for all wrapper components")
    lines.append(" */")
    lines.append("")
    
    # Sort files by name
    sorted_files = sorted(generated_files, key=lambda f: f.stem)
    
    # Import statements
    for file in sorted_files:
        component_name = file.stem  # e.g., "ButtonWrapper"
        lines.append(f"export {{ default as {component_name} }} from './{file.stem}';")
        lines.append(f"export {{ {component_name.replace('Wrapper', 'Metadata')} }} from './{file.stem}';")
    
    lines.append("")
    
    # Write index file
    index_file = output_dir / "index.js"
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✓ Generated index.js with {len(sorted_files)} exports")

if __name__ == "__main__":
    generate_all_wrappers()
