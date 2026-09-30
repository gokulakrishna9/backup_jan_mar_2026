"""Debug controller template rendering."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from jinja2 import Template
from swfaw.templates.controller_templates import ControllerTemplates

context = {
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

template = Template(ControllerTemplates.CONTROLLER_TEMPLATE)
result = template.render(context)

# Print lines containing TableAccess or UPDATE
for i, line in enumerate(result.split('\n'), 1):
    if 'TableAccess' in line or 'UPDATE' in line or 'PutMapping' in line:
        print(f"Line {i}: {repr(line)}")
