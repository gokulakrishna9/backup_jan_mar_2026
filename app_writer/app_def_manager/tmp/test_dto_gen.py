"""Test DTO generation directly to see what it produces."""
import sys, json
sys.path.insert(0, 'swfaw')
from models.layer_objects import DTOLayerObject, Field
from generators.dto_generator import DTOGenerator

# Load the definition
d = json.load(open('application_definitions/job_portal/webflux_dto_layer.json'))
for dto_def in d['dtos']:
    if dto_def['entityName'] == 'UserProfile' and dto_def['dtoType'] == 'Input':
        dto_fields = []
        for fd in dto_def['fields']:
            fd2 = dict(fd)
            if 'columnName' not in fd2:
                fd2['columnName'] = fd2['fieldName']
            dto_fields.append(Field(**fd2))

        dto = DTOLayerObject(
            entityName=dto_def['entityName'],
            className=dto_def['className'],
            packageName=dto_def['packageName'],
            fields=dto_fields,
            dtoType=dto_def['dtoType'],
            isRootEntity=False,
            fieldConfigs=dto_def.get('fields', []),
        )
        code = DTOGenerator.generate(dto)
        print(code)
        break
