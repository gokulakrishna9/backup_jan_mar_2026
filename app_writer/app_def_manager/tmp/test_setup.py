import requests

# Test POST /setup
r = requests.post('http://localhost:8081/setup',
    data={'username': 'admin', 'password': 'Admin123!', 'email': 'admin@jobportal.com'},
    allow_redirects=False)
print(f'Status: {r.status_code}')
print(f'Location: {r.headers.get("Location", "none")}')
print(f'Body: {r.text[:500]}')
