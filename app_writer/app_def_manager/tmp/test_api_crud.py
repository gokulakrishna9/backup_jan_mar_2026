"""Test the backend API directly — create a record and fetch it back."""
import requests

BASE = "http://localhost:8081"

# 1. Login first to get a token
print("=== Login ===")
r = requests.post(f"{BASE}/api/auth/login", json={"username": "superadmin", "password": "SuperAdmin123!"})
print(f"Login: {r.status_code}")
if r.status_code != 200:
    # Try registering
    r = requests.post(f"{BASE}/api/auth/register", json={"username": "superadmin", "password": "SuperAdmin123!", "email": "super@test.com"})
    print(f"Register: {r.status_code} {r.text[:200]}")
    r = requests.post(f"{BASE}/api/auth/login", json={"username": "superadmin", "password": "SuperAdmin123!"})
    print(f"Login retry: {r.status_code}")

if r.status_code == 200:
    token = r.json().get("token")
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Token: {token[:30]}...")
else:
    print(f"Login failed: {r.text[:200]}")
    headers = {}
    token = None

# 2. Create an education level
print("\n=== Create ===")
r = requests.post(f"{BASE}/api/education_levels", 
    json={"name": "Bachelor", "description": "Bachelor's degree", "sortorder": 1},
    headers=headers)
print(f"Create: {r.status_code}")
print(f"Response: {r.text[:300]}")

# 3. Fetch all
print("\n=== Fetch All ===")
r = requests.get(f"{BASE}/api/education_levels", headers=headers)
print(f"Fetch: {r.status_code}")
print(f"Response: {r.text[:300]}")

# 4. Try without auth
print("\n=== Fetch without auth ===")
r = requests.get(f"{BASE}/api/education_levels")
print(f"No auth: {r.status_code}")
