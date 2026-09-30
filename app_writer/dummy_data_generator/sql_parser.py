"""
SQL Parser - Extracts table definitions from SQL CREATE TABLE statements
"""

import re
from typing import List, Dict, Optional


class Column:
    def __init__(self, name: str, data_type: str, nullable: bool = True, 
                 auto_increment: bool = False, default: Optional[str] = None):
        self.name = name
        self.data_type = data_type
        self.nullable = nullable
        self.auto_increment = auto_increment
        self.default = default


class ForeignKey:
    def __init__(self, column: str, ref_table: str, ref_column: str):
        self.column = column
        self.ref_table = ref_table
        self.ref_column = ref_column


class Table:
    def __init__(self, name: str):
        self.name = name
        self.columns: List[Column] = []
        self.primary_keys: List[str] = []
        self.foreign_keys: List[ForeignKey] = []
        self.unique_constraints: List[List[str]] = []


class SQLParser:
    def parse_file(self, filepath: str) -> Dict[str, Table]:
        with open(filepath, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        return self.parse(sql_content)
    
    def parse(self, sql_content: str) -> Dict[str, Table]:
        tables = {}
        
        # Remove comments
        sql_content = re.sub(r'--.*$', '', sql_content, flags=re.MULTILINE)
        sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)
        
        # Find all CREATE TABLE statements - handle ENGINE and other trailing options
        create_table_pattern = r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?`?(\w+)`?\s*\((.*?)\)(?:\s*ENGINE\s*=\s*\w+)?(?:\s*DEFAULT\s+CHARSET\s*=\s*\w+)?(?:\s*COLLATE\s*=\s*[\w_]+)?;'
        matches = re.finditer(create_table_pattern, sql_content, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            table_name = match.group(1)
            table_def = match.group(2)
            
            table = Table(table_name)
            self._parse_table_definition(table, table_def)
            tables[table_name] = table
        
        return tables
    
    def _split_definitions(self, definition: str) -> List[str]:
        """Split table definition by commas, respecting parentheses and quotes."""
        parts = []
        current = []
        paren_depth = 0
        in_quote = False
        
        for char in definition:
            if char == "'" and not in_quote:
                in_quote = True
                current.append(char)
            elif char == "'" and in_quote:
                in_quote = False
                current.append(char)
            elif char == '(' and not in_quote:
                paren_depth += 1
                current.append(char)
            elif char == ')' and not in_quote:
                paren_depth -= 1
                current.append(char)
            elif char == ',' and paren_depth == 0 and not in_quote:
                parts.append(''.join(current).strip())
                current = []
            else:
                current.append(char)
        
        if current:
            parts.append(''.join(current).strip())
        
        return parts

    def _parse_table_definition(self, table: Table, definition: str):
        lines = self._split_definitions(definition)
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Primary key
            if re.match(r'PRIMARY\s+KEY', line, re.IGNORECASE):
                pk_match = re.search(r'PRIMARY\s+KEY\s*\((.*?)\)', line, re.IGNORECASE)
                if pk_match:
                    pk_cols = [col.strip('` ') for col in pk_match.group(1).split(',')]
                    table.primary_keys.extend(pk_cols)
            
            # Foreign key
            elif re.match(r'(?:CONSTRAINT.*?)?FOREIGN\s+KEY', line, re.IGNORECASE):
                fk_match = re.search(
                    r'FOREIGN\s+KEY\s*\(`?(\w+)`?\)\s*REFERENCES\s+`?(\w+)`?\s*\(`?(\w+)`?\)',
                    line, re.IGNORECASE
                )
                if fk_match:
                    fk = ForeignKey(fk_match.group(1), fk_match.group(2), fk_match.group(3))
                    table.foreign_keys.append(fk)
            
            # Unique constraint
            elif re.match(r'UNIQUE', line, re.IGNORECASE):
                unique_match = re.search(r'UNIQUE.*?\((.*?)\)', line, re.IGNORECASE)
                if unique_match:
                    unique_cols = [col.strip('` ') for col in unique_match.group(1).split(',')]
                    table.unique_constraints.append(unique_cols)
            
            # Skip INDEX, KEY, CHECK, CONSTRAINT lines (not column definitions)
            elif re.match(r'(INDEX|KEY|CHECK|CONSTRAINT)\s', line, re.IGNORECASE):
                continue
            
            # Column definition
            elif re.match(r'`?\w+`?\s+', line):
                col = self._parse_column(line)
                if col:
                    table.columns.append(col)
    
    def _parse_column(self, line: str) -> Optional[Column]:
        # Extract column name and full type (including ENUM values, size specifiers)
        col_match = re.match(r"`?(\w+)`?\s+", line, re.IGNORECASE)
        if not col_match:
            return None
        
        col_name = col_match.group(1)
        rest = line[col_match.end():]
        
        # Extract full data type including ENUM('val1','val2',...) or TYPE(size)
        enum_match = re.match(r"(ENUM\s*\([^)]+\))", rest, re.IGNORECASE)
        if enum_match:
            full_type = enum_match.group(1)
        else:
            type_match = re.match(r"(\w+(?:\s*\([^)]*\))?)", rest, re.IGNORECASE)
            full_type = type_match.group(1).strip() if type_match else rest.split()[0]
        
        nullable = 'NOT NULL' not in line.upper()
        auto_increment = 'AUTO_INCREMENT' in line.upper()
        
        # Extract default value
        default = None
        default_match = re.search(r"DEFAULT\s+('.*?'|\d+|NULL|CURRENT_TIMESTAMP)", line, re.IGNORECASE)
        if default_match:
            default = default_match.group(1).strip("'")
        
        return Column(col_name, full_type, nullable, auto_increment, default)
