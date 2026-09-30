"""
Data Generator - Creates realistic dummy data for tables
"""

import random
import re
import bcrypt
from typing import Dict, List, Any
from datetime import datetime, timedelta
from faker import Faker
from sql_parser import Table, Column
from dependency_analyzer import DependencyAnalyzer


class PasswordValue:
    """Holds both plain text and BCrypt-hashed password."""
    def __init__(self, plain: str):
        self.plain = plain
        self.hashed = bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def __str__(self):
        return self.plain


def snake_to_camel(snake_str: str) -> str:
    """Convert snake_case to camelCase"""
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


class DataGenerator:
    def __init__(self, tables: Dict[str, Table], analyzer: DependencyAnalyzer, leaf_records: int):
        self.tables = tables
        self.analyzer = analyzer
        self.leaf_records = leaf_records
        self.fake = Faker()
        self.generated_data: Dict[str, List[Dict[str, Any]]] = {}
        self.id_counters: Dict[str, int] = {}
    
    def generate_all(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate data for all tables in dependency order"""
        generation_order = self.analyzer.get_generation_order()
        
        for table_name in generation_order:
            table = self.tables[table_name]
            count = self._calculate_record_count(table_name)
            self.generated_data[table_name] = self._generate_table_data(table, count)
            print(f"  {table_name}: {count} records")
        
        return self.generated_data
    
    def _calculate_record_count(self, table_name: str) -> int:
        """Calculate how many records to generate based on dependency depth"""
        if self.analyzer.is_leaf_table(table_name):
            return self.leaf_records
        
        # For parent tables, calculate based on dependents
        dependents = self.analyzer.get_dependents(table_name)
        if not dependents:
            return self.leaf_records
        
        # Estimate based on foreign key relationships
        max_needed = 0
        for dependent in dependents:
            if dependent in self.generated_data:
                # Count unique foreign key values
                table = self.tables[dependent]
                for fk in table.foreign_keys:
                    if fk.ref_table == table_name:
                        unique_refs = len(set(
                            record.get(fk.column) 
                            for record in self.generated_data[dependent]
                            if record.get(fk.column) is not None
                        ))
                        max_needed = max(max_needed, unique_refs)
        
        return max(max_needed, self.leaf_records // 2)
    
    def _generate_table_data(self, table: Table, count: int) -> List[Dict[str, Any]]:
        """Generate data for a single table"""
        records = []
        
        for i in range(count):
            record = {}
            
            for col in table.columns:
                if col.auto_increment:
                    record[col.name] = self._get_next_id(table.name)
                elif col.name in table.primary_keys and not col.auto_increment:
                    record[col.name] = self._get_next_id(table.name)
                else:
                    # Check if this is a foreign key
                    fk = next((fk for fk in table.foreign_keys if fk.column == col.name), None)
                    if fk:
                        record[col.name] = self._get_foreign_key_value(fk)
                    else:
                        record[col.name] = self._generate_value(col)
            
            records.append(record)
        
        return records
    
    def _get_next_id(self, table_name: str) -> int:
        """Get next ID for a table"""
        if table_name not in self.id_counters:
            self.id_counters[table_name] = 1
        else:
            self.id_counters[table_name] += 1
        return self.id_counters[table_name]
    
    def _get_foreign_key_value(self, fk) -> Any:
        """Get a valid foreign key value from referenced table"""
        if fk.ref_table not in self.generated_data:
            return None
        
        ref_records = self.generated_data[fk.ref_table]
        if not ref_records:
            return None
        
        ref_record = random.choice(ref_records)
        return ref_record.get(fk.ref_column)
    
    def _parse_type_size(self, data_type: str):
        """Extract precision/scale or max length from type like DECIMAL(5,2) or VARCHAR(100)."""
        m = re.search(r'\(\s*(\d+)\s*(?:,\s*(\d+))?\s*\)', data_type)
        if m:
            return int(m.group(1)), int(m.group(2)) if m.group(2) else None
        return None, None

    def _generate_value(self, col: Column) -> Any:
        """Generate a value based on column type and name"""
        if col.nullable and random.random() < 0.1:
            return None
        
        col_name_lower = col.name.lower()
        col_type_lower = col.data_type.lower()
        
        # ENUM — parse actual values from column definition (check first, before name heuristics)
        if col_type_lower.startswith('enum'):
            enum_values = re.findall(r"'([^']*)'", col.data_type)
            if enum_values:
                return random.choice(enum_values)
            return random.choice(['active', 'inactive', 'pending'])
        
        # TINYINT(1) — treat as boolean (0 or 1)
        if re.match(r'tinyint\s*\(\s*1\s*\)', col_type_lower):
            return random.choice([0, 1])
        
        # Extract base type
        base_type_match = re.match(r'(\w+)', col_type_lower)
        base_type = base_type_match.group(1) if base_type_match else col_type_lower
        
        # For non-string types, skip name-based generation (prevents 'capacity' matching 'city')
        is_string_type = base_type in ['varchar', 'char', 'text', 'longtext', 'mediumtext']
        
        # Name-based generation (only for string types)
        if is_string_type:
            max_len, _ = self._parse_type_size(col.data_type)
            val = self._generate_by_name(col_name_lower, max_len)
            if val is not None:
                if max_len and len(str(val)) > max_len:
                    val = str(val)[:max_len]
                return val
            # Default string generation
            val = self.fake.sentence(nb_words=5)
            if max_len and len(val) > max_len:
                val = val[:max_len]
            return val
        
        # Type-based generation
        if base_type in ['int', 'integer', 'bigint', 'smallint', 'tinyint']:
            return random.randint(1, 1000)
        elif base_type in ['decimal', 'numeric', 'float', 'double', 'real']:
            precision, scale = self._parse_type_size(col.data_type)
            if precision and scale is not None:
                int_digits = precision - scale
                max_val = (10 ** int_digits) - (10 ** -scale)
                # Name-based hints for common constrained columns
                if 'rating' in col_name_lower:
                    return round(random.uniform(1.0, min(5.0, max_val)), scale)
                elif 'score' in col_name_lower:
                    return round(random.uniform(0.0, min(1.0, max_val)), scale)
                return round(random.uniform(0.0, max_val), scale)
            return round(random.uniform(1.0, 1000.0), 2)
        elif base_type in ['date']:
            return self.fake.date_between(start_date='-5y', end_date='today').isoformat()
        elif base_type in ['datetime', 'timestamp']:
            return self.fake.date_time_between(start_date='-2y', end_date='now').isoformat()
        elif base_type in ['time']:
            return self.fake.time()
        elif base_type in ['boolean', 'bool', 'bit']:
            return random.choice([True, False])
        elif base_type in ['json']:
            return '{}'
        
        return self.fake.word()

    def _generate_by_name(self, col_name_lower: str, max_len: int = None) -> Any:
        """Generate value based on column name heuristics. Returns None if no match."""
        if 'email' in col_name_lower:
            return self.fake.email()
        elif 'phone' in col_name_lower:
            return self.fake.phone_number()
        elif col_name_lower.endswith('_address') or col_name_lower == 'address':
            return self.fake.address().replace('\n', ', ')
        elif col_name_lower.endswith('_city') or col_name_lower == 'city':
            return self.fake.city()
        elif 'state' in col_name_lower or 'province' in col_name_lower:
            return self.fake.state()
        elif col_name_lower.endswith('_country') or col_name_lower == 'country':
            return self.fake.country()
        elif 'zip' in col_name_lower or 'postal' in col_name_lower:
            return self.fake.zipcode()
        elif 'first_name' in col_name_lower or 'firstname' in col_name_lower:
            return self.fake.first_name()
        elif 'last_name' in col_name_lower or 'lastname' in col_name_lower:
            return self.fake.last_name()
        elif 'username' in col_name_lower or 'user_name' in col_name_lower:
            return self.fake.user_name()
        elif col_name_lower.endswith('_name') or col_name_lower == 'name':
            return self.fake.name()
        elif 'password' in col_name_lower:
            plain = self.fake.password()
            if 'hash' in col_name_lower:
                return PasswordValue(plain)
            return plain
        elif 'url' in col_name_lower or 'website' in col_name_lower:
            return self.fake.url()
        elif 'company' in col_name_lower or 'organization' in col_name_lower:
            return self.fake.company()
        elif 'title' in col_name_lower:
            return self.fake.sentence(nb_words=6).rstrip('.')
        elif 'description' in col_name_lower or 'bio' in col_name_lower:
            return self.fake.text(max_nb_chars=min(200, max_len or 200))
        elif 'content' in col_name_lower or 'body' in col_name_lower:
            return self.fake.text(max_nb_chars=min(500, max_len or 500))
        return None
