"""Test delete with verbose output."""
import requests

BASE = "http://localhost:8081"
r = requests.post(f"{BASE}/api/auth/login", json={"username": "gokul", "password": "password"})
token = r.json().get("token")
headers = {"Authorization": f"Bearer {token}"}

# Create
r = requests.post(f"{BASE}/api/education_levels",
    json={"name": "ToDelete", "description": "test", "sortorder": 1},
    headers=headers)
rid = r.json().get("educationLevelId")
print(f"Created: {rid}")

# Verify exists
r = requests.get(f"{BASE}/api/education_levels/{rid}", headers=headers)
print(f"GET /{rid}: {r.status_code}")

# Delete - check response carefully
r = requests.delete(f"{BASE}/api/education_levels/{rid}", headers=headers)
print(f"DELETE /{rid}: status={r.status_code}, headers={dict(r.headers)}")
print(f"Body: [{r.text}]")
