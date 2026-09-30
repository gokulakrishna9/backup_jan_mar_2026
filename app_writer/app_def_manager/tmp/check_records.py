"""Check what records exist in education_level."""
import mysql.connector
conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='password', database='job_portal')
cur = conn.cursor()
cur.execute("SELECT * FROM education_level")
for row in cur.fetchall():
    print(row)
print(f"Total: {cur.rowcount}")
conn.close()
