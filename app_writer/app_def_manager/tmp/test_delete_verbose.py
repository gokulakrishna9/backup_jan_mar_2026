"""Test delete with verbose logging."""
import requests

BASE = "http://localhost:8081"
r = requests.post(f"{BASE}/api/auth/login", json={"username": "gokul", "password": "password"})
token = r.json().get("token")
headers = {"Authorization": f"Bearer {token}"}

# Create
r = requests.post(f"{BASE}/api/education_levels",
    json={"name": "DeleteTest", "description": "test", "sortorder": 1},
    headers=headers)
rid = r.json().get("educationLevelId")
print(f"Created: {rid}")

# Verify in list
r = requests.get(f"{BASE}/api/education_levels", headers=headers)
items = r.json().get("content", [])
ids = [i.get("educationLevelId") for i in items]
print(f"List IDs: {ids}")
print(f"Record {rid} in list: {rid in ids}")

# GET by ID
r = requests.get(f"{BASE}/api/education_levels/{rid}", headers=headers)
print(f"GET /{rid}: {r.status_code}")

# Try update first (uses same SecurityContextHolder pattern)
r = requests.put(f"{BASE}/api/education_levels/{rid}",
    json={"name": "Updated", "description": "updated", "sortorder": 2},
    headers=headers)
print(f"PUT /{rid}: {r.status_code}")

# Now delete
r = requests.delete(f"{BASE}/api/education_levels/{rid}", headers=headers)
print(f"DELETE /{rid}: {r.status_code} {r.text[:200]}")
