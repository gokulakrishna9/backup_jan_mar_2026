"""Test GET by ID."""
import requests
BASE = "http://localhost:8081"
r = requests.post(f"{BASE}/api/auth/login", json={"username": "gokul", "password": "password"})
token = r.json().get("token")
headers = {"Authorization": f"Bearer {token}"}

r = requests.get(f"{BASE}/api/education_levels/4", headers=headers)
print(f"GET /4: {r.status_code} {r.text[:200]}")
