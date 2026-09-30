#!/usr/bin/env python3
"""
Build all component definitions into a single JSON file.
Reads all individual component JSON files and combines them.
"""

import json
import os
from pathlib import Path

def build_component_definitions():
    """Build all component definitions into component_definitions.json"""
    
    # Get the directory containing this script
    script_dir = Path(__file__).parent
    
    # Dictionary to store all component definitions
    all_components = {}
    
    # Get all JSON files except component_definitions.json
    json_files = [f for f in script_dir.glob("*.json") 
                  if f.name != "component_definitions.json"]
    
    print(f"Found {len(json_files)} component JSON files")
    
    # Read each JSON file
    for json_file in sorted(json_files):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                component_data = json.load(f)
                component_name = component_data.get('name')
                
                if component_name:
                    all_components[component_name] = component_data
                    print(f"  ✓ Loaded {component_name}")
                else:
                    print(f"  ✗ Warning: {json_file.name} has no 'name' field")
                    
        except json.JSONDecodeError as e:
            print(f"  ✗ Error parsing {json_file.name}: {e}")
        except Exception as e:
            print(f"  ✗ Error reading {json_file.name}: {e}")
    
    # Write combined definitions
    output_file = script_dir / "component_definitions.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_components, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Successfully built component_definitions.json with {len(all_components)} components")
    
    # Print summary by category
    categories = {}
    for comp_name, comp_data in all_components.items():
        category = comp_data.get('category', 'Unknown')
        if category not in categories:
            categories[category] = []
        categories[category].append(comp_name)
    
    print("\nComponents by category:")
    for category in sorted(categories.keys()):
        print(f"  {category}: {len(categories[category])} components")
        for comp in sorted(categories[category]):
            print(f"    - {comp}")

if __name__ == "__main__":
    build_component_definitions()
