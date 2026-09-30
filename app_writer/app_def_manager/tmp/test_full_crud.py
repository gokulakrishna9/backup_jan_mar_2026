"""Full CRUD test: create, get by ID, update, delete."""
import requests

BASE = "http://localhost:8081"
r = requests.post(f"{BASE}/api/auth/login", json={"username": "gokul", "password": "password"})
token = r.json().get("token")
headers = {"Authorization": f"Bearer {token}"}

# Create
print("=== CREATE ===")
r = requests.post(f"{BASE}/api/education_levels",
    json={"name": "Masters", "description": "Masters degree", "sortorder": 2},
    headers=headers)
print(f"POST: {r.status_code}")
data = r.json()
rid = data.get("educationLevelId")
print(f"Created ID: {rid}")

# Get by ID
print(f"\n=== GET BY ID ({rid}) ===")
r = requests.get(f"{BASE}/api/education_levels/{rid}", headers=headers)
print(f"GET /{rid}: {r.status_code}")
print(f"Response: {r.text[:200]}")

# Update
print(f"\n=== UPDATE ({rid}) ===")
r = requests.put(f"{BASE}/api/education_levels/{rid}",
    json={"name": "Masters Updated", "description": "Updated desc", "sortorder": 3},
    headers=headers)
print(f"PUT /{rid}: {r.status_code}")
print(f"Response: {r.text[:200]}")

# Delete
print(f"\n=== DELETE ({rid}) ===")
r = requests.delete(f"{BASE}/api/education_levels/{rid}", headers=headers)
print(f"DELETE /{rid}: {r.status_code}")
print(f"Response: {r.text[:200] if r.text else '(empty)'}")

# Verify gone
print(f"\n=== VERIFY DELETED ===")
r = requests.get(f"{BASE}/api/education_levels/{rid}", headers=headers)
print(f"GET /{rid}: {r.status_code}")
