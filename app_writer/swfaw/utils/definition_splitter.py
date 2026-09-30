"""Utility to split application_definition.json into multiple files by layer.

This module provides functions to split a large application definition into
smaller, more manageable files organized by layer:
- webflux_project_metadata.json: Project and database configuration
- webflux_entities.json: All table/entity definitions
- webflux_relationships.json: All relationships extracted separately
- webflux_manifest.json: Index file that references all parts
- Layer definition files: Detailed configuration for each layer (webflux_ prefixed)
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from models.database_definition import DatabaseDefinition
from utils.layer_definition_generator import generate_all_layer_definitions
from version import MANIFEST_VERSION, SUPPORTED_MANIFEST_VERSIONS


def split_definition(db_def: DatabaseDefinition, output_dir: str) -> Dict[str, str]:
    """Split application definition into multiple files by layer.
    
    Args:
        db_def: The complete database definition
        output_dir: Output directory for the application
        
    Returns:
        Dictionary mapping file types to their paths
    """
    output_path = Path(output_dir)
    definitions_dir = output_path / 'application_definitions'
    definitions_dir.mkdir(parents=True, exist_ok=True)
    
    file_paths = {}
    
    # 1. Project Metadata (project + database config)
    project_metadata = {
        'projectMetadata': db_def.projectMetadata.model_dump()
    }
    metadata_file = definitions_dir / 'webflux_project_metadata.json'
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(project_metadata, f, indent=2, ensure_ascii=False)
    file_paths['project_metadata'] = str(metadata_file)
    
    # 2. Entities (tables without relationships)
    entities = []
    for table in db_def.tables:
        entity = {
            'name': table.name,
            'columns': [col.model_dump() for col in table.columns]
        }
        entities.append(entity)
    
    entities_data = {'entities': entities}
    entities_file = definitions_dir / 'webflux_entities.json'
    with open(entities_file, 'w', encoding='utf-8') as f:
        json.dump(entities_data, f, indent=2, ensure_ascii=False)
    file_paths['entities'] = str(entities_file)
    
    # 3. Relationships (extracted separately for clarity)
    relationships = []
    for table in db_def.tables:
        if table.relationships:
            for rel in table.relationships:
                relationship = {
                    'sourceTable': table.name,
                    'type': rel.type,
                    'targetTable': rel.targetTable,
                    'foreignKey': rel.foreignKey,
                    'joinTable': rel.joinTable
                }
                relationships.append(relationship)
    
    relationships_data = {'relationships': relationships}
    relationships_file = definitions_dir / 'webflux_relationships.json'
    with open(relationships_file, 'w', encoding='utf-8') as f:
        json.dump(relationships_data, f, indent=2, ensure_ascii=False)
    file_paths['relationships'] = str(relationships_file)
    
    # 4. Generate layer definition files (NEW)
    print("\n>> Generating layer definition files...")
    layer_files = generate_all_layer_definitions(db_def, output_dir)
    file_paths.update(layer_files)
    
    # 5. Manifest (index file)
    manifest = {
        'version': MANIFEST_VERSION,
        'format': 'split',
        'description': 'Application definition split into multiple files by layer',
        'files': {
            'project_metadata': 'webflux_project_metadata.json',
            'entities': 'webflux_entities.json',
            'relationships': 'webflux_relationships.json',
            'entity_layer': 'webflux_entity_layer.json',
            'repository_layer': 'webflux_repository_layer.json',
            'service_layer': 'webflux_service_layer.json',
            'controller_layer': 'webflux_controller_layer.json',
            'dto_layer': 'webflux_dto_layer.json',
            'query_layer': 'webflux_query_layer.json',
            'filter_layer': 'webflux_filter_layer.json',
            'group_definition_layer': 'webflux_group_definition_layer.json'
        },
        'statistics': {
            'total_entities': len(entities),
            'total_relationships': len(relationships),
            'total_columns': sum(len(e['columns']) for e in entities)
        }
    }
    manifest_file = definitions_dir / 'webflux_manifest.json'
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    file_paths['manifest'] = str(manifest_file)
    
    return file_paths


def load_split_definition(output_dir: str) -> DatabaseDefinition:
    """Load application definition from split files.
    
    Args:
        output_dir: Output directory containing application_definitions folder
        
    Returns:
        Complete DatabaseDefinition object
    """
    output_path = Path(output_dir)
    definitions_dir = output_path / 'application_definitions'
    
    if not definitions_dir.exists():
        raise FileNotFoundError(f"Definitions directory not found: {definitions_dir}")
    
    # Load manifest
    manifest_file = definitions_dir / 'webflux_manifest.json'
    if not manifest_file.exists():
        raise FileNotFoundError(f"Manifest file not found: {manifest_file}")
    
    with open(manifest_file, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    # Load project metadata
    metadata_file = definitions_dir / manifest['files']['project_metadata']
    with open(metadata_file, 'r', encoding='utf-8') as f:
        project_data = json.load(f)
    
    # Load entities
    entities_file = definitions_dir / manifest['files']['entities']
    with open(entities_file, 'r', encoding='utf-8') as f:
        entities_data = json.load(f)
    
    # Load relationships
    relationships_file = definitions_dir / manifest['files']['relationships']
    with open(relationships_file, 'r', encoding='utf-8') as f:
        relationships_data = json.load(f)
    
    # Reconstruct tables with relationships
    tables = []
    for entity in entities_data['entities']:
        # Find relationships for this entity
        entity_relationships = [
            rel for rel in relationships_data['relationships']
            if rel['sourceTable'] == entity['name']
        ]
        
        table = {
            'name': entity['name'],
            'columns': entity['columns'],
            'relationships': entity_relationships
        }
        tables.append(table)
    
    # Reconstruct complete definition
    complete_definition = {
        'projectMetadata': project_data['projectMetadata'],
        'tables': tables
    }
    
    return DatabaseDefinition(**complete_definition)


def load_layer_definitions_if_exist(output_dir: str) -> Dict[str, Any]:
    """Load layer definition files if they exist.
    
    Args:
        output_dir: Output directory containing application_definitions folder
        
    Returns:
        Dictionary with layer definitions, or None if files don't exist
        {
            'entity_layer': {...},
            'repository_layer': {...},
            'service_layer': {...},
            'controller_layer': {...},
            'dto_layer': {...}
        }
    """
    output_path = Path(output_dir)
    definitions_dir = output_path / 'application_definitions'
    
    if not definitions_dir.exists():
        return None
    
    # Check if manifest exists and has layer definition files
    manifest_file = definitions_dir / 'webflux_manifest.json'
    if not manifest_file.exists():
        return None
    
    with open(manifest_file, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    
    # Check if this is a v2.3+ manifest with layer definitions
    if manifest.get('version') not in SUPPORTED_MANIFEST_VERSIONS:
        return None
    
    # Check if layer definition files are listed in manifest
    layer_files = ['entity_layer', 'repository_layer', 'service_layer', 'controller_layer', 'dto_layer']
    if not all(layer in manifest.get('files', {}) for layer in layer_files):
        return None
    
    # Load all layer definition files
    layer_definitions = {}
    
    for layer_name in layer_files:
        layer_file = definitions_dir / manifest['files'][layer_name]
        
        if not layer_file.exists():
            # If any layer file is missing, return None (fall back to transformers)
            return None
        
        try:
            with open(layer_file, 'r', encoding='utf-8') as f:
                layer_definitions[layer_name] = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            # If any file is corrupted, return None (fall back to transformers)
            print(f"Warning: Failed to load {layer_file}: {e}")
            return None
    
    return layer_definitions
