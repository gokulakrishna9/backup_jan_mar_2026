import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from generators.document_storage_schema_generator import DocumentStorageSchemaGenerator

# Test 1: file storage enabled + one collection
result = DocumentStorageSchemaGenerator.generate({
    'fileStorage': {'enabled': True},
    'documentCollections': [{'name': 'AuditLog', 'tableName': 'audit_log_docs'}]
})
assert 'CREATE TABLE IF NOT EXISTS `file_metadata`' in result
assert 'CREATE TABLE IF NOT EXISTS `audit_log_docs`' in result
assert result.count('CREATE TABLE') == 2
print('PASS: file storage + collection')

# Test 2: nothing enabled
result = DocumentStorageSchemaGenerator.generate({
    'fileStorage': {'enabled': False},
    'documentCollections': []
})
assert result == ''
print('PASS: empty when nothing enabled')

# Test 3: only collections
result = DocumentStorageSchemaGenerator.generate({
    'fileStorage': {'enabled': False},
    'documentCollections': [{'name': 'Notes', 'tableName': 'notes_docs'}]
})
assert 'file_metadata' not in result
assert 'notes_docs' in result
print('PASS: collections only')

# Test 4: only file storage
result = DocumentStorageSchemaGenerator.generate({
    'fileStorage': {'enabled': True},
    'documentCollections': []
})
assert 'file_metadata' in result
assert result.count('CREATE TABLE') == 1
print('PASS: file storage only')

# Test 5: missing fileStorage key
result = DocumentStorageSchemaGenerator.generate({'documentCollections': []})
assert result == ''
print('PASS: missing fileStorage key')

# Test 6: multiple collections
result = DocumentStorageSchemaGenerator.generate({
    'fileStorage': {'enabled': False},
    'documentCollections': [
        {'name': 'A', 'tableName': 'table_a'},
        {'name': 'B', 'tableName': 'table_b'},
    ]
})
assert 'table_a' in result
assert 'table_b' in result
assert result.count('CREATE TABLE') == 2
print('PASS: multiple collections')

print('\nAll tests passed!')
