"""Quick verification that the updated JWT_SERVICE_TEMPLATE renders correctly."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from jinja2 import Template
from templates.jwt_templates import JWTTemplates

t = Template(JWTTemplates.JWT_SERVICE_TEMPLATE)
result = t.render(packageName='com.example.app')

checks = [
    ('generateToken method', 'public String generateToken(String username, Long userId,'),
    ('roles parameter', 'List<Map<String, Object>> roles'),
    ('tableAccess parameter', 'Map<String, List<String>> tableAccess'),
    ('queryGroupMemberships parameter', 'List<Long> queryGroupMemberships'),
    ('extractRoles method', 'public List<Map<String, Object>> extractRoles(String token)'),
    ('extractTableAccess method', 'public Map<String, List<String>> extractTableAccess(String token)'),
    ('extractQueryGroupMemberships method', 'public List<Long> extractQueryGroupMemberships(String token)'),
    ('ObjectMapper import', 'import com.fasterxml.jackson.databind.ObjectMapper'),
    ('TypeReference import', 'import com.fasterxml.jackson.core.type.TypeReference'),
    ('getClaims helper', 'private Claims getClaims(String token)'),
    ('roles claim in builder', '.claim("roles", rolesJson)'),
    ('tableAccess claim in builder', '.claim("tableAccess", tableAccessJson)'),
    ('queryGroupMemberships claim in builder', '.claim("queryGroupMemberships", queryGroupMembershipsJson)'),
]

all_passed = True
for name, expected in checks:
    if expected in result:
        print(f"  PASS: {name}")
    else:
        print(f"  FAIL: {name} - expected '{expected}'")
        all_passed = False

if all_passed:
    print("\nAll checks passed! Template renders correctly.")
else:
    print("\nSome checks failed!")
    sys.exit(1)
