"""Test login as gokul (SUPER_ADMIN) and check API access."""
import requests, json, base64

BASE = "http://localhost:8081"

# Login as gokul
r = requests.post(f"{BASE}/api/auth/login", json={"username": "gokul", "password": "Gokul@123"})
print(f"Login: {r.status_code}")
if r.status_code != 200:
    print(f"Error: {r.text[:200]}")
    # Try common passwords
    for pwd in ["Admin123!", "SuperAdmin123!", "password", "Gokul123!"]:
        r = requests.post(f"{BASE}/api/auth/login", json={"username": "gokul", "password": pwd})
        if r.status_code == 200:
            print(f"Password: {pwd}")
            break
        
if r.status_code == 200:
    data = r.json()
    token = data.get("token")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Decode JWT payload to see claims
    payload = token.split(".")[1]
    # Add padding
    payload += "=" * (4 - len(payload) % 4)
    decoded = json.loads(base64.b64decode(payload))
    print(f"\nJWT claims:")
    print(f"  sub: {decoded.get('sub')}")
    print(f"  roles: {decoded.get('roles')}")
    print(f"  tableAccess: {decoded.get('tableAccess')}")
    print(f"  queryGroupMemberships: {decoded.get('queryGroupMemberships')}")
    
    # Test API access
    r2 = requests.get(f"{BASE}/api/education_levels", headers=headers)
    print(f"\nGET /api/education_levels: {r2.status_code}")
    print(f"Response: {r2.text[:200]}")
    
    r3 = requests.post(f"{BASE}/api/education_levels",
        json={"name": "Bachelor", "description": "Bachelor degree", "sortorder": 1},
        headers=headers)
    print(f"\nPOST /api/education_levels: {r3.status_code}")
    print(f"Response: {r3.text[:200]}")
else:
    print("Could not login as gokul")
