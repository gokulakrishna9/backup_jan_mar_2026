import requests
r = requests.get('http://localhost:8081/swagger-ui.html', allow_redirects=False)
print(f'Status: {r.status_code}')
print(f'Location: {r.headers.get("Location", "none")}')

r2 = requests.get('http://localhost:8081/swagger-ui.html')
print(f'\nFull redirect status: {r2.status_code}')
print(f'Final URL: {r2.url}')
print(f'Content length: {len(r2.text)}')
if r2.status_code == 200:
    print('Swagger UI is working!')
else:
    print(f'Error: {r2.text[:200]}')
