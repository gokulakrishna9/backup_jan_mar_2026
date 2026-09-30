#!/usr/bin/env python3
"""
Dummy Data Generator - Generates test data from SQL schema definitions
"""

import argparse
import os
from datetime import datetime
from pathlib import Path
from sql_parser import SQLParser
from dependency_analyzer import DependencyAnalyzer
from data_generator import DataGenerator
from output_writer import OutputWriter


def main():
    parser = argparse.ArgumentParser(description='Generate dummy data from SQL schema')
    parser.add_argument('--input', required=True, help='Business SQL schema file (from mysql_database_design/)')
    parser.add_argument('--app-dir', help='Path to webflux_app folder for auth schema (e.g. generated_application/<app>/webflux_app)')
    parser.add_argument('--db-name', help='Database name (defaults to input filename)')
    parser.add_argument('--leaf-records', type=int, default=50, 
                       help='Average number of records for leaf tables')
    
    args = parser.parse_args()
    
    # Determine database name
    if args.db_name:
        db_name = args.db_name
    else:
        db_name = Path(args.input).stem
    
    # Create output directory
    script_dir = Path(__file__).parent
    output_dir = script_dir.parent / 'generated_data_folder'
    output_dir.mkdir(exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create output file paths
    output_prefix = output_dir / f"{db_name}_{timestamp}"
    json_file = f"{output_prefix}.json"
    sql_file = f"{output_prefix}.sql"
    
    print(f"Parsing business schema: {args.input}")
    sql_parser = SQLParser()
    tables = sql_parser.parse_file(args.input)
    print(f"  Found {len(tables)} business tables")
    
    # Merge auth schema if --app-dir provided
    if args.app_dir:
        auth_schema = Path(args.app_dir) / 'auth-schema.sql'
        if auth_schema.exists():
            print(f"Parsing auth schema: {auth_schema}")
            auth_tables = sql_parser.parse_file(str(auth_schema))
            tables.update(auth_tables)
            print(f"  Found {len(auth_tables)} auth tables")
        else:
            print(f"⚠️  Auth schema not found: {auth_schema}")
    
    print(f"Total: {len(tables)} tables")
    
    print("\nAnalyzing dependencies...")
    analyzer = DependencyAnalyzer(tables)
    generation_order = analyzer.get_generation_order()
    print(f"Generation order: {' -> '.join(generation_order)}")
    
    print(f"\nGenerating data (leaf tables: ~{args.leaf_records} records)...")
    generator = DataGenerator(tables, analyzer, args.leaf_records)
    all_data = generator.generate_all()
    
    print("\nWriting output files...")
    writer = OutputWriter(tables, all_data)
    writer.write_json(json_file)
    writer.write_sql(sql_file)
    
    print(f"\n✓ Generated {sum(len(records) for records in all_data.values())} total records")
    print(f"✓ JSON output: {json_file}")
    print(f"✓ SQL output: {sql_file}")


if __name__ == '__main__':
    main()
