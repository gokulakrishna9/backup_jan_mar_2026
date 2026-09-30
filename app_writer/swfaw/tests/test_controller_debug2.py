"""Debug controller template rendering - update section."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from jinja2 import Template

# Test just the update section
test_template = """{% if endpoints.update and endpoints.update.enabled %}UPDATE_PRESENT{% endif %}"""

context = {
    'endpoints': {
        'update': {'enabled': True, 'path': '/{id}'},
    }
}

template = Template(test_template)
result = template.render(context)
print(f"Result: '{result}'")

# Now test with the actual template
from swfaw.templates.controller_templates import ControllerTemplates

full_context = {
    'packageName': 'com.example.controller',
    'dtoPackage': 'com.example.dto',
    'servicePackage': 'com.example.service',
    'exceptionPackage': 'com.example.exception',
    'securityPackage': 'com.example.security',
    'entityName': 'Project',
    'className': 'ProjectController',
    'serviceName': 'ProjectService',
    'basePath': '/api/projects',
    'tableName': 'project',
    'isRootEntity': True,
    'endpoints': {
        'create': {'enabled': True, 'path': ''},
        'getById': {'enabled': True, 'path': '/{id}'},
        'getAll': {'enabled': True, 'path': '', 'defaultPageSize': 20},
        'update': {'enabled': True, 'path': '/{id}'},
        'delete': {'enabled': True, 'path': '/{id}'}
    },
    'customEndpoints': [],
    'corsConfig': {'enabled': False},
    'hasActivityTracking': False
}

template2 = Template(ControllerTemplates.CONTROLLER_TEMPLATE)
result2 = template2.render(full_context)

# Check if the update section is present at all
if 'Update Project by ID' in result2:
    print("Update section IS present in output")
    # Find the update section
    lines = result2.split('\n')
    for i, line in enumerate(lines):
        if 'Update' in line or 'update' in line.lower():
            print(f"  Line {i+1}: {line}")
else:
    print("Update section is MISSING from output")
    # Print around where it should be
    lines = result2.split('\n')
    for i, line in enumerate(lines):
        if 'findAll' in line or 'delete' in line.lower():
            print(f"  Line {i+1}: {line}")
