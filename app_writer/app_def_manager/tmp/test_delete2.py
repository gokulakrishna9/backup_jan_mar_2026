"""Test create then delete."""
import requests

BASE = "http://localhost:8081"
r = requests.post(f"{BASE}/api/auth/login", json={"username": "gokul", "password": "password"})
token = r.json().get("token")
headers = {"Authorization": f"Bearer {token}"}

# Create
r = requests.post(f"{BASE}/api/education_levels",
    json={"name": "Test Delete", "description": "Will be deleted", "sortorder": 99},
    headers=headers)
print(f"Create: {r.status_code}")
record_id = r.json().get("educationLevelId")
print(f"Created ID: {record_id}")

# Delete
r = requests.delete(f"{BASE}/api/education_levels/{record_id}", headers=headers)
print(f"Delete: {r.status_code}")
print(f"Response: {r.text[:200] if r.text else '(empty)'}")

# Verify gone
r = requests.get(f"{BASE}/api/education_levels/{record_id}", headers=headers)
print(f"Get after delete: {r.status_code}")
