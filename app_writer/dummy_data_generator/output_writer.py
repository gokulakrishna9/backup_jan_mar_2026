"""
Output Writer - Writes generated data to JSON and SQL formats
"""

import json
from typing import Dict, List, Any
from datetime import datetime, date
from sql_parser import Table
from data_generator import PasswordValue


def _snake_to_camel(snake_str: str) -> str:
    """Convert snake_case to camelCase"""
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


class OutputWriter:
    def __init__(self, tables: Dict[str, Table], data: Dict[str, List[Dict[str, Any]]]):
        self.tables = tables
        self.data = data
    
    def write_json(self, filepath: str):
        """Write data to JSON file with metadata (camelCase keys for API compatibility)"""
        camel_data = {}
        for table_name, records in self.data.items():
            camel_data[table_name] = [
                {_snake_to_camel(k): (v.plain if isinstance(v, PasswordValue) else v) for k, v in record.items()}
                for record in records
            ]

        output = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_records": sum(len(records) for records in self.data.values()),
                "tables": {
                    table_name: len(records) 
                    for table_name, records in self.data.items()
                }
            },
            "data": camel_data
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, default=str)
    
    def write_sql(self, filepath: str):
        """Write data to SQL INSERT statements"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("-- Generated test data\n")
            f.write(f"-- Generated at: {datetime.now().isoformat()}\n")
            f.write(f"-- Total records: {sum(len(records) for records in self.data.values())}\n\n")
            
            # Disable foreign key checks
            f.write("SET FOREIGN_KEY_CHECKS = 0;\n\n")
            
            for table_name, records in self.data.items():
                if not records:
                    continue
                
                f.write(f"-- {table_name} ({len(records)} records)\n")
                table = self.tables[table_name]
                
                for record in records:
                    columns = []
                    values = []
                    
                    for col in table.columns:
                        if col.name in record:
                            columns.append(f"`{col.name}`")
                            values.append(self._format_value(record[col.name]))
                    
                    if columns:
                        f.write(f"INSERT INTO `{table_name}` ({', '.join(columns)}) ")
                        f.write(f"VALUES ({', '.join(values)});\n")
                
                f.write("\n")
            
            # Re-enable foreign key checks
            f.write("SET FOREIGN_KEY_CHECKS = 1;\n")
    
    def _format_value(self, value: Any) -> str:
        """Format a value for SQL INSERT"""
        if value is None:
            return "NULL"
        elif isinstance(value, PasswordValue):
            escaped = value.hashed.replace("'", "''")
            return f"'{escaped}'"
        elif isinstance(value, bool):
            return "1" if value else "0"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, (datetime, date)):
            return f"'{value.isoformat()}'"
        else:
            # Escape single quotes
            escaped = str(value).replace("'", "''")
            return f"'{escaped}'"
