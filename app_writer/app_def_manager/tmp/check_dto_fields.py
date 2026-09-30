"""Check what fields the DTO definition has for UserProfile Input."""
import json
d = json.load(open('application_definitions/job_portal/webflux_dto_layer.json'))
for dto in d['dtos']:
    if dto['entityName'] == 'UserProfile' and dto['dtoType'] == 'Input':
        print(f"Input DTO fields ({len(dto['fields'])}):")
        for f in dto['fields']:
            print(f"  {json.dumps(f)}")
