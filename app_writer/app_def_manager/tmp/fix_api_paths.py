"""Fix react_api_services.json basePaths to match generated controller @RequestMapping paths.
The controllers strip underscores from basePath, so React services need to match."""
import json, re
from pathlib import Path

# Read generated controller paths
import glob
controller_paths = {}
for f in glob.glob('generated_application/job_portal/webflux_app/src/main/java/com/jobportal/controller/*Controller.java'):
    with open(f) as fh:
        content = fh.read()
    # Extract entity name from @Tag annotation
    tag_match = re.search(r'@Tag\(name = "(\w+)"', content)
    path_match = re.search(r'@RequestMapping\("([^"]+)"\)', content)
    if tag_match and path_match:
        controller_paths[tag_match.group(1)] = path_match.group(1)

# Update react_api_services.json
api_path = Path('application_definitions/job_portal/react_api_services.json')
services = json.loads(api_path.read_text(encoding='utf-8'))
updated = 0
for svc in services:
    entity = svc['entityName']
    if entity in controller_paths and svc['basePath'] != controller_paths[entity]:
        old = svc['basePath']
        svc['basePath'] = controller_paths[entity]
        print(f"  {entity}: {old} -> {controller_paths[entity]}")
        updated += 1

api_path.write_text(json.dumps(services, indent=2), encoding='utf-8')
print(f"\nUpdated {updated} paths in react_api_services.json")
