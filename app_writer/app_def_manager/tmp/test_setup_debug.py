"""Debug /setup POST — check exact response."""
import requests

# Test GET first
r = requests.get('http://localhost:8081/setup')
print(f"GET /setup: {r.status_code}")

# Test POST with form data
r = requests.post('http://localhost:8081/setup',
    data={'username': 'admin', 'password': 'Admin123!', 'email': 'admin@jobportal.com', 'confirmPassword': 'Admin123!'},
    allow_redirects=False)
print(f"POST /setup (form): {r.status_code}")
print(f"Response headers: {dict(r.headers)}")
print(f"Body (first 300): {r.text[:300]}")

# Test POST with JSON
r2 = requests.post('http://localhost:8081/setup',
    json={'username': 'admin', 'password': 'Admin123!', 'email': 'admin@jobportal.com', 'confirmPassword': 'Admin123!'},
    allow_redirects=False)
print(f"\nPOST /setup (json): {r2.status_code}")
print(f"Body (first 300): {r2.text[:300]}")
