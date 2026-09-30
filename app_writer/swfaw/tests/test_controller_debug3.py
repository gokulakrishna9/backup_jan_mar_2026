"""Debug Jinja2 dict.update resolution issue."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from jinja2 import Template

# Test: does Jinja2 resolve endpoints.update to the dict method or the key?
t1 = Template("{% if endpoints.update %}YES{% else %}NO{% endif %}")
t2 = Template("{% if endpoints['update'] %}YES{% else %}NO{% endif %}")
t3 = Template("{% if endpoints.update and endpoints.update.enabled %}YES{% else %}NO{% endif %}")

ctx = {'endpoints': {'update': {'enabled': True, 'path': '/{id}'}}}

print(f"endpoints.update: {t1.render(ctx)}")
print(f"endpoints['update']: {t2.render(ctx)}")
print(f"endpoints.update and endpoints.update.enabled: {t3.render(ctx)}")

# Check what endpoints.update actually resolves to
t4 = Template("{{ endpoints.update }}")
print(f"endpoints.update value: {t4.render(ctx)}")
