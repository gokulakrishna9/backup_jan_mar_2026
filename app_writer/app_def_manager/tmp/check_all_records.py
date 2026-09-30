"""Check record counts and test delete with existing record."""
import requests, mysql.connector

# Check DB
conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='password', database='job_portal')
cur = conn.cursor()
for table in ['education_level', 'record_owner', 'auth_user']:
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    print(f"  {table}: {cur.fetchone()[0]} rows")

cur.execute("SELECT * FROM education_level")
for row in cur.fetchall():
    print(f"  education_level row: {row}")
conn.close()

# Test delete via API
BASE = "http://localhost:8081"
r = requests.post(f"{BASE}/api/auth/login", json={"username": "gokul", "password": "password"})
token = r.json().get("token")
headers = {"Authorization": f"Bearer {token}"}

r = requests.get(f"{BASE}/api/education_levels", headers=headers)
data = r.json()
items = data.get("content", [])
print(f"\nAPI GET: {len(items)} records")
if items:
    rid = items[0].get("educationLevelId")
    print(f"Deleting ID {rid}...")
    r = requests.delete(f"{BASE}/api/education_levels/{rid}", headers=headers)
    print(f"DELETE: {r.status_code} {r.text[:200]}")
