"""Test POST /setup with browser-like headers to reproduce the 403."""
import requests

# Mimic browser POST exactly
r = requests.post('http://localhost:8081/setup',
    data='username=superadmin&email=super%40jobportal.com&password=SuperAdmin123!&confirmPassword=SuperAdmin123!',
    headers={
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://localhost:8081',
        'Referer': 'http://localhost:8081/setup',
    },
    allow_redirects=False)
print(f"Status: {r.status_code}")
print(f"Location: {r.headers.get('Location', 'none')}")
print(f"Body: [{r.text[:200]}]")
