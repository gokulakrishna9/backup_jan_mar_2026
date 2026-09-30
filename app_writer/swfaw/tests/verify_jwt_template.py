"""Quick verification that JWT_SERVICE_TEMPLATE has all required methods and claims."""
import sys
sys.path.insert(0, "swfaw")

from jinja2 import Template
from templates.jwt_templates import JWTTemplates

template = Template(JWTTemplates.JWT_SERVICE_TEMPLATE)
result = template.render(packageName="com.example.security")

checks = [
    ("generateToken with roles param", "List<Map<String, Object>> roles" in result),
    ("generateToken with tableAccess param", "Map<String, List<String>> tableAccess" in result),
    ("generateToken with queryGroupMemberships param", "List<Long> queryGroupMemberships" in result),
    ("roles claim serialized", 'claim("roles", rolesJson)' in result),
    ("tableAccess claim serialized", 'claim("tableAccess", tableAccessJson)' in result),
    ("queryGroupMemberships claim serialized", 'claim("queryGroupMemberships", queryGroupMembershipsJson)' in result),
    ("extractRoles method exists", "public List<Map<String, Object>> extractRoles(String token)" in result),
    ("extractTableAccess method exists", "public Map<String, List<String>> extractTableAccess(String token)" in result),
    ("extractQueryGroupMemberships method exists", "public List<Long> extractQueryGroupMemberships(String token)" in result),
    ("ObjectMapper for JSON serialization", "ObjectMapper" in result),
    ("TypeReference for deserialization", "TypeReference" in result),
    ("null-safe roles handling", "roles != null ? roles : Collections.emptyList()" in result),
    ("null-safe tableAccess handling", "tableAccess != null ? tableAccess : Collections.emptyMap()" in result),
    ("null-safe queryGroupMemberships handling", "queryGroupMemberships != null ? queryGroupMemberships : Collections.emptyList()" in result),
]

all_pass = True
for name, passed in checks:
    status = "PASS" if passed else "FAIL"
    if not passed:
        all_pass = False
    print(f"  [{status}] {name}")

print(f"\nAll checks passed: {all_pass}")
if not all_pass:
    sys.exit(1)
