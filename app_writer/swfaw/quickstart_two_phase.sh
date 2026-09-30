#!/bin/bash
# Quick start script for two-phase workflow

echo "=================================="
echo "swfaw_v2 Two-Phase Quick Start"
echo "=================================="
echo ""

# Check if input file is provided
if [ -z "$1" ]; then
    echo "Usage: ./quickstart_two_phase.sh <sql_or_json_file> [output_directory]"
    echo ""
    echo "Examples:"
    echo "  ./quickstart_two_phase.sh ../mysql_database_design/schema.sql"
    echo "  ./quickstart_two_phase.sh ../mysql_database_design/schema.sql ../generated_application/my_app"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_DIR="${2:-../generated_application/$(basename $INPUT_FILE .sql)_$(date +%Y%m%d_%H%M%S)}"

echo "Input: $INPUT_FILE"
echo "Output: $OUTPUT_DIR"
echo ""

# Run unified workflow
python generate_app.py --input "$INPUT_FILE" --output "$OUTPUT_DIR"

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================="
    echo "Generation Complete!"
    echo "=================================="
    echo ""
    echo "Next steps:"
    echo "1. Setup database:"
    echo "   mysql -u root -p -e 'CREATE DATABASE your_db_name;'"
    echo "   mysql -u root -p your_db_name < $OUTPUT_DIR/auth-schema.sql"
    echo "   mysql -u root -p your_db_name < $OUTPUT_DIR/activity-tracking-schema.sql"
    echo ""
    echo "2. Build and run:"
    echo "   cd $OUTPUT_DIR"
    echo "   mvn clean install"
    echo "   mvn spring-boot:run"
    echo ""
    echo "3. Complete setup at: http://localhost:8081/setup"
else
    echo ""
    echo "Generation failed. Check errors above."
    exit 1
fi
