#!/usr/bin/env python3
"""Convert SQL to JSON for swfaw_v2"""
import re
import json
import sys
import argparse
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Convert SQL schema to JSON database definition'
    )
    parser.add_argument(
        'sql_file',
        help='Path to SQL schema file'
    )
    parser.add_argument(
        '--output',
        '-o',
        default=None,
        help='Output JSON file path (default: application_definition.json in same directory as SQL file)'
    )
    
    args = parser.parse_args()
    
    sql_file = args.sql_file
    
    # Default output: application_definition.json in same directory as SQL file
    if args.output is None:
        sql_path = Path(sql_file)
        output_file = sql_path.parent / 'application_definition.json'
    else:
        output_file = args.output
    
    print(f'Reading SQL file: {sql_file}')
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Extract database name
    db_match = re.search(r'CREATE DATABASE.*?`(\w+)`', sql_content, re.IGNORECASE)
    db_name = db_match.group(1) if db_match else 'ems_recruitment_portal'

    print(f'Database: {db_name}')

    # Find all CREATE TABLE statements
    table_pattern = r'CREATE TABLE(?:\s+IF\s+NOT\s+EXISTS)?\s+`?(\w+)`?\s*\(((?:(?!CREATE TABLE).)+?)\)(?:\s*ENGINE[^;]*)?;'
    tables = re.findall(table_pattern, sql_content, re.DOTALL | re.IGNORECASE)

    print(f'Found {len(tables)} tables')

    parsed_tables = []

    for table_name, table_def in tables:
        print(f'  Parsing table: {table_name}')
        
        columns = []
        primary_key = None
        
        lines = table_def.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('--'):
                continue
            
            # Primary key (separate PRIMARY KEY constraint)
            if 'PRIMARY KEY' in line.upper() and not re.match(r'`?(\w+)`?\s+', line):
                pk_match = re.search(r'PRIMARY KEY.*?\(([^)]+)\)', line, re.IGNORECASE)
                if pk_match:
                    primary_key = pk_match.group(1).strip('`').strip()
                continue
            
            # Skip constraints (but not PRIMARY KEY which is handled separately)
            if ('FOREIGN KEY' in line.upper() or 'CONSTRAINT' in line.upper() or 
                ('KEY' in line.upper() and 'PRIMARY KEY' not in line.upper())):
                continue
            
            # Column definition
            col_match = re.match(r'`?(\w+)`?\s+([A-Z]+(?:\([^)]+\))?(?:\s+UNSIGNED)?)', line, re.IGNORECASE)
            if col_match:
                col_name = col_match.group(1)
                col_type = col_match.group(2).strip()
                
                if col_name in ['created_by_id', 'updated_by_id']:
                    continue
                
                # Check for inline PRIMARY KEY
                is_primary = 'PRIMARY KEY' in line.upper()
                if is_primary:
                    primary_key = col_name
                
                nullable = 'NOT NULL' not in line.upper()
                unique = 'UNIQUE' in line.upper()
                
                columns.append({
                    'name': col_name,
                    'type': col_type,
                    'primaryKey': is_primary,
                    'nullable': nullable,
                    'unique': unique
                })
        
        # Mark primary key from separate PRIMARY KEY constraint if found
        if primary_key:
            for col in columns:
                if col['name'] == primary_key:
                    col['primaryKey'] = True
                    break
        
        parsed_tables.append({
            'name': table_name,
            'columns': columns,
            'relationships': []
        })

    # Create database definition
    db_definition = {
        'projectMetadata': {
            'name': db_name.replace('_', '-'),
            'applicationName': db_name.replace('_', ' ').title(),
            'groupId': 'com.example',
            'artifactId': db_name.replace('_', '-'),
            'version': '1.0.0',
            'port': 8081,
            'sqlFileName': Path(sql_file).name,
            'dateCreated': datetime.now().strftime('%Y-%m-%d'),
            'database': {
                'type': 'mysql',
                'host': 'localhost',
                'port': 3306,
                'name': db_name,
                'username': 'root',
                'password': 'password'
            }
        },
        'tables': parsed_tables
    }

    print(f'\nWriting to: {output_file}')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(db_definition, f, indent=2)

    print(f'\nConversion complete!')
    print(f'  Total tables: {len(parsed_tables)}')
    print(f'  Output file: {output_file}')


if __name__ == '__main__':
    main()
