"""Debug POST /setup — check exact 403 response."""
import requests

r = requests.post('http://localhost:8081/setup',
    data={
        'username': 'admin',
        'password': 'Admin123!',
        'email': 'admin@jobportal.com',
        'confirmPassword': 'Admin123!'
    },
    allow_redirects=False)
print(f"Status: {r.status_code}")
print(f"Headers: {dict(r.headers)}")
print(f"Body: [{r.text}]")
