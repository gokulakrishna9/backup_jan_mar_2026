# Dummy Data Generator

Generates realistic test data from SQL database definitions while maintaining referential integrity.

## Features

- Parses SQL CREATE TABLE statements
- Maintains foreign key relationships
- Configurable record counts at leaf level
- Generates both JSON and SQL INSERT formats
- Includes metadata about record counts per table
- Automatic timestamped output files

## Usage

```bash
python main.py --input schema.sql --leaf-records 100
```

With custom database name:
```bash
python main.py --input schema.sql --db-name my_database --leaf-records 100
```

## Arguments

- `--input`: Path to SQL schema file (required)
- `--db-name`: Database name for output files (optional, defaults to input filename)
- `--leaf-records`: Average number of records for leaf tables (default: 50)

## Output Files

Files are automatically saved to `../generated_data_folder/`:
- `{db_name}_{timestamp}.json`: JSON array of all records with metadata
- `{db_name}_{timestamp}.sql`: SQL INSERT statements ready to execute

Example output:
- `../generated_data_folder/example_schema_20260310_143022.json`
- `../generated_data_folder/example_schema_20260310_143022.sql`
