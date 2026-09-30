#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Generate test data with 100 records at leaf level
python main.py --input example_schema.sql --leaf-records 100

# Or with custom database name
python main.py --input example_schema.sql --db-name my_test_db --leaf-records 100

# The output files will be automatically saved to:
# ../generated_data_folder/{db_name}_{timestamp}.json
# ../generated_data_folder/{db_name}_{timestamp}.sql
