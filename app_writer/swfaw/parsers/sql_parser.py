"""SQL Parser for converting MySQL schemas to application definitions."""

import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

from models.database_definition import DatabaseDefinition, ProjectMetadata, DatabaseConfig, Table, Column


class SQLParser:
    """Parser for MySQL SQL schemas."""
    
    def parse_file(self, sql_file: str) -> DatabaseDefinition:
        """Parse SQL file and return DatabaseDefinition."""
        sql_path = Path(sql_file)
        
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Extract database name
        db_match = re.search(r'CREATE DATABASE.*?`(\w+)`', sql_content, re.IGNORECASE)
        db_name = db_match.group(1) if db_match else 'database'
        
        # Parse tables
        tables = self._parse_tables(sql_content)
        
        # Create project metadata
        project_metadata = ProjectMetadata(
            name=db_name.replace('_', '-'),
            applicationName=db_name.replace('_', ' ').title(),
            groupId='com.example',
            artifactId=db_name.replace('_', '-'),
            version='1.0.0',
            port=8081,
            sqlFileName=sql_path.name,
            dateCreated=datetime.now().strftime('%Y-%m-%d'),
            database=DatabaseConfig(
                type='mysql',
                host='localhost',
                port=3306,
                name=db_name,
                username='root',
                password='password'
            )
        )
        
        return DatabaseDefinition(
            projectMetadata=project_metadata,
            tables=tables
        )
    
    def _parse_tables(self, sql_content: str) -> List[Table]:
        """Parse all CREATE TABLE statements."""
        table_pattern = r'CREATE TABLE(?:\s+IF\s+NOT\s+EXISTS)?\s+`?(\w+)`?\s*\(((?:(?!CREATE TABLE).)+?)\)(?:\s*ENGINE[^;]*)?;'
        table_matches = re.findall(table_pattern, sql_content, re.DOTALL | re.IGNORECASE)
        
        tables = []
        for table_name, table_def in table_matches:
            columns = self._parse_columns(table_def)
            
            tables.append(Table(
                name=table_name,
                columns=columns,
                relationships=[]
            ))
        
        return tables
    
    def _parse_columns(self, table_def: str) -> List[Column]:
        """Parse column definitions from table definition."""
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
            
            # Skip constraints
            if ('FOREIGN KEY' in line.upper() or 'CONSTRAINT' in line.upper() or 
                ('KEY' in line.upper() and 'PRIMARY KEY' not in line.upper())):
                continue
            
            # Column definition
            col_match = re.match(r'`?(\w+)`?\s+([A-Z]+(?:\([^)]+\))?(?:\s+UNSIGNED)?)', line, re.IGNORECASE)
            if col_match:
                col_name = col_match.group(1)
                col_type = col_match.group(2).strip()
                
                # Skip audit columns
                if col_name in ['created_by_id', 'updated_by_id']:
                    continue
                
                # Check for inline PRIMARY KEY
                is_primary = 'PRIMARY KEY' in line.upper()
                if is_primary:
                    primary_key = col_name
                
                nullable = 'NOT NULL' not in line.upper()
                unique = 'UNIQUE' in line.upper()
                
                columns.append(Column(
                    name=col_name,
                    type=col_type,
                    primaryKey=is_primary,
                    nullable=nullable,
                    unique=unique
                ))
        
        # Mark primary key from separate PRIMARY KEY constraint
        if primary_key:
            for col in columns:
                if col.name == primary_key:
                    col.primaryKey = True
                    break
        
        return columns
