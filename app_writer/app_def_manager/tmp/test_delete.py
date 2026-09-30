"""Test delete endpoint."""
import requests

BASE = "http://localhost:8081"

# Login as gokul
r = requests.post(f"{BASE}/api/auth/login", json={"username": "gokul", "password": "password"})
token = r.json().get("token")
headers = {"Authorization": f"Bearer {token}"}

# List records
r = requests.get(f"{BASE}/api/education_levels", headers=headers)
print(f"GET: {r.status_code}")
data = r.json()
items = data.get("content", data) if isinstance(data, dict) else data
print(f"Records: {len(items) if isinstance(items, list) else 'unknown'}")

if isinstance(items, list) and len(items) > 0:
    record_id = items[0].get("educationLevelId")
    print(f"\nDeleting record {record_id}...")
    r = requests.delete(f"{BASE}/api/education_levels/{record_id}", headers=headers)
    print(f"DELETE: {r.status_code}")
    print(f"Response: {r.text[:300]}")
