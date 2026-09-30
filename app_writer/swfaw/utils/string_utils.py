"""String utility functions for code generation."""


def to_pascal_case(text: str) -> str:
    """Convert string to PascalCase.
    
    Examples:
        ems_course -> Course
        user_profile -> UserProfile
    """
    # Remove common prefixes
    text = text.replace('ems_', '')
    
    return ''.join(word.capitalize() for word in text.split('_'))


def to_camel_case(text: str) -> str:
    """Convert string to camelCase.
    
    Examples:
        course_id -> courseId
        user_name -> userName
    """
    pascal = to_pascal_case(text)
    return pascal[0].lower() + pascal[1:] if pascal else ''


def map_sql_type_to_java(sql_type: str) -> str:
    """Map SQL data type to Java data type.
    
    Args:
        sql_type: SQL type like 'BIGINT', 'VARCHAR(255)', 'TEXT', 'BIGINT UNSIGNED'
        
    Returns:
        Java type like 'Long', 'String', 'Boolean'
    """
    type_map = {
        'BIGINT': 'Long',
        'INT': 'Integer',
        'INTEGER': 'Integer',
        'SMALLINT': 'Short',
        'TINYINT': 'Byte',
        'VARCHAR': 'String',
        'CHAR': 'String',
        'TEXT': 'String',
        'LONGTEXT': 'String',
        'MEDIUMTEXT': 'String',
        'BOOLEAN': 'Boolean',
        'BOOL': 'Boolean',
        'BIT': 'Boolean',
        'DATE': 'LocalDate',
        'DATETIME': 'LocalDateTime',
        'TIMESTAMP': 'LocalDateTime',
        'TIME': 'LocalTime',
        'DECIMAL': 'BigDecimal',
        'NUMERIC': 'BigDecimal',
        'FLOAT': 'Float',
        'DOUBLE': 'Double',
        'REAL': 'Double',
        'BLOB': 'byte[]',
        'BINARY': 'byte[]',
        'VARBINARY': 'byte[]',
        'JSON': 'String',
        'UUID': 'UUID',
        'ENUM': 'String'
    }
    
    # Extract base type (remove size specification and UNSIGNED keyword)
    base_type = sql_type.split('(')[0].strip().upper()
    base_type = base_type.replace(' UNSIGNED', '').strip()
    
    return type_map.get(base_type, 'String')


def pluralize(word: str) -> str:
    """Simple pluralization for English words.
    
    Args:
        word: Singular word
        
    Returns:
        Plural form
    """
    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word.endswith(('s', 'x', 'z', 'ch', 'sh')):
        return word + 'es'
    else:
        return word + 's'


def singularize(word: str) -> str:
    """Simple singularization for English words.
    
    Args:
        word: Plural word
        
    Returns:
        Singular form
    """
    if word.endswith('ies'):
        return word[:-3] + 'y'
    elif word.endswith('es'):
        return word[:-2]
    elif word.endswith('s'):
        return word[:-1]
    else:
        return word
