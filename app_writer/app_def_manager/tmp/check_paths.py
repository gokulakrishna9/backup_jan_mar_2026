"""Check basePath values in controller layer vs generated Java files."""
import json, glob, re

# From definition
d = json.load(open('application_definitions/job_portal/webflux_controller_layer.json'))
print("=== Definition basePaths ===")
for c in d['controllers']:
    print(f"  {c['entityName']}: {c['basePath']}")

# From generated Java
print("\n=== Generated @RequestMapping ===")
for f in sorted(glob.glob('generated_application/job_portal/webflux_app/src/main/java/com/jobportal/controller/*Controller.java')):
    with open(f) as fh:
        content = fh.read()
    m = re.search(r'@RequestMapping\("([^"]+)"\)', content)
    name = f.split('/')[-1].replace('.java', '')
    if m:
        print(f"  {name}: {m.group(1)}")
